<script setup lang="ts">
import type { Album } from '~/types'

import PlayButton from '~/components/audio/PlayButton.vue'
import { computed } from 'vue'

interface Props {
  serie: Album
}

const props = defineProps<Props>()

const cover = computed(() => props.serie?.cover ?? null)
</script>

<template>
  <div class="channel-serie-card">
    <div class="two-images">
      <img
        v-if="cover && cover.urls.original"
        v-lazy="$store.getters['instance/absoluteUrl'](cover.urls.medium_square_crop)"
        alt=""
        class="channel-image"
        @click="$router.push({name: 'library.albums.detail', params: {id: serie.id}})"
      >
      <img
        v-else
        alt=""
        class="channel-image"
        src="../../assets/audio/default-cover.png"
        @click="$router.push({name: 'library.albums.detail', params: {id: serie.id}})"
      >
      <img
        v-if="cover && cover.urls.original"
        v-lazy="$store.getters['instance/absoluteUrl'](cover.urls.medium_square_crop)"
        alt=""
        class="channel-image"
        @click="$router.push({name: 'library.albums.detail', params: {id: serie.id}})"
      >
      <img
        v-else
        alt=""
        class="channel-image"
        src="../../assets/audio/default-cover.png"
        @click="$router.push({name: 'library.albums.detail', params: {id: serie.id}})"
      >
    </div>
    <div class="content ellipsis">
      <strong>
        <router-link
          class="discrete link"
          :to="{name: 'library.albums.detail', params: {id: serie.id}}"
        >
          {{ serie.title }}
        </router-link>
      </strong>
      <div class="description">
        <span>
          {{ $t('components.audio.ChannelSerieCard.meta.episodes', serie.tracks_count) }}
        </span>
      </div>
    </div>
    <div class="controls">
      <play-button
        :icon-only="true"
        :is-playable="true"
        :button-classes="['ui', 'circular', 'vibrant', 'icon', 'button']"
        :album="serie"
      />
    </div>
  </div>
</template>
