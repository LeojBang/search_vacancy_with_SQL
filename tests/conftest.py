import json
import os

import pytest

from src.config import config
from src.db_manager import DBManager
from src.sql_database import DataBaseSQL


@pytest.fixture
def vacancy():
    return [
        {"salary": {"from": 1000, "to": 2000}, "address": "Moscow", "name": "Developer"},
        {"salary": None, "address": "Saint Petersburg", "name": "Analyst"},
        {"salary": {"from": 1500, "to": 3000}, "address": None, "name": "Manager"},
        {"salary": {"from": 2000, "to": 4000}, "address": "Novosibirsk", "name": "Engineer"},
    ]


@pytest.fixture
def vacancies():
    file_path = os.path.join(os.path.dirname(__file__), "../data/data.json")
    with open(file_path) as f:
        return json.load(f)


@pytest.fixture
def db_instance(vacancies):
    """Фикстура для создания экземпляра DataBaseSQL и вставки данных."""
    params = config()
    db = DataBaseSQL("test_sql_database", **params)
    db.insert_data_to_db(vacancies)
    return db, params


@pytest.fixture
def dbm_instance(vacancies):
    """Фикстура для создания экземпляра DataBaseSQL и вставки данных."""
    params = config()
    dbm = DBManager("test_sql_database", **params)
    return dbm, params
