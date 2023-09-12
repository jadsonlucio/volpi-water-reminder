import { getCurrentUser, loginUser } from '../services/auth';
import { defineStore, storeToRefs } from 'pinia';
import { AUTH_HEADER_NAME } from 'src/config/global';
import { LoginForm, User } from 'src/services/interface';
import { ref } from 'vue';
import { useWaterConsumptionStore } from './waterConsumption';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User>();

  const login = async (loginForm: LoginForm) => {
    const authResp = await loginUser(loginForm);
    localStorage.setItem(AUTH_HEADER_NAME, authResp.auth_token);
    await loadUser();
  };

  const loadUser = async () => {
    const me = await getCurrentUser();
    user.value = me;
  };

  return { user, login, loadUser };
});
