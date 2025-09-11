<script setup>
import { ref } from "vue";
import InputText from "primevue/inputtext";
// import Calendar from "primevue/calendar";
import Dropdown from "primevue/dropdown";
import Textarea from "primevue/textarea";
import Button from "primevue/button";

import axios from "axios";

const formData = ref({
  ubicacion: "",
  tipo_evento: "",
  nivel_gravedad: "",
  descripcion: "",
});

const guardarReporte = async () => {
  try {
    const usuario_email = localStorage.getItem("usuario_email");
    const response = await axios.post("http://127.0.0.1:8000/reportes", {
      ubicacion: formData.value.ubicacion,
      tipo_evento: formData.value.tipo_evento,
      nivel_gravedad: formData.value.nivel_gravedad,
      descripcion: formData.value.descripcion,
      usuario_email, // <-- aquí agregas el email
    });
    console.log("Reporte guardado:", response.data);
  } catch (error) {
    console.error("Error al guardar reporte:", error);
  }
};

const eventTypes = ref(["Delito", "Accidente", "Desastre Natural", "Incendio", "Otro"]);

const gravityLevels = ref(["Leve", "Moderado", "Grave", "Crítico"]);

// const submitForm = () => {
//   console.log("Datos del reporte:", formData.value);
//   // Aquí va la lógica para enviar los datos a tu API.
// };

const resetForm = () => {
  formData.value = {
    fecha: null,
    hora: null,
    ubicacion: "",
    tipoEvento: null,
    nivelGravedad: null,
    descripcion: "",
  };
};
</script>

<template>
  <div class="h-screen w-full relative">
    <img
      src="../ssicons/carretera.jpg"
      alt="Fondo de carretera"
      class="absolute inset-0 w-full h-full object-cover z-0 opacity-80"
    />

    <div class="relative z-10 p-8 bg-[#262673]/30 rounded-xl text-white mx-auto max-w-4xl mt-10">
      <h2 class="text-3xl font-bold mb-6 text-center">Formulario de Reporte de Eventos</h2>
      <form @submit.prevent="submitForm">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- <div>
            <label for="fecha" class="block font-semibold mb-2">Fecha</label>
            <Calendar
              id="fecha"
              v-model="formData.fecha"
              class="w-full text-black"
              autocomplete="off"
              dateFormat="dd/mm/yy"
            />
          </div>
          <div>
            <label for="hora" class="block font-semibold mb-2">Hora</label>
            <Calendar
              id="hora"
              v-model="formData.hora"
              class="w-full text-black"
              autocomplete="off"
              timeOnly
            />
          </div> -->
          <div>
            <label for="ubicacion" class="block font-semibold mb-2">Ubicación</label>
            <InputText
              id="ubicacion"
              v-model="formData.ubicacion"
              class="w-full bg-white text-black"
              autocomplete="off"
            />
          </div>
          <div>
            <label for="tipoEvento" class="block font-semibold mb-2">Tipo de Evento</label>
            <Dropdown
              id="tipoEvento"
              v-model="formData.tipo_evento"
              :options="eventTypes"
              placeholder="Selecciona un tipo"
              class="w-full text-black"
            />
          </div>
          <div>
            <label for="gravedad" class="block font-semibold mb-2">Nivel de Gravedad</label>
            <Dropdown
              id="gravedad"
              v-model="formData.nivel_gravedad"
              :options="gravityLevels"
              placeholder="Selecciona un nivel"
              class="w-full text-black"
            />
          </div>
          <div class="md:col-span-2">
            <label for="descripcion" class="block font-semibold mb-2">Descripción Detallada</label>
            <Textarea
              id="descripcion"
              v-model="formData.descripcion"
              class="w-full bg-white text-black"
              :autoResize="true"
              rows="5"
            >
            </Textarea>
          </div>
        </div>

        <div class="mt-8 flex justify-end gap-2">
          <Button
            type="button"
            label="Limpiar"
            severity="secondary"
            @click="resetForm"
            class="rounded-full! bg-black/30! px-4! py-2! text-white! border-none!"
          ></Button>
          <Button
            @click="guardarReporte"
            class="rounded-full! bg-black/30! px-4! py-2! text-white! border-none!"
            type="button"
            label="Guardar"
          ></Button>
        </div>
      </form>
    </div>
  </div>
</template>
