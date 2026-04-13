<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import Button from '../ui/Button.vue';
import { useVacancyStore } from '@/stores/vacancy';

const emit = defineEmits(["successful"])

const vacancyStore = useVacancyStore()
const authStore = useAuthStore()

async function submitHandler(event: SubmitEvent) {
    const form = new FormData(event.target as HTMLFormElement)
    const {title, location, availability} = Object.fromEntries(form)
    const vacancy = await vacancyStore.postVacancy({
        title: String(title),
        organization: authStore.user.name,
        location: String(location),
        availability: String(availability),
    })
    emit("successful", vacancy)
}
</script>

<template>
    <form @submit.prevent="submitHandler">
        <div class="
            grid grid-cols-2
            gap-4
        ">
            <div class=" mb-2">
                <label class="
                    block
                    text-base font-medium text-ink
                    mb-1.5
                ">Functietitel</label>
                <input class="
                    w-full
                    px-3.5 py-2.5
                    border border-border rounded-md
                    font-dm text-sm text-ink
                    bg-white outline-none
                    transition-colors duration-200
                " required name="title" type="text" placeholder="bijv. Python Developer">
            </div>
            <div class=" mb-2">
                <label class="
                    block
                    text-base font-medium text-ink
                    mb-1.5
                ">Locatie</label>
                <input class="
                    w-full
                    px-3.5 py-2.5
                    border border-border rounded-md
                    font-dm text-sm text-ink
                    bg-white outline-none
                    transition-colors duration-200
                " required name="location" type="text" placeholder="bijv. Amsterdam">
            </div>
        </div>
        <div class="
            grid grid-cols-2
            gap-4
        ">
            <div class=" mb-2">
                <label class="
                    block
                    text-base font-medium text-ink
                    mb-1.5
                ">Dienstverband</label>
                <input class="
                    w-full
                    px-3.5 py-2.5
                    border border-border rounded-md
                    font-dm text-sm text-ink
                    bg-white outline-none
                    transition-colors duration-200
                " required name="availability" type="text" placeholder="Fulltime / Parttime">
            </div>
            <div class=" mb-2">
                <label class="
                    block
                    text-base font-medium text-ink
                    mb-1.5
                ">Salaris (optioneel)</label>
                <input class="
                    w-full
                    px-3.5 py-2.5
                    border border-border rounded-md
                    font-dm text-sm text-ink
                    bg-white outline-none
                    transition-colors duration-200
                " placeholder="bijv. €3.500 – €5.000">
            </div>
        </div>
        <div class="mb-4">
            <label class="
                block
                text-base font-medium text-ink
                mb-1.5
            ">Omschrijving</label>
            <textarea class="
                w-full
                px-3.5 py-2.5
                border border-border rounded-md
                font-dm text-sm text-ink
                bg-white outline-none
                transition-colors duration-200
                h-32
            " type="text" placeholder="bijv. €3.500 – €5.000"></textarea>
        </div>
        <div style="display:flex;gap:10px;justify-content:flex-end">
            <Button type="primary">Vacature publiceren</Button>
        </div>
    </form>
</template>