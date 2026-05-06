# PR230 Neutral Primitive Route Completion

**Status:** exact negative boundary / neutral primitive-rank-one route not complete on current PR230 surface
**Runner:** `scripts/frontier_yt_pr230_neutral_primitive_route_completion.py`
**Certificate:** `outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json`

This is the theorem-native hard-physics lane.  Conditional Perron/rank-one
support already exists: if PR230 supplies a same-surface positivity-improving
neutral transfer operator, an isolated lowest pole, and positive source/Higgs
overlaps, the source pole and canonical Higgs pole can be identified without
source-coordinate fiat.

Current PR230 does not supply that premise.  The branch has no primitive-cone
certificate, no neutral irreducibility certificate, no off-diagonal neutral
generator, and no accepted rank-one purity certificate.  Existing commutant,
decoupling, no-orthogonal-coupling, and source-only shortcuts are checked and
blocked.

This boundary is not a claim that the theorem is impossible.  It says the next
positive step must construct the missing same-surface neutral off-diagonal /
primitive-transfer certificate, or supply future physical rows.

```bash
python3 scripts/frontier_yt_pr230_neutral_primitive_route_completion.py
# SUMMARY: PASS=12 FAIL=0
```
