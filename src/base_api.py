from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс инициализации пути до файла и получения вакансий по ключевому слову"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def _load_vacancies(self) -> None:
        """Метод для загрузки вакансий"""
        pass

    @abstractmethod
    def _validate_vacancy(self) -> None:
        """Метод проверки, что нужные данные не имеют значение None"""
        pass
