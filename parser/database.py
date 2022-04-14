import sqlite3

try:
    sqlite_connection = sqlite3.connect('sqlite_db_busstops.db')
    sqlite_create_table_query = '''CREATE TABLE stopsker (
                                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name_stop TEXT NOT NULL,
                                longtude REAL NOT NULL,
                                latitude REAL NOT NULL,
                                Route_Num text NOT NULL);'''

    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица SQLite создана")

    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
 
con = sqlite3.connect('sqlite_db_busstops.db')
 
def sql_insert(con, entities):
 
    cursorObj = con.cursor()        #вне цикла
    
    cursorObj.execute('INSERT INTO stopsker (Name_stop, longtude, latitude, Route_Num) VALUES(?, ?, ?, ?)', entities)
    
    con.commit()          #вне цикла
 
entities = ("Kringe", 5.95, 4.25, "654L")
 
sql_insert(con, entities)