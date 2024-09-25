let network;

document.addEventListener('DOMContentLoaded', () => {
    fetchNetwork();
    document.getElementById('find-path').addEventListener('click', findPath);
    document.getElementById('run-simulation').addEventListener('click', runSimulation);
});

async function fetchNetwork() {
    try {
        const response = await fetch('/api/network');
        const data = await response.json();
        drawNetwork(data);
    } catch (error) {
        console.error('Error fetching network data:', error);
    }
}

function drawNetwork(data) {
    const container = document.getElementById('network-container');
    if (!container) {
        console.error('Network container not found');
        return;
    }
    const options = {
        nodes: {
            shape: 'circle',
        },
        edges: {
            smooth: false,
        },
        physics: {
            enabled: false,
        },
    };
    network = new vis.Network(container, data, options);
}

async function findPath() {
    const start = document.getElementById('start-node').value;
    const end = document.getElementById('end-node').value;

    if (!start || !end) {
        alert('Please enter both start and end nodes');
        return;
    }

    try {
        const response = await fetch('/api/path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ start, end }),
        });
        const data = await response.json();

        highlightPath(data.astar_path, '#ff0000');
        highlightPath(data.qlearning_path, '#00ff00');
        highlightPath(data.combined_path, '#0000ff');

        displayMetrics(data.metrics);
    } catch (error) {
        console.error('Error finding path:', error);
    }
}

function highlightPath(path, color) {
    if (!network || !path) return;
    for (let i = 0; i < path.length - 1; i++) {
        network.updateEdge(path[i], path[i+1], { color: color });
    }
}

function displayMetrics(metrics) {
    const metricsDiv = document.getElementById('metrics');
    if (!metricsDiv) return;
    metricsDiv.innerHTML = `
        <h3>Performance Metrics</h3>
        <p>Convergence Speed: ${metrics.convergence_speed.toFixed(2)}</p>
        <p>Path Efficiency: ${metrics.path_efficiency.toFixed(2)}</p>
        <p>Adaptability: ${metrics.adaptability.toFixed(2)}</p>
    `;
}

async function runSimulation() {
    const iterations = document.getElementById('simulation-iterations').value;

    if (!iterations || isNaN(iterations)) {
        alert('Please enter a valid number of iterations');
        return;
    }

    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ iterations: parseInt(iterations) }),
        });
        const data = await response.json();

        displaySimulationResults(data);
    } catch (error) {
        console.error('Error running simulation:', error);
    }
}

function displaySimulationResults(results) {
    const resultsDiv = document.getElementById('simulation-results');
    if (!resultsDiv) return;
    resultsDiv.innerHTML = `
        <h3>Simulation Results</h3>
        <p>Average Path Length: ${results.avg_path_length.toFixed(2)}</p>
        <p>Average Convergence Time: ${results.avg_convergence_time.toFixed(2)}</p>
        <p>Success Rate: ${(results.success_rate * 100).toFixed(2)}%</p>
    `;
}
