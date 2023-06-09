<script setup lang="ts">
import type { ConfigField } from '~/composables/moderation/useEditConfigs'
import type { Review, ReviewState, ReviewStatePayload } from '~/types'
import type { Change } from 'diff'

import { diffWordsWithSpace } from 'diff'
import { useRouter } from 'vue-router'
import { computed, ref } from 'vue'
import { useStore } from '~/store'

import axios from 'axios'

import useEditConfigs from '~/composables/moderation/useEditConfigs'
import useErrorHandler from '~/composables/useErrorHandler'

interface Events {
  (e: 'approved', isApproved: boolean): void
  (e: 'deleted'): void
}

interface Props {
  obj: Review
  currentState?: ReviewState
}

const emit = defineEmits<Events>()
const props = withDefaults(defineProps<Props>(), {
  currentState: () => ({})
})

const configs = useEditConfigs()
const router = useRouter()
const store = useStore()

const canApprove = computed(() => !props.obj.is_applied && store.state.auth.availablePermissions.library)
const canDelete = computed(() => {
  if (props.obj.is_applied || props.obj.is_approved) return false
  if (!store.state.auth.authenticated) return false

  return props.obj.created_by.full_username === store.state.auth.fullUsername
    || store.state.auth.availablePermissions.library
})

const previousState = computed(() => props.obj.is_applied
  // mutation was applied, we use the previous state that is stored
  // on the mutation itself
  ? props.obj.previous_state
  // mutation is not applied yet, so we use the current state that was
  // passed to the component, if any
  : props.currentState
)

const detailUrl = computed(() => {
  if (!props.obj.target) return ''

  const name = props.obj.target.type === 'track'
    ? 'library.tracks.edit.detail'
    : props.obj.target.type === 'album'
      ? 'library.albums.edit.detail'
      : props.obj.target.type === 'artist'
        ? 'library.artists.edit.detail'
        : undefined

  return router.resolve({
    name,
    params: {
      id: props.obj.target.id,
      editId: props.obj.uuid
    }
  }).href
})

const updatedFields = computed(() => {
  if (!props.obj?.target) return []

  const payload = props.obj.payload
  const fields = Object.keys(payload)

  const state = previousState.value

  return fields.map((id) => {
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const config = configs[props.obj.target!.type].fields.find((field) => id === field.id)
    const getValueRepr = config?.getValueRepr ?? (v => v)

    const result = {
      id,
      config,
      new: payload[id],
      newRepr: getValueRepr(payload[id]) ?? '',
      old: undefined,
      oldRepr: '',
      diff: []
    } as {
      id: string
      config: ConfigField
      old?: ReviewStatePayload
      new: ReviewStatePayload
      oldRepr: string
      newRepr: string
      diff: Change[]
    }

    if (state?.[id]) {
      const oldState = state[id]
      result.old = oldState
      result.oldRepr = getValueRepr('value' in oldState
        ? oldState.value
        : oldState
      ) ?? ''

      // we compute the diffs between the old and new values
      result.diff = diffWordsWithSpace(result.oldRepr, result.newRepr)
    }

    return result
  })
})

const isLoading = ref(false)
const remove = async () => {
  isLoading.value = true

  try {
    await axios.delete(`mutations/${props.obj.uuid}/`)
    emit('deleted')
  } catch (error) {
    useErrorHandler(error as Error)
  }

  isLoading.value = false
}

const approve = async (approved: boolean) => {
  const url = approved
    ? `mutations/${props.obj.uuid}/approve/`
    : `mutations/${props.obj.uuid}/reject/`

  isLoading.value = true

  try {
    await axios.post(url)
    emit('approved', approved)
    store.commit('ui/incrementNotifications', { count: -1, type: 'pendingReviewEdits' })
  } catch (error) {
    useErrorHandler(error as Error)
  }

  isLoading.value = false
}
</script>

