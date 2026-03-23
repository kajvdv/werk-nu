import vacancyApi from "@/api/vacancy";
import type { VacancyCreate } from "@/types/vacancy";
import { defineStore } from "pinia";

export const useVacancyStore = defineStore("vacancy", () => {
    async function postVacancy(data: VacancyCreate) {
        return await vacancyApi.postVacancy(data)
    }
    return { postVacancy }
})