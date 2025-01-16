from decimal import Decimal


def test_db_manager_get_all_vacancies(dbm_instance):
    dbm, params = dbm_instance
    vacancy = dbm.get_all_vacancies()
    assert len(vacancy) == 522
    assert vacancy[0][0] == "ВкусВилл"
    assert vacancy[0][1] == "Специалист по тендерам"
    assert vacancy[0][2] == 200000
    assert vacancy[0][3] == "https://hh.ru/vacancy/115482776"


def test_db_manager_get_companies_and_vacancies_count(dbm_instance):
    dbm, params = dbm_instance
    vacancy = dbm.get_companies_and_vacancies_count()
    assert len(vacancy) == 10
    assert vacancy[0][0] == "ВкусВилл"
    assert vacancy[0][1] == 93


def test_db_manager_get_avg_salary(dbm_instance):
    dbm, params = dbm_instance
    vacancy = dbm.get_avg_salary()
    assert len(vacancy) == 366
    assert vacancy[0][0] == "Специалист отдела телемаркетинга (работа из дома), г. Самара"
    assert vacancy[0][1] == Decimal(61000.000000000000)


def test_db_manager_get_vacancies_with_higher_salary(dbm_instance):
    dbm, params = dbm_instance
    vacancy = dbm.get_vacancies_with_higher_salary()
    assert len(vacancy) == 207
    assert vacancy[0][1] == "Специалист по тендерам"
    assert vacancy[0][2] == "https://hh.ru/vacancy/115482776"
    assert vacancy[0][3] == "Москва"
    assert vacancy[0][4] == 200000


def test_db_manager_get_vacancies_with_keyword(dbm_instance):
    dbm, params = dbm_instance
    keyword_for_vacancy = "Специалист"
    vacancy = dbm.get_vacancies_with_keyword(keyword_for_vacancy)
    assert len(vacancy) == 55
    assert vacancy[0][1] == "Специалист по тендерам"
    assert vacancy[1][1] == "Специалист по взысканию и розыску автомобилей"
    assert vacancy[4][1] == "Специалист по лабораторным исследованиям"
    assert vacancy[10][1] == "Специалист по работе с клиентами"
