""" provide priority queue algorithm
    that is used in dijkstra_core
"""
import heapq
import math
import os
import sqlite3

import read_db


class CalRoad:
    """The class returned from
    calculation function contains three objects:
    coords_ruadlist of coordinates from the stop
    1 to stop 2
    length - float variable containing length
    between 1 and 2 stops
    stops - list, id of two stops
    route - id of the route that we are counting
    distance between stops"""

    def __init__(self, stop1, stop2, route, road, length):
        self.coords_road = road
        self.length = length
        self.stops = [stop1, stop2]
        self.route = route

    def get_coords(self):
        """return coords between two stops"""
        return self.coords_road

    def get_length(self):
        """return length between two stops"""
        return self.length

    def get_stops(self):
        """return start stoop and finish stop"""
        return self.stops

    def get_route(self):
        """return route connecting these stops"""
        return self.route


class Path:
    """used to return information
        about the best way from one stop
        to another"""

    def __init__(self, stop1, stop2, stops_path,
                 routes_path, path_of_coords):
        self.stop1_ = stop1
        self.stop2_ = stop2
        self.path_of_stops_ = stops_path
        self.path_of_routes_ = routes_path
        self.path_of_coords_ = path_of_coords

    def get_stop1(self):
        """return the start stop"""
        return self.stop1_

    def get_stop2(self):
        """return the fnish stop"""
        return self.stop2_

    def get_path_of_routes(self):
        """return path of routes connecting the stops"""
        return self.path_of_routes_

    def get_path_of_stops(self):
        """return path of stops connecting the stops"""
        return self.path_of_stops_

    def get_path_of_coords(self):
        """return path of coords cnnecting the stops"""
        return self.path_of_coords_


def find_road(chain_coords, stop1_coords, stop2_coords, ring):
    """look for the positions of the coordinates
        of stops in the chain of coordinates of the route"""
    position_stop1 = list()
    position_stop2 = list()

    for index in range(len(chain_coords)):
        if chain_coords[index] == stop1_coords:
            position_stop1.append(index)
        elif chain_coords[index] == stop2_coords:
            position_stop2.append(index)

    if (len(position_stop1) == 0) or (len(position_stop2) == 0):
        return []

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

    return road


def calculation(route, stop1, stop2):
    """stop1 is id of start stop
    stop2 is id of end stop
    route is id of route
    cur is sql cursor
    function return class CalRoad"""
    # if stop1 is stop
    if stop1 == stop2:
        return CalRoad(stop1, stop2, route, [], 0)

    try:

        cur = SQLITE_CONNECTION.cursor()

        # get a chain of stop ids
        cur.execute("SELECT chain_stops FROM routesker WHERE _id = ?", [route])
        chain_str_id = cur.fetchone()[0].split()

        # translate stop ids into int
        chain_id = list()
        for item in chain_str_id:
            chain_id.append(int(item))
        del chain_str_id

        # get a chain of coordinates
        cur.execute("SELECT chain_cords FROM routesker WHERE _id = ?", [route])
        chain_str_coords = cur.fetchone()[0].split()

        # compose and translate coordinates into float
        chain_coords = list()
        for index in range(0, len(chain_str_coords), 2):
            chain_coords.append((
                            float(chain_str_coords[index]),
                            float(chain_str_coords[index + 1])
                            ))
        del chain_str_coords

        # check if the route is circular
        cur.execute("SELECT Ring FROM routesker WHERE _id = ?", [route])
        ring = int(cur.fetchone()[0])

        # get a coords of stop1 id and translate it into float
        cur.execute("SELECT Cords FROM stopsker WHERE _id = ?", [stop1])
        stop1_coords_str = cur.fetchone()[0].split()
        stop1_coords = (float(stop1_coords_str[0]), float(stop1_coords_str[1]))
        del stop1_coords_str

        # get a coords of stop2 id and translate it into float
        cur.execute("SELECT Cords FROM stopsker WHERE _id = ?", [stop2])
        stop2_coords_str = cur.fetchone()[0].split()
        stop2_coords = (float(stop2_coords_str[0]), float(stop2_coords_str[1]))
        del stop2_coords_str

    except Exception as exce:  # pylint: disable=broad-except
        print({exce})
        exit()
    else:
        road = find_road(chain_coords, stop1_coords, stop2_coords, ring)

        # we find out the smallest chain of coordinates
        enroute = []
        length = math.inf
        for way in road:

            # sum up the distances between the points
            length_way = 0
            for index in range(len(way) - 1):
                # formula for calculating the distance between
                # two points and on a plane: sqrt((x2-x1)^2 + (y2-y1)^2)
                length_way += (
                    ((way[index + 1][0] - way[index][0]) ** 2)
                    + ((way[index + 1][1] - way[index][1]) ** 2)
                ) ** 0.5

            if length_way < length:
                length = length_way
                enroute = way

        # print(enroute, end="\n\n")

        info = CalRoad(stop1, stop2, route, enroute, length)
        # print(info.get_coords())

        return info


