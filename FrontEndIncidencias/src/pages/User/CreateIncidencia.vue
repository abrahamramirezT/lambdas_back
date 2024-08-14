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

            
            <div class="mb-4">
              <label for="aula" class="block text-sm font-medium text-gray-700">Aula:</label>
              <input 
                type="text" 
                id="aula" 
                v-model="form.aula" 
                required 
                class="mt-1 p-2 w-full border rounded-md"
              />
            </div>

  

            
            <div class="mb-4">
  <label for="estatus" class="block text-sm font-medium text-gray-700">Edicio:</label>
  <select 
    id="edificio" 
    v-model="form.edificio" 
    required 
    class="mt-1 p-2 w-full border rounded-md"
  >
    <option value="Docencia 1">Docencia 1</option>
    <option value="Docencia 2">Docencia 2</option>
    <option value="Docencia 3">Docencia 3</option>
    <option value="Docencia 4">Docencia 4</option>
    <option value="Docencia 5">Docencia 5</option>
    <option value="Cecadec">Cecadec</option>
    <option value="Biblioteca">Biblioteca</option>
    <option value="Rectoria">Rectoria</option>

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
          estatus: '1',
          fto_base64: '',
          user_id:''
        },
      };
    },
    methods: {
      async submitForm() {
        try {
          const response = await axios.post('https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/create_incidence', this.form);
          alert('Incidencia creada exitosamente.');
          this.$router.push('/home-user'); // Redirige a la página principal después de crear la incidencia
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
  
  .float-right {
    float: right;
  }
  </style>
  