def calculate_metrics(graph, astar_path, qlearning_path, combined_path):
    astar_cost = sum(graph.cost(astar_path[i], astar_path[i+1]) for i in range(len(astar_path)-1))
    qlearning_cost = sum(graph.cost(qlearning_path[i], qlearning_path[i+1]) for i in range(len(qlearning_path)-1))
    combined_cost = sum(graph.cost(combined_path[i], combined_path[i+1]) for i in range(len(combined_path)-1))

    convergence_speed = len(combined_path) / ((len(astar_path) + len(qlearning_path)) / 2)
    path_efficiency = combined_cost / ((astar_cost + qlearning_cost) / 2)
    adaptability = abs(len(combined_path) - len(astar_path)) / len(astar_path)

    return {
        'convergence_speed': convergence_speed,
        'path_efficiency': path_efficiency,
        'adaptability': adaptability
    }
