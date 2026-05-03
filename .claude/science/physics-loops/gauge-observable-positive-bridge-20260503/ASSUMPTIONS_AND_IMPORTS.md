# ASSUMPTIONS AND IMPORTS - Gauge Observable Positive Bridge

**Date:** 2026-05-03

## Allowed retained / current-surface inputs

| # | Input | Role | Current authority surface |
|---|---|---|---|
| A1 | `A_min` from the stretch note: finite Wilson lattice gauge-scalar path integral at completed `beta_eff`, local Wilson plaquette observable, and local one-plaquette response `R_O(beta)` | Fixed problem surface | `docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md` |
| A2 | Standard Wilson finite-volume path integral identities with exact Haar integration and character orthogonality | Standard QFT / Wilson lattice machinery | Stretch note section 1 and retained Wilson stack |
| A3 | Canonical Wilson normalization `g_bare=1`, `beta=6` | Fixes the physical gauge coupling side; not a fitted observable import | `MINIMAL_AXIOMS_2026-04-11.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, and gauge-scalar temporal completion note |
| A4 | Gauge-scalar temporal completion theorem up to its explicitly conditional observable bridge | Parent reduction target | `docs/GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md` |
| A5 | Gauge-vacuum plaquette character recurrence and source-sector factorization | Narrows exact plaquette to environment character data | `docs/GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md`, `docs/GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md` |
| A6 | Local environment factorization and residual environment identification | Names the missing environment factor without fitting it | `docs/GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md`, `docs/GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md` |
| A7 | Spatial environment transfer / tensor-transfer construction | Supplies the formal operator whose Perron state would determine `rho_(p,q)(6)` | `docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md`, `docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md` |
| A8 | Exact finite-matrix Perron solve once an explicit retained transfer matrix is known | Allowed standard linear algebra | `docs/GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` for reference-solve pattern only |
| A9 | Exact local response inverse and susceptibility-flow law | New branch-derived bounded primitive closing bridge equality without evaluating `P(6)` | `docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_IMPLICIT_FLOW_THEOREM_NOTE_2026-05-03.md` |

## Forbidden load-bearing imports

| # | Forbidden import | Why forbidden here |
|---|---|---|
| F1 | Fitted `beta_eff` chosen to match lattice or PDG data | The user fixed this as forbidden; it would make the bridge observational rather than derived |
| F2 | Perturbative beta-function running as the bridge derivation | The stretch note already excludes it as route O3 |
| F3 | PDG / experimental `alpha_s` or inferred plaquette values | Comparator only; not a Wilson-framework derivation |
| F4 | Monte-Carlo `P(6) ~= 0.5934` | Comparator only; cannot determine `rho_(p,q)(6)` |
| F5 | Same-surface analytic interpolation or monotonicity selector for `P(6)` | Prior no-go says the framework point remains underdetermined |
| F6 | Admitting `Z_6^env(W)` or `rho_(p,q)(6)` as a primitive without retained-grade derivation/authority | This is exactly the missing bridge object; admitting it would restate the gate |
| F7 | A bootstrap or SDP bracket as an exact bridge | Bounds are not equality unless they collapse to a point from allowed constraints |

## Comparators only

- Canonical lattice Monte-Carlo plaquette near `P(6) ~= 0.5934`.
- Existing bridge-support / self-consistency values in the repo.
- Literature lattice bootstrap brackets, if later used, only to audit scale
  and plausibility after a derivation is complete.

## Import ledger conclusion

The Block 01 positive route does not add `Z_6^env(W)` as an admitted axiom.
It closes only the bridge equality by deriving the exact response-coordinate
inverse and susceptibility-flow law. The explicit environment character measure
remains open evaluation data; any later artifact that imports it without
derivation must keep actual current-surface status `open` or
`conditional-support`.
