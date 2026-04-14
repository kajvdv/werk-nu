import OrgHomeView from '@/views/OrgHomeView.vue'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import RegisterOrgView from '@/views/RegisterOrgView.vue'
import RegisterUserView from "@/views/RegisterUserView.vue"
import { createRouter, createWebHistory } from 'vue-router'
import PostVacancyView from '@/views/PostVacancyView.vue'
import VacanciesView from '@/views/VacanciesView.vue'
import ManageVacanciesView from '@/views/ManageVacanciesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: "/", component: MainView},
    {path: "/login", component: LoginView},
    {path: "/organizations/register", component: RegisterOrgView},
    {path: "/users/register", component: RegisterUserView},
    {path: "/organizations/me", component: OrgHomeView},
    {path: "/vacancies/post", component: PostVacancyView},
    {path: "/vacancies/me", component: ManageVacanciesView},
    {path: "/vacancies", component: VacanciesView},
  ],
})

export default router
