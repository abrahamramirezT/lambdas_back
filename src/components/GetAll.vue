<template>
  <div class="wrapper">
    <div>
    <h2>Ver Todos</h2>
    <table v-if="items.length">
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
        <tr v-for="item in items" :key="item.reporte_id">
          <td>{{ item.reporte_id }}</td>
          <td>{{ item.titulo }}</td>
          <td>{{ item.fecha }}</td>
          <td>{{ item.descripcion }}</td>
          <td>{{ item.estatus ? 'Activo' : 'Inactivo' }}</td>
          <td>
            <img :src="item.fto_url" alt="Foto" style="width: 100px; height: auto;" />
          </td>
          <td class="actions">
            <button @click="editItem(item.reporte_id)" class="update">Actualizar</button>
            <button @click="deleteItem(item.reporte_id)" class="delete">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Cargando datos...</p>
    </div>
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
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get('https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/read_all_incidence');
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
        try {
          await axios.delete(`https://omp7h5yonf.execute-api.us-east-1.amazonaws.com/Prod/delete_incidence/${id}`);
          alert('Elemento eliminado correctamente.');
          this.fetchItems(); // Actualiza la lista después de eliminar
        } catch (error) {
          console.error('Error al eliminar el elemento:', error);
          alert('Error al eliminar el elemento.');
        }
      }
    },
  },
};
</script>

<style scoped>

.wrapper{
  padding-left:5%;
  padding-right:5%
}
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
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}


.actions {
  display: flex;
  justify-content: center;
}

.update {
  background-color: blue; /* Color de fondo para el botón de actualización */
}

.update:hover {
  background-color: darkblue; /* Color de fondo en hover para el botón de actualización */
  transform: scale(1.05); /* Escala ligeramente el botón al pasar el cursor sobre él */
}

.delete {
  background-color: red; /* Color de fondo para el botón de eliminación */
}

.delete:hover {
  background-color: darkred; /* Color de fondo en hover para el botón de eliminación */
  transform: scale(1.05); /* Escala ligeramente el botón al pasar el cursor sobre él */
}
</style>
