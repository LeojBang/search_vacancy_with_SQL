from abc import ABC, abstractmethod


class Base_SQL(ABC):
    def __init__(self, database_name: str, params: dict) -> None:
        pass

    @abstractmethod
    def create_database(self) -> None:
        pass

    @abstractmethod
    def create_tables(self) -> None:
        pass

    @abstractmethod
    def insert_data_to_db(self, vacancies: list[dict]) -> None:
        pass
