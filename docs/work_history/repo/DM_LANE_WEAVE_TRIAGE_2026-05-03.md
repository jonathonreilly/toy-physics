# DM Lane Weave Triage — 2026-05-03

**Status:** historical / diagnostic — repo-hygiene governance packet for the
DM flagship lane; documents weave-or-not decisions for ~63 unwoven DM_*
theorem notes; introduces no canonical-surface changes.

## Purpose

This triage packet answers a single governance question raised by the
companion canonical-weave audit
([`CANONICAL_WEAVE_AUDIT_2026-05-03.md`](CANONICAL_WEAVE_AUDIT_2026-05-03.md),
PR `#448`): **should the unwoven DM_* theorem notes on `main` be woven onto
the canonical authority surfaces, or are they appropriately classified as
historical / diagnostic route history that should remain unwoven?**

The DM lane is currently classified as `open flagship lane` in
[`docs/ASSUMPTION_DERIVATION_LEDGER.md`](../../ASSUMPTION_DERIVATION_LEDGER.md):
"Exact transport-chain progress is real, but final DM quantitative closure
is still not closed." The retained surface and the historical / diagnostic
/ route-history surface are separated by design per
[`docs/repo/CONTROLLED_VOCABULARY.md`](../../repo/CONTROLLED_VOCABULARY.md);
this triage uses only the existing controlled vocabulary.

## Scope and method

Enumeration script:

```
ls docs/DM_*_THEOREM_NOTE*.md
# for each, check whether filename appears in any of:
#   docs/CANONICAL_HARNESS_INDEX.md
#   docs/publication/ci3_z3/DERIVATION_ATLAS.md
#   docs/repo/LANE_REGISTRY.yaml
#   docs/work_history/repo/LANE_STATUS_BOARD.md
```

Of 107 `DM_*_THEOREM_NOTE*.md` files on `main`, 44 are already referenced on
at least one canonical authority surface (overwhelmingly via
`DERIVATION_ATLAS.md` section `G. DM and cosmology tools`) and 63 are not.
This packet triages the 63 unwoven notes by sub-family.

For each sub-family, this packet samples the **Status:** line declared
inside each note (the note-level claim-strength label) and records what the
notes say about themselves.

## Existing classification

From [`docs/ASSUMPTION_DERIVATION_LEDGER.md`](../../ASSUMPTION_DERIVATION_LEDGER.md)
(row "DM flagship lane"):

> | DM flagship lane | open flagship lane | Exact transport-chain progress
> is real, but final DM quantitative closure is still not closed. |

The ledger preamble adds the explicit guardrail:

> do not convert DM or CKM companions into theorem-grade closure by prose

`docs/work_history/repo/LANE_STATUS_BOARD.md` does not currently carry a DM
row; the historical lane-board is scoped to gravity / staggered / Wilson /
Z2 / mirror lanes, and the DM lane is tracked through the ledger row above
plus the live atlas section.

`docs/repo/LANE_REGISTRY.yaml` likewise carries no DM lane entry.

`docs/publication/ci3_z3/DERIVATION_ATLAS.md` carries section `G. DM and
cosmology tools` with ~50 woven DM/leptogenesis/PMNS rows, all uniformly
labeled `exact subderivation on open gate`,
`exact reduction theorem on open gate`,
`exact obstruction theorem on open gate`,
`exact boundary theorem on open gate`,
`exact negative closeout on open gate`,
`exact transport provenance`,
`bounded support theorem`, or `bounded package on open gate`.

## Inventory: unwoven DM_* notes by sub-family (63 total)

