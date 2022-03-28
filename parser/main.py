import requests
import json

npage=0             #переменная для количества страниц

headers = {         #заголовки для работы с сайтом
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
}

def get_page(url):                                  #функция, получающая html-код страницы и записывающая его в файл
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("index.html","w", encoding="utf-8") as file:
        file.write(response.text)

def get_json(url):                                  #функция, получающая json-код страницы и записывающая его в файл
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("result.json","w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)

def collect_numpage():                              #функция, получающая кол-во страниц, которые нужно спарсить с сайта -> записывается в npage
    s = requests.Session()
    response = s.get(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1", headers=headers)
    data=response.json()
    npage = data.get("Count")
    print(npage)
    return npage
    
def collect_data(npage):
    s = requests.Session()                          #запускаем сессию, отправляем запрос
    """                                            #часть кода, которая получает счетчик страниц, исходя из текущей открытой, если вдруг понадобится
    response = s.get(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1", headers=headers)
        
    if response.status_code != 200:                 #если возникла проблема с получением ответа, то написать "error" и выйти
        print("error")
        return 0
    else:
        print("")
    
    
    data=response.json()                            #записываем 
    
    #print("f")
    
    pag_count = data.get("Result")[9].get("Number")
    if (pag_count%10 == 0):
        pag_count=pag_count//10
    else:
        pag_count=pag_count%10 
    print(pag_count)
    #print("f")
    """
    
    with open("database.txt","w", encoding="utf-8") as database:    #открываем запись в файл
        
        #print(npage)
        for i in range(1, npage+1):                             #цикл по страницам
                                                            #конструируем ссылку на нашу страницу:
            url=f"https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber={i}"
            
            try:                                            #пробуем получить код страницы
                r=s.get(url=url,headers=headers)
                print("\nget_ok")   
            
            finally:                                        
               while (r.status_code!=200):                  #если не получилось получить корректно, то пробуем до тех пор, пока не получится
                                                                
                    if r.status_code != 200:
                        print("get_error")
                        r=s.get(url=url,headers=headers)
                        print("trying again...")
                    else:
                        print("er_get_ok \n")
            
            #print(url)
            
            data = r.json()                                 #записываем полученные данные в формате json
        
            names=data.get("Result")                        #получаем данные из структуры "Result"
            
            for name in names:                              #бежим по столбцам дата-таблицы
                value1=name.get("Cells").get("StationName")   #получает имя остановки
                value2_0=name.get("Cells").get("geoData").get("coordinates")[0] #получает координаты остановки
                value2_1=name.get("Cells").get("geoData").get("coordinates")[1]
                value3=name.get("Cells").get("RouteNumbers")    #получает маршруты остановки
                seq=[f"{value1}",f"{value2_0}",f"{value2_1}",f"{value3}"]
                #print(seq)
                database.writelines(line + ' ' for line in seq)
                database.write('\n') 
            print("Прогресс: ", round(100/npage*(i),2),"%")
            
def main():
    #для получения html-кода:
    #get_page(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1")
    #для получения json-кода страницы:
    #get_json(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1")
    #для работы самого парсера:
    npage=collect_numpage()
    collect_data(npage)
    
if __name__ == "__main__":
    main()