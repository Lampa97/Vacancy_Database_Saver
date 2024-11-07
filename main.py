from src.companies_fetcher import HeadHunterCompanies

from src.vacancies_fetcher import HeadHunterVacancies

from src.db_manager import DBManager


my_list = [
    "Pooling",
    "Amigoweb",
    "Doubletapp",
    "InlyIT",
    "PUSK",
    "Digital Sail",
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

vac.fetch_vacancies(10, pars.id_list)

vacs = vac.filter_data()


db = DBManager('Chelsea1905')

db.create_database()

db.fill_up_tables(pars.companies_list, vacs)

print(pars.total_vacancies)