<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="'pf'" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow p-6 overflow-y-auto">
      <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-2xl font-semibold mb-6">Actualizar Incidencia</h1>

        <form @submit.prevent="submitForm">
          <div class="mb-4">
            <label for="titulo" class="block text-sm font-medium text-gray-700">Título:</label>
            <input 
              type="text" 
              id="titulo" 
              v-model="form.titulo" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>

          <div class="mb-4">
            <label for="descripcion" class="block text-sm font-medium text-gray-700">Descripción:</label>
            <textarea 
              id="descripcion" 
              v-model="form.descripcion" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            ></textarea>
          </div>

          <div class="mb-4">
            <label for="fecha" class="block text-sm font-medium text-gray-700">Fecha:</label>
            <input 
              type="date" 
              id="fecha" 
              v-model="form.fecha" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>

          <div class="mb-4">
            <label for="estatus" class="block text-sm font-medium text-gray-700">Estatus:</label>
            <select 
              id="estatus" 
              v-model="form.estatus" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option value="1">Pendiente</option>
              <option value="2">En Progreso</option>
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

          <div class="mb-4">
            <label for="estudiante" class="block text-sm font-medium text-gray-700">Estudiante:</label>
            <input 
              type="text" 
              id="estudiante" 
              v-model="form.estudiante" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>
          
          <div class="mb-4">
            <label for="aula" class="block text-sm font-medium text-gray-700">Aula:</label>
            <input 
              type="text" 
              id="aula" 
              v-model="form.aula_nombre" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>

          <div class="mb-4">
            <label for="edificio" class="block text-sm font-medium text-gray-700">Edificio:</label>
            <input 
              type="text" 
              id="edificio" 
              v-model="form.edificio_nombre" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>

          <div class="mb-4">
            <label for="matricula" class="block text-sm font-medium text-gray-700">Matricula:</label>
            <input 
              type="text" 
              id="matricula" 
              v-model="form.matricula" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>
          
          <div class="mb-4">
            <label for="grado" class="block text-sm font-medium text-gray-700">Grado:</label>
            <input 
              type="text" 
              id="grado" 
              v-model="form.grado_nombre" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>

          <div class="mb-4">
            <label for="grupo" class="block text-sm font-medium text-gray-700">Grupo:</label>
            <input 
              type="text" 
              id="grupo" 
              v-model="form.grupo_nombre" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>

          <div class="mb-4">
            <label for="div_academica" class="block text-sm font-medium text-gray-700">División Académica:</label>
            <input 
              type="text" 
              id="div_academica" 
              v-model="form.div_academica_nombre" 
              required 
              class="mt-1 p-2 w-full border rounded-md"
              disabled
            />
          </div>

          <button 
            type="submit" 
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Actualizar Incidencia
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
        estatus: '',
        fto_base64: ''
      },
    };
  },
  created() {
    this.fetchIncidencia();
  },
  methods: {
    async fetchIncidencia() {
      const reporteId = this.$route.params.reporte_id;
      try {
        const response = await axios.get(`https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/read_one_incidence/${reporteId}`);
        const incidencia = response.data;
        this.form = {
          titulo: incidencia.titulo,
          descripcion: incidencia.descripcion,
          estudiante: incidencia.estudiante,
          aula_nombre: incidencia.aula_nombre,
          edificio_nombre: incidencia.edificio_nombre,
          matricula: incidencia.matricula,
          fecha: incidencia.fecha,
          estatus: incidencia.estatus,
          grado_nombre: incidencia.grado_nombre,
          grupo_nombre: incidencia.grupo_nombre,
          div_academica_nombre: incidencia.div_academica_nombre,
          fto_base64: ''
        };
      } catch (error) {
        console.error('Error al obtener la incidencia:', error);
        alert('Hubo un problema al cargar la incidencia.');
      }
    },
    async submitForm() {
      const reporteId = this.$route.params.reporte_id;
      const data = {
        id: reporteId,
        estatus: this.form.estatus,
        fto_base64: this.form.fto_base64, // Este campo solo se envía si se selecciona una imagen
      };
      
      try {
        await axios.put(`https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/update_incidence/${reporteId}`, data);
        alert('Incidencia actualizada exitosamente.');
        this.$router.push('/home-pf');
      } catch (error) {
        console.error('Error al actualizar la incidencia:', error);
        alert('Hubo un problema al actualizar la incidencia.');
      }
    },

    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.form.fto_base64 = e.target.result.split(',')[1];
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
