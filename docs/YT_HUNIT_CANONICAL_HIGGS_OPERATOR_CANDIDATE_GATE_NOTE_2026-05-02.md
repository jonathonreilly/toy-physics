# H_unit Canonical-Higgs Operator Candidate Gate

**Status:** exact negative boundary / H_unit not canonical-Higgs operator realization  
**Runner:** `scripts/frontier_yt_hunit_canonical_higgs_operator_candidate_gate.py`  
**Certificate:** `outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json`

## Purpose

The canonical-Higgs operator route naturally raises a candidate: use the legacy
`H_unit` substrate bilinear as `O_H`.  This gate tests that candidate without
using the forbidden `H_unit` matrix-element readout as authority.

## Result

The gate is not passed.  `H_unit` is a named D17/substrate bilinear candidate,
but current artifacts do not certify it as the canonical Higgs radial operator
for PR #230.  The live audited objection is exactly the old `H_unit` readout
shortcut, and the D17/source-pole attempt leaves the source overlap, pole
residue, inverse-propagator derivative, and canonical kinetic metric open.

The runner records a mixing witness that keeps the `H_unit` unit norm and
`H_unit` top readout fixed while the canonical-Higgs Yukawa changes through an
orthogonal neutral scalar admixture.  Therefore `H_unit` can enter a future
`C_sH` / `C_HH` route only after it has the same purity, pole-residue, and
canonical-normalization certificates required of any `O_H` candidate.

## Claim Boundary

This is an exact negative boundary, not retained or proposed-retained
top-Yukawa closure.  It does not use `H_unit` matrix-element readout,
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette, or `u0`, and it
does not set `kappa_s = 1`, `cos(theta)=1`, `c2 = 1`, or `Z_match = 1`.

## Verification

```bash
python3 scripts/frontier_yt_hunit_canonical_higgs_operator_candidate_gate.py
# SUMMARY: PASS=18 FAIL=0
```

Next action: if using `H_unit` as `O_H`, first supply `C_HH` / `C_sH` pole
residues and a purity/canonical-Higgs identity certificate.  Otherwise pivot
to W/Z response with identity certificates or seed-controlled FH/LSZ chunk
processing.
