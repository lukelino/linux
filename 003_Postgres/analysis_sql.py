#! /usr/local/bin/python3
import functions


def main():
    conn, cur = functions.connect()
    status = True
    functions.print_menu()
    while status:
        choice = int(input('Choice: '))
        if choice == 1:
            functions.create_table(conn, cur, 'teachers')
        elif choice == 2:
            functions.insert_data(conn, cur, 'teachers')
        elif choice == 3:
            keys = input('SELECT BY: ')
            records = functions.select_from_db(conn, cur, 'teachers', keys)
            functions.print_selected_data(records, keys)
        elif choice == 4:
            records = functions.select_from_db(conn, cur, 'teachers')
            functions.print_selected_data(records)
        elif choice == 5:
            functions.disconnect(conn, cur)
            break
        functions.print_menu()


if __name__ == '__main__':
    main()
