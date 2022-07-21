import mysql.connector
from mysql.connector import errorcode


class SqlContextManager():
    """Context manager for the Sql Database
    """
    SUPPORTED_DB_TABLES_ALIAS = ['FAV', 'WL']
    SUPPORTED_DB_TABLES = ['favorites', 'watch_later']

    def __init__(self):
        self.mydb = mysql.connector.connect(
              host="127.0.0.1",
              user="root",
              password="admin",
              database="discountpopcorntime"
            )

        self.mycursor = self.mydb.cursor(buffered=True, dictionary=True)
        # print('init method called')

    def __enter__(self):
        # print('enter method called')
        return self
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        # print('exit method called')
        self.mycursor.close()        
        self.mydb.close()

    def initalize_tables(self):
        TABLES = {}

        TABLES['favorites'] = (
                "CREATE TABLE `favorites` ("
                "  `show_title` VARCHAR(255) NOT NULL,"
                "  `release_date` VARCHAR(20) NOT NULL,"
                "  `show_rating` VARCHAR(5) NULL,"
                "  `thumbnail` VARCHAR(255) NOT NULL,"
                "  `link` VARCHAR(255) NOT NULL,"
                "  PRIMARY KEY (`link`)"
                ") ENGINE=InnoDB")

        TABLES['watch_later'] = (
                "CREATE TABLE `watch_later` ("
                "  `show_title` VARCHAR(255) NOT NULL,"
                "  `release_date` VARCHAR(20) NOT NULL,"
                "  `show_rating` VARCHAR(5) NULL,"
                "  `thumbnail` VARCHAR(255) NOT NULL,"
                "  `link` VARCHAR(255) NOT NULL,"
                "  PRIMARY KEY (`link`)"
                ") ENGINE=InnoDB")

        TABLES['watch_history'] = (
                "CREATE TABLE `watch_history` ("
                "  `link` VARCHAR(255) NOT NULL,"
                "  PRIMARY KEY (`link`)"
                ") ENGINE=InnoDB")

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.mycursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
            # self.mycursor.execute("CREATE TABLE favorites (show_title VARCHAR(255), release_date VARCHAR(10), show_rating VARCHAR(5), thumbnail VARCHAR(255), link VARCHAR(255) UNIQUE)")

    def commit(self, table_name: str, data: list) -> bool:
        """Commit the new information into the DB

        Args:
            table_name (str): Table to be searched. Valid options are either "favorites" or "watch_later"
            data (list): list of len(5) the holds the information about the title

        Returns:
            bool: True on success
        """
        assert len(data) == 5, "Not enough data to populate table. List must have 5 indexes"
        # print(data)
        # Add entry to DB
        try:
            self.mycursor.execute("INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s');" % (table_name, data[0], data[1],data[2],data[3],data[4]))
            self.mydb.commit()
        except mysql.connector.errors.IntegrityError as err:
            print("Entry already exists")
            return False

    def delete(self, table_name: str, data: list):
        print(f"Deleteing from DB: {data}")
        self.mycursor.execute("DELETE FROM %s WHERE link='%s'" % (table_name, data[-1]))
        self.mydb.commit()


    def search_table(self, table_name: str, link: str) -> bool:
        """Searches the desired tables for any entry

        Args:
            table_name (str): Table to be searched. Valid options are either "favorites" or "watch_later"
            link (str): tmdbID. Ex "/tv/14658"

        Returns:
            bool: True if exists within the DB. False is not.
        """
        self.mycursor.execute("SELECT * FROM %s WHERE link='%s'" % (table_name, link[-1]))
        result = self.mycursor.fetchone()
        if result:
            return True
        return False


    def show_tables(self, table_name: str) -> list:
        """_summary_

        Args:
            table_name (str): Name of the desired table to have returned

        Returns:
            list: Every row and column in the given table
        """
        # Each key has the value in the order: [show_title, release_date, show_rating, thumbnail, link]
        query = ("SELECT * FROM %s" % table_name)
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

if __name__ == '__main__':
    with SqlContextManager() as manager:
        # print('with statement block')
        manager.initalize_tables()
        # test_1 = ['survivor', '1/24/2000', None, '/t/p/w94_and_h141_bestv2/5TVfHUnY84VAVur8FNllbkgnKmQ.jpg', '/tv/14658']
        # manager.add_favorite(test_1)
        # if manager.search_table('favorites', '/tv/14658'):
            # print(True)
        # manager.show_tables()