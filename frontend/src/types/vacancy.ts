
interface VacancyBase{
    title: string
}


export interface VacancyCreate extends VacancyBase {
}

export interface VacancyPublic extends VacancyBase {
    organization_id: string
    id: string
}