from graph import Graph, Vertex
import unittest


class VertexTests(unittest.TestCase):

    def setUp(self):
        self.vertex = Vertex("A")

    def test_init(self):
        assert self.vertex.id is 'A'
        assert not self.vertex.neighbors

    def test_add_neighbor(self):
        # Adding a neighbor
        neighbor_one = "B"
        self.vertex.add_neighbor(neighbor_one)
        assert len(self.vertex.get_neighbors()) is 1
        assert neighbor_one in self.vertex.neighbors
        assert self.vertex.get_edge_weight(neighbor_one) is 0

        # Adding another neighbor
        neighbor_two = 'C'
        self.vertex.add_neighbor(neighbor_two, 4)
        assert len(self.vertex.get_neighbors()) is 2
        assert neighbor_two in self.vertex.neighbors
        assert self.vertex.get_edge_weight(neighbor_two) is 4

        # Handling duplicate vertex
        self.vertex.add_neighbor(neighbor_one, 8)
        assert len(self.vertex.get_neighbors()) is 2
        assert neighbor_one in self.vertex.neighbors
        assert self.vertex.get_edge_weight(neighbor_one) is 8
        
    def test_negatives(self):
        # Requesting a weight from a non existing edge
        assert self.vertex.get_edge_weight("B") is None


class GraphTests(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_init(self):
        assert not self.graph.vertices_dict
        assert self.graph.num_vertices is 0

    def test_add_vertex(self):
        # Add one vertex
        self.graph.add_vertex("B")
        assert self.graph.num_vertices is 1
        assert len(self.graph.vertices_dict.keys()) is 1
        assert "B" in self.graph.vertices_dict

        # Add another vertex
        self.graph.add_vertex("A")
        assert self.graph.num_vertices is 2
        assert len(self.graph.vertices_dict.keys()) is 2
        assert "A" in self.graph.vertices_dict

        # Should avoid adding duplicate
        self.graph.add_vertex("B")
        assert self.graph.num_vertices is 2
        assert len(self.graph.vertices_dict.keys()) is 2

    def test_get_vertex(self):
        # Add vertex
        self.graph.add_vertex("B")

        # Find the newly added vertex
        found_vertex = self.graph.get_vertex("B")
        assert found_vertex.id is "B"

        # Test for non existing vertex
        assert self.graph.get_vertex("C") is None

    def test_add_edge(self):
        # Populate the graph with vertices A, B, C, D, E, F, G
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_vertex("D")
        self.graph.add_vertex("E")
        self.graph.add_vertex("F")
        self.graph.add_vertex("G")

        # Add edge from A to B with the cost of 10
        self.graph.add_edge("A", "B", 10)
        vertex_a = self.graph.get_vertex("A")
        vertex_b = self.graph.get_vertex("B")
        vertex_c = self.graph.get_vertex("C")

        # Vertex A should have an edge to vertex B with the cost of 10
        assert "B" in vertex_a.neighbors
        assert vertex_a.get_edge_weight("B") is 10
        assert "A" in vertex_b.neighbors
        assert vertex_b.get_edge_weight("A") is 10

        self.graph.add_edge("A", "C", 5)
        self.graph.add_edge("B", "C", 10)

        assert "C" in vertex_a.neighbors and "C" in vertex_b.neighbors
        assert vertex_a.get_edge_weight("C") is 5
        assert vertex_b.get_edge_weight("C") is 10
        assert vertex_c.get_edge_weight("A") is 5 and vertex_c.get_edge_weight("B") is 10

        # Test for bad inputs
        assert self.graph.add_edge("O", "B", 12) is None

        # Made vertex A have 5 edges / neighbor
        self.graph.add_edge("A", "D", 11)
        self.graph.add_edge("A", "E", 12)
        self.graph.add_edge("A", "F", 45)
        # Vertex A neighbors = [B, C, D, E, F]
        # Graph should refuse add an edge from A to G
        assert self.graph.add_edge("A", "G") is None
        assert vertex_a.neighbors["F"] is 45
        assert "G" not in vertex_a.neighbors

    def test_get_verticles(self):
        # Populate the graph with vertices A, B, C
        self.graph.add_vertex("B")
        self.graph.add_vertex("A")
        self.graph.add_vertex("C")

        vertices_list = self.graph.get_vertices()
        assert list
        assert len(vertices_list) is 3
        assert "A" in vertices_list
        assert "B" in vertices_list
        assert "C" in vertices_list

    def test_get_edges(self):
        # Populate the graph with vertices A, B, C
        self.graph.add_vertex("B")
        self.graph.add_vertex("A")
        self.graph.add_vertex("C")

        self.graph.add_edge("A", "B", 10)
        self.graph.add_edge("A", "C", 5)
        self.graph.add_edge("B", "C", 10)

        edges_set = self.graph.get_edges()

        assert len(edges_set) is 3
        assert ("A", "B", 10) in edges_set or ("B", "A", 10)
        assert ("A", "C", 5) in edges_set or ("C", "A", 5) in edges_set
        assert ("B", "C", 10) in edges_set or ("C", "B", 10) in edges_set

    def test_BFS(self):
        # Populate the graph with vertices
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_vertex("D")
        self.graph.add_vertex("E")
        self.graph.add_vertex("F")
        self.graph.add_vertex("G")

        # Add connections (non weighted edges for now)
        self.graph.add_edge("A", "B")  # (A -> B)
        self.graph.add_edge("A", "C")  # (A -> C)
        self.graph.add_edge("B", "C")  # (B -> C)
        self.graph.add_edge("C", "D")  # (C -> D)
        self.graph.add_edge("C", "E")  # (C -> E)
        self.graph.add_edge("C", "F")  # (C -> F)
        self.graph.add_edge("A", "F")  # (A -> F)

        # Bad input, starting vertex doesn't exist
        value = self.graph.breadth_first_search(' R', 1)
        assert value is None

        # Inputting negative length
        negative_length = self.graph.breadth_first_search(' A', -1)
        assert negative_length is None

        # Good input, starting vertex is A and find nodes that are 2 length away
        vertex_array = self.graph.breadth_first_search("A", 2)
        assert len(vertex_array) is 2
        for vertex in vertex_array:
            assert vertex.id is 'D' or vertex.id is 'E'

        # Edge input, too big of a length
        too_big = self.graph.breadth_first_search('A', 3)
        assert len(too_big) is 0