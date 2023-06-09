<script setup lang="ts">
import type { Track, Album, Artist, Library } from '~/types'

import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { getDomain } from '~/utils'
import { useStore } from '~/store'

import axios from 'axios'

import EmbedWizard from '~/components/audio/EmbedWizard.vue'
import SemanticModal from '~/components/semantic/Modal.vue'
import PlayButton from '~/components/audio/PlayButton.vue'
import RadioButton from '~/components/radios/Button.vue'
import TagsList from '~/components/tags/List.vue'

import useReport from '~/composables/moderation/useReport'
import useLogger from '~/composables/useLogger'

interface Props {
  id: number
}

const props = defineProps<Props>()
const { report, getReportableObjects } = useReport()

const object = ref<Artist | null>(null)
const libraries = ref([] as Library[])
const albums = ref([] as Album[])
const tracks = ref([] as Track[])
const showEmbedModal = ref(false)

const nextAlbumsUrl = ref(null)
const nextTracksUrl = ref(null)
const totalAlbums = ref(0)
const totalTracks = ref(0)

const dropdown = ref()

const logger = useLogger()
const store = useStore()
const router = useRouter()

const domain = computed(() => getDomain(object.value?.fid ?? ''))
const isPlayable = computed(() => !!object.value?.albums.some(album => album.is_playable))
const wikipediaUrl = computed(() => `https://en.wikipedia.org/w/index.php?search=${encodeURI(object.value?.name ?? '')}`)
const musicbrainzUrl = computed(() => object.value?.mbid ? `https://musicbrainz.org/artist/${object.value.mbid}` : null)
const discogsUrl = computed(() => `https://discogs.com/search/?type=artist&title=${encodeURI(object.value?.name ?? '')}`)
const publicLibraries = computed(() => libraries.value?.filter(library => library.privacy_level === 'everyone') ?? [])
const cover = computed(() => object.value?.cover?.urls.original
  ? object.value.cover
  : object.value?.albums.find(album => album.cover?.urls.original)?.cover
)
const headerStyle = computed(() => cover.value?.urls.original
  ? { backgroundImage: `url(${store.getters['instance/absoluteUrl'](cover.value.urls.original)})` }
  : ''
)

const { t } = useI18n()
const labels = computed(() => ({
  title: t('components.library.ArtistBase.title')
}))

const isLoading = ref(false)
const fetchData = async () => {
  isLoading.value = true
  logger.debug(`Fetching artist "${props.id}"`)

  const artistsResponse = await axios.get(`artists/${props.id}/`, { params: { refresh: 'true' } })
  if (artistsResponse.data.channel) {
    return router.replace({ name: 'channels.detail', params: { id: artistsResponse.data.channel.uuid } })
  }

  object.value = artistsResponse.data

  const [tracksResponse, albumsResponse] = await Promise.all([
    axios.get('tracks/', { params: { artist: props.id, hidden: '', ordering: '-creation_date' } }),
    axios.get('albums/', { params: { artist: props.id, hidden: '', ordering: '-release_date' } })
  ])

  tracks.value = tracksResponse.data.results
  nextTracksUrl.value = tracksResponse.data.next
  totalTracks.value = tracksResponse.data.count

  nextAlbumsUrl.value = albumsResponse.data.next
  totalAlbums.value = albumsResponse.data.count

  albums.value = albumsResponse.data.results

  isLoading.value = false
}

watch(() => props.id, fetchData, { immediate: true })
</script>

