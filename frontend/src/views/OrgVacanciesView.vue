<script setup lang="ts">
import VacancyDisplay from '@/components/vacancy/VacancyCard.vue';
import { useVacancyStore } from '@/stores/vacancy';

const VacancyStore = useVacancyStore()

VacancyStore.getOwnVacancies()
</script>

<template>
    org vacancies view    
    <div v-for="vacancy in VacancyStore.vacancies">
        <!-- {{ vacancy.title }}
        <button @click="">Show applications</button> -->
        <VacancyDisplay :vacancy="vacancy"/>
    </div>
</template>
