# PR #230 FH/LSZ Ready Chunk Response-Stability Diagnostic

**Status:** bounded-support / FH-LSZ ready chunk response-stability diagnostic
**Runner:** `scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py`
**Certificate:** `outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json`

## Result

The current seed-controlled ready set has sixteen L12 chunks
`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]`.  Their same-source top response slopes are finite:

```text
chunk001: dE/ds = 1.4356354951944574
chunk002: dE/ds = 6.629960999250584
chunk003: dE/ds = 1.4159189031935757
chunk004: dE/ds = 6.80363930805008
chunk005: dE/ds = 1.4282013633170878
chunk006: dE/ds = 1.2423254657958398
chunk007: dE/ds = 1.4279585199127138
chunk008: dE/ds = 1.4358688402488398
chunk009: dE/ds = 1.4329511536106778
chunk010: dE/ds = 1.4266663595777471
chunk011: dE/ds = 1.4274485932311824
chunk012: dE/ds = 1.4326654432439319
chunk013: dE/ds = 1.2459279992373107
chunk014: dE/ds = 6.6959198043875165
chunk015: dE/ds = 1.4232091419530353
chunk016: dE/ds = 1.4136616747562865
```

The partial set fails the diagnostic stability rule:

```text
n_chunks = 16
relative_stdev = 0.8943920916391181
spread_ratio = 5.476535332624479
relative_fit_error = 8.121324509664896
stability_rule = n >= 8, relative_stdev < 0.25, spread_ratio < 2
stability_passed = false
```

The fitted slope uncertainties are also too large for production-grade
response use at this stage.  This is expected for `16/63` L12 chunks and is a
reason to keep collecting chunks, not a physics closure.

The 2026-05-03 response-window forensics runner separates this from the target
time-series stability.  The fitted-slope central values have
`relative_stdev=0.8943920916391181`, while the tau=1 target diagnostic across
the same chunks has `relative_stdev=0.006010378980783995` and
`spread_ratio=1.0229374224682368`.  That is useful debugging support, but it
does not authorize switching the production response readout without a
predeclared response-window acceptance gate.

## Claim Boundary

This diagnostic does not authorize retained or proposed-retained wording.  It
does not treat `dE/ds` as physical `dE/dh`, does not set `kappa_s = 1`, and
does not use observed target values, `H_unit`, Ward authority, `alpha_LM`,
plaquette, or `u0` as proof inputs.

Even a stable production slope would still need the scalar LSZ pole derivative,
model-class or pole-saturation control, FV/IR/zero-mode control, and
canonical-Higgs source-pole identity before physical `y_t` closure.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_forensics.py
# SUMMARY: PASS=10 FAIL=0
```
