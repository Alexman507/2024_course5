import psycopg2

from src.db import DBStore


class DBManager(DBStore):
    """Класс для вывода информации из БД PostgreSQL"""

    def get_data_from_bd(self, request, request_name):
        """
        Получает данные с помощью запроса
        С выводом на печать
        request_name - что запрос должен показать
        """
        print(f"ЗАПРОС: {request_name}:")
        with psycopg2.connect(**self.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(request)
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии, зряплаты и ссылки на вакансию"""
        request_name = self.get_all_vacancies.__doc__
        request = "SELECT vacancies.name AS vacancy, employers.name AS employer, salary, vacancies.url,\
                            region_name, requirements FROM vacancies \
                            JOIN employers USING (employer_id) \
                            ORDER BY vacancies.salary DESC;"
        self.get_data_from_bd(request, request_name)

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass

