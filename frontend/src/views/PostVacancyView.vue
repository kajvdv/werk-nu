<script setup lang="ts">
import PostVacancyForm from '@/components/vacancy/PostVacancyForm.vue';
import type { VacancyPublic } from '@/types/vacancy';
import { ref } from 'vue';

const state = ref<VacancyPublic | null>(null)

function successHandler(data: VacancyPublic) {
    console.log(data)
    state.value = data
}

</script>

<template>
    <PostVacancyForm v-if="state == null" @successful="successHandler"/>
    <div id="submitted-vacancy" v-else-if="state">
        <div>{{ state.title }}</div>
        <div>{{ state.organization_id }}</div>
        <div>{{ state.id }}</div>
        <button id="confirm-post">Confirm</button>
    </div>
</template>