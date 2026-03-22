import { defineStore } from 'pinia'
import authApi from "@/api/auth"

export const useAuthStore = defineStore("auth", () => {
    function login(username: string, password: string) {
        authApi.login(username, password)
    }
    
    return {login}
})