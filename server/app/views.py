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
    autocomp = TextField('Station 1', id = 'city_autocomplete', validators = [DataRequired()])
    autocomp1 = TextField('Station 2', id = 'ity_autocomplete', validators = [DataRequired()])
    submit = SubmitField()


 # Class consists of info about current stop
class STOP:
    def __init__(self, ID, name, x, y):
        self.id = ID 
        self.name = name
        self.abscissa = x
        self.ordinate = y

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_x(self):
        return self.abscissa

    def get_y(self):
        return self.ordinate

def read_stops(sql_connection):
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

    except Exception as e:
        print({e})
        sql_connection.close()
        exit()
        
    else:
        return stops


def read_way(stop1, stop2, sql_connection):
    try:
        cur = sql_connection.cursor()
        # For two stops get optimal route between them

        # Get id of stop1
        cur.execute("SELECT _id FROM stopsker WHERE Name_stop = ?",
            [stop1])

        Input = cur.fetchone()

        # if we don't have stop1
        if Input is None:
            return [], []
        else:
            id1 = int(Input[0])

        # Get id of stop2
        cur.execute("SELECT _id FROM stopsker WHERE Name_stop = ?",
            [stop2])

        Input = cur.fetchone()

        # if we don't have stop2
        if Input is None:
            return [], []
        else:
            id2 = int(Input[0])

        # Get optimal way and transfers in it  
        cur.execute("SELECT route, transfer FROM way WHERE id1 = ? and id2 = ?",
        [id1, id2])
        Input = cur.fetchone()

        # if no way 
        if Input is None:
            return [], []

        # way_str consists of names
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

    except Exception as e:
        print({e})
        sql_connection.close()
        exit()
    else:
        return way, transfer

def TEST_PRINT_STOPS(stops, way, transfer):
    print("\nOptimal way:")
    for element in way:
        print(
            "   {} {} {}".format(
                element.get_name(),
                element.get_x(),
                element.get_y()
        ))

    print("\nTransfer:")
    for elem in transfer:
        print("Name of stop: {}, x: {}, y: {}, to route: {}".format(
            elem[0].get_name(),
            elem[0].get_x(),
            elem[0].get_y(),
            elem[1]
        ))

    print("\nStops")
    for stop in stops:
        print("{}) {} - {} {}".format(stop.get_id(),
        stop.get_name(), stop.get_x(), stop.get_y()))

def connection():
    try:
        path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'example_server.db'
        )
        sqlite_connection = sqlite3.connect(path)

    except Exception as e:
        print({e})
        exit()
    else:
        return sqlite_connection
print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


map = folium.Map(location=[55.752004, 37.617734],
                min_zoom=8, 
                max_zoom=18, 
              zoom_start = 10,
              height='80%')

marker_cluster = MarkerCluster().add_to(map)

# map creating
coord = []
# координаты маршрута

sql_connection = connection()
stops = read_stops(sql_connection)
cities = []
for stop in stops:
    cities.append(stop.get_name())
print(cities)
sql_connection.close()



for stop in stops:
    print(stop.abscissa)
    print(stop.ordinate)
    folium.CircleMarker(location=[stop.ordinate, stop.abscissa], radius=9, popup = stop.name, fill_color="red", color="gray", fill_opacity = 0.9).add_to(marker_cluster)
map.save("app/templates/mapa.html")
# map fill
@app.route('/_autocomplete', methods=['GET'])
def autocomplete(): 
    return Response(json.dumps(cities), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    bus1 = ''
    bus2 = ''
    form = SearchForm(request.form)
    if form.validate_on_submit():
        bus1 = form.autocomp.data
        bus2 = form.autocomp1.data
        print(bus1)
        print(bus2)
        sql_connection = connection()
        way, transfer = read_way(bus1, bus2, sql_connection)
        coord.clear()
        # coord - координаты остановок маршрута
        for ways in way:
            print(ways.name, ' ', ways.abscissa, ' ', ways.ordinate)
            coord.append([ways.ordinate, ways.abscissa])
        for transfers in transfer:
            print(transfers[0].name, transfers[0].abscissa, transfers[0].ordinate, transfers[1])
        sql_connection.close()
        map1 = map
        if len(coord)>0:
            folium.PolyLine(coord, color="red").add_to(map1)
        map1.save("app/templates/mapa.html")
        return render_template("search.html", form=form)
    return render_template("search.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")
