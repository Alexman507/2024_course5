from abc import ABC

import requests

from src.abstract_api import AbstractAPI


class HH(AbstractAPI, ABC):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, area=113) -> None:
        self.area = area
        self.params = None

    def get_response(self, url, params):
        """Возвращает ответ из сайта по заданным параметрам
        :param url: адрес запроса к API
        :param params: параметры для запроса"""

        try:
            response = requests.get(url, self.params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(e.args)
            return None


