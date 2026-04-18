# Publication Control Plane

**Date:** 2026-04-15
**Purpose:** define how claims are admitted to the package without creating
parallel authority paths

## Package Layers

1. retained flagship core
2. bounded observation-facing portfolio
3. live flagship gates
4. frozen-out families

## Current Lane Rule

Each lane gets one canonical authority stack.

For the current live quantitative gauge / YT / Higgs stack, that authority
surface is:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md)
- [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md)
- [YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../YT_EW_DELTA_R_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](../../YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
- [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md)
- [YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md](../../YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md)
- [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)
- [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md)
- [HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)

For the current bounded charged-lepton package, that stack is:

- [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](../../CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
- [CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md](../../CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- [HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md](../../HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md)
- [MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md](../../MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md)
- [STRUCTURAL_NO_GO_SURVEY_NOTE.md](../../STRUCTURAL_NO_GO_SURVEY_NOTE.md)
- [HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md](../../HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)

Older route notes may remain in the repo, but they are not package authority
unless the package links to them directly.

## File Roles

| File | Role |
|---|---|
| [README.md](./README.md) | package front door |
| [EXTERNAL_REVIEWER_GUIDE.md](./EXTERNAL_REVIEWER_GUIDE.md) | reviewer read order |
| [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) | canonical inventory |
| [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md) | narrative explanation of the inventory |
| [CLAIMS_TABLE.md](./CLAIMS_TABLE.md) | retained manuscript claim surface |
| [DERIVATION_ATLAS.md](./DERIVATION_ATLAS.md) | reusable theorem / subderivation toolbox |
| [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) | retained evidence contract plus bounded live-gate capture |
| [RESULTS_INDEX.md](./RESULTS_INDEX.md) | note / runner map for captured components |
| [Historical frozen-out registry](../../work_history/publication/FROZEN_OUT_REGISTRY.md) | explicit registry of excluded families |

## Promotion Rule For New Science

Any newly landed component should enter the package in this order:

1. land or refresh the local authority note and runner
2. classify it in [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
3. explain that classification in [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
4. if it belongs to the retained surface, add it to:
   [CLAIMS_TABLE.md](./CLAIMS_TABLE.md) and
   [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
5. if it belongs to a bounded live-gate stack, add every required component to:
   [DERIVATION_ATLAS.md](./DERIVATION_ATLAS.md) and
   [RESULTS_INDEX.md](./RESULTS_INDEX.md)
6. if it stays excluded, update [Historical frozen-out registry](../../work_history/publication/FROZEN_OUT_REGISTRY.md)
7. only then update manuscript prose

## Replacement Rule

Do not append a new canonical note on top of a stale canonical note.

When a lane is promoted or cleaned:

- replace the stale front-door wording
- replace stale package routing
- keep route history outside the authority stack

The package should show one live current stack per lane, not archaeology.
