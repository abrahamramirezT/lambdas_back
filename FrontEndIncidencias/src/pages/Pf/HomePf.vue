<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="userRole" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow flex items-center justify-center p-6">
      <div class="bg-white shadow-md rounded-lg p-8 text-center max-w-lg">
        <h1 class="text-4xl font-semibold mb-4 text-gray-800">¡Bienvenido a la Gestión de Incidencias!</h1>
        <p class="text-gray-600 mb-6">
          Esta es la plataforma donde podrás gestionar y monitorear todas las incidencias de manera eficiente.
        </p>
       
      </div>
    </div>
  </div>
</template>

<script>
import AppNavbar from '@/components/AppNavbar.vue';

export default {
  components: {
    AppNavbar,
  },
  data() {
    return {
      userRole: '', // Inicializar el rol del usuario
    };
  },
  created() {
    this.userRole = localStorage.getItem('role'); // Obtener el rol desde localStorage
  },
  methods: {
    goToDashboard() {
      if (this.userRole === 'admin') {
        this.$router.push('/admin');
      } else if (this.userRole === 'Physical') {
        this.$router.push('/physical');
      } else {
        alert('Rol no reconocido. Por favor, inicia sesión nuevamente.');
        this.$router.push('/login');
      }
    },
  },
};
</script>

<style scoped>
.bg-gray-100 {
  background-color: #ffffff;
}

.bg-white {
  background-color: #273646;
}

.text-gray-800 {
  color: #ffffff;
}

.text-gray-600 {
  color: #ffffff;
}

button:hover {
  background-color: #317b5a;
}
</style>
