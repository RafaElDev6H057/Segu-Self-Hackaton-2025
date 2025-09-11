<script setup>
import { ref } from "vue";

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// Cierra el menú si se hace clic fuera de él
const closeMenuOnClickOutside = (event) => {
  const menuButton = document.getElementById("menu-button");
  const menu = document.querySelector(".origin-top-right");
  if (menu && menuButton && !menu.contains(event.target) && !menuButton.contains(event.target)) {
    isMenuOpen.value = false;
  }
};

// Agrega un listener de eventos para el clic fuera del menú
import { onMounted, onUnmounted } from "vue";
onMounted(() => {
  document.addEventListener("click", closeMenuOnClickOutside);
});
onUnmounted(() => {
  document.removeEventListener("click", closeMenuOnClickOutside);
});
</script>
<template>
  <div class="relative inline-block text-left z-10000">
    <div>
      <button
        @click="toggleMenu"
        class="inline-flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 focus:ring-blue-500 transition-colors"
        id="menu-button"
        aria-expanded="true"
        aria-haspopup="true"
      >
        Menú de Opciones
        <svg class="-mr-1 ml-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path
            fill-rule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>

    <div
      v-show="isMenuOpen"
      class="origin-top-right absolute right-0 mt-2 w-64 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="menu-button"
    >
      <div class="py-1">
        <!-- <div class="flex justify-center py-4">
          <img
            src="https://via.placeholder.com/150"
            alt="Imagen de perfil o logo"
            class="w-24 h-24 rounded-full"
          />
        </div> -->

        <router-link
          to="/mapa"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          role="menuitem"
          @click="toggleMenu"
        >
          Mapa
        </router-link>
        <router-link
          to="/reportes-estadisticos"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          role="menuitem"
          @click="toggleMenu"
        >
          Reportes Estadísticos
        </router-link>
        <router-link
          to="/reportes"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          role="menuitem"
          @click="toggleMenu"
        >
          Reportes
        </router-link>
        <router-link
          to="/historial-incidentes"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          role="menuitem"
          @click="toggleMenu"
        >
          Historial de Incidentes
        </router-link>
        <a
          href="https://chat.whatsapp.com/LrmKsQRRdIB6jnkddAt19J?mode=ems_wa_c"
          target="_blank"
          rel="noopener noreferrer"
          class="block px-4 py-2 text-sm text-black hover:bg-gray-100"
        >
          Unirse a grupo de WhatsApp
        </a>
      </div>
    </div>
  </div>
</template>
