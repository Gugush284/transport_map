import sqlite3
import os


class nstop:
    # Конструктор
    # elem consists of [id of nearby station, 
    # length of the way to it]
    def __init__(self, elem):
        self.nid = elem[0]
        self.len = elem[1]

    # return stop id
    def stop(self):
        return self.nid
    
    # return weight of the edge
    def weight(self):
        return self.len

class edge:
    # Конструктор
    def __init__(self):
        self.routes = list()
        self.stop = dict()

    # Filling in the fields
    # Array is a list of neigbors with route ways to them
    # Array consists of [[id of nearby station, length of the way
    # to it], route to the station]
    def add_edge(self, array):
        self.routes.append(array[1])
        self.stop[array[1]] = list()
        for elem in array[0]:
            self.stop[array[1]].append(nstop(elem))

    def get_route(self, index):
        return self.routes[index] 
    
    def get_routes_len(self):
        return len(self.routes)

    def get_stops(self, route):
        return self.stop[route]

# Search coords of stop in the route chain
# Create an array of chain index and add index if coords
# are the same
# Chain is chain of coordinates for current route
# Coords is [x,y] that we should find in chain
# Route is current route
def search_in_chain(chain, coords, route):
    array = list()

    if(len(chain)%2 != 0):
        print("Odd chain in the route with id - {}".format(route))
        exit()

    for index in range(0, len(chain), 2):
        if (chain[index] == coords[0])&(
        chain[index+1] == coords[1]):
            array.append(index)
    return array

# Count lenth between begin station and final station
# by coords
# begin_index is an index of begin station's x coordinate
# end_index is an index of final station's x coordinate
# Chain is chain of coordinates for current route
def Count_chain(sqlite_connection, begin_index, end_index, chain):
    sum = 0
    try:
        # We go through the x coordinate chain part using index 
        # index+1 is an index of station's y coordinate 
        for index in range(begin_index, end_index, 2):
            # Use sqrt((x1-x2)^2+(y1-y2)^2)
            sum += (((float(chain[index])-float(chain[index+2])) ** 2) 
            + ((float(chain[index+1])-float(chain[index+3])) ** 2)) ** 0.5
    except ValueError:
        print("Worng fomat of data in DATA BASE")
        sqlite_connection.close()
        exit()
    else:
        return sum

# sqlite_connection is a connection to data base
# cursor = sqlite_connection.cursor()
# id is an id of current stop
# idn is an id of neighbor stop
# Route is current route
def calculatу_weight(sqlite_connection, id, idn, route, cursor):
    try:
        # Find coordinate chain for the current route in Data base
        command = "SELECT chain_cords FROM routesker WHERE _id = "
        command += route
        cursor.execute(command)
        chain_coords = cursor.fetchone()[0].split()

        # Find coordinates of nearby station
        command = "SELECT Cords FROM stopsker WHERE _id = "
        command += str(idn)
        cursor.execute(command)
        neighbor_coords = cursor.fetchone()[0].split()

        # Find coordinates of nearby station
        command = "SELECT Cords FROM stopsker WHERE _id = "
        command += str(id)
        cursor.execute(command)
        coords = cursor.fetchone()[0].split()

        # Searching for the occurrence of coordinates in the chain
        array_index = search_in_chain(chain_coords, coords, route)
        assert(len(array_index) != 0)
        array_n_index = search_in_chain(chain_coords, neighbor_coords, route)
        assert(len(array_n_index) != 0)
        assert(array_index != array_n_index)

        # Calculating the weight of the edge 
        # for each option for current route
        weight = list()
        for i in array_index:
            for j in array_n_index:
                if (i > j):
                    weight.append(Count_chain(sqlite_connection, j, i, chain_coords))
                else:
                    weight.append(Count_chain(sqlite_connection, i, j, chain_coords))
        assert(len(weight) != 0)   

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
    except AssertionError:
       print("No such coords in DATA BASE")
       sqlite_connection.close()
       exit()
    else:
        # Choose the shortest way
        length = weight[0]
        if len(weight) != 1:
            for it in weight:
                if length > it:
                    length =  it
        return length

