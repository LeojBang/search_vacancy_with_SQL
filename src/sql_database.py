from typing import Any

import psycopg2

from src.base_sql import Base_SQL
from src.logger import setup_logger

logger = setup_logger(__name__)


class DataBaseSQL(Base_SQL):
    """
    Класс для работы с базой данных SQL.
    Выполняет создание базы данных и таблиц, а также подключение к базе данных.
    """

    def __init__(self, database_name: str = "headhunter", **params: dict[str, Any]):
        super().__init__(database_name, params)
        self.database_name = database_name
        self.params = params
        try:
            logger.info("Подключаемся к базе данных PostgreSQL для создания базы.")
            self.conn = psycopg2.connect(dbname="postgres", **self.params)
            self.conn.autocommit = True
            logger.info(f"Подключение к базе данных {self.database_name} успешно установлено.")
        except psycopg2.Error as e:
            logger.error(f"Ошибка подключения к базе данных PostgreSQL: {e}")
            raise

        self.create_database()
        self.create_tables()

    def create_database(self) -> None:
        """Создаем базу данных, если её нет"""
        try:
            logger.info(f"Создаём базу данных {self.database_name} (если её нет).")

            with self.conn.cursor() as cur:
                cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
                cur.execute(f"CREATE DATABASE {self.database_name}")
                logger.info(f"База данных {self.database_name} успешно создана.")

        except psycopg2.Error as e:
            logger.error(f"Ошибка при создании базы данных: {e}")
            raise

        finally:
            self.conn.close()

    def create_tables(self) -> None:
        """Создаем таблицы в базе данных"""
        try:
            logger.info(f"Создаём таблицы в базе данных {self.database_name}.")

            self.conn = psycopg2.connect(dbname=self.database_name, **self.params)  # Подключение к новой базе
            self.conn.autocommit = True

            # Создаем таблицы
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS employees (
                        emp_id SERIAL PRIMARY KEY,
                        employer_id int,
                        employer_name VARCHAR(100),
                        employer_url VARCHAR(100)
                    )
                """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        emp_id int,
                        vacancy_name VARCHAR(100),
                        vacancy_url VARCHAR(100),
                        city VARCHAR(50),
                        salary INT,
                        FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
                    )
                """
                )
            logger.info("Таблицы успешно созданы.")
        except psycopg2.Error as e:
            logger.error(f"Ошибка при создании таблиц: {e}")
            raise
        finally:
            self.conn.commit()
            self.conn.close()

    def insert_data_to_db(self, vacancies: list[dict]) -> None:
        """Вставляем данные в таблицы базы данных"""
        try:
            logger.info(f"Начинаем вставку данных в базу данных {self.database_name}.")

            self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                for vacancy in vacancies:
                    try:
                        # Вставляем данные в таблицу employees
                        cur.execute(
                            """
                            INSERT INTO employees (employer_id, employer_name, employer_url)
                            VALUES (%s, %s, %s)
                            RETURNING emp_id
                        """,
                            (
                                vacancy.get("employer", {}).get("id"),
                                vacancy.get("employer", {}).get("name"),
                                vacancy.get("employer", {}).get("alternate_url"),
                            ),
                        )

                        # Получаем ID работодателя
                        employer_id = cur.fetchone()[0]

                        # Вставляем данные в таблицу vacancies
                        cur.execute(
                            """
                            INSERT INTO vacancies (emp_id, vacancy_name, vacancy_url, city, salary)
                            VALUES (%s, %s, %s, %s, %s)
                        """,
                            (
                                employer_id,
                                vacancy.get("name"),
                                vacancy.get("alternate_url"),
                                vacancy.get("address", {}).get("city"),
                                (
                                    vacancy.get("salary", {}).get("from")
                                    if vacancy.get("salary", {}).get("from") is not None
                                    else vacancy.get("salary", {}).get("to")
                                ),
                            ),
                        )
                        logger.info(f"Вакансия {vacancy.get('id')} успешно вставлена.")

                    except psycopg2.Error as e:
                        logger.error(f"Ошибка при обработке вакансии {vacancy.get('id')}: {e}")
                        continue
                    except KeyError as e:
                        logger.warning(f"KeyError: отсутствует ключ {e} в вакансии {vacancy.get('id')}")
                        continue
                    except TypeError as e:
                        logger.warning(f"TypeError: неверный тип данных в вакансии {vacancy.get('id')}: {e}")
                        continue
                    except Exception as e:
                        logger.error(f"Неизвестная ошибка при обработке вакансии {vacancy.get('id')}: {e}")
                        continue
            logger.info("Все вакансии успешно вставлены.")
        except psycopg2.Error as e:
            logger.error(f"Ошибка при подключении к базе данных для вставки данных: {e}")
            raise
        finally:
            self.conn.commit()
            self.conn.close()
