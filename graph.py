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
        return self.neighbors[vertex] if vertex in self.neighbors else None


# This is an undirected graph

class Graph:
    def __init__(self):
        """ initializes a graph object with an empty dictionary."""
        self.vertices_dict = {}
        self.num_vertices = 0
        self.total_edges = 0  # Number of all unique edges

    def add_vertex(self, key):
        """add a new vertex object to the graph with
        the given key and return the vertex """

        if key in self.vertices_dict:
            print("Vertex: " + key + " already exist")
            return

        new_vertex = Vertex(key)

        self.vertices_dict[key] = new_vertex
        self.num_vertices += 1

        return new_vertex

    def get_vertex(self, key):
        """return the vertex if it exists"""
        return self.vertices_dict[key] if key in self.vertices_dict else None

    def add_edge(self, from_vert, to_vert, cost=0):
        """add an edge from one to another vertex with a cost"""
        # Handle bad inputs and edge cases
        if from_vert == to_vert:
            print('Both from vertex and to vertex are the same')
            return

        elif from_vert not in self.vertices_dict or to_vert not in self.vertices_dict:
            print('{} or {} are not in dictionary of vertices'.format(from_vert, to_vert))
            return

        elif len(self.vertices_dict[from_vert].get_neighbors()) >= 5:
            print('{} is too popular already'.format(from_vert))
            return

        elif len(self.vertices_dict[to_vert].get_neighbors()) >= 5:
            print('{} is too popular already'.format(to_vert))
            return

        home_vertex = self.vertices_dict[from_vert]
        home_vertex.add_neighbor(to_vert, cost)

        neighbor_vertex = self.vertices_dict[to_vert]
        neighbor_vertex.add_neighbor(from_vert, cost)

        self.total_edges += 1

    def get_vertices(self):
        """return all the vertices in the graph"""
        return self.vertices_dict.keys()

    def get_edges(self):
        """ Return a set of all unique the edges in the graph"""
        # Store a tuple ( from_vertex, to_vertex, weight)
        unique_edges = set()

        for vertex in self.get_vertices():
            curr_vertex = self.vertices_dict[vertex]
            for neighbor in curr_vertex.get_neighbors():

                edge = (vertex, neighbor, curr_vertex.neighbors[neighbor])
                reversed_edge = (neighbor, vertex, curr_vertex.neighbors[neighbor])

                if reversed_edge in unique_edges:
                    pass
                else:
                    unique_edges.add(edge)

        return unique_edges

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

    # Add connections (non weighted edges for now)
    graph.add_edge("Friend 1", "Friend 2")
    graph.add_edge("Friend 2", "Friend 3")

    # Challenge 1: Output the vertices & edges
    # Print vertices
    print("The vertices are: ", graph.get_vertices(), "\n")

    print("The edges are: ")
    for edge in graph.get_edges():
        print(edge)
