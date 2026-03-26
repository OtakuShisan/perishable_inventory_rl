import numpy as np

PRICE_DISCOUNT = [0.0, 0.1, 0.25, 0.5]


def compute_reward(config, sales, price_levels, inventory, expiry, expired_units, bundle_type):

    base_prices = np.array(config["base_price"])

    discounts = np.array([PRICE_DISCOUNT[p] for p in price_levels])

    prices = base_prices * (1 - discounts)

    revenue = (prices * sales).sum()

    wastage_cost = expired_units * np.mean(config["wastage_cost_per_unit"])

    holding_cost = (inventory * config["holding_cost_per_unit"]).sum()

    penalty = 0
    for i, p in enumerate(price_levels):
        if p == 3 and expiry[i] > 2:
            penalty += 2.0

    bundle_bonus = 5.0 if bundle_type != 0 else 0.0

    reward = revenue - wastage_cost - holding_cost - penalty + bundle_bonus

    return reward, config["reward_info"](
        revenue=revenue,
        wastage_cost=wastage_cost,
        holding_cost=holding_cost,
        discount_penalty=penalty,
        bundle_bonus=bundle_bonus,
        expired_units=expired_units,
    )