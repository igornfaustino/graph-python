'''
    Graph Class
'''

import queue
import vertex
import edge


class Graph(object):
    """Class to store a edges's array and a vertex's dictionary"""

    def __init__(self, directed=False):
        """create a object graph
            directed (bool, optional): Defaults to False.
                tells if the graph is directed or not
        """

        self.__edges = {}  # tupla diccionary (no source, no dest)
        self.__adjacent_list = {}
        self.__directed = directed
        self.__distance = {}  # guarda a distancia entre os vertices (bfs)
        self.__predecessors = {}  # predecessores do vertex [bfs]

    # edge function
    # start here
    def add_edge(self, source, destination, label=None, value=None):
        """add a new connetion to the graph

        connects two vertex, if the graph is directed, this connection leaves
        the origin until the destination only.
        if the graph is not directed, the connection will be both the source
        to the destination as the destination to the source

        Args:
            source (Vertex): a source vertex
            destination (Vertex): a destination vertex
            label (stg, optional): Defaults to None. A label to this connection
            value (float, optional): Defaults to None.
                A value to this connection
        """

        # create a new edge
        new_edge = edge.Edge(source, destination, label=label, value=value)

        # test if the destination isn't connected with the source
        if destination not in self.__adjacent_list[source]:
            # insert source
            if new_edge.get_source() not in self.__adjacent_list:
                self.__adjacent_list[new_edge.get_source()] = []
            # insert destination
            if new_edge.get_destination() not in self.__adjacent_list:
                self.__adjacent_list[new_edge.get_destination()] = []

            # insert edge and update adjacent list
            self.__edges[(new_edge.get_source(),
                          new_edge.get_destination())] = new_edge
            self.__adjacent_list[new_edge.get_source()].append(
                new_edge.get_destination())

        # if not directed.. do the same with the other node
        if not self.__directed:
            if source not in self.__adjacent_list[destination]:
                self.__edges[(new_edge.get_destination(),
                              new_edge.get_source())] = new_edge
                self.__adjacent_list[new_edge.get_destination()].append(
                    new_edge.get_source())

    def remove_edge(self, edge_to_remove):
        """remove a connection from the graph

        Args:
            edge_to_remove (Edge): a edge (connection) that you want to remove
        """

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

    def get_all_edges(self):
        """Return all the edges on the graph

        Returns:
            list: return a list with all the edges
        """

        edges = []
        for key in self.__edges:
            if (self.__edges[key] not in edges):
                edges.append(self.__edges[key])

        return edges

    def get_edge_from_souce_destination(self, source, destination):
        """Get a edge from a source and a destination vertex

        Args:
            source (Vertex): a source vertex from the connetion
            destination (Vertex): a destination vertex from the connetion

        Returns:
            Edge: return the egde that maches with the source and destination
                or return None
        """

        if self.__edges[(source, destination)]:
            return self.__edges[(source, destination)]
        return None
    # end here

    # Vertex functions
    # start here
    def add_vertex(self, name, value=None):
        """Add a new vertex to the graph

        Args:
            name (str): a name to the new vertex
            value (float, optional): Defaults to None.
                a value to the new vertex
        """

        for key in self.__adjacent_list:
            if key.get_name() == name:
                return

        new_vertex = vertex.Vertex(name, value=None)
        self.__adjacent_list[new_vertex] = []

    def get_vertex(self, name):
        """get a vertex from the graph

        Args:
            name (str): name of the vertex that you want

        Returns:
            Vertex: return a vertex that matches with the name, or return None
        """

        for key in self.__adjacent_list:
            if key.get_name() == name:
                return key
        return None

    def get_all_vertex(self):
        """Return all the vertex on the graph

        Returns:
            list: return a list with all the vertex
        """

        vertex = []
        for key in self.__adjacent_list:
            vertex.append(key)

        return vertex

    def adjacents_vertex(self, vertex):
        """Get the list of adjacents from a vertex

        Args:
            vertex (vertex): vertex you want to know the adjacent

        Returns:
            list: list of all adjacents of a vertex
        """

        return self.__adjacent_list[vertex]

    def remove_vertex(self, vertex_to_remove):
        """Remove a vertex and all the connections he have

        Args:
            vertex_to_remove (Vertex): vertex you want to remove
        """

        for key in self.__adjacent_list:
            if vertex_to_remove in self.__adjacent_list[key]:
                self.__adjacent_list[key].remove(vertex_to_remove)
        self.__adjacent_list.pop(vertex_to_remove, None)
        for key in list(self.__edges):
            if vertex_to_remove in key:
                self.__edges.pop(key, None)
    # end here

    def print_adjacent_list(self):
        """Print the adjacent list, A.K.A the graph
        """

        print(self.__adjacent_list)

    def get_order(self):
        """Return o order of the graph

        Returns:
            int: return the order of the graph
        """

        return len(self.__adjacent_list)

    def breadth_first_search(self, initial_vertex):
        """Calculate the distance of all vertex from one
        if a vertex can't be reach by the initial vertex,
        the distance will be infinity.. (float("inf"))

        Args:
            initial_vertex (Vetex): calculate the distance of
                all vertices up to this initial vertex

        Returns:
            Dict: dictionaty with the key as the vertex and the body
                the distance from the initial vertex
        """

        # colors:
        #   white: not visited
        #   grey: in the queue
        #   black: nothing more to do
        for key in self.__adjacent_list:
            if key != initial_vertex:
                # set color for all vertices except the initial one to white
                key.set_color(0)
                self.__distance[key] = float("inf")
                self.__predecessors[key] = None

        # if the initial_vertex is not a valid one,
        # all the vertex will have distance equals to infinity
        if not initial_vertex:
            return self.__distance

        initial_vertex.set_color(1)  # inital vertex color to grey
        self.__distance[initial_vertex] = 0
        q = queue.Queue()
        q.put(initial_vertex)  # insert in the queue the initial vertex

        while not q.empty():
            vertex = q.get()

            for v in self.__adjacent_list[vertex]:
                if v.get_color() == 0:  # if a vertex color is white
                    v.set_color(1)  # turn to grey
                    self.__distance[v] = self.__distance[vertex] + 1
                    self.__predecessors[v] = vertex
                    q.put(v)
            vertex.set_color(2)  # color to black

        return self.__distance

    def degree_vertex(self, vertex):
        """Get the degree of a vertex

        Args:
            vertex (Vertex): vertex you want know the degree

        Returns:
            integer: degree of a vertex
        """

        if self.__directed:
            inVertex = 0
            outVertex = len(self.__adjacent_list[vertex])
            for key in self.__adjacent_list:
                if vertex in self.__adjacent_list[key]:
                    inVertex = inVertex + 1
            return outVertex + inVertex
        else:
            return len(self.__adjacent_list[vertex])

    def is_completed(self):
        """tell if a graph is completed or not

        Returns:
            Bool: return if the graph is completed
        """

        for node in self.__adjacent_list:
            for key in self.__adjacent_list:
                if node != key:
                    if node not in self.__adjacent_list[key]:
                        return False
        return True


if __name__ == '__main__':
    graph = Graph()
    graph.add_vertex('teste')
    graph.add_vertex('teste')
    graph.add_vertex('teste2')
    graph.add_edge(graph.get_vertex('teste'), graph.get_vertex('teste2'))
    print(graph.adjacents_vertex(graph.get_vertex('teste')))
    print(graph.get_order())
    print(graph.get_all_edges())
    myEdge = graph.get_edge_from_souce_destination(
        graph.get_vertex('teste'), graph.get_vertex('teste2'))
    graph.remove_vertex(graph.get_vertex('teste'))
    print(graph.get_all_edges())
    graph.print_adjacent_list()
