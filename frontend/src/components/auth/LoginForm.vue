<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore()

async function submitHandler(event: SubmitEvent) {
    const form = new FormData(event.target as HTMLFormElement)
    const {username, password} = Object.fromEntries(form)
    await authStore.login(String(username), String(password))
}
</script>

<template>
    <form @submit.prevent="submitHandler">
        <label for="username">Email</label>
        <input id="login-username" type="email" name="username">
        <label for="password">Password</label>
        <input id="login-password" type="password" name="password">
        <input id="login-submit" type="submit" value="Login">
    </form>
</template>