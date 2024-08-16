<template>
  <div class="container mx-auto p-4">
    <h2 class="text-2xl font-semibold mb-4">{{ title }}</h2>
    <div class="overflow-x-auto">
      <table v-if="items.length" class="min-w-full bg-white shadow-md rounded-lg">
        <thead class="bg-gray-500 text-white">
          <tr>
            <th v-for="header in headers" :key="header" class="py-3 px-4 text-left">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id" class="border-b text-gray-700">
            <td v-for="(value, key) in item" :key="key" class="py-3 px-4">
              <template v-if="key === 'actions'">
                <!-- Si el rol es Admin, muestra Aprobar, Rechazar, Actualizar y Eliminar -->
                <template v-if="role === 'admin'">
                  <button @click="editItemAdmin(item)" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">
                    Actualizar
                  </button>
                  <button @click="deleteItem(item.id)" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">
                    Eliminar
                  </button>
                </template>
                <!-- Si el rol es Physical, solo muestra Actualizar -->
                <template v-else-if="role === 'pf'">
                  <button @click="editItem(item)" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">
                    Actualizar
                  </button>
                </template>
              </template>
              <template v-else-if="key === 'fto_url'">
                <img :src="value" alt="Foto" class="w-24 h-auto rounded-md" />
              </template>
              <template v-else-if="key === 'estatus'">
                <span :class="statusClass(value)">
                  {{ formatEstatus(value) }}
                </span>
              </template>
              <template v-else>
                {{ value }}
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
    role: {  // Añade una prop para el rol del usuario
      type: String,
      required: true,
    },
  },
  methods: {
    editItem(item) {
  // Redirige a la ruta con el ID de la incidencia
  this.$router.push({ name: 'PfUpdate', params: { reporte_id: item.id } });
},
editItemAdmin(item) {
  // Redirige a la ruta con el ID de la incidencia
  this.$router.push({ name: 'AdminUpdate', params: { reporte_id: item.id } });
},

async deleteItem(id) {
      if (confirm("¿Estás seguro de que deseas eliminar esta incidencia?")) {
        try {
          // Realiza la solicitud DELETE a la API
          await axios.delete(`https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/delete_incidence/${id}`);
          alert('Incidencia eliminada exitosamente.');

          // Refresca la lista de incidencias o remueve la incidencia eliminada de la lista
          this.items = this.items.filter(item => item.id !== id);

        } catch (error) {
          console.error('Error al eliminar la incidencia:', error);
          alert('Hubo un problema al eliminar la incidencia.');
        }
      }
    },
    approveItem(id) {
      this.$emit('approve-item', id);
    },
    rejectItem(id) {
      this.$emit('reject-item', id);
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
    statusClass(estatus) {
      switch (estatus) {
        case 1:
          return 'text-yellow-500';
        case 2:
          return 'text-blue-500';
        case 3:
          return 'text-green-500';
        default:
          return 'text-gray-500';
      }
    }
  },
};
</script>

<style scoped>
/* Ya se han utilizado estilos Tailwind CSS en el template, así que no es necesario añadir más estilos aquí. */
</style>