# Top-Yukawa Same-1PI Scalar-Pole Boundary

**Date:** 2026-05-01  
**Status:** exact negative boundary / same-1PI not PR230 closure  
**Runner:** `scripts/frontier_yt_same_1pi_scalar_pole_boundary.py`  
**Certificate:** `outputs/yt_same_1pi_scalar_pole_boundary_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for same-1PI use after independent scalar LSZ normalization
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The same-1PI route does not independently fix scalar LSZ/pole normalization."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The same-1PI route is the most tempting way to repair the old Ward lane:
equate the scalar-singlet four-fermion coefficient in the one-gluon-exchange
representation and in a scalar-exchange representation.

This note checks whether that route already closes PR #230.  It does not.

## Runner Result

```text
python3 scripts/frontier_yt_same_1pi_scalar_pole_boundary.py
# SUMMARY: PASS=6 FAIL=0
```

The runner verifies:

| Check | Result |
|---|---|
| same-1PI note uses `H_unit` / `F_Htt` Rep-B data | pass |
| Rep-B note defines `F_Htt` through the `H_unit` matrix element | pass |
| same-1PI and Rep-B ledger rows are not clean PR #230 authorities | pass |
| prior Ward-decomposition no-go already flags the same-1PI boundary | pass |
| a fixed four-fermion coefficient allows different scalar vertex normalizations | pass |

## Core Obstruction

A four-fermion exchange coefficient fixes the product

```text
Gamma^(4) = y^2 D_phi.
```

It does not separately fix `y` and the scalar propagator normalization
`D_phi`.  Under a scalar field/source rescaling,

```text
y -> kappa y,
D_phi -> D_phi / kappa^2,
```

the same `Gamma^(4)` is preserved while the external scalar-leg readout changes.

## Consequence

The same-1PI route can only become useful for PR #230 after an independent
theorem fixes:

```text
scalar pole residue / canonical normalization
+ physical scalar carrier
+ external scalar LSZ factor
```

Until then, same-1PI coefficient equality is not an audit-clean physical
top-Yukawa readout.  It risks re-entering the old `H_unit` matrix-element
definition trap.

## Non-Claims

- This note does not reject the same-1PI `g_bare` support route in its own scope.
- This note does not promote PR #230.
- This note does not define `y_t` through `H_unit`.
- This note does not use observed top mass or Yukawa values.
