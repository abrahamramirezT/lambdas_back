<!-- src/components/PutForm.vue -->
<template>
    <div>
      
      <form @submit.prevent="updateItem">
      <h2>Actualizar Elemento</h2>
        <label for="id">ID del Elemento:</label>
        <input type="number" id="reporte_id" v-model="reporte_id" required readonly />
  
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
  
        <button type="submit">Actualizar</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        reporte_id: null,
        titulo: '',
        descripcion: '',
        fecha: '',
        estatus: true, // Valor por defecto
      };
    },
    created() {
      const reporte_id = this.$route.query.reporte_id;
      if (reporte_id) {
        this.reporte_id = reporte_id;
        this.fetchItem(reporte_id);
      } else {
        console.error('No se proporcionó reporte_id en la consulta.');
      }
    },
    methods: {
      async fetchItem(reporte_id) {
        try {
          const response = await axios.get(`https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/read_one_incidence/${reporte_id}`);
          if (response.data) {
            const item = response.data;
            this.titulo = item.titulo || '';
            this.descripcion = item.descripcion || '';
            this.fecha = item.fecha || '';
            // Asegúrate de que el valor de estatus sea booleano
            this.estatus = item.estatus === true;
          } else {
            console.error('Respuesta vacía o inesperada de la API:', response);
          }
        } catch (error) {
          console.error('Error fetching item:', error.response ? error.response.data : error.message);
        }
      },
      async updateItem() {
        if (!this.reporte_id) {
          console.error('El ID del elemento no está definido.');
          alert('El ID del elemento no está definido.');
          return;
        }
  
        const updatedItem = {
          titulo: this.titulo,
          fecha: this.fecha,
          descripcion: this.descripcion,
          estatus: this.estatus,
        };
  
        console.log('Datos a enviar:', updatedItem); // Verifica que los datos sean correctos
  
        try {
          const response = await axios.put(
            `https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/update_incidence/${this.reporte_id}`,
            updatedItem,
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );
  
          if (response.status === 200) {
            alert('Elemento actualizado correctamente.');
            this.$router.push('/get-all'); // Redirige a la vista de todos los elementos
          } else {
            throw new Error('Error al actualizar el elemento. Estado: ' + response.status);
          }
        } catch (error) {
          console.error('Error al actualizar el elemento:', error.response ? error.response.data : error.message);
          alert('Error al actualizar el elemento.');
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
  