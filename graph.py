from linked_queue import LinkedQueue

""" 
Vertex Class
A helper class for the Graph class that defines vertices and vertex neighbors.
"""


class Vertex(object):

    def __init__(self, vertex):
        """
        Initialize a vertex and its neighbors
        neighbors: set of vertices adjacent to self,
        stored in a dictionary with key = vertex,
        value = weight of edge between self and neighbor.
        """
        self.id = vertex
        self.neighbors = {}

    def add_neighbor(self, vertex, weight=0):
        """
        Add a neighbor along a weighted edge
        Runtime: O(1)
        """
        self.neighbors[vertex] = weight

    def __str__(self):
        """output the list of neighbors of this vertex"""
        return str(self.id) + " adjacent to " + str([x for x in self.neighbors.keys()])

    def get_neighbors(self):
        """
        Return the neighbors of this vertex
        Runtime: O(n) where n is the number of neighbors
        """
        return self.neighbors.keys()

    def get_id(self):
        """
        Return the id of this vertex
        Runtime: O(1)
        """
        return self.id

    def get_edge_weight(self, vertex):
        """
        Return the weight of this edge
        Runtime: O(1)
        """
        return self.neighbors[vertex] if vertex in self.neighbors else None


# This is an undirected graph

class Graph:
    def __init__(self):
        """ initializes a graph object with an empty dictionary."""
        self.vertices_dict = {}
        self.num_vertices = 0
        self.total_edges = 0  # Number of all unique edges

    def __iter__(self):
        """iterate over the vertex objects in the
        graph, to use sytax: for v in g"""
        return iter(self.vertices_dict.values())

    def add_vertex(self, key):
        """
        Add a new vertex object to the graph with the given key and return the vertex
        Runtime: O(1)* since the graph store the vertices as a dictionary
        """

        if key in self.vertices_dict:
            print("Vertex: " + key + " already exist")
            return

        new_vertex = Vertex(key)

        self.vertices_dict[key] = new_vertex
        self.num_vertices += 1

        return new_vertex

    def get_vertex(self, key):
        """
        Return the vertex if it exists
        Runtime: O(1) since the graph store the vertices as a dictionary
        """
        return self.vertices_dict[key] if key in self.vertices_dict else None

    def add_edge(self, from_vert, to_vert, cost=0):
        """
        Add an edge from one to another vertex with a cost
        Runtime: O(1) since the graph store vertices as a dictionary and
                the Vertex class store neighbors in a dictionary.
        """
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
        """
        Return all the vertices in the graph
        Runtime: O(n) where n is the number of keys in dictionary
        """
        return self.vertices_dict.keys()

    def get_edges(self):
        """
        Return a set of all unique the edges in the graph
        Runtime: O(V*E) where V is the number of vertices and E is the number of edges for a vertex
        """
        # Store a tuple ( from_vertex, to_vertex, weight)
        unique_edges = set()

        for vertex in self:
            for neighbor in vertex.get_neighbors():
                curr_edge = (vertex.id, neighbor, vertex.neighbors[neighbor])
                reversed_edge = (neighbor, vertex.id, vertex.neighbors[neighbor])

                if reversed_edge in unique_edges:
                    pass
                else:
                    unique_edges.add(curr_edge)

        return unique_edges

    def is_empty(self):
        """Return true if the graph doesn't have any vertices"""
        return len(self.get_vertices()) is 0

    def breadth_first_search_length(self, vertex, length):
        """
        Perform breadth first search and return all nodes that met
        the require length from the inputted vertex.
        Runtime: O(V + E)
        """
        if vertex not in self.vertices_dict:
            return

        vertices = []

        # Create queue to store nodes not yet traversed in level-order
        queue = LinkedQueue()

        # Enqueue given starting node and a length of 0
        queue.enqueue((self.vertices_dict[vertex], 0))  # Queue = [(vertex, length), ... ]

        visited_dict = {self.vertices_dict[vertex].id: 0}  # A dictionary to keep track of the visited vertices

        while not queue.is_empty():

            value = queue.dequeue()  # curr_vertex = (Vertex, length)

            curr_vertex = value[0]
            vertex_length = value[1]

            # Fast break if there current vertex's length is bigger than the target
            if vertex_length > length:
                break

            for neighbor in curr_vertex.get_neighbors():
                if neighbor not in visited_dict:

                    if vertex_length + 1 == length:  # If the neighbor met the require length
                        vertices.append(self.vertices_dict[neighbor])

                    # Enqueue the neighbor with an incremented length
                    new_value = (self.vertices_dict[neighbor], vertex_length + 1)
                    queue.enqueue(new_value)

                    # Add the neighbor to the visited dictionary
                    visited_dict[new_value[0].id] = new_value[1]

        return vertices

    def find_path_bfs(self, from_vert, to_vert):  # Algorithm from Wikipedia and The Coding Train help understand it
        """
        Return a list of vertex that represent a path from one vertex to another
        Runtime: O(V + E)
        """
        if from_vert not in self.vertices_dict or to_vert not in self.vertices_dict:
            print('{} or {} are not in dictionary of vertices'.format(from_vert, to_vert))
            return

        elif from_vert == to_vert:
            print('Both from vertex and to vertex are the same')
            return [self.vertices_dict[from_vert]]

        queue = LinkedQueue()
        queue.enqueue((self.vertices_dict[from_vert], 0))   # Enqueue the from vertex

        # A dictionary to keep track of the visited vertices along with their predecessor
        visited_dict = {self.vertices_dict[from_vert].id: None}

        while not queue.is_empty():

            value = queue.dequeue()  # curr_vertex = (Vertex, length)

            curr_vertex = value[0]

            if curr_vertex.id == to_vert:
                break

            for neighbor in curr_vertex.get_neighbors():
                if neighbor not in visited_dict:
                    # Enqueue the neighbor with an incremented length
                    new_value = (self.vertices_dict[neighbor], curr_vertex)
                    queue.enqueue(new_value)

                    # Add the neighbor to the visited dictionary
                    visited_dict[new_value[0].id] = new_value[1]

        # If unable to find the path
        if to_vert not in visited_dict:
            return

        path = [self.vertices_dict[to_vert]]

        next_vertex = visited_dict[to_vert]

        while next_vertex is not None:
            path.append(next_vertex)
            next_vertex = visited_dict[next_vertex.id]

        path.reverse()

        return path

