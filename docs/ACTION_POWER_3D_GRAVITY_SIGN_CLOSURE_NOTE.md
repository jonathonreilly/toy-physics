# Action-Power 3D Barrier Gravity-Sign Closure

**Date:** 2026-04-04  
**Status:** bounded negative result on the current ordered 3D power-action family

## Question

Can the retained 3D close-slit power-action barrier card recover **gravity
toward mass** on the current ordered lattice family by changing only:

- field strength
- forward-connectivity density
- geometric jitter with fixed NN-style topology

## Fixed family

- 3D ordered forward lattice
- `L = 12`, `W = 6`, `h = 1.0`
- action `S = L |f|^0.5`
- close-slit barrier:
  - slit A: `(2, 0)`
  - slit B: `(-2, 0)`
- detector: full last layer
- observable: detector `z`-centroid shift

This note is intentionally narrower than the main action-power harness. It
only asks whether the **sign** of the 3D barrier gravity observable can flip
from away to toward on the current ordered family.

## Results

### 1. Field-strength weakening fails

On the NN topology (`9` edges/node), with `mass_z = 3` and `mass_z = 6`,
the gravity sign stays **away** across the tested window:

- `strength = 1e-5 .. 1e-3`
- toward count: `0/14`

### 2. Denser forward connectivity fails

Increasing next-layer connectivity also fails to recover attraction:

- span `1` -> `9` edges/node
- span `2` -> `25` edges/node
- span `3` -> `49` edges/node

All tested rows stay **away** at the retained close-slit barrier geometry.

### 3. Geometric jitter fails

Random position perturbations with the same NN topology also fail:

- jitter `0.0, 0.1, 0.3, 0.5`
- `8` seeds at each jitter
- toward count: `0/8` at every tested jitter

The mean shift becomes slightly more negative at larger jitter, so geometric
noise does not rescue the sign.

## Honest read

This closes the current 3D ordered-family barrier-sign lane as a **bounded
negative**:

- the action-power branch **does** retain a real 3D barrier card for Born /
  `k=0` / MI / `d_TV` / decoherence
- it **does** retain a 3D no-barrier companion with `1/b^2`-like distance
  scaling and nearly linear mass response
- it **does not** retain barrier attraction on the current ordered 3D family

So the safe synthesis is:

- **3D no-barrier law behavior** is real on this branch
- **3D barrier attraction** is not recovered by the current bounded ordered
  follow-up sweeps

## What this does NOT close

- a future topology-changing 3D family
- continuum-limit rescue beyond the current ordered-family finite harness
- other action families

It only closes the current ordered-family 3D power-action barrier lane.

## Artifact chain

- [`scripts/action_power_3d_gravity_sign_closure.py`](/Users/jonreilly/Projects/Physics/scripts/action_power_3d_gravity_sign_closure.py)
- [`logs/2026-04-04-action-power-3d-gravity-sign-closure.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-action-power-3d-gravity-sign-closure.txt)
