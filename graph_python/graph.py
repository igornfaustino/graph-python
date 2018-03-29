'''
    Graph Class
'''


class Graph(object):
    "Class to store a edges's array and a vertex's dictionary"

    def __init__(self, directed=False):
        self.__edges = {}  # tupla diccionary (no source, no dest)
        self.__adjacent_list = {}
        self.__directed = directed

    def add_edge(self, edge):
        "Add a new edge to the graph"

        # insert source
        if edge.get_source() not in self.__adjacent_list:
            self.__adjacent_list[edge.get_source()] = []
        # insert destination
        if edge.get_destination() not in self.__adjacent_list:
            self.__adjacent_list[edge.get_destination()] = []

        # insert edge and update adjacent list
        self.__edges[(edge.get_source(), edge.get_destination())] = edge
        self.__adjacent_list[edge.get_source()].append(edge.get_destination())

        # if not directed.. do the same with the other node
        if not self.directed:
            self.__edges[(edge.get_destination(), edge.get_source())] = edge
            self.__adjacent_list[edge.get_destination()].append(
                edge.get_source())

    def remove_edge(self, edge_to_remove):
        "Remove a edge from the graph"

        # Remove vertex from the adjacent_list
        self.__adjacent_list[edge_to_remove.get_source()].remove(
            edge_to_remove.get_destination())
        self.__edges.pop(
            (edge_to_remove.get_source(), edge_to_remove.get_destination())
        )
        if not self.__directed:
            self.__adjacent_list[edge_to_remove.get_destination()].remove(
                edge_to_remove.get_source())
            self.__edges.pop(
                (edge_to_remove.get_destination(), edge_to_remove.get_source())
            )

    def add_vertex(self, new_vertex):
        "Add a new vertex to the graph"

        self.__adjacent_list[new_vertex] = []

    def remove_vertex(self, vertex_to_remove):
        "Remove a vertex and they edges"

        for key in self.__adjacent_list:
            if vertex_to_remove in self.__adjacent_list[key]:
                self.__adjacent_list[key].remove(vertex_to_remove)
        self.__adjacent_list.pop(vertex_to_remove, None)
        for key in self.__edges:
            if vertex_to_remove in key:
                self.__edges.pop(key, None)

    def get_edge_from_souce_destination(self, source, destination):
        "Get a edge from a source and a destination node"

        return self.__edges[(source, destination)]

    def print_adjacent_list(self):
        "Print the adjacent list"

        print(self.__adjacent_list)

    def get_order(self):
        "Return o order of the graph"

        return len(self.__adjacent_list)

    def get_vertex(self):
        "Return all the vertex on the graph"

        vertex = []
        for key in self.__adjacent_list:
            vertex.append(key)

        return vertex

    def get_edges(self):
        "Return all the edges on the graph"

        edges = []
        for key in self.__edges:
            if (self.__edges[key] not in edges):
                edges.append(self.__edges[key])

        return edges
