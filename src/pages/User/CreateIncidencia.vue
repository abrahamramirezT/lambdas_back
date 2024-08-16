<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Navbar -->
    <AppNavbar :role="'user'" class="w-64 bg-white shadow-lg" />

    <!-- Contenido Principal -->
    <div class="flex-grow p-6 overflow-y-auto">
      <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-2xl font-semibold mb-6">Crear Nueva Incidencia</h1>

        <!-- Usamos el componente Form de vee-validate -->
        <Form @submit="submitForm">
          <div class="mb-4">
            <label for="titulo" class="block text-sm font-medium text-gray-700">Título:</label>
            <Field
              id="titulo"
              name="titulo"
              type="text"
              v-model="form.titulo"
              rules="required|min:3"
              class="mt-1 p-2 w-full border rounded-md"
            />
            <ErrorMessage name="titulo" class="text-red-500 text-sm" />
          </div>

          <div class="mb-4">
            <label for="descripcion" class="block text-sm font-medium text-gray-700">Descripción:</label>
            <Field
              as="textarea"
              id="descripcion"
              name="descripcion"
              v-model="form.descripcion"
              rules="required|min:10"
              class="mt-1 p-2 w-full border rounded-md"
            />
            <ErrorMessage name="descripcion" class="text-red-500 text-sm" />
          </div>

          <div class="mb-4">
            <label for="estudiante" class="block text-sm font-medium text-gray-700">Estudiante:</label>
            <Field
              id="estudiante"
              name="estudiante"
              type="text"
              v-model="form.estudiante"
              rules="required|alpha"
              class="mt-1 p-2 w-full border rounded-md"
            />
            <ErrorMessage name="estudiante" class="text-red-500 text-sm" />
          </div>

          <!-- Selector de Aula -->
          <div class="mb-4">
            <label for="aula" class="block text-sm font-medium text-gray-700">Aula:</label>
            <Field
              as="select"
              id="aula"
              name="aula"
              v-model="form.aula"
              rules="required"
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option value="" disabled>Seleccione un aula</option>
              <option v-for="aula in aulas" :key="aula.id" :value="aula.aula_id">
                {{ aula.nombre }}
              </option>
            </Field>
            <ErrorMessage name="aula" class="text-red-500 text-sm" />
          </div>

          <!-- Selector de Edificio -->
          <div class="mb-4">
            <label for="edificio" class="block text-sm font-medium text-gray-700">Edificio:</label>
            <Field
              as="select"
              id="edificio"
              name="edificio"
              v-model="form.edificio"
              rules="required"
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option value="" disabled>Seleccione un edificio</option>
              <option v-for="edificio in edificios" :key="edificio.id" :value="edificio.edificio_id">
                {{ edificio.nombre }}
              </option>
            </Field>
            <ErrorMessage name="edificio" class="text-red-500 text-sm" />
          </div>

          <!-- Selector de División Académica -->
          <div class="mb-4">
            <label for="div_academica" class="block text-sm font-medium text-gray-700">División Académica:</label>
            <Field
              as="select"
              id="div_academica"
              name="div_academica"
              v-model="form.div_academica"
              rules="required"
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option value="" disabled>Seleccione una división</option>
              <option v-for="div_academica in div_academicas" :key="div_academica.id" :value="div_academica.div_aca_id">
                {{ div_academica.nombre }}
              </option>
            </Field>
            <ErrorMessage name="div_academica" class="text-red-500 text-sm" />
          </div>

          <!-- Selector de Grado -->
          <div class="mb-4">
            <label for="grado" class="block text-sm font-medium text-gray-700">Grado:</label>
            <Field
              as="select"
              id="grado"
              name="grado"
              v-model="form.grado"
              rules="required"
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option value="" disabled>Seleccione un grado</option>
              <option v-for="grado in grados" :key="grado.id" :value="grado.grado_id">
                {{ grado.nombre }}
              </option>
            </Field>
            <ErrorMessage name="grado" class="text-red-500 text-sm" />
          </div>

          <!-- Selector de Grupo -->
          <div class="mb-4">
            <label for="grupo" class="block text-sm font-medium text-gray-700">Grupo:</label>
            <Field
              as="select"
              id="grupo"
              name="grupo"
              v-model="form.grupo"
              rules="required"
              class="mt-1 p-2 w-full border rounded-md"
            >
              <option value="" disabled>Seleccione un grupo</option>
              <option v-for="grupo in grupos" :key="grupo.id" :value="grupo.grupo_id">
                {{ grupo.nombre }}
              </option>
            </Field>
            <ErrorMessage name="grupo" class="text-red-500 text-sm" />
          </div>

          <div class="mb-4">
            <label for="matricula" class="block text-sm font-medium text-gray-700">Matricula:</label>
            <Field
              id="matricula"
              name="matricula"
              type="text"
              v-model="form.matricula"
              rules="required|alpha_num"
              class="mt-1 p-2 w-full border rounded-md"
            />
            <ErrorMessage name="matricula" class="text-red-500 text-sm" />
          </div>

          <div class="mb-4">
            <label for="fecha" class="block text-sm font-medium text-gray-700">Fecha:</label>
            <Field
              id="fecha"
              name="fecha"
              type="date"
              v-model="form.fecha"
              rules="required"
              class="mt-1 p-2 w-full border rounded-md"
            />
            <ErrorMessage name="fecha" class="text-red-500 text-sm" />
          </div>

          

          <!-- Campo para Subir Imagen (Solo JPG) -->
          <div class="mb-4">
            <label for="foto" class="block text-sm font-medium text-gray-700">Subir Foto:</label>
            <Field
              id="foto"
              name="foto"
              type="file"
              @change="onFileChange"
              accept="image/jpeg"
              class="mt-1 p-2 w-full border rounded-md"
            />
            <ErrorMessage name="foto" class="text-red-500 text-sm" />
          </div>

          <button
            type="submit"
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Enviar Incidencia
          </button>
        </Form>
      </div>
    </div>
  </div>
