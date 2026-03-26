from grader import grade


def heuristic_agent(obs):

    prices = []

    for inv, exp in zip(obs.inventory_levels, obs.avg_days_to_expiry):

        if exp <= 2:
            prices.append(3)
        elif obs.demand_surge_flag:
            prices.append(0)
        else:
            prices.append(1)

    send_notification = 1 if sum(obs.inventory_levels) > 200 else 0

    bundle = 0
    near = [i for i, e in enumerate(obs.avg_days_to_expiry) if e <= 2]

    if len(near) >= 2:
        bundle = 1

    return dict(
        price_levels=prices,
        bundle_type=bundle,
        send_notification=send_notification,
    )


if __name__ == "__main__":

    for t in ["easy", "medium", "hard"]:
        score = grade(t, heuristic_agent)
        print(t, score)