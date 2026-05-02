# PR #230 Source-Higgs Cross-Correlator Import Audit

**Status:** exact negative boundary / source-Higgs cross-correlator import audit
**Runner:** `scripts/frontier_yt_source_higgs_cross_correlator_import_audit.py`
**Certificate:** `outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json`

## Purpose

The source-pole purity gate identified a possible positive route: measure a
pole cross-correlator `C_sH` between the PR #230 scalar source and the
canonical Higgs radial operator.  This audit asks whether that object is
already present or authorized on the current PR surface.

## Result

No current authority supplies it.  The production harness has top
source-response and same-source `C_ss` support, but no `C_sH`, canonical-Higgs
operator, or W/Z response schema.  Existing EW/SM Higgs notes start after a
canonical `H` is supplied or select allowed monomials; they do not derive the
PR source operator overlap.

The already-open shortcut blockers remain load-bearing:

- gauge `v` and canonical `Z_h` do not identify the source operator;
- effective-potential Hessians do not fix the source direction;
- BRST/ST/Nielsen identities do not fix source-pole purity;
- the W/Z response manifest is planning support, not `C_sH` evidence.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not define canonical `H` by fiat, does not set `kappa_s = 1`, and does
not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette,
or `u0` as proof inputs.

## Next Action

Either implement the missing `C_sH` or W/Z response measurement with a
canonical-Higgs identity certificate, or continue with a sector-overlap /
source-pole purity theorem or seed-controlled FH/LSZ production processing.
