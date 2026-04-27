# No-Go Ledger

The charged-lepton mass lane already has extensive route-pruning evidence.
This ledger prevents the workstream from reusing killed routes as if they were
new.

| Route | Current disposition | Source | Effect on retained objective |
|---|---|---|---|
| `alpha_s(v)/2` down-type mass-ratio analogy for `m_e/m_mu` | no-go | `MASS_SPECTRUM_DERIVED_NOTE.md` Phase 3 | charged-lepton hierarchy is not the down-quark CKM-dual law |
| `Z_3` invariance alone | no-go | `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` §5.1 | does not force a unique Koide direction |
| Pure APBC temporal refinement | no-go | same §5.2 | off-diagonal curvature vanishes; route permanently closed |
| Observable-principle character symmetry alone | no-go | same §5.3 | does not force equal character weights |
| Native `SU(2)_L` gauge exchange | no-go | same §5.4 | cannot generate cross-species charged-lepton mixing |
| Anomaly-forced `3+1` ingredients | no-go | same §5.5 | species-blind inside charged-lepton sector |
| Universal Koide across sectors | no-go | same §5.6 | Koide is charged-lepton-specific, not a universal sector law |
| Canonical intermediate lift of `O_0 + T_2` | no-go for new diagonal content | same §6.1 | diagonal readout inherits source weights |
| Retained variational principles on current surface | no-go for Koide forcing | same §6.2 | retained `C_3`-invariant principles do not pick the asymmetric point |
| Fourth-order signed Clifford ordering | no-go | same §6.3 | signed ordering sums cancel |
| Current one-Higgs gauge selection | no-go for charged-lepton eigenvalues | `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`; `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md` | selects allowed monomial but leaves `Y_e` free |
| Direct top-Ward lift to charged-lepton `y_tau` | no-go | `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md` | top `1/sqrt(6)` needs the color x isospin `Q_L` surface; charged leptons need a new generation/loop/source primitive |
| Standalone radiative `alpha_LM/(4pi)` tau selector | no-go for tau selection; support retained | `CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md` | electroweak charged-lepton Casimir is `(1, 1, 1)` across generations; assigning the scale to tau requires a separate retained generation/source law |
| Koide `Q` plus selected-line/Brannen phase as standalone generation selector | no-go for generation/tau-scale selection; ratio support retained | `CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md` | `Q` erases the selected-line phase, the `Q` source route and Brannen endpoint are conditional, and cyclic relabelings preserve unordered ratios while moving the largest slot label |

## Closed Cycle 1 Question

Can the top Ward identity be lifted to a charged-lepton `y_tau` theorem without
adding a new generation-selection, loop-normalization, or source-domain
primitive?

Answer: no. The direct lift is closed as an exact retention-gate no-go.

## Closed Cycle 2 Question

Can the existing radiative `alpha_LM/(4pi)` support stack be promoted to a
standalone retained `y_tau` selector?

Answer: no. It remains strong scale support, but its Casimir data are
generation-blind and cannot select tau without a new primitive.

## Closed Cycle 3 Question

Can the current Koide `Q` support plus selected-line/Brannen phase support be
promoted to a retained generation-selection primitive without PDG charged-
lepton masses?

Answer: no. The combination remains useful ratio/phase support, but it does
not select the physical source-free `Q` representative, the based selected-
line endpoint/radian readout, or a non-observational generation/tau-scale
label. A new physical source/endpoint/generation law is required.
