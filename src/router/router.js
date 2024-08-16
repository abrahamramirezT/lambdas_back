import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/components/Login.vue';
import ActivateUser from '@/layout/ActivateUser.vue';
import HomeAdmin from '@/pages/Admin/HomeAdmin.vue';
import HomePf from '@/pages/Pf/HomePf.vue';
import HomeUser from '@/pages/User/HomeUser.vue';
import AdminHechas from '@/pages/Admin/AdminHechas.vue';
import AdminAutorizadas from '@/pages/Admin/AdminAutorizadas.vue';
import PfHechas from '@/pages/Pf/PfHechas.vue'
import CreateIncidencia from '@/pages/User/CreateIncidencia.vue';
import PfUpdate from '@/pages/Pf/PfUpdate.vue'
import AdminUpdate from '../pages/Admin/AdminUpdate.vue';
const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/home-admin',
    name: 'HomeAdmin',
    component: HomeAdmin,
    meta: {
      requiresAuth: true,
      role: 'admin',
    },
  },
  {
    path: '/home-pf',
    name: 'HomePf',
    component: HomePf,
    meta: {
      requiresAuth: true,
      role: 'pf',
    },
  },
  {
    path: '/home-user',
    name: 'HomeUser',
    component: HomeUser,
    meta: {
      requiresAuth: true,
      role: 'user',
    },
  },
  {
    path: '/activate-user',
    name: 'ActivateUser',
    component: ActivateUser,
  },

 
  {
    path: '/admin-hechas',
    name: 'AdminHechas',
    component: AdminHechas,
    meta: {
      requiresAuth: true,
      role: 'admin',
    },
  },
  {
    path: '/admin-update/:reporte_id',
    name: 'AdminUpdate',
    component: AdminUpdate,
    meta: {
      requiresAuth: true,
      role: 'admin',
    },
  },
  {
    path: '/admin-autorizadas',
    name: 'AdminAutorizadas',
    component: AdminAutorizadas,
    meta: {
      requiresAuth: true,
      role: 'admin',
    },
  },
 
  {
    path: '/pf-hechas',
    name: 'PfHechas',
    component: PfHechas,
    meta: {
      requiresAuth: true,
      role: 'pf',
    },
  },
  {
    path: '/pf-update/:reporte_id',
    name: 'PfUpdate',
    component: PfUpdate,
    meta: {
      requiresAuth: true,
      role: 'pf',
    },
  },
 
  {
    path: '/create-incidencia',
    name: 'CreateIncidencia',
    component: CreateIncidencia,
    meta: {
      requiresAuth: true,
      role: 'user',
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Middleware para validar la autenticación y el rol
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('id_token');
  const userRole = localStorage.getItem('role');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      // Si no está autenticado, redirigir al login
      next('/login');
    } else if (to.meta.role && to.meta.role !== userRole) {
      // Si el usuario no tiene el rol adecuado, redirigir a una página de acceso denegado o a la ruta de su rol
      alert('No tienes permiso para acceder a esta página.');
      if (userRole === 'admin') {
        next('/home-admin');
      } else if (userRole === 'pf') {
        next('/home-pf');
      } else if (userRole === 'user') {
        next('/home-user');
      } else {
        next('/login');
      }
    } else {
      // Si está autenticado y tiene el rol adecuado, permitir acceso
      next();
    }
  } else {
    // Si la ruta no requiere autenticación, permitir acceso
    next();
  }
});

// Manejo global de errores
router.onError((error) => {
  console.error('Router error:', error);
  // Limpiar localStorage
  localStorage.removeItem('id_token');
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('role');
  // Redirigir al login
  router.push('/login');
});

export default router;
