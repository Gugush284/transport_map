import sqlite3
import os

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

# Getting all stops in the database 
# with name, x, y and id
# Output is a list of class STOP
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

# Read optimal way in class STOP, way in coords
# and transfers in the way
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

    except Exception as e:
        print({e})
        sql_connection.close()
        exit()
    else:
        return way_cords, way, transfer

def TEST_PRINT_STOPS(stops, way, transfer, way_cords):
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

    print("\nWay in cords:")
    print(way_cords)


# Getting a connection to the database
def connection():
    try:
        # Getting the path to the db file
        path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'example_server.db'
        )
        # Connecting
        sqlite_connection = sqlite3.connect(path)

    except Exception as e:
        print({e})
        exit()
    else:
        return sqlite_connection

def main():
    try:
        sql_connection = connection()

        # stops is a list of class STOP elements
        # way is list of class STOP in route order
        # transfer is list of [class STOP, name of route]
        # way_cords is a list of [x, y] coords in way 
        way_cords, way, transfer = read_way("Dubki", "Beskudnikovo", sql_connection)
        stops = read_stops(sql_connection)

        TEST_PRINT_STOPS(stops, way, transfer, way_cords)
    finally:
        sql_connection.close()


if __name__ == "__main__":
    main()
    