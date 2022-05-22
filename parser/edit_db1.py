import sqlite3
import math
#программа корректирует столбец Route_Num: вставляет туда валидные id маршрута + удаляет остановки, у которых на самом деле не оказалось маршрута из базы данных
con = sqlite3.connect('database.db')

def update_sqlite_table_stopsker(sid, Rout_Num):                    #функция обновления списка маршрутов остановок
    try:
        sql_update_query = """Update stopsker set Route_Num = ? where _id = ?"""
        data = (Rout_Num, sid)
        cur.execute(sql_update_query, data)
        con.commit()
        #print("Запись в stopsker успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def update_sqlite_table_routesker2(rid, cnss):                                      #функция обновления цепочки остановок маршрута 
    
    try:
        sql_update_query = """Update routesker set chain_stops = ? where _id = ?"""
        data = (cnss, rid)
        cur.execute(sql_update_query, data)
        con.commit()
        #print("Запись в routesker(chain_stops) успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def delete_record(sid):                                                     #функция удаления остановки
    try:
        sql_delete_query = """DELETE from stopsker where _id = ?"""
        data=[sid]
        cur.execute(sql_delete_query,data)
        con.commit()
        #print("Запись успешно удалена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        
#второй цикл фикса
with con:
    cur = con.cursor()    
    cur.execute("SELECT * FROM stopsker")
    stops = cur.fetchall()

    cur.execute("SELECT _id FROM stopsker")
    stops_id = cur.fetchall()
    sid_list = [x for t in stops_id for x in t]             #преобразование списка кортежей в список: запоминаем _id всех остановок
    #print(sid_list)
    
    cur.execute("SELECT * FROM routesker")
    routes = cur.fetchall()

    #занулим столбец Route_Num в stopsker:
    
    for stops in stops:
        update_sqlite_table_stopsker(stops[0],'')
    
    #заполним столбец Route_num:     
    
    for route in routes:                    #цикл по маршрутам
        rid=route[0]                    #запоминаем id маршрута
        chain_stops=route[2].split(" ") #берём цепочку остановок (только в одну сторону) из бд, преобразуя в список id остановок
        chain_stops.remove('')          #удаляем пустой символ
        for c_stop in chain_stops:          #цикл по остановкам в маршруте
            id_stop=int(c_stop)             #запоминаем id остановки
                                            #проверяем, существует ли такая остановка
            if id_stop in sid_list:         #если существует, то вставляем номер маршрута в Route_Num данной остановки
                sql_select_query="""select Route_Num from stopsker where _id = ?""" #вставка номера маршрута в прежний лист маршрутов
                cur.execute(sql_select_query,(id_stop,))                    #достаём текущий список маршрутов
                Route_num_cort=cur.fetchall()                               #текущий список маршрутов в виде кортежа
                Route_num_list=[x for t in Route_num_cort for x in t]       #получаем его в виде списка
                try: 
                    Route_num_list.remove('')                               #удаляем пустой элемент, если есть
                except ValueError:
                    k=0
                Route_num_list.append(rid)                                  #вставляем в массив маршрутов наш новый маршрут
                Route_num_str=''.join([(str(e)+' ') for e in Route_num_list]) #собираем массив обратно в строку
                Route_num_str=Route_num_str[:len(Route_num_str)-1]          #удаляем ненужный пробел в конце
                update_sqlite_table_stopsker(id_stop,Route_num_str)         #обновляем список маршрутов в базе данных для данной остановки
                continue
            
            else:              #если не существует, то удаляем эту остановку из chain_stops
                chain_stops.remove(c_stop)      #удалить остановку из списка остановок маршрута
                chain_stops_r=''.join([(e+" ") for e in chain_stops])   #собираем строку из массива
                update_sqlite_table_routesker2(rid,chain_stops_r)       #обновляем данные об остановках в маршруте в базе данных
    
    cur.execute("SELECT * FROM stopsker")
    stops = cur.fetchall()
    for stop in stops:                          #удаляем остановку с пустыми маршрутами
        stop_routes=stop[3]
        if len(stop_routes)==0:
            delete_record(stop[0])
            
    con.commit()
cur.close()
con.close()  