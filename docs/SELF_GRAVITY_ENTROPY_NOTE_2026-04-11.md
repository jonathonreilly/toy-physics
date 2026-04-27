# Self-Gravity Bipartition Entropy Probe

**Date:** 2026-04-11  
**Script:** `scripts/frontier_self_gravity_entropy.py`  
**Status:** proposed_retained exploratory negative / inconclusive for area-law claims

## Question

Does a simple bipartition entropy observable on the retained parity-coupled
staggered self-gravity lane show anything area-law-like or otherwise
publication-interesting?

## Observable

For a single-particle state on a graph and a bipartition `A|B`, define

`p_A = sum_{i in A} |psi_i|^2`

and the binary subsystem entropy

`S(A) = -p_A log p_A - (1-p_A) log(1-p_A)`.

This is intentionally simple. It is **not** a many-body entanglement entropy,
and it is bounded above by `ln(2) = 0.6931`.

## Operating Point

The probe reuses the retained self-gravity lane:

- `MASS = 0.30`
- `MU2 = 0.22`
- `DT = 0.12`
- `G_SELF = 50.0`
- `N_ITER = 20`

Families:

- random geometric (`n=36`)
- growing (`n=48`)
- layered cycle (`n=24`)

Cuts per family:

- `x_half`: geometric half split
- `depth_half`: half split by BFS depth from the source
- `random_half`: equal-volume random split

Control:

- 32-sample equal-volume random-half ensemble per family

## Exact Rerun Numbers

### Random geometric (`n=36`)

| Cut | Boundary | `p_free` | `S_free` | `p_self` | `S_self` | `ΔS = S_self - S_free` |
|---|---:|---:|---:|---:|---:|---:|
| `x_half` | 6 | 0.0953 | 0.3147 | 0.2527 | 0.5652 | +0.2505 |
| `depth_half` | 10 | 0.4515 | 0.6884 | 0.9985 | 0.0110 | -0.6774 |
| `random_half` | 29 | 0.4373 | 0.6853 | 0.8463 | 0.4291 | -0.2562 |

Summary:

- `S_self` range: `0.0110 -> 0.5652`
- 3-cut `corr(boundary, S_self) = +0.122`
- random-half ensemble:
  - boundary range: `26 -> 43`
  - `S_self` range: `0.1480 -> 0.6931`
  - `corr(boundary, S_self) = +0.285`

### Growing (`n=48`)

| Cut | Boundary | `p_free` | `S_free` | `p_self` | `S_self` | `ΔS = S_self - S_free` |
|---|---:|---:|---:|---:|---:|---:|
| `x_half` | 37 | 0.3313 | 0.6351 | 0.4514 | 0.6884 | +0.0533 |
| `depth_half` | 77 | 0.4968 | 0.6931 | 0.7212 | 0.5919 | -0.1013 |
| `random_half` | 94 | 0.5988 | 0.6735 | 0.6073 | 0.6699 | -0.0035 |

Summary:

- `S_self` range: `0.5919 -> 0.6884`
- 3-cut `corr(boundary, S_self) = -0.399`
- random-half ensemble:
  - boundary range: `75 -> 107`
  - `S_self` range: `0.3854 -> 0.6931`
  - `corr(boundary, S_self) = -0.088`

### Layered cycle (`n=24`)

| Cut | Boundary | `p_free` | `S_free` | `p_self` | `S_self` | `ΔS = S_self - S_free` |
|---|---:|---:|---:|---:|---:|---:|
| `x_half` | 8 | 0.3629 | 0.6551 | 0.9990 | 0.0080 | -0.6470 |
| `depth_half` | 12 | 0.5455 | 0.6890 | 0.9773 | 0.1085 | -0.5805 |
| `random_half` | 20 | 0.5531 | 0.6875 | 0.6534 | 0.6453 | -0.0421 |

Summary:

- `S_self` range: `0.0080 -> 0.6453`
- 3-cut `corr(boundary, S_self) = +0.983`
- random-half ensemble:
  - boundary range: `14 -> 26`
  - `S_self` range: `0.1397 -> 0.6930`
  - `corr(boundary, S_self) = +0.489`

## Aggregate Readout

- mean entropy shift across the 9 named cuts: `-0.2227`
- maximum entropy shift across the 9 named cuts: `+0.2505`
- 3-cut boundary correlations by family:
  - random geometric: `+0.122`
  - growing: `-0.399`
  - layered cycle: `+0.983`
- random-half ensemble correlations by family:
  - random geometric: `+0.285`
  - growing: `-0.088`
  - layered cycle: `+0.489`

## Interpretation

This simple entropy observable does **not** currently support an area-law
claim.

What is real:

- self-gravity often **reduces** the bipartition entropy by localizing the
  packet more strongly on one side of the cut
- the effect is topology- and cut-dependent
- layered-cycle localization can drive the entropy close to zero on aligned
  cuts

What is **not** established:

- robust boundary-controlled scaling
- a clean family-universal monotone relation between boundary size and entropy
- anything like black-hole or holographic area-law behavior

The main limitation is structural: for a single-particle state, this binary
subsystem entropy is capped at `ln(2)` and is controlled primarily by the mass
split `p_A`, not by boundary complexity itself.

## Honest Conclusion

This probe is worth keeping, but as a **negative / inconclusive result for
area-law entropy**.

The publication-interesting piece is narrower:

- parity-coupled self-gravity changes subsystem occupancy entropy in a
  topology-sensitive way
- but this simple observable is not yet the right instrument for a serious
  area-law or holography claim

The next credible step would require either:

1. a many-body / multi-orbital fermionic state, or
2. a stronger graph partition observable whose scaling is not trivially bounded
   by `ln(2)`.
