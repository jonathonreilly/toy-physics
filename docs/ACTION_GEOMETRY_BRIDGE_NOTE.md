# Action Geometry Bridge Note

**Date:** 2026-04-04  
**Status:** bounded geometry-dependent bridge probe; safe read is mixed bridge

## Purpose

This note freezes a stricter version of the regularity crossover question:

- same generated DAG family
- same seed set
- same barrier / detector geometry
- same field shape and strength
- two actions only:
  - spent-delay
  - valley-linear `S = L(1-f)`

The question is not whether one action is universally better. The question is
whether the preference shifts smoothly as the geometry becomes more regular.

## Primary artifact

- Script: [`scripts/action_geometry_bridge_probe.py`](/Users/jonreilly/Projects/Physics/scripts/action_geometry_bridge_probe.py)
- Log: [`logs/2026-04-04-action-geometry-bridge-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-action-geometry-bridge-probe.txt)

## Frozen replay setup

The replay uses:

- `seeds = 12`
- `layers = 20`
- `npl = 25`
- `xyz_range = 8.0`
- `connect_radius = 5.0`
- `regularities = (0.0, 0.1, 0.2, 0.3, 0.4, 0.55, 0.7, 0.85, 0.95)`

The sweep compares:

- spent-delay
- valley-linear

on the same DAG family for each regularity level.

## Frozen replay result

| regularity | valley TOWARD | spent TOWARD | delta | advantage |
|---|---:|---:|---:|---:|
| `0.00` | `16/36` | `24/36` | `-22.2%` | `-0.624841` |
| `0.10` | `19/36` | `19/36` | `0.0%` | `+0.052785` |
| `0.20` | `20/36` | `24/36` | `-11.1%` | `-0.247367` |
| `0.30` | `15/36` | `20/36` | `-13.9%` | `-0.339599` |
| `0.40` | `24/36` | `15/36` | `+25.0%` | `+0.182256` |
| `0.55` | `20/36` | `18/36` | `+5.6%` | `-0.141862` |
| `0.70` | `9/36` | `13/36` | `-11.1%` | `-0.070982` |
| `0.85` | `20/36` | `15/36` | `+13.9%` | `+0.113573` |
| `0.95` | `16/36` | `12/36` | `+11.1%` | `+0.421028` |

Derived bridge read:

- best observed advantage at `regularity = 0.40`
- estimated crossover regularity `~ 0.10`
- advantage-vs-regularity fit: positive slope, but low `R^2`

## Safe interpretation

- The action preference does shift with regularity on the tested family.
- The shift is real enough to freeze as a branch fact.
- The shift is not cleanly monotonic on this slice.
- The safest label is **mixed bridge**.

## What this does not prove

- It does **not** prove a universal action unification.
- It does **not** prove valley-linear replaces spent-delay.
- It does **not** prove a continuum theorem.
- It does **not** settle the architecture split outside the tested slice.

## Why this matters

This is stricter than chat narrative because it freezes:

1. the exact controlled family
2. the matched seeds and detector geometry
3. the full regularity grid
4. the branch-specific mixed outcome

That makes the action/geometry split easier to read without overpromising a
theorem.
