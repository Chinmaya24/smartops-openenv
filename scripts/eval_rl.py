from stable_baselines3 import PPO
from env.gym_wrapper import SmartOpsGymEnv

env = SmartOpsGymEnv()

model = PPO.load("smartops_ppo")

obs, _ = env.reset()

total_reward = 0

for _ in range(50):
    action, _ = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)

    total_reward += reward

    if done:
        obs, _ = env.reset()

print("Average Reward:", total_reward / 50)