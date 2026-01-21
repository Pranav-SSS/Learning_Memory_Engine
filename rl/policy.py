import random
from collections import defaultdict
random.seed(42)

class TeachingPolicy:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon
        self.q = defaultdict(lambda: defaultdict(float))
        self.n = defaultdict(lambda: defaultdict(int))

        self.actions = [
            "explanation",
            "example",
            "practice",
            "prerequisite"
        ]

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return max(self.actions, key=lambda a: self.q[state][a])

    def update(self, state, action, reward):
        self.n[state][action] += 1
        count = self.n[state][action]
        self.q[state][action] += (reward - self.q[state][action]) / count