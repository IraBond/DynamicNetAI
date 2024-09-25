import random
from algorithms.astar import AStar
from algorithms.qlearning import QLearning
from algorithms.markov_tree import MarkovTree

class SimulationEnvironment:
    def __init__(self, graph):
        self.graph = graph
        self.astar = AStar(graph)
        self.qlearning = QLearning(graph)
        self.markov_tree = MarkovTree(graph)

    def run(self, iterations):
        total_path_length = 0
        total_convergence_time = 0
        successful_paths = 0

        for _ in range(iterations):
            start = random.choice(list(self.graph.graph.nodes()))
            goal = random.choice(list(self.graph.graph.nodes()))

            if start != goal:
                path = self.markov_tree.find_path(start, goal, self.astar, self.qlearning)
                if path[-1] == goal:
                    total_path_length += len(path) - 1
                    total_convergence_time += len(path)  # Simplified measure of convergence time
                    successful_paths += 1

        avg_path_length = total_path_length / successful_paths if successful_paths > 0 else 0
        avg_convergence_time = total_convergence_time / successful_paths if successful_paths > 0 else 0
        success_rate = successful_paths / iterations

        return {
            'avg_path_length': avg_path_length,
            'avg_convergence_time': avg_convergence_time,
            'success_rate': success_rate
        }
