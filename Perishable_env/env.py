import numpy as np
from pydantic import BaseModel
from typing import List, Tuple
from demand_model import compute_demand
from reward import compute_reward
from tasks import get_task_config


class Observation(BaseModel):
    day_number: int
    inventory_levels: List[float]
    avg_days_to_expiry: List[float]
    current_price_level: List[int]
    last_day_sales: List[float]
    seasonality_factor: float
    demand_surge_flag: int
    notification_active_flag: int
    active_bundle_type: int


class Action(BaseModel):
    price_levels: List[int]
    bundle_type: int
    send_notification: int


class RewardInfo(BaseModel):
    revenue: float
    wastage_cost: float
    holding_cost: float
    discount_penalty: float
    bundle_bonus: float
    expired_units: float


class PerishableInventoryEnv:

    EPISODE_LENGTH = 30

    def __init__(self, task_name="easy"):
        self.task_name = task_name
        self.config = get_task_config(task_name)
        self.n_skus = self.config["n_skus"]
        self.seed = 42
        self.rng = np.random.default_rng(self.seed)

        self.reset()

    def reset(self, seed=None):
        if seed is not None:
            self.seed = seed
            self.rng = np.random.default_rng(seed)

        self.day = 0

        self.inventory = np.array(self.config["initial_inventory"], dtype=float)
        self.expiry = np.array(self.config["initial_expiry"], dtype=float)

        self.price_levels = np.zeros(self.n_skus, dtype=int)
        self.last_sales = np.zeros(self.n_skus)

        self.notification_flag = 0
        self.bundle_type = 0

        self.seasonality = 1.0

        self.surge_flag = 0

        return self.state()

    def state(self):
        return Observation(
            day_number=self.day,
            inventory_levels=self.inventory.tolist(),
            avg_days_to_expiry=self.expiry.tolist(),
            current_price_level=self.price_levels.tolist(),
            last_day_sales=self.last_sales.tolist(),
            seasonality_factor=self.seasonality,
            demand_surge_flag=int(self.surge_flag),
            notification_active_flag=int(self.notification_flag),
            active_bundle_type=int(self.bundle_type),
        )

    def _update_surge(self):
        if not self.config["surge"]:
            self.surge_flag = 0
            self.surge_type = None
            return

        prob = 0.15
        if self.rng.random() < prob:
            self.surge_flag = 1
            self.surge_type = self.rng.choice(["heatwave", "festival", "rain"])
        else:
            self.surge_flag = 0
            self.surge_type = None

    def step(self, action_dict):
        action = Action(**action_dict)

        self.price_levels = np.array(action.price_levels)
        self.notification_flag = action.send_notification
        self.bundle_type = action.bundle_type

        self._update_surge()

        demands = compute_demand(
            rng=self.rng,
            config=self.config,
            inventory=self.inventory,
            expiry=self.expiry,
            price_levels=self.price_levels,
            bundle_type=self.bundle_type,
            notification_flag=self.notification_flag,
            seasonality=self.seasonality,
            surge_flag=self.surge_flag,
            surge_type=getattr(self, "surge_type", None),
        )

        sales = np.minimum(self.inventory, demands)
        self.inventory -= sales
        self.last_sales = sales

        expired = (self.expiry <= 0) * self.inventory
        expired_units = expired.sum()
        self.inventory -= expired

        self.expiry -= 1

        reward, info = compute_reward(
            config=self.config,
            sales=sales,
            price_levels=self.price_levels,
            inventory=self.inventory,
            expiry=self.expiry,
            expired_units=expired_units,
            bundle_type=self.bundle_type,
        )

        self.day += 1
        done = self.day >= self.EPISODE_LENGTH

        return self.state(), reward, done, info.dict()