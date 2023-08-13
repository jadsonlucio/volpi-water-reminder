<template>
  <div class="container mt-4 rounded-lg bg-white">
    <slot name="title"><AppScreenTitle :title="props.title" /></slot>

    <div class="content mt-4">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppScreenTitle from './AppScreenTitle.vue';

const props = defineProps<{ title: string }>();
</script>
