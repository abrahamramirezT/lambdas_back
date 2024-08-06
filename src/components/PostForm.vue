<!-- src/components/PostForm.vue -->
<template>
    <div>
      
      <form @submit.prevent="submitForm" class="form">
      <h2>Crear Nuevo</h2>
        <label for="titulo">Título:</label>
        <input type="text" id="titulo" v-model="titulo" required />
  
        <label for="descripcion">Descripción:</label>
        <input type="text" id="descripcion" v-model="descripcion" required />
  
        <label for="fecha">Fecha:</label>
        <input type="date" id="fecha" v-model="fecha" required />
  
        <label for="estatus">Estatus:</label>
        <select id="estatus" v-model="estatus" required>
          <option :value="true">Activo</option>
          <option :value="false">Inactivo</option>
        </select>
  
        <label for="fto">Seleccionar Foto:</label>
        <input type="file" id="fto" @change="handleFileChange" accept="image/*" required />
  
        <button type="submit">Enviar</button>
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
        estatus: true, // Valor por defecto
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
          estatus: this.estatus, // Booleano
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
          // Limpia el formulario después de enviar
          this.titulo = '';
          this.descripcion = '';
          this.fecha = '';
          this.estatus = true; // Valor por defecto
          this.fto_base64 = ''; // Limpia el campo base64
        } catch (error) {
          console.error('Error al enviar el formulario:', error);
          alert('Error al crear el elemento. Inténtalo de nuevo.');
        }
      },
    },
  };
  </script>
  
  <style scoped>

  div{
    display:flex;
    justify-content:center;
  }
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
  