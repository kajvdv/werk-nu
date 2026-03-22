import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: MainView},
    {path: "/login", component: LoginView},
  ],
})

export default router
