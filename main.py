from src.companies_fetcher import HeadHunterCompanies

from src.vacancies_fetcher import HeadHunterVacancies


my_list = [
    "HTS",
    "ООО Роболайн",
    "Doubletapp",
    "SL Soft",
    "Itwis",
    "InlyIT",
    "Skillline",
    "Mindbox",
    "SPRINTHOST",
    "Voximplant",
]


pars = HeadHunterCompanies(my_list)

pars.prepare_to_fetch()


pars.get_companies_info()

pars.get_companies_id()

vac = HeadHunterVacancies()

vac.fetch_vacancies(1, pars.id_list)

vacs = vac.filter_data()

print(vacs)

print(pars.total_vacancies)