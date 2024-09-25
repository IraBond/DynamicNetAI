import numpy as np

class QLearning:
    def __init__(self, graph, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.graph = graph
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def update_q_value(self, state, action, reward, next_state):
        current_q = self.get_q_value(state, action)
        max_next_q = max([self.get_q_value(next_state, a) for a in self.graph.neighbors(next_state)])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def choose_action(self, state):
        if np.random.random() < self.exploration_rate:
            return np.random.choice(list(self.graph.neighbors(state)))
        else:
            q_values = [self.get_q_value(state, action) for action in self.graph.neighbors(state)]
            if np.all(np.array(q_values) == 0):
                return np.random.choice(list(self.graph.neighbors(state)))
            return list(self.graph.neighbors(state))[np.argmax(q_values)]

    def find_path(self, start, goal, max_steps=1000):
        current_state = start
        path = [current_state]
        steps = 0

        while current_state != goal and steps < max_steps:
            action = self.choose_action(current_state)
            next_state = action
            reward = -self.graph.cost(current_state, next_state)
            self.update_q_value(current_state, action, reward, next_state)
            current_state = next_state
            path.append(current_state)
            steps += 1
            print(f"Step {steps}: State={current_state}, Action={action}, Reward={reward}")

        if steps >= max_steps:
            print("Reached max steps, stopping pathfinding.")
        elif current_state == goal:
            print(f"Goal reached in {steps} steps.")
        
        return path

    def train(self, start, goal, episodes):
        for episode in range(episodes):
            path = self.find_path(start, goal)
            print(f"Episode {episode + 1}: Path length = {len(path)}")
            self.exploration_rate = max(self.exploration_rate * 0.99, 0.01)
