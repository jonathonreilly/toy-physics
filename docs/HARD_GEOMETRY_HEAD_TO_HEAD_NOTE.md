# Hard Geometry Head-To-Head Note

**Date:** 2026-04-03  
**Status:** review-safe head-to-head summary

This note compares the three hard-geometry lanes that are still worth
carrying forward after the hardening pass:

- dense central-band hard geometry + layer norm
- generated asymmetry-persistence hard geometry + layer norm
- mirror symmetry / Z2-protected transfer geometry

The comparison is intentionally narrow. It uses only the retained metrics
that are already supported on `main`:

- corrected Born `|I3|/P`
- `pur_min` / `pur_cl`
- gravity centroid delta
- narrow range statements

## 1. Dense Central-Band + Layer Norm

This is the strongest retained same-graph joint lane.

Best retained high-N row:

- `N = 80`, `npl = 80`
- `LN + |y|`
- Born: `0.000±0.000`
- `pur_min = 0.500±0.000`
- gravity: `+2.799±1.612`

With collapse included, the same pocket keeps Born clean and lowers the
purity floor further:

- `LN + |y| + collapse`
- purity: `0.374±0.057`
- gravity: `+2.929±1.467`

Narrow read:

- this is the best joint coexistence pocket
- it is Born-clean
- it is still bounded and narrows by `N = 100`

## 2. Generated Asymmetry-Persistence + Layer Norm

This is the strongest retained gravity-side lane.

Best retained direct gravity row:

- `N = 100`
- threshold `0.20`
- Born: `2.31e-16`
- `pur_cl = 0.921±0.043`
- gravity: `+2.102±0.825`

Mass-side follow-up:

- threshold `0.10`, LN: `delta ~= 0.4032 * M^0.420`, `R^2 = 0.970`
- threshold `0.20`, LN: `delta ~= 0.5332 * M^0.262`, `R^2 = 0.892`

Narrow read:

- this lane is Born-clean on the dense probe
- it carries the stronger direct gravity-side signal
- it is the best gravity-side-alone vector
- it is not the best joint coexistence lane because the gravity sign is
  density-sensitive and not uniformly positive across the dense scan

## 3. Mirror Chokepoint / Z2-Protected Transfer

This is the highest-upside idea, and it is now artifact-backed at small `N`,
but it is still provisional.

Current status:

- [`scripts/mirror_chokepoint_joint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_chokepoint_joint.py)
- Born-clean at `N=15` and `N=25`
- `gravity = +1.2927±0.691` at `N=15`
- `gravity = +2.2748±0.525` at `N=25`
- `pur_cl = 0.5769±0.02` at `N=15`
- `pur_cl = 0.7329±0.05` at `N=25`
- fails by `N=40+`

Narrow read:

- conceptually the most interesting symmetry-protection idea
- Born-safe in the tested chokepoint range
- not yet scalable enough to outrank the retained hard-geometry lanes

## Head-To-Head Ranking

1. Best joint coexistence: dense central-band + layer norm
2. Best gravity side alone: generated asymmetry-persistence + layer norm
3. Highest-upside but provisional: mirror chokepoint / Z2-protected transfer

## Bottom Line

Hard geometry remains the shared enabler. The cleanest retained joint lane
is dense central-band + layer norm. The strongest retained gravity-side lane
is generated asymmetry-persistence + layer norm. Mirror chokepoint is now the
most promising unresolved vector, but it still stops at small `N` and remains
provisional.
