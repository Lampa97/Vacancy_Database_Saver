from abc import ABC, abstractmethod

import psycopg2

from src.logger import logger_setup

db_logger = logger_setup()


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

    def __init__(self, password, database_name='hh_vacancies'):
        self.__params = {'host': 'localhost', 'user': 'postgres', 'password': password}
        self.__database_name = database_name

    def create_database(self):
        conn = psycopg2.connect(
            dbname='postgres', **self.__params
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {self.__database_name}")
        cur.execute(f"CREATE DATABASE {self.__database_name}")

        conn.close()

        db_logger.info(f'Created database {self.__database_name}')

        conn = psycopg2.connect(dbname=self.__database_name, **self.__params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL,
                    name VARCHAR(255) NOT NULL,
                    CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)
                )
            """)
        db_logger.info('Created table employers')

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL,
                    name VARCHAR(255),
                    from_salary INTEGER,
                    to_salary INTEGER,
                    url TEXT,
                    employer_id INTEGER REFERENCES employers(employer_id)
                )
            """)
        db_logger.info('Created table vacancies')
        conn.commit()
        conn.close()

    def fill_up_tables(self, companies, vacancies):
        conn = psycopg2.connect(dbname=self.__database_name, **self.__params)

        with conn.cursor() as cur:
            for employer in companies:
                cur.execute(f"""
                    INSERT INTO employers (name) VALUES ('{employer}')
                """)
            db_logger.info('Successfully inserted data into employers')
            for vacancy in vacancies:
                cur.execute(f"""
                    INSERT INTO vacancies (name, from_salary, to_salary, url, employer_id) 
                    VALUES (%s, %s, %s, %s, (SELECT employer_id from employers e WHERE e.name = '{vacancy['employer']}'))
                    """, (vacancy['name'], vacancy['salary']['from'], vacancy['salary']['to'], vacancy['url']))
            db_logger.info('Successfully inserted data into vacancies')
        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass

