<template>
  <AppScreenTemplate title="Histórico de hidratação">
    <template #content>
      <div>
        <div class="row">
          <div class="col col-12 col-md-4">
            <span class="text-lg font-medium">Faixa de dias</span>
            <AppDateInput
              v-model="filterForm.date"
              range
              input-format="YYYY-MM-DD"
            />
          </div>
        </div>
        <div
          class="flex justify-center"
          v-if="waterConsumptionDailyRecords?.length == 0"
        >
          <span class="text-lg font-medium"
            >Sem dados coletados durante essa data</span
          >
        </div>
        <div v-else>
          <q-list
            bordered
            padding
            separator
            class="rounded-borders overflow-scroll max-h-[500px]"
          >
            <q-item
              v-for="waterConsumptionRecord in waterConsumptionDailyRecords"
              :key="waterConsumptionRecord.date"
              clickable
              v-ripple
            >
              <q-item-section avatar>
                <q-icon name="local_drink" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label lines="1">Água</q-item-label>
                <q-item-label caption>{{
                  moment(waterConsumptionRecord.date)
                    .local()
                    .format('dddd, D [de] MMMM [de] YYYY')
                }}</q-item-label>
              </q-item-section>

              <q-item-section side>
                <div>
                  <div class="font-bold text-right">
                    {{ waterConsumptionRecord.total_consumption_ml }}ML
                  </div>
                  <div>
                    {{
                      (
                        waterConsumptionRecord.percentage_consumption * 100
                      ).toFixed(0)
                    }}% da Meta
                  </div>
                </div>
              </q-item-section>
            </q-item>
          </q-list>
        </div>
      </div>
    </template>
  </AppScreenTemplate>
</template>

<script setup lang="ts">
import moment from 'moment';
import 'moment/dist/locale/pt-br';
import AppDateInput from 'src/components/wrappers/AppDateInput.vue';
import { reactive, ref, watch } from 'vue';
import { WaterConsumptionDailyHistory } from 'src/services/interface';
import { getWaterConsumption } from 'src/services/waterConsumption';
import AppScreenTemplate from 'src/components/AppScreenTemplate.vue';

moment.locale('pt-br');

const inputFormat = 'YYYY-MM-DD';
const loadingRecords = ref(false);
const waterConsumptionDailyRecords =
  ref<WaterConsumptionDailyHistory['daily_consumptions']>();
const filterForm = reactive({
  date: {
    to: moment().format(inputFormat),
    from: moment().subtract(30, 'days').format(inputFormat),
  },
});

watch(
  filterForm,
  async (filterForm) => {
    try {
      loadingRecords.value = true;
      waterConsumptionDailyRecords.value = await getWaterConsumption({
        date_after: moment(filterForm.date.from).toDate(),
        date_before: moment(filterForm.date.to).toDate(),
      });
    } finally {
      loadingRecords.value = false;
    }
  },
  { immediate: true }
);
</script>
