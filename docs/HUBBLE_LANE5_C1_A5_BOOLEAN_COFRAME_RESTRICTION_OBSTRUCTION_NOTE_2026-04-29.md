# Lane 5 `(C1)` A5 Boolean-Coframe Restriction Obstruction Note

**Date:** 2026-04-29
**Status:** proposed_retained exact negative boundary / stretch-attempt result
on `frontier/lane4-neutrino-cascade-20260427`; does not close `(C1)`.
**Runner:** `scripts/frontier_hubble_lane5_c1_a5_boolean_coframe_restriction_obstruction.py`
**Lane:** 5 -- Hubble constant derivation, `(C1)` absolute-scale gate

## Purpose

After A1, A2, and A4, the remaining constructive `(C1)` route is a direct
`P_A` module-morphism / metric-compatible coframe theorem. This note tests
the most literal version of that route:

```text
Does P_A H_cell inherit the Clifford/CAR coframe response by restricting the
natural odd Boolean/Jordan-Wigner coframe operators on H_cell = (C^2)^4?
```

The answer is no. The natural full-cell odd coframe generators change
Hamming weight. Since `P_A` is the Hamming-weight-one packet, it is not a
reducing submodule for those generators. Their compression to `P_A H_cell` is
zero, not a metric-compatible `Cl_4` response.

This is a narrow obstruction. It does not prove that no intrinsic active-block
coframe theorem can exist. It blocks only the direct restriction shortcut.

## Minimal Premises Used

- The time-locked primitive event cell:

  ```text
  H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16.
  ```

- The primitive carrier:

  ```text
  P_A = P_{|S|=1},   rank(P_A)=4,   Tr((I_16/16)P_A)=1/4.
  ```

- The natural full-cell odd Boolean/Jordan-Wigner coframe generators on
  `(C^2)^4`, used as a concrete candidate inherited coframe response.
- Standard finite Clifford/CAR algebra.

No measured value of `G`, `hbar`, `M_Pl`, `H_0`, or any cosmological
observable enters this obstruction.

## Result

Let `Gamma_i` be the natural full-cell Jordan-Wigner odd generators for the
four primitive axes. They obey the full-cell Clifford relation

```text
{Gamma_i, Gamma_j} = 2 delta_ij I_16.
```

But each `Gamma_i` flips one primitive coframe bit. Acting on a
Hamming-weight-one basis state, it sends the state to Hamming weight zero or
two. Therefore

```text
P_A Gamma_i P_A = 0
```

for every primitive axis `i`, and

```text
[P_A, Gamma_i] != 0.
```

The compressed operators cannot satisfy the metric-compatible active-block
law

```text
(P_A Gamma_i P_A)^2 = P_A.
```

They square to zero, not to the identity on `P_A H_cell`.

The full-cell occupation parity also restricts to a scalar on the
weight-one packet:

```text
P_A (-1)^N P_A = -P_A,
```

so the inherited occupation grading does not supply the two-plus-two
even/odd split used by the two-mode active CAR carrier.

## What Still Survives

The obstruction is not that `C^4` cannot carry `Cl_4`. It can. The runner
constructs an intrinsic active-block `Cl_4(C)` representation on a separate
`C^4` basis and verifies that it generates `M_4(C)`.

The problem is descent:

```text
natural full-cell odd coframe response
  -/-> active rank-four coframe response by restriction to P_A H_cell.
```

A positive theorem must therefore do one of the following:

- construct the active-block coframe response intrinsically on `P_A H_cell`;
- derive a quotient or number-preserving bilinear theorem that selects a
  metric-compatible `Cl_4` basis on the weight-one packet;
- supply a new module-morphism law changing the projection/response relation;
- keep the Clifford/CAR coframe response as an explicit carrier premise.

## Runner Witness

The runner checks nine facts.

1. The Hamming-weight-one packet has `rank(P_A)=4` and `c_cell=1/4`.
2. The natural full-cell Jordan-Wigner coframe generators obey `Cl_4`.
3. `P_A` is not reducing for those odd generators.
4. Each compressed operator `P_A Gamma_i P_A` is zero.
5. The compressed response fails metric compatibility.
6. Every full-cell odd generator shifts each weight-one basis state outside
   `P_A`.
7. Full-cell occupation parity restricts to a scalar on `P_A`.
8. An intrinsic active-block `Cl_4` representation exists, showing the issue
   is descent rather than dimension.
9. The exposed import is an intrinsic active-block coframe law, a
   quotient/bilinear theorem, or an explicit carrier premise.

Current output:

```text
TOTAL: PASS=9, FAIL=0
```

## Claim Boundary

Safe wording:

> The natural full-cell odd Boolean/Jordan-Wigner coframe response does not
> descend to `P_A H_cell` by compression, because the Hamming-weight-one
> packet is not a reducing submodule for the odd coframe generators.

Unsafe wording:

> This proves that no active-block Clifford/CAR coframe theorem can exist.

That stronger statement is not shown. The obstruction is against direct
restriction from the natural full-cell odd coframe maps. An intrinsic or
quotient active-block theorem remains a possible but still open route.

## Relation To Prior `(C1)` Boundaries

- A1 showed that arbitrary bulk CAR plus rank-four support does not force CAR
  on `P_A H_cell` without a projection/morphism theorem.
- A4 showed that the primitive parity gate supplies a selector inside CAR
  semantics but does not force the CAR/coframe response.
- A5 now shows that the most direct inherited full-cell odd coframe response
  also fails, because `P_A` is not reducing for the natural odd generators.

Together these do not close Lane 5. They sharpen the remaining `(C1)` target:

```text
derive an intrinsic active-block metric-compatible Clifford/CAR coframe law,
or keep the carrier/metrology premise explicit.
```
