<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="'user'" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow p-6 overflow-y-auto">
      <!-- Sección de Dashboard -->
      <div class="bg-white shadow-md rounded-lg p-6 mb-6">
        <!-- Tabla de Incidencias -->
        <h2 class="text-xl font-semibold mb-4">Incidencias Pendientes de Arreglar</h2>
        <DataTable
          title="Ver Todos"
          :items="filteredItems"
          :headers="headers"
          :role="'admin'"
          @approve-item="approveItem"
          @reject-item="rejectItem"
        />
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/AppNavbar.vue';
import DataTable from '@/components/DataTable.vue';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';

export default {
  components: {
    AppNavbar,
    DataTable,
  },
  data() {
    return {
      items: [],
      headers: ['ID', 'Título', 'Fecha', 'Descripción', 'Estudiante', 'Aula', 'Edificio', 'Matricula','Grado', 'Grupo', 'Division Academica', 'Status', 'Foto'],
    };
  },
  computed: {
    filteredItems() {
      return this.items.filter(item => item.estatus === 1); // Filtrar incidencias pendientes
    },
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get('https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/read_all_incidence');
        this.items = response.data.map(incidencia => ({
          id: incidencia.reporte_id,
          titulo: incidencia.titulo,
          fecha: incidencia.fecha,
          descripcion: incidencia.descripcion,
          estudiante: incidencia.estudiante,
          aula: incidencia.aula,
          edificio: incidencia.edificio,
          matricula: incidencia.matricula,
          grado: incidencia.grado,
          grupo: incidencia.grupo,
          div_academica: incidencia.div_academica,
          estatus: incidencia.estatus,
          fto_url: incidencia.fto_url
        }));
      } catch (error) {
        console.error('Error al obtener las incidencias:', error);
        alert('Hubo un problema al cargar las incidencias.');
      }
    },
    approveItem(id) {
      // Lógica para aprobar la incidencia
      alert(`Incidencia ${id} aprobada`);
      // Llamar al API para actualizar el estatus de la incidencia
      this.fetchItems(); // Refresca la lista después de aprobar/rechazar
    },
    rejectItem(id) {
      // Lógica para rechazar la incidencia
      alert(`Incidencia ${id} rechazada`);
      // Llamar al API para actualizar el estatus de la incidencia
      this.fetchItems(); // Refresca la lista después de aprobar/rechazar
    },
    
  },
  mounted() {
    this.fetchItems();
  },
};
</script>

<style scoped>
/* Estilos adicionales para el layout */
.bg-gray-100 {
  background-color: #f7f7f7;
}

.flex-grow {
  overflow-y: auto;
}

button:hover {
  background-color: #317b5a;
}
</style>
