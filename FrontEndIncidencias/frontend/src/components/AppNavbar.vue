<!-- src/components/AppNavbar.vue -->
<template>
  <nav>
    <ul>
      <li><router-link to="/get-all">Ver Todos</router-link></li>
      <li><router-link to="/post">Agregar</router-link></li>
      <li v-if="isAuthenticated"><button @click="logout">Cerrar Sesión</button></li>
    </ul>
  </nav>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      // Verifica si el usuario está autenticado
      return !!localStorage.getItem('id_token');
    }
  },
  methods: {
    logout() {
      // Elimina los tokens del almacenamiento local
      localStorage.removeItem('id_token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('role');
      
      // Redirige al usuario a la página de inicio de sesión
      this.$router.push('/login');
    }
  }
}
</script>

<style>
nav {
  background-color: #36986f;
  color: white;
  padding: 10px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline;
  margin-right: 10px;
}
button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}
button:hover {
  background-color: #d32f2f;
}
</style>
