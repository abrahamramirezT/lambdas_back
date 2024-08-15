<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="'user'" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow p-6 overflow-y-auto">
      <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-2xl font-semibold mb-6">Crear Nueva Incidencia</h1>

        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label for="titulo" class="block text-sm font-medium text-gray-700">Título:</label>
            <input 
              type="text" 
              id="titulo" 
              v-model="form.titulo" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            />
          </div>

          <div class="mb-4">
            <label for="descripcion" class="block text-sm font-medium text-gray-700">Descripción:</label>
            <textarea 
              id="descripcion" 
              v-model="form.descripcion" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            ></textarea>
          </div>

          <div class="mb-4">
            <label for="estudiante" class="block text-sm font-medium text-gray-700">Estudiante:</label>
            <input 
              type="text" 
              id="estudiante" 
              v-model="form.estudiante" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            />
          </div>

          <!-- Selector de Aula -->
          <div class="mb-4">
            <label for="aula" class="block text-sm font-medium text-gray-700">Aula:</label>
            <select 
              id="aula" 
              v-model="form.aula" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option v-for="aula in aulas" :key="aula.id" :value="aula.aula_id">
                {{ aula.nombre }}
              </option>
            </select>
          </div>

          <!-- Selector de Edificio -->
          <div class="mb-4">
            <label for="edificio" class="block text-sm font-medium text-gray-700">Edificio:</label>
            <select 
              id="edificio" 
              v-model="form.edificio" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option v-for="edificio in edificios" :key="edificio.id" :value="edificio.edificio_id">
                {{ edificio.nombre }}
              </option>
            </select>
          </div>

          <!-- Selector de División Académica -->
          <div class="mb-4">
            <label for="div_academica" class="block text-sm font-medium text-gray-700">División Académica:</label>
            <select 
              id="div_academica" 
              v-model="form.div_academica" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option v-for="div_academica in div_academicas" :key="div_academica.id" :value="div_academica.div_aca_id">
                {{ div_academica.nombre }}
              </option>
            </select>
          </div>

          <!-- Selector de Grado -->
          <div class="mb-4">
            <label for="grado" class="block text-sm font-medium text-gray-700">Grado:</label>
            <select 
              id="grado" 
              v-model="form.grado" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option v-for="grado in grados" :key="grado.id" :value="grado.grado_id">
                {{ grado.nombre }}
              </option>
            </select>
          </div>

          <!-- Selector de Grupo -->
          <div class="mb-4">
            <label for="grupo" class="block text-sm font-medium text-gray-700">Grupo:</label>
            <select 
              id="grupo" 
              v-model="form.grupo" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option v-for="grupo in grupos" :key="grupo.id" :value="grupo.grupo_id">
                {{ grupo.nombre }}
              </option>
            </select>
          </div>

          <div class="mb-4">
            <label for="matricula" class="block text-sm font-medium text-gray-700">Matricula:</label>
            <input 
              type="text" 
              id="matricula" 
              v-model="form.matricula" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            />
          </div>

          <div class="mb-4">
            <label for="fecha" class="block text-sm font-medium text-gray-700">Fecha:</label>
            <input 
              type="date" 
              id="fecha" 
              v-model="form.fecha" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            />
          </div>

          <div class="mb-4">
            <label for="estatus" class="block text-sm font-medium text-gray-700">Estatus:</label>
            <select 
              id="estatus" 
              v-model="form.estatus" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            >
              <option value="1">Pendiente</option>
            </select>
          </div>

          <div class="mb-4">
            <label for="foto" class="block text-sm font-medium text-gray-700">Subir Foto:</label>
            <input 
              type="file" 
              id="foto" 
              @change="onFileChange" 
              accept="image/*" 
              class="mt-1 p-2 w-full border rounded-md"
            />
          </div>

          <button 
            type="submit" 
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Enviar Incidencia
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/AppNavbar.vue';
import axios from 'axios';

export default {
  components: {
    AppNavbar,
  },
  data() {
    return {
      form: {
        titulo: '',
        descripcion: '',
        fecha: '',
        estudiante: '',
        aula: '',
        edificio: '',
        matricula: '',
        div_academica: '',
        grado: '',
        grupo: '',
        estatus: '1',
        fto_base64: '',
      },
      aulas: [], // Array para almacenar las aulas
      edificios: [], // Array para almacenar los edificios
      grados: [],
      grupos: [],
      div_academicas: [],
    };
  },
  mounted() {
    this.fetchAulas();
    this.fetchEdificios();
    this.fetchDivisionesAcademicas();
    this.fetchGrado();
    this.fetchGrupo();
  },
  methods: {
    async fetchAulas() {
      try {
        const response = await axios.get('https://c8eynvsepi.execute-api.us-east-1.amazonaws.com/Stage/read_all_aula');
        this.aulas = response.data; // Asume que la API devuelve un array de aulas con { id, nombre }
        console.log(this.aulas); // Verifica que los datos se están cargando correctamente

      } catch (error) {
        console.error('Error al obtener las aulas:', error);
      }

    },
    async fetchEdificios() {
      try {
        const response = await axios.get('https://bqscm2peg3.execute-api.us-east-1.amazonaws.com/Stage/read_all_edificio');
        this.edificios = response.data; // Asume que la API devuelve un array de edificios con { id, nombre }
      } catch (error) {
        console.error('Error al obtener los edificios:', error);
      }
    },
    async fetchDivisionesAcademicas() {
      try {
        const response = await axios.get('https://a9mo06q838.execute-api.us-east-1.amazonaws.com/Stage/read_all_div_academica');
        this.div_academicas = response.data; // Asume que la API devuelve un array de divisiones académicas con { id, nombre }
      } catch (error) {
        console.error('Error al obtener las divisiones académicas:', error);
      }
    },
    async fetchGrado() {
      try {
        const response = await axios.get('https://lp51xyfzbk.execute-api.us-east-1.amazonaws.com/Stage/read_all_grado');
        this.grados = response.data; // Asume que la API devuelve un array de grados con { id, nombre }
        console.log(this.grados); 

      } catch (error) {
        console.error('Error al obtener los grados:', error);
      }
    },
    async fetchGrupo() {
      try {
        const response = await axios.get('https://xfy9zgjuxf.execute-api.us-east-1.amazonaws.com/Stage/read_all_grupo');
        this.grupos = response.data; // Asume que la API devuelve un array de grupos con { id, nombre }
        console.log(this.grupos); 
      } catch (error) {
        console.error('Error al obtener los grupos:', error);
      }
    },
    async submitForm() {
      try {
        console.log("Datos enviados:", this.form); 
        const response = await axios.post('https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/create_incidence', this.form);
        alert('Incidencia creada exitosamente.');
        this.$router.push('/home-user');
      } catch (error) {
        console.error('Error al crear la incidencia:', error);
        alert('Hubo un problema al crear la incidencia.');
      }
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.form.fto_base64 = e.target.result.split(',')[1]; // Guardar solo la parte base64
        };
        reader.readAsDataURL(file);
      }
    },
  },
};
</script>

<style scoped>
.bg-gray-100 {
  background-color: #f7f7f7;
}
</style>
