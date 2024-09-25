import networkx as nx
import random

class NetworkGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.generate_random_graph()

    def generate_random_graph(self, num_nodes=10, num_edges=15):
        for i in range(num_nodes):
            self.graph.add_node(i, pos=(random.random(), random.random()))

        while self.graph.number_of_edges() < num_edges:
            a = random.randint(0, num_nodes - 1)
            b = random.randint(0, num_nodes - 1)
            if a != b and not self.graph.has_edge(a, b):
                weight = random.uniform(1, 10)
                self.graph.add_edge(a, b, weight=weight)

    def neighbors(self, node):
        return list(self.graph.neighbors(node))

    def cost(self, a, b):
        return self.graph[a][b]['weight']

    def get_node_pos(self, node):
        return self.graph.nodes[node]['pos']

    def to_dict(self):
        return {
            'nodes': [{'id': node, 'label': str(node)} for node in self.graph.nodes()],
            'edges': [{'from': u, 'to': v, 'label': str(round(d['weight'], 2))} for u, v, d in self.graph.edges(data=True)]
        }
