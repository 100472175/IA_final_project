import gym
import numpy as np


# Define the temperature control environment using the gym library
class TempControlEnv(gym.Env):
    def __init__(self):
        super.__init__()
        self.observation_space = gym.spaces.Discrete(19)
        self.action_space = gym.spaces.Discrete(2)
        self.state = None
        self.desired_temp = 22

    def reset(self):
        self.state = np.random.randint(16, 26)
        return self.state

    def step(self, action):
        assert self.action_space.contains(action)
        if action == 0:
            # heating off
            temp_change_probs = [0.7, 0.1, 0.2]
            if self.state == 16:
                temp_change_probs = [0.9, 0.0, 0.1]
        else:
            # heating on
            temp_change_probs = [0.5, 0.2, 0.2, 0.1]
            if self.state == 24:
                temp_change_probs = [0.2, 0.0, 0.2, 0.6]
            elif self.state == 24.5:
                temp_change_probs = [0.2, 0.0, 0.7, 0.1]
            elif self.state == 25:
                temp_change_probs = [0.0, 0.0, 0.1, 0.9]
        temp_change = np.random.choice([-0.5, 0.0, 0.5, 1.0], p=temp_change_probs)
        self.state = np.clip(self.state + temp_change, 16, 25)
        reward = -abs(self.state - self.desired_temp)
        done = (self.state == self.desired_temp)
        return self.state, reward, done, {}

    def render(self, mode='human'):
        print(f"Temperature: {self.state} degrees Celsius")


# Define the value iteration algorithm to calculate the optimal policy
def value_iteration(env, gamma=0.9, theta=1e-5):
    V = np.zeros(env.observation_space.n)
    while True:
        delta = 0
        for s in range(env.observation_space.n):
            v = V[s]
            V[s] = max(
                [sum([p * (r + gamma * V[s_]) for p, s_, r, _ in env.env.P[s][a]]) for a in range(env.action_space.n)])
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    policy = np.zeros(env.observation_space.n)
    for s in range(env.observation_space.n):
        q_vals = np.array(
            [sum([p * (r + gamma * V[s_]) for p, s_, r, _ in env.env.P[s][a]]) for a in range(env.action_space.n)])
        policy[s] = np.argmax(q_vals)
    return policy, V


# Create the temperature control environment and calculate the optimal policy
env = TempControlEnv()
policy, V = value_iteration(env)

# Print the optimal policy and the corresponding state values
for s in range(env.observation_space.n):
    print(f"State {s}: Action {policy[s]}, Value {V[s]}")
