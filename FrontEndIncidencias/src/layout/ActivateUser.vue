<template>
    <div class="flex justify-center items-center h-screen bg-gray-100">
      <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-lg">
        <h2 class="text-3xl text-[#317b5a] font-semibold text-center mb-6">Activar Usuario</h2>
        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label for="username" class="block mb-2 text-sm font-medium text-gray-600">Usuario:</label>
            <input type="text" id="username" v-model="username" required
              class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
          </div>
          
          <div>
            <label for="temporary_password" class="block mb-2 text-sm font-medium text-gray-600">Contraseña Anterior:</label>
            <input type="password" id="temporary_password" v-model="temporary_password" required
              class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
          </div>
          
          <div>
            <label for="new_password" class="block mb-2 text-sm font-medium text-gray-600">Contraseña Nueva:</label>
            <input type="password" id="new_password" v-model="new_password" required
              class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
          </div>
  
          <div class="flex justify-between">
            <button @click="goBack"
              class="px-4 py-2 text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-[#317b5a]">
              Regresar
            </button>
            <button type="submit"
              class="px-4 py-2 text-white bg-[#317b5a] rounded-lg hover:bg-[#35495E] focus:outline-none focus:ring-2 focus:ring-[#317b5a]">
              Enviar
            </button>
            
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {

      return {
        username: '',
        temporary_password: '',
        new_password: '',
      };
    },
    methods: {
      async submitForm() {
        const userData = {
          username: this.username,
          temporary_password: this.temporary_password,
          new_password: this.new_password,
        };
  
        try {
          const response = await axios.post('https://h91d57g3rl.execute-api.us-east-1.amazonaws.com/Stage/change_password', userData, {
            headers: {
              'Content-Type': 'application/json',
            },
          });
          console.log('Respuesta del servidor:', response.data);
          alert('Usuario activado: ' + JSON.stringify(response.data));
          this.$router.push('/login');
        } catch (error) {
          console.error('Error al activar el usuario:', error);
          alert('Error al activar el usuario. Inténtalo de nuevo.');
        }
      },
      goBack() {
        this.$router.push('/login');
      },
    },
  };
  </script>
  
  <style scoped>
  /* La mayoría de los estilos están manejados por Tailwind CSS */
  </style>
  