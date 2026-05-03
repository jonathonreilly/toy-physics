# PR #230 FH/LSZ Chunk Combiner Gate

**Status:** open / FH-LSZ chunk combiner gate blocks partial or non-independent evidence
**Runner:** `scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py`
**Certificate:** `outputs/yt_fh_lsz_chunk_combiner_gate_2026-05-01.json`

## Question

The L12 FH/LSZ production manifest gives `63` foreground-sized chunk commands.
This block asks what must be true before those chunks can become even an L12
candidate production summary, without letting filenames or partial output
stand in for evidence.

## Result

The gate reconstructs the full L12 chunk grid and audits future chunk outputs
for:

- `metadata.phase == "production"`;
- run-control provenance, including the expected seed, command settings, and
  chunk-local production artifact directory;
- numba gauge-seed-control metadata proving the gauge RNG was seeded inside the
  production path before thermalization;
- duplicate gauge-evolution signatures across distinct metadata seeds;
- same-source `dE_top/ds` from shifts `-0.01, 0.0, 0.01`;
- same-source `C_ss(q)` / `Gamma_ss(q)` for modes `0,0,0`, `1,0,0`,
  `0,1,0`, and `0,0,1`;
- scalar-source and scalar-LSZ metadata that explicitly do not use the
  measurements as physical Yukawa readouts.

The current status after processing chunk012 and the chunk001 target-series
replacement is:

```text
expected chunks: 63
present chunks: 12
ready chunks: 12
ready chunk indices: [1,2,3,4,5,6,7,8,9,10,11,12]
```

The production harness now records `metadata.run_control`, so future chunk
certificates expose the seed and command settings needed by the combiner.
The combiner also verifies the manifest reconstructs `63` unique artifact
directories.

Chunks001-012 are ready under the `numba_gauge_seed_v1` seed-control policy
and pass the duplicate-signature gate.  The set is still incomplete:
`51/63` L12 chunks remain missing, no combined L12 output exists, and L12-only
would still be non-retained without L16/L24, pole-derivative/model-class,
FV/IR/zero-mode, and canonical-Higgs identity gates.

## Claim Boundary

This is an acceptance gate only:

```text
proposal_allowed: false
```

No absent, partial, non-independent, or L12-only chunk set is PR #230 retained
closure.  Even a complete L12 combination would still need L16/L24 scaling, an
isolated scalar pole inverse-derivative fit, finite-volume/IR/zero-mode
control, and the retained-proposal certificate.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py scripts/yt_direct_lattice_correlator_production.py
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0
```
