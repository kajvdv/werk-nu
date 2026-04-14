import type { VacancyCreate, VacancyPublic, VacancyPublicOwn } from "@/types/vacancy";
import client from "./client";


function isVacancy(data: any): data is VacancyPublic[] {
    for (const vacancy of data) {
        if ((typeof vacancy.title !== "string")             
            || (typeof vacancy.organization !== "string")      
            || (typeof vacancy.location !== "string")          
            || (typeof vacancy.availability !== "string")      
            || (typeof vacancy.organization_id !== "string")   
            || (typeof vacancy.id !== "string")                
            || (typeof vacancy.newVacancy !== "boolean")       
            || (typeof vacancy.closed !== "boolean")) return false
    }
    return true
}

function isOwnVacancy(data: any): data is VacancyPublicOwn[] {
    for (const vacancy of data) {
        if ((typeof vacancy.title !== "string")             
            || (typeof vacancy.organization !== "string")      
            || (typeof vacancy.location !== "string")          
            || (typeof vacancy.availability !== "string")      
            || (typeof vacancy.organization_id !== "string")   
            || (typeof vacancy.id !== "string")                
            || (typeof vacancy.newVacancy !== "boolean")       
            || (typeof vacancy.closed !== "boolean")
            || (typeof vacancy.created_at !== "string")       
            || (typeof vacancy.applyCount !== "number"))
            return false
    }
    return true
}


export default {
    async postVacancy(data: VacancyCreate) {
        const response = await client.post("/vacancies", data)
        return response.data
    },

    async getVacancies() {
        const response = await client.get("/vacancies")
        const data = response.data
        if (isVacancy(data)) {
            return data
        } else {
            return []
        }
    },

    async deleteVacancy(id: string) {
        await client.delete(`/vacancies/${id}`)
    },

    async getOwnVacancies() {
        const response = await client.get("/vacancies/me")
        const data = response.data
        if (isOwnVacancy(data)) {
            return data
        } else {
            return []
        }
    },

    async apply(vacancyID: string) {
        const response = await client.post(`/vacancies/${vacancyID}/applications`)
    }
}