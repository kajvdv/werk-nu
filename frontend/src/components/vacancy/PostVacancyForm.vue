<script setup lang="ts">
import { useVacancyStore } from '@/stores/vacancy';

const emit = defineEmits(["successful"])

const vacancyStore = useVacancyStore()

async function submitHandler(event: SubmitEvent) {
    const form = new FormData(event.target as HTMLFormElement)
    const {title} = Object.fromEntries(form)
    const vacancy = await vacancyStore.postVacancy({
        title: String(title)
    })
    emit("successful", vacancy)
}
</script>

<template>
    Post a new vacancy
    <form @submit.prevent="submitHandler">
        <label for="vacancy-title">Title</label>
        <input id="post-vacancy-title" type="text" name="title">
        <input id="post-vacancy-submit" type="submit" value="Post">
    </form>
</template>