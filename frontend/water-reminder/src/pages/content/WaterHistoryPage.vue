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
          v-if="waterConsumptionRecords?.length == 0"
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
              v-for="waterConsumptionRecord in waterConsumptionRecords"
              :key="waterConsumptionRecord.id"
              clickable
              v-ripple
            >
              <q-item-section avatar>
                <q-icon name="local_drink" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label lines="1">Água</q-item-label>
                <q-item-label caption>{{
                  moment(waterConsumptionRecord.date).format('LLLL')
                }}</q-item-label>
              </q-item-section>

              <q-item-section side>
                <div>
                  <div class="font-bold text-right">
                    {{ waterConsumptionRecord.consumption_ml }}ML
                  </div>
                  <div>Coeficiente 1.0</div>
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
import AppDateInput from 'src/components/wrappers/AppDateInput.vue';
import { reactive, ref, watch } from 'vue';
import { WaterConsumptionRecord } from 'src/services/interface';
import { getWaterConsumption } from 'src/services/waterConsumption';
import AppScreenTemplate from 'src/components/AppScreenTemplate.vue';
const inputFormat = 'YYYY-MM-DD';
const loadingRecords = ref(false);
const waterConsumptionRecords = ref<WaterConsumptionRecord[]>();
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
      waterConsumptionRecords.value = await getWaterConsumption({
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
