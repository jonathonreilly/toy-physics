# Source-Resolved Generated Support + Mass Scaling

**Date:** 2026-04-05  
**Status:** bounded partial recovery on the compact generated DAG family, but
**Claim type:** bounded_theorem
not a mass-scaling closure

**Audit-conditional perimeter (2026-05-03):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
runner output supports the stated finite numerical readout, but the
runner has no explicit PASS/FAIL assertions and the claim relies on
interpreting 'far from linear' and 'mass-scaling class' without a
closed threshold or independent comparator in the provided material."
This rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The supported content
of this note is the displayed numerical readout itself: per-`s`
detector tables, the four-strength fitted centroid-shift exponents
(`-0.299` baseline, `-0.152` kNN-floor), and the two-row aggregate
table — all reproduced byte-for-byte by the registered runner output.
The §"Safe read" qualitative phrasing ("far from the retained linear
class", "non-Newtonian regime") is bounded interpretation that depends
on a comparator threshold not in the restricted packet; the
supported perimeter is just the finite numerical readout, not the
classifier-level interpretation.

## Artifact chain

- [`scripts/source_resolved_generated_support_mass_scaling.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_support_mass_scaling.py)
- [`logs/2026-04-05-source-resolved-generated-support-mass-scaling.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-support-mass-scaling.txt)

## Question

Does the retained compact generated-family support-recovery tweak also restore
the weak-field mass-scaling class?

This probe stays deliberately narrow:

- compact generated 3D DAG family
- one connectivity-side tweak: next-layer `k`-nearest floor augmentation
- one self-consistent Green readout
- one support metric: detector effective support `N_eff`
- one mass-scaling observable: centroid-shift exponent across source strength

## Frozen result

The frozen probe uses:

- family seeds `0..3`
- `N_LAYERS = 16`
- `NODES_PER_LAYER = 24`
- `CONNECT_RADIUS = 3.2`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- Green kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.50`
- field target max `0.02`
- connectivity tweak:
  - baseline adjacency plus next-layer `k`-nearest floor augmentation
  - `k_nearest = 3`
  - `min_edges = 5`

Zero-source sanity:

- baseline max `|zero-source shift| = 0.000e+00`
- tweak max `|zero-source shift| = 0.000e+00`

Per-`s` detector / scaling readout (baseline):

| `s` | `delta_mean` | sign | `N_eff` |
| --- | ---: | :---: | ---: |
| `0.0010` | `-8.435233e-02` | `AWAY` | `2.57` |
| `0.0020` | `-8.893522e-02` | `AWAY` | `2.60` |
| `0.0040` | `-7.117551e-02` | `AWAY` | `2.71` |
| `0.0080` | `-4.548761e-02` | `AWAY` | `2.78` |

Per-`s` detector / scaling readout (baseline + `kNN` floor):

| `s` | `delta_mean` | sign | `N_eff` |
| --- | ---: | :---: | ---: |
| `0.0010` | `-4.028207e-01` | `AWAY` | `4.67` |
| `0.0020` | `-2.911836e-01` | `AWAY` | `4.86` |
| `0.0040` | `+9.461983e-02` | `TOWARD` | `5.49` |
| `0.0080` | `+4.128727e-01` | `TOWARD` | `5.97` |

Aggregated readout (one row per case; centroid-shift column is the
arithmetic mean of per-`s` `delta_mean` values across the four source
strengths):

| case | mean centroid shift | sign rows | mean `N_eff` | fitted F~M exponent |
| --- | ---: | ---: | ---: | ---: |
| baseline generated family | `-7.249e-02` | `0/4` TOWARD | `2.66` | `-0.299` |
| baseline + `kNN` floor | `-4.658e-02` | `2/4` TOWARD | `5.25` | `-0.152` |

## Safe read

The connectivity tweak does recover something on the compact generated family:

- detector support broadens by `N_eff`
- the aggregated centroid sign moves back toward `TOWARD`

But the mass-scaling class does **not** recover:

- the fitted centroid-shift exponent remains far from the retained linear class
- the baseline and tweak both sit in a non-Newtonian regime on this family
- the tweak improves breadth and sign, not the weak-field mass-law

## Honest limitation

This is still not a full generated-family transfer of the exact-lattice Green
pocket.

The remaining concentration metrics are still strong, and the source-response
scaling is not linear.

## Branch verdict

Treat this as a real partial recovery:

- baseline generated family is still localized and `AWAY`
- one simple connectivity-side modification partially broadens support
- the centroid moves back toward `TOWARD`
- but the weak-field mass-scaling class does not come back
- so this is a support/sign rescue, not a generated-family closure
