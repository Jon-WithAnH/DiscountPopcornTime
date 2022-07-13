from CustomDatatypes.butt import butt
import mysql.connector

class SQLScripts:

    def __init__(self) -> None:
        self.mycursor = None

    # def build2(self):
    #     mydb = mysql.connector.connect(
    #       host="localhost",
    #       user="yourusername",
    #       password="yourpassword"
    #     )

    def build(self) -> None:
        mydb = mysql.connector.connect(
              host="127.0.0.1",
              user="root",
              password="admin",
              database="favorites"
            )

        self.mycursor = mydb.cursor()
        self.mycursor.execute("SHOW TABLES")

    def check_if_exists(self):
        self.mycursor.execute("SHOW TABLES")

    def method1(self):
        print("test")

# tt = butt()

if __name__ == '__main__':
    test = SQLScripts()
    test.build()
    # test.check_if_exists()