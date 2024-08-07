<template>
    <div>
      <h2>Registrar Usuario</h2>
      <form @submit.prevent="submitForm">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="nombre" required />
  
        <label for="apellido_paterno">Apellido Paterno:</label>
        <input type="text" id="apellido_paterno" v-model="apellido_paterno" required />
  
        <label for="apellido_materno">Apellido Materno:</label>
        <input type="text" id="apellido_materno" v-model="apellido_materno" required />
  
        <label for="user">Username:</label>
        <input type="text" id="user" v-model="user" required />
  
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
  
        <button type="submit">Enviar</button>
      </form>
  
      <!-- Botón de regresar -->
      <button @click="goBack">Regresar</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        nombre: '',
        apellido_paterno: '',
        apellido_materno: '',
        user: '',
        password: '', 
      };
    },
    methods: {
      async submitForm() {
        const newItem = {
          nombre: this.nombre,
          apellido_paterno: this.apellido_paterno,
          apellido_materno: this.apellido_materno,
          user: this.user,
          password: this.password, 
        };
  
        try {
          const response = await axios.post('https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/create_user', newItem, {
            headers: {
              'Content-Type': 'application/json'
            }
          });
          console.log('Respuesta del servidor:', response.data);
          alert('Elemento creado: ' + JSON.stringify(response.data));
          // Redirige al inicio de sesión después de crear el usuario
          this.$router.push('/login');
        } catch (error) {
          console.error('Error al enviar el formulario:', error);
          alert('Error al crear el elemento. Inténtalo de nuevo.');
        }
      },
      goBack() {
        // Redirige a la página de inicio de sesión
        this.$router.push('/login');
      },
    },
  };
  </script>
  
  <style scoped>
  form {
    display: flex;
    flex-direction: column;
  }
  
  label {
    margin: 5px 0;
  }
  
  input, select {
    margin-bottom: 10px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  button:hover {
    background-color: #36986f;
  }
  </style>
  