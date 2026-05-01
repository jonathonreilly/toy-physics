# YT Asymptotic-Safety Fixed-Point No-Go Note

**Date:** 2026-05-01
**Status:** no-go / exact-negative-boundary on the current SM-bridge surface
**Runner:** `scripts/frontier_yt_asymptotic_safety_fixed_point_no_go.py`
**Certificate:** `outputs/yt_asymptotic_safety_fixed_point_no_go_2026-05-01.json`

```yaml
actual_current_surface_status: no-go / exact-negative-boundary
conditional_surface_status: "A future non-SM UV fixed-point theorem could reopen this route as new structure."
hypothetical_axiom_status: "Nontrivial UV fixed point / asymptotic-safety completion."
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The one-loop SM fixed-point route forces the Gaussian point, not the PR #230 y_t value."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

Can `beta_lambda(M_Pl)=0` be derived by asserting that the Planck boundary is a
fixed point of the SM beta-vector?

## Verdict

No, not on the current SM-bridge surface.

At one loop, the gauge beta functions are

```text
beta_g1 = (41/10) g_1^3
beta_g2 = -(19/6) g_2^3
beta_g3 = -7 g_3^3.
```

Their simultaneous real perturbative fixed point is

```text
g_1 = g_2 = g_3 = 0.
```

At that Gaussian gauge point,

```text
beta_y_t = (9/2) y_t^3,
beta_lambda |_{lambda=0} = -6 y_t^4.
```

So full one-loop beta-vector stationarity forces

```text
y_t = 0,
```

not the nonzero PR #230 selector value.

## Partial Fixed Points Are Extra Selectors

One can instead impose only selected beta conditions, such as

```text
beta_y_t = 0,
beta_lambda = 0.
```

But that is no longer a fixed point of the SM beta-vector.  It is another
selector.  The runner verifies that combining the two partial beta conditions
imposes a nontrivial compatibility relation among `g_1`, `g_2`, and `g_3`;
the current substrate does not derive that relation.

## Authority Boundary

The existing [G_BARE_DERIVATION_NOTE.md](G_BARE_DERIVATION_NOTE.md) already
records that the `SU(3)` lattice beta-function fixed-point route does not
provide a nontrivial fixed point.  This note adds the corresponding PR #230
top-Yukawa boundary: a perturbative SM fixed-point reading cannot replace the
missing Planck stationarity theorem.

## Non-Claims

This note does not rule out all possible asymptotic-safety or UV-completion
theories.  It rules out only the current-surface move:

> cite perturbative SM beta-vector stationarity as the derivation of
> `beta_lambda(M_Pl)=0` for PR #230.

Such a route either gives the Gaussian `y_t=0` point or adds new non-SM
structure.

## Verification

```bash
python3 scripts/frontier_yt_asymptotic_safety_fixed_point_no_go.py
# SUMMARY: PASS=8 FAIL=0
```
