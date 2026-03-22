import client from "@/api/client"


export default {
    login(username: string, password: string) {
        const form = new FormData()
        form.append("username", username)
        form.append("password", password)
        client.post("/token", form)
    }
}