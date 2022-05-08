import heapq
import math
import os
import sqlite3
from audioop import reverse


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
        cur.execute("SELECT _id FROM routesker")
        amount = cur.fetchall()

        for num in amount:
            # num[0] is id of route
            id = num[0]

            # read chain of stops id for current stop
            cur.execute("SELECT chain_stops FROM routesker WHERE _id = ?", str(id))
            chain = cur.fetchone()[0].split()

            # change type of elem of chain
            chain_int = list()
            for elem in chain:
                chain_int.append(int(elem))

            # finding out if the route is circular
            cur.execute("SELECT Ring FROM routesker WHERE _id = ?", str(id))

            routes[int(id)] = route_info(chain_int, cur.fetchone()[0])

    except Exception as e:
        print({e})
        sqlite_connection.close()
        exit()
    else:
        return routes


def read_graph(sqlite_connection, cur):
    graph = dict()

    try:
        # Look for amount of stops and write to
        # a variable named "amount"
        cur.execute("SELECT _id FROM stopsker")
        amount = cur.fetchall()

        for num in amount:
            # id of current stop
            id = num[0]

            graph[id] = list()


            cur.execute("SELECT Route_Num FROM stopsker WHERE _id = ?", [str(id)])

            # array_routes is routes passing through the current stop
            array_routes = cur.fetchone()[0].split()

            for route in array_routes:
                # Get chain of stops for current route
                cur.execute("SELECT chain_stops FROM routesker WHERE _id = ?", route)
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


def read_db():
    try:
        # Connecting to data base
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "example.db")
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()
        # graph is a dict, where key is id of the station
        # graph[key] has a type of class edge list
        # routes is a dict, where key is id of the route
        # routes[key] has a type of list
        routes = read_routes(sqlite_connection, cur)
        graph = read_graph(sqlite_connection, cur)

    except Exception as e:
        print({e})
        exit()
    else:
        return graph, routes
    finally:
        sqlite_connection.close()


def TEST_PRINT(graph, routes):
    try:
        # Connecting to data base
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "example.db")
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        # Print stops in graph
        key_graph = graph.keys()
        for key in key_graph:

            cur.execute("SELECT Name_stop FROM stopsker WHERE _id = ?",
                [str(key)])
            name = cur.fetchone()[0]

            for elem in graph[key]:
                cur.execute("SELECT Name_route FROM routesker WHERE _id = ?",
                    str(elem.get_route_name()))

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
            cur.execute("SELECT Name_route FROM routesker WHERE _id = ?",
                str(key))

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

    except Exception as e:
        print({e})
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
        cur.execute("SELECT chain_stops FROM routesker WHERE _id = ?",
            str(route))
        chain_str_id = cur.fetchone()[0].split()

        # translate stop ids into int
        chain_id = list()
        for item in chain_str_id:
            chain_id.append(int(item))
        del chain_str_id

        # get a chain of coordinates
        cur.execute("SELECT chain_cords FROM routesker WHERE _id = ?", 
            str(route))
        chain_str_coords = cur.fetchone()[0].split()

        # compose and translate coordinates into float
        chain_coords = list()
        for index in range(0, len(chain_str_coords), 2):
            chain_coords.append(
                (float(chain_str_coords[index]), float(chain_str_coords[index + 1]))
            )
        del chain_str_coords

        # check if the route is circular
        cur.execute("SELECT Ring FROM routesker WHERE _id = ?",
            str(route))
        ring = int(cur.fetchone()[0])

        # get a coords of stop1 id and translate it into float
        cur.execute("SELECT Cords FROM stopsker WHERE _id = ?",
            str(stop1))
        stop1_coords_str = cur.fetchone()[0].split()
        stop1_coords = (float(stop1_coords_str[0]), float(stop1_coords_str[1]))
        del stop1_coords_str

        # get a coords of stop2 id and translate it into float
        cur.execute("SELECT Cords FROM stopsker WHERE _id = ?",
            str(stop2))
        stop2_coords_str = cur.fetchone()[0].split()
        stop2_coords = (float(stop2_coords_str[0]), float(stop2_coords_str[1]))
        del stop2_coords_str

    except Exception as e:
        print({e})
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
                    if position1 < position2:
                        way = list()
                        for index in range(position1, position2 + 1, 1):
                            way.append(chain_coords[index])
                        road.append(way)
        else:
            # if the route is circular, we find
            # a chain of coordinates connecting the stops
            for position1 in position_stop1:
                for position2 in position_stop2:
                    way = list()
                    if position1 < position2:
                        # if there is a start in the chain
                        # first, and then the end
                        for index in range(position1, position2 + 1, 1):
                            way.append(chain_coords[index])
                        road.append(way)
                    else:
                        # if there is an end in the chain first, and then a
                        # start, go from the start to the end of the chain
                        # array, and from the beginning of the array to the end
                        for index in range(position1, len(chain_coords), 1):
                            way.append(chain_coords[index])
                        for index in range(0, position2 + 1, 1):
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
        for index in range(len(enroute) - 1):
            # formula for calculating the distance between
            # two points and on a plane: sqrt((x2-x1)^2 + (y2-y1)^2)
            length += (
                ((enroute[index + 1][0] - enroute[index][0]) ** 2)
                + ((enroute[index + 1][1] - enroute[index][1]) ** 2)
            ) ** 0.5

        return length


def TEST_calculation():
    try:
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "example.db")
        sqlite_connection = sqlite3.connect(path)
        cur = sqlite_connection.cursor()

        print("Enter id of route")
        r_id = int(input())
        print("Enter id of first stop")
        s1_id = int(input())
        print("Enter id of second stop")
        s2_id = int(input())

    except Exception as e:
        print({e})
    else:
        print(calculation(r_id, s1_id, s2_id, cur))
    finally:
        sqlite_connection.close()


