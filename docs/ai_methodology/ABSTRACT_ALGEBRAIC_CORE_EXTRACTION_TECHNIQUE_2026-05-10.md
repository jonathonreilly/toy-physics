# Abstract-Algebraic Core Extraction Technique

**Date:** 2026-05-10
**Status:** AI-methodology doctrine derived from a 27-PR parallel-agent
campaign on 2026-05-10. Documents a reproducible technique for converting
ostensibly-blocked critical audit-graph rows into retainable narrow
`positive_theorem` source notes.
**Companion reference for agents:**
[`skills/physics-loop/references/abstract-algebraic-core-extraction.md`](skills/physics-loop/references/abstract-algebraic-core-extraction.md)

## What this is

A reproducible protocol for taking a "stuck" audit-graph row
(`audited_conditional`, `unaudited critical`, `missing_bridge_theorem`,
`scope_too_broad`) and shipping a standalone narrow theorem that audits
clean and retains. The technique was discovered empirically during a
2026-05-10 parallel-agent campaign (Rounds 1+2, 27 deliverables) and is
validated by a 100% retainable-artifact rate across 23 attempts.

The technique is not a new physics result. It is a packaging discipline.
The audit lane already classifies claim_type and resolves dependency
chains; this technique exploits the fact that most stuck rows mix
purely-algebraic skeletons with heavy physical imports, and the
audit-lane verdicts (`notes_for_re_audit_if_any`) tell you exactly where
the carve-out boundary is.

## Why it works

Most stuck source notes mix three layers in the same claim:

1. **Abstract-algebraic skeleton.** Forced by `MINIMAL_AXIOMS_2026-05-03`
   (Cl(3) on Z^3) alone — sometimes by even less (standard
   representation theory, polynomial algebra over abstract symbols, or
   universal trigonometry).
2. **Implicit physical/conceptual imports.** Specific Wilson action,
   plaquette numerics, named open gates, governance conventions
   (`Q_e = -1`, quark/lepton labelling), unit conventions.
3. **Numerical evaluations.** Retained values cited as sanity checks but
   not load-bearing for the proof.

The mixing prevents clean retention. The implicit imports are either
not cited as one-hop deps (so the chain never closes), or are cited but
the upstream is itself unaudited / conditional / structurally blocked
(so the row sits in `retained_pending_chain` indefinitely). The
audit-lane policy in [`docs/audit/README.md`](../audit/README.md) calls
this pattern "definition-as-derivation" or "conditional-on-open-work"
and is built precisely to detect it.

The technique decomposes the three layers, ships the algebraic skeleton
as a standalone narrow theorem with `deps=[]` (or only retained-grade
deps), and explicitly declares the implicit imports out of scope in a
mandatory "What this does NOT claim" section. The result is a
`positive_theorem` that audits clean and resolves to
`effective_status: retained`.

## The 4 mandatory exercises (in order, BEFORE engineering)

Per MEMORY.md "Run Counterfactual Pass before compute" and the SU(3)
campaign's 7-wasted-PR lesson on wrong-geometry assumptions: run the
four exercises before any code is written. Each produces a written
artifact in the agent's reasoning trace.

### 1. Assumptions exercise

Read [`docs/MINIMAL_AXIOMS_2026-05-03.md`](../MINIMAL_AXIOMS_2026-05-03.md),
the source note, and the audit verdict
(`notes_for_re_audit_if_any` + `verdict_rationale` +
`chain_closure_explanation` in `docs/audit/data/audit_ledger.json`).

Enumerate every implicit assumption the source note's load-bearing step
makes. Classify each:

- **(✓) derivable from A1+A2** — the framework's two axioms (Cl(3)
  algebra, Z^3 substrate) alone force it. Safe.
- **(✗) hidden import** — admitted convention, fitted value,
  conditionally-retained upstream, or named-open-gate dependency. The
  carve-out boundary candidate.
- **(?) needs first-principles derivation** — not yet known to be
  derivable. Out of scope for this PR.

The audit verdict's `repair_class` is the diagnostic. Each `repair_class`
maps to a specific carve-out shape:

| repair_class | Carve-out shape |
|---|---|
| `missing_dependency_edge` | Wire a retained one-hop dep as citation; OR write a narrow note providing the missing identity |
| `dependency_not_retained` | Either retain the upstream first OR carve out the piece that doesn't need that upstream |
| `missing_bridge_theorem` | Extract the abstract-algebraic skeleton; explicitly declare the bridge step out of scope |
| `scope_too_broad` | Split into a cleanable narrow theorem + an open limb |
| `runner_artifact_issue` | Make runner self-contained with explicit threshold checks |
| `compute_required` | Cache a hash-pinned runner log; OR provide independent algebraic verification |
| `other` | Read the auditor's note prose; structurally identical to one of the above |

### 2. First-principles (Elon) exercise

