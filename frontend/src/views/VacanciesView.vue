<script setup lang="ts">
import { ref } from 'vue';

const vacancies = ref([])

</script>

<template>
    <div v-for="vacancy in vacancies" :id="vacancy.id"></div>
</template>