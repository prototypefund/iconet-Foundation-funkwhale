<script setup lang="ts">
import { computed } from 'vue'

import ChannelsWidget from '~/components/audio/ChannelsWidget.vue'
import TrackWidget from '~/components/audio/track/Widget.vue'
import AlbumWidget from '~/components/audio/album/Widget.vue'
import ArtistWidget from '~/components/audio/artist/Widget.vue'
import RadioButton from '~/components/radios/Button.vue'

interface Props {
  id: string
}

const props = defineProps<Props>()

const labels = computed(() => ({
  title: `#${props.id}`
}))
</script>

<template>
  <main v-title="labels.title">
    <section class="ui vertical stripe segment">
      <h2 class="ui header">
        <span class="ui circular huge hashtag label component-label">
          {{ labels.title }}
        </span>
      </h2>
      <radio-button
        type="tag"
        :object-id="id"
      />
      <router-link
        v-if="$store.state.auth.availablePermissions['library']"
        class="ui right floated button"
        :to="{name: 'manage.library.tags.detail', params: {id: id}}"
      >
        <i class="wrench icon" />
        {{ $t('components.library.TagDetail.link.moderation') }}
      </router-link>

      <div class="ui hidden divider" />
      <div class="ui row">
        <artist-widget
          :key="'artist' + id"
          :controls="false"
          :filters="{playable: true, ordering: '-creation_date', tag: id, include_channels: 'false'}"
        >
          <template #title>
            <router-link :to="{name: 'library.artists.browse', query: {tag: id}}">
              {{ $t('components.library.TagDetail.link.artists') }}
            </router-link>
          </template>
        </artist-widget>
        <div class="ui hidden divider" />
        <div class="ui hidden divider" />
        <h3 class="ui header">
          {{ $t('components.library.TagDetail.header.channels') }}
        </h3>
        <channels-widget
          :key="'channels' + id"
          :show-modification-date="true"
          :limit="12"
          :filters="{tag: id, ordering: '-creation_date'}"
        />
        <div class="ui hidden divider" />
        <div class="ui hidden divider" />
        <album-widget
          :key="'album' + id"
          :show-count="true"
          :controls="false"
          :filters="{playable: true, ordering: '-creation_date', tag: id}"
        >
          <template #title>
            <router-link :to="{name: 'library.albums.browse', query: {tag: id}}">
              {{ $t('components.library.TagDetail.link.albums') }}
            </router-link>
          </template>
        </album-widget>
        <div class="ui hidden divider" />
        <div class="ui hidden divider" />
        <track-widget
          :key="'track' + id"
          :show-count="true"
          :limit="12"
          item-classes="track-item inline"
          :url="'/tracks/'"
          :is-activity="false"
          :filters="{playable: true, ordering: '-creation_date', tag: id}"
        >
          <template #title>
            {{ $t('components.library.TagDetail.header.tracks') }}
          </template>
        </track-widget>
        <div class="ui clearing hidden divider" />
      </div>
    </section>
  </main>
</template>
