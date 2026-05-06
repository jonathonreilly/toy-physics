# Handoff

## Result

The note and runner were repaired by narrowing the claim to the exact
finite-dimensional `H_unit` component-overlap identity:

```text
<alpha_0,a_0 | H_unit | alpha_0,a_0> = 1 / sqrt(N_iso*N_c).
```

For `(N_iso,N_c)=(2,3)`, this is `1/sqrt(6)`.

## Files Changed

- `docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md`
- `docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md`
- `docs/YT_RETENTION_LANDING_READINESS_2026-04-18.md`
- `scripts/frontier_yt_ssb_matching_gap.py`
- `scripts/frontier_yt_retention_landing_readiness.py`
- `logs/retained/yt_ssb_matching_gap_2026-04-18.log`
- `logs/retained/yt_retention_landing_readiness_2026-04-18.log`
- `.claude/science/physics-loops/yt-ssb-matching-gap-arithmetic-repair/`

## Verification

```bash
python3 scripts/frontier_yt_ssb_matching_gap.py
python3 -m py_compile scripts/frontier_yt_ssb_matching_gap.py
python3 scripts/frontier_yt_retention_landing_readiness.py
```

Runner results: SSB verifier `19 PASS, 0 FAIL`; landing-readiness aggregate
`1617 PASS, 0 FAIL`.

## Remaining Blocker

The physical SSB/Yukawa matching theorem remains open. A future route must
derive HS/source normalization, SSB VEV division, chirality projection,
LSZ/external-state normalization, and absence of extra factors from the
retained action.

## Next Exact Action

Run a fresh independent audit on the changed note and runner.
