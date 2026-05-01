# Lane 2 Assumptions And Imports

**Updated:** 2026-05-01T10:53:48Z  
**Loop:** `lane2-atomic-scale-20260428`  
**Science block:** 01  
**Claim boundary:** open/scaffold-only unless a later artifact retires the listed blockers.

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `1/alpha_EM(M_Z) = 127.67` | Existing framework EW-scale coupling input; possible high-scale endpoint for QED running | derived | `docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md`, `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` | yes for QED-running route | yes for any alpha(M_Z) -> alpha(0) route | retained threshold-resolved QED transport bridge | usable high-scale input only; not atomic alpha(0) |
| `alpha(0)` | Low-energy Coulomb coupling in the Rydberg formula | unsupported import for framework closure; comparator in scaffold | `scripts/frontier_atomic_rydberg_dependency_firewall.py`, `docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md` | yes | yes | derive threshold-resolved QED bridge or admit as non-derivation comparator | open Nature-grade blocker |
| `m_e` | Electron mass in `E_1 = -m_e alpha(0)^2 / 2` | unsupported import for framework closure; textbook comparator in scaffold | `docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md`, `docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md` | yes | yes | Lane 6 charged-lepton mass retention / y_e activation law, recorded only as dependency here | open blocker; do not work Lane 6 in this loop |
| Nonrelativistic Coulomb/Schrodinger limit in physical units | Downstream bridge from framework substrate to the hydrogen Hamiltonian | admitted standard bridge in scaffold | `docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md` | yes | yes | prove retained physical-unit reduction or demote scaffold-only use | open blocker |
| `b_QED = (2/3)(N_color + 1)^2 = 32/3` | Structural asymptotic QED beta coefficient ingredient | retained/exact structural support, above all thresholds only | `docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md` | yes for QED-running route | not sufficient alone | threshold-resolved decoupling theorem plus retained charged thresholds | support ingredient; not an alpha(0) bridge |
| Charged particle threshold masses | Decoupling scales in alpha(M_Z) -> alpha(0) transport | unsupported imports for Lane 2 closure | charged leptons, quarks, hadronic vacuum polarization; no Lane 2 retained set | yes | yes for QED bridge | retained mass thresholds or exact insensitivity/no-go theorem | open blocker; Lane 6/Lane 3/Lane 1 dependencies only |
| Hadronic vacuum polarization / quark threshold convention | Nonperturbative low-energy contribution to alpha transport | unsupported import / standard correction context | not retained in Lane 2 | yes for precision alpha(0) bridge | yes unless shown negligible under target status | Lane 1/3 hadronic support or admitted comparator-only correction | open blocker |
| Existing hydrogen/helium eigensolver | Numerical scaffold for substitution once inputs are retained | bounded exploratory scaffold | `docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md`, `scripts/frontier_atomic_hydrogen_helium_probe.py` | yes as future harness | yes for verification, not as derivation | substitute retained inputs after upstream gates close | scaffold success separated from closure |
| Existing Rydberg firewall | Negative boundary separating alpha(M_Z) from alpha(0) and textbook inputs | exact negative boundary on current surface | `docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`, `scripts/frontier_atomic_rydberg_dependency_firewall.py` | yes as no-go memory | yes for honest status | refine into actionable threshold theorem if possible | active baseline |
| Literature / textbook QFT beta-function formulae | Standard form of one-loop gauge running and decoupling logic | literature theorem / admitted standard bridge | already used by `docs/SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md` | yes for running-route proof shape | yes if a QED bridge is attempted | record as bridge, not framework derivation | allowed as standard theorem context |

## Immediate Audit Result

No retained Rydberg closure is available at loop start. The highest-leverage
non-overlapping route is to determine whether the retained structural QED beta
coefficient can honestly upgrade the alpha(M_Z) -> alpha(0) bridge, or whether
it instead sharpens the dependency firewall by proving a threshold-resolved
transport prerequisite.

## Block 01 Update

`scripts/frontier_atomic_qed_threshold_bridge_firewall.py` proves that
`alpha_EM(M_Z)` plus the retained asymptotic `b_QED=32/3` does not determine
`alpha(0)`. The newly exposed load-bearing import is threshold-resolved QED
decoupling: charged thresholds and hadronic/vacuum-polarization handling must
be supplied or shown irrelevant before `alpha(0)` can be treated as retained.
