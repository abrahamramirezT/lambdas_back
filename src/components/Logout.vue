<!-- src/components/Logout.vue -->
<template>
    <div>
      <button @click="logout">Cerrar Sesión</button>
    </div>
  </template>
  
  <script>
  export default {
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
  