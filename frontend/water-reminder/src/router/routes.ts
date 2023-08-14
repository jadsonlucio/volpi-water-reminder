import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/content/WaterDailyPage.vue') },
      {
        path: 'history',
        component: () => import('pages/content/WaterHistoryPage.vue'),
      },
      {
        path: 'statistics',
        component: () => import('pages/content/WaterStatisticsPage.vue'),
      },
    ],
  },
  {
    path: '/login',
    component: () => import('src/pages/auth/LoginPage.vue'),
  },
  {
    path: '/register',
    component: () => import('src/pages/auth/RegisterPage.vue'),
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
