<template>
  <div id="app">
    <AppNavbar class="navbar" v-if="showNavbar" /> <!-- Muestra el Navbar solo si showNavbar es true -->
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
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
<style>

body {

  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  margin-top: 0px;
}


</style>
