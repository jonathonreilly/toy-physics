# PR230 Schur Route Completion

**Status:** exact negative boundary / strict Schur `A/B/C` route not complete; bounded two-source correlator subblock support present
**Runner:** `scripts/frontier_yt_pr230_schur_route_completion.py`
**Certificate:** `outputs/yt_pr230_schur_route_completion_2026-05-06.json`

The Schur route is real hard-physics support: if a same-surface neutral scalar
kernel basis and block rows `A`, `B`, `C` plus derivatives are supplied, the
Schur-complement formula computes the source-pole denominator derivative.

Current PR230 now has a bounded two-source correlator subblock witness from the
completed taste-radial rows:
`outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json`.
That witness is not source-only data: it packages finite `C_ss/C_sx/C_xx` rows
for the certified source/complement chart.  It is still not the strict Schur
kernel packet because it has no pole derivatives, isolated-pole/FV/IR
authority, canonical `O_H`, or source-overlap bridge.

Existing artifacts also prove sufficiency and reject source-only shortcuts,
compressed-denominator bootstraps, finite ladder row extraction, and
outside-math row naming as physical authority.

This is a current-surface boundary only.  The route reopens with a neutral
kernel basis certificate plus Schur `A/B/C` rows or an equivalent theorem.

```bash
python3 scripts/frontier_yt_pr230_schur_route_completion.py
# SUMMARY: PASS=12 FAIL=0
```
