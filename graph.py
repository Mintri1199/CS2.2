""" Vertex Class
A helper class for the Graph class that defines vertices and vertex neighbors.
"""


class Vertex(object):

    def __init__(self, vertex):
        """initialize a vertex and its neighbors
        neighbors: set of vertices adjacent to self,
        stored in a dictionary with key = vertex,
        value = weight of edge between self and neighbor.
        """
        self.id = vertex
        self.neighbors = {}

    def add_neighbor(self, vertex, weight=0):
        """add a neighbor along a weighted edge"""
        if vertex in self.neighbors:
            return
        else:
            self.neighbors[vertex] = weight

    def __str__(self):
        """output the list of neighbors of this vertex"""
        return str(self.id) + " adjacent to " + str([x for x in self.neighbors.keys()])

    def get_neighbors(self):
        """return the neighbors of this vertex"""
        return self.neighbors.keys()

    def get_id(self):
        """return the id of this vertex"""
        return self.id

    def get_edge_weight(self, vertex):
        """return the weight of this edge"""
        return self.neighbors[vertex]


""" Graph Class
A class demonstrating the essential
facts and functionalities of graphs.
"""


class Graph:
    def __init__(self):
        """ initializes a graph object with an empty dictionary."""
        self.vertices_dict = {}
        self.num_vertices = 0

    def add_vertex(self, key):
        """add a new vertex object to the graph with
        the given key and return the vertex """

        self.num_vertices += 1

        if key in self.vertices_dict:
            print("Vertex: " + key + " already exist")
            return

        new_vertex = Vertex(key)

        self.vertices_dict[key] = new_vertex

        return new_vertex

    def get_vertex(self, key):
        """return the vertex if it exists"""
        return self.vertices_dict[key] if key in self.vertices_dict[key] else None

    def add_edge(self, from_vert, to_vert, cost=0):
        """add an edge from one to another vertex with a cost"""
        assert from_vert != to_vert, 'Both from vertex and to vertex are the same'
        assert from_vert in self.vertices_dict, 'From vertex is not in dictionary of vertices'
        assert to_vert in self.vertices_dict, 'To vertex is not in dictionary of vertices'

        home_vertex = self.vertices_dict[from_vert]
        home_vertex.add_neighbor(to_vert, cost)

    def get_vertices(self):
        """return all the vertices in the graph"""
        return self.vertices_dict.keys()

    def __iter__(self):
        """iterate over the vertex objects in the
        graph, to use sytax: for v in g"""
        return iter(self.vertices_dict.values())


# Driver code


if __name__ == "__main__":

    # Challenge 1: Create the graph

    graph = Graph()

    # Add your friends
    graph.add_vertex("Friend 1")
    graph.add_vertex("Friend 2")
    graph.add_vertex("Friend 3")

    # ...  add all 10 including you ...

    # Add connections (non weighted edges for now)
    graph.add_edge("Friend 1", "Friend 2")
    graph.add_edge("Friend 2", "Friend 3")

    # Challenge 1: Output the vertices & edges
    # Print vertices
    print("The vertices are: ", graph.get_vertices(), "\n")

    print("The edges are: ")
    for vertex in graph:
        for neighbor in vertex.get_neighbors():
            print("( {} , {} )".format(vertex.get_id(), neighbor))
