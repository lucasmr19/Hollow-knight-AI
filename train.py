# Training the agent with PPO
from stable_baselines3 import PPO
from HollowKnightEnv import HollowKnightEnv

# Create and wrap the environment
env = HollowKnightEnv("Hollow Knight")

# Initialize the PPO model with a CNN policy. Change hyperparameters as needed.
model = PPO("CnnPolicy", env, verbose=1,
            learning_rate=0.0003, n_steps=2048,
            batch_size=64, gae_lambda=0.95,
            gamma=0.99)


# Train the model for 100,000 timesteps
model.learn(total_timesteps=100000)