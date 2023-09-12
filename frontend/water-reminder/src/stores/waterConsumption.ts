import moment from 'moment';
import { defineStore } from 'pinia';
import { WaterConsumptionForm } from 'src/services/interface';
import { DailyConsumption } from 'src/services/interface';
import {
  getWaterConsumption,
  saveWaterConsumption,
} from 'src/services/waterConsumption';
import { computed, ref } from 'vue';

export const useWaterConsumptionStore = defineStore('water-consumption', () => {
  const currentDateConsumption = ref<Date>();
  const currentDailyConsumption = ref<DailyConsumption>();
  const savingDayRecords = ref(false);
  const loadingDayRecords = ref(true)

  const updateDay = async (day: string | Date) => {
    if (typeof day == 'string') day = moment(day).toDate();
    currentDateConsumption.value = day;
    try {
      loadingDayRecords.value = true;
      const consumption_records = await getWaterConsumption({
        date_before: day,
        date_after: day,
      });
      if (consumption_records.length == 0) {
        currentDailyConsumption.value = {
          date: moment(day).format('YYYY-MM-DD'),
          records: [],
          goal_ml: 0,
          remaining_goal: 0,
          percentage_consumption: 0,
          total_consumption_ml: 0,
        };
      }
      const dailyConsumption = consumption_records[0];
      currentDailyConsumption.value = dailyConsumption;
    } finally {
      loadingDayRecords.value = false
    }
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
    try {
      savingDayRecords.value = true;
      await saveWaterConsumption(waterConsumptionFormCurrentDate);
      await updateDay(currentDateConsumption.value);
    } finally {
      savingDayRecords.value = false;
    }
  };

  const consumptionStatus = computed(() => {
    if (!currentDailyConsumption.value) {
      return {
        dailyGoal: 0,
        currentWaterConsumption: 0,
        remainingGoal: 0,
        currentWaterConsumptionPercentage: 0,
      };
    }
    return {
      dailyGoal: currentDailyConsumption.value.goal_ml,
      currentWaterConsumption:
        currentDailyConsumption.value?.total_consumption_ml,
      remainingGoal: currentDailyConsumption.value.remaining_goal,
      currentWaterConsumptionPercentage: Math.round(
        currentDailyConsumption.value.percentage_consumption * 100
      ),
    };
  });

  return {
    currentDailyConsumption,
    consumptionStatus,
    savingDayRecords,
    loadingDayRecords,
    updateDay,
    saveCurrentDateConsumptionRecord,
  };
});
