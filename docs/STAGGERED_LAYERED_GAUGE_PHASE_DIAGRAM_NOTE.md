# Staggered Layered Gauge Phase Diagram Note

**Date:** 2026-04-10  
**Status:** proposed_retained phase-diagram probe

This note freezes the geometry sweep that turns the layered gauge holdout into
an explicit criterion on the same graph-native staggered transport law.

## Question

Which layered graph features control native gauge/current closure?

The sweep varied:

- loop size
- loop density
- wrap/open choice
- local plaquette quality

## Harness

- Script:
  [`frontier_staggered_layered_gauge_phase_diagram.py`](../scripts/frontier_staggered_layered_gauge_phase_diagram.py)
- Operator: native staggered Hamiltonian with flux threaded through the detected
  cycle edge
- Observable: ground-state persistent-current span over `phi in [0, 2pi]`
- Retained side battery: Born/linearity, norm, force sign, `F∝M`, achromatic
  force, equivalence, robustness

## Exact Results

### Reference controls

| Family | n | Layers | Width | wrap | step | Gauge | J span | Notes |
|---|---:|---:|---:|---|---:|---|---:|---|
| `layered_dag_control` | 36 | 8 | 5 | open | 1 | `N/A` | `N/A` | acyclic control |
| `layered_sparse_holdout` | 55 | 10 | 6 | open | 1 | `FAIL` | `4.769e-06` | the original layered holdout |

### Brickwall class, step = 1

| Family | n | wrap | step | Gauge | J span |
|---|---:|---|---:|---|---:|
| `brickwall_w4_s1_open` | 32 | open | 1 | PASS | `4.260e-03` |
| `brickwall_w4_s1_wrap` | 32 | wrap | 1 | PASS | `5.204e-03` |
| `brickwall_w6_s1_open` | 48 | open | 1 | PASS | `1.145e-03` |
| `brickwall_w6_s1_wrap` | 48 | wrap | 1 | PASS | `3.006e-03` |
| `brickwall_w8_s1_open` | 64 | open | 1 | PASS | `4.906e-04` |
| `brickwall_w8_s1_wrap` | 64 | wrap | 1 | PASS | `1.537e-03` |

### Long-shift layered loops

| Family | n | wrap | step | Gauge | J span |
|---|---:|---|---:|---|---:|
| `brickwall_w4_s2_open` | 32 | open | 2 | FAIL | `1.107e-31` |
| `brickwall_w4_s2_wrap` | 32 | wrap | 2 | FAIL | `9.072e-19` |
| `brickwall_w6_s2_open` | 48 | open | 2 | FAIL | `1.013e-18` |
| `brickwall_w6_s2_wrap` | 48 | wrap | 2 | FAIL | `8.709e-34` |
| `brickwall_w8_s2_open` | 64 | open | 2 | FAIL | `5.213e-19` |
| `brickwall_w8_s2_wrap` | 64 | wrap | 2 | FAIL | `4.416e-19` |
| `brickwall_w4_s3_open` | 32 | open | 3 | PASS | `1.199e-02` |
| `brickwall_w4_s3_wrap` | 32 | wrap | 3 | PASS | `1.379e-03` |
| `brickwall_w6_s3_open` | 48 | open | 3 | FAIL | `1.812e-18` |
| `brickwall_w6_s3_wrap` | 48 | wrap | 3 | FAIL | `2.335e-31` |
| `brickwall_w8_s3_open` | 64 | open | 3 | FAIL | `1.959e-32` |
| `brickwall_w8_s3_wrap` | 64 | wrap | 3 | PASS | `1.430e-03` |

### Defect sweep at step = 1

| Family | n | wrap | step | Gauge | J span |
|---|---:|---|---:|---|---:|
| `defect_q75_open` | 48 | open | 1 | PASS | `5.360e-03` |
| `defect_q75_wrap` | 48 | wrap | 1 | PASS | `4.243e-03` |
| `defect_q50_open` | 48 | open | 1 | PASS | `6.705e-03` |
| `defect_q50_wrap` | 48 | wrap | 1 | PASS | `2.253e-03` |
| `defect_q25_open` | 48 | open | 1 | PASS | `2.235e-03` |
| `defect_q25_wrap` | 48 | wrap | 1 | PASS | `2.548e-03` |

## Boundary Readout

The cleanest retained reading from this sweep is:

- The acyclic layered DAG control is correctly `N/A` for gauge/current.
- The original sparse layered holdout still fails native gauge closure.
- The brickwall plaquette class with nearest-neighbor shift step `1` passes
  robustly for all tested widths and both open/wrap choices.
- Longer-shift layered geometries are unstable: step `2` fails throughout, and
  step `3` is mixed rather than monotone.

## Interpretation

The gauge/current holdout is not controlled by a single scalar such as raw cycle
rank or a simple edge-fraction proxy. The best geometry criterion from this
sweep is a **brickwall-like nearest-neighbor plaquette basis**:

- explicit local plaquettes are the right geometry
- open vs wrap is secondary once the plaquette basis exists
- longer-shift layered loops are not a reliable substitute
- the sparse layered DAG holdout fails because it does not have the same
  local plaquette structure as the brickwall class

The practical pass/fail boundary is therefore:

- **PASS**: layered brickwall / plaquette graphs built from nearest-neighbor
  staggered connections
- **FAIL**: sparse layered holdout graphs and most long-shift layered loop
  geometries
- **N/A**: acyclic layered DAG controls

## Retained Battery

Across all tested families in the sweep, the force battery remained intact:

- Born/linearity stayed at machine precision
- norm drift stayed machine precision
- force stayed TOWARD
- `F∝M`, achromatic force, equivalence, and robustness remained retained

