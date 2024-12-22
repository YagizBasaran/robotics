import numpy as np
from collections import deque

class ReplayBuffer:
    def __init__(self, max_size=1e6):
        self.storage = deque(maxlen=int(max_size))

    def add(self, transition):
        self.storage.append(transition)

    def sample(self, batch_size):
        indices = np.random.choice(len(self.storage), batch_size)
        states, actions, rewards, next_states, dones, goals = [], [], [], [], [], []
        for idx in indices:
            state, action, reward, next_state, done, goal = self.storage[idx]
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            dones.append(done)
            goals.append(goal)
        return (np.array(states), np.array(actions), np.array(rewards),
                np.array(next_states), np.array(dones), np.array(goals))

    def apply_her(self, strategy="future", k=4):
        for transition in list(self.storage):
            state, action, reward, next_state, done, goal = transition
            if strategy == "future":
                future_goals = [self.storage[np.random.randint(len(self.storage))][3] for _ in range(k)]
                for fg in future_goals:
                    new_reward = 1.0 if np.linalg.norm(fg - next_state) < 0.05 else 0.0
                    self.add((state, action, new_reward, next_state, done, fg))
