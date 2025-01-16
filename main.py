from src.config import config
from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.sql_database import DataBaseSQL


def main() -> None:
    hh = HeadHunterAPI()
    params = config()
    database = DataBaseSQL(**params)

    # Вставка данных о вакансиях в базу данных
    database.insert_data_to_db(hh.vacancies)

    # Подключение к базе данных через DBManager
    count = DBManager(**params)

    print("Привет! Я помогу тебе с информацией о вакансиях.")

    # Вывод всех вакансий
    print("\nВсе вакансии:")
    vacancies = count.get_all_vacancies()
    if vacancies:
        for vacancy in vacancies:
            employer_name, vacancy_name, salary, vacancy_url = vacancy
            print(f"Компания: {employer_name}")
            print(f"Вакансия: {vacancy_name}")
            print(f"Зарплата: {salary} руб.")
            print(f"Подробнее: {vacancy_url}\n")
    else:
        print("Вакансии не найдены.")

    # Компании и количество вакансий
    print("\nКомпании и количество вакансий:")
    companies_vacancies = count.get_companies_and_vacancies_count()
    if companies_vacancies:
        for company, count_vacancies in companies_vacancies:
            print(f"Компания: {company} - Вакансий: {count_vacancies}")
    else:
        print("Информация о компаниях не найдена.")

    # Средняя зарплата по вакансиям
    print("\nСредняя зарплата по вакансиям:")
    avg_salary = count.get_avg_salary()
    if avg_salary:
        for vacancy_name, avg in avg_salary:
            print(f"Вакансия: {vacancy_name} - Средняя зарплата: {round(avg, 2)} руб.")
    else:
        print("Не удалось получить информацию о средней зарплате.")

    # Вакансии с зарплатой выше средней
    print("\nВакансии с зарплатой выше средней:")
    high_salary_vacancies = count.get_vacancies_with_higher_salary()
    if high_salary_vacancies:
        for vacancy in high_salary_vacancies:
            vacancy_id, vacancy_name, vacancy_url, city, salary, employer_id = vacancy
            print(f"Вакансия: {vacancy_name}")
            print(f"Ссылка на вакансию: {vacancy_url}")
            print(f"Город: {city}")
            print(f"Зарплата: {salary} руб.\n")
    else:
        print("Вакансии с зарплатой выше средней не найдены.")

    # Поиск вакансий по ключевому слову
    keyword_for_searching = input(
        "\nВведите ключевое слово для поиска\nОставьте поле пустым, если хотите посмотреть все вакансии: "
    )
    if keyword_for_searching:
        print(f"\nВакансии с ключевым словом '{keyword_for_searching}':")
        search_results = count.get_vacancies_with_keyword(keyword_for_searching)
        if search_results:
            for vacancy in search_results:
                emp_id, vacancy_id, employer_name, vacancy_name, salary, vacancy_url = vacancy
                print(f"Вакансия: {employer_name}")
                print(f"Ссылка на вакансию: {vacancy_name}")
                print(f"Город: {salary}")
                print(f"Зарплата: {vacancy_url} руб.\n")
        else:
            print("Вакансий с таким ключевым словом не найдено.")
    else:
        print("\nВы выбрали показать все вакансии.")
        vacancies = count.get_all_vacancies()
        for vacancy in vacancies:
            employer_name, vacancy_name, salary, vacancy_url = vacancy
            print(f"Компания: {employer_name}")
            print(f"Вакансия: {vacancy_name}")
            print(f"Ссылка на вакансию: {vacancy_url}")
            print(f"Зарплата: {salary} руб.\n")


if __name__ == "__main__":
    main()
