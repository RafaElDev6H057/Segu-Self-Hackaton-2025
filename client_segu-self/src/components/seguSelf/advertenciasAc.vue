<script setup>
import { ref, onMounted } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import axios from "axios";

const warnings = ref([]);

// Obtener el correo del usuario logueado
const usuario_email = localStorage.getItem("usuario_email");

const fetchWarnings = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/reportes");
    // Filtrar solo los reportes del usuario logueado
    const data = response.data
      .filter((r) => r.usuario && r.usuario.email === usuario_email)
      .map((r) => ({
        email: r.usuario.email,
        fecha: r.fecha,
        hora: r.hora,
        ubicación: r.ubicacion,
        tipo_evento: r.tipo_evento,
        nivel_gravedad: r.nivel_gravedad,
        descripcion: r.descripcion,
      }));
    warnings.value = data;
  } catch (error) {
    warnings.value = [];
    console.error("Error al obtener reportes:", error);
  }
};

onMounted(fetchWarnings);
</script>

<template>
  <div class="h-screen w-full relative overflow-hidden">
    <img
      src="../ssicons/carretera.jpg"
      alt="Fondo de carretera"
      class="absolute inset-0 w-full h-full object-cover z-0 opacity-80"
    />

    <div class="relative z-10 p-8 rounded-xl text-write mx-auto max-w-4xl mt-10 bg-[#262673]/30">
      <div class="flex items-center justify-center mb-6">
        <img src="../ssicons/advertencia.png" alt="Icono de Advertencia" class="h-8 w-8 mr-2" />
        <h2 class="text-3xl font-bold">Historial de reportes</h2>
      </div>
      <DataTable :value="warnings" paginator :rows="10" tableStyle="min-width: 50rem">
        <Column field="email" header="Correo"></Column>
        <Column field="fecha" header="Fecha"></Column>
        <Column field="hora" header="Hora"></Column>
        <Column field="ubicación" header="Ubicación"></Column>
        <Column field="tipo_evento" header="Tipo de Evento"></Column>
        <Column field="nivel_gravedad" header="Nivel de Gravedad"></Column>
        <Column field="descripcion" header="Descripción"></Column>
        <template #empty>
          <div class="text-center p-4">No se encontraron advertencias.</div>
        </template>
      </DataTable>

      <div class="flex justify-end mt-2">
        <router-link
          to="/mapa"
          class="rounded-full bg-black/30 px-4 py-2"
          role="menuitem"
          @click="toggleMenu"
        >
          Atras
        </router-link>
      </div>
    </div>
  </div>
</template>
