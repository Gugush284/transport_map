import sqlite3
import os

class nstop:
    # Конструктор
    def __init__(self, id, len):
        self.nid = id
        self.len = len

    def stops(self):
        return self.nid

class edge:
    # Конструктор
    def __init__(self):
        self.routes = list()
        self.weight = dict()

    def add_edge(self, id, route, len):
        self.routes.append(route)
        self.weight[route] = nstop(id, len)

    def get_route(self, index):
        return self.routes[index] 
    
    def get_routes_len(self):
        return len(self.routes)

    def get_stops(self, route):
        return self.weight[route].stops()

def reading_db(graph):
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.db')
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        command = "SELECT COUNT(_id) FROM stopsker"
        cur.execute(command)
        num = int((cur.fetchone())[0])

        for i in range(num):
            command = "SELECT _id, Cords, Route_Num FROM stopsker WHERE _id = "
            command = command + str(i+1)
            cur.execute(command)
            one_result = cur.fetchone()

            id = int(one_result[0])
            cords = one_result[1].split()
            stop_route = one_result[2].split()

            graph[id] = edge()
            neig = list()

            for r in stop_route:
                command = "SELECT chain_stops FROM routesker WHERE _id = "
                command += r
                cur.execute(command)
                chain_stops = cur.fetchone()[0].split()
                id_n = list()
                for index in range(len(chain_stops)):
                    if id == int(chain_stops[index]):
                        if index == 0:
                            id_n.append(int(chain_stops[index+1]))
                        elif index == len(chain_stops)-1:
                            id_n.append(int(chain_stops[index-1]))
                        else:
                            id_n.append(int(chain_stops[index-1]))
                            id_n.append(int(chain_stops[index+1]))
                neig.append([id_n, r])

            for n in neig:
                graph[id].add_edge(n[0], int(n[1]), 0)
            
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
        return graph

def print_graph(graph):
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.db')
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
                print("     Route {}:".format(cur.fetchone()[0]), end=" ")
                for index2 in elem.get_stops(route):
                    command = "SELECT Name_stop FROM stopsker WHERE _id = "
                    command = command + str(index2)
                    cur.execute(command)
                    print(cur.fetchone()[0], end=" ") 
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
    finally:
        sqlite_connection.close()


def main():
    graph = dict()
    graph = reading_db(graph)
    print_graph(graph)

if __name__ == "__main__":
    main()