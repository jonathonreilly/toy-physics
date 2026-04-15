# Assumption / Derivation Ledger

**Date:** 2026-04-15
**Status:** current package ledger for what is assumed, derived, bounded, or open

This file replaces the retired toy-model ledger. It exists so the current
`Cl(3)` / `Z^3` package cannot blur axioms, derived subresults, bounded
bridges, and open gates.

## Current Ledger

| Ingredient / lane | Current status | Safe current statement |
|---|---|---|
| `Cl(3)` local algebra | axiom | accepted framework input |
| `Z^3` cubic lattice | axiom | accepted framework input |
| physical-lattice reading | axiom boundary | accepted framework input; explicit boundary for generation physicality and low-energy matching |
| `g_bare = 1` | accepted framework normalization | current canonical normalization surface |
| plaquette / `u_0` evaluation surface | computed on accepted surface | current package uses the accepted plaquette / mean-field surface |
| anomaly-forced `3+1` | retained / derived | retained theorem on current package |
| exact native `SU(2)` | retained / derived | retained theorem on current package |
| graph-first structural `SU(3)` | retained / derived | retained theorem on current package |
| one-generation matter closure | retained / derived | retained theorem on current package |
| three-generation physicality | retained / derived, axiom-dependent | retained on the physical-lattice reading; see generation axiom boundary note |
| electroweak hierarchy / `v` | retained / derived | `v = 245.080424447914 GeV` on the current accepted evaluation surface |
| `alpha_s(v) = alpha_bare / u_0^2` link-counting step | closed subderivation on open lane | current vertex-power theorem fixes the operator-level `u_0^2` dressing |
| `alpha_s(M_Z)` zero-input route | bounded | strongest current zero-input low-energy route gives `0.1181`, but package keeps the lane bounded |
| `y_t` endpoint at `v` | closed subderivation on open lane | current boundary theorem fixes `v`, not `M_Pl`, as the crossover endpoint |
| backward Ward low-energy bridge | bridge-conditioned support theorem | current EFT bridge note supports the bounded transfer from lattice Ward data to `y_t(v)` |
| zero-input top-mass route | bounded | current strongest zero-input route gives `m_t = 169.4 GeV` |
| import-allowed top-mass route | bounded companion | current strongest import-allowed companion gives `m_t = 171.0 GeV` |
| Higgs mechanism / lattice CW EWSB | derived mechanism-level result | Higgs mechanism is on the current package; exact mass is not |
| exact Higgs mass | open / bounded | no single final non-import Higgs mass authority is promoted |
| CKM quantitative closure | open / bounded | bounded magnitude and partial phase companions exist, but theorem-grade closure is not promoted |
| DM relic mapping | open / bounded | structural DM results exist, but the full relic bridge remains bounded |

## Writing Rule

When summarizing the current package:

- call retained rows retained
- call bounded rows bounded
- call bridge-conditioned rows bridge-conditioned
- do not convert strong bounded numbers into theorem-grade closure by prose

The publication matrix is the final package inventory when this ledger and a
summary note disagree.