Strip all conventions. Starting only from `MINIMAL_AXIOMS_2026-05-03`
(and sometimes less — many algebraic cores don't need A1 or A2 at all),
what is the minimal identity that captures the structural skeleton of
the target?

Often dramatically narrower than what the parent source note claims.
The narrow form is frequently:

- An algebraic identity over abstract positive scalars (R^+, Q^+).
- A symbolic identity over abstract symbols satisfying named
  parametric hypotheses (positivity, partition rank, conjugation
  symmetry).
- A textbook representation-theory fact specialized to the framework's
  finite case (Schur orthogonality, Burnside on M_3(C), Peter-Weyl on
  SU(3), Reynolds projector, Pauli irreducibility for Cl_n(C)).
- A pure polynomial-algebra fact on R[t] (boundedness, finite-limit
  forces constant, finite-support corollary).
- A canonical decomposition forced by the framework's discrete
  symmetry (D_4 orbit decomposition, Z_3 cyclic structure, cubic
  Coxeter triangulation).

### 3. Literature search

Use WebSearch (or the agent's literature-search tool of choice) to find
the relevant textbook hook. The narrow theorem is almost always a
specialization of a named classical result. The literature serves three
purposes:

1. Confirm the structural fact is textbook, not novel — this keeps the
   narrow theorem inside the "standard result, specialized" regime
   rather than "new science".
2. Identify the right named theorem to cite (Burnside 1905, Reynolds,
   Schur, Peter-Weyl, Osterwalder-Seiler 1978, Wald 1993, etc.).
3. Avoid accidentally re-deriving something incorrectly.

The cited literature is reference-only, not load-bearing. Per the
"Forbidden imports check", the narrow theorem must NOT consume a
literature numerical value as a derivation input. Citations live in
the note's "Relation to literature" or "Cross-references" section, not
in the proof.

### 4. Math search

Use `sympy` for symbolic verification, `scipy.special` for any special
functions, `numpy` for numerical edge cases, and explicit
counterexamples to confirm load-bearing assumptions are genuinely
necessary.

The companion runner must:

- Symbolically verify every claimed identity.
- Numerically test on concrete instances.
- Run a counterexample showing that breaking a named hypothesis
  breaks the identity (proves the hypothesis is load-bearing).
- End with a `PASS=N FAIL=M` summary line.

## Fallback hierarchy

Aim highest. Fall back only when the 4 exercises rule out higher tiers.

1. **Pure abstract algebra, `deps=[]`** — abstract symbols over R, C,
   or Q^+; no axioms consumed. Retains as `effective_status: retained`.
   *Examples in this session:* alpha_lm geometric mean (#969), g_bare
   rescaling (#1034), Wolfenstein λA cancellation (#1047), plaquette
   hierarchy polynomial boundedness (#1072), g_bare forced by Ward
   (#1070).
2. **Constrained abstract algebra, `deps=[]`** — pure algebra under
   explicit named hypotheses. Retains as `retained`.
   *Examples:* CKM inverse-square sum rule (#1082), g_bare constraint-
   vs-convention dimension counting (#1074), CKM CP phase ρη→δ
   (#1085).
3. **Standard representation theory, `deps=[]`** — textbook result
   cited as background only. Retains as `retained`.
   *Examples:* SU(3) Casimir = 4/3 (#1081), Pauli irreducibility for
   Cl(4) (#1031), Burnside on M_3(C) (#1041), Reynolds projector
   (#1079), Clifford chirality-dimension (#1038), cubic-Coxeter Regge
   deficit vanishing (#1043).
4. **Carve-out with retained-grade deps** — when the parent has both
   an abstract core and non-trivial finite data, ship just the
   cleanable core with citations to the retained finite-data
   companion. Retains as `retained_bounded` style.
   *Examples:* BH Wald-Newton coefficient identity (#1040), area-law
   CAR Fock equivalence (#1031), Wilson plaquette RP gauge-only
   (#1037), all 4 plaquette `missing_bridge_theorem` rows (#1076,
   #1078, #1083, #1087).
5. **Reclassification** — when existing audit machinery
   misclassified the row's claim_type. Edit `**Type:**` line in the
   source note; pipeline updates `claim_type_author_hint`.
   *Examples:* alpha_lm `decoration → positive_theorem` (#969),
   3d_correction_master `positive_theorem → meta` (#1033).
6. **Runner-artifact repair** — when the verdict is specifically
   `runner_artifact_issue`. Rewrite the runner as self-contained with
   explicit threshold checks, inlining helpers from imported probe
   modules where needed.
   *Example:* source_driven_field_recovery_sweep (#1036).
7. **Deprioritization synthesis** — only if the 4 exercises rule out
   all of the above. Honest acknowledgment that the target requires
   substantive open derivation work. claim_type `meta`,
   `proposal_allowed: false`.
   *Examples:* area_law_coefficient_gap terminal synthesis (#1030),
   quark_projector terminal synthesis (#959/0c967b379 landed via
   review-loop), DM_leptogenesis terminal synthesis (#960/landed),
   claude_complex_action terminal synthesis (#984/landed).

## Output discipline

Mirror an existing canonical narrow-theorem template byte-for-byte.
The canonical templates as of 2026-05-10:

- [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](../KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md)
  — flagship template: deps=[], abstract-symbol Statement, sympy proof,
  rigorous "What this does NOT claim", Forbidden imports check.
- [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](../KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)
  — variant for bridge-identity narrow theorems.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_NARROW_THEOREM_NOTE_2026-05-02.md`](../CKM_MAGNITUDES_STRUCTURAL_COUNTS_NARROW_THEOREM_NOTE_2026-05-02.md)
  — variant for parametric-hypothesis narrow theorems.

Required sections (in order):

1. Title.
2. Date metadata block: Date, Type, Claim scope, Status authority,
   Runner.
3. Statement (abstract symbols, explicit equations).
4. Proof (algebraic, sympy-verifiable).
5. What this claims (enumerate T1, T2, ...).
6. What this does NOT claim (rigorous scope discipline — the
   carve-out boundary).
7. Cited dependencies (`None` if pure-abstract; or explicit
   retained-grade list).
8. Forbidden imports check (PDG values, fitted selectors, admitted
   conventions, same-surface family arguments — all marked `No ...
   consumed`).
9. Validation (runner output, PASS=N FAIL=0 signature).

## Failure modes the technique avoids

- **Definition-as-derivation**: the audit-lane's named anti-pattern.
  The Forbidden imports check explicitly prohibits PDG values, fitted
  selectors, and admitted unit conventions from being load-bearing.
- **Numerical match without algebraic content**: the runner must verify
  symbolic identities, not just numerical coincidence. Counterexamples
  are mandatory.
- **New repo vocabulary**: the source note must mirror an existing
  canonical template byte-for-byte; no novel framing, no new
  claim_types, no new tags. Per MEMORY.md "Don't introduce new repo
  vocabulary in PRs" (2026-05-08).
- **New axioms**: A_min is fixed (Cl(3) on Z^3 + accepted
  normalizations); the technique never extends. Per MEMORY.md "No
  new axioms" (2026-05-04).
- **Scope creep**: the "What this does NOT claim" section is
  mandatory. Without it, the parent's heavy content leaks back into
  the narrow theorem and breaks the retention chain.

## Empirical evidence

The technique was applied 23 times across two parallel-agent campaigns
on 2026-05-10. Outcomes:

- 21 `positive_theorem` closures (deps=[] or retained-grade only).
- 2 `bounded_theorem` carve-outs with retained-grade deps.
- 0 cases where no retainable artifact could be shipped.

The biggest surprise: 4 of 4 plaquette `missing_bridge_theorem` rows
(documented in [`PLAQUETTE_ALPHA_S_CHAIN_AUDIT_MAP_SYNTHESIS_META_NOTE_2026-05-10.md`](../PLAQUETTE_ALPHA_S_CHAIN_AUDIT_MAP_SYNTHESIS_META_NOTE_2026-05-10.md)
as "out of scope for bounded source notes") yielded extractable narrow
cores when the 4-exercise protocol was applied (PRs #1076, #1078,
#1083, #1087). The chain map's pessimism missed extractable cores that
the audit verdict's own `OR-narrow` clause had already named.

Two cycles in the audit graph were actually broken: cycle-0003 (#1033
3d_correction_master reclassification) and cycle-0016 (#1081 su3_casimir
proof-walk standalone). Net cycle count 305 → 303.

## Relation to other AI methodology lanes

- [`METHODOLOGY_CASE_STUDIES_2026-04-25.md`](METHODOLOGY_CASE_STUDIES_2026-04-25.md):
  the case-study spine for the methodology paper. The 2026-05-10
  campaign provides a new case study: large-batch parallel agents
  applying the 4-exercise protocol. This document is the procedural
  doctrine that case study describes.
- [`skills/physics-loop/references/assumption-import-audit.md`](skills/physics-loop/references/assumption-import-audit.md):
  the existing protocol for auditing assumptions and imports. The
  core-extraction technique is a specialization that adds first-
  principles + literature + math steps to that audit and ships a
  retainable artifact.
- [`skills/physics-loop/references/route-patterns.md`](skills/physics-loop/references/route-patterns.md):
  the existing pattern library for route choice. The core-extraction
  technique is a hybrid of `constructive theorem`, `exact runner`,
  and `import retirement` routes.
- [`skills/physics-loop/references/literature-bridge-protocol.md`](skills/physics-loop/references/literature-bridge-protocol.md):
  the existing protocol for honest literature import. The
  core-extraction technique uses literature for hooks only, never as
  load-bearing import.

## What this document is NOT

- Not a new claim_type or new audit-lane status.
- Not a replacement for `assumption-import-audit.md` (it builds on
  that protocol).
- Not a way to ship novel physics — the technique surfaces
  textbook-shape narrow theorems that the framework's axioms already
  force, not new results.
- Not applicable to genuinely open derivation work (e.g., the 4
  plaquette `missing_bridge_theorem` rows' full bridge derivations
  remain open; only their narrow carve-outs landed).

## Forbidden imports check

This methodology document itself does not consume:

- No PDG observed values.
- No literature numerical comparators load-bearing.
- No fitted selectors.
- No admitted unit conventions.

It documents a procedural technique; no physics content is asserted.
