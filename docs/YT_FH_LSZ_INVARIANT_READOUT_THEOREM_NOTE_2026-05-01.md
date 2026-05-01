# Top-Yukawa Feynman-Hellmann / Scalar-LSZ Invariant Readout Theorem

**Date:** 2026-05-01
**Status:** exact-support / Feynman-Hellmann scalar-LSZ invariant readout formula
**Runner:** `scripts/frontier_yt_fh_lsz_invariant_readout_theorem.py`
**Certificate:** `outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json`

```yaml
actual_current_surface_status: exact-support / Feynman-Hellmann scalar-LSZ invariant readout formula
conditional_surface_status: conditional-support if same-source production response, isolated scalar pole, pole derivative, and canonical-Higgs match are supplied
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The invariant formula is theorem support, but the required same-source production pole-residue data are not present."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Theorem

For the same scalar source `s` used in both the top-energy response and scalar
two-point function,

```text
C_ss(q) = Tr[S V_q S V_-q]
Gamma_ss(q) = 1 / C_ss(q)
```

an isolated canonical scalar pole with residue `Res[C_ss]` gives the
source-normalization-invariant readout

```text
y_proxy = (dE_top/ds) / sqrt(Res[C_ss] at the pole)
        = (dE_top/ds) * sqrt(dGamma_ss/dp^2 at the pole).
```

Under a scalar source/operator rescaling,

```text
O_s -> c O_s
dE_top/ds -> c dE_top/ds
Res[C_ss] -> c^2 Res[C_ss]
dGamma_ss/dp^2 -> (dGamma_ss/dp^2) / c^2
```

so the combined LSZ response readout is invariant.  The forbidden shortcut
`kappa_s = 1` is not invariant.

Validation:

```text
python3 scripts/frontier_yt_fh_lsz_invariant_readout_theorem.py
# SUMMARY: PASS=7 FAIL=0
```

## Result

This retires one wording trap: the route does not need to declare `kappa_s = 1`.
It needs to measure `kappa_s` as the same-source pole overlap.

The result is exact support, not retained closure.  The missing data/theorem
items remain:

- same-source production `dE_top/ds`;
- same-source production `C_ss(q)`;
- isolated scalar pole in the controlled finite-volume/IR limit;
- `dGamma_ss/dp^2` at that pole;
- match of that pole to the canonical Higgs kinetic normalization used by `v`.

Until those are supplied, PR #230 cannot convert `dE_top/ds` into physical
`dE_top/dh` or claim retained top-Yukawa closure.
