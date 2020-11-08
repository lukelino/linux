#! /usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from datetime import timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, nullable=False)

    def __repr__(self):
        return self.task


def menu():
    print(f'1) Today\'s tasks\n'
          f'2) Week\'s tasks\n'
          f'3) All tasks\n'
          f'4) Missed tasks\n'
          f'5) Add task\n'
          f'6) Delete task\n'
          f'0) Exit')


def show_tasks(session, param=None, period='Nothing is missed!'):
    today = datetime.today()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if param == 'all_tasks':
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            print('\nAll tasks:')
            for i, task in enumerate(rows):
                print(f'{i + 1}. {task.task}. {task.deadline.day} {task.deadline.strftime("%b")}')
            print('')
        else:
            print(f'{period}\n')

    elif param == 'today_tasks':
        print(f'\nToday {today.day} {today.strftime("%b")}:')
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if rows:
            for task in rows:
                print(f'{task.id}. {task.task}')
        else:
            print(f'{period}\n')

    elif param == 'week_tasks':
        print('')
        for i in range(7):
            day_number = today + timedelta(days=i)
            week_day_number = day_number.weekday()
            day_name = day_names[week_day_number]
            print(f'{day_name} {day_number.day} {day_number.strftime("%b")}:')
            rows = session.query(Table).filter(Table.deadline == day_number.date()).all()
            if rows:
                for task in rows:
                    print(f'{task.id}. {task.task}')
                print('')
            else:
                print(f'{period}\n')


def add_task(session):
    new_task = input('Enter task:\n')
    new_deadline = input('Enter deadline\n')
    new_deadline = datetime.strptime(new_deadline, '%Y-%m-%d')
    new_row = Table(task=new_task, deadline=new_deadline.date())
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')


def missed_tasks(session):
    print('\nMissed tasks:')
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    if rows:
        for i, task in enumerate(rows):
            print(f'{i + 1}. {task.task}. {task.deadline.day} {task.deadline.strftime("%b")}')
        print('')
    else:
        print('Nothing is missed!\n')


def delete_task(session):
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        print('\nChoose the number of the task you want to delete:')
        for i, task in enumerate(rows):
            print(f'{i + 1}. {task.id} {task.task}. {task.deadline.day} {task.deadline.strftime("%b")}')
        to_delete = int(input())
        session.delete(rows[to_delete - 1])
        session.commit()
        print('The task has been deleted!')
        print('')
    else:
        print('Nothing to delete\n')


def main():
    Base.metadata.create_all(engine)  # creates a table in our database
    session_maker = sessionmaker(bind=engine)  # creates a session to access
    session = session_maker()  # creates an object to manage db

    menu()
    while (choice := input()) != '0':
        if choice == '1':
            show_tasks(session, 'today_tasks', 'Nothing to do!')
        elif choice == '2':
            show_tasks(session, 'week_tasks', 'Nothing to do!')
        elif choice == '3':
            show_tasks(session, 'all_tasks', 'Nothing to do!')
        elif choice == '4':
            missed_tasks(session)
        elif choice == '5':
            add_task(session)
        elif choice == '6':
            delete_task(session)
        menu()

    print('\nBye!')


if __name__ == '__main__':
    main()
