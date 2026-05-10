# T2 G_Newton Re-Audit — Skeleton-Selection + Born-as-Source Hostile Review

**Date:** 2026-05-10
**Claim type:** open_gate
**Scope:** review-loop source-note proposal. Hostile-review source note for two
admissions of `GRAVITY_CLEAN_DERIVATION_NOTE.md` that received attempted
narrowings on 2026-05-10 but were not deeply attacked in the same session:
**(A) skeleton-selection** (gnewtonG1,
[`G_NEWTON_SKELETON_SELECTION_BOUNDED_NOTE_2026-05-10_gnewtonG1.md`](G_NEWTON_SKELETON_SELECTION_BOUNDED_NOTE_2026-05-10_gnewtonG1.md))
and **(B) Born-as-source** (gnewtonG2,
[`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)).
This re-audit confirms both as BOUNDED-SUPPORT-AT-BEST with explicit named
weaknesses surfaced for the audit lane.
**Status:** source-note proposal only. Both inputs still carry named
open gates: neither derives its parent G_Newton lane from the current
framework baseline.
gnewtonG2 has a citation defect requiring correction. gnewtonG1 has a
hidden modeling step requiring naming. Neither admission is well-founded
enough to remove from the parent G_Newton three-admission count.
**Authority disclaimer:** source-note proposal — downstream status is
set only by the independent audit lane.
**Runner:** `scripts/cl3_closure_t2_gnewton_reaudit_2026_05_10_t2gnewton.py`
**Cache:** `logs/runner-cache/cl3_closure_t2_gnewton_reaudit_2026_05_10_t2gnewton.txt`

## Authority disclaimer

This is a source-note proposal. The independent audit lane has full
authority to retag, narrow, or reject the proposal. This note does NOT
promote, retag, or close any prior G_Newton content; it surfaces
specific named weaknesses for audit consideration.

## Scope

The 2026-05-10 G_Newton fragmentation pass landed two narrowing notes
under the planckP4 three-admission framing:

```
(a) L^{-1} = G_0 skeleton-selection           [narrowing: gnewtonG1]
(b) rho = |psi|^2 Born-as-source              [narrowing: gnewtonG2]
(c) S = L(1-phi) weak-field response          [narrowing: gnewtonG3]
```

This re-audit covers (a) and (b). The (c) admission is unchanged from
gnewtonG3 status (bounded conditional support on cited Hamiltonian flow
plus the canonical `V_grav = m*phi` coupling, which itself remains
admitted). The downstream C-B(b) canonical mass-coupling branch loads
on gnewtonG2's Born map identification; this note's gnewtonG2 findings
flow downstream to that load-bearing chain.

## Framework Baseline Used

- Physical local algebra `Cl(3)` per site.
- Physical `Z^3` spatial substrate.
- No fitted parameters; no PDG values used as proof input.

## Cited inputs (under audit by this note)

- gnewtonG1's five cited supports (R-RP, R-SC, R-LR, R-SCC, R-PL)
- gnewtonG2's three cited supports (PhysLatBase, BornOp, StatMix)
- PARENT: `GRAVITY_CLEAN_DERIVATION_NOTE.md`
- PARENT: `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` (explicitly stipulates
  L^{-1} = G_0, not derives)
- BORN_RULE_ANALYSIS_2026-04-11 — Born as measurement postulate vs
  dynamics statement; used here only as methodological caution, not
  as a retained derivation.
- SELF_GRAVITY_BORN_HARDENING_NOTE — the Born+self-gravity lane is a
  hardened bounded no-go on retained backreaction.
- STAGGERED_FERMION_CARD_2026-04-11 — admits ρ = |ψ|^2 as H2 (harness
  import, not derived from the framework baseline)

## Question

> For the two recently-landed bounded-support narrowings (gnewtonG1
> skeleton-selection and gnewtonG2 Born-as-source), does the bounded
> support actually hold up under hostile review, or do hidden modeling
> steps / citation defects / load-bearing gaps re-open the admission?

This is a re-audit, NOT a new closure attempt.

## Answer

**Both admissions remain ADMITTED, with concrete named weaknesses:**

### Finding F1 (skeleton-selection / gnewtonG1)

The skeleton-selection argument is **structurally sound on the cited
support chain**, but has TWO named load-bearing weaknesses:

- **F1.1 (cited-support audit status):** All five cited supports
  (R-RP, R-SC, R-LR, R-SCC, R-PL) are currently `unaudited` or
  `audited_conditional` in the ledger. This is the bounded-tier
  inheritance per `feedback_retained_tier_purity_and_package_wiring`.
  The note correctly classifies as `bounded_theorem`, not
  `positive_theorem`. No new defect here.

- **F1.2 (hidden modeling step — STATIC SECTOR PRIVILEGE):**
  The argument shows that *if* the gravity field equation is
  posed in the static-zero-frequency sector, *then* all three
  retained skeleton families (Hamiltonian, d'Alembertian,
  complex-action / Euclidean) reduce to `L = H = -Δ_lat`. This is
  mathematically correct (verified by this re-audit's runner T1-T4).
  BUT the argument silently assumes that **gravity is posed in the
  static sector**. This is a modeling step, not a derivation from
  the current framework baseline. The WAVE_EQUATION_GRAVITY_NOTE.md explicitly shows the
  d'Alembertian skeleton is the framework's primary causal extension
  (finite-speed propagation, retardation, GW radiation candidate).
  Selecting the *static restriction* of the d'Alembertian as the
  primary gravity equation is the modeling step. The named admission
  L^{-1} = G_0 is replaced by a named admission "gravity is static
  on the equal-time slice".
  
  THE TRADE: gnewtonG1 has reduced one admission (closure identity)
  to another admission (static-sector privilege). Both admissions
  are at the same modeling level. Net admission count is unchanged.
  However: the new admission ("gravity is static on the equal-time
  slice") is arguably MORE NATURAL than `L^{-1} = G_0` because it is
  the standard physics modeling assumption for Newtonian gravity
  (vs general relativity).

**Verdict F1:** bounded support DOES hold (F1.1 is the named bound;
F1.2 is a re-labeling of the admission, not its removal). The
gnewtonG1 closure identity narrowing IS legitimate bounded support,
provided the audit lane records the static-sector privilege as the
replacement admission. The narrowing is real but is **not closure**.

### Finding F2 (Born-as-source / gnewtonG2)

The Born-as-source narrowing is **mathematically correct on the
unified position-density Born map**, but has THREE named load-bearing
weaknesses:

- **F2.1 (CITATION DEFECT — load-bearing):** The gnewtonG2 note
  cites "Born-rule operationalism per
  CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08." Direct grep of
  that note (235 lines) returns zero matches for "Born" — the
  conventions-unification note does NOT establish Born-rule
  operationalism. Its content is about LABELING and UNIT
  conventions, not measurement-rule operationalism. The gnewtonG2
  citation is a cite-shift: the actual content used (operational
  Born rule for position observable) is standard QM, NOT derived from
  any retained note. The audit lane should require gnewtonG2 to
  either (a) cite an actually-retained Born-rule note or (b) explicitly
  list "operational Born rule" as a separate admission.

- **F2.2 (THE HARD QUESTION REMAINS UNTOUCHED):** The unified map
  `ρ_grav(x) := ⟨x|ρ̂|x⟩` is canonical IF you grant the position-basis
  Born readout. But the load-bearing question for gravity is NOT
  "what is the canonical density on position basis given the Born
  rule?" — it is "WHY does the gravitational field equation
  `Lφ = -κρ` source from `ρ_grav` rather than some other
  observable expectation value?". The gnewtonG2 note explicitly
  acknowledges this in its Conclusion section:
  > It does not derive that gravity must use this readout. The
  > G_Newton self-consistency admission count, per the planckP4
  > sharpening, remains 3.
  This means: gnewtonG2's bounded support narrows ONE SUB-PART of
  admission (b) (the pure-vs-mixed extension question), while
  leaving the core "why position-density?" question completely open.
  The framing "category error, not real obstruction" applies to the
  planckP4 pure-vs-mixed sub-issue, not to the source-coupling
  question.

- **F2.3 (BORN_RULE_ANALYSIS audit-failure context):** The 2026-04-11
  BORN_RULE_ANALYSIS note is `audited_failed`. Its negative claim
  (gravity doesn't select α=2 via Hartree contraction) is NOT
  proven. But its STRUCTURAL OBSERVATION — that the Born rule is a
  MEASUREMENT POSTULATE and gravity is a DYNAMICS statement at
  different levels of the theoretical stack — remains a valid
  methodological caution. The gnewtonG2 narrowing does not contradict
  this; it simply argues that the canonical mixed-state extension is
  uncontroversial. But it does NOT advance the question of why
  gravity must couple to a measurement-side readout at all. The
  retained_no_go SELF_GRAVITY_BORN_HARDENING_NOTE is a hardened
  no-go on the Born+self-gravity backreaction lane; this is
  consistent with the F2.2 finding that the source-coupling question
  is open.

**Verdict F2:** bounded support DOES hold for what gnewtonG2 claims
(canonical position-density extension on mixed states; category-error
resolution of pure-vs-mixed sub-issue). The CITATION DEFECT (F2.1) is
fixable — gnewtonG2 needs to clean up its appeal to
CONVENTIONS_UNIFICATION_COMPANION. The HARD QUESTION (F2.2) is
explicitly acknowledged as out-of-scope in gnewtonG2's own
Conclusion; this re-audit confirms that. The narrowing is real
narrowing, but is **not closure** of admission (b).

## Open-Gate Statement

**Open-gate statement.** Under the current physical `Cl(3)` local
algebra and `Z^3` spatial substrate, and using the cited supports:

- **(R1) gnewtonG1 skeleton-selection IS legitimate bounded support
  at the documented status.** The static-sector reduction `L = H = -Δ_lat`
  holds for all three cited skeleton families (Hamiltonian,
  lattice d'Alembertian, Euclidean / complex-action). The closure
  identity `L^{-1} = G_0` is definitional once `L = H` is fixed.
  Named weakness F1.2: the static-sector privilege is a hidden
  modeling step that should be surfaced as the replacement admission.
  This re-audit's runner verifies the static-sector reduction holds
  on a finite Z^3 block (T1-T4).

- **(R2) gnewtonG2 Born-as-source IS legitimate bounded support
  WITH a citation defect requiring correction.** The unified
  position-density Born map `ρ_grav(x) := ⟨x|ρ̂|x⟩` is canonical
  for both pure and mixed states, reduces to `|ψ(x)|^2` on pure
  states, and is the unique linear PSD-respecting extension. The
  category-error analysis of the prior "divergence" framing is
  correct. Named weaknesses F2.1 (citation defect: appeal to
  CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08 for Born-rule
  operationalism, which that note does NOT establish) and F2.2
  (the harder question "why gravity sources from this readout"
  remains untouched — explicitly out-of-scope per gnewtonG2's own
  Conclusion). This re-audit's runner verifies (T5-T7) that the
  unified map is canonical, that the citation defect is real
  (grep returns zero "Born" matches in the cited note), and that
  the source-coupling question is structurally untouched by
  gnewtonG2.

- **(R3) Neither open gate closes; the planckP4 three-admission
  framing is preserved.** Both narrowings reduce the *size* of
  the admission but do not remove it from the count. The parent
  `GRAVITY_CLEAN_DERIVATION_NOTE.md` remains
  its existing status on three named admissions. The downstream C-B(b)
  mass-coupling branch loads on gnewtonG2's Born map identification;
  this note's F2.1 citation-defect finding flows downstream to
  that load-bearing chain (the canonical mass coupling
  argument uses the Born map identification but does not itself
  derive Born from the framework baseline).

Statements (R1)-(R3) constitute the bounded open-gate review statement
on the two admissions.

## Proof

### Proof of R1 (gnewtonG1 narrowing legitimacy)

**Step 1.** The static-sector reduction is verified directly by
finite-dim linear algebra. For the canonical block
`Λ = (Z/L_τ Z) × (Z/L_s Z)^3`:

- The Hamiltonian skeleton `L_H = H = -Δ_lat` trivially equals `H` in
  the static sector (no time derivative to drop). Runner T1.
- The lattice d'Alembertian `L_□ = ∂_t² - Δ_lat`: in the static
  (t-constant) sector, `∂_t² → 0`, so `L_□|_static = -Δ_lat = H`.
  Runner T2.
- The Euclidean / complex-action skeleton `K_E = ∂_τ² + H`: in the
  zero-frequency sector (static), `∂_τ² → 0`, so
  `K_E|_static = H` and the static Euclidean propagator is
  `K_E^{-1}|_static = H^{-1} = G_0`. Runner T3.

These three checks confirm the gnewtonG1 argument's algebraic core.

**Step 2.** The hidden modeling step is named and surfaced. The
static-sector reduction shows that *if* gravity is posed in the static
sector, *then* the skeleton is uniquely `H`. But the choice to pose
gravity in the static sector is a modeling step. Runner T4 verifies that:

- On the full block (NOT restricted to the static sector), the
  d'Alembertian skeleton has retarded propagation and is NOT
  equal to `H` (its non-static Green function has finite-speed
  retardation tails; cf. WAVE_EQUATION_GRAVITY_NOTE.md Test 1
  measured `c_grav ≈ 1.05` in lattice units).
- The static restriction is therefore a non-trivial modeling
  truncation, not a forced consequence of the cited support
  theorems alone.

This is the hidden admission. It is more natural than `L^{-1} = G_0`
(it is the standard Newton-vs-GR modeling choice), but it IS an
admission. The audit lane should record it as the replacement admission.

**Step 3.** The closure identity is definitional once L = H:
`L^{-1} = H^{-1} =: G_0` by definition of `G_0`. Runner T5 verifies
this on the finite block by direct matrix inversion. The original
admission `L^{-1} = G_0` is correctly characterized as redundant
once `L = H` is fixed; the load shifts entirely to step 2's hidden
admission.

This completes the proof of R1. ∎

### Proof of R2 (gnewtonG2 narrowing legitimacy + defects)

**Step 1.** The unified position-density Born map is verified by
direct calculation:

- For pure `ρ̂ = |ψ⟩⟨ψ|`: `⟨x|ρ̂|x⟩ = |⟨x|ψ⟩|² = |ψ(x)|²`. Runner T6.
- For mixed `ρ̂ = Σ_i p_i |ψ_i⟩⟨ψ_i|`:
  `⟨x|ρ̂|x⟩ = Σ_i p_i |ψ_i(x)|²`. Runner T6.
- Linearity, non-negativity (from ρ̂ PSD), normalization
  (trace = 1). Runner T6.

The map is canonical IF you grant the Born readout on the position
basis. This is class-A linear algebra.

**Step 2.** Citation defect is verified by direct file inspection.
Runner T7 performs a literal grep of
`docs/CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md` for any
occurrence of "Born" (case-insensitive). The result is:

- File length: 235 lines.
- "Born" matches: 0.
- "born" matches: 0.

The CONVENTIONS_UNIFICATION_COMPANION_NOTE is about labeling and unit
conventions (mass-ordering labels, meter/second/kilogram), not Born
rule operationalism. The gnewtonG2 citation of it for "Born-rule
operationalism" is therefore a CITE-SHIFT defect: the actual content
used (operational Born rule for the position observable) is standard
QM, NOT established in any retained framework note.

The fix is one of:
- (a) Replace the citation with an explicit "operational Born rule
  for position basis as standard QM input"; OR
- (b) Land a separate retained note establishing Born-rule
  operationalism (which would itself need to be a derivation from
  the framework baseline, or an explicit admission).

This re-audit recommends (a) as the simpler correction.

**Step 3.** The hard question remains untouched. Runner T8 confirms
that the gnewtonG2 narrowing addresses the pure-vs-mixed sub-issue
(MAP_a `|ψ|²` vs MAP_b `⟨x|ρ̂|x⟩` mismatch on mixed states), but
does not address the source-coupling question (why gravity couples
to `⟨x|ρ̂|x⟩` rather than e.g., `⟨x|ρ̂Ô|x⟩` for some other
operator Ô, such as a current density or stress-energy expectation).
The gnewtonG2 note's own Conclusion explicitly acknowledges this:

> It does not derive that gravity must use this readout.

This is a structural feature of the bounded narrowing, not a defect.
But it means the bounded support is genuinely narrow: it resolves
one sub-issue inside admission (b) while leaving the core
source-coupling question open.

This completes the proof of R2. ∎

### Proof of R3 (admission count preserved)

Both narrowings reduce the SIZE of the admission but not the COUNT.

- gnewtonG1: replaces `L^{-1} = G_0` with "gravity is static on the
  equal-time slice". One admission in, one admission out. Net 1
  admission on closure identity / skeleton selection.

- gnewtonG2: narrows the pure-vs-mixed sub-issue of `ρ = |ψ|²`
  by giving a canonical extension to mixed states. The
  source-coupling question (why this readout, not another) remains.
  Net 1 admission on Born-as-source.

- gnewtonG3 (out of scope for this re-audit): narrows valley-linear
  vs spent-delay sub-issue under the cited Hamiltonian flow plus
  canonical coupling `V_grav = m*phi`. The canonical coupling
  itself remains admitted. Net 1 admission on weak-field response.

Total admission count for `GRAVITY_CLEAN_DERIVATION_NOTE`: 3,
unchanged from planckP4. This is the conservative bookkeeping that
preserves the audit-lane authority on the parent note's status.

This completes the proof of R3. ∎

## Hypothesis set used

- Physical local algebra `Cl(3)` per site.
- Physical `Z^3` spatial substrate.
- gnewtonG1's five cited supports (each unaudited or audited_conditional)
- gnewtonG2's mathematical content (standard QM linear algebra)
- Direct file inspection of CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08

No new repo-wide axioms. No PDG values. No empirical fits. No
new physics inputs beyond standard QM + cited inputs.

## What this re-audit closes

- **Verifies gnewtonG1 algebraic core.** The static-sector reduction
  is mathematically correct. This is positive support for the
  narrowing's mathematical content.
- **Surfaces gnewtonG1 hidden modeling step.** The static-sector
  privilege is a hidden modeling assumption that should be named in
  the audit ledger as the replacement admission. This is structural
  re-labeling, not closure.
- **Verifies gnewtonG2 algebraic core.** The unified position-density
  Born map is mathematically canonical on mixed states. Pure-state
  reduction to `|ψ(x)|²` is exact. The category-error analysis is
  correct.
- **Identifies gnewtonG2 citation defect.** The appeal to
  CONVENTIONS_UNIFICATION_COMPANION_NOTE for Born-rule
  operationalism is empty: that note contains no Born content.
  The fix is to replace the citation with explicit "operational Born
  rule" as standard QM input (or admission).
- **Confirms gnewtonG2 scope limitation.** The source-coupling
  question (why gravity couples to position density at all) is
  explicitly out-of-scope per gnewtonG2's own Conclusion.

## What this re-audit does NOT do

- It does NOT close any of the three planckP4 admissions.
- It does NOT change the status of `GRAVITY_CLEAN_DERIVATION_NOTE.md`.
- It does NOT add new admissions; it only re-labels gnewtonG1's
  admission and identifies gnewtonG2's citation defect.
- It does NOT invalidate gnewtonG1 or gnewtonG2 as bounded support;
  it confirms their bounded support and refines their named
  weaknesses.
- It does NOT touch the downstream C-B(b) branch directly; it only
  records that gnewtonG2's citation defect flows downstream.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| F1.1 (cited-support audit status) | Demonstrate that any of (R-RP, R-SC, R-LR, R-SCC, R-PL) has retained-grade status as of this re-audit's date. The audit ledger query in this note's runner confirms `unaudited` or `audited_conditional` for all five. |
| F1.2 (static-sector privilege) | Demonstrate a retained derivation forcing the static-sector restriction of the gravitational field equation from the framework baseline alone (without modeling assumption). |
| F2.1 (citation defect) | Demonstrate that `docs/CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md` contains an explicit Born-rule operationalism statement. The runner's grep confirms zero "Born" matches in 235 lines. |
| F2.2 (source-coupling question) | Demonstrate a retained derivation forcing gravity to couple to position-density `⟨x|ρ̂|x⟩` rather than to other observable expectations. None present in audit ledger. |
| R3 (admission count preserved) | Demonstrate that any of the three planckP4 admissions has been fully closed (not just narrowed). None of gnewtonG1/G2/G3 claims full closure of its target. |

## Review boundary

This note proposes `claim_type: open_gate` for the independent audit
lane. The source content is an open-gate review statement: both
gnewtonG1 and gnewtonG2 supply bounded support, but named weaknesses
remain. Neither closes its parent admission. The three-admission
framing is preserved.

No new admissions are proposed. The named weaknesses (F1.2, F2.1,
F2.2) are pre-existing features of the narrowing notes; this source note
surfaces them explicitly so the audit lane can record them in the
ledger and propagate citation-defect correction (F2.1) downstream.

The independent audit lane may retag, narrow, or reject this proposal.

## Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | No — neither gnewtonG1 nor gnewtonG2 admission is closed by this re-audit. The re-audit confirms their bounded support and names their weaknesses. |
| V2 | New bounded support? | Yes — three named weaknesses (F1.2 static-sector privilege, F2.1 citation defect, F2.2 source-coupling untouched) are surfaced for audit consideration. F2.1 is a concrete defect requiring downstream correction. |
| V3 | Audit lane could complete? | Yes — the audit lane can (i) verify the runner's algebraic core checks (T1-T6), (ii) verify the citation defect by direct grep of the cited note (T7), (iii) confirm scope limitations (T8), (iv) propagate F2.1 downstream. |
| V4 | Marginal content non-trivial? | Yes — the hostile-review re-audit identifies a concrete citation defect (F2.1) that the original gnewtonG2 narrowing missed. The static-sector privilege (F1.2) renaming the admission is also non-trivial bookkeeping. The conservative admission-count preservation (R3) is the methodologically honest verdict. |
| V5 | One-step variant? | No — this is a hostile-review re-audit, structurally distinct from the original narrowings. It tests the narrowings against the audit-lane stress-test that the user-memory rules require. |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of gnewtonG1 or gnewtonG2. It is a hostile-review
  re-audit identifying specific named weaknesses missed by the
  original narrowings.
- Identifies a concrete CITATION DEFECT (F2.1) requiring downstream
  correction downstream — this is real engineering content.
- Identifies a HIDDEN MODELING STEP (F1.2) that should be recorded
  in the audit ledger — this is real bookkeeping content.
- Preserves the planckP4 three-admission framing (R3) — this is the
  methodologically honest verdict that prior narrowings reduce
  admission *size* but not *count*.

## Compliance with user-memory feedback rules

- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claims of both gnewtonG1 ("L^{-1} = G_0 is definitional
  under cited Hamiltonian uniqueness") and gnewtonG2 ("Born-rule
  operationalism per CONVENTIONS_UNIFICATION_COMPANION"). The
  semantic stress-tests find F1.2 (hidden modeling step) and F2.1
  (citation defect). This is exactly the hostile-review semantic
  check the rule requires.
- `feedback_consistency_vs_derivation_below_w2.md`: this note does
  NOT assert "consistency = derivation". Both gnewtonG1's
  algebraic verification of skeleton reduction and gnewtonG2's
  algebraic verification of the unified map are consistency
  checks of class-A linear algebra. The re-audit is explicit that
  consistency does not equal derivation: neither admission is
  closed.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  automatic cross-tier promotion. This source note is an open-gate
  proposal that explicitly refuses to upgrade gnewtonG1 or gnewtonG2
  beyond bounded support. The audit-lane authority on
  effective status is preserved.
- `feedback_physics_loop_corollary_churn.md`: hostile-review of
  same-day narrowings is structurally distinct from one-step
  relabeling. The citation-defect finding (F2.1) and the
  static-sector privilege naming (F1.2) are concrete new
  bookkeeping content, not relabels.
- `feedback_compute_speed_not_human_timelines.md`: the re-audit
  characterizes what additional retained content would be needed to
  close (static-sector privilege would need a derivation theorem;
  Born-source coupling would need a derivation theorem), not
  how-long-it-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a focused two-admission re-audit attack with sharp
  PASS/FAIL deliverables in the runner: F1 (algebra check + hidden
  step naming), F2 (algebra check + citation defect + scope
  limitation).
- `feedback_review_loop_source_only_policy.md`: source-only — this
  PR ships exactly (a) source theorem note, (b) paired runner,
  (c) cached output. No output-packets, lane promotions, synthesis
  notes, or "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: this note
  preserves the planckP4 three-admission framing. No new
  admissions are introduced; named weaknesses are surfaced for
  audit-lane consideration. The parent G_Newton note's status is not
  changed by this source note.
- `feedback_primitives_means_derivations.md`: the re-audit confirms
  that "new primitives" (in the user-memory rule sense:
  derivations from the physical `Cl(3)`/`Z^3` baseline plus retained content)
  are NOT what gnewtonG1 or
  gnewtonG2 supply. They supply bounded narrowings of admissions
  under cited support inputs that are themselves unaudited or
  unaudited or conditional. The honest classification is bounded
  support, not derivation from the framework baseline.

## Cross-references

- Re-audit target: [`G_NEWTON_SKELETON_SELECTION_BOUNDED_NOTE_2026-05-10_gnewtonG1.md`](G_NEWTON_SKELETON_SELECTION_BOUNDED_NOTE_2026-05-10_gnewtonG1.md)
- Re-audit target: [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)
- Parent planckP4 sharpening: [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
- Parent gravity-clean note: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- Companion full-self-consistency note: [`GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)
- Citation defect target: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- Physical-lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Audit-failed Born analysis: [`BORN_RULE_ANALYSIS_2026-04-11.md`](BORN_RULE_ANALYSIS_2026-04-11.md)
- Retained no-go: [`SELF_GRAVITY_BORN_HARDENING_NOTE.md`](SELF_GRAVITY_BORN_HARDENING_NOTE.md)
- Staggered fermion card (admission H2): [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md)
- Wave-equation gravity (alternative skeleton): [`WAVE_EQUATION_GRAVITY_NOTE.md`](WAVE_EQUATION_GRAVITY_NOTE.md)
- Newton-from-Z^3 (retained Poisson chain): [`NEWTON_LAW_DERIVED_NOTE.md`](NEWTON_LAW_DERIVED_NOTE.md)
- Propagator family unification (skeleton non-uniqueness): [`PROPAGATOR_FAMILY_UNIFICATION_NOTE.md`](PROPAGATOR_FAMILY_UNIFICATION_NOTE.md)
- Downstream sibling (load-bearing on gnewtonG2): C-B(b) canonical mass-coupling branch
- Framework baseline: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Honest status

**Bounded open-gate review on the framework baseline plus direct inspection of
the named cited content of the gnewtonG1 and gnewtonG2 source notes.**
The algebraic core of both narrowings is verified by this re-audit's
runner. The named weaknesses (F1.2, F2.1, F2.2) are surfaced for the
audit lane.

**Audit-lane handoff:**

```yaml
proposed_claim_type: open_gate
proposed_claim_scope: |
  Hostile-review source note for gnewtonG1 (skeleton-selection) and
  gnewtonG2 (Born-as-source) narrowings. Records both as bounded
  support with explicit named weaknesses:
  F1.2 hidden modeling step (static-sector privilege replaces
  closure identity); F2.1 citation defect (Born-rule operationalism
  cited from a note with zero Born content); F2.2 source-coupling
  question untouched (explicitly out-of-scope per gnewtonG2). Net
  effect: neither open gate closes; planckP4 three-admission framing
  preserved; the downstream C-B(b) mass-coupling chain inherits F2.1
  for correction.
proposed_load_bearing_step_class: A (linear algebra verification + 
  direct file inspection of cited content)
status_authority: independent audit lane only
admitted_observation_status: null
source_inputs: standard QM linear algebra + direct grep of cited content
```

## Validation

```bash
python3 scripts/cl3_closure_t2_gnewton_reaudit_2026_05_10_t2gnewton.py
```

Expected output: structural verification of (i) gnewtonG1 algebraic
core T1-T4 (static-sector reduction of three skeleton families to
H = -Δ_lat exact), (ii) gnewtonG1 hidden modeling step T5 (non-static
d'Alembertian has retardation, confirming static restriction is
modeling), (iii) gnewtonG2 unified Born map T6 (linearity, pure
reduction, mixed reduction, non-negativity, normalization), (iv)
gnewtonG2 citation defect T7 (zero "Born" matches in
CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md), (v) gnewtonG2
scope limitation T8 (source-coupling question untouched), (vi)
admission count preservation T9 (three-admission framing intact),
(vii) hostile-review synthesis T10.

Total: PASS=N, FAIL=0 across re-audit checks (specific N reported in
the runner output line).

Cached: [`logs/runner-cache/cl3_closure_t2_gnewton_reaudit_2026_05_10_t2gnewton.txt`](../logs/runner-cache/cl3_closure_t2_gnewton_reaudit_2026_05_10_t2gnewton.txt)
