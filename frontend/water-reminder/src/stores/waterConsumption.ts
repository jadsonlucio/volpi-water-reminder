import moment from 'moment';
import { WaterConsumptionForm } from './../services/interface';
import { defineStore } from 'pinia';
import { WaterConsumptionRecord } from 'src/services/interface';
import {
  getWaterConsumption,
  saveWaterConsumption,
} from 'src/services/waterConsumption';
import { computed, ref } from 'vue';

export const useWaterConsumptionStore = defineStore('water-consumption', () => {
  const dailyConsumptionGoal = ref<number>();
  const currentDateConsumption = ref<Date>();
  const currentDateConsumptionRecords = ref<WaterConsumptionRecord[]>();

  const updateDay = async (day: string | Date) => {
    if (typeof day == 'string') day = moment(day).toDate();
    currentDateConsumption.value = day;
    currentDateConsumptionRecords.value = await getWaterConsumption({
      date_before: day,
      date_after: day,
    });
  };

  const saveCurrentDateConsumptionRecord = async (
    waterConsumptionForm: Omit<WaterConsumptionForm, 'date'>
  ) => {
    if (!currentDateConsumption.value)
      throw new Error(
        'you must have a current date consumption variable to run this function'
      );
    const waterConsumptionFormCurrentDate: WaterConsumptionForm = {
      ...waterConsumptionForm,
      date: currentDateConsumption.value,
    };
    const consumptionRecord = await saveWaterConsumption(
      waterConsumptionFormCurrentDate
    );
    if (!waterConsumptionForm.id) {
      currentDateConsumptionRecords.value?.push(consumptionRecord);
    }
  };

  const currentWaterConsumption = computed(() => {
    const waterConsumption = currentDateConsumptionRecords.value?.reduce(
      (curr, record) => record.comsumption_ml + curr,
      0
    );
    if (!waterConsumption) return 0;
    return waterConsumption;
  });

  const consumptionStatus = computed(() => {
    if (!dailyConsumptionGoal.value) {
      return {
        dailyGoal: 0,
        currentWaterConsumption: currentWaterConsumption.value,
        remainingGoal: 0,
        currentWaterConsumptionPercentage: 0,
      };
    }
    return {
      dailyGoal: dailyConsumptionGoal.value,
      currentWaterConsumption: currentWaterConsumption.value,
      remainingGoal:
        dailyConsumptionGoal.value >= currentWaterConsumption.value
          ? dailyConsumptionGoal.value - currentWaterConsumption.value
          : 0,
      currentWaterConsumptionPercentage: Math.round(
        (currentWaterConsumption.value / dailyConsumptionGoal.value) * 100
      ),
    };
  });

  return {
    dailyConsumptionGoal,
    currentDateConsumptionRecords,
    consumptionStatus,
    updateDay,
    saveCurrentDateConsumptionRecord,
  };
});
