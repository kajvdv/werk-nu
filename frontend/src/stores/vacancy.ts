import vacancyApi from "@/api/vacancy";
import type { VacancyCreate, VacancyPublic } from "@/types/vacancy";
import { defineStore } from "pinia";
import { ref } from "vue";


export const useVacancyStore = defineStore("vacancy", () => {
    const vacancies = ref<VacancyPublic[]>([])
    
    async function postVacancy(data: VacancyCreate) {
        return await vacancyApi.postVacancy(data)
    }

    async function getVacancies() {
        const data = await vacancyApi.getVacancies()
        vacancies.value = data
    }

    async function apply(vacancyID: string) {
        await vacancyApi.apply(vacancyID)
    }

    return { postVacancy, getVacancies, vacancies, apply }
})