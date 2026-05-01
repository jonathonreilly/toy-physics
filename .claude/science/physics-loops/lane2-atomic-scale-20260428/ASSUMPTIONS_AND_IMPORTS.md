# Lane 2 Assumptions And Imports

**Updated:** 2026-05-01T11:47:19Z
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
| Dimensionless lattice Coulomb Hamiltonian `H_g = -Delta_x - g/|x|` | Coupling-relative atomic companion and input to the scale-bridge stretch | bounded support / retained-operator-surface companion | `docs/work_history/atomic/HYDROGEN_HELIUM_ATOMIC_COMPANION_NOTE_2026-04-18.md`, `scripts/frontier_atomic_hydrogen_lattice_companion.py` | yes for the physical-unit stretch | yes as a conditional bridge surface | prove exact scaling to physical Hamiltonian and isolate remaining unit inputs | usable for exact conditional scale algebra; not absolute eV closure |
| Continuum Coulomb spectrum `lambda_n = -g^2/(4 n^2)` | Algebraic bridge between dimensionless lattice scaling and Bohr formula | admitted standard Coulomb theorem / exact support bridge | `scripts/frontier_atomic_nr_coulomb_scale_bridge.py` | yes for the scale theorem | yes for the stretch artifact only | replace with framework-native spectral theorem if demanded by review | allowed support bridge; not framework-native by itself |
| Physical length map `a = g/(2 mu Z alpha)` | Converts dimensionless lattice coordinate to physical units | admitted unit map in the stretch theorem | `.claude/science/physics-loops/lane2-atomic-scale-20260428/notes/ATOMIC_NR_COULOMB_SCALE_BRIDGE_STRETCH_NOTE_2026-05-01.md` | yes | yes for retained physical-unit closure | derive kinetic normalization/unit map from framework or keep as open bridge | exact conditional map; still open as framework-native retention |
| Rydberg product `mu alpha(0)^2` | The single product fixed by an absolute Coulomb energy after the standard map is admitted | exact factorization support / not a derivation of the gates | `.claude/science/physics-loops/lane2-atomic-scale-20260428/notes/ATOMIC_RYDBERG_GATE_FACTORIZATION_FANOUT_NOTE_2026-05-01.md`, `scripts/frontier_atomic_rydberg_gate_factorization_fanout.py` | yes | yes as a dependency boundary | derive `mu` and `alpha(0)` independently, or explicitly demote to a fitted product | open; the product cannot retire the separate mass and coupling gates |
| Planck/source-unit lattice anchor | Possible fixed physical-lattice length context for the atomic coordinate | package pin / conditional Planck support context | `docs/PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md`, `docs/PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`, `.claude/science/physics-loops/lane2-atomic-scale-20260428/notes/ATOMIC_PLANCK_UNIT_MAP_FIREWALL_NOTE_2026-05-01.md` | yes if used in unit-map route | not sufficient alone | derive the atomic effective coupling map on the same surface | length/source context only; not an atomic Rydberg closure |
| `g_atomic = 2 mu a_lat Z alpha(0)` | Dimensionless coupling needed to put the atomic Coulomb problem on a fixed lattice length anchor | exact conditional bridge | `scripts/frontier_atomic_planck_unit_firewall.py` | yes | yes | retain `mu`, retain `alpha(0)`, and derive the low-energy kinetic/coupling map | open; Planck unit does not determine it |
| `T_EM = sum_f N_c Q_f^2 log(M_Z/m_f^eff)` | Weighted threshold moment needed for one-loop `alpha_EM(M_Z) -> alpha(0)` transport | exact reduction / exposed prerequisite | `.claude/science/physics-loops/lane2-atomic-scale-20260428/notes/ATOMIC_ALPHA0_THRESHOLD_MOMENT_NO_GO_NOTE_2026-05-01.md`, `scripts/frontier_atomic_alpha0_threshold_moment_no_go.py` | yes | yes for `alpha(0)` route | derive charged-threshold and hadronic matching moment, or prove target-status insensitivity | open; charges/counts fix weights, not logs or matching |
| Massive relativistic dispersion `E^2 = m^2 + p^2` | Conditional bridge to the Schrodinger kinetic prefactor after rest-energy subtraction | exact conditional support bridge | `docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md`, `docs/LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md`, `scripts/frontier_atomic_massive_nr_limit_bridge.py` | yes for kinetic-limit route | not sufficient alone | retain the low-energy one-particle mass sector and Coulomb coupling on the same surface | usable bridge; atomic prefactor remains mass-gated |
| Schrodinger kinetic prefactor `1/(2m)` | Physical-unit kinetic normalization in the atomic Hamiltonian | exact conditional consequence / open retained input | `.claude/science/physics-loops/lane2-atomic-scale-20260428/notes/ATOMIC_MASSIVE_NR_LIMIT_BRIDGE_NOTE_2026-05-01.md` | yes | yes | derive retained `m_e`/reduced mass without Lane 6 collision, or keep as admitted bridge/comparator | open; Lorentz support does not pick electron mass |

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

