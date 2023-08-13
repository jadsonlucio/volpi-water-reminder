<template>
  <div class="flex h-screen justify-center items-center">
    <q-form ref="formRef" class="m-4">
      <div class="row q-col-gutter-x-lg">
        <div class="col-12 col-lg-4 col-md-6">
          <QInput
            v-model="form.username"
            filled
            standout
            bottom-slots
            label="Nome usuário"
          />
        </div>
        <div class="col-12 col-lg-4 col-md-6">
          <QInput
            filled
            standout
            bottom-slots
            v-model="form.password"
            type="password"
            label="Senha"
          />
        </div>
        <div class="col-12 col-lg-4 col-md-6">
          <QInput
            filled
            standout
            bottom-slots
            v-model="form.confirm_password"
            type="password"
            label="Confirmar senha"
          />
        </div>
        <div class="col-12 col-lg-4 col-md-6">
          <QInput
            filled
            standout
            bottom-slots
            type="email"
            v-model="form.email"
            label="Email"
          />
        </div>
        <div class="col-12 col-lg-4 col-md-6">
          <QInput
            filled
            standout
            bottom-slots
            v-model="form.first_name"
            label="Nome"
          />
        </div>
        <div class="col-12 col-lg-4 col-md-6">
          <QInput
            filled
            standout
            bottom-slots
            v-model="form.last_name"
            label="Sobrenome"
          />
        </div>
      </div>
      <div class="flex justify-end mt-8">
        <QBtn label="Cadastrar" type="submit" color="primary" />
      </div>
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { QInput, QForm, QBtn } from 'quasar';
import { reactive, ref } from 'vue';
import { RegisterForm } from 'src/services/interface';
import { registerUser } from 'src/services/auth';

const formRef = ref<QForm | null>(null);

const form = reactive<RegisterForm>({
  username: '',
  password: '',
  confirm_password: '',
  email: '',
  first_name: '',
  last_name: '',
  weight: NaN,
});

const confirmUserRegistation = () => {
  if (formRef.value) {
    formRef.value.validate().then((success) => {
      if (success) {
        registerUser(form);
      } else {
        // oh no, user has filled in
        // at least one invalid value
      }
    });
  }
};
</script>
