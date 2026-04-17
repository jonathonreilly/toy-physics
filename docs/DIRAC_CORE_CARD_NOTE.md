# Dirac 3+1D Core Card Note

**Date:** 2026-04-10  
**Harness:** [`scripts/frontier_dirac_walk_3plus1d_core_card.py`](../scripts/frontier_dirac_walk_3plus1d_core_card.py)

This note freezes the first literal **16-row** integrated `DIR-3D` core-card
runner. The goal is
to stop treating the Dirac lane as four disconnected probes (`v3`, `v4`,
decoherence, panel) and instead report one consolidated read.

## Operating Point

- operating point: `n = 17`, `N = 12`, `m0 = 0.10`, `strength = 5e-4`, `offset = 3`
- stability point: `n = 29`
- `N` sweep for growth: `8,10,12,14,16,18,20,22,24`
- offset sweep for distance law: `2,3,4,5,6` at `N = 16`

## Integrated Result

The current integrated score is:

- **12/16**

Retained positives:

- `C1` Born `|I3|/P = 3.98e-16`
- `C2` slit distinguishability `d_TV = 0.7898`
- `C3` null control exact
- `C4` `F∝M` linearity `R^2 = 1.000000`
- `C5` TOWARD gravity bias at the retained operating point
- `C6` explicit record-purity decoherence row passes on both tested geometries
- `C7` mutual information positive
- `C8` purity stability `CV = 0.3801`
- `C12` AB visibility `V = 0.5056`
- `C14` split mass vs gravity susceptibility passes with `best_g = 0.030`,
  `R^2 = 1.0000`
- `C15` boundary robustness passes with periodic/open sign agreement
  `9/9` on the `N` sweep and `5/5` on the offset sweep
- `C16` multi-observable gravity passes under the primary readouts:
  centroid/shell agree `5/6`, first-arrival is stable

Failures:

- `C9` gravity growth with propagation is non-monotone
- `C10` distance law is mixed-sign at the larger-lattice stress point (`3/5` TOWARD)
- `C11` strict isotropy gate fails even though the low-k KG fit is exact:
  `R^2 = 1.000000`, isotropy ratio `1.1034`
- `C13` fixed-`theta` `k`-achromaticity fails: matched-travel `k` sweep has
  `CV = 0.3606` and the measured deflection stays wavelength-sensitive

## Interpretation

This is the cleanest current 3+1D read on the branch:

- the `DIR-3D` lane is the first retained 3+1D route that closes proper Born,
  exact low-k KG, nonzero AB, `F∝M`, split susceptibility, boundary robustness,
  and a positive operating-point gravity bias
- the remaining blocker is not “does 3D work at all?” but “why does the gravity
  lane stay non-monotone and mixed-sign under deeper stress?”
- the multi-observable panel shows that centroid and shell are the primary
  sign gates; peak is too wave-sensitive to serve as a promotion metric

## Carry-Forward

The right next attacks are no longer broad moonshots. They are targeted fixes
for the remaining three failures:

1. explain or remove the `N`-growth oscillation
2. clean up the mixed-sign offset law
3. close the residual isotropy gap under the strict `C11` gate
4. reduce the surviving carrier-`k` sensitivity in `C13`
