<script setup>
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
// import Button from "primevue/button";
import { Form } from "@primevue/forms";
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const password = ref("");
const email = ref("");
const router = useRouter();

const iniciar_sesion = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/usuarios/iniciar_sesion", {
      email: email.value,
      password: password.value,
    });
    // Si la respuesta es exitosa y el usuario existe, redirige a /mapa
    if (response.data.status == 201) {
      // Después de un login exitoso
      localStorage.setItem("usuario_email", email.value);
      router.push("/mapa");
    } else {
      alert("Usuario o contraseña incorrectos.");
    }
  } catch (error) {
    alert("Usuario o contraseña incorrectos.", error);
  }
};
</script>

<template>
  <div class="h-screen w-full relative overflow-hidden">
    <img
      src="../ssicons/carretera.jpg"
      alt="Fondo"
      class="absolute inset-0 w-full h-full object-cover z-0"
    />
    <div
      class="relative z-10 h-full flex flex-col md:flex-row items-center justify-center gap-12 p-4"
    >
      <div class="flex items-center justify-center mb-8 md:mb-0">
        <img
          src="../ssicons/logo.png"
          alt="SecuSelf Logo"
          class="w-80 h-80 object-cover rounded-lg shadow-md"
        />
      </div>
      <Card class="w-68 max-w-sm shadow-lg bg-blue-900/30">
        <template #title>
          <div class="text-center pb-4">
            <h2 class="text-xl font-semibold text-white">Login</h2>
          </div>
        </template>
        <template #content>
          <Form :resolver @submit="onFormSubmit" class="flex flex-col gap-4">
            <FormField v-slot="$field" as="div" name="correo" initialValue="">
              <InputText
                type="email"
                placeholder="Correo"
                class="w-59 px-3 py-2 bg-gray-100 text-gray-800 rounded focus:outline-none focus:border-blue-400"
                v-model="email"
              />
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
                {{ $field.error?.message }}
              </Message>
            </FormField>
            <FormField v-slot="$field" asChild name="password" initialValue="">
              <div class="mb-4">
                <Password
                  placeholder="Password"
                  :feedback="false"
                  toggleMask
                  class=""
                  v-model="password"
                />
                <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
                  {{ $field.error?.message }}
                </Message>
              </div>
            </FormField>
            <button
              class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-700"
              @click="iniciar_sesion"
            >
              Ingresar
            </button>
            <!-- <router-link
              to="/mapa"
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              role="menuitem"
              @click="$emit('toggle-menu')"
            >
              Ingresar
            </router-link> -->
            <router-link
              to="/registro"
              class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-700 text-center"
              role="menuitem"
              @click="$emit('toggle-menu')"
            >
              Registrarse
            </router-link>
          </Form>
        </template>
      </Card>
    </div>
  </div>
</template>
