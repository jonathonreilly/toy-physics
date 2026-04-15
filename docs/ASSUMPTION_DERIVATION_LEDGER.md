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
| hierarchy / `v` theorem | derived | `v = 246.28 GeV` is on the promoted package surface. |
| `R_conn = 8/9` color factor | derived | Canonical authority is [RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md); it is not a fit knob. |
| EW normalization package | derived | `sin^2(theta_W)`, `1/alpha_EM`, `g_1(v)`, and `g_2(v)` are now promoted with the complete chain. |
| renormalized `y_t` endpoint | derived | `y_t(v) = 0.9176` is now promoted with the complete chain. |
| top pole mass package | derived | `m_t(pole) = 172.57 GeV` (2-loop) and `173.10 GeV` (3-loop) are promoted package rows. |
| Higgs CW/stability package | derived | `m_H = 119.8 GeV` (2-loop), `129.7 GeV` (full 3-loop boundary), and absolute vacuum stability are promoted package rows. |
| DM relic mapping | bounded/open | Strong bounded companions remain, but the relic bridge is still not closed. |
| CKM quantitative closure | bounded/open | Strong bounded flavor subresults exist, but ab initio quantitative closure is not promoted. |

## Writing rule

- call computed inputs computed
- call derived rows derived
- call bounded rows bounded
- do not demote a promoted row by leaving it on a stale bounded package
- do not convert DM or CKM companions into theorem-grade closure by prose
