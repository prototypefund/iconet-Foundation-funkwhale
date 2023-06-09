<script setup lang="ts">
import type { SmartSearchProps } from '~/composables/navigation/useSmartSearch'
import type { OrderingProps } from '~/composables/navigation/useOrdering'
import type { RouteRecordName } from 'vue-router'
import type { OrderingField } from '~/store/ui'

import { computed, ref, watch } from 'vue'
import { truncate } from '~/utils/filters'
import { useI18n } from 'vue-i18n'

import axios from 'axios'

import ImportStatusModal from '~/components/library/ImportStatusModal.vue'
import ActionTable from '~/components/common/ActionTable.vue'
import Pagination from '~/components/vui/Pagination.vue'

import useSharedLabels from '~/composables/locale/useSharedLabels'
import useSmartSearch from '~/composables/navigation/useSmartSearch'
import useOrdering from '~/composables/navigation/useOrdering'
import useErrorHandler from '~/composables/useErrorHandler'
import usePage from '~/composables/navigation/usePage'

interface Props extends SmartSearchProps, OrderingProps {
  filters?: object

  // TODO(wvffle): Remove after https://github.com/vuejs/core/pull/4512 is merged
  orderingConfigName?: RouteRecordName
  defaultQuery?: string
  updateUrl?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  defaultQuery: '',
  updateUrl: false,
  filters: () => ({}),
  orderingConfigName: undefined
})

const search = ref()

const page = usePage()
type ResponseType = { count: number, results: any[] }
const result = ref<null | ResponseType>(null)

const { onSearch, query } = useSmartSearch(props)
const { onOrderingUpdate, orderingString, paginateBy, ordering, orderingDirection } = useOrdering(props)

const orderingOptions: [OrderingField, keyof typeof sharedLabels.filters][] = [
  ['creation_date', 'creation_date'],
  ['name', 'name'],
  ['length', 'length'],
  ['items_count', 'items_count']
]

const { t } = useI18n()
const actionFilters = computed(() => ({ q: query.value, ...props.filters }))
const actions = computed(() => [
  {
    name: 'delete',
    label: t('components.manage.library.TagsTable.action.delete.label'),
    confirmationMessage: t('components.manage.library.TagsTable.action.delete.warning'),
    isDangerous: true,
    allowAll: false,
    confirmColor: 'danger'
  }
])

const isLoading = ref(false)
const fetchData = async () => {
  isLoading.value = true
  const params = {
    page: page.value,
    page_size: paginateBy.value,
    q: query.value,
    ordering: orderingString.value,
    ...props.filters
  }

  try {
    const response = await axios.get('/manage/tags/', {
      params
    })

    result.value = response.data
  } catch (error) {
    useErrorHandler(error as Error)
    result.value = null
  } finally {
    isLoading.value = false
  }
}

onSearch(() => (page.value = 1))
watch(page, fetchData)
onOrderingUpdate(fetchData)
fetchData()

const sharedLabels = useSharedLabels()
const labels = computed(() => ({
  searchPlaceholder: t('components.manage.library.TagsTable.placeholder.search')
}))

const detailedUpload = ref()
const showUploadDetailModal = ref(false)
</script>

<template>
  <div>
    <div class="ui inline form">
      <div class="fields">
        <div class="ui six wide field">
          <label for="tags-search">{{ $t('components.manage.library.TagsTable.label.search') }}</label>
          <form @submit.prevent="query = search.value">
            <input
              id="tags-search"
              ref="search"
              name="search"
              type="text"
              :value="query"
              :placeholder="labels.searchPlaceholder"
            >
          </form>
        </div>
        <div class="field">
          <label for="tags-ordering">{{ $t('components.manage.library.TagsTable.ordering.label') }}</label>
          <select
            id="tags-ordering"
            v-model="ordering"
            class="ui dropdown"
          >
            <option
              v-for="(option, key) in orderingOptions"
              :key="key"
              :value="option[0]"
            >
              {{ sharedLabels.filters[option[1]] }}
            </option>
          </select>
        </div>
        <div class="field">
          <label for="tags-ordering-direction">{{ $t('components.manage.library.TagsTable.ordering.direction.label') }}</label>
          <select
            id="tags-ordering-direction"
            v-model="orderingDirection"
            class="ui dropdown"
          >
            <option value="+">
              {{ $t('components.manage.library.TagsTable.ordering.direction.ascending') }}
            </option>
            <option value="-">
              {{ $t('components.manage.library.TagsTable.ordering.direction.descending') }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <import-status-modal
      v-if="detailedUpload"
      v-model:show="showUploadDetailModal"
      :upload="detailedUpload"
    />
    <div class="dimmable">
      <div
        v-if="isLoading"
        class="ui active inverted dimmer"
      >
        <div class="ui loader" />
      </div>
      <action-table
        v-if="result"
        :objects-data="result"
        :actions="actions"
        action-url="manage/tags/action/"
        id-field="name"
        :filters="actionFilters"
        @action-launched="fetchData"
      >
        <template #header-cells>
          <th>
            {{ $t('components.manage.library.TagsTable.table.tag.header.name') }}
          </th>
          <th>
            {{ $t('components.manage.library.TagsTable.table.tag.header.artists') }}
          </th>
          <th>
            {{ $t('components.manage.library.TagsTable.table.tag.header.albums') }}
          </th>
          <th>
            {{ $t('components.manage.library.TagsTable.table.tag.header.tracks') }}
          </th>
          <th>
            {{ $t('components.manage.library.TagsTable.table.tag.header.creationDate') }}
          </th>
        </template>
        <template
          #row-cells="scope"
        >
          <td>
            <router-link :to="{name: 'manage.library.tags.detail', params: {id: scope.obj.name }}">
              {{ truncate(scope.obj.name, 30, undefined, true) }}
            </router-link>
          </td>
          <td>
            {{ scope.obj.artists_count }}
          </td>
          <td>
            {{ scope.obj.albums_count }}
          </td>
          <td>
            {{ scope.obj.tracks_count }}
          </td>
          <td>
            <human-date :date="scope.obj.creation_date" />
          </td>
        </template>
      </action-table>
    </div>
    <div>
      <pagination
        v-if="result && result.count > paginateBy"
        v-model:current="page"
        :compact="true"
        :paginate-by="paginateBy"
        :total="result.count"
      />

      <span v-if="result && result.results.length > 0">
        {{ $t('components.manage.library.TagsTable.pagination.results', {start: ((page-1) * paginateBy) + 1, end: ((page-1) * paginateBy) + result.results.length, total: result.count}) }}
      </span>
    </div>
  </div>
</template>
