from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
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

def new_task():
    """
    Add new task to database from the input
    :return:
    """
    print("Enter task")
    task_desc = input()
    new_row = Table(
        task=task_desc)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def read_task(count):
    """
    Reads a tasks from database and printed them in command promt in the list form
    :param count: how many task to print
    :return:
    """
    if count == "all":
        all_rows = session.query(Table).all()
        if len(all_rows) == 0:
            print("Nothing to do!")
        else:
            print("Today:")
            i = 1
            for taks in all_rows:
                print(f"{i}. {taks}")
                i += 1
    else:
        count = int(count)
        pass

def main_menu():
    """
    Main menu
    :return:
    """
    print("""1) Today's tasks
2) Add task
0) Exit""")
    choose = input()
    if choose == '1':
        read_task("all")
    elif choose == '2':
        new_task()
    elif choose == '0':
        exit()

# =====
while True:
    main_menu()
