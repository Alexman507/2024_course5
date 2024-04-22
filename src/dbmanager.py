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
        request = '''SELECT vacancies.name AS vacancy, employers.name AS employer, CONCAT(salary_from, ' - ', salary_to)
                             AS salary, vacancies.url, requirements FROM vacancies
                            JOIN employers USING (employer_id)
                            ORDER BY vacancies.salary DESC;'''
        self.get_data_from_bd(request, request_name)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        request_name = self.get_avg_salary.__doc__
        request = '''SELECT vacancies.name, CONCAT(CAST(AVG(vacancies.salary) AS int), ' рублей'), 
                        CONCAT(COUNT(vacancies.name), ' шт.') AS number_of_vacancies 
                        FROM vacancies GROUP BY vacancies.name 
                        ORDER BY AVG(vacancies.salary) DESC;'''

        self.get_data_from_bd(request, request_name)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        request_name = self.get_vacancies_with_higher_salary.__doc__
        request = '''SELECT * FROM vacancies, 
                        (SELECT AVG(vacancies.salary) AS middle_salary FROM vacancies WHERE vacancies.salary > 0) 
                        AS vacancy_avg WHERE vacancies.salary > vacancy_avg.middle_salary 
                        ORDER BY vacancies.salary DESC;'''
        self.get_data_from_bd(request, request_name)

    def get_vacancies_with_keyword(self, word_list):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова
        """
        request_name = self.get_vacancies_with_keyword.__doc__
        head = "SELECT * FROM vacancies"
        end = ''
        for i, w in enumerate(word_list, start=0):
            if i == 0:
                end += f" WHERE vacancies.name LIKE '%{w}%'"
            else:
                end += f" OR vacancies.name LIKE '%{w}%'"
        else:
            end += ' ORDER BY vacancies.name DESC;'
        request = head + end
        self.get_data_from_bd(request, request_name)

