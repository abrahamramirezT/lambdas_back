<template>
    <div>
      <h2>Activar Usuario</h2>
      <form @submit.prevent="submitForm">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
  
        <label for="temporary_password">Contraseña Anterior:</label>
        <input type="text" id="temporary_password" v-model="temporary_password" required />
  
        <label for="new_password">Contraseña Nueva:</label>
        <input type="text" id="new_password" v-model="new_password" required />

  
        <button type="submit">Enviar</button>
        <button @click="goBack">Regresar</button>

      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        titulo: '',
        descripcion: '',
        fecha: '',
        estatus: '1', // Valor por defecto
        fto_base64: '', // Almacena la imagen en base64
      };
    },
    methods: {
      handleFileChange(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            // Convierte el archivo a base64 y lo almacena en fto_base64
            this.fto_base64 = e.target.result.split(',')[1]; // Obtiene solo la parte Base64
          };
          reader.readAsDataURL(file);
        }
      },
      async submitForm() {
        const newItem = {
          titulo: this.titulo,
          fecha: this.fecha,
          descripcion: this.descripcion,
          estatus: this.estatus,
          fto_base64: this.fto_base64, // Base64 de la imagen
        };
  
        try {
          const response = await axios.post('https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/create_incidence', newItem, {
            headers: {
              'Content-Type': 'application/json'
            }
          });
          console.log('Respuesta del servidor:', response.data);
          alert('Elemento creado: ' + JSON.stringify(response.data));
          // Redirige a la vista de todos los elementos después de crear la incidencia
          this.$router.push('/get-all');
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
  }
  
  button:hover {
    background-color: #36986f;
  }
  </style>
  