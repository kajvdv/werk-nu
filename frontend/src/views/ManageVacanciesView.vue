<script setup lang="ts">
import Heading from '@/components/ui/typography/Heading.vue';
import VacancyCard from '@/components/vacancy/VacancyCard.vue';
import Button from '@/components/ui/Button.vue';
import { useVacancyStore } from '@/stores/vacancy';
import { computed } from 'vue';

const vacancyStore = useVacancyStore()
vacancyStore.getOwnVacancies()

const vacancyCount = computed(() => vacancyStore.ownVacancies.length)

function vacancyAge(postedAt: string) {
  const seconds = Math.floor((Date.now() - new Date(postedAt)) / 1000)

  if (seconds < 60) return 'zojuist geplaatst'
  if (seconds < 3600) return `${Math.floor(seconds / 60)} minuten geleden`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} uur geleden`
  if (seconds < 2592000) return `${Math.floor(seconds / 86400)} dagen geleden`
  if (seconds < 31536000) return `${Math.floor(seconds / 2592000)} maanden geleden`
  return `${Math.floor(seconds / 31536000)} jaar geleden`
}
</script>

<template>
  <div class="p-8 max-w-3xl mx-auto">
    <Heading>Mijn vacatures</Heading>
    <div class="font-title text-base text-muted mb-6">{{ vacancyCount }} vacatures</div>
    <div class="flex flex-col gap-2">
      <VacancyCard
        v-for="vacancy in vacancyStore.ownVacancies"
        :title-badge="vacancy.applyCount + ' sollicitaties'"
        :vacancy="vacancy"
      >
        <template #meta>
          <span>{{ vacancyAge(vacancy.created_at) }}</span>
          <span>{{ vacancy.location }}</span>
          <span>{{ vacancy.availability }}</span>
        </template>
        <!-- <Button :small="true" type="outline">Sollicitaties</Button>
        <Button :small="true" type="outline">Sluiten</Button> -->
        <template #default>
          <Button @click="() => vacancyStore.deleteVacancy(vacancy.id)" :small="true" type="red">Verwijder</Button>
        </template>
      </VacancyCard>
    </div>
  </div>
</template>