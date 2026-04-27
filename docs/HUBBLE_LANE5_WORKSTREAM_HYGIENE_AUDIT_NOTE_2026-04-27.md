# Lane 5 Workstream Hygiene Audit

**Date:** 2026-04-27
**Status:** retained branch-local hygiene-audit note on
`frontier/hubble-h0-20260426`. Cross-cycle audit checking Cycles 1-6
for unmodeled premises, broken cross-references, and inadvertent
overclaim before the post-workstream review-and-integration pipeline.
**Lane:** 5 — Hubble constant `H_0` derivation
**Workstream:** `hubble-h0-20260426`

---

## 0. Scope

This audit reviews the six branch-local Lane 5 cycle artifacts:

1. `docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`
2. `docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`
3. `docs/HUBBLE_LANE5_COSMIC_HISTORY_RATIO_NECESSITY_NO_GO_NOTE_2026-04-26.md`
4. `docs/HUBBLE_LANE5_ETA_RETIREMENT_GATE_AUDIT_NOTE_2026-04-26.md`
5. `docs/HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md`
6. `docs/HUBBLE_LANE5_WORKSTREAM_STATUS_NOTE_2026-04-27.md`

Plus the two paired runners and logs:

- `scripts/frontier_hubble_tension_structural_lock.py` +
  `logs/2026-04-26-hubble-tension-structural-lock.txt`
- `scripts/frontier_cosmology_open_number_reduction.py` +
  `logs/2026-04-26-cosmology-open-number-reduction.txt`

The audit checks for:

- **(A1)** broken cross-references (cited file does not exist at the
  given path);
