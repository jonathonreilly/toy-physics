# Majorana Self-Dual Staircase-Lift Obstruction Theorem

**Date:** 2026-04-15
**Status:** exact frontier boundary after the local self-dual selector theorem
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_self_dual_staircase_lift_obstruction.py`

## Question

After the exact local axis-exchange theorem selects the self-dual point

`rho = 1`

on the background-normalized Majorana block, does the **current exact stack**
now lift that point to an absolute Majorana staircase anchor?

Equivalently:

- maybe the local finite-point selector was the last missing ingredient
- maybe the current `Z_3` lift can now embed that selected point into a unique
  staircase level
- maybe the branch no longer needs any new non-homogeneous bridge once the
  local self-dual point is exact

## Bottom line

No.

The exact local self-dual point is still only **projective** on the current
stack.

Once the admitted local Majorana family is background-normalized and the exact
axis-exchange selector is imposed, the selected local family reduces to the
positive ray

`K_sd(lambda) = lambda (sigma_z + sigma_x)`, `lambda > 0`.

All retained exact local selected observables on that family are identical
across `lambda`:

- `rho = 1`
- `W_rel = (1/2) log 2`
- `Q_rel = 1`

The current three-generation `Z_3` lift is still homogeneous under the same
positive rescaling:

`Delta_lambda(M_0) = lambda (M_0 \otimes J_2)`.

So the exact selected local point does **not** by itself lift to an absolute
staircase anchor on the present stack.

The remaining blocker sharpens again:

> full closure now requires a genuinely new non-homogeneous local-to-generation
> bridge, or a new absolute-scale datum, beyond the current exact stack

## Inputs

This theorem combines:

- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_BACKGROUND_NORMALIZATION_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md](./NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md)
- [NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md)

Those notes already prove:

1. the genuinely new one-generation source increment is fixed up to rephasing
   to the pure-pairing ray
2. the admitted local block carries the exact normalized response
   `W_rel = (1/2) log(1 + rho^2)`, `Q_rel = rho^2`
3. exact axis exchange forces the unique positive local selector `rho = 1`
4. the current exact source stack remains homogeneous under positive rescaling
5. the current three-generation `Z_3` lift can shape a pairing texture but
   cannot activate or normalize it absolutely

So the remaining loophole is now narrower:

> maybe the exact local self-dual point is itself the missing staircase bridge

## Exact theorem

### 1. The selected local self-dual family is one positive ray

On the admitted local family

`H(z,x,y) = z sigma_z + x sigma_x + y sigma_y`,

background normalization reduces the selector problem to the ratio

`rho^2 = (x^2 + y^2) / z^2`.

The source-ray theorem plus local rephasing reduce the genuinely new increment
to the canonical pairing axis, and the axis-exchange fixed-point theorem then
forces

`rho = 1`.

Therefore the exact selected local family is

`K_sd(lambda) = lambda (sigma_z + sigma_x)`, `lambda > 0`.

So the selected local object is one positive ray, not an absolute point in the
un-normalized source space.

### 2. All retained exact local selected observables are identical on that ray

On the exact selected family:

- `rho = 1`
- `W_rel = (1/2) log 2`
- `Q_rel = 1`

for every positive `lambda`.

So the current exact local data after selection are insensitive to the overall
rescaling of the selected family.

### 3. The current three-generation lift is still homogeneous

Take any nonzero symmetric generation representative `M_0` on the current
retained `Z_3` texture class and form the canonical pairing block

`Delta_lambda(M_0) = lambda (M_0 \otimes J_2)`.

Then under positive rescaling:

- the normalized pairing block is unchanged
- the normalized singlet/doublet spectrum is unchanged
- the charge sector remains exactly charge `-2`

So the current generation lift still organizes one texture **class** up to
overall scale only.

### 4. Therefore the exact local self-dual point does not lift to an absolute
staircase anchor on the current stack

The exact local selector removes the local finite-point ambiguity, but the
current exact local selected data are projective and the current retained
generation lift remains homogeneous under the same rescaling.

So the branch still cannot distinguish:

- `k = 7`
- `k = 8`
- or any other absolute staircase placement

from the current exact self-dual-selected Majorana data alone.

## The theorem-level statement

**Theorem (Self-dual staircase-lift obstruction on the current exact Majorana
stack).**
Assume:

1. the admitted local source ray up to rephasing
2. the exact background-normalized local response curve
3. the exact local axis-exchange fixed-point selector `rho = 1`
4. the current retained three-generation `Z_3` texture lift
5. the current exact rescaling homogeneity of that source/texture stack

Then:

1. the selected local self-dual family is the positive ray
   `K_sd(lambda) = lambda (sigma_z + sigma_x)`
2. the retained exact local selected observables are identical across that ray
3. the current retained three-generation lift is homogeneous under the same
   positive rescaling
4. therefore the exact local self-dual point does not by itself lift to an
   absolute Majorana staircase anchor on the present stack

Equivalently: the remaining missing object is no longer a local finite-point
selector. It is a new non-homogeneous local-to-generation bridge or absolute-
scale datum beyond the current stack.

## What this closes

This closes the last obvious loophole of the form:

- maybe the exact local self-dual point `rho = 1` is already enough to fix the
  Majorana staircase level on the current stack

Answer: no.

So the branch no longer needs vague wording like:

> maybe one more theorem on the current selected local point will finish the
> staircase law

The current exact stack is now sharper than that.

## What this does not close

This note does **not** prove:

- that no future local-to-generation bridge can be found
- that no future absolute-scale datum can be derived
- that the universal-theory program is ruled out

It is an exact obstruction theorem on the **current exact stack only**.

## Consequence for DM

For the DM denominator this means:

- the retained local Dirac suppression theorem is exact
- the local Majorana selector now has an exact self-dual point
- but the present stack still does not lift that point to the absolute
  right-handed-neutrino staircase level

So full zero-import `eta`, and therefore full zero-import DM closure, is still
not available on the current stack.

## Safe wording

**Can claim**

- the exact local Majorana self-dual point is now closed
- the current exact stack still does not lift that point to an absolute
  staircase anchor
- the remaining missing object is a new non-homogeneous local-to-generation
  bridge or absolute-scale datum beyond the current stack

**Cannot claim**

- that the final staircase law is impossible in principle
- that no future extension of the framework can close the lane

## Command

```bash
python3 scripts/frontier_neutrino_majorana_self_dual_staircase_lift_obstruction.py
```
