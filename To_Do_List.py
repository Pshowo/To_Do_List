from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

# Created database "todo.db"
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_task():
    """
    Read current date and get from database all records with this date and display it.
    :return:
    """
    today_is = datetime.today().date()
    print("\nToday {} {}:".format(today_is.strftime('%d'), today_is.strftime('%b')))
    today_task = session.query(Table.task).filter(Table.deadline == today_is).all()
    if len(today_task) == 0:
        print("Nothing to do!")
    else:
        i = 1
        for task in today_task:
            print(f"{i}. {task[0]}")
            i += 1


def week_task():
    """
    Prints all tasks for 7 day from today
    :return:
    """
    today_is = datetime.today().date()
    for day in range(7):
        # today
        day_task = today_is + timedelta(days=day)
        day_name = day_task.weekday()

        if day_name == 0:
            day_name = "Monday"
        elif day_name == 1:
            day_name = "Tuesday"
        elif day_name == 2:
            day_name = "Wednesday"
        elif day_name == 3:
            day_name = "Thursday"
        elif day_name == 4:
            day_name = "Friday"
        elif day_name == 5:
            day_name = "Saturday"
        elif day_name == 6:
            day_name = "Sunday"

        print('{} {} {}:'.format(day_name, day_task.strftime('%d'), day_task.strftime('%b')))
        day_task = session.query(Table.task).filter(Table.deadline == day_task).all()
        if day_task:
            i = 1
            for task in day_task:
                print(f"{i}. {task[0]}")
                i += 1
        else:
            print("Nothing to do!")
        print()

def add_task():
    """
    Add new task with date to database from the input
    :return:
    """
    print("Enter task")
    task_desc = input()
    print("Enter deadline")
    dead_line = input()
    dead_line = datetime.strptime(dead_line, '%Y-%m-%d')
    new_row = Table(
        task=task_desc,
        deadline=dead_line)
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")


def all_task(count):
    """
    Reads all tasks from database and printed them with deadline in command promt in the list form
    :param count: how many task to print
    :return:
    """
    if count == "all":
        all_rows = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
        if len(all_rows) == 0:
            print("Nothing to do!")
        else:
            print("All tasks:")
            i = 1
            for taks in all_rows:
                print(f"{i}. {taks[0]}. {taks[1].strftime('%d').replace('0','')} {taks[1].strftime('%b')}")
                i += 1
    else:
        count = int(count)
        pass
    print()


def main_menu():
    """
    Main menu
    :return:
    """
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Add task")
    print("0) Exit")
    choose = input()
    print()
    if choose == "1":
        today_task()
    elif choose == '2':
        week_task()
    elif choose == '3':
        all_task("all")
    elif choose == '4':
        add_task()
    elif choose == '0':
        exit()

# =====
while True:
    main_menu()
