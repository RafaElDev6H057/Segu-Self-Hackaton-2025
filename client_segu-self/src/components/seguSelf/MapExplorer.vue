<template>
  <div class="map-container">
    <header>
      <h1>SeguSelf</h1>
      <nav>
        <button class="btn-primary" @click="isMenuOpen = !isMenuOpen">Menu</button>
        <MenuSS v-if="isMenuOpen" @click-outside="isMenuOpen = false" />
      </nav>
    </header>

    <main class="fixed-main">
      <div id="map" class="fixed-map"></div>
      <div class="route-form">
        <input
          type="text"
          v-model="startPoint"
          placeholder="Ingrese punto de inicio (ej., Guadalajara)"
        />
        <input
          type="text"
          v-model="endPoint"
          placeholder="Ingrese punto de llegada (ej., Puerto Vallarta)"
        />
        <button class="btn-primary" @click="handleRouteRequest" :disabled="loading">
          {{ loading ? "Buscando…" : "Obtener Ruta" }}
        </button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>

      <!-- Formulario para agregar punto de peligro -->
      <div class="danger-form">
        <h3>Agregar Punto de Peligro</h3>

        <input type="text" v-model="newDanger.name" placeholder="Nombre del punto" />

        <input type="number" v-model.number="newDanger.lat" placeholder="Latitud" step="any" />

        <input type="number" v-model.number="newDanger.lng" placeholder="Longitud" step="any" />

        <button
          class="btn-primary ml-0!"
          type="button"
          @click="enableSelectLocation"
          :disabled="selectingLocation"
        >
          {{ selectingLocation ? "Haz clic en el mapa..." : "Seleccionar en mapa" }}
        </button>

        <select v-model.number="newDanger.level">
          <option disabled value="">Selecciona un nivel</option>
          <option :value="1">Nivel 1</option>
          <option :value="2">Nivel 2</option>
          <option :value="3">Nivel 3</option>
        </select>

        <button class="btn-primary ml-0!" @click="agregarPuntoPeligro">Agregar</button>
      </div>
    </main>

    <footer>&copy; 2025 Lombax jr</footer>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import MenuSS from "./MenuSS.vue";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

let map = null;
let routeLayer = null;
let tempMarker = null;

const isMenuOpen = ref(false);

const startPoint = ref("");
const endPoint = ref("");
const errorMessage = ref(null);
const loading = ref(false);

const newDanger = ref({
  name: "",
  lat: "",
  lng: "",
  level: 1,
});

const selectingLocation = ref(false);

const agregarPuntoPeligro = () => {
  if (
    !newDanger.value.name ||
    newDanger.value.lat === "" ||
    newDanger.value.lng === "" ||
    !newDanger.value.level
  ) {
    alert("Completa todos los campos para agregar el punto de peligro.");
    return;
  }
  const nuevoId =
    dangerousLocations.value.length > 0
      ? Math.max(...dangerousLocations.value.map((p) => p.id)) + 1
      : 1;
  dangerousLocations.value.push({
    id: nuevoId,
    name: newDanger.value.name,
    lat: parseFloat(newDanger.value.lat),
    lng: parseFloat(newDanger.value.lng),
    level: newDanger.value.level,
  });
  renderDangerMarkers();
  // Limpiar formulario
  newDanger.value = { name: "", lat: "", lng: "", level: 1 };
  if (tempMarker) {
    map.removeLayer(tempMarker);
    tempMarker = null;
  }
};

const enableSelectLocation = () => {
  selectingLocation.value = true;
};

const handleMapClick = (e) => {
  if (!selectingLocation.value) return;
  const { lat, lng } = e.latlng;
  newDanger.value.lat = lat;
  newDanger.value.lng = lng;
  // Mostrar marcador temporal
  if (tempMarker) map.removeLayer(tempMarker);
  tempMarker = L.marker([lat, lng], { opacity: 0.7 }).addTo(map);
  selectingLocation.value = false;
};

// Mapbox token
const MAPBOX_TOKEN =
  "pk.eyJ1IjoiZGFya2RpZWdvMTAyIiwiYSI6ImNtZmVxczMwZTBhNXcyaXE1Z2owZHh3aGcifQ.1YjZ8c6hm-PS4HShVo3PBA";

