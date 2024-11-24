import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/ProductView.vue')
    },
    {
      path: '/my-account',
      name: 'my-account',
      component: () => import('../views/MyAccount.vue')
    }
  ]
})

export default router
