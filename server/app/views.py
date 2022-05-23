from flask import render_template, flash, redirect, request, Response
from flask.wrappers import Request
from app import app
import json
from wtforms import TextField, SubmitField, Form
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import sqlite3
import os
import folium
from folium.plugins import MarkerCluster

class SearchForm(FlaskForm):
    autocomp = TextField('First stop', id = 'city_autocomplete', validators = [DataRequired()])
    autocomp1 = TextField('Last stop', id = 'ity_autocomplete', validators = [DataRequired()])
    submit = SubmitField()


 # Class consists of info about current stop
class STOP:
    """
    Класс содержит в себе:
    id - id остановки
    name - имя остановки
    x - широта
    y - долгота
    """
    def __init__(self, id, name, x, y):
        self.id = id 
        self.name = name
        self.abscissa = x
        self.ordinate = y

    def get_id(self):
        """Возвращаем id"""
        return self.id

    def get_name(self):
        """Возвращаем имя"""
        return self.name

    def get_x(self):
        """Возвращаем широту"""
        return self.abscissa

    def get_y(self):
        """Возвращаем долготу"""
        return self.ordinate


def read_stops(sql_connection):
    """
    Getting all stops in the database
    with name, x, y and id
    Output is a list of class STOP
    """

    stops = list()

    try:
        cur = sql_connection.cursor()

        # Get all stop ids
        cur.execute("SELECT _id FROM stopsker")
        amount = cur.fetchall()

        # For each id read indo from data base to class stop
        for item in amount:
            cur.execute("SELECT Name_stop FROM stopsker WHERE _id = ?",
                [item[0]])

            name = str(cur.fetchone()[0])

            cur.execute("SELECT Cords FROM stopsker WHERE _id = ?", 
                [item[0]])

            coords = cur.fetchone()[0].split()

            stops.append(STOP(
                int(item[0]),
                name,
                float(coords[0]),
                float(coords[1])
                )
            )

    except Exception as exc:
        print({exc})
        sql_connection.close()
        exit()
        
    else:
        return stops


def read_way(stop1, stop2, sql_connection):
    """
    Read optimal way in class STOP, way in coords
    and transfers in the way
    """
    try:
        cur = sql_connection.cursor()
        # For two stops get optimal route between them

        # Get id of stop1
        cur.execute("SELECT _id FROM stopsker WHERE Name_stop = ?",
            [stop1])

        Input = cur.fetchone()

        # if we don't have stop1
        if Input is None:
            return [], [], []
        else:
            id1 = int(Input[0])

        # Get id of stop2
        cur.execute("SELECT _id FROM stopsker WHERE Name_stop = ?",
            [stop2])

        Input = cur.fetchone()

        # if we don't have stop2
        if Input is None:
            return [], [], []
        else:
            id2 = int(Input[0])

        # Get optimal way, way in coords and transfers in it  
        cur.execute("SELECT route, transfer, cords FROM way WHERE id1 = ? and id2 = ?",
        [id1, id2])
        Input = cur.fetchone()

        # if no way
        if Input is None:
            return [], [], []

        # Convert the received ids into the class STOP 
        # And filling in the list "way"
        way = list()
        for element in Input[0].split():
            cur.execute("SELECT Name_stop, Cords FROM stopsker WHERE _id = ?",
                [element])
            info = cur.fetchone()
            cords = info[1].split()
            way.append(STOP(
                element,
                info[0],
                float(cords[0]),
                float(cords[1])
            ))
            
        # Convert the received stop ids into the class STOP,
        # Convert the received route id into str "name route"
        # And filling in the list "transfer" by [class stop, name route]
        transfer = list()
        for elem in Input[1].split(";"):
            one_transfer = elem.split()
            
            cur.execute("SELECT Name_stop, Cords FROM stopsker WHERE _id = ?",
            [one_transfer[0]])
            info = cur.fetchone()
            cords = info[1].split()
            
            cur.execute("SELECT Name_route FROM routesker WHERE _id = ?",
            [one_transfer[1]])
            name_route = cur.fetchone()[0]
            
            transfer.append([
                STOP(
                    one_transfer[0],
                    info[0],
                    float(cords[0]),
                    float(cords[1])
                    ),
                name_route])

        # We get the coordinates as a string, clear 
        # from \n and \r, clear from spaces, 
        # converte the string to list of [x, y], 
        # where x and y are float
        way_cords = list()
        for item in (Input[2].split('\n')):
            way_cords.append(item.split())
        way_cords = [
            [float(item[0]), float(item[1])]
            for item in way_cords]

    except Exception as exc:
        print({exc})
        sql_connection.close()
        exit()
    else:
        return way_cords, way, transfer


def connection():
    """Getting a connection to the database"""
    try:
        # Getting the path to the db file
        path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'example_server.db'
        )
        # Connecting
        sqlite_connection = sqlite3.connect(path)

    except Exception as exc:
        print({exc})
        exit()
    else:
        return sqlite_connection

