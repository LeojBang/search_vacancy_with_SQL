from typing import Any

import psycopg2

from src.base_db import DBBase
from src.logger import setup_logger

# Настроим логгер для этого модуля
logger = setup_logger(__name__)


class DBManager(DBBase):
    """
    Класс для работы с базой данных для извлечения информации о вакансиях и компаниях.

    Этот класс наследуется от DBBase и предоставляет методы для выполнения SQL-запросов к базе данных:
    - Получение количества вакансий по каждой компании.
    - Получение всех вакансий.
    - Получение средней зарплаты по вакансиям.
    - Получение вакансий с зарплатой выше средней.
    - Получение вакансий, содержащих указанное ключевое слово.
    """

    def __init__(self, database_name: str = "headhunter", **params: dict) -> None:
        """Инициализирует объект DBManager с параметрами для подключения к базе данных."""
        super().__init__()
        self.database_name = database_name
        self.params = params
        logger.info(f"Инициализация DBManager с базой данных: {self.database_name}")

    def connect(self) -> Any:
        """Устанавливает соединение с базой данных."""
        # Проверяем, что все необходимые параметры присутствуют
        required_params = ["host", "user", "password", "port"]
        for param in required_params:
            if param not in self.params:
                logger.error(f"Отсутствует обязательный параметр: {param}")
                raise ValueError(f"Отсутствует обязательный параметр: {param}")

        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params)
            logger.info(f"Успешное подключение к базе данных: {self.database_name}")
            return conn
        except psycopg2.Error as e:
            logger.error(f"Ошибка при подключении к базе данных {self.database_name}: {e}")
            raise

    def get_companies_and_vacancies_count(self) -> Any:
        """Получает количество вакансий для каждой компании."""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    logger.info("Запуск запроса для получения количества вакансий по компаниям.")
                    cur.execute(
                        """
                        SELECT employees.employer_name, COUNT(vacancy_id) FROM vacancies
                        JOIN employees ON employees.emp_id = vacancies.emp_id
                        GROUP BY employer_name
                        """
                    )
                    result = cur.fetchall()
                    logger.info("Запрос для получения количества вакансий по компаниям успешно выполнен.")
                    return result
        except Exception as e:
            logger.error(f"Ошибка при получении количества вакансий по компаниям: {e}")
            raise

    def get_all_vacancies(self) -> Any:
        """Получает все вакансии с информацией о работодателе, названии вакансии, зарплате и URL вакансии"""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    logger.info("Запуск запроса для получения всех вакансий.")
                    cur.execute(
                        """
                        SELECT employees.employer_name, vacancies.vacancy_name, vacancies.salary, vacancies.vacancy_url
                        FROM vacancies
                        JOIN employees ON employees.emp_id = vacancies.emp_id
                        """
                    )
                    result = cur.fetchall()
                    logger.info("Запрос для получения всех вакансий успешно выполнен.")
                    return result
        except Exception as e:
            logger.error(f"Ошибка при получении всех вакансий: {e}")
            raise

    def get_avg_salary(self) -> Any:
        """Получает среднюю зарплату по вакансиям."""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    logger.info("Запуск запроса для получения средней зарплаты.")
                    cur.execute(
                        """
                        SELECT vacancies.vacancy_name, AVG(vacancies.salary) FROM vacancies
                        GROUP BY vacancies.vacancy_name
                        """
                    )
                    result = cur.fetchall()
                    logger.info("Запрос для получения средней зарплаты успешно выполнен.")
                    return result
        except Exception as e:
            logger.error(f"Ошибка при получении средней зарплаты: {e}")
            raise

    def get_vacancies_with_higher_salary(self) -> Any:
        """Получает вакансии с зарплатой выше средней."""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    logger.info("Запуск запроса для получения вакансий с зарплатой выше средней.")
                    cur.execute(
                        """
                        SELECT * FROM vacancies
                        WHERE salary > (SELECT AVG(salary) FROM vacancies)
                        """
                    )
                    result = cur.fetchall()
                    logger.info("Запрос для получения вакансий с зарплатой выше средней успешно выполнен.")
                    return result
        except Exception as e:
            logger.error(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")
            raise

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Получает вакансии, содержащие указанное ключевое слово."""
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    logger.info(f"Запуск запроса для получения вакансий с ключевым словом: {keyword}.")
                    cur.execute(
                        f"""
                        SELECT * FROM vacancies
                        WHERE vacancy_name LIKE '%{keyword}%'
                        """
                    )
                    result = cur.fetchall()
                    logger.info(f"Запрос для получения вакансий с ключевым словом '{keyword}' успешно выполнен.")
                    return result
        except Exception as e:
            logger.error(f"Ошибка при получении вакансий с ключевым словом {keyword}: {e}")
            raise
