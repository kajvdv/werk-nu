<script setup lang="ts">
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter()
const authStore = useAuthStore()

</script>

<template>
    main view
    <RouterLink id="register-organization" to="/organizations/register">Register organization</RouterLink>
    <RouterLink id="register-user" to="/users/register">Register</RouterLink>
</template>