import sqlite3

def check_func(func):
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (sqlite3.OperationalError, sqlite3.IntegrityError):
            print(f"{func.__name__} returns an error, please try again with another value")
            return None

    return wrapper_func

class SQL:
    def __init__(self):
        self.conn = sqlite3.connect("baza.db")
        self.curs = self.conn.cursor()
        try:
            self.curs.execute("""CREATE TABLE main (user TEXT, password TEXT)""")
        except sqlite3.OperationalError:
            print("=#=#=main table already exists!=#=#=")

    @check_func
    def execute(self, query: str):
        self.curs.execute(query)
        self.conn.commit()

    @check_func
    def add_value(self, username, password):
        try:
            self.curs.execute("INSERT INTO main (user, password) VALUES (?,?)", (username, password))
            self.conn.commit()
        except Exception as e:
            print(e)

    @check_func
    def add_many(self, user_list: list):
        self.curs.executemany("INSERT INTO main (user, password) VALUES (?,?)", user_list)

    @check_func
    def check_table(self, table="main"):
        for row in self.curs.execute(f"SELECT * FROM {table}"):
            print(row)

    @check_func
    def caniuse(self):
        print(f"=#=#=You can use {self.__class__}=#=#=")


if __name__ == "__main__":
    print("You cannot run this python file!")
    exit()