# a part that works this the stops in the route
# counting implicit edges
def dijkstra_core(
    num_of_route,
    stop_num,
    start_pointer,
    sum_im_ed_1,
    routes,
    dist,
    prev_stop,
    last_route,
    priority_queue,
):
    """runs along routes and chooses the optimal path length"""
    sum_im_ed = sum_im_ed_1
    route = routes[num_of_route].get_route()
    flag = 0
    end_pointer = len(route) - 1
    for index in range(start_pointer, end_pointer - 1):
        if index != start_pointer and route[index] == stop_num:
            flag = 1
            break
        sum_im_ed += calculation(num_of_route, route[index],
                                 route[index + 1]).get_length()
        # checking whether the road will be shorter
        # if so, then we change the corresponding parameters
        if dist[route[index + 1]] > sum_im_ed:
            dist[route[index + 1]] = sum_im_ed
            prev_stop[route[index + 1]] = route[index]
            last_route[route[index + 1]] = num_of_route
            heapq.heappush(priority_queue,
                           (dist[route[index + 1]],
                            route[index + 1]))

    # block that mange a jump from the end of an array to its beginning
    if flag == 0:
        sum_im_ed += calculation(num_of_route, route[len(route) - 1],
                                 route[0]).get_length()
        if dist[route[0]] > sum_im_ed:
            dist[route[0]] = sum_im_ed
            prev_stop[route[0]] = route[len(route) - 1]
            last_route[route[0]] = num_of_route
            heapq.heappush(priority_queue, (dist[route[0]], route[0]))

        for index in range(0, start_pointer):
            if index != start_pointer and route[index] == stop_num:
                break
            sum_im_ed += calculation(num_of_route, route[index],
                                     route[index + 1]).get_length()
            if dist[route[index + 1]] > sum_im_ed:
                dist[route[index + 1]] = sum_im_ed
                prev_stop[route[index + 1]] = route[index]
                last_route[route[index + 1]] = route
                heapq.heappush(priority_queue,
                               (dist[route[index + 1]],
                                route[index + 1]))


def routes_to_all_stops(start_stop, graph, routes, seq_stops):
    """return the opt way to all stops from start_stop"""
    # stop has an id id \in [1 ... amount_of_stops]
    # that is why we are making structures in len(graph) + 1
    # priority_queue a struct where we are putting a stop and a length to it
    max_num = max(seq_stops)
    priority_queue = []
    heapq.heapify(priority_queue)
    # last_route -- a list with the last route from which we came to stop
    # needs for optimization and getting final path
    last_route = [None for i in range(max_num + 1)]
    # prev_stop -- a list with the last stop from with we came to stop
    prev_stop = [None for i in range(max_num + 1)]
    # the long of the way to the stop
    dist = [math.inf for i in range(max_num + 1)]
    # if a stop was visited 1 else 0
    # needs for optimization
    visited = [0 for i in range(max_num + 1)]
    # pushing the start_stop to heapq
    heapq.heappush(priority_queue, (0, start_stop))
    dist[start_stop] = 0
    prev_stop[start_stop] = start_stop

    while len(priority_queue) != 0:
        # taking the min path
        tmp = heapq.heappop(priority_queue)
        way_len = tmp[0]
        stop_num = tmp[1]
        if visited[stop_num] == 1:
            continue
        # looking if there is a sense to start dijkstra
        if way_len > dist[stop_num]:
            continue
        # we running all routes which a pasing througth our stop
        for i in range(len(graph[stop_num])):
            route = graph[stop_num][i].get_route_name()
            pointer = graph[stop_num][i].get_pointer()
            sum_im_ed = dist[stop_num]
            # use that trick not for making a lot of transfers
            if route != last_route[stop_num] and stop_num != start_stop:
                sum_im_ed += 1

            for j in range(len(pointer)):
                dijkstra_core(
                    route,
                    stop_num,
                    pointer[j],
                    sum_im_ed,
                    routes,
                    dist,
                    prev_stop,
                    last_route,
                    priority_queue,
                )
        # note that all possible paths from the node have been parsed
        visited[stop_num] = 1
    # return the stracture consists of start stop, final stop
    # list of stops connecting them
    # list of routes connecting them
    return return_routes(last_route, prev_stop, graph, start_stop)


def path_of_stops(start_stop, last_stop, mass):
    """return path consisting of stops"""
    path = list()
    path.append(last_stop)
    while last_stop != start_stop:
        path.append(mass[last_stop])
        last_stop = mass[last_stop]
    path.reverse()
    return path


def path_of_routes(mass, route):
    """return path consisting of routes"""
    path = list()
    for i in enumerate(mass):
        path.append(route[mass[i]])
    path[0] = path[1]
    return path


def coord_way(stops, route):
    """return path consisting of coords"""
    res = list()
    if len(stops) == 0:
        return res
    for i in range(1, len(stops)):
        res.append(calculation(route[i], stops[i - 1], stops[i]).get_coords())
    if len(res) != 1:
        for i in range(len(res) - 1):
            res[i].pop(len(res[i]) - 1)
    return res


