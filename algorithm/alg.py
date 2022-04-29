from ast import Delete
import sqlite3
import os

class edge:
    # Конструктор
    # pointer indicates the sequence numbers
    # in the chain of stops for the route
    # route is one of the passing routes 
    # through this stop
    def __init__(self, route, pointer):
        self.route = route
        self.pointer = pointer

    def get_pointer(self):
        return self.pointer

    def get_route_name(self):
        return self.route

class route_info:
    # Конструктор
    # RING indicates if the route is a ring 
    # route is one of the passing routes 
    # through this stop
    def __init__(self, route, RING):
        self.route = route
        self.ring = RING

    def get_ring(self):
        return self.ring

    def get_route(self):
        return self.route

def read_routes(sqlite_connection, cur):
    routes = dict()

    try:
        # Look for amount of routes and write to
        # a variable named "amount"
        command = "SELECT _id FROM routesker"
        cur.execute(command)
        amount = cur.fetchall()
        
        for num in amount:
            # num[0] is id of route
            id = num[0]
            
            # read chain of stops id for current stop
            command = "SELECT chain_stops FROM routesker WHERE _id = "
            command += str(id)
            cur.execute(command)
            chain = cur.fetchone()[0].split()

            # change type of elem of chain
            chain_int = list()
            for elem in chain:
                chain_int.append(int(elem))

            # finding out if the route is circular 
            command = "SELECT Ring FROM routesker WHERE _id = "
            command += str(id)
            cur.execute(command)

            routes[int(id)] = route_info(chain_int, cur.fetchone()[0])

    except sqlite3.ProgrammingError:
        print("ProgrammingError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.OperationalError:
        print("OperationalError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.NotSupportedError:
        print("NotSupportedError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.IntegrityError:
        print("IntegrityError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.DatabaseError:
        print("DatabaseError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.Error:
        print("Error in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.Warning:
        print("Warning in DATA BASE")
        sqlite_connection.close() 
        exit()
    except ValueError:
        print("Worng data format in DATA BASE")
        sqlite_connection.close() 
        exit()
    else:
        return routes 

def read_graph(sqlite_connection, cur):
    graph = dict()

    try:
        # Look for amount of stops and write to
        # a variable named "amount"
        command = "SELECT _id FROM stopsker"
        cur.execute(command)
        amount = cur.fetchall()
        
        for num in amount:
            # id of current stop
            id = num[0]

            graph[id] = list()

            command = "SELECT Route_Num FROM stopsker WHERE _id = "
            command += str(id)
            cur.execute(command)

            # array_routes is routes passing through the current stop
            array_routes = cur.fetchone()[0].split()
            
            for route in array_routes:
                # Get chain of stops for current route
                command = "SELECT chain_stops FROM routesker WHERE _id = "
                command += route
                cur.execute(command)
                chain = cur.fetchone()[0].split()

                # Find indicator of the sequence number
                # in the chain of stops for the route
                pointer = list()
                counter = 0
                for stop in chain:
                    if int(stop) == id:
                        pointer.append(counter)
                    counter += 1
                graph[id].append(edge(int(route), pointer))

    except sqlite3.ProgrammingError:
        print("ProgrammingError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.OperationalError:
        print("OperationalError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.NotSupportedError:
        print("NotSupportedError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.IntegrityError:
        print("IntegrityError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.DatabaseError:
        print("DatabaseError in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.Error:
        print("Error in DATA BASE")
        sqlite_connection.close() 
        exit()
    except sqlite3.Warning:
        print("Warning in DATA BASE")
        sqlite_connection.close() 
        exit()
    except ValueError:
        print("Worng data format in DATA BASE")
        sqlite_connection.close() 
        exit()
    else:
        return graph

def read_db():
    try:
        # Connecting to data base
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'example.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        # graph is a dict, where key is id of the station
        # graph[key] has a type of class edge list
        # routes is a dict, where key is id of the route
        # routes[key] has a type of list
        routes = read_routes(sqlite_connection, cur)
        graph = read_graph(sqlite_connection, cur)   

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
        exit()
    else:
        return graph, routes
    finally:
        sqlite_connection.close()

def TEST_PRINT(graph, routes):
    try:
        # Connecting to data base
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'example.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        # Print stops in graph
        key_graph = graph.keys()
        for key in key_graph:

            command = "SELECT Name_stop FROM stopsker WHERE _id = "
            command += str(key)
            cur.execute(command)
            name = cur.fetchone()[0]

            for elem in graph[key]:
                command = "SELECT Name_route FROM routesker WHERE _id = "
                command += str(elem.get_route_name())
                cur.execute(command)

                print("{} (id = {}) in {} by {} positions: {}".format(name, key,
                cur.fetchone()[0], elem.get_pointer(), routes[elem.get_route_name()].get_route()))


        # Print routes
        print("\nRoutes:")

        key_routes = routes.keys()
        for key in key_routes:
            command = "SELECT Name_route FROM routesker WHERE _id = "
            command += str(key)
            cur.execute(command)

            if routes[key].get_ring() != 0:
                route_name = "Ring route"
            else:
                route_name = "Route"

            print("{} {}: {}".format(route_name, cur.fetchone()[0], routes[key].get_route()))

        print("\n", end="")

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
        exit()
    finally:
        sqlite_connection.close()


# stop1 is id of start stop
# stop2 is id of end stop
# route is id of route
# cur is sql cursor
def calculation(route, stop1, stop2, cur):

    # if stop1 is stop 
    if stop1 == stop2:
        return 0

    try:
        
        # get a chain of stop ids 
        command = "SELECT chain_stops FROM routesker WHERE _id = "
        command += str(route)
        cur.execute(command)
        chain_str_id = cur.fetchone()[0].split()

        # translate stop ids into int
        chain_id = list()
        for item in chain_str_id:
            chain_id.append(int(item))        
        del chain_str_id

        # get a chain of coordinates
        command = "SELECT chain_cords FROM routesker WHERE _id = "
        command += str(route)
        cur.execute(command)
        chain_str_coords = cur.fetchone()[0].split()

        # compose and translate coordinates into float
        chain_coords = list()
        for index in range(0, len(chain_str_coords), 2):
            chain_coords.append((
                float(chain_str_coords[index]),
                float(chain_str_coords[index+1])
            ))
        del chain_str_coords

        # check if the route is circular
        command = "SELECT Ring FROM routesker WHERE _id = "
        command += str(route)
        cur.execute(command)
        ring = int(cur.fetchone()[0])

        # get a coords of stop1 id and translate it into float
        command = "SELECT Cords FROM stopsker WHERE _id = "
        command += str(stop1)
        cur.execute(command)
        stop1_coords_str = cur.fetchone()[0].split()
        stop1_coords = (float(stop1_coords_str[0]), 
        float(stop1_coords_str[1]))
        del stop1_coords_str
        
        # get a coords of stop2 id and translate it into float
        command = "SELECT Cords FROM stopsker WHERE _id = "
        command += str(stop2)
        cur.execute(command)
        stop2_coords_str = cur.fetchone()[0].split()
        stop2_coords = (float(stop2_coords_str[0]), 
        float(stop2_coords_str[1]))
        del stop2_coords_str

    except sqlite3.ProgrammingError:
        print("ProgrammingError in DATA BASE")
        return -1
    except sqlite3.OperationalError:
        print("OperationalError in DATA BASE")
        return -1
    except sqlite3.NotSupportedError:
        print("NotSupportedError in DATA BASE")
        return -1
    except sqlite3.IntegrityError:
        print("IntegrityError in DATA BASE")
        return -1
    except sqlite3.DatabaseError:
        print("DatabaseError in DATA BASE")
        return -1
    except sqlite3.Error:
        print("Error in DATA BASE")
        return -1
    except sqlite3.Warning:
        print("Warning in DATA BASE")
        return -1
    except ValueError:
        print("Worng data format in DATA BASE")
        return -2
    else:

        # look for the positions of the coordinates 
        # of stops in the chain of coordinates of the route
        position_stop1 = list()
        position_stop2 = list()

        for index in range(len(chain_coords)):
            if chain_coords[index] == stop1_coords:
                position_stop1.append(index)
            elif chain_coords[index] == stop2_coords:
                position_stop2.append(index)

        if (len(position_stop1) == 0) or (len(position_stop2) == 0):
            return -3

        road = list()
        
        # if the route is not circular, we find from right to
        # left all the coordinate chains connecting the stops
        if ring != 1:
            for position1 in position_stop1:
                for position2 in position_stop2:
                    if (position1 < position2):
                        way = list()
                        for index in range(position1, position2+1, 1):
                            way.append(chain_coords[index])
                        road.append(way)
        else:
        # if the route is circular, we find
        # a chain of coordinates connecting the stops
           for position1 in position_stop1:
                for position2 in position_stop2:
                    way = list()
                    if (position1 < position2):
                    # if there is a start in the chain 
                    # first, and then the end
                        for index in range(position1, position2+1, 1):
                            way.append(chain_coords[index])
                        road.append(way)
                    else:
                    # if there is an end in the chain first, and then a 
                    # start, go from the start to the end of the chain 
                    # array, and from the beginning of the array to the end
                        for index in range(position1, len(chain_coords), 1):
                            way.append(chain_coords[index])
                        for index in range(0, position2+1, 1):
                            way.append(chain_coords[index])
                        road.append(way)

        if len(road) == 0:
                return -3

        # we find out the smallest chain of coordinates
        enroute = road[0]
        for way in road:
            if len(way) < len(enroute):
                enroute = way

        del way
        del road
        del position_stop1
        del position_stop2

        # sum up the distances between the points
        length = 0
        for index in range(len(enroute)-1):
            # formula for calculating the distance between 
            # two points and on a plane: sqrt((x2-x1)^2 + (y2-y1)^2)
            length += (((enroute[index + 1][0] - enroute[index][0]) ** 2) + (
                (enroute[index + 1][1] - enroute[index][1]) ** 2)) ** 0.5
                
        return length

def TEST_calculation():
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'example.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        print ("Enter id of route")
        r_id = int(input())
        print ("Enter id of first stop")
        s1_id = int(input())
        print ("Enter id of second stop")
        s2_id = int(input())

    except sqlite3.ProgrammingError:
        print("ProgrammingError in DATA BASE")
    except sqlite3.OperationalError:
        print("OperationalError in DATA BASE")
    except sqlite3.NotSupportedError:
        print("NotSupportedError in DATA BASE")
    except sqlite3.IntegrityError:
        print("IntegrityError in DATA BASE")
    except sqlite3.DatabaseError:
        print("DatabaseError in DATA BASE")
    except sqlite3.Error:
        print("Error in DATA BASE")
    except sqlite3.Warning:
        print("Warning in DATA BASE")
    except ValueError:
        print("Worng data format in DATA BASE")
    else:
        print(calculation(r_id, s1_id, s2_id, cur))
    finally:
        sqlite_connection.close()

def fun():
    # graph is a dict, where key is id of the station
    # graph[key] has a type of class edge list
    # routes is a dict, where key is id of the route
    # routes[key] has a type of route_info
    graph, routes = read_db()

def main():
    # graph is a dict, where key is id of the station
    # graph[key] has a type of class edge list
    # routes is a dict, where key is id of the route
    # routes[key] has a type of route_info
    graph, routes = read_db()
    TEST_PRINT(graph, routes)
    TEST_calculation()

if __name__ == "__main__":
    main()
else:
    fun()