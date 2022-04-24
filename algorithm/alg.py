import sqlite3
import os

class edge:
    # Конструктор
    # pointer indicates the sequence number
    # in the chain of stops for the route
    # route is one of the passing routes 
    # through this stop
    def __init__(self, route, pointer):
        self.route = route
        self.pointer = pointer

    def get_pointer(self):
        return self.pointer

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

            routes[int(id)] = chain_int

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
                pointer = 0
                for stop in chain:
                    if int(stop) == id:
                        break;
                    pointer += 1
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

        key_graph = graph.keys()
        for key in key_graph:

            command = "SELECT Name_stop FROM stopsker WHERE _id = "
            command += str(key)
            cur.execute(command)
            name = cur.fetchone()[0]

            for elem in graph[key]:
                command = "SELECT Name_route FROM routesker WHERE _id = "
                command += str(elem.get_route())
                cur.execute(command)

                print("{} (id = {}) in {} by {} position: {}".format(name, key,
                cur.fetchone()[0], elem.get_pointer()+1, routes[elem.get_route()]))

        print()

        key_routes = routes.keys()
        for key in key_routes:
            print(routes[key])
            


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

def main():
    # graph is a dict, where key is id of the station
    # graph[key] has a type of class edge list
    # routes is a dict, where key is id of the route
    # routes[key] has a type of list
    graph, routes = read_db()
    TEST_PRINT(graph, routes)


if __name__ == "__main__":
    main()