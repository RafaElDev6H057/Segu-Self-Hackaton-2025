<script setup>
import Button from "primevue/button";
import InputText from "primevue/inputtext";

import { ref } from "vue";
import axios from "axios";

const nombre = ref("");
const apellido_paterno = ref("");
const apellido_materno = ref("");
const edad = ref(0);
const direccion = ref("");
const email = ref("");
const telefono = ref("");
const password = ref("");

const registrarUsuario = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/usuarios/registrar", {
      nombre: nombre.value,
      apellido_paterno: apellido_paterno.value,
      apellido_materno: apellido_materno.value,
      edad: edad.value,
      direccion: direccion.value,
      email: email.value,
      telefono: telefono.value,
      password: password.value,
    });
    // Puedes mostrar un mensaje de éxito aquí si lo deseas
    console.log("Usuario registrado:", response.data);
  } catch (error) {
    // Manejo de errores
    console.error("Error al registrar usuario:", error);
  }
};
</script>

<template>
  <div class="h-screen w-full relative">
    <img
      src="../ssicons/carretera.jpg"
      alt="Fondo de carretera"
      class="absolute inset-0 w-full h-full object-cover z-0 opacity-80"
    />
    <div
      class="relative z-10 bg-[#262673]/30 bg-opacity-5 p-8 rounded-xl text-white mx-auto max-w-2xl mt-10"
    >
      <h2 class="text-3xl font-bold mb-6 text-center">Registro</h2>
      <div class="p-fluid">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="nombre" class="block font-semibold mb-2">Nombre</label>
            <InputText
              id="nombre"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="nombre"
            />
          </div>
          <div>
            <label for="apellido_paterno" class="block font-semibold mb-2">Apellido Paterno</label>
            <InputText
              id="apellido_paterno"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="apellido_paterno"
            />
          </div>
          <div>
            <label for="apellido_materno" class="block font-semibold mb-2">Apellido Materno</label>
            <InputText
              id="apellido_materno"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="apellido_materno"
            />
          </div>
          <div>
            <label for="edad" class="block font-semibold mb-2">Edad</label>
            <InputText
              id="edad"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="edad"
            />
          </div>
          <div>
            <label for="direccion" class="block font-semibold mb-2">Dirección</label>
            <InputText
              id="direccion"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="direccion"
            />
          </div>
          <div>
            <label for="email" class="block font-semibold mb-2">Email</label>
            <InputText
              id="email"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="email"
            />
          </div>
          <div>
            <label for="telefono" class="block font-semibold mb-2">Teléfono</label>
            <InputText
              id="telefono"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="telefono"
            />
          </div>
          <div>
            <label for="contraseña" class="block font-semibold mb-2">Contraseña</label>
            <InputText
              id="contraseña"
              class="w-full bg-white text-black"
              autocomplete="off"
              v-model="password"
            />
          </div>
        </div>
      </div>

      <div class="mt-8 flex justify-end gap-2">
        <Button type="button" label="Cancelar" severity="secondary"></Button>
        <Button @click="registrarUsuario" type="button" label="Registrar"> </Button>
      </div>
    </div>
  </div>
</template>
