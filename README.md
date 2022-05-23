# **Transport map**

## Описание
__Transport map__ - это приложение формирующее базу данных, основываясь на данных, полученных с ["Портала открытых данных правительства Москвы"](https://data.mos.ru). Далее с помощью *algorithm* формируется новая база данных, где находятся оптимальные маршруты, соединяющие любые две пары остановок. Далее подключается *server*, где и происходит визуализация карты.
## Функционал 
Пользователю предоставляются два окна, куда он может вбивать назание остановок, между которыми ему требуется совершить свой путь. Если у пользоателя возникла проблема с названием остановок, то окна подскажут ему решение. Так же пользователь может свободно перемещаться по карте. 

При желании можно построить автобусные маршруты для любого другого города, при наличии даных. 

## Ограничения приложения 

К сожалению приложение не позволяет легко добавлять маршруты в базу данных, оно так же не предоставляет выбор маршрута, а сразу предлагает оптимальный. 

## Усановка и запуск

Для установки требуется набрать следующую команду в терминале: 

```python
 git clone git@github.com:Gugush284/transport_card.git  
``` 


Для работы парсера для скачивания данных требуются следующие библиотеки: 

+ ```requests```
+ ```json```
+ ```time```
+ ```math``` 
+ ```sqlite3```


Для того, чтоб запустить parser нужно: 
1. Запустить файл _parser_db.py_ (парсит данные с сайта, записывает их в базу данных)

Для того, чтоб запустить программу, исправляющую databse, нужно:
1. Запустить файл _edit_db.py_ (программа заменяет имена маршрутов и остановок на их id)
2. Запустить файл _edit_db1.py_ (программа корректирует столбец Route_Num, проверяя его данные на валидность)
3. Запустить файл _edit_db2.py_ (программа для вставки обратного пути цепочки остановок для некольцевого маршрута+возможной инверсии обозначений кольцевого маршрута)
4. Запустить файл _edit_db3.py_ (программа вставляет координаты остановки в координаты маршрута + вставляет обратные координаты для маршрута в обратную сторону)

Для работы алгоритма необходимо:
Либо переимееновать базу данных в _example.db_, либо в коде _alg.py_ и _read_db_ заменить упоминания файла _example.db_ при использовании библиотеки os на нужное Вам название 

Для корректной работы сервера необходимо установить следующие библиотеки: 

+ ```os```
+ ```flask``` 
+ ```flask_wtf``` 
+ ```sqlite```
+ ```folium```

1. Для того, чтобы запустить сервер, необходимо запустить _python_ скрипт run.py и перейти по [ссылке.](http://127.0.0.1:5000/) 
2. На открытой странице небходимо ввести названия первой и последней остановки, и нажать на кнопку _отправить_ чтобы получить маршрут. 
 3. Для того, чтобы вернуться на первоначальную страницу, необоходимо нажать на _back to map_. Шаблоны для URL страниц находятся в директории _app/templates_. 
4. _Search.html_ отвечает за первоначальную страницу, _login.html_ - за страницу с построеным маршрутом. 
5. Обработка URL запросов и построение маршрута производятся в файле _views.py_.
6. Cкрипт __init__.py инициализирует сервер и импортирует _views.py_ 
7. Для построения маршрута и карты со всеми остановками в скрипте _views.py_ создаются файлы _basic_map.html_ и _route_map.html_