| Sub-family | Count | Representative declared **Status:** lines |
|---|---|---|
| `DM_NEUTRINO_*` | 18 | `exact positive atmospheric-scale theorem on the current diagonal`; `exact triplet-coordinate form of the intrinsic DM CP tensor`; `support — structural or confirmatory support note` (×9 across triplet/even-response/two-Higgs/swap notes); `bounded conditional normalization selector`; `bounded conditional theorem — IF the projectors and block M(m,j) are supplied as inputs, THEN the Schur return ...`; `exact local structural theorem on the DM circulant coefficient space`; `exact theorem on the activation law of the invented phase-lift`; `bounded — bounded or caveated result note` |
| `DM_WILSON_*` | 16 | `exact flagship-route refinement theorem after the Wilson-parent audit`; `exact current-main frontier theorem clarifying what remains open`; `exact source-side reduction theorem on the open DM gate`; `exact current-branch theorem sharpening the DM transport-side`; `exact current-branch nonuniqueness theorem for constructive-sign`; `exact multiplicity theorem on the constructive positive branch`; `exact local differential theorem on the open DM selector gate`; `exact translation theorem for the live conditional branch-choice`; `exact theorem exhausting the "positive branch alone" selector`; `exact constructive theorem showing the structured Wilson response`; `support-level candidate only — the path is still chosen`; `support — structural or confirmatory support note` |
| `DM_PMNS_*` | 7 | `exact no-go for the current exact local selector families`; `honest no-go on the current theorem stack`; `exact positive current-activation theorem on the proposed_retained hw=1 response family`; `support — structural or confirmatory support note` (×4 covering chamber/seed/ordered-chain/upper-octant) |
| `DM_LEPTOGENESIS_*` | 6 | `bounded — bounded or caveated result note` (×4: projection, flavor-column functional, analytic stationary classification, relative-action stationarity); transport-decomposition / transport-integral notes carry no explicit `Status:` line — paired exact-result family rather than headline closures |
| `DM_SELECTOR_*` | 5 | `selector-side support theorem on the open DM gate` (×3: branch-separation, threshold-stabilization, shifted-doublet imag-sign); `selector-side bridge support theorem on the open DM gate`; `support — structural or confirmatory support note` |
| `DM_ABCC_*` | 4 | `support — structural or confirmatory support note` (cubic closure); `SUPPORT THEOREM. The old chamber+DPLE route survives the audit`; `bounded — bounded or caveated result note` (×2: PMNS non-singularity, signature forcing) |
| `DM_SIGMA_HIER_*` | 2 | `no-go theorem for a named derivation family. Any H-intrinsic or ...`; `conditional/support theorem on the open DM PMNS gate` |
| `DM_*` (singletons) | 5 | `DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM`: "Exact matrix-analysis theorem; status is **support**"; `DM_EFFECTIVE_PARENT_ONE_CLOCK_TRANSFER_BOUNDARY`: `exact proposed_retained one-clock transfer law on the enlarged slice space`; `DM_ETA_NSITES_V_STRUCTURAL_SUPPORT_LIFT`: `bounded support — the candidate is recorded as a framework-composed structural product`; `DM_SPLIT2_INTERVAL_CERTIFIED_DOMINANCE_CLOSURE`: `support — structural or confirmatory support note`; `DM_Z3_TEXTURE_FACTOR`: `exact positive overlap theorem on the proposed_retained Z_3 basis bridge` |

The dominant declared character is **support / boundary / reduction /
no-go on the open DM gate** — exactly the same controlled-vocabulary
phrases already used by the woven `G. DM and cosmology tools` rows in
`DERIVATION_ATLAS.md`.

## Triage decision matrix

For each sub-family the recommendation is one of:

- `weave to DERIVATION_ATLAS.md` — clean structural support theorem on the
  retained / open-gate DM surface; the note's declared status matches the
  existing atlas wording for that section.
- `weave to LANE_STATUS_BOARD.md only` — the note belongs to a historical
  lane-board row rather than the publication atlas. (Not applicable here:
  there is no DM lane row on `LANE_STATUS_BOARD.md`, and adding one would
  be a separate governance decision out of scope for this triage.)
- `leave unwoven; route-history-only` — exploratory / superseded /
  selector-bank-internal note that is correctly preserved on `main` as
  route history but is not load-bearing for any retained authority surface.
- `governance decision required` — ambiguous at the sub-family level;
  flagged for the user.

