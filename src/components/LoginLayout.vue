<template>
    <div class="login-layout">
      <router-view></router-view> <!-- Aquí se renderiza el componente de login -->
    </div>
  </template>
  
  <style scoped>
  .login-layout {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
  }
  </style>
  