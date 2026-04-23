# Planck-Scale Boundary Lane Full Assumption Stress Audit

**Date:** 2026-04-23  
**Status:** science-only full-lane assumption audit  
**Audit runner:** `scripts/frontier_planck_boundary_lane_full_assumption_stress_audit.py`

## Question

The Planck boundary lane is now mathematically much sharper than it was at the
start of the day:

- the boundary carrier has been reduced to the exact time-locked Schur carrier
  `L_Sigma`;
- the canonical same-surface transfer law has been isolated and shown to be
  contractive;
- the first exact non-affine vacuum law has been derived,
  `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;
- the action-native pressure law has been reduced to one additive vacuum
  density `nu`;
- the `C^16` lane has isolated the exact coarse quarter-valued scalar
  `m_axis = 1/4`.

That means the boundary lane is no longer blocked by diffuse ambiguity. It is
blocked by a small number of explicit assumptions and bridge choices.

This note audits those assumptions honestly.

## Bottom line

The current Planck boundary lane is **not** being held up by a hidden algebra
bug. It is being held up by three genuinely physical assumptions:

1. the physical closure scalar really is the boundary growth pressure
   `p_* = sup spec(G_Sigma)`;
2. the physical boundary carrier really is the exact time-locked Schur carrier
   rather than some nonlinear/non-Gaussian replacement;
3. one of the current bridge observables really feeds the physical pressure:
   either the non-affine Schur vacuum density `p_vac(L_Sigma)` or the exact
   `C^16` axis-sector mass `m_axis = 1/4`.

The two highest-value assumption reversals are constructive rather than
destructive:

1. reverse the empty-vacuum privilege and derive a nonzero boundary
   vacuum-action density `nu`; on the exact witness that would need
   `nu = 5/4`;
2. reverse the fixed democratic `C^16` / fixed `hw=1` projector choice and
   derive a boundary-induced weighted state or projector from the Schur/Perron
   data themselves.

The third good idea is more conceptual:

3. relax the direct growth-pressure reading and derive a canonical
   thermodynamic conversion from the exact vacuum density
   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)` to the physical pressure,
   e.g. via a large-deviation, Legendre, or relative-entropy theorem.

Those are the best places to push next. Most other assumption reversals merely
reopen older routes or collapse the present lane.

## Exact route snapshot

On the exact rational witness already shared by the boundary notes,

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

the current exact numbers are:

- `lambda_min(L_Sigma) = 1`
- canonical transfer radius:
  `rho(T_can(1)) = e^(-1)`
- non-affine vacuum density:
  `p_vac(L_Sigma) = (1/4) log(5/3) ~= 0.127706`
- action-native pressure family:
  `p_*(nu) = nu - 1`
- required quarter-closing vacuum density:
  `nu = 5/4`
- democratic `C^16` primitive share:
  `m_cell = 1/16`
- democratic `C^16` axis-sector mass:
  `m_axis = 4/16 = 1/4`

So the lane currently has three exact candidate same-surface scalars:

- `p_vac(L_Sigma) = (1/4) log(5/3)`
- `nu - lambda_min(L_Sigma)`
- `m_axis = 1/4`

The remaining scientific burden is to explain which one is physically read out,
or how the physically correct one is canonically converted from the others.

## Classification legend

- `harmless / equivalent reformulation`
  the route survives unchanged; only packaging or reference choice moves.
- `would reopen an older route`
  the present sharpening is lost, but an earlier broader search lane returns.
- `would kill the current route`
  the current boundary-lane framing stops being the right problem.
- `suggests a genuinely new attack direction`
  the reversal does not merely collapse the route; it points to a new theorem
  target.

## Full assumption inventory

