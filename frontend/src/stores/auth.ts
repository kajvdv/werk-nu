import { defineStore } from 'pinia'
import authApi from "@/api/auth"
import { ref, computed } from 'vue'
import type { UserCreate } from '@/types/auth'

function getToken(){
    const token = sessionStorage.getItem("accessToken")
    if (!token) return ""
    else return token
}

export const useAuthStore = defineStore("auth", () => {
    const user = computed(() => {
        const token = getToken()
        if (!token) {
            return {}
        } else {
            return JSON.parse(atob(token.split(".")[1]))
        }
    })
    const isAuthenticated = computed(() => {
        return !!getToken()
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