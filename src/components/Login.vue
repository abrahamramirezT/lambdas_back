<template>
  <div>
    <h2>Iniciar Sesión</h2>
    <!-- Solo debe haber un elemento <form> que contenga todos los campos y el botón -->
    <form @submit.prevent="login">
      <div>
        <label for="username">Usuario:</label> <br>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Contraseña:</label> <br>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Iniciar Sesión</button>
    </form>
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
  },
};
</script>

<style scoped>

input{
  margin:2.5vh
}
button {
  margin: 2.5vh;
}
</style>
