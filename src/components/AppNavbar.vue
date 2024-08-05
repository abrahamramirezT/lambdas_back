<template>
  <nav>
    <ul>
      <li><router-link to="/get-all">Ver Todos</router-link></li>
      <li><router-link to="/post">Agregar</router-link></li>
      <li><router-link to="/put">Actualizar</router-link></li>
      <li v-if="isAuthenticated">
        <button @click="logout">Cerrar Sesión</button>
      </li>
      <!-- Agregar un nuevo botón, por ejemplo, para la página de perfil -->
      <li v-if="isAuthenticated">
        <router-link to="/profile">
          <button>Perfil</button>
        </router-link>
      </li>
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
  background-color: #36986f; /* Color de fondo del navbar */
  color: white; /* Color del texto */
  padding: 10px; /* Espaciado interno */
  font-weight: bold; /* Negrita en el texto */
}

ul {
  list-style-type: none; /* Elimina los puntos de la lista */
  padding: 0; /* Elimina el padding por defecto */
  margin: 0; /* Elimina el margin por defecto */
}

li {
  display: inline; /* Muestra los elementos de la lista en línea */
  margin-right: 10px; /* Espacio entre los elementos de la lista */
}

a {
  color: white; /* Color de los enlaces */
  text-decoration: none; /* Elimina el subrayado de los enlaces */
}

a:hover {
  text-decoration: underline; /* Subrayado en hover */
}

button {
  background-color: #f44336; /* Color de fondo del botón */
  color: white; /* Color del texto del botón */
  border: none; /* Elimina el borde del botón */
  padding: 5px 10px; /* Espaciado interno del botón */
  cursor: pointer; /* Muestra un cursor pointer sobre el botón */
}

button:hover {
  background-color: #d32f2f; /* Color de fondo del botón en hover */
}
</style>