## Block 01 Stretch Update

`scripts/frontier_atomic_nr_coulomb_scale_bridge.py` proves the exact
conditional physical-unit scale identity:

```text
H_g = -Delta_x - g/|x|
g = 2 mu a Z alpha
E = lambda / (2 mu a^2)
=> E_n = -mu (Z alpha)^2 / (2 n^2)
```

This partially sharpens the nonrelativistic Coulomb/Schrodinger gate: once
`mu/m_e`, `alpha(0)`, and a physical unit map are supplied, the dimensionless
companion needs no fitted Rydberg target. It does not retire those inputs and
does not make the physical unit map framework-native.

## Block 01 Fan-Out Update

`scripts/frontier_atomic_rydberg_gate_factorization_fanout.py` proves the
current gate factorization and records the required stuck fan-out. The fan-out
checks five non-overlapping frames: minimal Coulomb algebra, QED running,
charged-lepton mass, physical-unit kinetic map, and scaffold falsifier.

The new import boundary is that a single Rydberg-scale number constrains only
the product `mu alpha(0)^2` after the standard map is supplied. It does not
derive retained `mu`, retained `alpha(0)`, or the framework-native unit map.
The honest status remains open with exact gate-factorization support.

## Block 01 Planck-Unit Map Update

`scripts/frontier_atomic_planck_unit_firewall.py` proves that the current
Planck/source-unit package does not close the Lane 2 atomic physical-unit map.
Even if the package pin `a_lat = 1/M_Pl` is used as a length anchor, the atomic
dimensionless coupling is still

```text
g_atomic = 2 mu a_lat Z alpha(0).
```

Current Lane 2 has not retained `mu` or `alpha(0)`, so the Planck unit moves
the unit-map problem into `g_atomic` rather than retiring it. The direct route
that identifies the finite-box companion's convenient `g=1` with the Planck
lattice coupling is an exact no-go: with comparator electron mass and
Planck spacing it would require a non-atomic low-energy coupling and gives a
super-Planckian atomic energy scale.

## Block 01 Alpha(0) Threshold-Moment Update

`scripts/frontier_atomic_alpha0_threshold_moment_no_go.py` proves the sharper
one-loop reduction for the QED-running gate:

```text
1/alpha_low
  = 1/alpha(M_Z)
    + (2 / 3 pi) T_EM
    + Delta_match,
T_EM = sum_f N_c Q_f^2 log(M_Z/m_f^eff).
```

The retained charge/count surface fixes `sum_f N_c Q_f^2 = 8` and therefore
`b_QED = 32/3`; it does not fix `T_EM` or `Delta_match`. The exact open
import for any future Lane 2 `alpha(0)` route is now a threshold/matching
moment theorem or an exact insensitivity theorem.

## Block 01 Massive NR Limit Update

`scripts/frontier_atomic_massive_nr_limit_bridge.py` proves the conditional
kinetic bridge from the retained Lorentz/dispersion support surface:

```text
E^2 = m^2 + p^2
E - m = p^2/(2m) + O(p^4/m^3).
```

This sharpens the physical-unit Schrodinger-limit gate by isolating the
kinetic prefactor. It does not retire the mass gate: different retained masses
produce different kinetic prefactors, and Lane 2 still lacks retained
electron/reduced mass, retained `alpha(0)`, and a retained Coulomb coupling in
the same low-energy sector.
