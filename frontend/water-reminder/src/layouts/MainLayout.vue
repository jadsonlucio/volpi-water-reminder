<template>
  <q-layout class="bg-[#F1F2F6]" view="hHh lpR fFf">
    <q-header reveal elevated class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <Logo></Logo>
          <span class="font-bold"> WATER REMINDER</span>
        </q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab to="/" label="Consumo diário" />
        <q-route-tab to="/statistics" label="Estatísticas" />
        <q-route-tab to="/history" label="Histórico" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- <q-footer reveal elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          <div>Water Reminder</div>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer> -->
  </q-layout>
</template>

<script setup lang="ts">
import Logo from 'src/components/LogoComponent.vue';
</script>