| ID | Assumption | If it is wrong | Classification | Load |
| --- | --- | --- | --- | --- |
| `B01` | Writing the target as `p_* = 1/4` is equivalent to writing it as `rho(T(1)) = e^(1/4)` at one clock step. | This mostly changes clock-step or logarithm packaging, not the science. | `harmless / equivalent reformulation` | `1` |
| `B02` | The physical boundary lane lives on the exact time-locked `3+1` surface with `a_s = c a_t`. | The anisotropic family `beta = (c a_t / a_s)^2` reopens and the older pre-lock search over relative spacetime weighting returns. | `would reopen an older route` | `4` |
| `B03` | The physical boundary carrier is faithfully represented by a positive quadratic bulk carrier whose exact boundary reduction is the Schur operator `L_Sigma`. | The Schur/Gaussian/action lane loses its physical footing; the current boundary route dies as framed. | `would kill the current route` | `5` |
| `B04` | The physical boundary dynamics should be read through a one-clock semigroup `T(tau) = exp(tau G)` with a linear generator on the same carrier. | One should search for a resolvent, determinant, KMS, relative-transfer, or other non-semigroup observable instead. | `suggests a genuinely new attack direction` | `4` |
| `B05` | The closure scalar to be explained is really the boundary growth pressure `p_* = sup spec(G_Sigma)`. | The whole quarter-pressure formulation stops being the right target; almost every current boundary statement changes meaning. | `would kill the current route` | `5` |
| `B06` | Normalizing `Z(L_Sigma)` against `Z(I_n)` only removes the universal Gaussian measure factor on the same mode space. | This changes reference bookkeeping more than physics; the non-affine determinant law survives modulo equivalent renormalization. | `harmless / equivalent reformulation` | `1` |
| `B07` | Retaining the exact Schur action really kills multiplicative `lambda` freedom and leaves only one additive vacuum density `nu`. | The older affine normalization obstruction `G -> lambda G + mu I` comes back. | `would reopen an older route` | `3` |
| `B08` | The canonical empty-vacuum reference `I(0;0) = 0`, equivalently `nu = 0`, is physically privileged. | A nonzero boundary vacuum-action density becomes admissible and could directly close the witness through `nu = 5/4`. | `suggests a genuinely new attack direction` | `3` |
| `B09` | The relevant microscopic `C^16` state is the democratic state `rho_cell = I_16 / 16`. | The lane should derive a boundary-induced weighted `C^16` state from Schur/Perron data rather than assume democracy. | `suggests a genuinely new attack direction` | `3` |
| `B10` | The `hw=1` axis-sector projector is the physically correct coarse `3+1` observable cut out of the `C^16` carrier. | A different coarse projector or dynamically induced sector could replace `m_axis = 1/4` as the boundary-matching scalar. | `suggests a genuinely new attack direction` | `3` |
| `B11` | If the `C^16` bridge is right, the physical additive shift / pressure is the exact axis-sector mass `m_axis = 1/4`. | The current `C^16` bridge fails and the program falls back to the older vacuum/action routes. | `would reopen an older route` | `4` |
| `B12` | If the non-affine vacuum law matters physically, the physical pressure equals or is canonically converted from `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`. | The determinant law becomes bookkeeping only, and one must close the lane through `nu` or `m_axis` instead. | `would reopen an older route` | `4` |
| `B13` | Once the democratic state and axis projector are fixed, `m_axis = 4 m_cell` is just coarse/fine repackaging, not new physics. | This changes notation only; the same quarter-valued scalar remains. | `harmless / equivalent reformulation` | `1` |

## What the audit says assumption by assumption

### `B01`, `B06`, `B13` are packaging assumptions

These are not where the science risk lives.

- `B01` is just target packaging:
  `p_* = 1/4` versus `rho(T(1)) = e^(1/4)`.
- `B06` is just vacuum-reference packaging:
  `Z(L_Sigma)` versus `Z(L_Sigma) / Z(I_n)`.
- `B13` is just `C^16` packaging:
  coarse axis-sector mass versus four fine primitive shares.

If any of these are "wrong", the lane does not really change.

### `B02`, `B07`, `B11`, `B12` are route-selection assumptions

If these fail, the present sharpened lane does not disappear, but it loses one
of its hard-earned reductions and returns to an older broader search.

- `B02` reopens anisotropic spacetime weighting.
- `B07` reopens the old affine normalization family.
- `B11` reopens the pre-`C^16` boundary bridge search.
- `B12` reopens the pre-determinant bridge search.

These are important, but they do not by themselves invalidate the overall
Planck program.

### `B03` and `B05` are the hardest route-defining assumptions

These are the genuinely load-bearing ones.

- `B03` says the whole boundary lane should be organized around the exact
  time-locked Schur carrier.
- `B05` says the quantity that matters physically is the boundary growth
  pressure `p_*`.

