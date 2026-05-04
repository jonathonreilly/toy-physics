# PR #230 FH/LSZ Target-Observable ESS Certificate

**Status:** bounded-support / FH-LSZ target-observable ESS certificate passed
**Runner:** `scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py`
**Certificate:** `outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json`

## Purpose

The autocorrelation gate cannot use plaquette ESS as a proxy for the
load-bearing FH/LSZ observables.  This runner reads only the same-source target
series emitted by the production harness:

- `scalar_source_response_analysis.per_configuration_slopes`
- `scalar_two_point_lsz_analysis.mode_rows[*].C_ss_timeseries`

It block-averages by completed chunk and reports an initial-positive ESS for
the target observables.  This is production-processing support, not physics
evidence.

## Result

An initial target-observable ESS check on chunks001-012 had limiting ESS
`150.2439730312628`, below the predeclared threshold `200`.  The campaign then
launched chunks013-016 with fixed seeds, no `--resume`, distinct
production-output directories, and concurrency capped at four workers.

After chunks025-026 completed:

```text
python3 scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py
# SUMMARY: PASS=8 FAIL=0

ready_chunk_indices = [1, 2, 3, ..., 24, 25, 26]
limiting_target_ess = 355.8130499055201
minimum_target_ess_per_volume = 200.0
limiting_target_ess_observable = source_slope_tau1
```

The downstream autocorrelation/ESS gate now passes for target observables:

```text
python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=11 FAIL=0
```

## Claim Boundary

This certificate does not authorize retained or `proposed_retained` wording.
It does not set `kappa_s = 1`, does not treat `dE/ds` as physical `dE/dh`, and
does not use `H_unit`, Ward authority, observed top mass, observed `y_t`,
`alpha_LM`, plaquette, or `u0` as proof input.

The ready set is still only `26/63` L12 chunks and `416/1000` saved
configurations.  Response stability still fails, the scalar-pole
derivative/model-class/FV/IR gates remain open, and the source pole is not
identified with the canonical Higgs radial mode.

## Next Action

Continue seed-controlled chunks only as production support, and prioritize
the remaining closure blockers: response stability, scalar-pole
derivative/model-class/FV/IR control, and a same-surface canonical-Higgs
identity route such as `C_sH`/`C_HH` Gram purity or real W/Z response rows with
sector-overlap identity.
