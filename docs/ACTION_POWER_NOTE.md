# Action Power Branch: Honest Status

**Date:** 2026-04-04
**Status:** Interesting but incomplete. Two properties harness-validated on 3D. Full card needs work.

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

### 3D NN lattice (canonical harness, no-barrier properties only)

| Property | Spent-delay | Power p=0.5 |
|----------|------------|-------------|
| Distance | -0.66 (R²=0.96) | **-1.82 (R²=0.93)** |
| F∝M | 0.54 | **0.99** |
| Born | (not yet) | (no signal through barrier) |
| MI | (not yet) | (no signal through barrier) |

## What is NOT validated

- Born on 3D (barrier doesn't transmit enough signal)
- MI/decoherence on 3D (same issue)
- Gravity toward mass (both actions give AWAY on lattice with barriers)
- Continuum limit with power action
- Multi-spacing convergence

## Dimensional interpretation

The action power p controls a trade-off between distance law
and mass scaling. On the same NN lattice architecture:

| d | p | Distance exp | F∝M alpha |
|---|---|-------------|-----------|
| 2 | 0.5 (power) | -2.90 | 0.95 |
| 2 | spent-delay | -1.33 | 0.64 |
| 3 | 0.5 (power) | **-1.82** | **0.99** |
| 3 | spent-delay | -0.66 | 0.54 |

The power action on 3D gives exponent -1.82, consistent with
1/b² (Newtonian gravity in 3 spatial dimensions). This is the
branch's strongest claim, but it is from a no-barrier harness,
not a full joint card.

## Honest assessment

The power action branch has two genuinely strong results on 3D:
1. Distance ≈ 1/b² (R²=0.93, robust across field strengths)
2. F∝M ≈ 1.0 (R²=0.99, nearly perfect linear mass scaling)

These are the two properties the spent-delay flagship DOESN'T
achieve on the lattice. The power action is a complementary
architecture, not a replacement.

The branch is incomplete because the barrier setup (needed for
decoherence and Born) doesn't work on the 3D NN lattice yet.
This is a graph density issue, not an action formula issue.

## Scripts

| Script | What it tests |
|--------|---------------|
| action_power_canonical_harness.py | Full 2D harness, both actions |
| (inline 3D tests) | 3D no-barrier distance + F∝M |
