# Lane 5 `(C1)` Carrier/Metrology Axiom Audit Note

**Date:** 2026-04-29
**Status:** support / open boundary audit on `main`; does not close
`(C1)` and does not promote any theorem or claim.
**Runner:** `scripts/frontier_hubble_lane5_c1_carrier_metrology_axiom_audit.py`
**Lane:** 5 -- Hubble constant derivation, `(C1)` absolute-scale gate

## Purpose

This note closes the current Lane 5 `(C1)` stretch sequence honestly. It does
not promote `H_0`, `H_inf`, `a/l_P`, or an SI action unit. It records the
minimal conditional premise that would be needed after the A1/A2/A4/A5/A6
route work.

## Route State Entering This Audit

The current cascade tested five `(C1)` routes.

| Route | Result | Boundary |
|---|---|---|
| A1 Grassmann-to-boundary CAR descent | exact negative boundary | Bulk CAR plus rank-four support needs a `P_A` reducing-module theorem. |
| A2 action-unit metrology from `g_bare`/plaquette/APBC | exact negative boundary | Dimensionless lattice inputs do not choose dimensional `kappa`. |
| A4 parity-gate-to-CAR | exact support/boundary | The gate supplies the half-zone selector inside CAR but does not force CAR. |
| A5 Boolean-coframe restriction | exact negative boundary | Natural full-cell odd coframe generators do not reduce to `P_A`. |
| A6 bilinear active-block route | exact support/boundary | Bilinears generate `M_4(C)` on `P_A`, but do not select the coframe basis or action unit. |

Thus the current stack has not derived `(C1)`. It has narrowed the missing
premise.

## Minimal Conditional Premise

The remaining conditional route has two pieces.

### 1. Active-Block Selector

Supply a primitive metric/orientation/phase selector on the active
one-particle `P_A` algebra:

```text
End(P_A H_cell) ~= M_4(C)
  -> selected metric-compatible Cl_4 coframe basis
  -> selected oriented CAR pairings (t,n) and (tau_1,tau_2).
```

This selector must do more than state that `M_4(C)` can host `Cl_4`; A6
already proves that. It must select the coframe response from the framework's
primitive structure.

### 2. Action-Unit Metrology

Supply a non-rescaling-invariant clock/source/action map:

```text
dimensionless lattice action + primitive boundary/action carrier
  -> selected dimensional action quantum kappa.
```

This must break the A2 degeneracy:

```text
(S_dim, kappa) -> (lambda S_dim, lambda kappa).
```

Without this metrology map, the package can carry native dimensionless phase
and lattice units, but not an absolute dimensional action unit.

## Conditional Consequence If Accepted

If both premises are accepted or derived, then the existing conditional
Planck stack becomes available:

```text
active Cl_4/CAR coframe response
  -> primitive-CAR carrier
  -> parity-gated half-zone selector
  -> c_Widom = c_cell = 1/4
  -> source-unit normalized G_Newton,lat = 1
  -> a/l_P = 1 in natural units.
```

That would supply the `(C1)` absolute-scale premise for the Lane 5 two-gate
Hubble program. It would still need `(C2)` or `(C3)` for numerical `H_0`.

## Current Honest Status

The current status is:

```text
C1 derived from current stack: false
C1 conditional route explicitly stated: true
remaining decision: human science judgment or new selector/metrology theorem
```

This is a human-judgment boundary because accepting the minimal
carrier/metrology premise is a new physical axiom choice unless a later theorem
derives it from `A_min`.

## Runner Witness

The runner checks seven facts.

1. A1, A2, A4, and A5 direct shortcuts are blocked.
2. A6 is capacity-positive but selector-open.
3. The minimal active-block selector premise is explicit.
4. The minimal metrology premise is explicit.
5. The current stack does not derive `(C1)` without those premises.
6. The conditional route is well-formed if the premises are accepted.
7. Lane 5 `(C1)` now requires human science judgment or a new theorem.

Current output:

```text
TOTAL: PASS=7, FAIL=0
```

## Claim Boundary

Safe wording:

> The `(C1)` absolute-scale gate is narrowed to a minimal carrier/metrology
> premise: a primitive selector for the active `Cl_4` coframe response on
> `P_A H_cell` plus a non-rescaling-invariant action-unit map. The current
> stack has not derived those premises.

Unsafe wording:

> Lane 5 `(C1)` is retained because the conditional premise is now explicit.

Explicit conditional premises are not derivations. They are useful only if the
review process accepts them as axioms, or if a later theorem derives them.

## Cascade Decision

This note justifies treating Lane 5 `(C1)` as blocked for the current cascade
unless a fresh selector/metrology theorem appears. It does **not** by itself
create an all-lane stop condition; the cascade must still check the remaining
queued lanes for fresh viable premises before stopping.
