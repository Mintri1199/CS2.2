# Read line
# If line only contain G then pass
#   Any lines follow it that doesn't start with a open parenthesis
#   are vertices.
# If a line start with a open parenthesis then its an edge
#   Continue until the file has been read
import sys

class Vertex(object):

    def __init__(self, data):
        """Initialize vertex with data and neighbors
        neighbors: set of vertices adjacent to self,
        stored in a dictionary with key = vertex,
        value = weight of edge between self and neighbor."""
        self.data = data
        self.neighbors = {}

    def add_neighbor(self, vertex, weight=0):
        """add a neighbor along a weighted edge"""
        self.neighbors[vertex] = weight

    def __str__(self):
        """output the list of neighbors of this vertex"""
        return str(self.data) + " adjacent to:\n " + str([x + '\n' for x in self.neighbors.keys()])

    def get_neighbors(self):
        """return the neighbors of this vertex"""
        return self.neighbors.keys()

    def get_id(self):
        """return the id of this vertex"""
        return self.data

    def get_edge_weight(self, vertex):
        """return the weight of this edge"""
        return self.neighbors[vertex] if vertex in self.neighbors else None


class Graph:

    def __init__(self, undirected=False):
        self.vertices_dict = {}
        self.num_vertices = 0
        self.num_edges = 0
        self.undirected = undirected

    def __iter__(self):
        """iterate over the vertex objects in the
        graph, to use sytax: for v in g"""
        return iter(self.vertices_dict.values())

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

    def add_edge(self, from_vert, to_vert, cost=0):
        """add an edge from one to another vertex with a cost"""
        # Handle bad inputs and edge cases
        if from_vert == to_vert:
            print('Both from vertex and to vertex are the same')
            return

        elif from_vert not in self.vertices_dict or to_vert not in self.vertices_dict:
            print('{} or {} are not in dictionary of vertices'.format(from_vert, to_vert))
            return

        home_vertex = self.vertices_dict[from_vert]
        home_vertex.add_neighbor(to_vert, cost)
        self.num_edges += 1

        if self.undirected:
            dest_vertex = self.vertices_dict[from_vert]
            dest_vertex.add_neighbor(from_vert, cost)
            self.num_edges += 1

    def get_vertices(self):
        """return all the vertices in the graph"""
        return self.vertices_dict.keys()

    def get_edges(self):
        """ Return a set of all unique the edges in the graph"""
        # Store a tuple ( from_vertex, to_vertex, weight)
        unique_edges = set()

        for vertex in self:
            for neighbor in vertex.get_neighbors():
                curr_edge = (vertex.id, neighbor, vertex.neighbors[neighbor])
                unique_edges.add(curr_edge)

        return unique_edges

    def read_file(self, text_file):
        """Read the given file and add all the vertices and edges"""
        with open(text_file, 'r') as file:
            for line in file:
                if len(line) == 2:
                    self.undirected = line == 'D\n'

                elif line[0] != "(":
                    self._read_vertices(line)

                else:
                    self._read_edge(line)

    def _read_edge(self, text):
        """Read the text and add the edge to the graph"""
        from_vertex = ''
        to_vertex = ''

    def _read_vertices(self, text):
        """Read the text and add vertices"""
        curr_key = ''
        for index in range(len(text) - 1):

            char = text[index]

            if char == ',':
                self.add_vertex(curr_key)
                curr_key = ''
            else:
                curr_key += char
                if index == len(text) - 2:
                    self.add_vertex(curr_key)


if __name__ == "__main__":
    # Create a graph
    graph = Graph()

    # filename = sys.argv[1]

    temp_file = "graph_data.txt"

    graph.read_file(temp_file)
    
    print(graph.get_vertices())
    print(graph.num_vertices)  # should print 0