<template>
  <main v-title="labels.title">
    <div
      v-if="isLoading"
      class="ui vertical segment"
    >
      <div :class="['ui', 'centered', 'active', 'inline', 'loader']" />
    </div>
    <template v-if="object && !isLoading">
      <section
        v-title="object.name"
        :class="['ui', 'head', {'with-background': cover}, 'vertical', 'center', 'aligned', 'stripe', 'segment']"
        :style="headerStyle"
      >
        <div class="segment-content">
          <h2 class="ui center aligned icon header">
            <i class="circular inverted users violet icon" />
            <div class="content">
              {{ object.name }}
              <div
                v-if="albums"
                class="sub header"
              >
                {{ $t('components.library.ArtistBase.meta.tracks', totalTracks) }}
                {{ $t('components.library.ArtistBase.meta.albums', totalAlbums) }}
              </div>
            </div>
          </h2>
          <tags-list
            v-if="object.tags && object.tags.length > 0"
            :tags="object.tags"
          />
          <div class="ui hidden divider" />
          <div class="header-buttons">
            <div class="ui buttons">
              <radio-button
                type="artist"
                :object-id="object.id"
              />
            </div>
            <div class="ui buttons">
              <play-button
                :is-playable="isPlayable"
                class="vibrant"
                :artist="object"
              >
                {{ $t('components.library.ArtistBase.button.play') }}
              </play-button>
            </div>

            <semantic-modal
              v-if="publicLibraries.length > 0"
              v-model:show="showEmbedModal"
            >
              <h4 class="header">
                {{ $t('components.library.ArtistBase.modal.embed.header') }}
              </h4>
              <div class="scrolling content">
                <div class="description">
                  <embed-wizard
                    :id="object.id"
                    type="artist"
                  />
                </div>
              </div>
              <div class="actions">
                <button class="ui deny button">
                  {{ $t('components.library.ArtistBase.button.cancel') }}
                </button>
              </div>
            </semantic-modal>
            <div class="ui buttons">
              <button
                class="ui button"
                @click="dropdown.click()"
              >
                {{ $t('components.library.ArtistBase.button.more') }}
              </button>
              <button
                ref="dropdown"
                v-dropdown
                class="ui floating dropdown icon button"
              >
                <i class="dropdown icon" />
                <div class="menu">
                  <a
                    v-if="domain != $store.getters['instance/domain']"
                    :href="object.fid"
                    target="_blank"
                    class="basic item"
                  >
                    <i class="external icon" />
                    {{ $t('components.library.ArtistBase.link.domain', {domain: domain}) }}
                  </a>

                  <button
                    v-if="publicLibraries.length > 0"
                    role="button"
                    class="basic item"
                    @click.prevent="showEmbedModal = !showEmbedModal"
                  >
                    <i class="code icon" />
                    {{ $t('components.library.ArtistBase.button.embed') }}
                  </button>
                  <a
                    :href="wikipediaUrl"
                    target="_blank"
                    rel="noreferrer noopener"
                    class="basic item"
                  >
                    <i class="wikipedia w icon" />
                    {{ $t('components.library.ArtistBase.link.wikipedia') }}
                  </a>
                  <a
                    v-if="musicbrainzUrl"
                    :href="musicbrainzUrl"
                    target="_blank"
                    rel="noreferrer noopener"
                    class="basic item"
                  >
                    <i class="external icon" />
                    {{ $t('components.library.ArtistBase.link.musicbrainz') }}
                  </a>
                  <a
                    :href="discogsUrl"
                    target="_blank"
                    rel="noreferrer noopener"
                    class="basic item"
                  >
                    <i class="external icon" />
                    {{ $t('components.library.ArtistBase.link.discogs') }}
                  </a>
                  <router-link
                    v-if="object.is_local"
                    :to="{name: 'library.artists.edit', params: {id: object.id }}"
                    class="basic item"
                  >
                    <i class="edit icon" />
                    {{ $t('components.library.ArtistBase.button.edit') }}
                  </router-link>
                  <div class="divider" />
                  <div
                    v-for="obj in getReportableObjects({artist: object})"
                    :key="obj.target.type + obj.target.id"
                    role="button"
                    class="basic item"
                    @click.stop.prevent="report(obj)"
                  >
                    <i class="share icon" /> {{ obj.label }}
                  </div>

                  <div class="divider" />
                  <router-link
                    v-if="$store.state.auth.availablePermissions['library']"
                    class="basic item"
                    :to="{name: 'manage.library.artists.detail', params: {id: object.id}}"
                  >
                    <i class="wrench icon" />
                    {{ $t('components.library.ArtistBase.link.moderation') }}
                  </router-link>
                  <a
                    v-if="$store.state.auth.profile && $store.state.auth.profile.is_superuser"
                    class="basic item"
                    :href="$store.getters['instance/absoluteUrl'](`/api/admin/music/artist/${object.id}`)"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <i class="wrench icon" />
                    {{ $t('components.library.ArtistBase.link.django') }}
                  </a>
                </div>
              </button>
            </div>
          </div>
        </div>
      </section>
      <router-view
        :key="$route.fullPath"
        :tracks="tracks"
        :next-tracks-url="nextTracksUrl"
        :next-albums-url="nextAlbumsUrl"
        :albums="albums"
        :is-loading-albums="isLoading"
        :object="object"
        object-type="artist"
        @libraries-loaded="libraries = $event"
      />
    </template>
  </main>
</template>
