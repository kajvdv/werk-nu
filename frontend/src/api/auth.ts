import client from "@/api/client"
import type { UserCreate } from "@/types/auth"


export default {
    async login(username: string, password: string) {
        const form = new FormData()
        form.append("username", username)
        form.append("password", password)
        const response = await client.post("/token", form)
        const {access_token} = response.data
        client.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        sessionStorage.setItem("accessToken", access_token)
    },

    async registerOrganization(
        name: string, email: string, password: string
    ) {
        await client.post("/organizations", {
            name, email, password
        })
    },

    async registerUser(data: UserCreate) {
        await client.post("/users", data)
    }
}