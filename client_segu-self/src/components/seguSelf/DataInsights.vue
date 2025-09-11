<template>
  <div class="main-container">
    <header>
      <h1>Análisis de Datos</h1>
      <nav>
        <button class="btn-primary" @click="isMenuOpen = !isMenuOpen">Menu</button>
        <MenuSS v-if="isMenuOpen" @click-outside="isMenuOpen = false" />
      </nav>
    </header>

    <main>
      <div class="stats-card">
        <h2>Estadísticas de Reportes por Dirección</h2>
        <p>Analizando datos del campo para mostrar la frecuencia de los reportes.</p>

        <div v-if="loading" class="loading-state">Analizando datos con IA...</div>

        <div v-else>
          <div class="ai-insight-box">
            <h3>Análisis de la IA:</h3>
            <p v-html="aiSummary"></p>
          </div>

          <ul class="stats-list">
            <li v-for="(stats, index) in zipCodeStats" :key="index" class="stat-item">
              <span class="stat-label"
                >Dirección: <span class="stat-value">{{ stats.zipCode }}</span></span
              >
              <span class="stat-label"
                >Total de Reportes: <span class="stat-value">{{ stats.totalReports }}</span></span
              >
            </li>
          </ul>
        </div>
      </div>
    </main>

    <footer>&copy; 2025 Lombax jr</footer>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

import MenuSS from "./MenuSS.vue";

const marked = window.marked;

const isMenuOpen = ref(false);

const zipCodeStats = ref([]);
const loading = ref(true);
const aiSummary = ref("");

function isWithinLastWeek(dateStr) {
  const today = new Date();
  const date = new Date(dateStr);
  const diff = today - date;
  return diff >= 0 && diff <= 7 * 24 * 60 * 60 * 1000;
}

// const simulatedData = [
//   { zipCode: "70230", totalReports: 154 },
//   { zipCode: "71000", totalReports: 98 },
//   { zipCode: "70801", totalReports: 210 },
//   { zipCode: "71001", totalReports: 76 },
//   { zipCode: "71002", totalReports: 112 },
// ];

const getStatistics = async () => {
  loading.value = true;
  try {
    // 1. Obtener todos los reportes
    const res = await fetch("http://127.0.0.1:8000/reportes");
    if (!res.ok) throw new Error("No se pudieron obtener los reportes");
    const allReports = await res.json();

    // 2. Filtrar solo los de la última semana
    const recentReports = allReports.filter((r) => isWithinLastWeek(r.fecha));

    // 3. Generar estadísticas por código postal (zipCode)
    // Si tus reportes tienen un campo zipCode, usa ese. Si no, ajusta aquí.
    // Supondré que el campo es r.ubicacion y contiene el código postal.
    // Si no, deberás adaptar esta parte.
    const zipStats = {};
    for (const r of recentReports) {
      const zip = r.ubicacion; // Cambia esto si tienes un campo específico para el código postal
      if (!zipStats[zip]) zipStats[zip] = 0;
      zipStats[zip]++;
    }
    zipCodeStats.value = Object.entries(zipStats).map(([zipCode, totalReports]) => ({
      zipCode,
      totalReports,
    }));

    // 4. Preparar el prompt con los datos filtrados
    const prompt = `
Analiza el siguiente conjunto de reportes recientes de incidentes. Considera la ubicación, el tipo de evento, el nivel de gravedad y la descripción. 
Identifica las zonas de mayor riesgo, los tipos de eventos más frecuentes y los niveles de gravedad predominantes. 
Resume los hallazgos de forma breve y clara, solo con los resultados esenciales y recomendaciones puntuales sobre áreas a evitar o donde extremar precauciones. 
Limita la respuesta a máximo 10 líneas y responde únicamente en texto plano, sin formato markdown.

Datos:
${JSON.stringify(recentReports, null, 2)}
`;

    // 5. Consumir el endpoint de IA
    const backendResponse = await fetch("http://localhost:8000/ia/analizar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    if (!backendResponse.ok) {
      throw new Error(`HTTP error! estado: ${backendResponse.status}`);
    }

    const result = await backendResponse.json();

    aiSummary.value = result.summary
      ? marked
        ? marked.parse(result.summary)
        : result.summary
      : "La IA no devolvió ningún análisis.";
  } catch (error) {
    console.error("Error de obtención de datos o análisis de IA:", error);
    aiSummary.value =
      "Error al obtener información de la IA. Por favor, revisa el servidor backend.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  getStatistics();
});
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* full screen height */
  width: 100vw; /* full screen width */
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #0d0d1a;
  color: #ffffff;
  overflow-x: hidden; /* prevent unwanted shrink/scroll */
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
}

.btn-primary:hover {
  background-color: #e60000;
  color: #ffffff;
  box-shadow: 0 0 12px #ffbb33, 0 0 24px #e60000;
}

main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
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

.stats-card {
  background-color: #141432;
  border-radius: 16px;
  border: 2px solid #262673;
  box-shadow: 0 0 15px #262673, 0 0 30px #e60000;
  padding: 2rem;
  width: 100%;
  max-width: 700px;
}

.stats-card h2 {
  font-size: 1.5rem;
  color: #ffbb33;
  text-shadow: 0 0 8px #ffbb33, 0 0 16px #e60000;
  margin-bottom: 0.5rem;
}

.stats-card p {
  color: #aaa;
  font-style: italic;
  margin-bottom: 1.5rem;
}

.loading-state {
  text-align: center;
  font-size: 1.2rem;
  color: #e60000;
  padding: 2rem;
}

.stats-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #262673;
  transition: background-color 0.3s;
}

.stat-item:hover {
  background-color: #1a1a44;
}

.stat-label {
  font-weight: 500;
}

.stat-value {
  color: #ffbb33;
  font-weight: bold;
}

.ai-insight-box {
  background-color: #2a2a53;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 2rem;
  border: 1px solid #5d5d88;
}

.ai-insight-box h3 {
  font-size: 1.2rem;
  color: #90ee90;
  margin-bottom: 0.5rem;
}

.ai-insight-box p {
  color: #e0e0e0;
  line-height: 1.5;
}
</style>
