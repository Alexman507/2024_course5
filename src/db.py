import psycopg2


class DBStore:
    """
    Класс для работы с базой данных (подключение, создание, запись)
    """

    def __init__(self, db_params, db_name='hh'):
        self.db_params: dict = db_params
        self.db_name = db_name
        self.conn = psycopg2.connect(**self.db_params)
        self.conn.autocommit = True

    def check_connection(self):
        with self.conn.cursor() as cur:
            cur.execute('SELECT 1')
        self.conn.close()

    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute(f'CREATE DATABASE {self.db_name}')
            self.conn.close()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                   CREATE TABLE employers(
                   employer_id INT PRIMARY KEY,
                   employer_name VARCHAR(150) NOT NULL,
                   url_employer TEXT
                   )
                   ''')

        with self.conn.cursor() as cur:
            cur.execute('''
               CREATE TABLE vacancies(
               vacancy_id INT PRIMARY KEY,
               vacancy_name VARCHAR(150) NOT NULL,
               city_name VARCHAR(100),
               date_published DATE,
               employer_id INT ,
               salary_from INTEGER,
               salary_to INTEGER,
               url_vacancy TEXT,
    
               CONSTRAINT fk_vacancies_employers 
               FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
               )
               ''')

        self.conn.close()

    def save_to_db(self, vacancies_list, employer_list):
        print('vacancies_list:', vacancies_list)
        print('employer_list:', employer_list)
        with self.conn.cursor() as cur:
            for employer in employer_list:
                cur.execute(
                    '''
                    INSERT INTO employers (employer_name, employer_id, url_employer)
                    VALUES (%s, %s, %s)
                    ''',
                    (employer['employer_name'], employer['employer_id'], employer['url_employer'])
                )
            for item in vacancies_list:
                cur.execute(
                    '''
                    INSERT INTO vacancies (
                    vacancy_id,
                    vacancy_name,
                    city_name,
                    date_published,
                    employer_id,
                    salary_from,
                    salary_to,
                    url_vacancy
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''',
                    (
                        item['vacancy_id'],
                        item['vacancy_name'],
                        item['city_name'],
                        item['date_published'],
                        item['employer_id'],
                        item['salary_from'],
                        item['salary_to'],
                        item['url_vacancy']
                    )
                )
        self.conn.close()
