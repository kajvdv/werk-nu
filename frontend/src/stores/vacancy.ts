import vacancyApi from "@/api/vacancy";
import type { VacancyCreate, VacancyPublic, VacancyPublicOwn } from "@/types/vacancy";
import { defineStore } from "pinia";
import { ref } from "vue";


export const useVacancyStore = defineStore("vacancy", () => {
    const vacancies = ref<VacancyPublic[]>([])
    const ownVacancies = ref<VacancyPublicOwn[]>([])
    
    async function postVacancy(data: VacancyCreate) {
        return await vacancyApi.postVacancy(data)
    }

    async function getVacancies() {
        const data = await vacancyApi.getVacancies()
        vacancies.value = data
    }

    async function deleteVacancy(id: string) {
        await vacancyApi.deleteVacancy(id)
        await getOwnVacancies()
    }

    async function getOwnVacancies() {
        const data = await vacancyApi.getOwnVacancies()
        ownVacancies.value = data
    }

    async function apply(vacancyID: string) {
        await vacancyApi.apply(vacancyID)
    }

    return {
        postVacancy,
        getVacancies,
        deleteVacancy,
        getOwnVacancies,
        vacancies,
        ownVacancies,
        apply,
    }
})