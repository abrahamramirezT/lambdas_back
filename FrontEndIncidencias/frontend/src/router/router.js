import Vue from 'vue';
import Router from 'vue-router';
import GetAll from '../components/GetAll.vue';
import PostForm from '../components/PostForm.vue';
import PutForm from '../components/PutForm.vue';
import Login from '../components/Login.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      redirect: '/get-all',
    },
    {
      path: '/login',
      component: Login,
      meta: { requiresAuth: false },
    },
    {
      path: '/get-all',
      component: GetAll,
      meta: { requiresAuth: true, roles: ['admin', 'user'] }, // Solo para roles específicos
    },
    {
      path: '/post',
      component: PostForm,
      meta: { requiresAuth: true, roles: ['admin'] }, // Solo para rol admin
    },
    {
      path: '/put',
      component: PutForm,
      meta: { requiresAuth: true, roles: ['user'] }, // Solo para rol admin
    },
    {
      path: '*',
      redirect: '/login',
    },
  ],
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('id_token');
  const userRole = localStorage.getItem('role');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/login'); // Redirige al login si no está autenticado
    } else if (to.meta.roles && !to.meta.roles.includes(userRole)) {
      next('/'); // Redirige a la página principal si no tiene permisos
    } else {
      next(); // Permite el acceso
    }
  } else {
    next(); // Permite el acceso si no se requiere autenticación
  }
});

export default router;
