<script setup lang="ts">
import type { BackendError } from '~/types'

import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { computed, ref } from 'vue'

import axios from 'axios'

import DomainsTable from '~/components/manage/moderation/DomainsTable.vue'

interface Props {
  allowListEnabled: boolean
}

const props = defineProps<Props>()

const { t } = useI18n()

const router = useRouter()

const labels = computed(() => ({
  domains: t('views.admin.moderation.DomainsList.title')
}))

const domainName = ref('')
const domainAllowed = ref(props.allowListEnabled || undefined)

const isCreating = ref(false)
const errors = ref([] as string[])
const createDomain = async () => {
  isCreating.value = true
  errors.value = []

  try {
    const response = await axios.post('manage/federation/domains/', { name: domainName.value, allowed: domainAllowed.value })
    router.push({
      name: 'manage.moderation.domains.detail',
      params: { id: response.data.name }
    })
  } catch (error) {
    errors.value = (error as BackendError).backendErrors
  }

  isCreating.value = false
}
</script>

<template>
  <main v-title="labels.domains">
    <section class="ui vertical stripe segment">
      <h2 class="ui left floated header">
        {{ $t('views.admin.moderation.DomainsList.header.domains') }}
      </h2>
      <form
        class="ui right floated form"
        @submit.prevent="createDomain"
      >
        <div
          v-if="errors && errors.length > 0"
          role="alert"
          class="ui negative message"
        >
          <h4 class="header">
            {{ $t('views.admin.moderation.DomainsList.header.failure') }}
          </h4>
          <ul class="list">
            <li
              v-for="(error, key) in errors"
              :key="key"
            >
              {{ error }}
            </li>
          </ul>
        </div>
        <div class="inline fields">
          <div class="field">
            <label for="add-domain">{{ $t('views.admin.moderation.DomainsList.label.addDomain') }}</label>
            <input
              id="add-domain"
              v-model="domainName"
              type="text"
              name="domain"
            >
          </div>
          <div
            v-if="allowListEnabled"
            class="field"
          >
            <input
              id="allowed"
              v-model="domainAllowed"
              type="checkbox"
              name="allowed"
            >
            <label for="allowed">{{ $t('views.admin.moderation.DomainsList.label.addToAllowList') }}</label>
          </div>
          <div class="field">
            <button
              :class="['ui', {'loading': isCreating}, 'success', 'button']"
              type="submit"
              :disabled="isCreating"
            >
              {{ $t('views.admin.moderation.DomainsList.button.add') }}
            </button>
          </div>
        </div>
      </form>
      <div class="ui clearing hidden divider" />
      <domains-table :allow-list-enabled="allowListEnabled" />
    </section>
  </main>
</template>
