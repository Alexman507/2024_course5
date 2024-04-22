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
            vacancies = self.get_response(url=f'https://api.hh.ru/vacancies/{vacancy_id}', params=None)
            for vacancy in vacancies:
                vacancies_list.append({'vacancies': {
                    'vacancy': vacancy['name'],
                    'city': vacancy['area']['name'],
                    'salary_from': vacancy['salary']['from'],
                    'salary_to': vacancy['salary']['to'],
                    'date_published': vacancy['published_at'],
                    'url_vacancy': vacancy['url'],
                }})
        return vacancies_list
