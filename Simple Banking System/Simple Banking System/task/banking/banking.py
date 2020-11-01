#! /usr/bin/python3.8

import random
import sys
import sqlite3


def connect():
    try:
        # f = r'/home/lukasz/Py/Simple Banking System/Simple Banking System/task/banking/'
        f_name = r'card.s3db'
        connection = sqlite3.connect(f_name)
        cursor = connection.cursor()
    except Exception as error:
        sys.exit(error)
    return connection, cursor


def disconnect(connection, cursor):
    if connection:
        connection.close()
        cursor.close()
    else:
        print('No connection!')


def create_table(connection, cursor, table):
    if connection:
        try:
            query_data = f"""
            CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
            );

            """
            cursor.execute(query_data)
            connection.commit()
        except Exception as error:
            sys.exit(error)


def drop_table(connection, cursor, table):
    if connection:
        try:
            cursor.execute(f'DROP TABLE IF EXISTS {table}')
            connection.commit()
        except Exception as error:
            print(error)


def luhn_algorithm(card_num):
    lst = [int(x) for x in card_num]
    digit = lst[-1]
    lst = lst[:-1]
    lst_second_stage = []
    i = 1
    while i < len(lst) + 1:
        if i % 2 == 0:
            lst_second_stage.append(lst[i - 1])
        else:
            lst_second_stage.append(lst[i - 1] * 2)
        i += 1
    lst_sub = []
    for x in lst_second_stage:
        if x <= 9:
            lst_sub.append(x)
        else:
            lst_sub.append(x - 9)
    sum_lst = sum(lst_sub)
    if (sum_lst + digit) % 10 == 0:
        return True
    else:
        return False


class Account:
    """Main account"""

    def __init__(self):
        self.balance = 0

    @classmethod
    def add_income(cls, connection, cursor, table, records):
        income = int(input('Enter income:\n'))
        income = int(records[2]) + income
        income = str(income)
        if update_balance(connection, cursor, table, income, records):
            print('Income was added!\n')

    @classmethod
    def do_transfer(cls, connection, cursor, table, records):
        print('\nTransfer')
        target_account = input('Enter card number:\n')
        if luhn_algorithm(target_account):
            result = get_data_from_db(connection, cursor, table, target_account)
            if not result:
                print('\nSuch a card does not exist.\n')
            elif target_account == records[0]:
                print("You can't transfer money to the same account!\n")
            else:
                to_be_transferred = int(input('\nEnter how much money you want to transfer:\n'))
                if to_be_transferred > int(records[2]):
                    print('Not enough money!\n')
                else:
                    total_be_transferred = to_be_transferred + int(result[1])
                    to_be_subtracted = int(records[2]) - to_be_transferred
                    update_balance(connection, cursor, table, to_be_subtracted, records)
                    if update_balance(connection, cursor, table, total_be_transferred, result):
                        print('Success!\n')
        else:
            print('Probably you made a mistake in the card number. Please try again!\n')


class Card(Account):
    """class Card"""

    ALL_CARDS = {}

    def __init__(self):
        super().__init__()
        self.beginning = 400000
        self.card_num = ''
        self.PIN = str(random.randint(0, 9999)).zfill(4)
        self.total_card_num = ''
        self.int_total_card_num = [int(x) for x in self.card_num]

    def get_card_num(self):
        return self.card_num

    def create_card_number(self):
        self.card_num = str(self.beginning) + str(random.randint(0, 9999999999)).zfill(10)
        while self.card_num in Card.ALL_CARDS.keys():
            self.card_num = str(self.beginning) + str(random.randint(0, 9999999999)).zfill(10)

    def pair_card_num_and_pin(self):
        Card.ALL_CARDS.setdefault(self.card_num, self.PIN)

    def insert_data(self, connection, cursor, table):
        if connection:
            try:
                query_data = f"""
                                INSERT INTO {table} (number, pin, balance)
                                VALUES ('{self.card_num}', '{self.PIN}', '{self.balance}');
                                """
                cursor.execute(query_data)
                connection.commit()
            except Exception as error:
                print(error)

    def print_card_data(self):
        print(f'\nYour card has been created\n'
              f'Your card number:\n{self.card_num}\n'
              f'Your card PIN:\n{self.PIN}\n')


def menu():
    print('1. Create an account\n'
          '2. Log into account\n'
          '0. Exit')


def logged_menu():
    print('1. Balance\n'
          '2. Add income\n'
          '3. Do transfer\n'
          '4. Close account\n'
          '5. Log out\n'
          '0. Exit')


def get_data_from_db(connection, cursor, table, card_num_input, your_pin=None):
    if connection:
        if your_pin is not None:
            query = f"""
                        SELECT number, pin, balance FROM {table} WHERE number={card_num_input} AND pin={your_pin};
                    """
        else:
            query = f"""
                        SELECT number, balance FROM {table} WHERE number={card_num_input};
                    """
        cursor.execute(query)
        return cursor.fetchone()


def update_balance(connection, cursor, table, income, records, i=0):
    if connection:
        try:
            query = f"""
                    UPDATE {table}
                    SET balance = {income} WHERE number={records[i]};
                    """
            cursor.execute(query)
            connection.commit()
            return True
        except Exception as error:
            print(error)


def close_account(connection, cursor, table, card_num_input):
    if connection:
        try:
            query = f"""
                    DELETE FROM {table} WHERE number={card_num_input};
                    """
            cursor.execute(query)
            connection.commit()
            print('\nThe account has been closed!\n')
        except Exception as error:
            print(error)


def log_in_to_account(connection, cursor, table):
    print('\nEnter your card number:')
    card_num_input = input()
    print('Enter your PIN:')
    your_pin = input()
    if connection:
        try:
            records = get_data_from_db(connection, cursor, table, card_num_input, your_pin)
            if not records:
                print('\nWrong card number or PIN!')
            else:
                print('\nYou have successfully logged in!\n')
                logged_menu()
                choose = input()
                while True:
                    if choose == '0':
                        print('\nBye!')
                        sys.exit()
                    elif choose == '1':
                        print(f'Balance: {records[2]}\n')
                    elif choose == '2':
                        Account.add_income(connection, cursor, table, records)
                    elif choose == '3':
                        Account.do_transfer(connection, cursor, table, records)
                    elif choose == '4':
                        close_account(connection, cursor, table, card_num_input)
                    elif choose == '5':
                        break
                    records = get_data_from_db(connection, cursor, table, card_num_input, your_pin)
                    logged_menu()
                    choose = input()
        except Exception as error:
            print(error)


def main():
    conn, cur = connect()
    create_table(conn, cur, 'card')
    person = []
    i = 0
    while True:
        menu()
        choose = input()
        if choose == '0':
            break
        elif choose == '1':
            tmp_person = Card()
            person.append(tmp_person)
            person[i].create_card_number()
            num = person[i].get_card_num()
            while luhn_algorithm(num) is False:
                person[i].create_card_number()
                num = person[i].get_card_num()
            create_table(conn, cur, 'card')
            person[i].insert_data(conn, cur, 'card')
            person[i].pair_card_num_and_pin()
            person[i].print_card_data()
            i += 1
        elif choose == '2':
            log_in_to_account(conn, cur, 'card')
    print('\nBye!')
    # disconnect(conn, cur)


if __name__ == '__main__':
    main()
