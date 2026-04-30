# Lane 5 `(C1)` A6 Bilinear Active-Block Support/Boundary Note

**Date:** 2026-04-29
**Status:** support / current-surface boundary result on `main`; does
not close `(C1)` and does not promote any theorem or claim.
**Runner:** `scripts/frontier_hubble_lane5_c1_a6_bilinear_active_block_support_boundary.py`
**Lane:** 5 -- Hubble constant derivation, `(C1)` absolute-scale gate

## Purpose

A5 blocked the most literal inherited-coframe shortcut: the natural full-cell
odd coframe generators shift Hamming weight, so they do not restrict to
`P_A H_cell`.

This note tests the surviving quotient/bilinear route:

```text
Do number-preserving bilinears a_i^dagger a_j on the one-particle P_A sector
at least supply enough active-block algebra to host an intrinsic Cl_4
coframe response?
```

The answer is yes as support, but not as closure. The bilinears generate the
full active matrix algebra `M_4(C)` on `P_A H_cell`, so an intrinsic `Cl_4`
response can live there. However, the bilinear algebra alone does not select a
unique metric coframe basis, oriented pairing, phase convention, or
dimensional action unit. A selector/metrology theorem remains load-bearing.

## Minimal Premises Used

- The time-locked primitive event cell:

  ```text
  H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16.
  ```

- The Hamming-weight-one packet:

  ```text
  P_A = P_{|S|=1},   rank(P_A)=4,   c_cell=1/4.
  ```

- Standard four-mode CAR creation/annihilation operators used as finite
  algebra infrastructure.
- Number-preserving bilinears `a_i^dagger a_j`.

No measured value of `G`, `hbar`, `M_Pl`, `H_0`, or any cosmological
observable enters this support/boundary result.

## Positive Support Result

On the one-particle sector `P_A H_cell`, the bilinears

```text
E_ij = P_A a_i^dagger a_j P_A
```

act exactly as matrix units:

```text
E_ij E_kl = delta_jk E_il.
```

Therefore they generate

```text
End(P_A H_cell) ~= M_4(C).
```

Since complex `Cl_4(C) ~= M_4(C)`, the active-block algebra is large enough to
host the metric-compatible Clifford response used in the Target 3 Clifford
phase bridge. This is the constructive content left after A5:

```text
direct odd restriction fails,
but number-preserving bilinears make an intrinsic active-block Cl_4 possible.
```

## Boundary Result

Existence is not selection. The same bilinear algebra admits many distinct
`Cl_4` presentations:

- active basis permutations conjugate one valid `Cl_4` basis into another;
- continuous active-basis phase rotations also preserve the bilinear algebra
  while changing the Clifford presentation;
- the common `(S,kappa)` action-unit rescaling degeneracy remains unchanged.

Thus the bilinear route does not by itself identify:

```text
which four active generators are the primitive metric coframe axes,
which oriented pairing gives (t,n) and (tau_1,tau_2),
which phase convention is the native action unit,
or which dimensional kappa is selected.
```

The missing theorem is now sharper:

```text
derive a primitive metric/orientation/phase selector on the bilinear
one-particle P_A algebra, plus a non-rescaling-invariant action-unit map.
```

## Runner Witness

The runner checks nine facts.

1. The one-particle `P_A` sector has rank four and `c_cell=1/4`.
2. The number-preserving bilinears generate a `16`-dimensional active algebra.
3. The bilinears recover all `4 x 4` matrix units on `P_A`.
4. The matrix units obey the expected multiplication law.
5. The active bilinear algebra can host a `Cl_4` response.
6. The same bilinear algebra admits a distinct permuted `Cl_4` basis.
7. A continuous active-basis phase rotation is also not fixed by the bilinear
   algebra.
8. The bilinear route does not pin a dimensional action unit.
9. The exposed blocker is selector/metrology, not algebraic existence.

Current output:

```text
TOTAL: PASS=9, FAIL=0
```

## Claim Boundary

Safe wording:

> Number-preserving bilinears on the one-particle `P_A` sector generate the
> full active matrix algebra, so an intrinsic active-block `Cl_4` response is
> algebraically possible. The bilinear algebra alone does not select the
> metric coframe basis or action-unit map.

Unsafe wording:

> The bilinear active-block algebra derives the primitive Clifford/CAR coframe
> response and closes `(C1)`.

That stronger statement is blocked by the selector and metrology ambiguity
above.

## Consequence For Lane 5 `(C1)`

A6 narrows the remaining `(C1)` problem. The route is no longer blocked by
active-block algebraic capacity. It is blocked by selection:

```text
M_4(C) capacity on P_A H_cell
  + missing primitive metric/orientation/phase selector
  + missing action-unit metrology
  => no retained C1 closure yet.
```

The next honest step is either a theorem that supplies this selector, or a
minimal carrier/metrology axiom audit that records the human science-judgment
boundary explicitly.
