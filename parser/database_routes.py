import sqlite3

try:
    sqlite_connection = sqlite3.connect('sqlite_db.db')
    sqlite_create_table_query = '''CREATE TABLE routesker (
                                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name_route TEXT NOT NULL,
                                chain_stops TEXT NOT NULL,
                                chain_cords TEXT NOT NULL);'''

    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица SQLite создана")
    
    sqlite_create_table_query = '''CREATE TABLE stopsker (
                                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name_stop TEXT NOT NULL,
                                longtude REAL NOT NULL,
                                latitude REAL NOT NULL,
                                Route_Num text NOT NULL);'''
    
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица2 SQLite создана")
    
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
 
con = sqlite3.connect('sqlite_db.db')
 
def sql_insert(con, entities):
 
    cursorObj = con.cursor()        #вне цикла
    
    cursorObj.execute('INSERT INTO routesker (Name_route, chain_stops, chain_cords) VALUES(?, ?, ?)', entities)
    
    con.commit()          #вне цикла
 
entities = ("Kringe", "Kringe", "Kringe")
 
sql_insert(con, entities)