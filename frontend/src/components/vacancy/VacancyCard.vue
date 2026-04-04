<script setup lang="ts">

import Badge from '../ui/Badge.vue';
import type { VacancyPublic } from '@/types/vacancy';
import Button from '../ui/Button.vue';
import { computed } from 'vue';

const {vacancy} = defineProps<{
    vacancy: VacancyPublic
}>()

const opacityClass = computed(() => vacancy.closed ? 'opacity-50' : 'opacity-100')
</script>

<template>
    <div :class="`
      bg-white
      border rounded-2xl border-border
      px-6 py-5
      flex items-center justify-between
      transition-shadow duration-200
      hover:shadow-card
      ${opacityClass}
    `">
        <div>
            <h3>{{ vacancy.title }} <Badge v-if="vacancy.newVacancy" color="yellow">Nieuw</Badge></h3>
            <div class="
                text-xs text-muted
                flex gap-4
            ">
                <span>{{ vacancy.organization }}</span>
                <span>{{ vacancy.location }}</span>
                <span>{{ vacancy.availability }}</span>
            </div>
        </div>
        <div class="flex gap-3 items-center">
          <Badge v-if="!vacancy.closed" color="green">Open</Badge>
          <Badge v-else color="red">Gesloten</Badge>
          <Button type="primary">Solliciteer</Button>
        </div>
    </div>
</template>

<style scoped>
h3 {
    margin-bottom: 4px;
}
</style>