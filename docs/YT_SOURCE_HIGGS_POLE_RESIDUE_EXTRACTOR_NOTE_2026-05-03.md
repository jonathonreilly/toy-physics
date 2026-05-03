# PR #230 Source-Higgs Pole-Residue Extractor Gate

**Status:** open / source-Higgs pole-residue extractor awaiting valid production rows  
**Runner:** `scripts/frontier_yt_source_higgs_pole_residue_extractor.py`  
**Certificate:** `outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json`

## Purpose

The source-Higgs harness can emit finite-mode `C_ss`, `C_sH`, and `C_HH`
rows.  The rank-repair route needs isolated-pole residues before the
source-Higgs builder and O_sp-Higgs Gram-purity postprocessor can test
`O_sp = +/- O_H`.

This runner supplies that missing bridge.  It writes
`outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json`
only after all extraction gates pass.

## Current Result

The current default input is the reduced unratified-operator smoke artifact.
It is intentionally rejected because it is not production data, has an
unratified canonical-Higgs operator, has only two momentum modes, has two
configurations, and lacks model-class pole-saturation and FV/IR controls.
No pole-residue row file is written.

Required future inputs:

- production phase with `production_targets = true`;
- `numba_gauge_seed_v1` seed metadata;
- ratified same-surface canonical-Higgs operator certificate;
- at least four distinct `p_hat_sq` modes and enough configurations for errors;
- model-class / pole-saturation control;
- FV/IR / zero-mode control;
- forbidden-import firewall false;
- `used_as_physical_yukawa_readout = false`.

## Validation

```text
python3 scripts/frontier_yt_source_higgs_pole_residue_extractor.py
# SUMMARY: PASS=9 FAIL=0
```

## Claim Boundary

This is an input bridge only.  It does not claim retained or
`proposed_retained` closure, does not define `O_H` by fiat, does not treat
finite-mode rows as pole residues before the pole gate, and does not set
`kappa_s = 1`, `cos(theta) = 1`, `c2 = 1`, or `Z_match = 1`.

Next action: run a production source-Higgs cross-correlator artifact with a
ratified canonical-Higgs operator and the required controls, then rerun this
extractor, the source-Higgs builder, the Gram-purity postprocessor, and the
retained-route gate.
