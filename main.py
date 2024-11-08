from time import sleep

from src.companies_fetcher import HeadHunterCompanies
from src.db_manager import DBManager
from src.vacancies_fetcher import HeadHunterVacancies

MY_COMPANIES_LIST = [
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


def initial_setup() -> list:
    """Setting up the companies for search"""
    print("Welcome to Vacancy Database Saver App! Let's get started and setup your tool.\n")

    user_company_list = input(
        f"""Please type names of companies (separated by coma) you would like to search for their open vacancies
    or just press ENTER to use default list of companies. (By default: {MY_COMPANIES_LIST}\n"""
    )
    if user_company_list:
        companies_list = user_company_list.split(",")
    else:
        companies_list = MY_COMPANIES_LIST
    return companies_list


def parsing_companies(companies_list: list) -> list:
    """Parsing companies from given list"""
    companies_parser = HeadHunterCompanies(companies_list)

    companies_parser.prepare_to_fetch()

    companies_parser.get_companies_info()

    companies_parser.get_companies_id()

    return companies_parser.id_list


def parsing_vacancies(companies_id_list: list) -> list:
    """Parsing vacancies with companies id list"""
    vacancies_parser = HeadHunterVacancies()

    vacancies_parser.fetch_vacancies(companies_id_list)

    filtered_data = vacancies_parser.filter_data()

    return filtered_data


def setting_up_database(user_name: str, password: str) -> DBManager:
    """Preparing database for further work"""
    db_manager = DBManager(user_name, password)

    db_manager.create_database()

    return db_manager


def set_database_option(option_number: str, database: DBManager) -> bool:
    """Choosing one of working method from DBManager class"""
    app_status = True
    if option_number == "1":
        database.get_all_vacancies()
    elif option_number == "2":
        database.get_companies_and_vacancies_count()
    elif option_number == "3":
        database.get_avg_salary()
    elif option_number == "4":
        database.get_vacancies_with_higher_salary()
    elif option_number == "5":
        user_keyword = input("Please type your keyword: \n")
        database.get_vacancies_with_keyword(user_keyword)
    elif option_number == "0":
        app_status = False
    else:
        print("Cannot recognize your choice. Please try again.\n")
    if app_status is True:
        print("\nYou may continue work or exit the application\n")
    return app_status


def main() -> None:
    companies_list = initial_setup()

    print("Cool! Now it's time to establish connection with your PostGres database\n")

    user_name = input("Please enter your PostGres username: ")
    password = input("Please enter your password: ")
    db_manager = setting_up_database(user_name, password)
    sleep(1)

    print("All right! Initiating search on HeadHunter...\n")
    sleep(2)

    companies_id = parsing_companies(companies_list)
    sleep(2)
    vacancies = parsing_vacancies(companies_id)
    sleep(2)

    db_manager.fill_up_tables(companies_list, vacancies)
    print("Search is completed and your database is ready! Now you may choose option number to work with vacancies.\n")
    sleep(2)
    running_app = True
    while running_app:
        user_choice = input(
            """
        1. See all available vacancies and their respective employers.
        2. See how much vacancies each employer has.
        3. See average salary among all available vacancies.
        4. See vacancies with salary bigger than average.
        5. See vacancies filtered by a keyword.
        0. Exit the application.\n"""
        )

        running_app = set_database_option(user_choice, db_manager)
        sleep(3)

    print("Finish working. Thank You!")
    input("\n\n\nPress Enter to exit.")


if __name__ == "__main__":
    main()
