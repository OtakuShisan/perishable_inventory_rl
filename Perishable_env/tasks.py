from reward import compute_reward


def get_task_config(task):

    base = dict(
        base_price=[50, 30, 20, 40],
        base_daily_demand=[20, 18, 25, 15],
        shelf_life=[5, 4, 3, 6],
        holding_cost_per_unit=[0.5, 0.4, 0.3, 0.5],
        wastage_cost_per_unit=[10, 8, 6, 9],
        price_elasticity=[1.2, 1.1, 1.4, 1.0],
        bundles={
            1: [0, 2],
            2: [1, 3],
            3: [2, 0],
        },
        initial_inventory=[120, 100, 140, 90],
        initial_expiry=[4, 3, 2, 5],
        reward_info=compute_reward.__annotations__.get("return", tuple)[1],
    )

    if task == "easy":
        base["n_skus"] = 1
        base["noise_std"] = 0
        base["surge"] = False

    elif task == "medium":
        base["n_skus"] = 4
        base["noise_std"] = 2
        base["surge"] = False

    else:
        base["n_skus"] = 4
        base["noise_std"] = 4
        base["surge"] = True
        base["holding_cost_per_unit"] = [1.0, 0.9, 0.8, 1.1]

    return base