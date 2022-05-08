import requests
import json
import time
from time import sleep
import math

headers = {         #заголовки для работы с сайтом
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
}

def collect_data():                            #функция, скачивающая данные с заданного количества страниц
    s = requests.Session()                          #запускаем сессию, отправляем запрос
    
    with open("database.txt","w", encoding="utf-8") as database:    #открываем запись в файл
        
        i=1                                                 #переменная счета страниц 
        while True:                                         #цикл по страницам
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
                print("Добрались до конца!")
                break
                
            for name in names:                              #бежим по столбцам дата-таблицы
                cells = name["Cells"]
                print(
                    cells["StationName"], #получает имя остановки
                    *cells["geoData"]["coordinates"], #получает координаты остановки
                    cells["RouteNumbers"],  #получает маршруты остановки
                    sep=";", file=database
                )
                
            print("Прогресс: ", round(100/1179*(i),2),"%")
            i=i+1
def main():
    collect_data()
    
if __name__ == "__main__":
    main()