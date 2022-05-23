import os
import sqlite3

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

def read_routes(sqlite_connection):
    routes = dict()

    try:
        cur = sqlite_connection.cursor()

        # Look for amount of routes and write to
        # a variable named "amount"
        cur.execute("SELECT _id FROM routesker")
        amount = cur.fetchall()

        for num in amount:
            # num[0] is id of route
            id = num[0]

            # read chain of stops id for current stop
            cur.execute("SELECT chain_stops FROM routesker WHERE _id = ?",
                [id])
            chain = cur.fetchone()[0].split()

            # change type of elem of chain
            chain_int = list()
            for elem in chain:
                chain_int.append(int(elem))

            # finding out if the route is circular
            cur.execute("SELECT Ring FROM routesker WHERE _id = ?",
                [id])

            routes[int(id)] = route_info(chain_int, cur.fetchone()[0])

    except Exception as e:
        print({e})
        sqlite_connection.close()
        exit()
    else:
        return routes


def read_graph(sqlite_connection):
    graph = dict()

    try:
        cur = sqlite_connection.cursor()

        # Look for amount of stops and write to
        # a variable named "amount"
        cur.execute("SELECT _id FROM stopsker")
        amount = cur.fetchall()

        for num in amount:
            # id of current stop
            id = num[0]

            graph[id] = list()


            cur.execute("SELECT Route_Num FROM stopsker WHERE _id = ?",
                [id])

            # array_routes is routes passing through the current stop
            array_routes = cur.fetchone()[0].split()

            for route in array_routes:
                # Get chain of stops for current route
                cur.execute("SELECT chain_stops FROM routesker WHERE _id = ?",
                    [route])
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

    except Exception as e:
        print({e})
        sqlite_connection.close()
        exit()
    else:
        return graph

def TEST_PRINT(graph, routes, sqlite_connection, seq_stops):
    try:
        cur = sqlite_connection.cursor()

        # Print stops in graph
        key_graph = graph.keys()
        for key in key_graph:

            cur.execute("SELECT Name_stop FROM stopsker WHERE _id = ?",
                [str(key)])
            name = cur.fetchone()[0]

            for elem in graph[key]:
                cur.execute("SELECT Name_route FROM routesker WHERE _id = ?",
                    [elem.get_route_name()])

                print(
                    "{} (id = {}) in {} by {} positions: {}".format(
                        name,
                        key,
                        cur.fetchone()[0],
                        elem.get_pointer(),
                        routes[elem.get_route_name()].get_route(),
                    )
                )

        # Print routes
        print("\nRoutes:")

        key_routes = routes.keys()
        for key in key_routes:
            cur.execute(
                "SELECT Name_route FROM routesker WHERE _id = ?",
                [key])

            if routes[key].get_ring() != 0:
                route_name = "Ring route"
            else:
                route_name = "Route"

            print(
                "{} {}: {}".format(
                    route_name, cur.fetchone()[0],
                    routes[key].get_route()
                )
            )

        print("\n", end="")
        print(seq_stops)
        print("\n", end="")

    except Exception as e:
        print({e})
        exit()

def sequence_id(sqlite_connection):
    try:
        cur = sqlite_connection.cursor()

        cur.execute("SELECT _id FROM stopsker")

        seq = list()
        for elem in cur.fetchall():
            seq.append(int(elem[0]))

    except Exception as e:
        print({e})
        exit()
    else:
        return seq

def main():
    try:
        # Connecting to data base
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "example.db")
        sqlite_connection = sqlite3.connect(path)
        # graph is a dict, where key is id of the station
        # graph[key] has a type of class edge list
        # routes is a dict, where key is id of the route
        # routes[key] has a type of list
        routes = read_routes(sqlite_connection)
        graph = read_graph(sqlite_connection)
        seq_stops = sequence_id(sqlite_connection)

    except Exception as e:
        print({e})
        exit()
    else:
        TEST_PRINT(graph, routes, sqlite_connection, seq_stops)
    finally:
        sqlite_connection.close()

if __name__ == "__main__":
    main()
    