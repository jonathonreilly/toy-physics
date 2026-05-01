# Top-Yukawa Scalar Bethe-Salpeter Kernel / Residue Degeneracy

**Date:** 2026-05-01
**Status:** exact negative boundary / scalar Bethe-Salpeter pole-residue degeneracy
**Runner:** `scripts/frontier_yt_scalar_bs_kernel_residue_degeneracy.py`
**Certificate:** `outputs/yt_scalar_bs_kernel_residue_degeneracy_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary / scalar Bethe-Salpeter pole-residue degeneracy
conditional_surface_status: conditional-support if the interacting denominator, finite-volume/IR limit, and pole-residue derivative are derived
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "No retained theorem fixes the interacting Bethe-Salpeter/RPA denominator derivative or bounds finite-Nc pole-residue remainders."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Check

The runner starts from the same-source scalar two-point measurement primitive:

```text
C_ss(q)=Tr[S V_q S V_-q]
Gamma_ss(q)=1/C_ss(q)
```

It then grants, only for the no-go exercise, an isolated scalar pole at
`p_hat^2 = -1`.  The finite measured Euclidean values are held fixed.  A
family of analytic denominator deformations is constructed:

```text
Gamma_eta(x) = Gamma_ref(x)
             + eta Gamma_ref'(x_pole)
               (x-x_pole) prod_i (x-x_i) / prod_i (x_pole-x_i)
```

This deformation vanishes at every measured finite momentum `x_i` and at the
granted pole, but changes `dGamma/dp^2` at the pole.

Validation:

```text
python3 scripts/frontier_yt_scalar_bs_kernel_residue_degeneracy.py
# SUMMARY: PASS=6 FAIL=0
```

## Result

Finite same-source samples plus pole naming do not fix the LSZ residue.  The
runner preserves all currently measured `Gamma_ss(q)` values and preserves the
granted pole location while moving the pole derivative, residue proxy, and
`kappa_s` proxy.

At physical `N_c=3`, natural `1/N_c^2`-sized denominator remainders already move
the `kappa_s` proxy by more than five percent without changing the finite
samples.  Therefore a large-`N_c` or finite-mode pole narrative is not a
retained proof at `N_c=3`.

## Claim Boundary

This block does not rule out a future scalar Bethe-Salpeter closure.  It rules
out the current shortcut:

- measured same-source finite modes are not a pole-residue theorem;
- a granted pole location is not a residue calculation;
- source/projector normalization must be derived in the same interacting
  denominator;
- the finite-volume, gauge-zero-mode, and IR limits must be fixed before
  `dGamma_ss/dp^2` is load-bearing.

Until those pieces are supplied, `dE_top/ds` cannot be converted to physical
`dE_top/dh`, and `kappa_s = 1` remains forbidden.