<template>
  <div class="ui fluid card">
    <div class="content">
      <h4 class="header">
        <router-link :to="detailUrl">
          {{ $t('components.library.EditCard.header.modification', {id: obj.uuid.substring(0, 8)}) }}
        </router-link>
      </h4>
      <div class="meta">
        <router-link
          v-if="obj.target && obj.target.type === 'track'"
          :to="{name: 'library.tracks.detail', params: {id: obj.target.id }}"
        >
          <i class="music icon" />
          {{ $t('components.library.EditCard.link.track', {id: obj.target.id, name: obj.target.repr}) }}
        </router-link>
        <br>
        <human-date
          :date="obj.creation_date"
          :icon="true"
        />

        <span class="right floated">
          <span v-if="obj.is_approved && obj.is_applied">
            <i class="success check icon" />
            {{ $t('components.library.EditCard.status.applied') }}
          </span>
          <span v-else-if="obj.is_approved">
            <i class="success check icon" />
            {{ $t('components.library.EditCard.status.approved') }}
          </span>
          <span v-else-if="obj.is_approved === null">
            <i class="warning hourglass icon" />
            {{ $t('components.library.EditCard.status.pending') }}
          </span>
          <span v-else-if="obj.is_approved === false">
            <i class="danger x icon" />
            {{ $t('components.library.EditCard.status.rejected') }}
          </span>
        </span>
      </div>
    </div>
    <div
      v-if="obj.summary"
      class="content"
    >
      {{ obj.summary }}
    </div>
    <div class="content">
      <table
        v-if="obj.type === 'update'"
        class="ui celled very basic fixed stacking table"
      >
        <thead>
          <tr>
            <th>
              {{ $t('components.library.EditCard.table.update.header.field') }}
            </th>
            <th>
              {{ $t('components.library.EditCard.table.update.header.oldValue') }}
            </th>
            <th>
              {{ $t('components.library.EditCard.table.update.header.newValue') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="field in updatedFields"
            :key="field.id"
          >
            <td>{{ field.id }}</td>

            <td v-if="field.diff">
              <template v-if="field.config?.type === 'attachment' && field.oldRepr">
                <img
                  class="ui image"
                  alt=""
                  :src="$store.getters['instance/absoluteUrl'](`api/v1/attachments/${field.oldRepr}/proxy?next=medium_square_crop`)"
                >
              </template>
              <template v-else>
                <span
                  v-for="(part, key) in field.diff.filter(p => !p.added)"
                  :key="key"
                  :class="['diff', {removed: part.removed}]"
                >
                  {{ part.value }}
                </span>
              </template>
            </td>
            <td v-else>
              {{ $t('components.library.EditCard.table.update.notApplicable') }}
            </td>

            <td
              v-if="field.diff"
              :title="field.newRepr"
            >
              <template v-if="field.config?.type === 'attachment' && field.newRepr">
                <img
                  class="ui image"
                  alt=""
                  :src="$store.getters['instance/absoluteUrl'](`api/v1/attachments/${field.newRepr}/proxy?next=medium_square_crop`)"
                >
              </template>
              <template v-else>
                <span
                  v-for="(part, key) in field.diff.filter(p => !p.removed)"
                  :key="key"
                  :class="['diff', {added: part.added}]"
                >
                  {{ part.value }}
                </span>
              </template>
            </td>
            <td
              v-else
              :title="field.newRepr"
            >
              <template v-if="field.config?.type === 'attachment' && field.newRepr">
                <img
                  class="ui image"
                  alt=""
                  :src="$store.getters['instance/absoluteUrl'](`api/v1/attachments/${field.newRepr}/proxy?next=medium_square_crop`)"
                >
              </template>
              <template v-else>
                {{ field.newRepr }}
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div
      v-if="obj.created_by"
      class="extra content"
    >
      <actor-link :actor="obj.created_by" />
    </div>
    <div
      v-if="canDelete || canApprove"
      class="ui bottom attached buttons"
    >
      <button
        v-if="canApprove && obj.is_approved !== true"
        :class="['ui', {loading: isLoading}, 'success', 'basic', 'button']"
        @click="approve(true)"
      >
        {{ $t('components.library.EditCard.button.approve') }}
      </button>
      <button
        v-if="canApprove && obj.is_approved === null"
        :class="['ui', {loading: isLoading}, 'warning', 'basic', 'button']"
        @click="approve(false)"
      >
        {{ $t('components.library.EditCard.button.reject') }}
      </button>
      <dangerous-button
        v-if="canDelete"
        :class="['ui', {loading: isLoading}, 'basic danger button']"
        :action="remove"
      >
        {{ $t('components.library.EditCard.button.delete') }}
        <template #modal-header>
          <p>
            {{ $t('components.library.EditCard.modal.delete.header') }}
          </p>
        </template>
        <template #modal-content>
          <div>
            <p>
              {{ $t('components.library.EditCard.modal.content.warning') }}
            </p>
          </div>
        </template>
        <template #modal-confirm>
          <p>
            {{ $t('components.library.EditCard.button.delete') }}
          </p>
        </template>
      </dangerous-button>
    </div>
  </div>
</template>
