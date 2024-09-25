from flask import Flask, render_template, jsonify, request
from network.graph import NetworkGraph
from algorithms.astar import AStar
from algorithms.qlearning import QLearning
from algorithms.markov_tree import MarkovTree
from simulation.environment import SimulationEnvironment
from utils.metrics import calculate_metrics

app = Flask(__name__)

# Initialize the network graph
network = NetworkGraph()

# Initialize algorithms
astar = AStar(network)
qlearning = QLearning(network)
markov_tree = MarkovTree(network)

# Initialize simulation environment
simulation = SimulationEnvironment(network)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/network', methods=['GET'])
def get_network():
    return jsonify(network.to_dict())

@app.route('/api/path', methods=['POST'])
def find_path():
    data = request.json
    start = data['start']
    end = data['end']
    episodes = data.get('episodes', 100)  # Default to 100 episodes if not provided
    
    # Train Q-learning
    qlearning.train(start, end, episodes)
    
    # Run A* algorithm
    astar_path = astar.find_path(start, end)
    
    # Run Q-learning
    qlearning_path = qlearning.find_path(start, end)
    
    # Run combined A* with Q-learning and Markov Trees
    combined_path = markov_tree.find_path(start, end, astar, qlearning)
    
    # Calculate metrics
    metrics = calculate_metrics(network, astar_path, qlearning_path, combined_path)
    
    return jsonify({
        'astar_path': astar_path,
        'qlearning_path': qlearning_path,
        'combined_path': combined_path,
        'metrics': metrics
    })

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    data = request.json
    iterations = data['iterations']
    
    results = simulation.run(iterations)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
