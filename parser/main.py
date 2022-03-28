import requests
import json

npage=0

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
}

def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("index.html","w", encoding="utf-8") as file:
        file.write(response.text)

def get_json(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("result.json","w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)

def collect_numpage():
    s = requests.Session()
    response = s.get(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1", headers=headers)
    data=response.json()
    npage = data.get("Count")
    print(npage)
    return npage
    
def collect_data(npage):
    s = requests.Session()
    response = s.get(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1", headers=headers)
    
    if response.status_code != 200:
        print("error")
        return 0
    else:
        print("")
    
    
    data=response.json()
    
    #print("f")
    
    pag_count = data.get("Result")[9].get("Number")
    if (pag_count%10 == 0):
        pag_count=pag_count//10
    else:
        pag_count=pag_count%10 
    print(pag_count)
    #print("f")
    #result_data []
    with open("namesofstops","w", encoding="utf-8") as stops:
        
        #print(npage)
        for i in range(1, npage):
            url=f"https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber={i}"
            
            try:
                r=s.get(url=url,headers=headers)
                print("\nget_ok")
            
            finally:
               while (r.status_code!=200):      
                                                                
                    if r.status_code != 200:
                        print("get_error")
                        print("")
                    else:
                        print("er_get_ok \n")
            
            print(url)
            

            data = r.json()
        
            names=data.get("Result")
        
            for name in names:
                value=name.get("Cells").get("Name")
                #print(value)
                stops.write(value)
                stops.write('\n')
            print("Прогресс завершен на:", round(100/npage*(i),1))
def main():
    #get_page(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1")
    #get_json(url="https://data.mos.ru/api/rows/getresultwithcount?datasetId=752&search=&sortField=Number&sortOrder=ASC&versionNumber=7&releaseNumber=335&pageNumber=1")
    npage=collect_numpage()
    collect_data(npage)
    
if __name__ == "__main__":
    main()