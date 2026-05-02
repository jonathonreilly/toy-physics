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

The current status is:

```text
expected chunks: 63
present chunks: historical chunk001/chunk002 exist, but fail the seed-independence gate
ready chunks: 0
```

The production harness now records `metadata.run_control`, so future chunk
certificates expose the seed and command settings needed by the combiner.
The combiner also verifies the manifest reconstructs `63` unique artifact
directories.

After the numba seed audit, historical chunk001/chunk002 are no longer counted
as ready L12 evidence.  They lack the `numba_gauge_seed_v1` marker and share a
duplicate gauge-evolution signature across distinct metadata seeds.  Future
chunks must be rerun under the patched harness before they can count toward
combination.

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
