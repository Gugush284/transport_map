import sqlite3
import os

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

def read_stops(sql_connection, cur):
    stops = list()

    try:
        command = "SELECT _id FROM stopsker"
        cur.execute(command)
        amount = cur.fetchall()

        for item in amount:
            command = "SELECT Name_stop FROM stopsker WHERE _id = "
            command += str(item[0])
            cur.execute(command)

            name = str(cur.fetchone()[0])

            command = "SELECT Cords FROM stopsker WHERE _id = "
            command += str(item[0])
            cur.execute(command)

            coords = cur.fetchone()[0].split()

            stops.append(STOP(int(item[0]), name, float(coords[0]),
                float(coords[1])))

    except Exception as e:
        print({e})
        sql_connection.close()
        exit()
        
    else:
        return stops

def read_optimal_route(stop1, stop2, sql, cur):
    try:
        command = "SELECT _id FROM stopsker WHERE Name_stop = '"
        command += str(stop1)
        command += "'"
        cur.execute(command)

        Input = cur.fetchone()

        if Input is None:
            return -1, [], [] 
        else:
            id1 = int(Input[0])

        command = "SELECT _id FROM stopsker WHERE Name_stop = '"
        command += str(stop2)
        command += "'"
        cur.execute(command)

        Input = cur.fetchone()

        if Input is None:
            return -2, [], [] 
        else:
            id2 = int(Input[0])

        command = "SELECT route, transfer FROM way WHERE id1 = "
        command += str(id1)
        command += " and id2 = "
        command += str(id2)
        cur.execute(command)
        Input = cur.fetchone()

        if Input is None:
            return -3, [], []

        way = [int(elem) for elem in Input[0].split()]

        way_str = list()
        for elem in way:
            command = "SELECT Name_stop FROM stopsker WHERE _id = "
            command += str(elem)
            cur.execute(command)
            way_str.append(cur.fetchone()[0])

        transfer = list()
        for elem in Input[1].split(";"):
            one_transfer = elem.split()
            
            command = "SELECT Name_stop FROM stopsker WHERE _id = "
            command += str(one_transfer[0])
            cur.execute(command)
            name_stop = cur.fetchone()[0]

            command = "SELECT Name_route FROM routesker WHERE _id = "
            command += str(one_transfer[1])
            cur.execute(command)
            name_route = cur.fetchone()[0]
            
            transfer.append([name_stop, name_route])

    except Exception as e:
        print({e})
        sql.close()
        exit()
    else:
        return 0, way_str, transfer

def read_db(stop1, stop2, sql_connection, cursor):
    stops = read_stops(sql_connection, cursor)

    errno, way, transfer = read_optimal_route(stop1, stop2,
     sql_connection, cursor)
    if errno == -1:
        print("No such start station")
    elif errno == -2:
        print("No such final station")
    elif errno == -3:
        print("No route for this stations")
    else:
        return stops, way, transfer

    return stops, [], []

def connection():
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'example_server.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

    except Exception as e:
        print({e})
        exit()
    else:
        return sqlite_connection, cur

def fun():
    sql_connection, cursor = connection()

    print("Enter first stop")
    stop1 = "STOP 1"
    print("Enter second stop")
    stop2 = "STOP 7"

    stops, way, transfer = read_db(stop1, stop2, sql_connection, cursor)

    return stops, way, transfer

def TEST_PRINT_STOPS(stops, way, transfer):
    print("\nOptimal way:")
    print("{}\n".format(way))

    print("Transfer:")
    print("{}\n".format(transfer))

    print("Stops")
    for stop in stops:
        print("{}) {} - {} {}".format(stop.get_id(),
        stop.get_name(), stop.get_x(), stop.get_y()))

def main():
    stops, way, transfer = fun()
    TEST_PRINT_STOPS(stops, way, transfer)

if __name__ == "__main__":
    main()
else:
    fun() 