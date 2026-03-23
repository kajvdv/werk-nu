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
    await authStore.registerOrganization(
        String(name),
        String(email),
        String(password),
    )
    emit("successful")
}

</script>

<template>
    <form @submit.prevent="submitHandler">
        <input name="name" type="text" id="org-name">
        <input name="email" type="email" id="org-email" required>
        <input name="password" type="password" id="org-password">
        <input type="submit" value="Register" id="register-org-submit">
    </form>
</template>