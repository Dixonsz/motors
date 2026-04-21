import { createRouter, createWebHistory } from 'vue-router'
import { marcaRoutes } from '../../modules/marcas/routes'

const routes = [
  {
    path: '/',
    redirect: '/marcas',
  },
  ...marcaRoutes,
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
