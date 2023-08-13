import { getCurrentInstance, ref, watch } from 'vue';

export const twoWayBinding = <
  T extends Record<string, unknown>,
  K extends keyof T
>(
  props: T,
  variableName: K
) => {
  const instance = getCurrentInstance();
  if (!instance) {
    throw new Error('Cannot get current instance');
  }
  const refVariable = ref<T[K]>();

  watch(
    () => props[variableName as string],
    (newValue) => {
      refVariable.value = newValue as T[K];
    },
    {
      immediate: true,
    }
  );

  watch(
    () => refVariable.value,
    (newValue) => {
      const variableNameString = variableName.toString();
      instance.emit(`update:${variableNameString}`, newValue);
    }
  );

  return refVariable;
};
