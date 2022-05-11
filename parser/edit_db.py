import sqlite3
import math

con = sqlite3.connect('database.db')

def is_number(s):                           #функция определения является ли строка числом
    try:
        float(s)
        return 1
    except ValueError:
        return 0

def sql_insert_Num_stop(values_s):             #функция вставки в таблицу остановок номера маршрута
    cur.execute('INSERT INTO stopsker (Name_stop, Cords, Route_Num) VALUES(?, ?, ?)', values_s)

def sql_insert_stop(values_s):             #функция вставки в таблицу остановки
    cur.execute('INSERT INTO stopsker (Name_stop, Cords, Route_Num) VALUES(?, ?, ?)', values_s)

def update_sqlite_table_stopsker(sid, Rout_Num):                    #функция обновления списка маршрутов остановок
    
    try:
        sql_update_query = """Update stopsker set Route_Num = ? where _id = ?"""
        data = (Rout_Num, sid)
        cur.execute(sql_update_query, data)
       # sqlite_connection.commit()
        #print("Запись в stopsker успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def update_sqlite_table_routesker(rid, cncs):                           #функция обновления цепочки координат маршрута 
    
    try:
        sql_update_query = """Update routesker set chain_cords = ? where _id = ?"""
        data = (cncs, rid)
        cur.execute(sql_update_query, data)
       # sqlite_connection.commit()
        #print("Запись в routesker(chain_cords) успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def update_sqlite_table_routesker2(rid, cnss):                                      #функция обновления цепочки остановок маршрута 
    
    try:
        sql_update_query = """Update routesker set chain_stops = ? where _id = ?"""
        data = (cnss, rid)
        cur.execute(sql_update_query, data)
       # sqlite_connection.commit()
        #print("Запись в routesker(chain_stops) успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def delete_record(sid):                                                     #функция удаления остановки
    try:
        sql_delete_query = """DELETE from stopsker where _id = ?"""
        data=[sid]
        cur.execute(sql_delete_query,data)
        #sqlite_connection.commit()
        #print("Запись успешно удалена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def delete_record2(rid):                                                #функция удаления маршрута
    try:
        sql_delete_query = """DELETE from routesker where _id = ?"""
        data=[rid]
        cur.execute(sql_delete_query,data)
        #sqlite_connection.commit()
        #print("Запись успешно удалена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        
with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM stopsker")
    stops = cur.fetchall()
    delets=0
    delets2=0
    j=0   
    
    cur.execute("SELECT * FROM routesker")                              #Цикл для удаления цифр в цепочке остановок маршрута
    routes = cur.fetchall()
    for route in routes:
        id_r=route[0]
        chain_stops_r=route[2]
        
        chain_stops_r_mas=chain_stops_r.split(" - ")

        msp=[]
        for element in chain_stops_r_mas:
            dig=is_number(element)
            if dig==0:
                msp.append(element)
        
        #print(msp)
        chain_stops_r_mas=msp     
        chain_stops_r=''.join([(e+" - ") for e in chain_stops_r_mas])
        update_sqlite_table_routesker2(id_r,chain_stops_r)
    
    
    
    for stop in stops:
        id_s=stop[0]
        name_s=stop[1]
        cords_s=stop[2]
        routes_s=stop[3]      
        f2=0
        
        split=routes_s.split(" ")
        routes_s=routes_s+' '
        
        for Route_Num in split:
            
            f1=0
            cur.execute("SELECT * FROM routesker")
            routes = cur.fetchall()
            
            for route in routes:
                id_r=route[0]
                name_r=route[1]
                chain_stops_r=route[2]
                chain_cords_r=route[3]
                
                if (name_r==Route_Num):
                    f1=1
                    break
                    
            if (f1==0):                                             #если маршрут не нашёлся в таблице маршрутов, то стереть его из маршрутов остановки в таблице остановок
                routes_s=routes_s.replace((Route_Num+" "),"",1)
                #print("инвалидный трек, новый лист маршрутов: "+routes_s)
                update_sqlite_table_stopsker(id_s, routes_s)
                
            if (f1==1):
                chain_stops_r_spl=chain_stops_r.split(" - ")
                if name_s in chain_stops_r_spl:
                    f2=1
                else:
                    f2=0
                
                if f2==1:
                    chain_cords_r=chain_cords_r+cords_s+"\n"                #вставляем координаты станции в координаты маршрута
                    update_sqlite_table_routesker(id_r,chain_cords_r)
                    
                    routes_s=routes_s.replace(Route_Num,str(id_r),1)        #меняем маршрут-номер на id в Route_Num
                    update_sqlite_table_stopsker(id_s, routes_s)
                    
                    chain_stops_r=chain_stops_r.replace(name_s,str(id_s),1) #меняем имя остановки в chain_stops на id
                    update_sqlite_table_routesker2(id_r,chain_stops_r)
                
                if f2==0:
                    routes_s=routes_s.replace((Route_Num+" "),"",1)
                    #print("инвалидный трек, новый лист маршрутов: "+routes_s)
                    update_sqlite_table_stopsker(id_s, routes_s)
            
            sp=routes_s.split(" ")
            
            if len(sp)==1:
                delets=delets+1
                delete_record(id_s)
    
        print("Прогресс: ",round(j/len(stops)*100,2),"%")
        j+=1
        
    cur.execute("SELECT * FROM routesker")                      #цикл для удаления оставшихся не подтверждённых остановок из цепочки остановок
    routes = cur.fetchall()
    for route in routes:
        id_r=route[0]
        chain_stops_r=route[2]
        
        chain_stops_r_mas=chain_stops_r.split(" - ")

        msp=[]
        for element in chain_stops_r_mas:
            dig=is_number(element)
            if dig==1:
                msp.append(element)
        chain_stops_r_mas=msp     
           
        chain_stops_r=''.join([(e+" ") for e in chain_stops_r_mas])
        update_sqlite_table_routesker2(id_r,chain_stops_r)
    
    
    
    cur.execute("SELECT * FROM routesker")                      #цикл для удаления "пустых" маршрутов
    routes = cur.fetchall()
    for route in routes:
        id_r=route[0]
        chain_stops_r=route[2]
        if len(chain_stops_r)==0:
            delets2=delets2+1
            delete_record2(id_r)

    print('\n')
    print("Количество удалённых остановок: ",delets)
    print("Количество удалённых маршрутов: ",delets2)
    con.commit()
