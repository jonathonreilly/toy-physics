# PR #230 Source-Pole Purity Cross-Correlator Gate

**Status:** open / source-pole purity cross-correlator gate not passed
**Runner:** `scripts/frontier_yt_source_pole_purity_cross_correlator_gate.py`
**Certificate:** `outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json`

## Purpose

The remaining canonical-Higgs identity route needs source-pole purity: the
measured source pole must be the canonical Higgs radial mode used by `v`.
This block asks whether source-only pole data can prove that purity.

## Result

Source-only data are not enough.  The runner constructs two models with the
same source pole residue, same source response, and same source inverse
propagator derivative, but different overlap with the canonical Higgs radial
mode.

The models are separated by data that are not in the current QCD top harness:

- a source-Higgs pole cross-correlator `C_sH`;
- an equivalent source-pole purity theorem;
- an independent canonical-Higgs response observable, such as same-source W/Z
  mass slopes.

The refreshed runner distinguishes an absence guard from evidence.  The
production metadata may name the required `O_H`, `C_sH`, and `C_HH` rows, but
while that block is `enabled: false` and `absent_guarded`, it is claim hygiene
only and does not count as a cross-correlator observable.

Without one of these, `C_ss` and source response remain source-coordinate
observables and do not certify source-pole purity.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat `C_ss` as a source-pole purity proof, does not set
`kappa_s = 1`, and does not use `H_unit`, `yt_ward_identity`, observed top
mass, observed `y_t`, `alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Add or derive a source-Higgs cross-correlator/purity theorem, or implement an
independent canonical-Higgs response observable such as same-source W/Z mass
slopes.
