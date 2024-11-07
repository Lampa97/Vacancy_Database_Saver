from abc import ABC, abstractmethod

import requests

from src.logger import general_logger


class BaseVacancyParser(ABC):
    """Abstract class for vacancy parsers"""

    @abstractmethod
    def fetch_vacancies(self, pages_amount, employers_info):
        pass

    @abstractmethod
    def filter_data(self):
        pass


class HeadHunterVacancies(BaseVacancyParser):
    """Class-connector to hh.ru API for getting open vacancies of desired companies"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies = []

    @property
    def url(self):
        return self.__url

    @property
    def headers(self):
        return self.__headers

    @property
    def params(self):
        return self.__params

    def fetch_vacancies(self, pages_amount: int, employers_id: list) -> None:
        """Fetching vacancies from HeadHunter"""
        page_number = 0
        while page_number <= abs(pages_amount):
            general_logger.info(f"Parsing page number: {page_number}")
            response = requests.get(
                self.__url,
                headers=self.__headers,
                params={"page": page_number, "per_page": 100, "employer_id": employers_id},
            )
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.vacancies.extend(vacancies)
                general_logger.info("Vacancies successfully added to list")
            page_number += 1

    def filter_data(self) -> list:
        """Choosing only useful information from api response and returning filtered list with salary in RUB"""
        filtered_data = []
        for vacancy in self.vacancies:
            try:
                if vacancy.get("salary").get("currency") == "RUR":
                    current_vacancy = dict()
                    current_vacancy["name"] = vacancy["name"]
                    current_vacancy["salary"] = vacancy.get("salary")
                    current_vacancy["url"] = vacancy["alternate_url"]
                    current_vacancy["experience"] = vacancy["experience"]["name"]
                    current_vacancy["employer"] = vacancy["employer"]["name"]
                    del current_vacancy["salary"]["gross"]
                    filtered_data.append(current_vacancy)
            except AttributeError:
                continue
        return filtered_data
