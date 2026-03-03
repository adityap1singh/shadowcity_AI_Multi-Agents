import numpy as np
import random
from collections import deque

class CityEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.stability = 0.5
        self.economy = 0.5
        self.happiness = 0.5
        self.corruption = 0.2
        return self.get_state()

    def get_state(self):
        return np.array([self.stability, self.economy, self.happiness, self.corruption])

    def step(self, actions):
        mayor_action, economic_action, blackhat_action = actions

        self.stability += (mayor_action - 0.5) * 0.1
        self.happiness += (mayor_action - 0.5) * 0.1
        self.economy += (economic_action - 0.5) * 0.1

        if blackhat_action > 0.7:
            self.happiness -= 0.1
            self.corruption += 0.05

        self.stability = np.clip(self.stability, 0, 1)
        self.economy = np.clip(self.economy, 0, 1)
        self.happiness = np.clip(self.happiness, 0, 1)
        self.corruption = np.clip(self.corruption, 0, 1)

        rewards = {
            "mayor": float(self.stability + self.happiness - self.corruption),
            "economic": float(self.economy),
            "blackhat": float(self.corruption + (1 - self.happiness))
        }

        return self.get_state(), rewards


class Agent:
    def __init__(self, name):
        self.name = name
        self.strategy = random.random()
        self.short_memory = deque(maxlen=10)
        self.long_memory = []
        self.emotion = {"frustration": 0.1, "aggression": 0.1, "cooperation": 0.5}
        self.reputation = 1.0
        self.total_reward = 0

    def act(self, state):
        noise = random.uniform(-0.1, 0.1)
        action = self.strategy + noise
        action += self.emotion["aggression"] * 0.1
        action -= self.emotion["cooperation"] * 0.05
        action = np.clip(action, 0, 1)
        self.short_memory.append(state.tolist())
        return action

    def update(self, reward):
        self.total_reward += reward
        self.long_memory.append(reward)
        if reward < 0.3:
            self.emotion["frustration"] += 0.05
        else:
            self.emotion["cooperation"] += 0.02

        for k in self.emotion:
            self.emotion[k] = float(np.clip(self.emotion[k], 0, 1))

    def evolve(self):
        self.strategy = float(np.clip(self.strategy + random.uniform(-0.1, 0.1), 0, 1))
        self.total_reward = 0


class EthicalAgent:
    def detect_deception(self, blackhat_action, state):
        corruption = state[3]
        happiness = state[2]
        return blackhat_action > 0.7 and corruption > 0.4 or happiness < 0.2

    def penalize(self, agent):
        agent.strategy *= 0.8
        agent.reputation -= 0.1
        agent.emotion["frustration"] += 0.1


def run_shadowcity(steps=20):
    env = CityEnvironment()
    mayor = Agent("Mayor")
    economic = Agent("Economic")
    blackhat = Agent("BlackHat")
    ethical = EthicalAgent()

    state = env.reset()
    history = []

    for _ in range(steps):
        mayor_action = mayor.act(state)
        economic_action = economic.act(state)
        blackhat_action = blackhat.act(state)

        state, rewards = env.step([mayor_action, economic_action, blackhat_action])

        mayor.update(rewards["mayor"])
        economic.update(rewards["economic"])
        blackhat.update(rewards["blackhat"])

        if ethical.detect_deception(blackhat_action, state):
            ethical.penalize(blackhat)

        history.append({
            "state": state.tolist(),
            "rewards": rewards
        })

    mayor.evolve()
    economic.evolve()
    blackhat.evolve()

    return {
        "final_state": state.tolist(),
        "history": history
    }