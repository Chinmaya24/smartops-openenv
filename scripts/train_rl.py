import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from env.gym_wrapper import SmartOpsGymEnv
import os


def train():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    print("🚀 Training started...")

    env = SmartOpsGymEnv()

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        tensorboard_log="./logs/",
    )

    eval_env = SmartOpsGymEnv()
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path="./models/",
        log_path="./logs/",
        eval_freq=2000,
        deterministic=True,
        render=False
    )

    model.learn(
        total_timesteps=30000,
        tb_log_name="smartops_run",
        callback=eval_callback
    )

    model.save("models/smartops_ppo_v1")

    print("✅ Training complete")


if __name__ == "__main__":
    train()
