from stable_baselines3 import PPO
from env.gym_wrapper import SmartOpsGymEnv
import os


def train():
    os.makedirs("logs", exist_ok=True)

    print("🚀 Training started...")

    env = SmartOpsGymEnv()

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        tensorboard_log="./logs/",
    )

    model.learn(
        total_timesteps=10000,
        tb_log_name="smartops_run"
    )

    model.save("smartops_ppo")

    print("✅ Training complete")


if __name__ == "__main__":
    train()