- **(A2)** unmodeled premises (a derivation step that depends on a
  retained item not listed in the cycle's premise inventory);
- **(A3)** inadvertent overclaim (status language stronger than the
  proof or evidence supports);
- **(A4)** import-ledger drift (a cycle quietly retires or imports a
  value not on the workstream's `ASSUMPTIONS_AND_IMPORTS.md` ledger);
- **(A5)** consolidation-table accuracy (Cycle 6's symmetry map must
  match Cycle 4's and Cycle 5's actual gate descriptions);
- **(A6)** runner-log fidelity (commit-tracked log matches latest
  runner output, all checks PASS).

## 1. Findings

### Finding 1 — broken `INPUTS_AND_QUALIFIERS_NOTE.md` references in Cycle 3 (FIXED)

**Category:** A1 (broken cross-reference).

Cycle 3
(`HUBBLE_LANE5_COSMIC_HISTORY_RATIO_NECESSITY_NO_GO_NOTE_2026-04-26.md`)
cited `INPUTS_AND_QUALIFIERS_NOTE.md` as a bare filename on lines
79 (§1 retained-input table), 85 (§2 proof, quoting from §3 of that
note), and 225 (§8 cross-references). The actual file lives at
`docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md`.

Cycles 1 and 6 reference the same file using the correct full path.

**Fix applied:** all three references updated to use the full path
`docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md`. No semantic
content changed; only the path string corrected.

### All other audit categories — clean

**A1 (broken cross-references, other):** A comprehensive grep over all
six artifacts for `*.md` references confirms every other cited path
resolves. Cycles 1, 2, 4, 5, 6 cross-references are clean.

**A2 (unmodeled premises):**

- Cycle 1: §1 explicitly lists premises `(P1) w_Lambda = -1` and
  `(P2) flat FRW` (after the 3 → 2 tightening edit recorded in
  REVIEW_HISTORY). The proof of (★) in §2 uses only these. The
  framework grounding (`Cl(3)/Z^3`, spectral-gap identity, matter-
  bridge identity) appears in §0 as context, not as load-bearing
  premise. Clean.
- Cycle 2: §1 lists 10 retained items used. The proof in §2 invokes
  only the matter-bridge identity, scale identification, FRW reduction,
  inverse reconstruction certificate, and the structural lock (Cycle 1).
  Each is on the §1 list. Clean.
- Cycle 3: §1 lists 7 retained items + the Planck-lane status. The
  case-analysis in §2 uses only `MINIMAL_AXIOMS_2026-04-11.md` plus the
  cited Planck-lane absolute-scale status. The case-analysis in §3
  uses the open-number-reduction theorem from Cycle 2 + the bounded
  cascade from `OMEGA_LAMBDA_DERIVATION_NOTE.md`. All on §1's list.
  Clean.
- Cycle 4: cites `DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`
  as primary authority for the live-routes inventory and the gate
  identification. The closed-route inventory in §4 cites 8 specific
  no-go notes; all exist on `main`. Clean.
- Cycle 5: cites `PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md` as
  primary authority. The closed-shortcut inventory cites 6 specific
  no-go notes; all exist on `main`. Clean.
- Cycle 6: synthesizes Cycles 1-5; no new derivation steps. Clean.

**A3 (inadvertent overclaim):**

- All six artifacts use the scoping phrase "retained ... on
  `main`-compatible surface, landed branch-locally" or the audit
  variant "retained branch-local audit note" (Cycles 4, 5, 6). This
  scoping is consistent with the skill's science-only delivery policy.
- No artifact uses unqualified Nature-grade or `main`-promotion
  language for a workstream-internal claim.
- Cycle 1's tension-stance claim (§4.2) is carefully bounded:
  late-time-only resolutions are forbidden; pre-recombination physics
  and measurement systematics are explicitly preserved as escape
  routes.
- Cycle 3's no-go is operationally falsifiable (§6: "exhibit a
  counterexample, and the no-go falls").
- Cycle 6's headline §0 attributes claim-state to each cycle's
  authority note rather than to the consolidation note itself.
  Clean.

**A4 (import-ledger drift):**

- The workstream's `ASSUMPTIONS_AND_IMPORTS.md` lists the inputs:
  `H_0`, `T_CMB`, `eta`, `alpha_GUT`, `R_Lambda`, plus comparators
  (Planck 2018, SH0ES 2022).
- No cycle introduces an additional input or silently retires one.
- Cycle 1's runner uses Planck 2018 as a numerical comparator (after
  the flatness fix); explicitly flagged in `LITERATURE_BRIDGES.md` as
  comparator-only.
- Cycle 2's runner uses Planck 2018 as a numerical comparator; same
  flagging.
- Cycles 3, 4, 5, 6 introduce no numerical inputs.
- Clean.

**A5 (consolidation-table accuracy):**

- Cycle 6 §3's symmetric two-gate map describes the `(C2)` gate as
  "right-sensitive 2-real `Z_3` doublet-block point-selection law on
  `dW_e^H = Schur_{E_e}(D_-)`". Cycle 4 §2 names the same: "the
  right-sensitive microscopic selector law on
  `dW_e^H = Schur_{E_e}(D_-)`, equivalently the intrinsic 2-real `Z_3`
  doublet-block point-selection law". Match.
- Cycle 6 §3 describes `(C1)` gate as "metric-compatible primitive
  Clifford/CAR coframe response on `P_A H_cell`". Cycle 5 §2 names
  the same: "the metric-compatible primitive Clifford/CAR coframe
  response on the rank-four primitive boundary block
  `P_A H_cell ⊆ H_cell`". Match.
- Cycle 6 §4 (per-cycle imports table) accurately reports that no
  numerical input was retired by any cycle.
- Clean.

**A6 (runner-log fidelity):**

- `logs/2026-04-26-hubble-tension-structural-lock.txt`: latest commit
  shows `summary: PASS=5 FAIL=0`. Re-running the runner is
  reproducible (sympy + numpy deterministic).
- `logs/2026-04-26-cosmology-open-number-reduction.txt`: latest commit
  shows `summary: PASS=5 FAIL=0`. Same.
- Clean.

## 2. Disposition

After Finding 1's fix, the workstream artifacts pass the hygiene
audit. The branch-local cycle artifacts are coherent, cross-references
resolve, premise inventories cover the actual derivation steps, status
language is appropriately scoped, and no input has silently drifted on
or off the workstream ledger.

The post-workstream review-and-integration pipeline can use the
consolidated status note
(`HUBBLE_LANE5_WORKSTREAM_STATUS_NOTE_2026-04-27.md`) as the read-first
surface and rely on the per-cycle artifacts for technical detail.

## 3. Cross-references

- All six cycle artifacts (listed in §0).
- `.claude/science/frontier-workstreams/hubble-h0-20260426/` — pack
  scaffold (STATE.yaml, ASSUMPTIONS_AND_IMPORTS.md, NO_GO_LEDGER.md,
  ROUTE_PORTFOLIO.md, ARTIFACT_PLAN.md, LITERATURE_BRIDGES.md,
  REVIEW_HISTORY.md, HANDOFF.md).

## 4. Boundary

This is a hygiene/audit note, not a theorem and not a runner-bearing
cycle. Its only structural action is the cross-reference fix in
Cycle 3. It does not retire any input, does not introduce a new claim,
and does not change the closure-pathway taxonomy or the gate
identifications.

A runner is not authored: hygiene auditing is editorial / structural
review, not numerical derivation.
