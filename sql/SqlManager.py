import mysql.connector
from mysql.connector import errorcode

class SqlContextManager():
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
                "  `release_date` VARCHAR(10) NOT NULL,"
                "  `show_rating` VARCHAR(5) NULL,"
                "  `thumbnail` VARCHAR(255) NOT NULL,"
                "  `link` VARCHAR(255) NOT NULL,"
                "  PRIMARY KEY (`link`)"
                ") ENGINE=InnoDB")

        TABLES['watch_later'] = (
                "CREATE TABLE `watch_later` ("
                "  `show_title` VARCHAR(255) NOT NULL,"
                "  `release_date` VARCHAR(10) NOT NULL,"
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

    def add_favorite(self, data: list) -> bool:
        """add the entry with the tmdb

        Args:
            tmdbID (str): TmdbID of the content. Expected format: /tv/71712
            address (str): _description_

        Returns:
            bool: True on success
        """
        assert len(data) == 5, "Not enough data to populate table. List must have 5 indexes"
        # check if tmdbID already exists. If so, remove it

        # Add entry to DB
        # self.mycursor.execute("INSERT INTO `discountpopcorntime`.`favorites` (`tmdbID`,`address`) VALUES ('%s', '%s');" % (tmdbID, address))
        try:
            self.mycursor.execute("INSERT INTO `discountpopcorntime`.`favorites` VALUES ('%s', '%s', '%s', '%s', '%s');" % (data[0], data[1],data[2],data[3],data[4]))
            self.mydb.commit()
        except mysql.connector.errors.IntegrityError as err:
            print("Entry already exists")
            # TODO: Toggle Entry
            return False
        # print(self.mycursor.execute("INSERT INTO `discountpopcorntime`.`favorites` (tmdbID, address) VALUES ('%s', '%s');" % (tmdbID, address)))
        # print(self.mycursor.execute("SELECT 'tmdbID' FROM 'discountpopcorntime'.'favorites';"))
        #INSERT INTO `discountpopcorntime`.`favorites`

    def search_table(self, table_name: str, link: str) -> bool:
        self.mycursor.execute("SELECT * FROM %s WHERE link='%s'" % (table_name, link))
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
 
with SqlContextManager() as manager:
    # print('with statement block')
    # manager.initalize_tables()
    test_1 = ['survivor', '1/24/2000', None, '/t/p/w94_and_h141_bestv2/5TVfHUnY84VAVur8FNllbkgnKmQ.jpg', '/tv/14658']
    # manager.add_favorite(test_1)
    if manager.search_table('favorites', '/tv/14658'):
        print(True)
    # manager.show_tables()