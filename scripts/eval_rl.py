import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stable_baselines3 import PPO
from env.gym_wrapper import SmartOpsGymEnv

env = SmartOpsGymEnv()

root = Path(__file__).resolve().parents[1]
for name in ("smartops_ppo_v1", "smartops_ppo"):
    p = root / "models" / f"{name}.zip"
    if p.exists():
        model = PPO.load(str(p))
        break
else:
    raise FileNotFoundError(
        "No trained model in models/. Run: pip install -r requirements-rl.txt && python scripts/train_rl.py"
    )

obs, _ = env.reset()

total_reward = 0

for _ in range(50):
    action, _ = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)

    total_reward += reward

    if done:
        obs, _ = env.reset()

print("Average Reward:", total_reward / 50)
