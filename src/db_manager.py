from abc import ABC, abstractmethod

import psycopg2

from src.logger import general_logger


class BaseDBManager(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass


class DBManager(BaseDBManager):
    """Class for working with PostGreSQL database"""

    password: str
    user_name: str
    database_name: str

    def __init__(self,  user_name, password, database_name="hh_vacancies"):
        self.__params = {"host": "localhost", "user": user_name, "password": password}
        self.__database_name = database_name

    def create_database(self):
        """Method for creating PostGreSQL database"""
        conn = psycopg2.connect(dbname="postgres", **self.__params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {self.__database_name}")
        cur.execute(f"CREATE DATABASE {self.__database_name}")

        conn.close()

        general_logger.info(f"Created database {self.__database_name}")

        conn = psycopg2.connect(dbname=self.__database_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    employer_id SERIAL,
                    name VARCHAR(255) NOT NULL,
                    CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)
                )
            """
            )
        general_logger.info("Created table employers")

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id SERIAL,
                    name VARCHAR(255),
                    from_salary INTEGER,
                    to_salary INTEGER,
                    url TEXT,
                    employer_id INTEGER REFERENCES employers(employer_id)
                )
            """
            )
        general_logger.info("Created table vacancies")
        conn.commit()
        conn.close()

    def fill_up_tables(self, companies, vacancies):
        """Method for filling up tables in PostGreSQL database"""
        conn = psycopg2.connect(dbname=self.__database_name, **self.__params)

        with conn.cursor() as cur:
            for employer in companies:
                cur.execute(
                    f"""
                    INSERT INTO employers (name) VALUES ('{employer}')
                """
                )
            general_logger.info("Successfully inserted data into employers")
            for vacancy in vacancies:
                cur.execute(
                    f"""
                    INSERT INTO vacancies (name, from_salary, to_salary, url, employer_id)
                    VALUES (%s, %s, %s, %s, (SELECT employer_id from employers e
                    WHERE e.name = '{vacancy['employer']}'))
                    """,
                    (vacancy["name"], vacancy["salary"]["from"], vacancy["salary"]["to"], vacancy["url"]),
                )
            general_logger.info("Successfully inserted data into vacancies")
        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """Method for grouping vacancies by their employer"""
        conn = psycopg2.connect(dbname=self.__database_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                       SELECT e.name, COUNT(*) from vacancies 
                       JOIN employers e USING(employer_id)
                        GROUP BY e.name
                        ORDER BY COUNT(*) DESC
                   """
                        )
            companies = cur.fetchall()
        conn.close()
        for row in companies:
            print(f'Company: {row[0]}. Open vacancies: {row[1]}')

    def get_all_vacancies(self):
        """Method for getting all vacancies with their company name"""
        conn = psycopg2.connect(dbname=self.__database_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                       SELECT e.name, v.name,  from_salary, to_salary, url from vacancies v
                       JOIN employers e USING(employer_id)
					   ORDER BY e.name
                   """
            )
            vacancies = cur.fetchall()
        conn.close()
        for index, vacancy in enumerate(vacancies, 1):
            if vacancy[2] is None:
                salary = f"До {vacancy[3]} руб."
            elif vacancy[3] is None:
                salary = f"От {vacancy[2]} руб."
            else:
                salary = f"От {vacancy[2]} до {vacancy[3]} руб."
            print(f"""Vacancy # {index}
            Company: {vacancy[0]}. Vacancy: {vacancy[1]}
            Salary: {salary}
            Link: {vacancy[4]}""")

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
