import numpy as np
from env import PerishableInventoryEnv


def run_episode(env, agent):

    obs = env.reset(seed=42)
    total_reward = 0
    total_wastage = 0
    total_sales = 0

    done = False

    while not done:
        action = agent(obs)
        obs, reward, done, info = env.step(action)

        total_reward += reward
        total_wastage += info["expired_units"]
        total_sales += sum(obs.last_day_sales)

    return total_reward, total_wastage, total_sales


def grade(task, agent):

    env = PerishableInventoryEnv(task)

    profit, wastage, sales = run_episode(env, agent)

    norm_profit = 1 / (1 + np.exp(-profit / 1000))

    wastage_score = 1 / (1 + wastage)

    turnover = sales / 1000

    if task == "easy":
        return norm_profit

    if task == "medium":
        return 0.7 * norm_profit + 0.3 * wastage_score

    return 0.5 * norm_profit + 0.3 * turnover + 0.2 * wastage_score