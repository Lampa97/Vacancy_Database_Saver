from abc import ABC, abstractmethod

import requests

from src.logger import logger_setup

api_logger = logger_setup()


class BaseCompaniesParser(ABC):
    """Abstract class for companies parsers"""

    @abstractmethod
    def prepare_to_fetch(self):
        pass

    @abstractmethod
    def get_companies_info(self):
        pass


class HeadHunterCompanies(BaseCompaniesParser):
    """Class-connector to hh.ru API for getting companies id by their names"""

    companies_list: list

    def __init__(self, companies_list):
        self.__companies_list = companies_list
        self.__url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__companies_name_id = []
        self.__id_list = []
        self.__total_vacancies = 0

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    @property
    def companies_list(self):
        return self.__companies_list

    @property
    def companies_name_id(self):
        return self.__companies_name_id

    @property
    def total_vacancies(self):
        return self.__total_vacancies

    @property
    def id_list(self):
        return self.__id_list

    def prepare_to_fetch(self) -> None:
        """Creating a dictionary with company name and id set to None"""
        for company in self.__companies_list:
            company_name_id = {"name": company, "id": None}
            self.__companies_name_id.append(company_name_id)

    def get_companies_info(self) -> None:
        """Getting company id number from HH API (only companies with active vacancies)"""
        for company in self.__companies_name_id:
            api_logger.info(f"Searching company: {company['name']}")
            response = requests.get(
                url=self.__url,
                headers=self.__headers,
                params={
                    "text": company["name"],
                    "page": 0,
                    "per_page": 100,
                    "only_with_vacancies": True,
                },
            )
            company_info = response.json()
            try:
                company["id"] = company_info["items"][0]["id"]
                api_logger.info(f"Found id: {company['id']} for {company['name']}")
            except IndexError:
                api_logger.info(f"Did not found id for {company['name']}")
            else:
                self.__total_vacancies += company_info['items'][0]['open_vacancies']


    def get_companies_id(self):
        """Creating list of companies id for further vacancies search"""
        self.__id_list = [company['id'] for company in self.__companies_name_id]

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

# pars = HeadHunterCompanies(my_list)
#
# pars.prepare_to_fetch()
#
#
# pars.get_companies_info()
#
# print(pars.companies_name_id)
#
# print(pars.total_vacancies)
#
# response = requests.get(
#     "https://api.hh.ru/employers",
#     headers={"User-Agent": "HH-User-Agent"},
#     params={"text": "Mindbox", "page": 0, "per_page": 100, "only_with_vacancies": True},
# )

# response1 = requests.get(
#     "https://api.hh.ru/vacancies",
#     headers={"User-Agent": "HH-User-Agent"},
#     params={
#         "text": "",
#         "page": 0,
#         "per_page": 100,
#         "employer_id": [
#             "1417893",
#             "370421",
#             "3096092",
#             "10610846",
#             "3585385",
#             "5998412",
#             "4604636",
#             "205152",
#             "743207",
#             "941273",
#         ],
#         "only_with_salary": True,
#     },
# )


# print(response.json())

# print(response1.json())
