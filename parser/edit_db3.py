import sqlite3
import math
import numpy as np
#эта программа работает с координатами маршрута (Прогресс): она вычисляет наиближайшую к остановке и после неё вставляет координату остановки
#а так же отображает зеркально цепочку координат маршрута для некольцевого маршрута (Прогресс2)
con = sqlite3.connect('database.db')

def update_sqlite_table_routesker(rid, cncs):                           #функция обновления цепочки координат маршрута 
    
    try:
        sql_update_query = """Update routesker set chain_cords = ? where _id = ?"""
        data = (cncs, rid)
        cur.execute(sql_update_query, data)
        con.commit()
        #print("Запись в routesker(chain_cords) успешно обновлена")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)        
        
with con:
    cur = con.cursor() 
    cur.execute("SELECT * FROM routesker")
    routes = cur.fetchall()        
    cur.execute("SELECT * FROM stopsker")
    stops = cur.fetchall()
    j=0
    
    for stop in stops:                          #цикл по остановкам
        stop_cs=stop[2]                         #записываем координаты остановки
        chain_cord_sp=stop_cs.split(" ")        #записываем её в массив
        dann=(float(chain_cord_sp[0]),float(chain_cord_sp[1]))      #данная координата в кортеже
        
        stop_routes_str=stop[3]                 #достаём маршруты остановки
        stop_routes=stop_routes_str.split(" ")  #записываем их в массив
        
        #i=0
        for route in stop_routes:               #бежим по массиву маршрутов
            rid=int(route)                      #записываем id маршрута
            sql_select_query="""select chain_cords from routesker where _id = ?"""
            cur.execute(sql_select_query,(rid,))    #достаём из бд цепочку координат маршрута
            chain_cords_cort=cur.fetchall()         #получаем в виде кортежа цепочку координат маршрута
            (chain_cords_str,)=chain_cords_cort[0]  #преобразовываем в строку кортеж
            
            chain_cords_list=chain_cords_str.split("\n")    #делаем из цепочки координат массив кортежей
            chain_cords_list.remove('')                     #удаляем пустой символ
            
            lst_cords=[]                                                #формируем список координат, в которых будет поиск
            for chain_cord in chain_cords_list:                         #цикл по кортежам в массиве
                chain_cord_sp=chain_cord.split(" ")                     #каждую координату делим на два числа
                lst_cords.append((float(chain_cord_sp[0]),float(chain_cord_sp[1]))) #вставляем в массив для работы в виде: (x,y)
            
            A=np.array(lst_cords)   #создаём рабочий массив типа np.array
            s_point = np.array(dann) #аналогично для заданной координаты остановки
            
            distances = np.linalg.norm(A-s_point, axis=1)   #вычисляем наименьшее расстояние
            min_index = np.argmin(distances)                #вычисляем индекс точки, дающей наименьшее расстояние
            #print(f"the closest point is {A[min_index]}, the point was {s_point}, at a distance of {distances[min_index]}")
            #print(rid)
            lst_cords[min_index]=dann              #вставляем координаты остановки на следующую после наиближайшей
            #print(lst_cords)
            #print(min_index)
            m=''                                    #собираем из массива обратно строку
            for crod in lst_cords:                  #цикл по координатам
                m=m+''.join([(str(e)+" ") for e in crod])+"\n"  #каждое число вставляем в виде строки
    
            update_sqlite_table_routesker(rid,m)    #вставляем в базу данных
            
            #print("Прогресс в маршрутах: ",round(i/len(stop_routes)*100,2),"%" )
            #i=i+1
        print("Прогресс: ",round(j/5245*100,2),"%" )
        j=j+1
    
    
    j=0
    cur.execute("SELECT * FROM routesker")
    routes = cur.fetchall()
    for route in routes:
        rid=route[0]
        ring=route[4]
        if ring==0:
            sql_select_query="""select chain_cords from routesker where _id = ?"""
            cur.execute(sql_select_query,(rid,))    #достаём из бд цепочку координат маршрута
            chain_cords_cort2=cur.fetchall()        #получаем в виде кортежа цепочку координат маршрута
            (chain_cords_str2,)=chain_cords_cort2[0] #преобразовываем в строку кортеж
            
            
            lst_cords2=chain_cords_str2.split("\n")  #делаем из цепочки координат массив кортежей
            lst_cords2.remove('')                    #удаляем пустой символ
            
            lst_cords_adds=lst_cords2[::-1]  #создаём массив в обратном порядке
            lst_cords_adds.pop(0)             #удаляем первый элемент
            
            lst_cords2=lst_cords2+lst_cords_adds  #соединяем новую цепочку маршрута из прямого и обратного путей
            
            m=''
            m=''.join([(str(e)+"\n") for e in lst_cords2])   #собираем это обратно в строку
            update_sqlite_table_routesker(rid,m)            #обновляем данные в базе данных
        print("Прогресс2: ",round(j/len(routes)*100,2),"%" )
        j=j+1   
    
    con.commit()
cur.close()
con.close()  