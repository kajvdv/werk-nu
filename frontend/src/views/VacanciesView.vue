<script setup lang="ts">
import VacancyCard from '@/components/vacancy/VacancyCard.vue';
import { useVacancyStore } from '@/stores/vacancy';
import type { VacancyPublic } from '@/types/vacancy';

const vacancyStore = useVacancyStore()
vacancyStore.getVacancies()

async function apply(vacanyId: string) {
    console.log("Apply! to", vacanyId)
    vacancyStore.apply(vacanyId)
}

</script>

<template>
  <div class="p-8 max-w-3xl mx-auto">
    <div class="font-title text-3xl text-ink mb-2">Openstaande vacatures</div>
    <div class="font-title text-m text-muted mb-6">{{ vacancyStore.vacancies.length }} vacatures beschikbaar</div>
    <div class="flex flex-col gap-2">
      <VacancyCard v-for="vacancy in vacancyStore.vacancies" :new-vacancy="vacancy.newVacancy" :vacancy="vacancy"/>
    </div>
  </div>
</template>