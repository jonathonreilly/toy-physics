# W/Z Response Repo Harness Import Audit

**Status:** exact negative boundary / repo-wide W/Z response harness import audit
**Runner:** `scripts/frontier_yt_wz_response_repo_harness_import_audit.py`
**Certificate:** `outputs/yt_wz_response_repo_harness_import_audit_2026-05-03.json`

## Purpose

PR #230 can close through a physical W/Z response route only if a same-source
electroweak mass-response measurement exists:

```text
y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)
```

with `dE_top/ds` and `dM_W/ds` measured under the same scalar source, with
covariance, production W/Z correlator mass fits, and sector-overlap /
canonical-Higgs identity certificates.

This audit asks whether that implementation already exists elsewhere in the
repo.

## Result

No existing artifact supplies the required W/Z response measurement.

- `scripts/yt_direct_lattice_correlator_production.py` is a QCD top-correlator
  harness with W/Z response marked `absent_guarded`.
- `EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md` supplies
  object-level W/Z mass algebra after canonical `H` is supplied; it does not
  measure `dM_W/ds`.
- The W/Z manifest, builder, gate, and absence guard define the future contract
  and claim firewall, but no measurement rows or candidate certificate exist.
- EW coupling and native `SU(2)` scripts provide gauge-context support only,
  not same-source W/Z correlator mass fits.

So the W/Z route is not hidden in existing code.  It remains a future physical
observable implementation route.

## Claim Boundary

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not treat static EW algebra as `dM_W/ds`, does not use observed W/Z or
top values as selectors, and does not set `k_top = k_gauge`, `kappa_s = 1`,
`c2 = 1`, or `Z_match = 1`.

## Next Action

Implement actual same-source W/Z response measurement rows in a dedicated EW
gauge/Higgs harness, or continue the source-Higgs `C_sH/C_HH` pole-row route
and the production FH/LSZ evidence lane.

## Verification

```bash
python3 scripts/frontier_yt_wz_response_repo_harness_import_audit.py
# SUMMARY: PASS=10 FAIL=0
```
