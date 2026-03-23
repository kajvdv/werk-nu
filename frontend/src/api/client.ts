import axios from "axios";

const client = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL + "/api",
})

client.interceptors.request.use(function(config) {
  const accessToken = sessionStorage.getItem("accessToken")
  if (accessToken) {
    config.headers["Authorization"] = `Bearer ${accessToken}`
  }
  return config
})

export default client