// === Permanent danger points ===
const dangerousLocations = ref([
  { id: 1, name: "Asalto a mano armada", lat: 23.181896, lng: -102.871353, level: 1 },
  { id: 2, name: "Guadalajara - Norte", lat: 20.68, lng: -103.32, level: 2 },
  { id: 3, name: "Fresnillo - Plaza", lat: 23.178, lng: -102.871, level: 3 },
  { id: 4, name: "Fresnillo - Norte", lat: 23.17, lng: -102.86, level: 1 },
  { id: 5, name: "Fresnillo - Sur", lat: 23.15, lng: -102.88, level: 2 },
]);

// === Helpers ===
const getDangerColor = (level) => {
  switch (level) {
    case 1:
      return "#ff6666"; // light red
    case 2:
      return "#e60000"; // medium red
    case 3:
      return "#660000"; // dark red
    default:
      return "#ff0000";
  }
};

// Update danger level permanently
const reinforceDangerPoint = (id) => {
  const point = dangerousLocations.value.find((p) => p.id === id);
  if (point && point.level < 3) {
    point.level += 1;
    renderDangerMarkers();
  }
};

// === Render Markers ===
let dangerMarkers = [];
const renderDangerMarkers = () => {
  // Remove old markers
  dangerMarkers.forEach((m) => map.removeLayer(m));
  dangerMarkers = [];

  dangerousLocations.value.forEach((point) => {
    const color = getDangerColor(point.level);
    const marker = L.marker([point.lat, point.lng], {
      icon: L.divIcon({
        className: "danger-marker",
        html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white;"></div>`,
      }),
    }).addTo(map);

    marker.bindPopup(`
      <b>${point.name}</b><br>
      Nivel: ${point.level}<br>
      <button onclick="window.reinforceDanger(${point.id})">Reforzar</button>
    `);

    dangerMarkers.push(marker);
  });
};

// === Make reinforce globally callable ===
window.reinforceDanger = (id) => {
  reinforceDangerPoint(id);
};

// === Geocode, routes, etc (your existing code) ===
const geocodeAddress = async (address) => {
  if (!address || address.trim() === "") return null;
  errorMessage.value = null;

  try {
    const mbUrl = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(
      address
    )}.json?limit=1&access_token=${MAPBOX_TOKEN}`;
    const mbRes = await fetch(mbUrl);
    if (mbRes.ok) {
      const mbData = await mbRes.json();
      if (mbData.features && mbData.features.length > 0) {
        const [lng, lat] = mbData.features[0].center;
        return L.latLng(lat, lng);
      }
    }
  } catch (err) {
    console.warn("[Geocode] Mapbox error:", err);
  }

  try {
    const nomUrl = `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(
      address
    )}`;
    const nomRes = await fetch(nomUrl, { headers: { "Accept-Language": "en" } });
    if (nomRes.ok) {
      const nomData = await nomRes.json();
      if (nomData && nomData.length > 0) {
        return L.latLng(parseFloat(nomData[0].lat), parseFloat(nomData[0].lon));
      }
    }
  } catch (err) {
    console.warn("[Geocode] Nominatim error:", err);
  }

  return null;
};

const getRouteFromMapbox = async (startLngLat, endLngLat) => {
  try {
    const profile = "driving";
    const waypoints = `${startLngLat.lng},${startLngLat.lat};${endLngLat.lng},${endLngLat.lat}`;
    const url = `https://api.mapbox.com/directions/v5/mapbox/${profile}/${waypoints}?alternatives=true&geometries=geojson&steps=false&access_token=${MAPBOX_TOKEN}`;

    const res = await fetch(url);
    if (!res.ok) return null;
    const data = await res.json();
    if (data.routes && data.routes.length > 0) {
      return data.routes[0].geometry;
    }
    return null;
  } catch (err) {
    return err;
  }
};

