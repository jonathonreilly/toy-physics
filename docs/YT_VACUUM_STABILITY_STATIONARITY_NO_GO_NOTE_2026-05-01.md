# YT Vacuum-Stability Stationarity No-Go Note

**Date:** 2026-05-01
**Status:** no-go / exact-negative-boundary on the current substrate surface
**Runner:** `scripts/frontier_yt_vacuum_stability_stationarity_no_go.py`
**Certificate:** `outputs/yt_vacuum_stability_stationarity_no_go_2026-05-01.json`

```yaml
actual_current_surface_status: no-go / exact-negative-boundary
conditional_surface_status: "A multiple-point or double-zero theorem could reopen the route if derived from the substrate."
hypothetical_axiom_status: "Planck tangency / double-criticality: beta_lambda(M_Pl)=0."
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "One-sided vacuum stability gives an inequality, not beta_lambda(M_Pl)=0."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

Can the framework derive the missing stationarity condition from a weaker
vacuum-stability premise?

The tested route is:

```text
lambda(M_Pl) = 0
lambda(mu < M_Pl) >= 0 near the boundary
therefore beta_lambda(M_Pl) = 0 ?
```

## Verdict

No.

At an upper boundary, one-sided local stability gives a sign inequality, not a
tangency equality.  With `t = log(mu)` and `epsilon > 0`,

```text
lambda(t_Pl - epsilon)
  = lambda(t_Pl) - epsilon beta_lambda(t_Pl) + O(epsilon^2).
```

If `lambda(t_Pl)=0` and the theory is required to stay nonnegative just below
the boundary, then the first-order condition is

```text
beta_lambda(t_Pl) <= 0.
```

The selector condition

```text
beta_lambda(t_Pl) = 0
```

is stronger.  It is a tangency or double-zero condition, not a consequence of
one-sided stability alone.

## Numerical Witness

Using the same Planck-scale gauge point as the double-criticality selector,
the one-loop beta boundary has a zero at

```text
y_star(M_Pl) = 0.388965102495.
```

The runner checks three local cases:

| Case | Result |
|---|---|
| `y_t < y_star` | `beta_lambda > 0`, so `lambda` turns negative just below `M_Pl`; locally unstable. |
| `y_t = y_star` | `beta_lambda = 0`; tangent boundary. |
| `y_t > y_star` | `beta_lambda < 0`, so `lambda` stays positive just below `M_Pl`; stable but nonstationary. |

Therefore stability supplies a lower-bound family, not a unique point.  It
cannot select the top Yukawa coupling.

## Authority Boundary

[VACUUM_CRITICAL_STABILITY_NOTE.md](VACUUM_CRITICAL_STABILITY_NOTE.md)
already scopes the vacuum-stability readout as bounded and inherited through
the current `y_t` lane.  [HIGGS_MASS_DERIVED_NOTE.md](HIGGS_MASS_DERIVED_NOTE.md)
states the `lambda(M_Pl)=0` boundary, but it does not prove the tangent
condition `beta_lambda(M_Pl)=0`.

Thus an appeal to "critical stability" cannot silently upgrade the
double-criticality selector to a retained derivation.  A positive route needs a
new substrate theorem saying the Planck boundary is a double zero or a
multiple-point tangency point.

## Route Fan-Out

| Route | Result | Reason |
|---|---|---|
| One-sided vacuum stability | blocked | Gives `beta_lambda <= 0`, not equality. |
| Critical tangent | conditional extra premise | Exactly the missing selector. |
| Multiple-point degeneracy | conditional extra premise | Needs a new theorem that the Planck boundary is a double zero. |
| Observed near-criticality | forbidden as derivation | Would import empirical near-criticality as proof input. |

## Relationship To PR #230

This closes the last obvious fast non-MC interpretation of the
double-criticality route.  The selector remains valuable as a consequence map:

```text
if beta_lambda(M_Pl)=0 is added or later derived, y_t(v)=0.9208739295
```

But on the current PR #230 surface, one-sided vacuum stability does not supply
that premise.

## Non-Claims

This note does not claim:

- that vacuum stability is false;
- that the double-criticality selector is numerically uninteresting;
- that a future multiple-point theorem cannot exist;
- that direct lattice correlator measurement is invalid.

It claims only:

> `lambda(M_Pl)=0` plus one-sided local stability implies at most a sign
> inequality on `beta_lambda(M_Pl)`.  It does not derive
> `beta_lambda(M_Pl)=0`.

## Verification

```bash
python3 scripts/frontier_yt_vacuum_stability_stationarity_no_go.py
# SUMMARY: PASS=13 FAIL=0
```
