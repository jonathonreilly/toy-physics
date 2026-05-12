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

The Z3 triplet subroute has advanced but still does not close the lane.  H1 is
supplied by the same-surface Z3 taste-triplet artifact, and H2 is now supplied
by the positive-cone projector certificate `Q_i^+=(I+S_i)/2`.  The refreshed
conditional primitive theorem therefore lists only H3/H4 as remaining:
physical neutral transfer/off-diagonal dynamics and coupling to the PR230
source/canonical-Higgs sector.

This boundary is not a claim that the theorem is impossible.  It says the next
positive step must construct the missing same-surface neutral off-diagonal /
primitive-transfer certificate, or supply future physical rows.

## 2026-05-07 H3/H4 Aperture Wiring Refresh

The completion gate now consumes
`outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json`
directly.  The latest refresh loads the complete `63/63` `C_sx/C_xx` packet as
support-only and keeps the exact missing roots explicit:

- H3 physical neutral transfer / off-diagonal generator: absent;
- H3 primitive-cone or irreducibility certificate: absent;
- H4 source-to-canonical-Higgs coupling: absent;
- finite `C_sx/C_xx` rows remain bounded staging support, not neutral transfer
  or `C_sH/C_HH` rows.

This refresh preserves the route as hard-physics open after a real H3/H4
artifact, but blocks any shortcut that treats H1/H2 Z3 support, commutant rank,
source-only rows, or the current taste-radial packet as primitive-cone
authority.

```bash
python3 scripts/frontier_yt_pr230_neutral_primitive_route_completion.py
# SUMMARY: PASS=15 FAIL=0
```
