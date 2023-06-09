<script setup lang="ts">
import type { Actor } from '~/types'

import { onBeforeRouteUpdate } from 'vue-router'
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from '~/store'

import axios from 'axios'

import useErrorHandler from '~/composables/useErrorHandler'
import useReport from '~/composables/moderation/useReport'

interface Events {
  (e: 'updated', value: Actor): void
}

interface Props {
  username: string
  domain?: string | null
}

const emit = defineEmits<Events>()
const props = withDefaults(defineProps<Props>(), {
  domain: null
})

const { report, getReportableObjects } = useReport()
const store = useStore()

const object = ref<Actor | null>(null)

const displayName = computed(() => object.value?.name ?? object.value?.preferred_username)
const fullUsername = computed(() => props.domain
  ? `${props.username}@${props.domain}`
  : `${props.username}@${store.getters['instance/domain']}`
)

const routerParams = computed(() => props.domain
  ? { username: props.username, domain: props.domain }
  : { username: props.username }
)

const { t } = useI18n()
const labels = computed(() => ({
  usernameProfile: t('views.auth.ProfileBase.title', { username: props.username })
}))

onBeforeRouteUpdate((to) => {
  to.meta.preserveScrollPosition = true
})

const isLoading = ref(false)
const fetchData = async () => {
  object.value = null
  isLoading.value = true

  try {
    const response = await axios.get(`federation/actors/${fullUsername.value}/`)
    object.value = response.data
  } catch (error) {
    useErrorHandler(error as Error)
  }

  isLoading.value = false
}

watch(props, fetchData, { immediate: true })
</script>

<template>
  <main
    v-title="labels.usernameProfile"
    class="main pusher page-profile"
  >
    <div
      v-if="isLoading"
      class="ui vertical segment"
    >
      <div class="ui centered active inline loader" />
    </div>
    <div class="ui head vertical stripe segment container">
      <div
        v-if="object"
        class="ui stackable grid"
      >
        <div class="ui five wide column">
          <button
            ref="dropdown"
            v-dropdown="{direction: 'downward'}"
            class="ui pointing dropdown icon small basic right floated button"
            style="position: absolute; right: 1em; top: 1em;"
          >
            <i class="ellipsis vertical icon" />
            <div class="menu">
              <a
                v-if="object.domain != $store.getters['instance/domain']"
                :href="object.fid"
                target="_blank"
                class="basic item"
              >
                <i class="external icon" />
                {{ $t('views.auth.ProfileBase.link.domainView', {domain: object.domain}) }}
              </a>
              <div
                v-for="obj in getReportableObjects({account: object})"
                :key="obj.target.type + obj.target.id"
                role="button"
                class="basic item"
                @click.stop.prevent="report(obj)"
              >
                <i class="share icon" /> {{ obj.label }}
              </div>

              <div class="divider" />
              <router-link
                v-if="$store.state.auth.availablePermissions['moderation']"
                class="basic item"
                :to="{name: 'manage.moderation.accounts.detail', params: {id: object.full_username}}"
              >
                <i class="wrench icon" />
                {{ $t('views.auth.ProfileBase.link.moderation') }}
              </router-link>
            </div>
          </button>
          <h1 class="ui center aligned icon header">
            <i
              v-if="!object.icon"
              class="circular inverted user success icon"
            />
            <img
              v-else
              v-lazy="$store.getters['instance/absoluteUrl'](object.icon.urls.medium_square_crop)"
              alt=""
              class="ui big circular image"
            >
            <div class="ellispsis content">
              <div class="ui very small hidden divider" />
              <span>{{ displayName }}</span>
              <div class="ui very small hidden divider" />
              <div
                class="sub header ellipsis"
                :title="object.full_username"
              >
                {{ object.full_username }}
              </div>
            </div>
            <template v-if="object.full_username === $store.state.auth.fullUsername">
              <div class="ui very small hidden divider" />
              <div class="ui basic success label">
                {{ $t('views.auth.ProfileBase.label.self') }}
              </div>
            </template>
          </h1>
          <div class="ui small hidden divider" />
          <div v-if="$store.getters['ui/layoutVersion'] === 'large'">
            <rendered-description
              :content="object.summary"
              :field-name="'summary'"
              :update-url="`users/${$store.state.auth.username}/`"
              :can-update="$store.state.auth.authenticated && object.full_username === $store.state.auth.fullUsername"
              @updated="emit('updated', $event)"
            />
          </div>
        </div>
        <div class="ui eleven wide column">
          <div class="ui head vertical stripe segment">
            <div class="ui container">
              <div class="ui secondary pointing center aligned menu">
                <router-link
                  class="item"
                  :to="{name: 'profile.overview', params: routerParams}"
                >
                  {{ $t('views.auth.ProfileBase.link.overview') }}
                </router-link>
                <router-link
                  class="item"
                  :to="{name: 'profile.activity', params: routerParams}"
                >
                  {{ $t('views.auth.ProfileBase.link.activity') }}
                </router-link>
              </div>
              <div class="ui hidden divider" />
              <router-view
                :object="object"
                @updated="fetchData"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
