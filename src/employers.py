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
        name_list = []
        url_list = []
        vacancy_url = []
        for employer_id in employer_ids:
            employer = self.get_response(url=f'https://api.hh.ru/employers/{employer_id}', params=self.params)
            name_list.append(employer['name'])
            url_list.append(employer['alternate_url'])
            vacancy_url.append({'employer_name': employer['name'], 'vacancies_url': employer['vacancies_url']})
        # Удаляем повторения в названиях работодателей и url функцией "set"
        set_name_list = set(name_list)
        set_url_list = set(url_list)
        for name in set_name_list:
            for url in set_url_list:
                employers_list.append({'employers': {'name': name, 'url': url}})
        return employers_list, vacancy_url

    def get_vacancies_ids(self, vacancy_url, filter_area=None):
        """
        Возвращает список доступных id вакансий
        :param vacancy_url: список вакансий (items) по работодателю
        :param filter_area: id города/области
        :return: список id вакансий
        """
        vacancies_ids = []
        vacancies = self.get_response(url=f'{vacancy_url["vacancies_url"]}', params=self.params)
        items = vacancies['items']
        for vacancy in items:
            if filter_area:
                if vacancy['area']['id'] == filter_area:
                    vacancies_ids.append(vacancy['id'])
            vacancies_ids.append(vacancy['id'])
        return vacancies_ids





