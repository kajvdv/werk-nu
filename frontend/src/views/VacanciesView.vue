<script setup lang="ts">
import VacancyCard from '@/components/vacancy/VacancyCard.vue';
import { useVacancyStore } from '@/stores/vacancy';
import Heading from '@/components/ui/typography/Heading.vue';

const vacancyStore = useVacancyStore()
vacancyStore.getVacancies()

async function apply(vacanyId: string) {
    vacancyStore.apply(vacanyId)
}

</script>

<template>
  <div class="p-8 max-w-3xl mx-auto">
    <Heading>Openstaande vacatures</Heading>
    <div class="font-title text-base text-muted mb-6">{{ vacancyStore.vacancies.length }} vacatures beschikbaar</div>
    <div class="flex flex-col gap-2">
      <VacancyCard v-for="vacancy in vacancyStore.vacancies" :new-vacancy="vacancy.newVacancy" :vacancy="vacancy"/>
    </div>
  </div>
</template>