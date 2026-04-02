import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from env.models import Action
from env.smart_ops_env import SmartOpsEnv

env = SmartOpsEnv()
obs = env.reset()

done = False

while not done:
    agent = obs.current_agent

    action = Action(agent=agent, action_type="auto")

    obs, reward, done, _ = env.step(action)

    print(f"Agent: {agent}")
    print(f"Memory: {obs.shared_memory}")
    print(f"Reward: {reward.score}, Feedback: {reward.feedback}")
    print("-" * 40)
