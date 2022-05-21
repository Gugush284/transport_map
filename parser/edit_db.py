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
        con.commit()
        #print("Запись в stopsker успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def update_sqlite_table_routesker(rid, cncs):                           #функция обновления цепочки координат маршрута 
    
    try:
        sql_update_query = """Update routesker set chain_cords = ? where _id = ?"""
        data = (cncs, rid)
        cur.execute(sql_update_query, data)
        con.commit()
        #print("Запись в routesker(chain_cords) успешно обновлена")
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

def delete_record2(rid):                                                #функция удаления маршрута
    try:
        sql_delete_query = """DELETE from routesker where _id = ?"""
        data=[rid]
        cur.execute(sql_delete_query,data)
        con.commit()
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
    
    con.commit()
    cur.close()
   
        
with con:
    cur = con.cursor()    
    cur.execute("SELECT * FROM stopsker")
    stops = cur.fetchall()

    cur.execute("SELECT _id FROM stopsker")
    stops_id = cur.fetchall()
    sid_list = [x for t in stops_id for x in t]             #преобразование списка кортежей в список
    #print(sid_list)
    
    cur.execute("SELECT * FROM routesker")
    routes = cur.fetchall()

    #занулим столбец Route_Num в stopsker:
    
    for stops in stops:
        update_sqlite_table_stopsker(stops[0],'')
    
    #заполним столбец Route_num:     
    
    for route in routes:                    #цикл по маршрутам
        rid=route[0]
        chain_stops=route[2].split(" ")
        chain_stops.remove('')
        for c_stop in chain_stops:          #цикл по остановкам в маршруте
            id_stop=int(c_stop)
                                            #проверяем, существует ли такая остановка
            if id_stop in sid_list:         #если существует, то вставляем координаты остановки в chain_cords
                sql_select_query="""select Route_Num from stopsker where _id = ?""" #вставка номера маршрута в прежний лист маршрутов
                cur.execute(sql_select_query,(id_stop,))
                Route_num_cort=cur.fetchall()
                Route_num_list=[x for t in Route_num_cort for x in t]
                try: 
                    Route_num_list.remove('')
                except ValueError:
                    k=0
                Route_num_list.append(rid)
                Route_num_str=''.join([(str(e)+' ') for e in Route_num_list])
                Route_num_str=Route_num_str[:len(Route_num_str)-1]
                update_sqlite_table_stopsker(id_stop,Route_num_str)
                                                                                    #вставка координат в chain_cords
                sql_select_query="""select chain_cords from routesker where _id = ?"""
                cur.execute(sql_select_query,(rid,))
                chain_cords_cort=cur.fetchall()
                (chain_cords_str,)=chain_cords_cort[0]
                
                sql_select_query="""select Cords from stopsker where _id = ?"""
                cur.execute(sql_select_query,(id_stop,))
                stop_id_cort=cur.fetchall()
                (stop_id_str,)=stop_id_cort[0]
                
                chain_cords_str=chain_cords_str+stop_id_str+"\n"
                update_sqlite_table_routesker(rid,chain_cords_str)
                continue
            
            else:              #если не существует, то удаляем эту остановку из chain_stops
                chain_stops.remove(c_stop)
                chain_stops_r=''.join([(e+" ") for e in chain_stops])
                update_sqlite_table_routesker2(rid,chain_stops_r)
    
    cur.execute("SELECT * FROM stopsker")
    stops = cur.fetchall()
    for stop in stops:                          #удаляем остановку с пустыми маршрутами
        stop_routes=stop[3]
        if len(stop_routes)==0:
            delete_record(stop[0])
        
with con:                                       #вставляем цепочку обратного маршрута для некольцевых путей
    cur = con.cursor()    
    cur.execute("SELECT * FROM routesker")
    routes = cur.fetchall()
    
    for route in routes:
        if route[4]==1:
            rid=route[0]                        #запоминаем id маршрута
            chain_stops=route[2].split(" ")     #получаем цепочку остановок
            chain_stops.remove('')              #удаляем последний элемент
            chain_stops_adds=chain_stops[::-1]  #создаём массив в обратном порядке
            chain_stops_adds.pop(0)             #удаляем первый элемент
            chain_stops=chain_stops+chain_stops_adds    #соединяем два массива
            chain_stops_r=''.join([(e+" ") for e in chain_stops])   #собираем строку
            update_sqlite_table_routesker2(rid,chain_stops_r)   #обновляем цепочку остановок для некольцевого маршрута
            
con.commit()
cur.close()
con.close()   

print('\n')
print("Количество удалённых остановок: ",delets)
print("Количество удалённых маршрутов: ",delets2)
    
