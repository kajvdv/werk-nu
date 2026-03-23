<script setup lang="ts">
import { ref } from 'vue';
import RegisterUserForm from '@/components/auth/RegisterUserForm.vue';

const isSuccessful = ref(false) 

function successHandler() {
    isSuccessful.value = true
}

</script>

<template>
    register user
    <RegisterUserForm v-if="!isSuccessful" @successful="successHandler"/>
    <div v-else id="successful-register">User registered successfully</div>
</template>