| Sub-family | Recommendation | Reason |
|---|---|---|
| `DM_NEUTRINO_*` (exact triplet-CP, atmospheric-scale, K00 / VEVEN / CODD bosonic-normalization, ODD-circulant Z_2 slot, Z_3 character transfer, source-surface microscopic positive probe) | `weave to DERIVATION_ATLAS.md` for the **exact**-status notes (~9 of 18); `leave unwoven; route-history-only` for the redundant `support — structural or confirmatory support note` triplet/two-Higgs/swap-reduction sub-batch (~9 of 18) | The exact-status neutrino-side theorems (atmospheric scale, intrinsic CP triplet form, Z_3 character activation, K00/VEVEN bosonic normalization) are the same shape as already-woven atlas rows like `DM neutrino positive-polar Hermitian CP theorem`, `DM intrinsic slot theorem`, and `DM exact H-side preimage bundle`. The redundant within-bank support batch documents which directions the bank is blind to and reads as internal route history rather than retained structural support. |
| `DM_WILSON_*` direct-descendant family (16 notes) | `governance decision required` | This is the largest unwoven sub-family and is the most ambiguous. The notes are explicitly labeled as exact frontier / branch / reduction / multiplicity theorems on the `D_-` / `Schur_E_e` / direct-descendant gate, which is the same gate already woven into the atlas via `DM Wilson direct-descendant Schur-Feshbach boundary support theorem`. However the package functions as a **route history of the Wilson-parent audit and its descendants**: collapse, frontier, multiplicity, plateau, branch discriminants, projected-source discriminants, and the `Wilson_to_DWEH` adjacent-chain / structured-extension / structured-model batch. Weaving all 16 would inflate the atlas's DM section with closely related route-history rows; weaving none risks losing a real exact reduction stack. Recommend the user (a) keep the existing single Schur-Feshbach atlas row as the canonical Wilson-direct-descendant entrypoint, and (b) decide whether to add a single grouped row pointing to a Wilson-direct-descendant **batch authority note** (which does not yet exist) rather than weaving the 16 individual theorem notes. |
| `DM_PMNS_*` (no-go and current-activation theorems; chamber / seed / ordered-chain support) | `weave to DERIVATION_ATLAS.md` for the two no-go theorems and the graph-first ordered-chain current-activation theorem (3 of 7); `leave unwoven; route-history-only` for the four support-status chamber / seed / ordered-chain / upper-octant notes (4 of 7) | The two PMNS no-go theorems (`local-selector-family no-go`, `Z_3 doublet-block center-positive sheet no-go`) and the ordered-chain current-activation theorem are direct counterparts of already-woven atlas rows (`DM Z_3 doublet-block current-bank blindness theorem`, `PMNS stationary CP incompatibility theorem`, etc.). The four support-status notes are within-route corollaries of the existing `DM Z_3 doublet-block point-selection theorem` and read as route history. |
| `DM_LEPTOGENESIS_*` (transport decomposition / integral, projection, flavor-column functional, analytic stationary classification, relative-action stationarity) | `leave unwoven; route-history-only` | All six are declared `bounded` or carry no explicit `Status:` line and sit upstream of the already-woven `DM transport status` and `PMNS reduction-exhaustion` atlas rows. They document how the transport chain was decomposed and projected before the `eta/eta_obs = 0.1888` provenance was frozen on the atlas. The atlas already carries `DM transport status` as `historical / diagnostic; exact transport provenance inside the flagship closure package`; the upstream decomposition / integral / projection notes are the route history of that provenance. |
| `DM_SELECTOR_*` (relative-action recovered, threshold stabilization, shifted-doublet imag-sign, packet closure) | `leave unwoven; route-history-only` | All five carry `selector-side support theorem on the open DM gate` or plain `support`. They are within-bank refinements of the same selector chamber the existing atlas row `DM source-bank Z_3 doublet-block selection obstruction theorem` already closes off as a current-bank obstruction. Weaving them would duplicate that obstruction at finer granularity without changing the gate. |
| `DM_ABCC_*` (cubic closure, five-basin chamber DPLE, PMNS non-singularity, signature forcing) | `governance decision required` | The ABCC chamber is the live closing chamber for the bounded `G1 DM-neutrino PMNS-as-f(H) bounded package` row already woven into the atlas (which references `ABCC_CP_PHASE_NO_GO_THEOREM_NOTE_2026-04-19.md`). Two of the four ABCC notes here (`PMNS non-singularity`, `signature forcing`) are the IVT / threshold lemma backbones that the woven `G1 ...` row implicitly leans on. Recommend the user decide whether the existing single `G1` row is sufficient as an authority pointer for the ABCC chamber, or whether the four ABCC notes should be woven as named one-hop deps under the `G1` row. |
| `DM_SIGMA_HIER_*` (H-intrinsic no-go, upper-octant selector) | `weave to DERIVATION_ATLAS.md` (1 of 2); `leave unwoven; route-history-only` (1 of 2) | The `H-intrinsic no-go theorem` is a named-family no-go in the same style as already-woven `PMNS stationary CP incompatibility theorem` and is a clean weave candidate. The `upper-octant selector` note is declared `conditional/support theorem on the open DM PMNS gate` and points back to the authoritative `I12` closeout theorem; it is appropriately route-history-only. |
| `DM_DPLE_*`, `DM_EFFECTIVE_PARENT_*`, `DM_ETA_NSITES_V_*`, `DM_SPLIT2_*`, `DM_Z3_TEXTURE_FACTOR_*` (singletons) | `weave to DERIVATION_ATLAS.md` for `DM_Z3_TEXTURE_FACTOR` and `DM_EFFECTIVE_PARENT_ONE_CLOCK_TRANSFER_BOUNDARY`; `leave unwoven; route-history-only` for the other three | The two recommended weave candidates are exact theorems on the proposed_retained surface that match existing atlas slot/character/transport-boundary rows. The three left unwoven (DPLE matrix-analysis, ETA n_sites lift, split2 interval-certified dominance) are bounded support / matrix-analysis tools that did not feed the live ABCC / G1 closure path. |

