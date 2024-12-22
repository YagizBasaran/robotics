import gymnasium as gym
from replay_buffer import ReplayBuffer
from models import Actor, Critic
from utils import evaluate, plot_results
import torch
import torch.optim as optim
import numpy as np

# Training parameters
ENV_NAME = "FetchReach-v1"
NUM_EPISODES = 500
BATCH_SIZE = 64
GAMMA = 0.98
TAU = 0.005
ALPHA = 0.2  # Initial entropy coefficient
LEARNING_RATE = 0.001
MAX_BUFFER_SIZE = 1e6
K = 4  # Number of HER goals per episode

def train_sac_her():
    # Initialize environment
    env = gym.make(ENV_NAME)
    state_dim = env.observation_space["observation"].shape[0]
    goal_dim = env.observation_space["desired_goal"].shape[0]
    action_dim = env.action_space.shape[0]
    max_action = env.action_space.high[0]

    # Initialize actor, critic, and target networks
    actor = Actor(state_dim + goal_dim, action_dim, max_action)
    critic = Critic(state_dim + goal_dim, action_dim)
    critic_target = Critic(state_dim + goal_dim, action_dim)
    critic_target.load_state_dict(critic.state_dict())

    # Optimizers
    actor_optimizer = optim.Adam(actor.parameters(), lr=LEARNING_RATE)
    critic_optimizer = optim.Adam(critic.parameters(), lr=LEARNING_RATE)

    # Replay buffer
    replay_buffer = ReplayBuffer(max_size=MAX_BUFFER_SIZE)

    # Training loop
    success_rates = []
    for episode in range(NUM_EPISODES):
        observation = env.reset()
        state, goal = observation["observation"], observation["desired_goal"]
        episode_transitions = []

        done = False
        while not done:
            state_goal = np.concatenate([state, goal])
            action = actor(torch.FloatTensor(state_goal).unsqueeze(0)).detach().numpy()[0]
            next_observation, reward, done, _ = env.step(action)
            next_state = next_observation["observation"]
            achieved_goal = next_observation["achieved_goal"]

            # Sparse reward
            reward = 1.0 if np.linalg.norm(achieved_goal - goal) < 0.05 else 0.0

            # Store transition
            episode_transitions.append((state, action, reward, next_state, done, goal))
            state = next_state

        # Add transitions to the replay buffer with HER
        for transition in episode_transitions:
            replay_buffer.add(transition)
        replay_buffer.apply_her(strategy="future", k=K)

        # Update actor and critic networks
        for _ in range(50):
            states, actions, rewards, next_states, dones, goals = replay_buffer.sample(BATCH_SIZE)

            # Convert to tensors
            states = torch.FloatTensor(states)
            actions = torch.FloatTensor(actions)
            rewards = torch.FloatTensor(rewards).unsqueeze(-1)
            next_states = torch.FloatTensor(next_states)
            dones = torch.FloatTensor(dones).unsqueeze(-1)
            goals = torch.FloatTensor(goals)

            # Concatenate states and goals
            state_goals = torch.cat([states, goals], dim=1)
            next_state_goals = torch.cat([next_states, goals], dim=1)

            # Update critic
            with torch.no_grad():
                next_actions = actor(next_state_goals)
                q1_next, q2_next = critic_target(next_state_goals, next_actions)
                q_next = torch.min(q1_next, q2_next) - ALPHA * torch.log_softmax(next_actions, dim=1)
                q_target = rewards + (1 - dones) * GAMMA * q_next

            q1, q2 = critic(state_goals, actions)
            critic_loss = ((q1 - q_target).pow(2) + (q2 - q_target).pow(2)).mean()
            critic_optimizer.zero_grad()
            critic_loss.backward()
            critic_optimizer.step()

            # Update actor
            actions_pred = actor(state_goals)
            q1_pred, _ = critic(state_goals, actions_pred)
            actor_loss = (ALPHA * torch.log_softmax(actions_pred, dim=1) - q1_pred).mean()
            actor_optimizer.zero_grad()
            actor_loss.backward()
            actor_optimizer.step()

            # Update target networks
            for param, target_param in zip(critic.parameters(), critic_target.parameters()):
                target_param.data.copy_(TAU * param.data + (1 - TAU) * target_param.data)

        # Evaluate the policy
        if episode % 10 == 0:
            success_rate = evaluate(env, actor, num_episodes=10)
            success_rates.append(success_rate)
            print(f"Episode {episode}, Success Rate: {success_rate * 100:.2f}%")

    # Plot and save results
    plot_results(success_rates)

if __name__ == "__main__":
    train_sac_her()
