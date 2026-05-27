import psycopg2 as ps
from dotenv import load_dotenv
import os

class database_conn:
    def __init__(self):

        load_dotenv(dotenv_path="db.env")

        self.psqlconn = ps.connect(
            host = os.getenv("DB_HOST"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT")
        )
        self.cursor = self.psqlconn.cursor()

    def auth_dataTable(self):
       
       self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth_data(
        id BIGSERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(100),
        email VARCHAR(60) NOT NULL,
        password VARCHAR(60) NOT NULL,
        date_of_registration VARCHAR(60) NOT NULL,
        phone_number VARCHAR(11),
        accnum VARCHAR(20) NOT NULL UNIQUE
        )''')
       
       self.psqlconn.commit()


class payment(database_conn):
    def __init__(self):
        super().__init__()

    def payment_table_init(self):

       

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment_table (
        id BIGSERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(60) UNIQUE,
        total_bal REAL NOT NULL,
        accountnum VARCHAR(10) NOT NULL UNIQUE
        )''')
        self.psqlconn.commit()


class transaction(database_conn):
    def __init__(self):
        super().__init__()

    def history_table_init(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_tab(
        id BIGSERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(60) NOT NULL,
        sender VARCHAR(60),
        amount REAL,
        date VARCHAR(60) NOT NULL,
        receiver VARCHAR(60) NOT NULL
        )''')
        self.psqlconn.commit()