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

def list_stops(cur):
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
    except sqlite3.ProgrammingError:
        print("ProgrammingError in DATA BASE")
        exit()
    except sqlite3.OperationalError:
        print("OperationalError in DATA BASE")
        exit()
    except sqlite3.NotSupportedError:
        print("NotSupportedError in DATA BASE")
        exit()
    except sqlite3.IntegrityError:
        print("IntegrityError in DATA BASE")
        exit()
    except sqlite3.DatabaseError:
        print("DatabaseError in DATA BASE")
        exit()
    except sqlite3.Error:
        print("Error in DATA BASE")
        exit()
    except sqlite3.Warning:
        print("Warning in DATA BASE")
        exit()
    except ValueError:
        print("Worng data format in DATA BASE")
    else:
        return stops

def Ways(stop1, stop2, cur):

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
        flag = 0
        for elem in Input[1].split(";"):
            one_transfer = elem.split()
            transfer.append([int(item) for item in one_transfer])

    except sqlite3.ProgrammingError:
        print("ProgrammingError in DATA BASE")
        exit()
    except sqlite3.OperationalError:
        print("OperationalError in DATA BASE")
        exit()
    except sqlite3.NotSupportedError:
        print("NotSupportedError in DATA BASE")
        exit()
    except sqlite3.IntegrityError:
        print("IntegrityError in DATA BASE")
        exit()
    except sqlite3.DatabaseError:
        print("DatabaseError in DATA BASE")
        exit()
    except sqlite3.Error:
        print("Error in DATA BASE")
        exit()
    except sqlite3.Warning:
        print("Warning in DATA BASE")
        exit()
    except ValueError:
        print("Worng data format in DATA BASE")
    else:
        return 0, way_str, transfer

def fun():
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'example_server.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()
    except sqlite3.ProgrammingError:
        print("ProgrammingError in DATA BASE")
        exit()
    except sqlite3.OperationalError:
        print("OperationalError in DATA BASE")
        exit()
    except sqlite3.NotSupportedError:
        print("NotSupportedError in DATA BASE")
        exit()
    except sqlite3.IntegrityError:
        print("IntegrityError in DATA BASE")
        exit()
    except sqlite3.DatabaseError:
        print("DatabaseError in DATA BASE")
        exit()
    except sqlite3.Error:
        print("Error in DATA BASE")
        exit()
    except sqlite3.Warning:
        print("Warning in DATA BASE")
        exit()
    else:
        print("Enter first stop")
        #stop1 = input()
        print("Enter second stop")
        #stop2 = 1

        errno, way, transfer = Ways("STOP 1", "STOP 7", cur)
        if errno == -1:
            print("No such start station")
        elif errno == -2:
            print("No such final station")
        elif errno == -3:
            print("No route for this stations")
        else:
            return list_stops(cur), way, transfer

        return list_stops(cur), [], []
    finally:
        sqlite_connection.close()

def TEST_PRINT_STOPS(stops, way, transfer):
    print(way)
    print(transfer)
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