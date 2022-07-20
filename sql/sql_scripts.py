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
              database="discountpopcorntime"
            )

        self.mycursor = mydb.cursor(buffered=True, dictionary=True)
        # self.mycursor.execute("CREATE TABLE favorites (tmdbID VARCHAR(255), address VARCHAR(255))")
        # self.mycursor.execute("SHOW TABLES")
        # self.mycursor.execute("DROP TABLE favorites")

    def create_tables(self):
        self.mycursor.execute("CREATE TABLE favorites (tmdbID VARCHAR(255), address VARCHAR(255))")

    def check_if_exists(self):
        mydb = mysql.connector.connect(
              host="127.0.0.1",
              user="root",
              password="admin",
              database="discountpopcorntime"
            )
        self.mycursor = mydb.cursor(buffered=True, dictionary=True)
        test = self.mycursor.execute("SELECT `tmdbID` FROM `discountpopcorntime`.`favorites`;")
        print(test)

    def method1(self):
        print("test")

# tt = butt()

if __name__ == '__main__':
    test = SQLScripts()
    test.build()
    test.check_if_exists()