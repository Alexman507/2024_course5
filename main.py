from src import hh, db, dbmanager, config, employers, vacancies


def main():
    employer_ids = [  # Выбранные работодатели
        2365329,  # 1 UpTrader
        2061860,  # 2 ООО Фандог
        2539590,  # 3 ООО DM365
        77364,  # 4 Petrovich
        1795976,  # 5 ITMO
        856498,  # 6 LESTA GAMES
        10938683,  # 7 Yakov Lushkov Neuro-Agency
        10069618,  # 8 ООО Редеп Эдженси
        5817234,  # 9 ООО Оператор Газпром ИД
        10955120,  # 10 СДД
        5686111,  # 11 Olima
        4295296,  # 12 SoftWise
        2261,  # 13 Балтика
        581224,  # 14 Монополия
        53676,  # 15 ОБИТ
        773781,  # 16 DATADVANCE

    ]
    db_params = config.config()
    db_store = db.DBStore(db_params=db_params, db_name='hh')
    # db_store.check_connection()
    # db_store.create_db()
    # db_store.create_tables()
    employers1 = employers.Employers()
    employers_to_db, vacancy_url = employers1.get_employers(employer_ids)
    vacancies1 = vacancies.Vacancies()
    vacancies_ids = employers1.get_vacancies_ids(vacancy_url)
    vacancies_to_db = vacancies1.get_vacancies(vacancies_ids)
    db_store.save_to_db(vacancies_list=vacancies_to_db, employer_list=employers_to_db)


def check_dbmanager_workflow():
    db_params = config.config()
    db_manager = dbmanager.DBManager(db_params=db_params, db_name='hh')
    # db_manager.get_companies_and_vacancies_count()
    # db_manager.get_all_vacancies()
    # db_manager.get_avg_salary()
    # db_manager.get_vacancies_with_higher_salary()
    db_manager.get_vacancies_with_keyword(word_list=['python', 'разработчик'])


if __name__ == '__main__':
    # main()
    check_dbmanager_workflow()