const handleRouteRequest = async () => {
  errorMessage.value = null;
  loading.value = true;

  try {
    if (routeLayer) {
      map.removeLayer(routeLayer);
      routeLayer = null;
    }

    const startCoords = await geocodeAddress(startPoint.value);
    const endCoords = await geocodeAddress(endPoint.value);

    if (!startCoords || !endCoords) {
      errorMessage.value = "Invalid start or end location";
      return;
    }

    const routeGeometry = await getRouteFromMapbox(startCoords, endCoords);
    if (!routeGeometry) {
      errorMessage.value = "Could not fetch route";
      return;
    }

    const feature = { type: "Feature", properties: {}, geometry: routeGeometry };
    routeLayer = L.geoJSON(feature, { style: { color: "#e60000", weight: 5, opacity: 0.9 } }).addTo(
      map
    );
    map.fitBounds(routeLayer.getBounds(), { padding: [50, 50] });
  } finally {
    loading.value = false;
  }
};

// === Init ===
onMounted(() => {
  map = L.map("map").setView([20.6736, -103.344], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  renderDangerMarkers();

  // Escuchar clicks en el mapa
  map.on("click", handleMapClick);
});
</script>

<style scoped>
/* Scoped styles to prevent style conflicts with other components */
.map-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #0d0d1a;
  color: #ffffff;
}

header {
  background-color: #141432;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.6);
  border-bottom: 2px solid #262673;
}

header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #ffbb33;
  text-shadow: 0 0 8px #ffbb33, 0 0 16px #e60000;
}

nav {
  display: flex;
  align-items: center;
}

.btn-primary {
  background-color: transparent;
  border: 2px solid #e60000;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  color: #ffbb33;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  text-shadow: 0 0 6px #ffbb33, 0 0 10px #e60000;
  box-shadow: 0 0 8px #e60000, inset 0 0 8px #e60000;
  margin-left: 1.5rem; /* Space between the links and the button */
}

.btn-primary:hover {
  background-color: #e60000;
  color: #ffffff;
  box-shadow: 0 0 12px #ffbb33, 0 0 24px #e60000;
}

.fixed-main {
  flex: none; /* Prevents flex-grow from affecting size */
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #0d0d1a;
  width: 100%; /* Ensures it fills parent */
  height: 80vh; /* Adjust as needed to maintain size */
}

#map.fixed-map {
  width: 90%;
  height: 90%;
  border-radius: 16px;
  border: 2px solid #262673;
  box-shadow: 0 0 15px #262673, 0 0 30px #e60000;
  flex-shrink: 0; /* Prevents the map from shrinking */
}

footer {
  background-color: #141432;
  text-align: center;
  padding: 0.75rem;
  font-size: 0.9rem;
  color: #ffbb33;
  border-top: 2px solid #262673;
  text-shadow: 0 0 8px #ffbb33, 0 0 12px #e60000;
}

.route-form {
  position: absolute;
  top: 150px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  background-color: #141432;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  z-index: 1000; /* Ensures the form is on top of the map */
}

.route-form input {
  padding: 10px;
  border: 1px solid #262673;
  border-radius: 6px;
  background-color: #0d0d1a;
  color: #fff;
  font-size: 1rem;
}

.route-form input::placeholder {
  color: #aaa;
}

/* Remove the unused nav-links styling */
.nav-links {
  display: none;
}

.danger-form {
  position: fixed;
  top: 90px; /* Debajo del header */
  left: 30px; /* Separado del borde izquierdo */
  background: #141432;
  padding: 18px 16px 14px 16px;
  border-radius: 12px;
  box-shadow: 0 6px 24px #000b;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1200;
  min-width: 250px;
  max-width: 320px;
  border: 2px solid #262673;
}

.danger-form h3 {
  margin: 0 0 10px 0;
  color: #ffbb33;
  font-size: 1.15rem;
  text-align: center;
}

.danger-form input,
.danger-form select {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #262673;
  background: #0d0d1a;
  color: #fff;
  font-size: 1rem;
}

.danger-form input::placeholder {
  color: #aaa;
}

.danger-form button {
  margin-top: 8px;
  width: 100%;
}

@media (max-width: 700px) {
  .danger-form {
    position: static;
    margin: 12px auto 0 auto;
    width: 95vw;
    max-width: 98vw;
  }
}
</style>
