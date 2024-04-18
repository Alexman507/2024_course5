


def create_db(self, db_params):
    db_name = 'HH'
    conn = psycopg2.connect(db_name, db_params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    conn.close()
    conn = psycopg2.connect(db_name, params=self.params)

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


def get_employers(self, employer_ids: list):
    """Возвращает список работодателей"""
    employers_list = []
    for employer_id in employer_ids:
        name_list = []
        url_list = []
        employers = self.get_url(employer_id)
        for employer in employers:
            name_list.append(employer['employer']['name'])
            url_list.append(employer['employer']['url'])
        # Удаляем повторения в названиях работодателей и url функцией "set"
        set_name_list = set(name_list)
        set_url_list = set(url_list)
        for name in set_name_list:
            for url in set_url_list:
                employers_list.append({'employers': {'name': name, 'url': url}})
    return employers_list


def get_vacancies(self, employee_ids):
    """Возвращает список вакансий"""
    vacancies_list = []
    for employee_id in employee_ids:
        vacancies = self.get_url(employee_id)
        for vacancy in vacancies:
            vacancies_list.append({'vacancies': {
                'vacancy': vacancy['name'],
                'city': vacancy['area']['name'],
                'salary_from': vacancy['salary']['from'],
                'salary_to': vacancy['salary']['to'],
                'date_published': vacancy['published_at'],
                'url_vacancy': vacancy['url'],
            }})
    return vacancies_list


def save_to_db(self):
    with open('vacancies.json', 'r') as f:
        self.vacancies = json.load(f)