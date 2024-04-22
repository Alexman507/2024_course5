import psycopg2


class DBStore:
    """
    Класс для работы с базой данных
    """
    def __init__(self, db_params, db_name='HH'):
        self.db_params: dict = db_params
        self.db_name = db_name

    def create_db(self):
        name = self.db_name
        params = self.db_params
        conn = psycopg2.connect(name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {name}')
        cur.execute(f'CREATE DATABASE {name}')

        conn.close()
        conn = psycopg2.connect(name, **params)

        with conn.cursor() as cur:
            cur.execute('''
                   CREATE TABLE employers(
                   employer_id INT PRIMARY KEY,
                   employer_name VARCHAR(150) NOT NULL,
                   url_employer TEXT
                   )
                   ''')

        with conn.cursor() as cur:
            cur.execute('''
               CREATE TABLE vacancies(
               vacancy_id INT PRIMARY KEY,
               vacancy_name VARCHAR(150) NOT NULL,
               city_name VARCHAR(100),
               publish_date DATE,
               employer_id INT ,
               salary_from INTEGER,
               salary_to INTEGER,
               url_vacancy TEXT,
    
               CONSTRAINT fk_vacancies_employers 
               FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
               )
               ''')

        conn.commit()
        conn.close()

    def save_to_db(self, vacancies_list, employer_list):
        name = self.db_name
        params = self.db_params
        conn = psycopg2.connect(name, **params)
        with conn.cursor() as cur:
            for employer in employer_list:
                cur.execute(
                    '''
                    INSERT INTO employers (employer_name)
                    VALUES (%s)
                    RETURNING employer_id
                    ''',
                    employer
                )
                employer_id = cur.fetchone()[0]
            for item in response:
                cur.execute(
                    '''
                    INSERT INTO vacancies (
                    vacancy_name,
                    city_name,
                    publish_date,
                    employer_id,
                    salary_from,
                    salary_to,
                    url_vacancy
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (
                        item['vacancy_name'],
                        item['city_name'],
                        item['publish_date'],
                        employer_id,
                        item['salary_from'],
                        item['salary_to'],
                        item['url_vacancy']
                    )
                )


