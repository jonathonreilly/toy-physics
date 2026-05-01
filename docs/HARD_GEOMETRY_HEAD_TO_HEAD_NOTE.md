# Hard Geometry Head-To-Head Note

**Date:** 2026-04-03  
**Status:** support - structural or confirmatory support note

This note compares the retained hard-geometry and symmetry lanes that are
still worth carrying forward after the hardening pass, plus the emergence-
facing grown-graph density constraint:

- dense central-band hard geometry + layer norm
- mirror symmetry / Z2-protected transfer geometry
- higher-symmetry `Z2 x Z2`
- generated asymmetry-persistence hard geometry + layer norm
- grown-graph density optimum near `npl≈30`

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

## 2. Mirror Chokepoint / Z2-Protected Transfer

This is now a real retained bounded pocket and the strongest symmetry-protected
challenger.

Best retained rows:

- dense boundary family with canonical fit
- `N = 100` retained on the dense boundary scan
- `NPL_HALF = 60`, `connect_radius = 5.0`
- strict chokepoint mirror
- Born `|I3|/P = 1.13e-15`
- `pur_cl = 0.9043±0.02`
- gravity: `+1.3089±0.570`

Canonical boundary fit:

- `(1 - pur_cl) = 0.3901 × N^(-0.245)`
- `R² = 0.126`

Range check:

- retained through `N = 100` on the dense boundary scan
- `N = 120` is the gravity wall

Narrow read:

- stronger retained gravity than the dense central-band row at `N = 40/60`
- weaker decoherence than the dense central-band row
- longer retained range than the strict pocket, but still bounded
- still Born-clean in the retained pocket

## 3. Higher-Symmetry `Z2 x Z2`

This is the best decoherence-side symmetry lane.

Best retained row:

- `N = 80`
- `pur_cl = 0.783±0.019`
- Born `|I3|/P = 1.48e-15`
- gravity at `k = 5`: `+2.771±0.567`
- gravity band: `+1.736±0.337`

Narrow read:

- Born-clean through the full tested window
- positive gravity signal at all tested `N`
- slower decoherence decay than the random baseline
- not the best gravity-side lane and not the best joint lane

## 4. Generated Asymmetry-Persistence + Layer Norm

This remains the strongest retained gravity-side lane.

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
- it is the best gravity side alone
- it is not the best joint coexistence lane because the gravity sign is
  density-sensitive and not uniformly positive across the dense scan

## 5. Grown-Graph Density Optimum

This is the best emergence-facing lane.

Retained read:

- grown graphs favor a density optimum near `npl≈30`
- dense grown graphs fail because CLT dominates
- exact symmetry works at any density because it preserves slit separation structurally

Narrow read:

- this is the strongest retained growth-law constraint
- it is not a better joint lane than the hard-geometry families

## Head-To-Head Ranking

1. Best joint coexistence: dense central-band + layer norm
2. Best symmetry-protected lane: mirror chokepoint / Z2-protected transfer
3. Best decoherence-side symmetry lane: `Z2 x Z2`
4. Best gravity side alone: generated asymmetry-persistence + layer norm
5. Best emergence-facing lane: grown-graph density optimum near `npl≈30`

## Bottom Line

Hard geometry remains the shared enabler. The cleanest retained joint lane is
dense central-band + layer norm. The strongest symmetry-protected challenger
is mirror chokepoint / Z2-protected transfer, which now reaches `N = 100` on
the dense boundary scan but remains bounded with `N = 120` as the gravity
wall. The strongest decoherence-side symmetry lane is `Z2 x Z2`, and the
strongest retained gravity-side-alone lane is generated asymmetry-persistence
+ layer norm. The strongest emergence-facing constraint is the grown-graph
density optimum near `npl≈30`; dense grown graphs fail once CLT dominates.
