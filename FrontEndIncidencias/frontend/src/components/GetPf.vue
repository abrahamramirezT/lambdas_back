<template>
    <div>
      <h2>Ver Todos</h2>
      <table v-if="filteredItems.length">
        <thead>
          <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Fecha</th>
            <th>Descripción</th>
            <th>Status</th>
            <th>Foto</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.reporte_id">
            <td>{{ item.reporte_id }}</td>
            <td>{{ item.titulo }}</td>
            <td>{{ item.fecha }}</td>
            <td>{{ item.descripcion }}</td>
            <td>{{ formatEstatus(item.estatus) }}</td>
            <td><img :src="item.fto_url" alt="Foto" style="width: 100px; height: auto;" /></td>
            <td>
              <button @click="editItem(item.reporte_id)">Actualizar</button>
              <button @click="deleteItem(item.reporte_id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Cargando datos...</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        items: [], // Inicializar como un array vacío
      };
    },
    created() {
      this.fetchItems();
    },
    computed: {
      filteredItems() {
        // Filtra los elementos que tienen estatus 'En Progreso' (valor 2)
        return this.items.filter(item => item.estatus === 2);
      }
    },
    methods: {
      async fetchItems() {
        const token = localStorage.getItem('idToken'); // Asume que el token está almacenado en localStorage
        try {
          const response = await axios.get('https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/read_all_incidence', {
            headers: {
              'Authorization': `Bearer ${token}`, // Incluye el token en la cabecera de autorización
            },
          });
          this.items = response.data; // Asume que la respuesta es un array de elementos
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      editItem(reporte_id) {
        this.$router.push({ path: '/put', query: { reporte_id } });
      },
      async deleteItem(id) {
        if (confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
          const token = localStorage.getItem('idToken'); // Incluye el token en la cabecera de autorización
          try {
            await axios.delete(`https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/delete_incidence/${id}`, {
              headers: {
                'Authorization': `Bearer ${token}`,
              },
            });
            alert('Elemento eliminado correctamente.');
            this.fetchItems(); // Actualiza la lista después de eliminar
          } catch (error) {
            console.error('Error al eliminar el elemento:', error);
            alert('Error al eliminar el elemento.');
          }
        }
      },
      formatEstatus(estatus) {
        switch (estatus) {
          case 1:
            return 'Pendiente';
          case 2:
            return 'En Progreso';
          case 3:
            return 'Completado';
          default:
            return 'Desconocido';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  th, td {
    padding: 10px;
    border: 1px solid #ddd;
  }
  
  th {
    background-color: #f2f2f2;
  }
  
  button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 5px;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 5px;
  }
  
  button:hover {
    background-color: #36986f;
  }
  </style>
  