# Quark Route-2 Exact Time Coupling

**Date:** 2026-04-19  
**Status:** exact conditional coupling family plus induced exact obstruction  
**Primary runner:** `scripts/frontier_quark_route2_exact_time_coupling.py`

## Safe statement

The Route-2 slice backbone is already exact on the current branch:

```text
Lambda_R exact SPD
T_R = exp(-Lambda_R)
V_R(t) = exp(-t Lambda_R) u_*.
```

So once an admissible readout map `P_R` is supplied, the branch now supports
the exact conditional spacetime family

```text
Xi_P(t ; c) = (P_R c) ⊗ V_R(t)
```

on the restricted carrier class `c`.

But the readout theorem from
[QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md](./QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md)
does not land. Therefore the current stack still does **not** determine one
unique exact `Theta_R -> Lambda_R` time-coupling law.

The honest endpoint is:

- exact slice generator / transfer backbone,
- exact conditional readout-to-slice coupling family,
- and an exact time-coupling obstruction induced by the unresolved readout map.

## 1. Exact slice backbone

The runner recomputes the live Route-2 slice data directly from the current
Schur boundary module.

On this branch:

```text
Lambda_R symmetry error = 3.33e-16
Lambda_R min eigenvalue = 1.148587
T_R symmetry error      = 9.96e-16
T_R eigenvalues         in (0, 1).
```

So the slice backbone remains exact and contractive. The seed law

```text
V_R(t) = exp(-t Lambda_R) u_*
```

also satisfies the exact semigroup composition law.

## 2. Exact conditional coupling family

Given any admissible readout map `P_R`, the smallest exact readout-to-slice
carrier is

```text
Xi_P(t ; c) = (P_R c) ⊗ exp(-t Lambda_R) u_*.
```

This is exact because:

1. the carrier column `c` is exact,
2. the map `P_R` is algebraic once chosen,
3. the slice factor `exp(-t Lambda_R) u_*` is exact.

So the branch does not lack an exact Route-2 carrier-to-slice family. What it
lacks is a theorem that selects one unique `P_R`.

## 3. Induced obstruction from the readout map

The runner makes the obstruction explicit using the reduced exact family

```text
P(rho_E) = [[1, 0, rho_E, 0],
            [0, -2, 0, 2]].
```

At the shell `E` column, all such maps agree:

```text
Xi_P(t ; E-shell)  is independent of rho_E.
```

But at the center `E` column,

```text
Xi_P(t ; E-center)
```

depends on

```text
1 + rho_E / 6.
```

So `rho_E = 0` and `rho_E = 21/4` produce the same exact shell coupling but
different exact center couplings on the same slice backbone.

That proves the obstruction:

> unresolved readout exactness is not a small numerical annoyance; it changes
> the spacetime tensor source factor itself, so it blocks a unique exact
> `Theta_R -> Lambda_R` time-coupling theorem on the current carrier.

## 4. Relation to the exact bilinear carrier

This note is specifically about the readout-driven law

```text
Theta_R -> Lambda_R.
```

It does **not** retract the exact bilinear-carrier construction already on the
branch. The exact carrier-side family built from `K_R` still exists.

The sharper point is narrower:

- exact carrier-side coupling exists,
- exact readout-to-slice coupling does not yet exist as a unique theorem,
- because the readout map itself remains unresolved.

## Honest endpoint

The Route-2 time-coupling block now ends cleanly at:

- exact `Lambda_R` / `T_R` backbone,
- exact conditional family `Xi_P`,
- exact induced obstruction from the missing readout map.

So the next theorem target is no longer “invent a time law.” It is:

> derive the exact readout map entry that removes the source-side ambiguity.

## Validation

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_time_coupling.py
```

Current expected result on this branch:

- `frontier_quark_route2_exact_time_coupling.py`: `PASS=8 FAIL=0`
