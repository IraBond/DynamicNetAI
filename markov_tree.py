import random

class MarkovTree:
    def __init__(self, graph):
        self.graph = graph
        self.transition_probabilities = {}

    def update_transition_probabilities(self, state, action, next_state):
        if state not in self.transition_probabilities:
            self.transition_probabilities[state] = {}
        if action not in self.transition_probabilities[state]:
            self.transition_probabilities[state][action] = {}
        if next_state not in self.transition_probabilities[state][action]:
            self.transition_probabilities[state][action][next_state] = 0
        self.transition_probabilities[state][action][next_state] += 1

    def get_next_state(self, state, action):
        if state in self.transition_probabilities and action in self.transition_probabilities[state]:
            probabilities = self.transition_probabilities[state][action]
            total = sum(probabilities.values())
            r = random.uniform(0, total)
            upto = 0
            for next_state, prob in probabilities.items():
                if upto + prob >= r:
                    return next_state
                upto += prob
        return action

    def find_path(self, start, goal, astar, qlearning):
        current_state = start
        path = [current_state]

        while current_state != goal:
            astar_action = astar.find_path(current_state, goal)[1]
            qlearning_action = qlearning.choose_action(current_state)
            
            # Combine A* and Q-learning decisions
            if random.random() < 0.5:
                action = astar_action
            else:
                action = qlearning_action

            next_state = self.get_next_state(current_state, action)
            self.update_transition_probabilities(current_state, action, next_state)
            current_state = next_state
            path.append(current_state)

        return path
