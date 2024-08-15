<template>
  <nav class="flex flex-col h-screen bg-blue-900 text-white w-1/5">
    <div class="flex items-center justify-center h-20 bg-blue-800">
      <!-- Logo -->
    </div>
    <div class="flex-grow mt-6">
      <ul class="space-y-4">
        <!-- Navigation Links -->

        <li 
          v-if="role === 'admin'" 
          class="px-4 py-2 hover:bg-blue-800 rounded-md"
          :class="{ 'bg-blue-700': isActive('/home-admin') }"
        >
          <router-link to="/home-admin" class="flex items-center">
            <i class="fas fa-tachometer-alt mr-3"></i>
            <span>Home</span>
          </router-link>
        </li>

        <li 
          v-if="role === 'admin'" 
          class="px-4 py-2 hover:bg-blue-800 rounded-md"
          :class="{ 'bg-blue-700': isActive('/admin-hechas') }"
        >
          <router-link to="/admin-hechas" class="flex items-center">
            <i class="fas fa-clipboard-check mr-3"></i>
            <span>Incidencias Hechas</span>
          </router-link>
        </li>

        <li 
          v-if="role === 'admin'" 
          class="px-4 py-2 hover:bg-blue-800 rounded-md"
          :class="{ 'bg-blue-700': isActive('/admin-autorizadas') }"
        >
          <router-link to="/admin-autorizadas" class="flex items-center">
            <i class="fas fa-clipboard-check mr-3"></i>
            <span>Incidencias Autorizadas</span>
          </router-link>
        </li>

        <li
          v-if="role === 'user'"
          class="px-4 py-2 hover:bg-blue-800 rounded-md"
          :class="{ 'bg-blue-700': isActive('/home-user') }"
        >
          <router-link to="/home-user" class="flex items-center">
            <i class="fas fa-clipboard-check mr-3"></i>
            <span>Home</span>
          </router-link>
        </li>

        <li 
          v-if="role === 'user'" 
          class="px-4 py-2 hover:bg-blue-800 rounded-md"
          :class="{ 'bg-blue-700': isActive('/create-incidencia') }"
        >
          <router-link to="/create-incidencia" class="flex items-center">
            <i class="fas fa-clipboard-check mr-3"></i>
            <span>Crear Incidencia</span>
          </router-link>
        </li>

        <li 
          v-if="role === 'pf'" 
          class="px-4 py-2 hover:bg-blue-800 rounded-md"
          :class="{ 'bg-blue-700': isActive('/home-pf') }"
        >
          <router-link to="/home-pf" class="flex items-center">
            <i class="fas fa-clipboard-check mr-3"></i>
            <span>Home</span>
          </router-link>
        </li>

        <li 
          v-if="role === 'pf'" 
          class="px-4 py-2 hover:bg-blue-800 rounded-md"
          :class="{ 'bg-blue-700': isActive('/pf-hechas') }"
        >
          <router-link to="/pf-hechas" class="flex items-center">
            <i class="fas fa-clipboard-check mr-3"></i>
            <span>Incidencias Hechas</span>
          </router-link>
        </li>
      </ul>
    </div>
    <!-- Botón de Cerrar Sesión -->
    <div class="flex items-center justify-center h-20 bg-blue-800">
      <button @click="logout" class="flex items-center justify-center w-full text-center text-white hover:bg-blue-700 px-4 py-2 rounded-md">
        <i class="fas fa-sign-out-alt mr-3"></i>
        <span>Cerrar Sesión</span>
      </button>
    </div>
  </nav>
</template>

<script>
import { useRoute } from 'vue-router';

export default {
  props: {
    role: {
      type: String,
      required: true,
    },
  },
  setup() {
    const route = useRoute();

    // Función para determinar si la ruta actual coincide con el link
    const isActive = (path) => {
      return route.path.startsWith(path); // Compara si la ruta comienza con el prefijo
    };

    return {
      isActive,
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('id_token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('role');
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
/* Ajustes adicionales */
nav {
  width: 16%; /* Ajustar ancho de la barra de navegación */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  transition: background-color 0.3s ease;
}

li:hover {
  background-color: #42b883; /* Color de fondo al pasar el cursor */
}

.bg-blue-700 {
  background-color: #317b5a; /* Color de fondo cuando está activo */
}

.bg-blue-800 {
  background-color: #273646; /* Fondo de los botones y navbar */
}

.bg-blue-900 {
  background-color: #273646; /* Fondo del navbar */
}

button:hover {
  background-color: #bd0903; /* Fondo al pasar el cursor sobre el botón de cerrar sesión */
}
</style>
