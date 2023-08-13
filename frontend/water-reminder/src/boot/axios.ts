import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { AUTH_HEADER_NAME } from 'src/config/global';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: 'http://localhost:8000/api' });

export const insertTokenInterceptor = (config: InternalAxiosRequestConfig) => {
  console.log(config);
  if (config.url == '/auth/') return config;
  const token = localStorage.getItem(AUTH_HEADER_NAME);
  if (token) {
    config.headers[AUTH_HEADER_NAME] = token;
  }
  return config;
};

api.interceptors.request.use(insertTokenInterceptor);

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };
