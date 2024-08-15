<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="'user'" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow p-6 overflow-y-auto">
      <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-2xl font-semibold mb-6">Crear Nueva Incidencia</h1>

        <form @submit.prevent="submitForm">
          <!-- Otros campos del formulario -->

          <!-- Selector de Aula -->
          <div class="mb-4">
            <label for="aula" class="block text-sm font-medium text-gray-700">Aula:</label>
            <select 
              id="aula" 
              v-model="form.aula" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option v-for="aula in aulas" :key="aula.id" :value="aula.id">
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
              <option v-for="edificio in edificios" :key="edificio.id" :value="edificio.id">
                {{ edificio.nombre }}
              </option>
            </select>
          </div>

          <!-- Otros campos del formulario -->

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
        estatus: '1',
        fto_base64: '',
      },
      aulas: [], // Array para almacenar las aulas
      edificios: [], // Array para almacenar los edificios
    };
  },
  mounted() {
    this.fetchAulas();
    this.fetchEdificios();
  },
  methods: {
    async fetchAulas() {
      try {
        const response = await axios.get('https://tu-api.com/aulas'); // Reemplaza con tu endpoint
        this.aulas = response.data; // Asume que la API devuelve un array de aulas con { id, nombre }
      } catch (error) {
        console.error('Error al obtener las aulas:', error);
      }
    },
    async fetchEdificios() {
      try {
        const response = await axios.get('https://tu-api.com/edificios'); // Reemplaza con tu endpoint
        this.edificios = response.data; // Asume que la API devuelve un array de edificios con { id, nombre }
      } catch (error) {
        console.error('Error al obtener los edificios:', error);
      }
    },
    async submitForm() {
      try {
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
