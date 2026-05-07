import numpy as np
import random

class TrafficRLAgent:
    def __init__(self):
        # 🔥 Use only meaningful states
        self.states = 4
        self.actions = 3

        self.q_table = np.zeros((self.states, self.actions))

        # Learning params
        self.alpha = 0.1
        self.gamma = 0.9

        # Exploration
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

    # 🔥 OPTIMIZED STATE MAPPING
    def get_state(self, traffic_count):
        if traffic_count < 5:
            return 0   # low traffic
        elif traffic_count < 10:
            return 1   # moderate
        elif traffic_count < 20:
            return 2   # high
        else:
            return 3   # heavy congestion

    # 🎯 ACTION SELECTION (ε-greedy)
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.actions - 1)
        return np.argmax(self.q_table[state])

    # 🔥 Q-LEARNING UPDATE
    def update_q(self, state, action, reward, next_state):
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])

        new_value = old_value + self.alpha * (
            reward + self.gamma * next_max - old_value
        )

        self.q_table[state, action] = new_value

        # 🔥 DECAY EXPLORATION
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # 📊 Debug helper
    def print_q_table(self):
        print("\n🧠 Q-Table:")
        for i, row in enumerate(self.q_table):
            print(f"State {i}: {row}")