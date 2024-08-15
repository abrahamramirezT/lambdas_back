<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="'admin'" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow p-6">
      <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-2xl font-semibold mb-6">Incidencias Recientes</h1>
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
      headers: ['ID', 'Título', 'Fecha', 'Descripción', 'Estudiante', 'Aula', 'Edificio', 'Matricula', 'Status', 'Grado', 'Grupo', 'División Académica', 'Foto', 'Acciones'],
    };
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      try {
        // Obtener las incidencias
        const response = await axios.get('https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/read_all_incidence');
        const incidencias = response.data.filter(incidencia => incidencia.estatus === 2);

        // Obtener los nombres correspondientes a las IDs foráneas
        const aulaRequests = incidencias.map(incidencia => this.fetchAulaNombre(incidencia.aula));
        const edificioRequests = incidencias.map(incidencia => this.fetchEdificioNombre(incidencia.edificio));
        const divisionRequests = incidencias.map(incidencia => this.fetchDivisionNombre(incidencia.div_academica));
        const gradoRequests = incidencias.map(incidencia => this.fetchGradoNombre(incidencia.grado));
        const grupoRequests = incidencias.map(incidencia => this.fetchGrupoNombre(incidencia.grupo));

        // Esperar a que todas las solicitudes se completen
        const [aulas, edificios, divisiones, grados, grupos] = await Promise.all([
          Promise.all(aulaRequests),
          Promise.all(edificioRequests),
          Promise.all(divisionRequests),
          Promise.all(gradoRequests),
          Promise.all(grupoRequests),
        ]);

        // Mapear los resultados y construir los items con los nombres en lugar de los IDs
        this.items = incidencias.map((incidencia, index) => ({
          reporte_id: incidencia.reporte_id,
          titulo: incidencia.titulo,
          fecha: incidencia.fecha,
          descripcion: incidencia.descripcion,
          estudiante: incidencia.estudiante,
          aula: aulas[index], // Usar el nombre del aula
          edificio: edificios[index], // Usar el nombre del edificio
          matricula: incidencia.matricula,
          grado: grados[index], // Usar el nombre del grado
          grupo: grupos[index], // Usar el nombre del grupo
          div_academica: divisiones[index], // Usar el nombre de la división académica
          estatus: incidencia.estatus,
          fto_url: incidencia.fto_url,
        }));
      } catch (error) {
        console.error('Error al obtener las incidencias:', error);
        alert('Hubo un problema al cargar las incidencias.');
      }
    },
    async fetchAulaNombre(id) {
      try {
        const response = await axios.get(`https://api.example.com/aulas/${id}`);
        return response.data.nombre; // Asume que el nombre viene en 'nombre'
      } catch (error) {
        console.error('Error al obtener el nombre del aula:', error);
        return 'Desconocido'; // Manejo de errores si no se puede obtener el nombre
      }
    },
    async fetchEdificioNombre(id) {
      try {
        const response = await axios.get(`https://api.example.com/edificios/${id}`);
        return response.data.nombre; // Asume que el nombre viene en 'nombre'
      } catch (error) {
        console.error('Error al obtener el nombre del edificio:', error);
        return 'Desconocido'; // Manejo de errores si no se puede obtener el nombre
      }
    },
    async fetchDivisionNombre(id) {
      try {
        const response = await axios.get(`https://api.example.com/divisiones/${id}`);
        return response.data.nombre; // Asume que el nombre viene en 'nombre'
      } catch (error) {
        console.error('Error al obtener el nombre de la división académica:', error);
        return 'Desconocido'; // Manejo de errores si no se puede obtener el nombre
      }
    },
    async fetchGradoNombre(id) {
      try {
        const response = await axios.get(`https://api.example.com/grados/${id}`);
        return response.data.nombre; // Asume que el nombre viene en 'nombre'
      } catch (error) {
        console.error('Error al obtener el nombre del grado:', error);
        return 'Desconocido'; // Manejo de errores si no se puede obtener el nombre
      }
    },
    async fetchGrupoNombre(id) {
      try {
        const response = await axios.get(`https://api.example.com/grupos/${id}`);
        return response.data.nombre; // Asume que el nombre viene en 'nombre'
      } catch (error) {
        console.error('Error al obtener el nombre del grupo:', error);
        return 'Desconocido'; // Manejo de errores si no se puede obtener el nombre
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
      headers: ['ID', 'Título', 'Fecha', 'Descripción', 'Estudiante','Aula','Edificio','Matricula', 'Status','Grado','Grupo','Division Academica', 'Foto', 'Acciones'],
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
          grado: incidencia.grado,
          grupo: incidencia.grupo,
          div_academica: incidencia.div_academica,
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
