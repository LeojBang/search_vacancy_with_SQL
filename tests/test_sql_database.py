import psycopg2
import pytest

from src.sql_database import DataBaseSQL


def test_sql_database_insert_data_to_db(db_instance, vacancies):
    db, params = db_instance

    with psycopg2.connect(dbname="test_sql_database", **params) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM employer")
            rows = cursor.fetchall()
            assert len(rows) == 10
            assert rows[0][2] == "ВкусВилл"
            assert rows[1][2] == "Ростелеком"


def test_sql_database_error_connection(db_instance, vacancies):
    db, params = db_instance
    with pytest.raises(psycopg2.Error):
        DataBaseSQL(
            "test_sql_database",
            user=params.get("user"),
            password="12345",
            host=params.get("host", "localhost"),
        )