</template>

<script>
import { Form, Field, ErrorMessage, defineRule } from 'vee-validate';
import { required, min, alpha, alpha_num } from '@vee-validate/rules';
import AppNavbar from '@/components/AppNavbar.vue';
import axios from 'axios';

// Definir reglas de validación
defineRule('required', required);
defineRule('min', min);
defineRule('alpha', alpha);
defineRule('alpha_num', alpha_num);

// Regla personalizada para validar archivos JPG
defineRule('jpg', (value) => {
  if (!value || !value[0]) return 'Debe seleccionar una imagen jpg.';
  
  const file = value[0];
  const validTypes = ['image/jpeg', 'image/jpg'];

  if (!validTypes.includes(file.type)) {
    return 'El archivo debe ser un JPG.';
  }

  return true;
});

export default {
  components: {
    AppNavbar,
    Form,
    Field,
    ErrorMessage,
  },
  data() {
    return {
      form: {
        titulo: '',
        descripcion: '',
        fecha: '',
        estudiante: '',
        aula: '',
        edificio: '',
        matricula: '',
        div_academica: '',
        grado: '',
        grupo: '',
        estatus: '1',
        fto_base64: '',
      },
      aulas: [],
      edificios: [],
      grados: [],
      grupos: [],
      div_academicas: [],
    };
  },
  mounted() {
    this.fetchAulas();
    this.fetchEdificios();
    this.fetchDivisionesAcademicas();
    this.fetchGrado();
    this.fetchGrupo();
  },
  methods: {
    async fetchAulas() {
      try {
        const response = await axios.get('https://c8eynvsepi.execute-api.us-east-1.amazonaws.com/Stage/read_all_aula');
        this.aulas = response.data;
      } catch (error) {
        console.error('Error al obtener las aulas:', error);
      }
    },
    async fetchEdificios() {
      try {
        const response = await axios.get('https://bqscm2peg3.execute-api.us-east-1.amazonaws.com/Stage/read_all_edificio');
        this.edificios = response.data;
      } catch (error) {
        console.error('Error al obtener los edificios:', error);
      }
    },
    async fetchDivisionesAcademicas() {
      try {
        const response = await axios.get('https://a9mo06q838.execute-api.us-east-1.amazonaws.com/Stage/read_all_div_academica');
        this.div_academicas = response.data;
      } catch (error) {
        console.error('Error al obtener las divisiones académicas:', error);
      }
    },
    async fetchGrado() {
      try {
        const response = await axios.get('https://lp51xyfzbk.execute-api.us-east-1.amazonaws.com/Stage/read_all_grado');
        this.grados = response.data;
      } catch (error) {
        console.error('Error al obtener los grados:', error);
      }
    },
    async fetchGrupo() {
      try {
        const response = await axios.get('https://xfy9zgjuxf.execute-api.us-east-1.amazonaws.com/Stage/read_all_grupo');
        this.grupos = response.data;
      } catch (error) {
        console.error('Error al obtener los grupos:', error);
      }
    },
    async submitForm() {
      try {
        const response = await axios.post('https://4ns4y61589.execute-api.us-east-1.amazonaws.com/Stage/create_incidence', this.form);
        alert('Incidencia creada exitosamente.');
        this.$router.push('/home-user');
      } catch (error) {
        console.error('Error al crear la incidencia:', error);
        alert('Hubo un problema al crear la incidencia.');
      }
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.form.fto_base64 = e.target.result.split(',')[1];
        };
        reader.readAsDataURL(file);
      }
    },
  },
};
</script>

<style scoped>
.bg-gray-100 {
  background-color: #f7f7f7;
}
</style>
