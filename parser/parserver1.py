# scraper.py
import requests
from bs4 import BeautifulSoup

url = 'https://data.mos.ru/opendata/752/data/table?versionNumber=7&releaseNumber=335'    #наш сайт
response = requests.get(url)        #получает код разметки
soup = BeautifulSoup(response.text, 'lxml')     #представляем html-разметку в виде текста в переменной soup
#quotes = soup.find_all('div', class_='row-link') # записываем в переменную quotes массив из элементов span с классом text
#authors = soup.find_all('small', class_='author') #ищем и записываем в переменную authos всех авторов
#tags = soup.find_all('div', class_='tags')  # -\\- для тэгов

#for i in range(0, len(quotes)):    
 #   print(quotes[i].text)           #печатает только текст цитаты из разметки html
    #print('--' + authors[i].text) #печатает только автора цитаты из разметки html
    #tagsforquote = tags[i].find_all('a', class_='tag')
    #for tagforquote in tagsforquote:
     #   print(tagforquote.text)
print(soup)     
    #print('\n')