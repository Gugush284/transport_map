import sqlite3
import math
#программа для вставки обратного пути цепочки остановок для некольцевого маршрута+возможной инверсии обозначений кольцевого маршрута
con = sqlite3.connect('database.db')

def update_sqlite_table_routesker2(rid, cnss):                                      #функция обновления цепочки остановок маршрута 
    
    try:
        sql_update_query = """Update routesker set chain_stops = ? where _id = ?"""
        data = (cnss, rid)
        cur.execute(sql_update_query, data)
        con.commit()
        #print("Запись в routesker(chain_stops) успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def update_sqlite_table_routesker3(rid, cnss):                                      #функция обновления кольцевого маршрута (инверсии) 
    
    try:
        sql_update_query = """Update routesker set Ring = ? where _id = ?"""
        data = (cnss, rid)
        cur.execute(sql_update_query, data)
        con.commit()
        #print("Запись в routesker(chain_stops) успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

with con:                                       #вставляем цепочку обратного маршрута для некольцевых путей
    cur = con.cursor()    
    cur.execute("SELECT * FROM routesker")
    routes = cur.fetchall()
    
    for route in routes:
        rid=route[0]                            #запоминаем id маршрута
        if route[4]==1:              
            chain_stops=route[2].split(" ")     #получаем цепочку остановок
            chain_stops.remove('')              #удаляем последний элемент
            chain_stops_adds=chain_stops[::-1]  #создаём массив в обратном порядке
            chain_stops_adds.pop(0)             #удаляем первый элемент
            chain_stops=chain_stops+chain_stops_adds    #соединяем два массива
            chain_stops_r=''.join([(e+" ") for e in chain_stops])   #собираем строку
            update_sqlite_table_routesker2(rid,chain_stops_r)   #обновляем цепочку остановок для некольцевого маршрута
            
            update_sqlite_table_routesker3(rid,0) #опционально, если база данных инвёрснута: меняем обозначение некольцевого маршрута с 1 на 0 
        else: 
            update_sqlite_table_routesker3(rid,1) #опционально, если база данных инвёрснута: меняем обозначение кольцевого маршрута с 0 на 1

    con.commit()
cur.close()
con.close()  