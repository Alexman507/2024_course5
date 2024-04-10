import json
from abc import ABC, abstractmethod

import psycopg2
import requests


class AbstractAPI(ABC):
    """
    Абстрактный класс для работы с API
    """

    @abstractmethod
    def get_url(self, params):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def create_db(self):
        pass

    @abstractmethod
    def save_to_db(self):
        pass


class HH(AbstractAPI, ABC):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, area=113, employer_id=None) -> None:
        self.area = area
        self.params = {
            'text': '',
            'page': 0,
            'per_page': 20,
            'area': self.area,
            'only_with_vacancies': True,
            'employer_id': employer_id,
        }
        vacancies = []

    def get_url(self, params):
        """Возвращает ответ из сайта по заданным параметрам
        :param params: параметры для запроса"""

        return requests.get("https://api.hh.ru/vacancies/", self.params).json()['items']

    def create_db(self):
        db_name = 'HH'
        conn = psycopg2.connect(db_name, params=self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {db_name}')
        cur.execute(f'CREATE DATABASE {db_name}')

        conn.close()
        conn = psycopg2.connect(db_name, params=self.params)

        with conn.cursor() as cur:
            cur.execute('''
                   CREATE TABLE companies(
                   company_id SERIAL PRIMARY KEY,
                   company_name VARCHAR(150) NOT NULL,
                   url_company TEXT
                   )
                   ''')

        with conn.cursor() as cur:
            cur.execute('''
               CREATE TABLE vacancies(
               vacancy_id SERIAL PRIMARY KEY,
               vacancy_name VARCHAR(150) NOT NULL,
               city_name VARCHAR(100),
               publish_date DATE,
               company_id INT ,
               salary_from INTEGER,
               salary_to INTEGER,
               url_vacancy TEXT,

               CONSTRAINT fk_vacancies_companies 
               FOREIGN KEY(company_id) REFERENCES companies(company_id)
               )
               ''')

        conn.commit()
        conn.close()

    def get_vacancies(self):
        """Возвращает список вакансий"""

        self.vacancies = self.get_url(self.params)
        return self.vacancies

    def save_to_db(self):
        with open('vacancies.json', 'r') as f:
            self.vacancies = json.load(f)

