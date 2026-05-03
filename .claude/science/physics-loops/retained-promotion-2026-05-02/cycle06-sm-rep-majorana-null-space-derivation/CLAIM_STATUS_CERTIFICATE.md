# Cycle 06 (Retained-Promotion) Claim Status Certificate — SM Representation Synthesis + Majorana Null-Space Derivation (closing derivation)

**Block:** physics-loop/sm-rep-majorana-null-space-derivation-2026-05-02
**Note:** docs/SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_sm_rep_majorana_null_space_derivation.py
**Target row:** `neutrino_majorana_operator_axiom_first_note` (claim_type=positive_theorem, audit_status=audited_conditional, td=185, lbs=B)

## Block type

**Closing derivation** (output type (a) per the new retained-promotion
campaign prompt). Integrated runner that **derives the verdict-identified
obstruction** by combining cycles 01+02+04 of this campaign into a
single derivation of the SM one-generation matter representation, then
solves the Majorana null space on the derived representation directly.

## Promotion Value Gate (V1–V5)

### V1: SPECIFIC verdict-identified obstruction this PR closes

Quoted from parent row's `verdict_rationale`:

> Issue: the classification depends on the anomaly-fixed one-generation
> spectrum, U(1)_Y charges, chirality surface, and right-handed sector
> being retained inputs, but those authorities are not present as
> one-hop ledger dependencies and some listed authority paths are not
> resolved by the audit bundle. Why this blocks: the runner hard-codes
> the representation and proves the invariant-bilinear result only
> conditional on that imported representation. Repair target: add
> retained one-hop dependencies or an integrated runner that derives
> the full representation from retained primitives before solving the
> Majorana null space.

**This PR's closing-derivation theorem provides the integrated runner
explicitly requested in the verdict's "or" clause.** It synthesizes:
- cycle 01 (SU(3)^3 cubic anomaly forces 3̄ for u_R^c, d_R^c),
- cycle 02 (SU(2) Witten Z_2 forces even doublet count),
- cycle 04 (U(1)_Y mixed anomalies force SM Y values, no-ν_R variant),

into a single derivation of the SM one-generation matter
representation, then solves the Majorana null space on the resulting
representation.

### V2: NEW derivation contained

The parent's runner (`frontier_neutrino_majorana_operator.py`) takes
the SM representation as a hand-coded input and proves the
invariant-bilinear result only conditional on that input.

This PR's derivation:

1. Re-derives Q_L's SU(3) triplet rep from graph-first SU(3) integration
   (retained, td=312).
2. Re-derives the no-ν_R variant of cycle 04: Y(u_R), Y(d_R), Y(e_R)
   uniquely fixed by anomaly cancellation alone, no neutrality input.
3. Synthesizes with cycle 01's forced 3̄ result and cycle 02's parity
   counting to derive the FULL one-generation rep (no-ν_R sector).
4. Solves the Majorana null space (SU(3) × SU(2) × U(1)_Y invariant
   same-chirality quadratic bilinears) on the DERIVED representation.
5. **No-ν_R sector**: Majorana null space is **empty** — no quadratic
   Majorana operator is admissible.
6. **With-ν_R sector** (admitting Y(ν_R) = 0 as additional input):
   Majorana null space is one-dimensional, spanned by `ν_R^T C P_R ν_R`,
   matching the parent's classification.
7. **Counterfactual**: changing any single Y value (e.g., y_3 = -2 → y_3 = -1)
   makes the previously-allowed Majorana operator gauge-non-invariant.
8. **Counterfactual**: changing rep (e.g., e_R from (1,1) to (1,3)) makes
   e_R Majorana bilinear gauge-non-invariant.

The integrated runner provides the missing derivation chain the
parent's runner lacked.

### V3: Audit lane couldn't already do this from existing retained primitives + standard math machinery

