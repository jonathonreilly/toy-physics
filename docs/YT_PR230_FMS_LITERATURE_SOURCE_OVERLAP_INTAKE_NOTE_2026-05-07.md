# PR230 FMS Literature Source-Overlap Intake

Status: exact negative boundary / literature bridge only; no closure proposal
authorized.

Runner:
`scripts/frontier_yt_pr230_fms_literature_source_overlap_intake.py`

Certificate:
`outputs/yt_pr230_fms_literature_source_overlap_intake_2026-05-07.json`

## Result

The targeted FMS/gauge-invariant-field rescan confirms a useful but limited
bridge.  The literature supports the shape of a future gauge-invariant
canonical scalar operator only after a same-surface EW/Higgs action supplies a
scalar doublet, canonical kinetic normalization, radial background `v`, and
LSZ-normalized scalar mass eigenstate.

That is not the current PR230 surface.  The branch still lacks:

- an accepted same-surface EW/Higgs action certificate;
- a current canonical `O_H` certificate;
- production `C_spH/C_HH` or `C_sH/C_HH` pole rows;
- Gram/source-overlap purity;
- FV/IR/threshold authority;
- retained-route approval.

Therefore the literature does not derive `kappa_s`, does not identify `O_sp`
or the taste-radial `x` operator with canonical `O_H`, and does not promote
time-kernel smoke/GEVP rows to pole-residue authority.

## Literature Role

The runner records these references as non-derivation context only:

- Froehlich, Morchio, Strocchi, "Higgs phenomenon without a symmetry breaking
  order parameter", DOI `10.1016/0370-2693(80)90594-8`.
- Maas, "Observables in Higgsed Theories", arXiv `1410.2740`.
- Maas and Pedro, "Gauge invariance and the physical spectrum in the
  two-Higgs-doublet model", arXiv `1601.02006`.
- "Gauge-invariant quantum fields", DOI `10.1140/epjc/s10052-024-13317-0`.

No reference is used as proof authority for a PR230 source-overlap
normalization.

## Acceptance Contract

A future positive source-Higgs artifact must supply one of:

1. accepted same-surface EW/Higgs action plus canonical
   `O_FMS = (Phi^dagger Phi - v^2/2) / v`, with PR230 source-coordinate
   transport to `O_sp` or the taste-radial source; or
2. direct production pole rows measuring the overlap:
   `Res_C_sp_sp`, `Res_C_spH`, and `Res_C_HH`, followed by Gram-purity,
   scalar-LSZ/FV/IR, assembly, retained-route, and campaign gates.

Until then, the cleanest route remains source-Higgs pole rows with certified
canonical `O_H`; the first fallback remains genuine same-source W/Z response
rows with identity/covariance/strict non-observed `g2`.

## Validation

```bash
python3 scripts/frontier_yt_pr230_fms_literature_source_overlap_intake.py
# SUMMARY: PASS=16 FAIL=0
```

## Claim Boundary

This artifact is not physical `y_t` evidence.  It does not use `H_unit`,
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette/u0, reduced pilots,
`kappa_s=1`, `c2=1`, `Z_match=1`, `g2=1`, or value recognition.  PR #230
remains draft/open with no retained or proposed_retained closure.
