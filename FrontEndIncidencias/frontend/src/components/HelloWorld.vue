<template>
  <div class="app">
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/table">Table</router-link></li>
        <li><router-link to="/post-form">Post Form</router-link></li>
        <li><router-link to="/put-form">Put Form</router-link></li>
      </ul>
    </nav>

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style scoped>
nav {
  background-color: #42b983;
  padding: 10px;
}
ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
}
li {
  margin-right: 20px;
}
a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}
a:hover {
  text-decoration: underline;
}
</style>
