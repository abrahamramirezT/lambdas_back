<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="'pf'" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow p-6">
      <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-2xl font-semibold mb-6">Incidencias En Progreso</h1>
        <DataTable
          title="Ver Todos"
          :items="items"
          :headers="headers"
          @edit-item="editItem"
          @delete-item="deleteItem"
        />
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/AppNavbar.vue';
import DataTable from '@/components/DataTable.vue';
import axios from 'axios';

export default {
  components: {
    AppNavbar,
    DataTable,
  },
  data() {
    return {
      items: [],
      headers: ['ID', 'Título', 'Fecha', 'Descripción', 'Estudiante','Aula','Edificio','Matricula', 'Status', 'Foto'],
    };
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
    try {
      const response = await axios.get('https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/read_all_incidence');
      // Filtrar las incidencias para que solo se muestren las que tienen estatus 1
      this.items = response.data
        .filter(incidencia => incidencia.estatus === 2) // Filtrar incidencias con estatus 1
        .map(incidencia => ({
          reporte_id: incidencia.reporte_id,
          titulo: incidencia.titulo,
          fecha: incidencia.fecha,
          descripcion: incidencia.descripcion,
          estudiante: incidencia.estudiante,
            aula: incidencia.aula,
            edificio: incidencia.edificio,
            matricula: incidencia.matricula,
          estatus: incidencia.estatus,
          fto_url: incidencia.fto_url,
          }));
    } catch (error) {
      console.error('Error al obtener las incidencias:', error);
      alert('Hubo un problema al cargar las incidencias.');
    }
  },
    editItem(item) {
      this.$router.push({ path: '/put', query: { reporte_id: item.reporte_id } });
    },
    deleteItem(id) {
      if (confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
        alert('Elemento eliminado correctamente.');
        this.fetchItems(); // Actualiza la lista después de eliminar
      }
    },
  },
};
</script>

<style scoped>
.bg-gray-100 {
  background-color: #f7f7f7;
}

.float-right {
  float: right;
}
</style>
