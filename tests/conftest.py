import psycopg2
import pytest

from src.config import config


@pytest.fixture
def vacancy():
    return [
        {"salary": {"from": 1000, "to": 2000}, "address": "Moscow", "name": "Developer"},
        {"salary": None, "address": "Saint Petersburg", "name": "Analyst"},
        {"salary": {"from": 1500, "to": 3000}, "address": None, "name": "Manager"},
        {"salary": {"from": 2000, "to": 4000}, "address": "Novosibirsk", "name": "Engineer"},
    ]


@pytest.fixture(scope="function")
def db_connection_employees(postgresql):
    conn = postgresql
    cur = conn.cursor()

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


    conn.commit()
    yield conn
    cur.execute("TRUNCATE TABLE employees RESTART IDENTITY;")
    conn.commit()
    cur.close()
    conn.close()


@pytest.fixture(scope="function")
def db_connection_vacancies(postgresql):
    conn = postgresql
    cur = conn.cursor()

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

    conn.commit()
    yield conn
    cur.execute("DROP TABLE vacancies")
    conn.commit()
    cur.close()
    conn.close()

