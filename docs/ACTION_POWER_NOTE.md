# Action Power Branch: Honest Status

**Date:** 2026-04-04
**Status:** bounded axiom-fork branch with a retained 3D barrier card and a 3D no-barrier law companion

## What this is

An AXIOM FORK exploring the action formula S = L × |f|^p as an
alternative to the spent-delay formula S = dl - √(dl² - L²).

Changing the action is a new branch. No claims inherited from the
spent-delay flagship.

## Harness-validated results

### 2D NN lattice (canonical harness, script: action_power_canonical_harness.py)

| Property | Spent-delay | Power p=0.5 |
|----------|------------|-------------|
| Born | 3.2e-16 ✅ | 2.2e-16 ✅ |
| k=0 | 0.0 ✅ | 0.0 ✅ |
| MI | 0.567 | 0.623 |
| d_TV | 0.789 | 0.834 |
| 1-pur | 0.441 | 0.431 |
| Gravity | -0.291 (AWAY) | -0.073 (AWAY) |
| Distance | -1.33 (R²=1.0) | -2.90 (R²=1.0) |
| F∝M | 0.64 | **0.95** |

### 3D NN lattice: close-slit barrier card (`L = 12`, `W = 6`)

| Property | Spent-delay | Power p=0.5 |
|----------|------------|-------------|
| Born | `4.24e-16` | **`2.63e-16`** |
| k=0 | `0.0` | `0.0` |
| MI | `0.446` | **`0.671`** |
| d_TV | `0.676` | **`0.812`** |
| 1-pur | **`0.449`** | `0.425` |
| Gravity | `-0.0113` (AWAY) | `-0.000076` (AWAY) |

Barrier geometry:

- slit A: `(y, z) = (2, 0)`
- slit B: `(y, z) = (-2, 0)`
- Born-only third slit C: `(y, z) = (0, 1)`
- detector: full last layer
- MI / `d_TV` / purity use the same close two-slit barrier card
- Born uses the same barrier plane with a genuine third slit and nonzero signal

### 3D NN lattice: no-barrier law companion on the same family

| Property | Spent-delay | Power p=0.5 |
|----------|------------|-------------|
| Distance exponent | `+0.74` (`R² = 0.733`) | **`-1.84` (`R² = 0.880`)** |
| F∝M alpha | `0.46` | **`1.00`** |

So the 3D branch now has:

- a **real barrier card** for Born / `k=0` / MI / `d_TV` / decoherence
- a **real no-barrier companion** for distance law and mass response
- but **not** a same-harness 3D gravity-toward-mass card

## What is NOT validated

- Gravity toward mass on the 3D barrier card
- A same-harness 3D card that includes Born, MI/decoherence, and the distance / mass laws all at once
- Continuum limit with power action
- Multi-spacing convergence / robustness

## Dimensional interpretation

The action power p controls a trade-off between distance law
and mass scaling. On the same NN lattice architecture:

| d | p | Distance exp | F∝M alpha |
|---|---|-------------|-----------|
| 2 | 0.5 (power) | -2.90 | 0.95 |
| 2 | spent-delay | -1.33 | 0.64 |
| 3 | 0.5 (power) | **-1.82** | **0.99** |
| 3 | spent-delay | -0.66 | 0.54 |

The power action on 3D gives exponent `-1.84` on the retained no-barrier
companion, consistent with a `1/b²`-like falloff on the tested window, while
also giving nearly linear mass response (`alpha = 1.00`).

## Honest assessment

The branch is stronger than it was before, but the honest read is still
bounded:

1. the 3D close-slit barrier card is now real and Born-clean
2. the 3D no-barrier power-action companion has the best current distance /
   mass-law behavior on this branch
3. the 3D barrier gravity sign is still wrong

So the action-power branch is now a real complementary 3D lane, not yet a
replacement for the spent-delay flagship and not yet a full same-harness
Newtonian closure.

## Scripts

| Script | What it tests |
|--------|---------------|
| action_power_canonical_harness.py | 2D same-harness comparison plus 3D close-slit barrier card and 3D no-barrier companion |

## Artifact chain

- [`scripts/action_power_canonical_harness.py`](/Users/jonreilly/Projects/Physics/scripts/action_power_canonical_harness.py)
- [`logs/2026-04-04-action-power-canonical-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-action-power-canonical-harness.txt)