# Driver code


if __name__ == "__main__":

    # Challenge 1: Create the graph

    graph = Graph()

    # Add your friends
    graph.add_vertex("Friend A")
    graph.add_vertex("Friend B")
    graph.add_vertex("Friend C")
    graph.add_vertex("Friend D")
    graph.add_vertex("Friend E")
    graph.add_vertex("Friend F")

    # Add connections (non weighted edges for now)
    graph.add_edge("Friend A", "Friend B")
    graph.add_edge("Friend A", "Friend C")
    graph.add_edge("Friend B", "Friend C")
    graph.add_edge("Friend C", "Friend D")
    graph.add_edge("Friend C", "Friend E")
    graph.add_edge("Friend C", "Friend F")
    graph.add_edge("Friend A", "Friend F")
    # Challenge 1: Output the vertices & edges
    #
    # print("The vertices are: ", graph.get_vertices(), "\n")
    #
    # print("The edges are: ")
    # for edge in graph.get_edges():
    #     print(edge)

    # # Chapter 3 BFS
    # print("Vertices that are 2 away from Vertex friend A are:")
    # array = graph.breadth_first_search_length("Friend A", 2)
    # for vertex in array:
    #     print(vertex.id)

    # Chapter 4 Find path
    print(', '.join([x.id for x in graph.find_path_bfs('Friend A', "Friend D")]))
