<template>
  <div class="flex flex-col h-screen justify-center items-center">
    <Logo></Logo>
    <q-form @submit="login" ref="formRef" class="m-4">
      <div class="row q-col-gutter-x-lg">
        <div class="col-12 col-lg-12 col-md-12">
          <QInput
            filled
            standout
            bottom-slots
            v-model="form.username"
            label="Nome usuário"
          ></QInput>
        </div>
        <div class="col-12 col-lg-12 col-md-12">
          <QInput
            filled
            standout
            bottom-slots
            v-model="form.password"
            label="Senha"
            :type="'password'"
          ></QInput>
        </div>
      </div>
      <div class="flex justify-end">
        <QBtn label="Entrar" type="submit" color="primary" class="mt-4" />
      </div>
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { QBtn, QInput, useQuasar } from 'quasar';
import { reactive } from 'vue';
import Logo from '../components/LogoComponent.vue';
import { LoginForm } from 'src/services/interface';
import { useAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router';

const $q = useQuasar();
const router = useRouter();
const authStore = useAuthStore();
const form = reactive<LoginForm>({ username: '', password: '' });

const login = async () => {
  try {
    await authStore.login(form);
    router.push({ path: '/' });
  } catch (e) {
    console.error(e);
    $q.notify({
      type: 'negative',
      message: 'Aconteceu um erro no login.',
      position: 'top',
    });
  }
};
</script>
