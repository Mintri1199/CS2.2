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
    pass