def return_routes(last_route, prev_stop, graph, start_stop):
    """return struct Path"""
    ans = list()
    for i in range(1, len(graph) + 1):
        if prev_stop[i] is None or i == start_stop:
            ans.append(Path(start_stop, i, [], [], []))
        else:
            mass = path_of_stops(start_stop, i, prev_stop)
            route = path_of_routes(mass, last_route)
            coords = coord_way(mass, route)
            ans.append(Path(start_stop, i, mass, route, coords))

    return ans


def opt_routes(graph, routes, seq_stops):
    """"finding the optimal route between all pairs of stops"""
    try:
        cur = SQLITE_CONNECTION.cursor()

        cur.execute(
            """
            Select count(name) FROM
            sqlite_sequence WHERE name
            = 'way'
            """
        )

        if cur.fetchone()[0] != 0:
            cur.execute("""DROP TABLE way""")

        cur.execute(
            """CREATE TABLE IF NOT EXISTS "way" (
                "_id"   INTEGER NOT NULL,
                "id1"   INTEGER,
                "id2"   INTEGER,
                "route" TEXT,
                "transfer"  TEXT,
                "cords" TEXT,
                PRIMARY KEY("_id" AUTOINCREMENT)
            );"""
        )

        SQLITE_CONNECTION.commit()

        # we run through all the stops in the graph
        # and find all the optimal paths from one stop to another
        for index in range(len(seq_stops)):
            i = seq_stops[index]
            print(i) 
            ways = routes_to_all_stops(i, graph, routes, seq_stops)

            for way in ways:

                if way.get_stop1() != way.get_stop2():

                    list_index = list()
                    for index in range(len(way.get_path_of_routes())):
                        if index == 0:
                            during_route = way.get_path_of_routes()[index]
                            list_index.append(index)
                        else:
                            if way.get_path_of_routes()[index] != during_route:
                                during_route = way.get_path_of_routes()[index]
                                list_index.append(index)

                    transfers = list()
                    for elem in list_index:
                        if elem == 0:
                            transfers.append(
                                [
                                    way.get_path_of_stops()[elem],
                                    way.get_path_of_routes()[elem],
                                ]
                            )
                        else:
                            transfers.append(
                                [
                                    way.get_path_of_stops()[elem - 1],
                                    way.get_path_of_routes()[elem],
                                ]
                            )

                    transfers_str = ""
                    for item in transfers:
                        transfers_str += " ".join(map(str, item))
                        transfers_str += ";\n"
                    transfers_str = transfers_str[: len(transfers_str) - 2]

                    coord_list = ""
                    for array in way.get_path_of_coords():
                        for item in array:
                            coord_list += " ".join(map(str, item))
                            coord_list += "\n"
                    coord_list = coord_list[: len(coord_list) - 1]

                    cur.execute(
                        """INSERT INTO way (id1, id2,
                                            route, transfer, cords)
                            VALUES (?, ?, ?, ?, ?)""",
                        [
                            way.get_stop1(),
                            way.get_stop2(),
                            " ".join(map(str, way.get_path_of_stops())),
                            transfers_str,
                            coord_list,
                        ],
                    )

                    SQLITE_CONNECTION.commit()

    except Exception as exce:  # pylint: disable=broad-except
        print({exce})
        exit()


def test_calculation(routes):
    """testing if calculation is good"""
    try:
        cur = SQLITE_CONNECTION.cursor()

        key_routes = routes.keys()
        for key in key_routes:
            plenty = set(routes[key].get_route())

            cur.execute("SELECT Name_route FROM routesker WHERE _id = ?",
                        [key])
            name_route = cur.fetchone()[0]

            print(f"Route {name_route}, {routes[key].get_route()}")

            for s1_id in plenty:
                for s2_id in plenty:
                    road_info = calculation(key, s1_id, s2_id)

                    cur.execute("SELECT Name_stop FROM stopsker WHERE _id = ?",
                                [s1_id])
                    name_s1 = cur.fetchone()[0]

                    cur.execute("SELECT Name_stop FROM stopsker WHERE _id = ?",
                                [s2_id])

                    print(f"Between {name_s1} and {cur.fetchone()[0]}")
                    print(f"-{road_info.get_length()}")
                    print(f"by {road_info.get_coords()}")

    except Exception as exce:  # pylint: disable=broad-except
        print({exce})
        exit()


def main():
    """the core of the project"""
    try:
        # Connecting to data base
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "example.db")
        global SQLITE_CONNECTION
        SQLITE_CONNECTION = sqlite3.connect(path)
        # graph is a dict, where key is id of the station
        # graph[key] has a type of class edge list
        # routes is a dict, where key is id of the route
        # routes[key] has a type of list
        routes = read_db.read_routes(SQLITE_CONNECTION)
        graph = read_db.read_graph(SQLITE_CONNECTION)
        seq_stops = read_db.sequence_id(SQLITE_CONNECTION, "stopsker")
    except Exception as exce:  # pylint: disable=broad-except
        print({exce})
        exit()
    else:
        # test_calculation(routes)
        opt_routes(graph, routes, seq_stops)
    finally:
        SQLITE_CONNECTION.close()


if __name__ == "__main__":
    main()
