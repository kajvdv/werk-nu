
interface VacancyBase{
    title: string
    organization: string
    location: string
    availability: string
}


export interface VacancyCreate extends VacancyBase {
}

export interface VacancyPublic extends VacancyBase {
    organization_id: string
    id: string
    newVacancy: boolean
    closed: boolean
}

export interface VacancyPublicOwn extends VacancyPublic {
    created_at: string
    applyCount: number
}