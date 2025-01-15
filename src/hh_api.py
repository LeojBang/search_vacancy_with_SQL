import requests

from src.base_api import BaseAPI
from src.logger import setup_logger

logger = setup_logger(__name__)


class HeadHunterAPI(BaseAPI):
    """
    Класс для работы с API HeadHunter.
    Этот класс выполняет загрузку вакансий с API HeadHunter, проверку данных вакансий на наличие обязательных полей
    (зарплаты и адреса) и их валидацию.
    Наследует от класса BaseAPI, который реализует основные функции для работы с API.
    """

    def __init__(self) -> None:
        """
        Инициализирует объект для работы с API HeadHunter.
        Устанавливает базовый URL для запросов, заголовки, параметры поиска вакансий и выполняет
        загрузку вакансий и их валидацию.
        """
        logger.info("Инициализация API HeadHunter")

        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {
            "text": None,
            "page": 0,
            "per_page": 100,
            "employer_id": [
                "1942330",
                "49357",
                "3036416",
                "78638",
                "2748",
                "2848663",
                "2180",
                "1942336",
                "3529",
                "816144",
            ],
        }
        self.__vacancies: list = []
        self._load_vacancies()
        self._validate_vacancy()
        logger.info(f"Загружено {len(self.__vacancies)} вакансий")

    @property
    def vacancies(self) -> list:
        """
        Возвращает список вакансий.
        """
        return self.__vacancies

    def _load_vacancies(self) -> None:
        """
        Загружает вакансии с API HeadHunter.
        Делаются запросы на страницы с вакансиями, начиная с первой страницы и до 20-й,
        с целью получения всех вакансий.
        Если API возвращает ошибку, возбуждается исключение.
        """
        logger.info("Начинаем загрузку вакансий")

        while self.__params["page"] != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code != 200:
                logger.error(f"Ошибка при запросе к API: статус {response.status_code}")

                raise requests.HTTPError(f"Ошибка при запросе к API: статус {response.status_code}")

            vacancies = response.json().get("items", [])
            logger.info(f"Получено {len(vacancies)} вакансий со страницы {self.__params['page']}")

            self.__vacancies.extend(vacancies)

            # Обеспечиваем, что self.params["page"] всегда целое число
            current_page = self.__params["page"]
            if isinstance(current_page, int):  # Проверка на тип
                self.__params["page"] = current_page + 1
        logger.info("Загрузка вакансий завершена")

    def _validate_vacancy(self) -> None:
        """
        Валидирует вакансии, удаляя те, у которых отсутствуют обязательные данные (зарплата или адрес).
        Удаляет вакансии, если зарплата или адрес не указаны.
        """

        for vacancy in self.__vacancies.copy():
            if vacancy["salary"] is None or vacancy["address"] is None:
                self.__vacancies.remove(vacancy)
