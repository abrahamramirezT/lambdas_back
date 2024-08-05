<template>
  <div id="app">
    <AppNavbar v-if="showNavbar" /> <!-- Muestra el Navbar solo si showNavbar es true -->
    <router-view />
  </div>
</template>

<script>
import AppNavbar from './components/AppNavbar.vue';

export default {
  name: 'App',
  components: {
    AppNavbar,
  },
  computed: {
    showNavbar() {
      // No mostrar el Navbar en la ruta de login
      return this.$route.path !== '/login';
    },
  },
};
</script>

<style>
body {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  margin-top: 40px;
}
</style>
