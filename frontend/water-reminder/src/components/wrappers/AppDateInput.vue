<script lang="ts" setup>
import moment from 'moment';
import { computed, ref } from 'vue';

import { twoWayBinding } from 'src/utils/vue';
import AppInput from './AppInput.vue';

const ptLocale = {
  months:
    'Janeiro_Fevereiro_Março_Abril_Maio_Junho_Julho_Agosto_Setembro_Outubro_Novembro_Dezembro'.split(
      '_'
    ),
  monthsShort: 'Jan_Fev_Mar_Abr_Mai_Jun_Jul_Ago_Set_Out_Nov_Dez'.split('_'),
  days: 'Domingo_Segunda-feira_Terça-feira_Quarta-feira_Quinta-feira_Sexta-feira_Sábado'.split(
    '_'
  ),
  daysShort: 'Dom_Seg_Ter_Qua_Qui_Sex_Sab'.split('_'),
  pluralDay: 'dias',
  format24h: true,
  firstDayOfWeek: 1,
};
interface Props {
  modelValue?: string | { to: string; from: string } | null;
  range?: boolean;
  inputFormat?: string;
  displayFormat?: string;
  includeTime?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  inputFormat: 'YYYY-MM-DD',
  displayFormat: 'DD/MM/YYYY',
  modelValue: '',
});

const emit = defineEmits(['update:modelValue']);

const displayMask = computed(() => {
  const mask = props.displayFormat.replace(/[YMDHm]/g, '#');
  if (props.range) {
    return `${mask} - ${mask}`;
  }
  return mask;
});
const displayValue = computed<string>({
  get() {
    const value = props.modelValue;
    if (!value) return '';
    if (props.range && typeof value == 'object') {
      const { from, to } = value;

      return `${moment(from, props.inputFormat).format(
        props.displayFormat
      )} - ${moment(to, props.inputFormat).format(props.displayFormat)}`;
    } else {
      return moment(value as string, props.inputFormat).format(
        props.displayFormat
      );
    }
  },
  set(value) {
    if (value) {
      if (props.range) {
        const [from, to] = value.split(' - ');
        const fromDate = moment(from, props.displayFormat);
        const toDate = moment(to, props.displayFormat);
        if (fromDate.isValid() && toDate.isValid()) {
          emit('update:modelValue', {
            from: fromDate.format(props.inputFormat),
            to: toDate.format(props.inputFormat),
          });
        } else {
          emit('update:modelValue', '');
        }
      } else {
        const date = moment(value, props.displayFormat);
        if (date.isValid()) {
          emit('update:modelValue', date.format(props.inputFormat));
        } else {
          emit('update:modelValue', '');
        }
      }
    }
  },
});

const localValue = twoWayBinding(props, 'modelValue');
const localTimeValue = computed({
  get: () => {
    if (!localValue.value) {
      return '';
    }
    return localValue.value.toString();
  },
  set: (value) => (localValue.value = value),
});
const showDate = ref(true);
</script>

<template>
  <AppInput v-bind="$attrs" v-model="displayValue" :mask="displayMask">
    <template #append>
      <q-icon name="event" color="primary" class="cursor-pointer">
        <q-popup-proxy
          ref="qDateProxy"
          cover
          transition-show="scale"
          transition-hide="scale"
        >
          <q-date
            v-if="showDate"
            v-model="localValue"
            :locale="ptLocale"
            :range="range"
            :mask="inputFormat"
          >
            <div class="row items-center justify-end">
              <q-btn
                v-if="includeTime"
                label="Hora"
                color="primary"
                flat
                @click="showDate = false"
              />
              <q-btn v-close-popup label="Fechar" color="primary" flat />
            </div>
          </q-date>
          <q-time
            v-else
            v-model="localTimeValue"
            :locale="ptLocale"
            :range="range"
            :mask="inputFormat"
          >
            <div class="row items-center justify-end">
              <q-btn
                label="Data"
                color="primary"
                flat
                @click="showDate = true"
              />
              <q-btn v-close-popup label="Fechar" color="primary" flat />
            </div>
          </q-time>
        </q-popup-proxy>
      </q-icon>
    </template>
  </AppInput>
</template>
