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
        request_name = self.get_companies_and_vacancies_count.__doc__
        request = '''
                SELECT * FROM employers 
                JOIN (SELECT employer_id, COUNT(*) AS "vacancies" FROM vacancies 
                JOIN employers USING(employer_id) GROUP BY employer_id) AS vacancy_count
                USING (employer_id)  ORDER BY vacancy_count.vacancies DESC;
                '''

        self.get_data_from_bd(request, request_name)

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии, зряплаты и ссылки на вакансию"""
        request_name = self.get_all_vacancies.__doc__
        request = "SELECT vacancies.name AS vacancy, employers.name AS employer, CONCAT(salary_from, ' - ', salary_to)\
                             AS salary, vacancies.url, requirements FROM vacancies \
                            JOIN employers USING (employer_id) \
                            ORDER BY vacancies.salary DESC;"
        self.get_data_from_bd(request, request_name)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова
        """
        pass

