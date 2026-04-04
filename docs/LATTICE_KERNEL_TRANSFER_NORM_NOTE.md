# 3D Kernel Transfer-Norm Probe

**Date:** 2026-04-04  
**Status:** bounded discrimination probe, not a promoted branch claim

This note freezes a small local probe of the exploratory 3D kernel lane.
It is intentionally narrower than the heavy `h=0.25` / 4D work Claude is
running elsewhere.

## Script

[`scripts/lattice_kernel_transfer_norm_probe.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_kernel_transfer_norm_probe.py)

## Log

[`logs/2026-04-04-lattice-kernel-transfer-norm-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-kernel-transfer-norm-probe.txt)

## What the probe measures

The probe computes a local outgoing transfer norm on a representative 3D
ordered-lattice neighborhood:

- kernel power `p` in `1/L^p`
- refinement `h`
- measure-corrected norm `h^2 × Σ exp(-β θ²) / L^p`

It is a discrimination harness, not a proof of the continuum limit.

## Retained local read

Using the measured norm with `h^2` normalization, the closest-to-marginal
power in the tested sweep is:

- `p = 1.5` is closest to stable across `h = 1.0, 0.5, 0.25, 0.125`
- `p = 2.0` is next, but still drifts with refinement
- `p = 2.5` and `p = 3.0` drift more strongly away from marginality

The fitted measured-norm slopes from the probe are:

| p | measured slope | read |
|---|---:|---|
| 1.5 | `+0.102` | closest to marginal |
| 2.0 | `-0.204` | still scales with `h` |
| 2.5 | `-0.598` | clearly non-marginal |
| 3.0 | `-1.046` | strongly non-marginal |

## Review-safe interpretation

- This does **not** prove the final 3D kernel power.
- It does **not** replace the same-harness propagation audits.
- It does **not** settle the branch-level promotion question.

What it does give us is a bounded local discriminator:

- the simple local transfer norm does not currently single out `p = 2.0`
- the probe points to a shallower effective marginality near `p = 1.5`
- that result should be treated as a review-safe warning, not a promoted law

## Why this matters

The probe is useful because it separates three questions that should not be
blurred together:

1. sign persistence under refinement
2. distance-tail steepening
3. finite-magnitude transfer control

Only the third question is tested here, and only in a local kernel-only way.
The full 3D branch still needs same-harness propagation and artifact-chain
closure before any promotion.
