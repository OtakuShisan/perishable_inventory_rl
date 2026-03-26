# Perishable Inventory Profit Optimization Environment

## Motivation

Quick-commerce dark stores must dynamically price perishable goods to reduce wastage and maximize profit.

This environment simulates daily pricing and promotion decisions under uncertainty.

## RL Formulation

Agent controls:

- Discount level per SKU
- Bundle activation
- Notification sending

Objective:

Maximize cumulative profit while minimizing wastage.

## Observation Space

Numeric vector including:

- Inventory levels
- Avg days to expiry
- Price level
- Sales history
- Seasonality
- Surge flags

## Action Space

Discrete:

- Price levels {0,1,2,3}
- Bundle type {0-3}
- Notification {0,1}

## Reward

Revenue  
− Holding cost  
− Wastage cost  
− Excessive discount penalty  
+ Bundle bonus

## Tasks

Easy: Single SKU deterministic  
Medium: Multi SKU stochastic  
Hard: Surge events + higher holding pressure  

## Setup
