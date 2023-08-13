<template>
  <div class="text-xl font-extrabold text-[#2196F3]">{{ titleUpperCase }}</div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{ title: string }>();

const titleUpperCase = computed(() => {
  return props.title.toUpperCase();
});
</script>
