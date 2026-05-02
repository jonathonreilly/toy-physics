# PR #230 FH/LSZ Chunk001 Production Checkpoint

**Status:** bounded-support / FH-LSZ chunk001 production checkpoint seed-invalid diagnostic
**Runner:** `scripts/frontier_yt_fh_lsz_chunk001_checkpoint_certificate.py`
**Certificate:** `outputs/yt_fh_lsz_chunk001_checkpoint_certificate_2026-05-02.json`

## Result

Historical `L12_T24` chunk001 completed under the production-targeted FH/LSZ
command.  It emits:

- production-phase run-control metadata;
- same-source scalar response `dE/ds`;
- same-source scalar two-point `C_ss(q)` / `Gamma_ss(q)` rows for the four
  modes and sixteen noise vectors;
- a chunk-local artifact directory.

After the numba seed-independence audit, the chunk combiner gate now sees:

```text
present_chunks = 2
ready_chunks = 0
expected_chunks = 63
```

Chunk001 lacks the `numba_gauge_seed_v1` marker and shares a duplicate
gauge-evolution signature with chunk002 across distinct metadata seeds.  It is
a production-format diagnostic, not independent production evidence, until it
is rerun under the patched harness or excluded.

## Claim Boundary

This is seed-invalid bounded production support only.  It is not retained or
proposed-retained closure because the historical chunk cannot count toward L12
combination, and PR #230 still needs L12 reruns, L16/L24 scaling, richer
pole-fit kinematics/model-class control, FV/IR/zero-mode control, and retained
proposal certification.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0

python3 -m py_compile scripts/frontier_yt_fh_lsz_chunk001_checkpoint_certificate.py
python3 scripts/frontier_yt_fh_lsz_chunk001_checkpoint_certificate.py
# SUMMARY: PASS=10 FAIL=0
```