If either of these is wrong, the present boundary lane is not the right lane
to close.

### `B04`, `B08`, `B09`, `B10` are the good reversal points

These are the most useful assumptions to challenge because reversing them does
not just collapse the lane. It suggests new science.

- `B04`: maybe the right readout is not a linear semigroup pressure but a
  resolvent, determinant, KMS, or relative-transfer object.
- `B08`: maybe the boundary worldtube carries a nonzero vacuum-action density.
- `B09`: maybe the microscopic boundary state is not democratic.
- `B10`: maybe the correct coarse projector is not the hand-selected `hw=1`
  axis sector.

Those are the places where a new theorem could still move the program
forward.

## Most load-bearing assumptions

### 1. `B05` -- the physical observable grammar is growth pressure

This is the most load-bearing assumption in the whole lane.

Everything currently called "quarter" is really the statement

`p_* = sup spec(G_Sigma) = 1/4`.

If that is not the physical scalar, then the entire boundary-quarter framing is
mis-aimed.

### 2. `B03` -- the physical boundary carrier is the exact time-locked Schur carrier

This is the carrier-side counterpart of `B05`.

If the true boundary object is not the Schur/Gaussian/action carrier, then the
present exact formulas

- `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`
- `p_*(nu) = nu - lambda_min(L_Sigma)`
- `L_Sigma = [[4/3,1/3],[1/3,4/3]]`

stop being the right same-surface witnesses.

### 3. Third place splits between the two bridge assumptions

The third load-bearing slot is not one clean winner. It is a split:

- `B11`: the `C^16` bridge assumption
  `physical pressure = m_axis`;
- `B12`: the vacuum/determinant bridge assumption
  `physical pressure = p_vac` or a canonical conversion of it.

At least one bridge family has to become physical, or the boundary lane stays
mathematically sharp but scientifically open.

## Plausible new derivation ideas from assumption reversals

### Idea 1: derive a nonzero boundary vacuum-action density

This is the best concrete idea in the whole audit and comes from reversing
`B08`.

The action lane already reduced the witness to

`p_*(nu) = nu - 1`.

So exact quarter is equivalent to

`nu = 5/4 = 1 + 1/4 = lambda_min(L_Sigma) + m_axis`.

That is a very sharp same-surface theorem target:

> derive a nonzero boundary vacuum-action density on the exact worldtube.

This is much better than redoing the whole boundary search.

### Idea 2: derive a boundary-induced weighted `C^16` state or projector

This comes from reversing `B09` and `B10`.

Right now the `C^16` bridge is strong but still partially hand-cut:

- the state is democratic,
- the projector is the `hw=1` axis sector,
- then `m_axis = 1/4`.

A better theorem would derive either:

- a weighted microscopic state from the Schur/Perron boundary data, or
- a canonical projector/sector from the boundary/worldtube dynamics.

That would turn the current `C^16` bridge from "exact matching scalar" into a
genuinely induced observable.

### Idea 3: derive a thermodynamic conversion from `p_vac` to `p_*`

This comes from relaxing `B05` and `B12` without abandoning the exact vacuum
law.

The determinant route already gave a first exact non-affine scalar:

`p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

What is missing is a theorem explaining why the physical growth pressure is
equal to, or canonically converted from, that vacuum free-energy density.

The most plausible mathematical shapes are:

- a large-deviation pressure theorem,
- a Legendre transform,
- a relative-entropy / free-energy conversion,
- or a determinant-to-growth comparison theorem on the same boundary carrier.

This is better than simply declaring `p_* = p_vac`.

## Honest verdict

The current boundary lane is not blocked by dozens of assumptions. It is
blocked by a small handful.

Three assumptions are genuinely route-defining:

- `B05` growth-pressure observable grammar,
- `B03` time-locked Schur carrier choice,
- and the bridge cluster `B11` / `B12`.

The most promising reversals are not "throw the lane away." They are:

1. derive `nu = 5/4` from same-surface boundary vacuum physics;
2. derive a boundary-induced weighted `C^16` state or coarse projector;
3. derive a canonical thermodynamic conversion from `p_vac(L_Sigma)` to the
   physical pressure.

Everything else is either packaging or a route-selection choice that mostly
reopens an older search lane.
