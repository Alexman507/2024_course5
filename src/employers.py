from src.hh import HH


class Employers(HH):
    """
    Класс для парсинга по url https://api.hh.ru/employers/
    """

    def get_employers(self, employer_ids: list):
        """
        Возвращает список работодателей
        :param employer_ids: список id работодателей
        :return: список работодателей"""
        employers_list = []
        name_list = []
        url_list = []
        for employer_id in employer_ids:
            employer = self.get_response(url=f'https://api.hh.ru/employers/{employer_id}', params=None)
            name_list.append(employer['employer']['name'])
            url_list.append(employer['employer']['url'])
        # Удаляем повторения в названиях работодателей и url функцией "set"
        set_name_list = set(name_list)
        set_url_list = set(url_list)
        for name in set_name_list:
            for url in set_url_list:
                employers_list.append({'employers': {'name': name, 'url': url}})
        return employers_list





