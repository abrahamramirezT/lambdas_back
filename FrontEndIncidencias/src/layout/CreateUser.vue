<template>
    <div class="flex justify-center items-center h-screen bg-gray-100">
      <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-lg">
        <h2 class="text-3xl text-[#317b5a] font-semibold text-center mb-6">Crear Usuario</h2>
        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label for="email" class="block mb-2 text-sm font-medium text-gray-600">Correo:</label>
            <input type="email" id="email" v-model="email" required
              class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
          </div>

          <div>
            <label for="username" class="block mb-2 text-sm font-medium text-gray-600">Usuario:</label>
            <input type="text" id="username" v-model="username" required
              class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
          </div>
          
          <div>
            <label for="password" class="block mb-2 text-sm font-medium text-gray-600">Contraseña:</label>
            <input type="password" id="password" v-model="password" required
              class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
          </div>
  
         
  
          <div class="flex justify-between">
            <button @click="goBack"
              class="px-4 py-2 text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-[#317b5a]">
              Regresar
            </button>
            <button type="submit"
              class="px-4 py-2 text-white bg-[#317b5a] rounded-lg hover:bg-[#35495E] focus:outline-none focus:ring-2 focus:ring-[#317b5a]">
              Crear Usuario
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
        password: '',
        email: '',
      };
    },
    methods: {
      async submitForm() {
        const newUser = {
          username: this.username,
          password: this.password,
          email: this.email,
        };
  
        try {
          const response = await axios.post('https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/create_user', newUser, {
            headers: {
              'Content-Type': 'application/json',
            },
          });
          console.log('Respuesta del servidor:', response.data);
          alert('Usuario creado: ' + JSON.stringify(response.data));
          this.$router.push('/login');
        } catch (error) {
          console.error('Error al crear el usuario:', error);
          alert('Error al crear el usuario. Inténtalo de nuevo.');
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
  