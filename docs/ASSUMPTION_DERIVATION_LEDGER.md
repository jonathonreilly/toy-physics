# Assumption / Derivation Ledger

**Status:** current package ledger for what is assumed, derived, bounded, or
open
**Date:** 2026-04-15

This file exists to stop the package from blurring axioms, computed inputs,
derived quantitative rows, and still-open companion lanes.

## Current ledger

| ingredient | current status | what is actually true now |
|---|---|---|
| `Cl(3)` on `Z^3` as physical theory | assumed framework axiom | This is the starting physical postulate of the package. |
| `M_Pl` as UV cutoff | assumed framework scale | Treated as the framework cutoff, not fitted from the SM. |
| SU(3) plaquette `<P> = 0.5934` at `beta = 6` | computed from the axiom | The complete prediction chain uses one computed lattice input, not an experimental import. |
| exact structural gauge/matter backbone | derived | `SU(3) x SU(2) x U(1)`, three generations, anomaly-forced `3+1`, and the retained matter structure are package-grade. |
| hierarchy / `v` theorem | derived | `v = 245.080424447914 GeV` is retained on the hierarchy lane; it is not part of the separate quantitative component stack. |
| `R_conn = 8/9` color factor | derived | Canonical authority is [RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md); it is not a fit knob. |
| EW normalization package | derived / retained quantitative lane | `sin^2(theta_W)`, `1/alpha_EM`, `g_1(v)`, and `g_2(v)` form a standalone retained EW lane. |
| renormalized `y_t` endpoint | bounded / derived | `y_t(v) = 0.9176` is a zero-import central value, but it inherits an approximately `3%` QFP/RGE-surrogate systematic. |
| top pole mass package | bounded / derived | `m_t(pole) = 172.57 GeV` (2-loop) and `173.10 GeV` (3-loop) inherit the bounded `y_t` systematic. |
| Higgs CW/stability package | bounded | the mechanism and boundary structure are derived, but exact `m_H` and vacuum stability remain bounded pending a framework-native full 3-loop implementation. |
| DM relic mapping | bounded/open | Strong bounded companions remain, but the relic bridge is still not closed. |
| CKM quantitative closure | bounded/open | Strong bounded flavor subresults exist, but ab initio quantitative closure is not promoted. |

## Writing rule

- call computed inputs computed
- call derived rows derived
- call bounded rows bounded
- do not demote a promoted row by leaving it on a stale bounded package
- do not convert DM or CKM companions into theorem-grade closure by prose
