<template>
  <div>
    <h2>Iniciar Sesión</h2>
    <form @submit.prevent="login">
      <label for="username">Usuario:</label>
      <input type="text" id="username" v-model="username" required />

      <label for="password">Contraseña:</label>
      <input type="password" id="password" v-model="password" required />

      <button type="submit">Iniciar Sesión</button>
    </form>

    <!-- Botón adicional para redirigir a otra página -->
    <button @click="goToRegisterUser">Registro User</button>
    <button @click="goToActivateUser">Activacion User</button>
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
        const response = await axios.post('https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/login', {
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
        this.$router.push('/get-all');
      } catch (error) {
        console.error('Error al iniciar sesión:', error);
        alert('Nombre de usuario o contraseña incorrectos.');
      }
    },
    goToRegisterUser() {
      // Redirige a la página de registro
      this.$router.push('/post_user');
    },
    goToActivateUser() {
      // Redirige a la página de registro
      this.$router.push('/activate_user');
    },
  },
};
</script>
