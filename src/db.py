import psycopg2


class DBStore:
    """
    Класс для работы с базой данных
    """
    @staticmethod
    def create_db(db_params: dict, db_name='HH'):
        db_name = db_name
        conn = psycopg2.connect(db_name, *db_params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {db_name}')
        cur.execute(f'CREATE DATABASE {db_name}')

        conn.close()
        conn = psycopg2.connect(db_name, *db_params)

        with conn.cursor() as cur:
            cur.execute('''
                   CREATE TABLE companies(
                   company_id SERIAL PRIMARY KEY,
                   company_name VARCHAR(150) NOT NULL,
                   url_company TEXT
                   )
                   ''')

        with conn.cursor() as cur:
            cur.execute('''
               CREATE TABLE vacancies(
               vacancy_id SERIAL PRIMARY KEY,
               vacancy_name VARCHAR(150) NOT NULL,
               city_name VARCHAR(100),
               publish_date DATE,
               company_id INT ,
               salary_from INTEGER,
               salary_to INTEGER,
               url_vacancy TEXT,
    
               CONSTRAINT fk_vacancies_companies 
               FOREIGN KEY(company_id) REFERENCES companies(company_id)
               )
               ''')

        conn.commit()
        conn.close()

    def save_to_db(self):
        with open('vacancies.json', 'r') as f:
            self.vacancies = json.load(f)
