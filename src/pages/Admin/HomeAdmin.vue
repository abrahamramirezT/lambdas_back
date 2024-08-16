  <template>
    <div class="flex h-screen bg-gray-100">
      <!-- Navbar -->
      <AppNavbar :role="'admin'" class="w-64 bg-white shadow-lg" />

      <!-- Contenido Principal -->
      <div class="flex-grow p-6 overflow-y-auto">
        <!-- Sección de Dashboard -->
        <div class="bg-white shadow-md rounded-lg p-6 mb-6">
          <h1 class="text-2xl font-semibold mb-6">Dashboard de Incidencias</h1>

          <!-- Gráficas -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-white shadow-md rounded-lg p-4">
              <canvas id="chart1"></canvas>
            </div>
            <div class="bg-white shadow-md rounded-lg p-4">
              <canvas id="chart2"></canvas>
            </div>
            <div class="bg-white shadow-md rounded-lg p-4">
              <canvas id="chart3"></canvas>
            </div>
          </div>

          <!-- Tabla de Incidencias -->
          <h2 class="text-xl font-semibold mb-4">Incidencias Pendientes de Arreglar</h2>
          <DataTable
            title="Ver Todos"
            :items="filteredItems"
            :headers="headers"
            @approve-item="approveItem"
            @reject-item="rejectItem"
            :role="'admin'"
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
        headers: ['ID', 'Título', 'Fecha', 'Descripción', 'Estudiante', 'Aula', 'Edificio', 'Matricula', 'Grado', 'Grupo', 'Division Academica','Status','Foto', 'Acciones'],
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
          fto_url: incidencia.fto_url,
          actions: true

        };
        
      });
      this.renderCharts();
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
      renderCharts() {
        Chart.register(...registerables);

        // Gráfico 1 - Doughnut Chart
        const ctx1 = document.getElementById('chart1').getContext('2d');
        new Chart(ctx1, {
          type: 'doughnut',
          data: {
            labels: ['Pendientes', 'En Progreso', 'Completadas'],
            datasets: [{
              data: [
                this.items.filter(item => item.estatus === 1).length,
                this.items.filter(item => item.estatus === 2).length,
                this.items.filter(item => item.estatus === 3).length
              ],
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          }
        });

        // Gráfico 2 - Bar Chart
        const ctx2 = document.getElementById('chart2').getContext('2d');
        new Chart(ctx2, {
          type: 'bar',
          data: {
            labels: ['Enero', 'Febrero', 'Marzo', 'Abril'],
            datasets: [{
              label: 'Incidencias por mes',
              data: [10, 15, 20, 25],
              backgroundColor: '#42A5F5',
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          }
        });

        // Gráfico 3 - Line Chart
        const ctx3 = document.getElementById('chart3').getContext('2d');
        new Chart(ctx3, {
          type: 'line',
          data: {
            labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'],
            datasets: [{
              label: 'Incidencias resueltas',
              data: [5, 10, 3, 8],
              borderColor: '#66BB6A',
              fill: false,
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          }
        });
      }
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
