from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """
    Абстрактный класс для работы с API
    """

    @abstractmethod
    def get_response(self, url, params):
        pass
