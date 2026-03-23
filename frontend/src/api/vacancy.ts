import type { VacancyCreate } from "@/types/vacancy";
import client from "./client";

export default {
    async postVacancy(data: VacancyCreate) {
        const response = await client.post("/me/vacancies", data)
        return response.data
    }
}