def change_color(color):
    if color == 'red':
        color = 'blue'
    elif color == 'blue':
        color = 'green'
    elif color == 'green':
        color = 'purple'
    elif color == 'purple':
        color = 'red'
    return color
#change color of route lines when transfer

map = folium.Map(location=[55.752004, 37.617734],
                min_zoom=8, 
                max_zoom=18, 
              zoom_start = 10,
              height='80%')

marker_cluster = MarkerCluster().add_to(map)

#creating map consisting
#of all bus stops

sql_connection = connection()
stops = read_stops(sql_connection)
sql_connection.close()

#getting stops coordinates from database

stopies = []
for stop in stops:
    stopies.append(stop.get_name())

#get list of station names for autocomplete

for stop in stops:
    folium.CircleMarker(location=[stop.ordinate, stop.abscissa], radius=9, popup = stop.get_name(), fill_color="red", color="gray", fill_opacity = 0.9).add_to(marker_cluster)

#fill map with station markers

map.save("app/templates/basic_map.html")

#save map into server templates

@app.route('/_autocomplete', methods=['GET'])
def autocomplete(): 
    return Response(json.dumps(stopies), mimetype='application/json')

#autocomplete handler

@app.route('/', methods=['GET', 'POST'])

#default URL page handler

def index():
    coord = []
    #coordinates of route
    bus1 = ''
    #name of first stop
    bus2 = ''
    #name of last stop
    form = SearchForm(request.form)
    if form.validate_on_submit():
        bus1 = form.autocomp.data
        bus2 = form.autocomp1.data

        #getting first and last stations from input form

        sql_connection = connection()
        way_cords, way, transfer = read_way(bus1, bus2, sql_connection)
        sql_connection.close()
        #getting route list and list of transfers
        #by reading from database
        #tranfer - class with coordinates of transfer 
        #stops and names of needed routes
        #way - class with coordinates and 
        #names of route stops
        #way_cords - list of coordinates of route points
        for ways in way:
            coord.append([ways.ordinate, ways.abscissa])

        #getting list of route coordinates into coord

        if len(coord)>0:
            
            #if route is builded
            
            map1 = folium.Map(location=[way[0].ordinate, way[0].abscissa],
                min_zoom=8, 
                max_zoom=18, 
              zoom_start = 15,
              height='80%')

            #creating map for bulding route

            i = 0

            #flag for highlighting boarding stop

            for ways in way:
                folium.CircleMarker(
                    location=[ways.ordinate, ways.abscissa],
                    popup = ways.name, fill_color="red", 
                    color="gray",
                    fill_opacity = 0.9
                ).add_to(map1)
            
            #putting route stops on the map

            for transfers in transfer:
                if i == 0:
                    folium.CircleMarker(
                        location=[transfers[0].ordinate,
                        transfers[0].abscissa],
                        popup = transfers[0].name + "\nlanding on: " + transfers[1],
                        fill_color="red", color="gray", fill_opacity = 0.9
                    ).add_to(map1)          
                    i = i + 1
                    #highlight first stop                
                else:                     
                    folium.CircleMarker(
                        location=[transfers[0].ordinate,
                        transfers[0].abscissa],
                        popup = transfers[0].name + "\ntransfer to: " + transfers[1],
                        fill_color="red",
                        color="gray",
                        fill_opacity = 0.9
                    ).add_to(map1)
                    
                    #highlight stops with transfer                      
            i = 1
            coords = []
            #creating list of points of route
            #line changes color on transfer stops
            color = 'red'
            #basic color of route lines
            for way_cord in way_cords:
                coords.append([way_cord[1], way_cord[0]])

                #building route through all
                #stops and turns
                if i < len(transfer):
                    #when still have stops with transfer
                    if (way_cord[1] == transfer[i][0].ordinate and way_cord[0] == transfer[i][0].abscissa):
                        #if point of routes is transfer stop
                        #changing color of route lines
                        i = i + 1
                        folium.PolyLine(coords, color=color).add_to(map1)
                        #draw lines on the map
                        color = change_color(color)
                        coords.clear()
                        coords.append([way_cord[1], way_cord[0]])
            folium.PolyLine(coords, color=change_color(color)).add_to(map1)
            coords.clear()
            map1.save("app/templates/route_map.html")

            #building map with route
            #and returning page with builded route
            return render_template("login.html", form=form)
            
    return render_template("search.html", form=form, message = "No such routes found")
    #if route in not builded
    #message is printed on
    #main URL page

@app.route('/login', methods=['GET', 'POST'])

#handler of page with stop route

def login():
    if request.method == 'POST':
    #return to main page
    #when button is pressed
        return render_template("search.html")
    return render_template("login.html")