# For each nearby station calculating the weight of the edge
# Also form a list([id, weight])
# id is an id of current stop
# Route is current route
# sqlite_connection is a connection to data base
# cursor = sqlite_connection.cursor()
# id_neighb is a list of ids of neighbor stops
def add_weight(sqlite_connection, id, id_neighb, route, cursor):
    elem = list()
    for idn in id_neighb:
        elem.append([idn, calculatу_weight(sqlite_connection,
        id, idn, route, cursor)])
    return elem

# Find neighbors and calculate way to them for each stop
# sqlite_connection is a connection to data base
# cursor = sqlite_connection.cursor()
# id is an id of current stop
# routes_id is a list of ids of routes passing through the stop
def find_neighbor(sqlite_connection, id, routes_id, cursor):
    # List of nearby stops and length of the way to them
    neig = list()

    try:
        # Searching neaighbors using one of the routes
        # passing through the stop
        for r in routes_id:
            command = "SELECT chain_stops FROM routesker WHERE _id = "
            command += r
            cursor.execute(command)
            chain_stops = cursor.fetchone()[0].split()

            # List of nearby routes
            id_n = list()

            # Searching nearby stops in the route chain of stops
            for index in range(len(chain_stops)):
                if id == int(chain_stops[index]):
                    if index == 0:
                        id_n.append(int(chain_stops[index+1]))
                    elif index == len(chain_stops)-1:
                        id_n.append(int(chain_stops[index-1]))
                    else:
                        id_n.append(int(chain_stops[index-1]))
                        id_n.append(int(chain_stops[index+1]))
            
            # Add weight to the way connecting stops
            id_and_weight = add_weight(sqlite_connection, id, id_n, 
            r, cursor)

            neig.append([id_and_weight, int(r)])
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
        print("Worng fomat of data in DATA BASE")
        sqlite_connection.close()
        exit()
    else:
        return neig

# graph is a dict, where key is id of the station
# graph[key] has a type of class edge and contains
# information about nearby stations: their ids, length to them
# and routes to them
def reading_db(graph):
    try:
        # Connecting to data base
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'example.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        # Find an amount of stops
        command = "SELECT COUNT(_id) FROM stopsker"
        cur.execute(command)
        num = int((cur.fetchone())[0])

        # For each station build the environment of the neighboring stops,
        # the routes leading to them and the length of the path to them
        for i in range(num):
            # Recieve id, routes for current station
            command = "SELECT _id, Route_Num FROM stopsker WHERE _id = "
            command = command + str(i+1)
            cur.execute(command)
            one_result = cur.fetchone()

            id = int(one_result[0])
            stop_route = one_result[1].split()

            # Create a new elem of graph
            graph[id] = edge()

            # Find neigbors with route ways to them
            neigbors = find_neighbor(sqlite_connection, id, stop_route,
            cur)

            for neigbor in neigbors:
                graph[id].add_edge(neigbor)      
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
        return graph 
    finally:
        sqlite_connection.close()

# Test function to print graph
def print_graph(graph):
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'example.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        key = graph.keys()
        for k in key:
            command = "SELECT Name_stop FROM stopsker WHERE _id = "
            command = command + str(k)
            cur.execute(command)
            print("{} has ways:".format(cur.fetchone()[0]))
            elem = graph[k]
            for index in range(elem.get_routes_len()):
                route = elem.get_route(index)
                command = "SELECT Name_route FROM routesker WHERE _id = "
                command = command + str(route)
                cur.execute(command)
                print("     Route {}:".format(cur.fetchone()[0]))
                
                counter = 0
                for point in elem.get_stops(route):
                    command = "SELECT Name_stop FROM stopsker WHERE _id = "
                    command = command + str(point.stop())
                    cur.execute(command)
                    counter += 1
                    print("     {}) {} - {}".format(counter, cur.fetchone()[0],
                    point.weight()))
                    # print("{} {} {} {}".format(type(k), type(route), 
                    # type(point.stop()), type(point.weight())))
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
    finally:
        sqlite_connection.close()

def read():
    graph = dict()
    graph = reading_db(graph)
    return graph

def main():
    graph = dict()
    graph = reading_db(graph)
    print_graph(graph)

if __name__ == "__main__":
    main()
else:
    read()