# a part that works this the stops in the route
# conting implicit edges
def dijkstra_core(
    route,
    stop_num,
    side,
    start,
    sum_im_ed_1,
    routes,
    dist,
    prev_stop,
    last_route,
    priority_queue,
):
    # variables that will help to write a loop
    # depending on the direction of movement
    sum_im_ed = sum_im_ed_1
    end_point = 0
    plus = 0
    start_2 = 0
    if side == 1:
        end_point = len(routes[route]) - 1
        plus = 1
        start_2 = 0
    else:
        end_point = 0
        plus = -1
        start_2 = len(routes[route]) - 1
    # we can have a route like {1, 2, 3, 4, 5, 6, 3, 2, 1}
    for k in range(start, end_point, plus):
        if k != start and routes[route][k] == stop_num:
            break
        if sum_im_ed > dist[routes[route][k]]:
            break
        sum_im_ed += calculation(route, routes[route][k], routes[route][k + plus])
        # checking whether the road will be shorter
        # if so, then we change the corresponding parameters
        if dist[routes[route][k]] > sum_im_ed:
            dist[routes[route][k]] = sum_im_ed
            prev_stop[routes[route][k]] = stop_num
            last_route[route[route][k]] = route
            heapq.heappush(
                priority_queue,
                (dist[routes[route][k]]),
                routes[route][k],
            )
    sum_im_ed += calculation(
        route, routes[route][len(routes[route]) - 1], routes[route][0]
    )
    for k in range(start_2, start, plus):
        if k != start and routes[route][k] == stop_num:
            break
        if sum_im_ed > dist[routes[route][k]]:
            break
        sum_im_ed += calculation(route, routes[route][k], routes[route][k + plus])
        if dist[routes[route][k]] > sum_im_ed:
            dist[routes[route][k]] = sum_im_ed
            prev_stop[routes[route][k]] = stop_num
            last_route[route[route][k]] = route
            heapq.heappush(
                priority_queue,
                (dist[routes[route][k]]),
                routes[route][k],
            )


def routes_to_all_stops(start_stop, graph, routes):
    # stop has an id id \in [1 ... amount_of_stops]
    # priority_queue -- a struct where we are putting a stop and a length to it
    priority_queue = []
    heapq.heapify(priority_queue)
    # last_route -- a list with the last route from which we came to stop
    last_route = [None for i in range(len(graph) + 1)]
    # prev_stop -- a list with the last stop from with we came to stop
    prev_stop = [None for i in range(len(graph) + 1)]
    # the long of the way to the stop
    dist = [math.inf for i in range(len(graph) + 1)]
    # if a stop was visited 1 else 0
    visited = [0 for i in range(len(graph) + 1)]
    # pushing the start_stop to heapq
    heapq.heappush(priority_queue, (0, start_stop))
    dist[start_stop] = 0
    prev_stop[start_stop] = start_stop

    while len(priority_queue) != 0:
        # taking the min path
        tmp = heapq.heappop(priority_queue)
        way_len = tmp[0]
        stop_num = tmp[1]
        visited[stop_num] = 1

        # looking if there is a sense to start dijkstra
        if way_len > dist[stop_num]:
            continue
        # we running all routes which a pasing througth our stop
        for i in range(len(graph[stop_num])):
            route = graph[stop_num][i].get_route_name()
            pointer = graph[stop_num][i].get_pointer()
            if_a_ring = routes[route].get_ring()
            # adding delty for changing the route
            sum_im_ed_1 = 1
            # run dijkstra depending on the type of route
            # if it a ring we shoul do dijkstra in both pathes
            if if_a_ring != 0:
                for j in range(len(pointer)):
                    # moving to the right
                    if visited[pointer[j]] == 1:
                        continue
                    sum_im_ed_1 += dist[stop_num]
                    dijkstra_core(
                        route,
                        stop_num,
                        1,
                        pointer[j],
                        sum_im_ed_1,
                        routes,
                        dist,
                        prev_stop,
                        last_route,
                        priority_queue,
                    )
                    # moving to the left
                    dijkstra_core(
                        route,
                        stop_num,
                        -1,
                        pointer[j],
                        sum_im_ed_1,
                        routes,
                        dist,
                        prev_stop,
                        last_route,
                        priority_queue,
                    )
            # if it's not a ring then one side
            else:
                for j in range(len(pointer)):
                    if visited[pointer[j]] == 1:
                        continue
                    # moving to the right
                    dijkstra_core(
                        route,
                        stop_num,
                        1,
                        pointer[j],
                        sum_im_ed_1,
                        routes,
                        dist,
                        prev_stop,
                        last_route,
                        priority_queue,
                    )
    return_routes(last_route, prev_stop, graph, start_stop)


def find_path(mass, start_stop, last_stop):
    path = list()
    path.append(last_stop)
    while last_stop != start_stop:
        path.append(mass[last_stop])
        last_stop = mass[last_stop]
    reverse(path)
    return path


def return_routes(last_route, prev_stop, graph, start_stop):
    for i in range(1, len(graph) + 1):
        if i != start_stop:
            return (
                start_stop,
                i,
                find_path(prev_stop, start_stop, i),
                find_path(last_route, start_stop, i),
            )


# the main function finding the optimal route between all pairs of stops
def opt_routes(graph, routes):
    # we run through all the stops in the graph
    # and find all the optimal paths from one stop to another
    for i in range(1, len(graph)):
        # returns dict consistes of stop and route to stop from "start_stop"
        d = routes_to_all_stops(i, graph, routes)
        # here you need to write function that will import the dict to new db


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
