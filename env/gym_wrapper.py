import gymnasium as gym
from gymnasium import spaces
import numpy as np

from env.smart_ops_env import SmartOpsEnv
from env.models import Action


class SmartOpsGymEnv(gym.Env):

    def __init__(self):
        super().__init__()
        self.env = SmartOpsEnv()

        self.observation_space = spaces.Box(low=0, high=10, shape=(6,), dtype=np.float32)

        self.action_space = spaces.Discrete(4)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if seed is not None:
            obs = self.env.reset(seed=seed)
        else:
            obs = self.env.reset()
        return self._encode_obs(obs), {}

    def step(self, action):
        agent_map = ["triage", "response", "escalation", "manager"]

        agent_name = agent_map[action]

        act = Action(agent=agent_name, action_type="auto")

        obs, reward, done, _ = self.env.step(act)

        return self._encode_obs(obs), float(reward.score), done, False, {}

    def _encode_obs(self, obs):
        memory = obs.shared_memory or {}

        return np.array([
            obs.step_count,
            1 if memory.get("category") else 0,
            memory.get("urgency", 0) or 0,
            1 if memory.get("response") else 0,
            1 if memory.get("escalated") else 0,
            memory.get("priority", 0) or 0
        ], dtype=np.float32)
