from src.companies_fetcher import HeadHunterCompanies

from src.vacancies_fetcher import HeadHunterVacancies

from src.db_manager import DBManager


my_companies_list = [
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


pars = HeadHunterCompanies(my_companies_list)

pars.prepare_to_fetch()


pars.get_companies_info()

pars.get_companies_id()

vac = HeadHunterVacancies()

vac.fetch_vacancies(pars.id_list)

vacs = vac.filter_data()


db = DBManager('postgres', 'Chelsea1905')

db.create_database()

db.fill_up_tables(pars.companies_list, vacs)

# db.get_companies_and_vacancies_count()
#
# db.get_all_vacancies()
#
# db.get_avg_salary()
#
# db.get_vacancies_with_higher_salary()

db.get_vacancies_with_keyword('разр')