import numpy as np

PRICE_MULTIPLIERS = [1.0, 1.2, 1.5, 2.2]


def expiry_multiplier(days):
    if days <= 1:
        return 2.0
    elif days <= 2:
        return 1.5
    return 1.0


def surge_multiplier(sku_index, surge_type):
    if surge_type == "heatwave" and sku_index == 2:
        return 2.0
    if surge_type == "festival" and sku_index in [0, 3]:
        return 1.8
    if surge_type == "rain" and sku_index == 1:
        return 1.6
    return 1.0


def compute_demand(
    rng,
    config,
    inventory,
    expiry,
    price_levels,
    bundle_type,
    notification_flag,
    seasonality,
    surge_flag,
    surge_type,
):
    demand = []

    for i in range(config["n_skus"]):

        base = config["base_daily_demand"][i]

        price_mult = PRICE_MULTIPLIERS[price_levels[i]]

        expiry_mult = expiry_multiplier(expiry[i])

        bundle_mult = 1.3 if i in config["bundles"].get(bundle_type, []) else 1.0

        notif_mult = 1.15 if notification_flag else 1.0

        surge_mult = surge_multiplier(i, surge_type) if surge_flag else 1.0

        noise = rng.normal(0, config["noise_std"])

        eff = (
            base
            * price_mult
            * expiry_mult
            * bundle_mult
            * notif_mult
            * seasonality
            * surge_mult
            + noise
        )

        demand.append(max(0, eff))

    return np.array(demand)