<script setup lang="ts">
import Heading from '@/components/ui/typography/Heading.vue';
import PostVacancyForm from '@/components/vacancy/PostVacancyForm.vue';
import type { VacancyPublic } from '@/types/vacancy';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

function successHandler(data: VacancyPublic) {
    router.push("/vacancies")
}

</script>

<template>
    <div class="p-8 max-w-3xl mx-auto">
        <Heading>Nieuwe vacature plaatsen</Heading>
        <div class="font-title text-base text-muted mb-6">Vul de details in. Sollicitanten kunnen direct reageren.</div>
        <PostVacancyForm @successful="successHandler"/>
    </div>
</template>