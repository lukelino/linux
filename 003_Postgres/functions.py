import sys
from configparser import ConfigParser
import psycopg2


f_name = r'/home/lukelino/Py/003_Postgres/config.ini'


def config(filename=f_name, section='postgres'):
    """ Read the config.ini file """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db.setdefault(param[0], param[1])
    else:
        print(f'No section {section} in {filename}.')
    return db


def connect():
    """ Connect with Postgres database """
    try:
        parameters = config()
        connection = psycopg2.connect(**parameters)
        cursor = connection.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        sys.exit(error)
    return connection, cursor


def disconnect(connection, cursor):
    """ Close the connection with Postgres """
    if connection:
        connection.close()
        cursor.close()
    else:
        print('No connection has been established.')


def create_table(connection, cursor, table):
    """ Creates table in Postgres database """
    if connection:
        try:
            postgres_query_data = f""" 
            CREATE TABLE IF NOT EXISTS {table}
            (
            id BIGSERIAL NOT NULL PRIMARY KEY,
             first_name VARCHAR(25) NOT NULL,
             last_name VARCHAR(50) NOT NULL,
             school VARCHAR(50) NOT NULL,
             hire_date DATE NOT NULL,
             salary NUMERIC NOT NULL 
             );
            """
            cursor.execute(postgres_query_data)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            sys.exit(error)


def insert_data(connection, cursor, table):
    """ Insert data into Postgres database """
    if connection:
        try:
            while (first_name := input('First name: ')) != '':
                last_name = input('Last name: ')
                school = input('School: ')
                hire_date = input('Hire date: ')
                salary = input('Salary: ')
                postgres_query_data = f"""
                INSERT INTO {table} (first_name, last_name, school, hire_date, salary)
                VALUES ('{first_name}', '{last_name}', '{school}', '{hire_date}', {salary});
                """
                cursor.execute(postgres_query_data)
                connection.commit()
        except (Exception, psycopg2.Error) as error:
            print(error)


def select_from_db(connection, cursor, table, keys=''):
    """ SELECT FROM Postgres database """

    if connection:
        try:
            if keys != '':
                postgres_query_data = f"""
                SELECT {keys} FROM {table};
                """
            else:
                postgres_query_data = f"""
                SELECT * FROM {table};
                """
            cursor.execute(postgres_query_data)
            records = cursor.fetchall()

            return records

        except (Exception, psycopg2.Error) as error:
            print(error)


def print_selected_data(records, keys=''):
    max_len = check_max(records)

    number_of_rows = len(records)
    number_of_columns = len(records[0])

    for i in range(number_of_rows):
        for row in range(number_of_columns):
            if 'id' in keys or row == number_of_columns - 1:
                print(str(records[i][row]).rjust(max_len[row] + 2), end=' ')
            else:
                print(str(records[i][row]).ljust(max_len[row] + 2), end=' ')
        print()


def check_max(records):
    """ Check max length of each column """
    max_len = [0] * len(records[0])
    for i in range(len(records)):
        for j in range(len(records[0])):
            if max_len[j] < len(str(records[i][j])):
                max_len[j] = len(str(records[i][j]))
    return max_len


def print_menu():
    print("""
    [1]. Create table
    [2]. Insert data
    [3]. Select data
    [4]. Print data
    [5]. Disconnect PostgreSQL and Exit
    """)

