# PR230 Schur Route Completion

**Status:** exact negative boundary / Schur `A/B/C` route not complete on current PR230 surface
**Runner:** `scripts/frontier_yt_pr230_schur_route_completion.py`
**Certificate:** `outputs/yt_pr230_schur_route_completion_2026-05-06.json`

The Schur route is real hard-physics support: if a same-surface neutral scalar
kernel basis and block rows `A`, `B`, `C` plus derivatives are supplied, the
Schur-complement formula computes the source-pole denominator derivative.

Current PR230 does not supply those rows.  Existing artifacts prove sufficiency
and reject source-only shortcuts, compressed-denominator bootstraps, finite
ladder row extraction, and outside-math row naming as physical authority.

This is a current-surface boundary only.  The route reopens with a neutral
kernel basis certificate plus Schur `A/B/C` rows or an equivalent theorem.

```bash
python3 scripts/frontier_yt_pr230_schur_route_completion.py
# SUMMARY: PASS=11 FAIL=0
```
