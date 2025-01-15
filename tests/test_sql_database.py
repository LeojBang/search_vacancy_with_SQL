import pytest

from src.config import config
from src.sql_database import DataBaseSQL


@pytest.mark.parametrize("employer_id, employer_name, employer_url", [
    ("816144", "ВкусВилл", "https://hh.ru/employer/816144"),
    ("78638", "Т-Банк", "https://hh.ru/employer/78638"),
])
def test_sql_database_employees(connect_to_db, employer_id, employer_name, employer_url):
    params = config()
    database = DataBaseSQL('test_headhunter', **params)
    conn = connect_to_db
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO employees (employer_id, employer_name, employer_url)
    VALUES (%s, %s, %s)
    """, (employer_id, employer_name, employer_url))
    conn.commit()

    cur.execute("SELECT * FROM employees")

    row = cur.fetchone()
    # Убедимся, что данные были вставлены корректно
    assert row[1:] == (int(employer_id), employer_name, employer_url)
