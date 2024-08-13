<template>
  <div class="flex h-screen w-screen overflow-hidden">
    <!-- Sección izquierda -->
    <div class="hidden lg:flex flex-col justify-center w-1/2 p-8 bg-white">
      <div class="max-w-md mx-auto">
        <div class="mb-8">
          <h3 class="text-sm text-gray-500">Sistema de Gestión de Incidencias</h3>
        </div>
        <div class="mb-8">
          <img src="https://picsum.photos/600/300" alt="Chart" class="rounded-lg" />
        </div>
        <div>
          <p class="mt-4 text-sm text-center text-gray-500">Gestión eficiente de incidencias en un solo lugar:</p>
        </div>
        <div class="mt-12 text-center">
          <h2 class="text-2xl text-[#317b5a] font-semibold">¡Bienvenido de nuevo!</h2>
          <p class="text-gray-500">Gestiona las incidencias de forma rápida y eficiente</p>
        </div>
        <div class="mt-4 flex justify-center space-x-2">
          <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
          <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
          <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
        </div>
      </div>
    </div>

    <!-- Sección derecha (Formulario) -->
    <div class="flex flex-col justify-center w-full lg:w-1/2 p-8 bg-gray-100">
      <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg w-full">
        <h2 class="mb-4 text-3xl text-[#317b5a] font-semibold text-center">¡Bienvenido de nuevo!</h2>
        <p class="mb-8 text-sm text-center text-gray-500">Gestiona las incidencias de forma rápida y eficiente</p>

        <form @submit.prevent="login">
          <div class="mb-4">
            <label for="username" class="block mb-2 text-sm font-medium text-gray-600">Usuario:</label>
            <div class="relative">
              <input type="text" id="username" v-model="username" required
                class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
              <span class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
                <!-- Ícono de usuario -->
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 7l9-5-9-5-9 5-9 5z" />
                </svg>
              </span>
            </div>
          </div>

          <div class="mb-6">
            <label for="password" class="block mb-2 text-sm font-medium text-gray-600">Contraseña:</label>
            <div class="relative">
              <input type="password" id="password" v-model="password" required
                class="w-full px-4 py-2 text-sm bg-gray-100 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#317b5a]" />
              <span class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
                <!-- Ícono de candado -->
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5v14" />
                </svg>
              </span>
            </div>
          </div>

          <div class="mb-4 text-right">
            <a href="#" class="text-sm text-[#317b5a] hover:underline">¿Olvidaste tu contraseña?</a>
          </div>

          <button type="submit"
            class="w-full px-4 py-2 text-white bg-[#317b5a] rounded-lg hover:bg-[#35495E] focus:outline-none focus:ring-2 focus:ring-[#317b5a]">
            Iniciar Sesión
          </button>
        </form>

        <div class="my-6 text-center">
          <span class="text-gray-400">o</span>
        </div>

        <div class="flex justify-between">
          <button @click="goToActivateUser" class="flex items-center justify-center w-full px-4 py-2 text-sm font-semibold text-gray-600 border rounded-lg hover:bg-gray-100">
            <i class="fas fa-user-check mr-2"></i>
            Activar Usuario
          </button>
          <button @click="goToRegisterUser" class="flex items-center justify-center w-full px-4 py-2 ml-2 text-sm font-semibold text-gray-600 border rounded-lg hover:bg-gray-100">
            <i class="fas fa-user-plus mr-2"></i>
            Crear Usuario
          </button>
        </div>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            ¿No tienes una cuenta? <a href="#" class="text-[#317b5a] hover:underline">Regístrate</a>
          </p>
        </div>
      </div>
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
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('https://h91d57g3rl.execute-api.us-east-1.amazonaws.com/Stage/login', {
          username: this.username,
          password: this.password,
        });

        const { id_token, access_token, refresh_token, role } = response.data;

        // Almacena los tokens en el almacenamiento local
        localStorage.setItem('id_token', id_token);
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('role', role);

        // Redirige a la página principal o protegida
        // Redirige según el rol del usuario
      if (role === 'admin') {
        this.$router.push('/home-admin');
      } else if (role === 'pf') {
        this.$router.push('/home-pf');
      } else if (role === 'user') {
        this.$router.push('/home-user');
      } else  {
        this.$router.push('/login');
        alert('No tienes permiso para acceder a esta aplicación.');
      }
    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      alert('Nombre de usuario o contraseña incorrectos.');
    }
  },
    goToRegisterUser() {
      // Redirige a la página de registro
      this.$router.push('/create-user');
    },
    goToActivateUser() {
      // Redirige a la página de activación de usuario
      this.$router.push('/activate-user');
    },
  },
};
</script>

<style scoped>
/* La mayoría de los estilos están manejados por Tailwind CSS */
</style>
