import sys
# from linked_queue import LinkedQueue


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
        self.edges_list = []
        self.num_vertices = 0
        self.num_edges = 0
        self.undirected = undirected

    def __iter__(self):
        """
        Iterate over the vertex objects in the
        graph, to use syntax: for vertex in graph
        """
        return iter(self.vertices_dict.values())

    def add_vertex(self, key):
        """
        Add a new vertex object to the graph with the given key, increment the count, and return the vertex
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

        # If one of the inputted vertices doesn't exist in the graph
        elif from_vert not in self.vertices_dict or to_vert not in self.vertices_dict:
            print('{} or {} are not in dictionary of vertices'.format(from_vert, to_vert))
            return

        reversed_edge = (to_vert, from_vert, cost)

        # Prevent duplicate edges in simple graph
        if reversed_edge in self.edges_list and self.undirected:
            return

        # Add to_vertex as neighbor to from_vertex
        home_vertex = self.vertices_dict[from_vert]
        home_vertex.add_neighbor(to_vert, cost)
        self.edges_list.append((from_vert, to_vert, cost))
        self.num_edges += 1

        # Add from_vertex as neighbor to to_vertex is it a simple graph
        if self.undirected:
            neighbor_vertex = self.vertices_dict[to_vert]
            neighbor_vertex.add_neighbor(from_vert, cost)

    def get_vertices(self):
        """
        Return all the vertices in the graph
        Runtime: O(n) where n is the number of keys in dictionary
        """
        return self.vertices_dict.keys()

    def get_edges(self):
        """
        Return a set of all unique the edges in the graph
        Runtime: O(1) since the graph store a list of edges
        """
        return self.edges_list

    def read_file(self, text_file):
        """
        Read the given file and add all the vertices and edges
        Runtime: O(n) where n is the number of character in the text file
        """
        with open(text_file, 'r') as file:
            for line in file:
                if len(line) == 2:
                    self.undirected = line[0] == 'D'

                elif line[0] != "(":
                    self._read_vertices(line)

                else:
                    self._read_edge(line)

    def _read_edge(self, text):
        """
        Read the text and add the edge to the graph
        Runtime: O(n) where n is the number of character in the text
        """
        cost = 0
        key = ''
        from_vertex = ''
        to_vertex = ''
        get_from = False
        get_to = False

        for index in range(len(text)):
            char = text[index]

            if char == '(':
                continue

            # Add the remaining key to the cost once the vertices have been found
            elif char == ')' and get_from and get_to and key != '':
                cost = int(key)

            elif char == ')' and not get_to and key != '':
                to_vertex = key
                break

            elif char == ',':

                if not get_from:
                    from_vertex = key
                    get_from = True
                    key = ''

                elif not get_to:
                    to_vertex = key
                    get_to = True
                    key = ''

            else:
                key += char

        self.add_edge(from_vertex, to_vertex, cost)

    def _read_vertices(self, text):
        """
        Read the text and add vertices
        Runtime: O(n) where n is the number of character in the text
        """
        curr_key = ''

        for index in range(len(text) - 1):  # - 1 of the text length to ignore '\n' character

            char = text[index]

            if char == ',':
                self.add_vertex(curr_key)
                curr_key = ''
            else:
                curr_key += char
                if index == len(text) - 2:
                    self.add_vertex(curr_key)

    def depth_first_search(self, start_vertex, target):
        """
        :param start_vertex:
        :param target:
        :return: Boolean value determine if there's a path between the two vertices
        """

        if start_vertex not in self.vertices_dict or target not in self.vertices_dict:
            return False

        visit_dict = {}

        self._dfs(self.vertices_dict[start_vertex], target, None, visit_dict)

        return visit_dict

    def _dfs(self, vertex, target, parent, visit):
        visit[vertex.data] = parent

        for neighbor in vertex.get_neighbors():
            if neighbor not in visit:
                if neighbor == target:
                    visit[neighbor] = vertex
                    return

                self._dfs(self.vertices_dict[neighbor], target, vertex, visit)

    def depth_first_search_iter(self, start_vertex, target):
        """
        :param start_vertex: The string key of the starting vertex
        :param target: The string key of the target vertex as a end point
        :return Boolean,
        """

        if start_vertex not in self.vertices_dict:
            return False, []

        stack = []
        stack.append(self.vertices_dict[start_vertex])
        visited = {}
        visited[start_vertex] = self.vertices_dict[start_vertex]

        while len(stack) != 0:

            vertex = stack.pop()

            if vertex.data == target:
                return True, visited.keys()

            for neighbor in vertex.get_neighbors():
                if neighbor not in visited:
                    visited[neighbor] = self.vertices_dict[neighbor]
                    stack.append(self.vertices_dict[vertex.data])
                    stack.append(self.vertices_dict[neighbor])
                    
                    break

        return False , []


if __name__ == "__main__":
    # Create a graph
    graph = Graph()
    filename = sys.argv[1]
    from_vertex = sys.argv[2]
    to_vertex = sys.argv[3]

    temp_file = "challenge_3_data.txt"

    graph.read_file(filename)

    print("# Vertices: {}".format(graph.num_vertices))
    print("# Edges: {}".format(graph.num_edges))
    print("Edges list: ")
    for edge in graph.get_edges():
        print(edge)

    found, path = graph.depth_first_search_iter('1', '5')
    print(path)
    print("Is the a path from vertex {} to vertex {}: {}".format('1', '5', str(found)))
    if found:
        print('Depth first search path: ' + ', '.join([x for x in path]))

