<script setup lang="ts">
import { ref } from 'vue';
import RegisterOrgForm from '@/components/auth/RegisterOrgForm.vue';

const isSuccessful = ref(false) 

function successHandler() {
    isSuccessful.value = true
}

</script>

<template>
    register organization
    <RegisterOrgForm v-if="!isSuccessful" @successful="successHandler"/>
    <div v-else id="successful-register">Organization registered successfully</div>
</template>