# Top-Yukawa Scalar-Channel Ladder Kernel Input Audit

**Date:** 2026-05-01  
**Status:** exact support / input audit; no retention proposal  
**Runner:** `scripts/frontier_yt_scalar_ladder_kernel_input_audit.py`  
**Certificate:** `outputs/yt_scalar_ladder_kernel_input_audit_2026-05-01.json`

```yaml
actual_current_surface_status: exact-support
conditional_surface_status: conditional-support for a future exact Bethe-Salpeter kernel theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The scalar pole residue, projector, and kernel limiting theorem remain open imports."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The active PR #230 blocker is no longer the numerical arithmetic of
`1/sqrt(6)`.  The blocker is the missing physical readout theorem:

```text
staggered scalar source two-point function
-> interacting scalar pole
-> LSZ residue / physical Higgs carrier
-> y_t from m_t and v, without H_unit matrix-element definition
```

This note audits the existing full-staggered PT code for the exact ingredients
that may be reused in the scalar-channel Bethe-Salpeter route.

## Allowed Formula Inputs

The existing full-staggered PT runner supplies usable formula-level inputs:

| Input | Reuse status |
|---|---|
| `D_psi_full(k) = sum_mu sin^2(k_mu)` | allowed formula |
| `D_gluon_full(k) = 4 sum_mu sin^2(k_mu/2)` | allowed formula |
| local scalar source form factor | allowed formula |
| point-split scalar kinematic factor | allowed as kinematics only |
| gauge-link kinematic factor | allowed as kinematics only |
| `C_F = 4/3` | allowed color factor |

The runner explicitly rejects legacy surfaces as proof inputs for PR #230:

| Surface | Status in this route |
|---|---|
| `CANONICAL_ALPHA_LM` / `alpha_LM` bridge | forbidden proof input |
| plaquette / `u0` tadpole normalization | forbidden proof input |
| `H_unit` matrix-element readout | forbidden proof input |
| old `yt_ward_identity` theorem | forbidden as physical `y_t` authority |
| observed top/Higgs/Yukawa values | forbidden as selectors |

## Runner Result

```text
python3 scripts/frontier_yt_scalar_ladder_kernel_input_audit.py
# SUMMARY: PASS=9 FAIL=0
```

Key checks:

| Check | Result |
|---|---|
| full staggered formula functions present | pass |
| forbidden legacy tokens identified | pass |
| staggered fermion denominator nonnegative | pass |
| Wilson gluon denominator nonnegative | pass |
| local scalar form factor is identity | pass |
| point-split scalar and gauge kinematic factors match | pass |
| conserved-vector numerator cancels by parity | pass |
| kinematic match does not force common dressing | pass |
| P1 runner lacks pole-residue closure objects | pass |

The point-split scalar and gauge-link kinematic factors match exactly in the
formula code:

```text
F_scalar_ps(k) = sum_mu cos^2(k_mu/2)
F_gauge(k)     = sum_mu cos^2(k_mu/2)
```

That equality is useful, but it is not a pole-residue theorem.  The scalar
bubble and gauge dressing weight the same numerator with different denominators
and different external-leg readouts.  The runner records this explicitly by
comparing a scalar-bubble weight to a gauge-dressing weight; their ratio is not
forced to one by the shared kinematic numerator.

## Remaining Exact Theorem

The next positive route must derive:

```text
exact scalar-channel Wilson-staggered Bethe-Salpeter kernel
+ scalar color/taste/spin projector independent of H_unit readout
+ controlled IR and finite-volume limit
+ eigenvalue crossing
+ pole residue from derivative of inverse scalar two-point function
```

Without those ingredients, the available formula equality is only exact support
for the next kernel theorem.  It does not close `y_t`.

## Non-Claims

- This note is not a `y_t` derivation.
- This note is not a retained scalar pole theorem.
- This note does not use `alpha_LM` or plaquette normalization.
- This note does not define `y_t` through an `H_unit` matrix element.
