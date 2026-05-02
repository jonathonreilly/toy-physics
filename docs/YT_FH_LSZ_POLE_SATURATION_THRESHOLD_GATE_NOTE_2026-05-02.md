# PR #230 FH/LSZ Pole-Saturation Threshold Gate

**Status:** open / FH-LSZ pole-saturation threshold gate blocks current finite-shell fit
**Runner:** `scripts/frontier_yt_fh_lsz_pole_saturation_threshold_gate.py`
**Certificate:** `outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json`

## Claim

Finite-shell same-source `Gamma_ss(q)` rows should only become LSZ evidence
after a model-class gate.  This runner makes one such gate executable: solve
the positive-Stieltjes linear feasibility problem for the allowed pole residue
interval under a candidate continuum threshold.

On the current finite-shell surface, positivity plus a near-pole continuum
threshold leaves the pole residue interval with zero lower bound and a broad
upper bound.  That is not a scalar LSZ normalization.

## Boundary

This is an acceptance gate, not closure.  It does not derive a physical scalar
pole, set `kappa_s = 1`, or use observed `m_t` / `y_t`.  A future route must
provide a pole-saturation theorem, continuum-threshold certificate, production
acceptance certificate, or microscopic scalar denominator theorem that makes
the residue interval tight.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_pole_saturation_threshold_gate.py
# SUMMARY: PASS=7 FAIL=0
```
