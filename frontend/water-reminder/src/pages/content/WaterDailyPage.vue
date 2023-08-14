<template>
  <AppScreenTemplate title="Consumo diário">
    <template #title>
      <div class="flex items-center gap-2">
        <AppScreenTitle title="Consumo diário" />
        <q-btn icon="event" round color="primary">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            <q-date v-model="form.date">
              <div class="row items-center justify-end q-gutter-sm">
                <q-btn label="Cancel" color="primary" flat v-close-popup />
                <q-btn label="OK" color="primary" flat v-close-popup />
              </div>
            </q-date>
          </q-popup-proxy>
        </q-btn>
      </div>
    </template>
    <template #content>
      <!-- <div v-if="!loadingDayRecords">
        <div>Meta do dia: {{ consumptionStatus.dailyGoal }} ML</div>
        <div>Meta restante: {{ consumptionStatus.remainingGoal }}</div>
        <div>
          Meta já consumida: {{ consumptionStatus.currentWaterConsumption }}
        </div>
        <div>
          Meta já consumida (%):
          {{ consumptionStatus.currentWaterConsumptionPercentage }}
        </div>
      </div>
      <div class="q-pa-md">
        <q-option-group
          :options="consumptionOptions"
          type="radio"
          v-model="consumptionML"
        />
        <QBtn
          label="Consumir"
          color="primary"
          :disable="!consumptionML"
          @click="registerWaterConsumption"
        />
      </div>

      <QDate v-model="form.date"></QDate> -->
      <div class="flex justify-center items-center">
        <q-circular-progress
          show-value
          :value="consumptionStatus.currentWaterConsumptionPercentage"
          size="400px"
          :thickness="0.2"
          color="blue"
          center-color="white"
          track-color="grey-3"
          class="q-ma-md"
        >
          <div
            class="flex flex-col justify-center items-center text-[#2196F3] font-extrabold text-[50px] sm:text-[100%]"
          >
            {{ consumptionStatus.currentWaterConsumptionPercentage }}%
          </div>
        </q-circular-progress>
        <div class="w-52">
          <div class="flex flex-col justify-center items-center">
            <span class="text-lg font-semibold">META DIÁRIA</span>
            <span class="text-xl font-extrabold text-[#2196F3]"
              >{{ consumptionStatus.currentWaterConsumption }}/{{
                consumptionStatus.dailyGoal
              }}
              ML</span
            >
          </div>
          <div class="mt-4 flex justify-center items-center gap-4">
            <QBtn round @click="addConsumptionValue(50)" color="grey-3"
              ><QIcon color="grey-6" name="add"
            /></QBtn>
            <QBtn
              @click="registerWaterConsumption"
              round
              size="lg"
              color="blue"
            >
              <div class="flex flex-col justify-center items-center">
                <QIcon size="sm" name="water_drop" />
                <span class="text-xs">{{ consumptionML }} ML</span>
              </div>
            </QBtn>
            <QBtn @click="addConsumptionValue(-50)" round color="grey-3"
              ><QIcon color="grey-6" name="remove"
            /></QBtn>
          </div>
        </div>
      </div>
    </template>
  </AppScreenTemplate>
</template>

<script setup lang="ts">
import { QBtn, QIcon } from 'quasar';
import { useAuthStore } from 'src/stores/auth';
import { useWaterConsumptionStore } from 'src/stores/waterConsumption';
import { onMounted, reactive, ref, watch } from 'vue';
import moment from 'moment';
import AppScreenTemplate from 'src/components/AppScreenTemplate.vue';
import AppScreenTitle from 'src/components/AppScreenTitle.vue';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const consumptionStore = useWaterConsumptionStore();
const { consumptionStatus } = storeToRefs(consumptionStore);
const loadingDayRecords = ref(true);
const consumptionML = ref<number>(300);
const form = reactive({ date: moment(moment.now()).format('YYYY/MM/DD') });

onMounted(async () => {
  try {
    loadingDayRecords.value = true;
    await authStore.loadUser();
    await consumptionStore.updateDay(new Date());
  } finally {
    loadingDayRecords.value = false;
  }
});

const registerWaterConsumption = async () => {
  if (!consumptionML.value) throw new Error('consumption value must be set');
  await consumptionStore.saveCurrentDateConsumptionRecord({
    consumption_ml: consumptionML.value,
  });
};

const addConsumptionValue = async (addValue: number) => {
  consumptionML.value = consumptionML.value + addValue;
};

watch(form, async () => {
  try {
    loadingDayRecords.value = true;
    await consumptionStore.updateDay(form.date);
  } finally {
    loadingDayRecords.value = false;
  }
});
</script>