## Headline triage outcome

| Decision | Approx. note count |
|---|---|
| `weave to DERIVATION_ATLAS.md` | ~14 (exact neutrino-side theorems, two PMNS no-gos + activation, sigma-hier no-go, two singletons) |
| `governance decision required` | ~20 (16 Wilson direct-descendants + 4 ABCC chamber backbones) |
| `leave unwoven; route-history-only` | ~29 (within-bank selector / leptogenesis-decomposition / redundant neutrino support / ordered-chain support / DPLE / ETA / split2) |

Most unwoven DM_* notes (~29 of 63, or ~46%) are appropriately classified
as historical / diagnostic route history. A smaller proven-clean fraction
(~14 of 63, or ~22%) is a candidate for a follow-on atlas weave PR. The
largest single sub-family (`DM_WILSON_*`, 16 notes) and the live-flagship
`DM_ABCC_*` chamber (4 notes) require a governance decision before any
weave PR runs, because they trade off atlas-row inflation against making
exact reductions visible.

## Recommended next-cycle actions

1. **Follow-on atlas weave PR** — Wave the ~14 clean structural notes
   (exact neutrino-side theorems + the two PMNS no-go theorems + the
   ordered-chain current-activation theorem + the sigma-hier H-intrinsic
   no-go + the two singleton candidates) onto
   `docs/publication/ci3_z3/DERIVATION_ATLAS.md` section
   `G. DM and cosmology tools`. These are the lowest-risk weave decisions
   and the language already matches the existing rows.
2. **Wilson-direct-descendant batch authority decision** — Before weaving
   the 16-note `DM_WILSON_DIRECT_DESCENDANT_*` family, decide whether to
   (a) treat the existing atlas row `DM Wilson direct-descendant
   Schur-Feshbach boundary support theorem` as the sole authority pointer
   and leave the 16 unwoven as route history, or (b) write a single
   batch-authority note (e.g.,
   `DM_WILSON_DIRECT_DESCENDANT_BATCH_NOTE_*.md`) and weave that one row.
   Option (b) avoids atlas-row inflation while preserving exact reductions
   on a canonical surface. Recommend (b) once the user confirms.
3. **ABCC chamber dependency decision** — Decide whether the four
   `DM_ABCC_*` notes should be woven as named one-hop deps under the
   already-woven `G1 DM-neutrino PMNS-as-f(H) bounded package` row, or
   whether the existing reference to `ABCC_CP_PHASE_NO_GO_THEOREM_NOTE` is
   sufficient. Either choice is honest; the user should pick one to avoid
   drift.
4. **Do not re-promote** — None of the unwoven DM_* notes warrants
   promotion of the DM lane out of `open flagship lane` status in
   `ASSUMPTION_DERIVATION_LEDGER.md`. The triage finding here is purely
   about index hygiene, not closure status.

## Cross-references

- [`docs/ASSUMPTION_DERIVATION_LEDGER.md`](../../ASSUMPTION_DERIVATION_LEDGER.md)
  ("DM flagship lane" row)
- [`docs/repo/CONTROLLED_VOCABULARY.md`](../../repo/CONTROLLED_VOCABULARY.md)
  (claim-strength labels and `historical / diagnostic` definition)
- [`docs/publication/ci3_z3/DERIVATION_ATLAS.md`](../../publication/ci3_z3/DERIVATION_ATLAS.md)
  (section `G. DM and cosmology tools`, ~50 already-woven DM rows)
- [`CANONICAL_WEAVE_AUDIT_2026-05-03.md`](CANONICAL_WEAVE_AUDIT_2026-05-03.md)
  (companion audit packet, PR `#448`)

## Constraints honored

- No edits to `CANONICAL_HARNESS_INDEX.md`, `DERIVATION_ATLAS.md`,
  `LANE_REGISTRY.yaml`, or `LANE_STATUS_BOARD.md` in this PR.
- Uses only existing controlled vocabulary (`historical / diagnostic`,
  `bounded`, `support`, `bounded support theorem`, `exact support theorem`,
  `exact reduction theorem`, `open flagship lane`, `route-history-only`).
- Concise per the triage scope; this packet is governance-only, not a
  load-bearing claim.
