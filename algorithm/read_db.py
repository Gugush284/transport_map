"""
Модуль os необходим для поиска абсолютного пути
до файла с базой данных
Модуль sqlite3 необходим для работы с базой данных
"""
import os
import sqlite3

class Edge:
    """
    Класс Edge содержит в себе два поля:
        id маршрта
        pointer - list индексов, отражающих позицию в маршруте
    Класс является элементом словаря graph
    """
    def __init__(self, route, pointer):
        self.route = route
        self.pointer = pointer

    def get_pointer(self):
        """Возвращаем pointer"""
        return self.pointer

    def get_route_name(self):
        """Возвращаем id маршрта"""
        return self.route


class Rinfo:
    """
    Класс Rinfo содержит в себе два поля:
        route - list, содержащий последовательность остановок в маршруте
        ring - флаг, указывающий на кольцевой маршрут
    Класс является элементом словаря routes
    """
    def __init__(self, route, ring):
        self.route = route
        self.ring = ring

    def get_ring(self):
        """Возвращаем ring"""
        return self.ring

    def get_route(self):
        """Возвращаем route"""
        return self.route

def read_routes(sqlite_connection):
    """
    Функция читает маршруты из базы данных и
    заполняет словарь routes классами Rinfo
    Ключом словаря является id маршрута
    """
    routes = dict()

    try:
        cur = sqlite_connection.cursor()

        # Look for amount of routes and write to
        # a variable named "amount"
        cur.execute("SELECT _id FROM routesker")
        amount = cur.fetchall()

        for num in amount:
            # num[0] is id of route
            id_route = num[0]

            # read chain of stops id for current stop
            cur.execute("SELECT chain_stops FROM routesker WHERE _id = ?",
                [id_route])
            chain = cur.fetchone()[0].split()

            # change type of elem of chain
            chain_int = list()
            for elem in chain:
                chain_int.append(int(elem))

            # finding out if the route is circular
            cur.execute("SELECT Ring FROM routesker WHERE _id = ?",
                [id_route])

            routes[int(id_route)] = Rinfo(chain_int, cur.fetchone()[0])

    except Exception as exp:
        print({exp})
        sqlite_connection.close()
        exit()
    else:
        return routes


def read_graph(sqlite_connection):
    """
    Функция читает остановки из базы данных и
    заполняет словарь graph классами Edge
    Ключом словаря является id остановки
    """
    graph = dict()

    try:
        cur = sqlite_connection.cursor()

        # Look for amount of stops and write to
        # a variable named "amount"
        cur.execute("SELECT _id FROM stopsker")
        amount = cur.fetchall()

        for num in amount:
            # id of current stop
            id_stop = num[0]

            graph[id_stop] = list()


            cur.execute("SELECT Route_Num FROM stopsker WHERE _id = ?",
                [id_stop])

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
                    if int(stop) == id_stop:
                        pointer.append(counter)
                    counter += 1
                graph[id_stop].append(Edge(int(route), pointer))

    except Exception as exp:
        print({exp})
        sqlite_connection.close()
        exit()
    else:
        return graph

def test_print(graph, routes, sqlite_connection, seq_stops):
    """
    Функция для тестирования кода. Запускается тогда, когда
    __name__ == __main__. Печатает Остановки, их позиции во
    всех маршрутахб маршруты, id всех остановок
    """
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
                    f"{name} (id = {key}) in {cur.fetchone()[0]} by",
                    f"{elem.get_pointer()} positions: {routes[elem.get_route_name()].get_route()}"
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
                f"{route_name}",
                f" {cur.fetchone()[0]}: {routes[key].get_route()}"
            )

        print("\n", end="")
        print(seq_stops)
        print("\n", end="")

    except Exception as exp:
        print({exp})
        exit()

def sequence_id(sqlite_connection):
    """
    Функция возвращает список из id всех остановок
    """
    try:
        cur = sqlite_connection.cursor()

        cur.execute("SELECT _id FROM stopsker")

        seq = list()
        for elem in cur.fetchall():
            seq.append(int(elem[0]))

    except Exception as exp:
        print({exp})
        exit()
    else:
        return seq

def main():
    """
    Главная функция
    Получаем путь до базы данных
    и вызываем остальные функции
    """
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

    except Exception as exp:
        print({exp})
        exit()
    else:
        test_print(graph, routes, sqlite_connection, seq_stops)
    finally:
        sqlite_connection.close()

if __name__ == "__main__":
    main()
    