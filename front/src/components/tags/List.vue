<script setup lang="ts">
import { truncate } from '~/utils/filters'
import { computed, ref } from 'vue'

interface Props {
  tags: string[]
  showMore?: boolean
  truncateSize?: number
  limit?: number
  labelClasses?: string
  detailRoute?: string
}

const props = withDefaults(defineProps<Props>(), {
  showMore: true,
  truncateSize: 25,
  limit: 5,
  labelClasses: '',
  detailRoute: 'library.tags.detail'
})

const honorLimit = ref(true)

const tags = computed(() => {
  if (!honorLimit.value) {
    return props.tags
  }

  return props.tags.slice(0, props.limit)
})
</script>

<template>
  <div class="component-tags-list">
    <router-link
      v-for="tag in tags"
      :key="tag"
      :to="{name: props.detailRoute, params: { id: tag } }"
      :class="['ui', 'circular', 'hashtag', 'label', props.labelClasses]"
    >
      <span class="hashtag symbol" />
      {{ truncate(tag, props.truncateSize) }}
    </router-link>
    <div
      v-if="props.showMore && tags.length < props.tags.length"
      role="button"
      class="ui circular inverted accent label"
      @click.prevent="honorLimit = false"
    >
      {{ $t('components.tags.List.button.more', props.tags.length - tags.length) }}
    </div>
  </div>
</template>
