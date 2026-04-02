# Asymmetry Persistence Joint Card Note

**Date:** 2026-04-02  
**Status:** dense same-graph joint card complete

## Question

The generated asymmetry-persistence lane already showed improvements in
`pur_cl`, and it stacked strongly with layer norm on `pur_min`.

The missing check was a one-page same-graph card with:

- `pur_cl`
- `pur_min`
- gravity
- corrected Born metric `|I3|/P`

## Setup

Script:
[scripts/asymmetry_persistence_joint_card.py](/Users/jonreilly/Projects/Physics/scripts/asymmetry_persistence_joint_card.py)

Log:
[logs/2026-04-02-asymmetry-persistence-joint-card.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-02-asymmetry-persistence-joint-card.txt)

Parameters:

- dense 3D generated graphs
- `N=80` with `npl=50`
- `N=100` with `npl=60`
- `8` matched seeds
- thresholds `0.00, 0.10, 0.20`
- linear and layer-normalized propagation both measured
- corrected Sorkin metric includes `-P(empty)`

## Results

### N = 80

| thr | keep% | pur_cl lin | pur_cl ln | pur_min lin | pur_min ln | grav lin | grav ln | Born lin | Born ln |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 100.0 | 0.998 | 0.954 | 0.998 | 0.954 | -0.862 | -0.349 | 1.73e-15 | 4.12e-16 |
| 0.10 | 97.4 | 0.982 | 0.889 | 0.981 | 0.889 | -0.344 | +0.520 | 9.21e-16 | 2.68e-16 |
| 0.20 | 97.2 | 0.981 | 0.881 | 0.981 | 0.881 | -0.297 | +0.485 | 8.78e-16 | 2.36e-16 |

### N = 100

| thr | keep% | pur_cl lin | pur_cl ln | pur_min lin | pur_min ln | grav lin | grav ln | Born lin | Born ln |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 100.0 | 0.989 | 0.944 | 0.989 | 0.943 | +0.946 | +0.784 | 1.24e-15 | 3.01e-16 |
| 0.10 | 98.0 | 0.947 | 0.871 | 0.947 | 0.869 | +1.873 | +1.126 | 9.75e-16 | 2.82e-16 |
| 0.20 | 97.7 | 0.953 | 0.862 | 0.953 | 0.860 | +1.897 | +1.357 | 1.06e-15 | 3.15e-16 |

## Safe interpretation

This lane is now a real same-graph joint positive.

What is established:

- generated hard geometry improves `pur_cl`
- generated hard geometry also improves `pur_min`
- layer norm stacks strongly on the same generated graphs
- corrected Born remains machine-clean throughout
- at `N=100`, gravity stays positive and is compatible with the
  persistence rule under both linear and layer-normalized propagation

Important nuance:

- `N=80` is directionally encouraging but not a strong gravity
  significance point; the main clean gravity coexistence row is `N=100`
- `pur_cl` and `pur_min` are nearly identical on these dense generated
  graphs, suggesting the decoherence floor is doing most of the work

Boundary check:

- a denser `N=120` probe (`npl=70`, `4` seeds) keeps corrected Born
  clean and still lowers `pur_min` under layer norm (`0.986 -> 0.946`),
  but gravity stays negative on all tested rows
- so the retained same-graph coexistence claim should stop at dense
  `N=100`, not `N=120`

## Bottom line

Generated asymmetry persistence has moved from “interesting mechanism
pilot” to a retained bounded joint lane.

It is still not an asymptotic rescue, but it now supports all four of:

1. topology-generated geometry
2. improved `pur_cl`
3. improved `pur_min`
4. Born-clean coexistence with positive gravity on dense `N=100`

The honest range for that claim is now: **dense `N=80-100`, bounded
before `N=120`**.
