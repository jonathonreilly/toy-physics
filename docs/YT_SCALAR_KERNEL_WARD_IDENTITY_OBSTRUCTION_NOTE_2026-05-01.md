# Top-Yukawa Scalar Kernel Ward-Identity Obstruction

**Date:** 2026-05-01
**Status:** exact negative boundary / scalar kernel Ward-identity obstruction
**Runner:** `scripts/frontier_yt_scalar_kernel_ward_identity_obstruction.py`
**Certificate:** `outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary / scalar kernel Ward-identity obstruction
conditional_surface_status: conditional-support if a retained scalar denominator derivative theorem is derived
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "K'(x_pole), zero-mode/IR limiting order, and common scalar/gauge dressing remain open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

After the pole-tuned residue-envelope obstruction, the shortest analytic route
would be a theorem deriving the interacting scalar-channel denominator:

```text
C_ss(x) = Pi(x) / D(x)
D(x) = 1 - K(x) Pi(x)
D(x_pole) = 0
D'(x_pole) = -K'(x_pole) Pi(x_pole) - K(x_pole) Pi'(x_pole)
```

This block asks whether the existing Ward/gauge/Feshbach surfaces already fix
`K'(x_pole)`.

## Result

They do not.

Validation:

```text
python3 scripts/frontier_yt_scalar_kernel_ward_identity_obstruction.py
# SUMMARY: PASS=9 FAIL=0
```

The runner verifies that:

- the old `yt_ward_identity` surface is audited-renaming, not authority;
- the determinant gate still names `K'(pole)` as open;
- exact Feshbach response preservation does not prove common scalar/gauge
  dressing;
- the common-dressing obstruction remains open;
- the residue-envelope parent remains open;
- a rank-count model leaves `K'(x_pole)` and common dressing unconstrained
  after the pole condition fixes `K(x_pole)`;
- a same-pole kernel family preserves `D(x_pole)=0` while changing the LSZ
  readout factor by `2.35319x`.

Therefore Ward/gauge identities do not close the scalar LSZ normalization
blocker.  Positive closure still needs the same-source scalar denominator and
derivative in a derived zero-mode/IR/finite-volume limit, or direct production
pole-derivative data.

## Claim Boundary

This block does not claim retained or proposed-retained top-Yukawa closure.  It
does not use `H_unit`, `yt_ward_identity`, observed target values,
alpha/plaquette/u0, reduced pilots, `c2 = 1`, `Z_match = 1`, or
`kappa_s = 1` as proof inputs.
