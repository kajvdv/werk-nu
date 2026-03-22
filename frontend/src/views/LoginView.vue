<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore()

function submitHandler(event: SubmitEvent) {
    const form = new FormData(event.target as HTMLFormElement)
    const {username, password} = Object.fromEntries(form)
    authStore.login(String(username), String(password))
}
</script>

<template>
    <form @submit.prevent="submitHandler">
        <label for="username">Email</label>
        <input type="email" name="username">
        <label for="password">Password</label>
        <input type="password" name="password">
        <input type="submit" value="Login">
    </form>
</template>