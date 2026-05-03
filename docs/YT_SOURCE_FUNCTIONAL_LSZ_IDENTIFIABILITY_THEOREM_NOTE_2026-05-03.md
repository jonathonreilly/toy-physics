# Source-Functional LSZ Identifiability Theorem

**Date:** 2026-05-03  
**Status:** exact negative boundary / source-functional LSZ identifiability theorem  
**Runner:** `scripts/frontier_yt_source_functional_lsz_identifiability_theorem.py`  
**Certificate:** `outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support if a future source-Higgs identity or response certificate supplies the missing overlap
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The source-functional LSZ theorem identifies the missing overlap; it does not derive it on the current surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Result

The runner asks what route 1 can honestly derive from the Cl(3)/Z3 scalar
source functional if an isolated scalar source pole is granted.

It finds an exact support theorem and an exact boundary:

- same-source LSZ data can form the source-coordinate invariant readout
  `(dE_top/ds) * sqrt(dGamma_ss/dp2)`;
- setting `kappa_s = 1` is still rejected because the raw source slope changes
  under `O_s -> c O_s`;
- source-only pole data do not determine the overlap between the measured
  source pole and the canonical Higgs radial mode used by `v`;
- source-only data also do not set the top coupling of an orthogonal neutral
  scalar to zero.

Verification:

```text
python3 scripts/frontier_yt_source_functional_lsz_identifiability_theorem.py
# SUMMARY: PASS=13 FAIL=0
```

## Consequence

Route 1 does not close from source-functional data alone.  The exact missing
non-source-only input is one of:

- `C_sH` and `C_HH` pole residues with Gram purity
  `Res(C_sH)^2 = Res(C_ss) Res(C_HH)`;
- a same-surface canonical-Higgs operator `O_H` and source-pole identity
  theorem;
- a real W/Z mass-response certificate measuring `dM_W/ds` or `dM_Z/ds` plus
  the sector-overlap identity;
- a microscopic rank-one neutral-scalar theorem excluding orthogonal source
  admixture and orthogonal top coupling.

## Non-Claims

- This note does not claim retained or proposed-retained top-Yukawa closure.
- This note does not set `kappa_s = 1`.
- This note does not identify `O_s` with canonical `H`.
- This note does not set `cos(theta) = 1`.
- This note does not use `H_unit`, `yt_ward_identity`, observed targets,
  `alpha_LM`, plaquette, `u0`, `c2 = 1`, `Z_match = 1`, or reduced pilots as
  proof input.

## Next Action

Implement or derive same-surface `C_sH` / `C_HH` pole-residue rows, or implement
a production W/Z mass-response observable with a sector-overlap certificate.
Source-only LSZ data are insufficient.
