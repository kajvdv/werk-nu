<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';

const emit = defineEmits(["successful"])

const authStore = useAuthStore()

async function submitHandler(event: SubmitEvent) {
    const form = new FormData(event.target as HTMLFormElement)
    const {
        name,
        email,
        password,
    } = Object.fromEntries(form)
    await authStore.registerUser({
        name: String(name),
        email: String(email),
        password: String(password),
    })
    emit("successful")
}

</script>

<template>
    <form @submit.prevent="submitHandler">
        <input name="name" type="text" id="user-name">
        <input name="email" type="email" id="user-email" required>
        <input name="password" type="password" id="user-password">
        <input type="submit" value="Register" id="register-user-submit">
    </form>
</template>