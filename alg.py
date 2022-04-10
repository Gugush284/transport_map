def read_base(fr):
    line = fr.readline()
    line = line.rstrip('\n\r')
    return line

def Add_id (ID, name, Id):
    ID[Id] = name
    return ID

def Add_graph (graph, ID, edges):
    graph[ID] = edges
    return graph

class edge:
    
    # Конструктор
    def __init__(self, Id, route):         
        self.Id = Id
        self.route = route

    def get_Id (self):
        return self.Id

    def get_route (self):
        return self.route

if __name__ == "__main__":
    file = open('example.txt','r')
    graph = dict()
    ID = dict()

    flag = True
    while flag:

        file_line = read_base(file)
        name_id =  file_line.split(' ')
        name = str(name_id[0])
        Id = int(name_id[1])
        ID = Add_id(ID, name, Id)

        edges = list()

        file_line = read_base(file)
        while (file_line != "!") and flag:
            if not file_line:
                flag = False
            else:
                flist = file_line.split(' ')
                Id_n = int(flist[0])
                bus_route = str(flist[1])
                elem_edge = edge(Id_n, bus_route)
                edges.append(elem_edge)

            file_line = read_base(file)
        
        graph = Add_graph (graph, Id, edges)
    
    for key in graph.keys():
        for x in range(len(graph[key])):
            print("FROM {0} TO {1} BY {2}".format(ID[key], ID[((graph[key])[x]).get_Id()], ((graph[key])[x]).get_route()))