The audit lane in restricted one-hop context cannot synthesize:
- Cycle 01 (Diophantine on SU(3)^3),
- Cycle 02 (parity on Witten Z_2),
- Cycle 04 (cubic on U(1)_Y mixed),
- Plus Majorana null-space solve on the derived rep,

simultaneously in one hop. The integrated runner is the missing
derivation.

### V4: Marginal content non-trivial

Yes:
- Three-cycle synthesis: cycles 01+02+04 combined into a single
  representation derivation.
- **Majorana null-space solve** on the DERIVED rep (numerical, not
  hand-coded).
- **No-ν_R contrast**: Majorana null space is empty without ν_R —
  matches cycle 04's no-ν_R variant; the framework's Majorana
  classification is contingent on the framework's choice to include
  ν_R.
- **Two counterfactuals**: changing Y values or reps breaks the
  Majorana null-space dimension.
- Connection between cycles 01-04 and the neutrino Majorana question.

This is genuine derivation content the parent row didn't have.

### V5: Not a one-step variant of an already-landed cycle

Cycle 01: forces RH quark color rep (3̄) via Diophantine.
Cycle 02: forces LH doublet count (4) via parity.
Cycle 03: scalar generator from Cauchy.
Cycle 04: forces SM Y values via cubic on no-ν_R sector.
Cycle 05: staggered scalar parity coupling via Kogut-Susskind.

**Cycle 06**: synthesis of cycles 01+02+04 + Majorana null-space
solve on the derived representation. Different parent row
(neutrino_majorana_operator vs anomaly cancellation rows), different
specific result (Majorana null space dimension, not anomaly closure or
hypercharge values), different math (gauge-invariant bilinear
classification, not Diophantine / parity / functional equation /
cubic / staggered translation).

The Majorana null-space solve adds entirely new content beyond
cycles 01-05. Not a one-step variant.

## Outcome classification (per new prompt)

**(a) Closing derivation.** This PR provides a new theorem note +
runner that **derives the verdict-identified obstruction** (integrated
representation derivation before Majorana null-space solve) by
combining cycles 01+02+04 + adding the null-space solve on the
derived rep.

The outcome IS retained-positive movement on the parent row's
load-bearing class-B step (representation derivation), conditional on
audit-lane ratification of:
- cycles 01, 02, 04 (PRs #382, #383, #390) being audit-ratified
  individually OR the integrated runner accepted as a standalone
  derivation;
- the standard ABJ anomaly cancellation requirement;
- the framework's retained graph-first SU(3) integration and
  associated narrow-ratio theorem (td=265).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention beyond the
  doubled-Y convention.
- No same-surface family arguments.
- No load-bearing dependency on the demoted
  `HYPERCHARGE_IDENTIFICATION_NOTE` (cycle 04's decoupling carries
  through).

## Audit-graph effect

If independent audit ratifies this derivation:
- Parent row `neutrino_majorana_operator_axiom_first_note` load-bearing
  class-B step closes: representation is now derived (via the
  integrated runner), not hand-coded.
- The chain to td=185 transitive descendants benefits from a derived
  representation anchor.
- The Majorana null-space classification result becomes derived
  rather than conditional on hand-coded inputs.

## Honesty disclosures

- This PR does NOT derive `Y(ν_R) = 0` from framework primitives.
  The with-ν_R Majorana null-space result is contingent on admitting
  ν_R as a neutral singlet (consistent with cycle 04's analysis).
- This PR does NOT prove the Majorana coefficient is nonzero. The
  parent's companion no-go notes
  (`NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE`,
  `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE`) show the
  framework's current native surface gives zero coefficient.
- This PR does NOT close PMNS / leptogenesis / Δm² questions —
  those are downstream phenomenology notes.
- Audit-lane ratification required; no author-side tier asserted.
- Cycles 01, 02, 04 are PRs not yet ratified. Cycle 06's
  derivation can stand on the integrated-runner path (re-derives
  inline) or on the cycles' eventual ratification — the integrated
  runner is non-conditional on the cycles' audit status.
