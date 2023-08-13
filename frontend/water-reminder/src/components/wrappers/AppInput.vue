<script setup lang="ts">
import { QInputProps } from 'quasar';
import { computed } from 'vue';

interface Props extends QInputProps {
  modelValue: string | number | null;
  label?: string;
  errorMessage?: string;
  innerLabel?: boolean;
  modelModifiers?: Record<string, unknown> | Record<string, never>;
  dataCy?: string;
  required?: boolean;
}
const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  label: '',
  errorMessage: '',
  innerLabel: false,
  modelModifiers: () => ({}),
  dataCy: 'base-input',
});
const emits = defineEmits(['update:modelValue']);

const localValue = computed<string | number | null | undefined>({
  get() {
    return props.modelValue;
  },
  set(value) {
    if (props.modelModifiers.number) {
      emits('update:modelValue', Number(value));
    } else {
      emits('update:modelValue', value);
    }
  },
});
const hasError = computed(() => props.errorMessage !== '');
</script>

<template>
  <div>
    <label
      v-if="!innerLabel && label"
      class="base-input__label text-label q-mb-sm block"
    >
      <template v-if="required"> {{ label }} * </template>
      <template v-else> {{ label }} </template>
    </label>
    <q-input
      v-model="localValue"
      :label="innerLabel ? label : undefined"
      :model-modifiers="props.modelModifiers"
      v-bind="$attrs"
      standout
      :error-message="errorMessage"
      :error="hasError"
      :data-cy="dataCy"
    >
      <template v-for="(_, name) in ($slots as {})" #[name]="slotData">
        <slot :name="name" v-bind="slotData || {}" />
      </template>
    </q-input>
  </div>
</template>
