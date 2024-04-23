from src.hh import HH


class Vacancies(HH):
    """Класс для работы с API HeadHunter по адресу https://api.hh.ru/vacancies/"""

    def get_vacancies(self, vacancies_ids):
        """Возвращает список вакансий
        :param vacancies_ids: список id вакансий
        :return: список вакансий {
        название,
        город,
        зарплата "от",
        зарплата "до",
        дата публикации,
        url вакансии,
        }"""
        vacancies_list = []
        for vacancy_id in vacancies_ids:
            vacancy = self.get_response(url=f'https://api.hh.ru/vacancies/{vacancy_id}', params=None)
            # print(vacancy)
            if self.if_salary(vacancy):
                vacancies_list.append({
                    'vacancy_id': vacancy['id'],
                    'vacancy_name': vacancy['name'],
                    'city_name': vacancy['area']['name'],
                    'salary_from': vacancy['salary']['from'],
                    'salary_to': vacancy['salary']['to'],
                    'date_published': vacancy['published_at'],
                    'url_vacancy': vacancy['alternate_url'],
                    'employer_id': vacancy['employer']['id'],
                })
        # print(vacancies_list)
        return vacancies_list

    @staticmethod
    def if_salary(vacancy):
        if 'salary' in vacancy:
            if vacancy['salary']:
                return True
