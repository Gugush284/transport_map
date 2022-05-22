import requests
import json
import time
from time import sleep
import math
import sqlite3

try:
    sqlite_connection = sqlite3.connect('database.db')                      #создаём бд, затем создаём в ней таблицу маршрутов с нужными нам полями
    sqlite_create_table_query = '''CREATE TABLE routesker (                
                                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name_route TEXT NOT NULL,
                                chain_stops TEXT NOT NULL,
                                chain_cords TEXT NOT NULL,
                                Ring INTEGER);'''
    
    cursor = sqlite_connection.cursor()             #создаём курсор
    cursor.execute(sqlite_create_table_query)       #заставляем его создать нужные нам таблицы
    sqlite_connection.commit()
    print("Таблица маршрутов создана SQLite создана")
                                         
    sqlite_create_table_query = '''CREATE TABLE stopsker (    
                                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name_stop TEXT NOT NULL,
                                Cords TEXT NOT NULL,
                                Route_Num text NOT NULL);'''
    
    cursor.execute(sqlite_create_table_query)       #заставляем его создать нужные нам таблицы
    sqlite_connection.commit()
    print("Таблица остановок создана SQLite создана")
    
    cursor.close()                                  #закрываем курсор

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()                   #закрываем подключение к sqlite
        print("Соединение с SQLite закрыто")

con = sqlite3.connect('database.db')                #снова подключаемся к sqlite для записи
cursorObj = con.cursor()                            #новый курсор

headers = {         #заголовки для работы с сайтом
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
}

def sql_insert_stop(values_s):             #функция вставки в таблицу остановки
    cursorObj.execute('INSERT INTO stopsker (Name_stop, Cords, Route_Num) VALUES(?, ?, ?)', values_s)

def sql_insert_route(values_r):            #функция вставки в таблицу маршрута
    cursorObj.execute('INSERT INTO routesker (Name_route, chain_stops, chain_cords, Ring) VALUES(?, ?, ?, ?)', values_r)

def collect_data_stops():                            #функция, скачивающая данные с базы данных остановок 
    s = requests.Session()                          #запускаем сессию, отправляем запрос
    
    i=1                                                 #переменная счета страниц 
    #for i in range(1,10):
    while True:                                        #цикл по страницам
                                                            #конструируем ссылку на нашу страницу:
        url=f"https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber={i}"
            
        try:                                            #пробуем получить код страницы
            r=s.get(url=url,headers=headers)
            print("\nget_ok")
            
        except 404:
            print("\nClient error")
            
        except 403:
            print("\nBan")
            break
                
        finally:                                        
            while (r.status_code!=200):                  #если не получилось получить корректно, то пробуем с перерывом в 10 секунд                    
                if r.status_code != 200:
                    print("got_error ", r.status_code)
                    print("\ntrying again in 10 sec...")
                    time.sleep(10)
                    r=s.get(url=url,headers=headers)
                else:
                    print("er_get_ok \n")
                        
        data = r.json()                                 #записываем полученные данные в формате json
        
        names=data["Result"]                        #получаем данные из структуры "Result"
            
        if len(names)==0:                           #если получаем пустые данные, то добрались до конца бд на сайте - закончить цикл
            print("Добрались до конца базы остановок!")
            break
        
        for name in names:                              #бежим по столбцам дата-таблицы
            cells = name["Cells"]
            values_s=(cells["StationName"],''.join([(str(e)+" ") for e in cells["geoData"]["coordinates"]]),cells["RouteNumbers"].replace("А","").replace(";",""))  #печатаем название остановки, координаты через пробел, номера маршрутов через неё
            sql_insert_stop(values_s) 
        print("Прогресс: ", round(100/1179*(i),2),"%")
        i=i+1
        
def collect_data_routes():                            #функция, скачивающая данные с базы данных маршрутов 
    s = requests.Session()                          #запускаем сессию, отправляем запрос
    
    i=1                                                 #переменная счета страниц 
    #for i in range(1,10):
    while True:                                        #цикл по страницам
                                                            #конструируем ссылку на нашу страницу:
        url=f"https://data.mos.ru/api/rows/getresultwithcount?datasetId=3221&search=&sortField=Number&sortOrder=ASC&versionNumber=1&releaseNumber=103&pageNumber={i}"
            
        try:                                            #пробуем получить код страницы
            r=s.get(url=url,headers=headers)
            print("\nget_ok")
            
        except 404:
            print("\nClient error")
            
        except 403:
            print("\nBan")
            break
                
        finally:                                        
            while (r.status_code!=200):                  #если не получилось получить корректно, то пробуем с перерывом в 10 секунд                    
                if r.status_code != 200:
                    print("got_error ", r.status_code)
                    print("\ntrying again in 10 sec...")
                    time.sleep(10)
                    r=s.get(url=url,headers=headers)
                else:
                    print("er_get_ok \n")
                        
        data = r.json()                                 #записываем полученные данные в формате json
        
        names=data["Result"]                        #получаем данные из структуры "Result"
            
        if len(names)==0:                           #если получаем пустые данные, то добрались до конца бд на сайте - закончить цикл
            print("Добрались до конца базы маршрутов!")
            break
        
        for name in names:                              #бежим по столбцам дата-таблицы
            cells = name["Cells"]
            
            try:                                        #проверяем кольцевой маршрут или нет
                z=cells["geoData"]["coordinates"][1]
                z=0
            except IndexError:
                #print("\n Кольцевой \n")
                z=1
            
            j=1
            m=''
            while True:                                 #цикл по координатам в цепочке для создания строчки координат через пробел
                try:                                    #пытаемся объединить две координаты в строчку и записать в строку
                    m=m+''.join([(str(e)+" ") for e in cells["geoData"]["coordinates"][0][j]])+"\n"
                    j=j+1
                except IndexError:                      #если вышли за пределы кол-ва координат, то выход
                    break
                       
            values_r=(cells["RouteNumber"],cells["TrackOfFollowing"],m,z)   #печатаем в базу данных номер маршрута, цепочку остановок, цепочку координат, кольцевой - не кольцевой
            sql_insert_route(values_r)
        print("Прогресс: ", round(100/93*(i),2),"%")
        i=i+1                                                                           #счетчик цикла страниц
    con.commit() 
        
def main():
    collect_data_stops()    #заполняем таблицу остановок
    collect_data_routes()   #заполняем таблицу маршрутов
    
if __name__ == "__main__":
    main()