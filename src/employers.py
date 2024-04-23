from src.hh import HH


class Employers(HH):
    """
    Класс для парсинга по url https://api.hh.ru/employers/
    """

    def get_employers(self, employer_ids: list):
        """
        Возвращает список работодателей
        :param employer_ids: список id работодателей
        :return: список работодателей (название, ссылка на hh)
        :return: список работодателей (название, ссылка на список вакансий)
        """
        employers_list = []
        vacancy_url = []
        for employer_id in employer_ids:
            employer = self.get_response(url=f'https://api.hh.ru/employers/{employer_id}', params=self.params)
            employers_list.append({'employer_name': employer['name'],
                                   'employer_id': employer['id'],
                                   'url_employer': employer['alternate_url']})
            vacancy_url.append({'employer_name': employer['name'],
                                'vacancies_url': employer['vacancies_url']})
        # print(vacancy_url)
        return employers_list, vacancy_url

    def get_vacancies_ids(self, vacancy_url, filter_area=None):
        """
        Возвращает список доступных id вакансий
        :param vacancy_url: список вакансий (items) по работодателю
        :param filter_area: id города/области
        :return: список id вакансий
        """
        vacancies_ids = []
        for url in vacancy_url:
            vacancies = self.get_response(url=url['vacancies_url'], params=self.params)
            for vacancy in vacancies['items']:
                if filter_area:
                    if vacancy['area']['id'] == filter_area:
                        vacancies_ids.append(vacancy['id'])
                vacancies_ids.append(vacancy['id'])
        return vacancies_ids





