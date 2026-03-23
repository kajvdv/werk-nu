import { defineStore } from 'pinia'
import authApi from "@/api/auth"
import { ref, computed } from 'vue'
import type { UserCreate } from '@/types/auth'

export const useAuthStore = defineStore("auth", () => {
    const user = ref()
    const token = ref(sessionStorage.getItem("access_token"))
    const isAuthenticated = computed(() => {
        if (!user.value || !token.value) return false
    })
    async function login(username: string, password: string) {
        await authApi.login(username, password)
    }

    async function registerOrganization(name: string, email: string, password: string) {
        await authApi.registerOrganization(
            name, email, password
        )
    }

    async function registerUser(data: UserCreate) {
        await authApi.registerUser(data)
    }
    
    return {user, isAuthenticated, login, registerOrganization, registerUser}
})