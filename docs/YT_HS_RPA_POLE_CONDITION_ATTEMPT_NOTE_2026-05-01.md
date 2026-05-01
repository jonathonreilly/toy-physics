# Top-Yukawa HS/RPA Pole-Condition Attempt

**Date:** 2026-05-01  
**Status:** exact negative boundary / HS-RPA contact route open only with a new kernel theorem  
**Runner:** `scripts/frontier_yt_hs_rpa_pole_condition_attempt.py`  
**Certificate:** `outputs/yt_hs_rpa_pole_condition_attempt_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support if a retained scalar-channel ladder/eigenvalue theorem is supplied
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The contact HS/RPA route needs a new scalar-channel coupling or kernel-reduction theorem."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The scalar-residue fan-out selected the HS/RPA pole route as the next
constructive attack.  This note tests whether the exact source bubble from the
previous stretch attempt can be promoted to a scalar pole-residue theorem on
the current `A_min` surface.

It cannot, unless a new scalar-channel kernel theorem is supplied.

## Setup

The exact source-bubble step gives a curvature `Pi(p)`.  A contact
Hubbard-Stratonovich / RPA scalar propagator would have the schematic inverse

```text
D_H(p)^-1 = G^-1 - Pi(p).
```

A scalar pole requires

```text
G^-1 = Pi(p_pole).
```

The problem is that `A_min` contains the Wilson gauge action and staggered
Dirac operator, but no independent local scalar contact coupling `G`.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_hs_rpa_pole_condition_attempt.py
# SUMMARY: PASS=9 FAIL=0
```

The runner checks:

| Check | Result |
|---|---|
| `A_min` has Wilson gauge + staggered Dirac | pass |
| `A_min` has no independent local four-fermion scalar contact | pass |
| prior Ward-decomposition no-go already blocks HS-to-Higgs identification | pass |
| RPA pole condition is a one-parameter family | pass |
| collapsing gauge exchange to contact `G` is scale-dependent | pass |
| full ladder route needs an eigenvalue crossing theorem | pass |

For the source-bubble fit used in the diagnostic, different target pole
locations require different contact couplings:

| target `p_hat^2` | required `G^-1` |
|---:|---:|
| `0.05` | `0.081374744241` |
| `0.10` | `0.079770138464` |
| `0.20` | `0.076790216010` |
| `0.50` | `0.069510659516` |
| `1.00` | `0.066940379644` |

Likewise, replacing Wilson gauge exchange by a contact proxy `1/q_hat^2`
depends on the chosen collapse scale; scanning `q_hat^2 in {0.05,0.10,0.20,
0.50,1.00}` gives a factor-20 spread.

## Boundary

The contact HS/RPA route is not closed by the current retained action.  It
would become a real positive route only after a theorem derives:

1. the scalar-channel Bethe-Salpeter/RPA kernel from Wilson gauge exchange;
2. the kernel eigenvalue crossing that creates the Higgs-carrier pole;
3. the pole residue from the derivative of that eigenvalue at the pole.

That theorem would be a genuine interacting scalar pole theorem, not a
rewording of the old Ward route.

## Non-Claims

- This note does not add a scalar contact coupling to `A_min`.
- This note does not identify an HS field with `H_unit` by definition.
- This note does not use observed top or Higgs data.
- This note does not close retained `y_t`.
