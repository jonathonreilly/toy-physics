# PR230 two-source taste-radial row production manifest

**Status:** bounded-support / two-source taste-radial `C_sx/C_xx` production manifest; rows absent  
**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_row_production_manifest.py`  
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json`

This block turns the completed taste-radial action certificate and row contract
into an executable, collision-guarded production-row plan.  It does not launch
jobs and it does not claim row evidence.

The manifest uses the existing optimized production harness:

- the three-mass top correlator scan is preserved;
- scalar FH/LSZ and source-Higgs rows remain selected-mass-only at `m=0.75`;
- normal-equation caching remains the per-configuration solve path;
- each chunk has a distinct seed, output JSON, and production artifact
  directory;
- `--resume` is deliberately absent from every planned command.

The planned L12_T24 row wave is `63` chunks x `16` configurations, with
four scalar momenta and x16 stochastic source-Higgs noise per configuration.
The recommended local concurrency is `2-3` workers until the machine-specific
resource envelope is rechecked.

The claim boundary is strict.  The planned rows are `C_sx/C_xx` for the
taste-radial second source `x`, not canonical-Higgs `C_sH/C_HH` rows.  Even
completed production rows would still need pole/FV/IR diagnostics and a
separate canonical `O_H`/source-overlap theorem or genuine physical-response
route before any retained/proposed-retained wording could be considered.

Validation:

```bash
python3 -m py_compile scripts/frontier_yt_pr230_two_source_taste_radial_row_production_manifest.py
python3 scripts/frontier_yt_pr230_two_source_taste_radial_row_production_manifest.py
```

Result: `PASS=16 FAIL=0`.

Exact next action: launch the missing chunks with max concurrency `2-3` using
the recorded commands, then add per-chunk schema gates, a combiner for
`C_sx/C_xx`, pole-residue/FV/IR diagnostics, and the separate physical bridge.
