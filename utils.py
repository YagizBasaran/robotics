import numpy as np
import matplotlib.pyplot as plt
import torch

def evaluate(env, actor, num_episodes=10):
    success = 0
    for _ in range(num_episodes):
        obs = env.reset()
        state, goal = obs["observation"], obs["desired_goal"]
        done = False
        while not done:
            state_goal = np.concatenate([state, goal])
            action = actor(torch.FloatTensor(state_goal).unsqueeze(0)).detach().numpy()[0]
            obs, reward, done, _ = env.step(action)
            state = obs["observation"]
            achieved_goal = obs["achieved_goal"]
            if np.linalg.norm(achieved_goal - goal) < 0.05:
                success += 1
                break
    return success / num_episodes

def plot_results(success_rates):
    plt.plot(success_rates)
    plt.xlabel("Episodes (x10)")
    plt.ylabel("Success Rate")
    plt.title("Training Success Rates")
    plt.show()
