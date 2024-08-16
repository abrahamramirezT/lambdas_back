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
          :items="filteredItems"
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
      headers: ['ID', 'Título', 'Fecha', 'Descripción', 'Estudiante','Aula','Edificio','Matricula',  'Grado', 'Grupo', 'Division Academica', 'Status', 'Foto'],
    };
  },
  computed: {
    filteredItems() {
      return this.items.filter(item => item.estatus === 2); // Filtrar incidencias pendientes
    },
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
  async fetchItems() {
    try {
      // Obtener las incidencias
      const response = await axios.get('https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/read_all_incidence');
      const incidencias = response.data;

      // Obtener datos relacionados (aulas, edificios, etc.)
      const [aulasRes, edificiosRes, gradosRes, gruposRes, divisionesRes] = await Promise.all([
        axios.get('https://c8eynvsepi.execute-api.us-east-1.amazonaws.com/Stage/read_all_aula'),
        axios.get('https://bqscm2peg3.execute-api.us-east-1.amazonaws.com/Stage/read_all_edificio'),
        axios.get('https://lp51xyfzbk.execute-api.us-east-1.amazonaws.com/Stage/read_all_grado'),
        axios.get('https://xfy9zgjuxf.execute-api.us-east-1.amazonaws.com/Stage/read_all_grupo'),
        axios.get('https://a9mo06q838.execute-api.us-east-1.amazonaws.com/Stage/read_all_div_academica')
      ]);

      const aulas = aulasRes.data;
      const edificios = edificiosRes.data;
      const grados = gradosRes.data;
      const grupos = gruposRes.data;
      const divisiones = divisionesRes.data;

      // Mapear los IDs con los nombres correspondientes
      this.items = incidencias.map(incidencia => {
        const aula = aulas.find(a => a.aula_id === incidencia.aula)?.nombre || 'N/A';
        const edificio = edificios.find(e => e.edificio_id === incidencia.edificio)?.nombre || 'N/A';
        const grado = grados.find(g => g.grado_id === incidencia.grado)?.nombre || 'N/A';
        const grupo = grupos.find(g => g.grupo_id === incidencia.grupo)?.nombre || 'N/A';
        const divisionAcademica = divisiones.find(d => d.div_aca_id === incidencia.div_academica)?.nombre || 'N/A';

        return {
          id: incidencia.reporte_id,
          titulo: incidencia.titulo,
          fecha: incidencia.fecha,
          descripcion: incidencia.descripcion,
          estudiante: incidencia.estudiante,
          aula: aula,
          edificio: edificio,
          matricula: incidencia.matricula,
          grado: grado,
          grupo: grupo,
          div_academica: divisionAcademica,
          estatus: incidencia.estatus,
          fto_url: incidencia.fto_url
        };
      });
    } catch (error) {
      console.error('Error al obtener las incidencias:', error);
      alert('Hubo un problema al cargar las incidencias.');
    }
  },
  // ...
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
