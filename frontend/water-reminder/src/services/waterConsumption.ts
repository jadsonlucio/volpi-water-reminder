import { api } from 'src/boot/axios';
import {
  WaterConsumptionFilter,
  WaterConsumptionRecord,
  WaterConsumptionForm,
} from './interface';
import moment from 'moment';

export const getWaterConsumption = async (
  filterForm: WaterConsumptionFilter
): Promise<WaterConsumptionRecord[]> => {
  const filterFormProcessed: { date_before?: string; date_after?: string } = {};
  if (filterForm.date_after)
    filterFormProcessed.date_after = moment(filterForm.date_after).format(
      'YYYY-MM-DD'
    );
  if (filterForm.date_before)
    filterFormProcessed.date_before = moment(filterForm.date_before).format(
      'YYYY-MM-DD'
    );
  const { data } = await api.get('/consumption/', {
    params: filterFormProcessed,
  });

  return data;
};

export const registerWaterConsumption = async (
  waterConsumptionForm: WaterConsumptionForm
): Promise<WaterConsumptionRecord> => {
  const { data } = await api.post('/consumption/', waterConsumptionForm);
  return data;
};

export const updateWaterConsumption = async (
  waterConsumptionForm: WaterConsumptionForm
): Promise<WaterConsumptionRecord> => {
  if (!waterConsumptionForm.id)
    throw new Error("can't update a water consumption record without id");
  const { data } = await api.put('/consumption/${}', waterConsumptionForm);
  return data;
};

export const saveWaterConsumption = async (
  waterConsumptionForm: WaterConsumptionForm
): Promise<WaterConsumptionRecord> => {
  if (waterConsumptionForm.id) {
    return await updateWaterConsumption(waterConsumptionForm);
  }
  return await registerWaterConsumption(waterConsumptionForm);
};

export const deleteWaterConsumption = async (waterConsumptionId: string) => {
  const { data } = await api.delete(`/consumption/${waterConsumptionId}`);
  return data;
};
