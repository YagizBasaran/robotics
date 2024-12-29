import numpy as np
from collections import deque
from tqdm import tqdm  # For progress bar during HER relabeling

class ReplayBuffer:
    def __init__(self, max_size=1e6):
        """
        Initialize the Replay Buffer.

        Args:
            max_size (int): Maximum number of transitions to store.
        """
        self.storage = deque(maxlen=int(max_size))
        self.goal_dim = None  # To track and enforce consistent goal shapes

    def add(self, transition):
        """
        Add a transition to the buffer.

        Args:
            transition (tuple): (state, action, reward, next_state, done, goal)
        """
        # Flatten and standardize shapes
        state = np.array(transition[0]).reshape(-1)
        action = np.array(transition[1]).reshape(-1)
        reward = transition[2]  # scalar
        next_state = np.array(transition[3]).reshape(-1)
        done = transition[4]  # scalar
        goal = np.array(transition[5]).flatten()  # Flatten the goal

        # Initialize goal_dim if not set
        if self.goal_dim is None:
            self.goal_dim = goal.shape[0]
        elif goal.shape[0] != self.goal_dim:
            raise ValueError(f"Inconsistent goal shape: {goal.shape}, expected {self.goal_dim}")

        self.storage.append((state, action, reward, next_state, done, goal))

    def sample(self, batch_size):
        """
        Sample a batch of transitions from the buffer.

        Args:
            batch_size (int): Number of transitions to sample.

        Returns:
            tuple: (states, actions, rewards, next_states, dones, goals)
        """
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

        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.float32),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32),
            np.array(goals, dtype=np.float32)  # Ensure consistent goal shape
        )

    def apply_her(self, strategy="future", k=4, recent_only=False):
        """
        Apply Hindsight Experience Replay (HER) by relabeling transitions.

        Args:
            strategy (str): HER strategy (e.g., "future").
            k (int): Number of HER relabeled goals to generate per transition.
            recent_only (bool): Whether to apply HER only to the most recent episode.
        """
        # Process recent transitions only if specified
        transitions = list(self.storage) if not recent_only else list(self.storage[-100:])  # Limit to 100 most recent

        for transition in tqdm(transitions, desc="Applying HER"):  # Progress bar for better monitoring
            state, action, reward, next_state, done, goal = transition

            if strategy == "future":
                # Generate k future goals randomly
                future_goals = [
                    np.array(transitions[np.random.randint(len(transitions))][3]).flatten()
                    for _ in range(k)
                ]
                for fg in future_goals:
                    fg = fg[:self.goal_dim]  # Ensure consistent shape for relabeled goals
                    new_reward = 1.0 if np.linalg.norm(fg - next_state[:self.goal_dim]) < 0.05 else 0.0
                    self.add((state, action, new_reward, next_state, done, fg))
