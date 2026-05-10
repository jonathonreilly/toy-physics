# Abstract-Algebraic Core Extraction

**Universal pre-engineering doctrine for `/physics-loop` work.** Every
new source note + companion runner should be produced by this protocol,
whether the target is fresh derivation work or recovery of a stuck
audit-graph row. The protocol is the integration layer that pulls
together [`assumption-import-audit.md`](assumption-import-audit.md) +
[`literature-bridge-protocol.md`](literature-bridge-protocol.md) and
adds first-principles and math-verification steps with explicit
output-shape discipline.

The technique's name describes what it produces: a narrow theorem whose
proof is the abstract-algebraic core that the framework axioms (or
less) genuinely force, separated from physical/conceptual imports that
belong elsewhere. The same technique applies whether you start from a
fresh physics question or from an already-stuck row.

For full rationale and case-study evidence see
[`../../../ABSTRACT_ALGEBRAIC_CORE_EXTRACTION_TECHNIQUE_2026-05-10.md`](../../../ABSTRACT_ALGEBRAIC_CORE_EXTRACTION_TECHNIQUE_2026-05-10.md).

## Premise

Every theoretical-physics claim in this framework decomposes into three
layers:

1. **Abstract-algebraic skeleton** — forced by `MINIMAL_AXIOMS_2026-05-03`
   alone (sometimes by less; sometimes by pure polynomial algebra or
   standard representation theory).
2. **Implicit physical/conceptual imports** — specific Wilson action,
   plaquette numerics, named open gates, governance conventions
   (`Q_e = -1`, quark/lepton labelling), unit conventions.
3. **Numerical evaluations** — retained values cited as sanity checks
   but not load-bearing for the proof.

A source note that mixes the three layers in one claim cannot retain
cleanly because the implicit imports either are not cited as one-hop
deps (so the chain never closes), or are cited but the upstream is
itself unaudited / conditional (so the row sits in
`retained_pending_chain` indefinitely). The audit-lane policy in
`docs/audit/README.md` §1 calls this the "definition-as-derivation" /
"conditional-on-open-work" pattern.

The technique separates the three layers up-front. It ships the
algebraic skeleton as a standalone narrow theorem with `deps=[]` (or
only retained-grade deps); the implicit imports are explicitly declared
out of scope in a mandatory "What this does NOT claim" section; the
numerical evaluations live in a clearly-marked "illustrative sanity
check" subsection.

## When to use this protocol

Use as the **default** for any `/physics-loop` cycle that intends to
produce a new source note + runner, in two main application contexts:

### Application A — fresh derivation work (proactive)

The cycle is attacking a physics question, no audit verdict exists yet.
Run the 4 exercises before writing any source-note text. Aim for the
narrowest theorem the framework axioms (or less) force. Get the
claim_type right the first time (`positive_theorem` with `deps=[]` is
the strongest tier; reach for it).

### Application B — stuck audit-graph row recovery (reactive)

The target row is `audited_conditional` / `unaudited critical` /
`audited_renaming` / `audited_numerical_match` and has an audit verdict
that names a `repair_class`. The verdict's
`notes_for_re_audit_if_any` IS the diagnostic — it tells you where the
carve-out boundary lives. Map the `repair_class` to one of the
narrow-theorem output shapes in the carve-out table below.

### When NOT to use this protocol

- The target is in `archive_unlanded/` (already retired as
  ratified negative result).
- The audit lane has already cleared the row (`audited_clean` or any
  `retained*` effective_status) and nothing about the source note has
  drifted.
- The target requires multi-day open-derivation work that genuinely
  cannot fit a bounded source note even after the 4 exercises (rare;
  do the 4 exercises first to confirm).

## Carve-out table (repair_class → narrow output)

Use this table in Application B (stuck audit-graph row recovery). For
Application A (fresh derivation), there is no `repair_class` yet — the
4 exercises produce the carve-out boundary directly without needing
an auditor diagnostic.

| repair_class | Carve-out shape |
|---|---|
| `missing_dependency_edge` | Wire a retained one-hop dep as citation; OR write a narrow note providing the missing identity as a standalone narrow theorem with `deps=[]`. |
| `dependency_not_retained` | Retain the upstream first (separate PR) OR carve out the piece that doesn't need that upstream as a narrow theorem. |
| `missing_bridge_theorem` | Extract the abstract-algebraic skeleton; explicitly declare the bridge step out of scope via "What this does NOT claim". |
| `scope_too_broad` | Split into a cleanable narrow theorem + an open limb; the open limb stays with the parent row. |
| `runner_artifact_issue` | Rewrite the runner as self-contained with explicit threshold checks; inline helpers from imported probe modules. |
| `compute_required` | Cache a hash-pinned runner log; OR provide independent algebraic verification that bypasses the slow compute. |
| `other` | Read the auditor's prose; structurally identical to one of the above. |

## The 4 mandatory exercises (BEFORE engineering)

Per the Counterfactual-Pass-Before-Compute rule. Run all four in order.
Produce written reasoning artifacts for each before any code is touched.

### 1. Assumptions exercise

Read these in order:

1. [`docs/MINIMAL_AXIOMS_2026-05-03.md`](../../../../MINIMAL_AXIOMS_2026-05-03.md)
2. The source note (`note_path` in the ledger row).
3. The audit verdict's `notes_for_re_audit_if_any`,
   `verdict_rationale`, `chain_closure_explanation` (look in
   `docs/audit/data/audit_ledger.json` row for the target).
4. Every prior verdict in the row's `previous_audits` (often names a
   repair direction earlier verdicts converged on).

Enumerate every implicit assumption the load-bearing step makes.
Classify each:

- **(✓) A1+A2 forces it** — derivable from Cl(3) on Z^3 + accepted
  normalizations. Safe to keep.
- **(✗) hidden import** — admitted convention / fitted value /
  conditionally-retained upstream / named-open-gate. **Carve-out
  boundary candidate.**
- **(?) needs derivation** — out of scope for this PR; declare in
  "What this does NOT claim".

### 2. First-principles (Elon) exercise

Strip conventions. From `MINIMAL_AXIOMS_2026-05-03` alone (or sometimes
less), what is the minimal identity that captures the structural
skeleton?

Frequently the right narrow form is one of:

- Algebraic identity over abstract positive scalars (R^+, Q^+) — pure
  polynomial algebra, no axioms consumed.
- Symbolic identity over abstract symbols under named parametric
  hypotheses (positivity, partition rank, conjugation symmetry).
- Textbook representation-theory fact specialized to the framework's
  finite case (Schur orthogonality, Burnside on M_3(C), Peter-Weyl on
  SU(3), Reynolds projector, Pauli irreducibility for Cl_n(C),
  Osterwalder-Seiler reflection positivity).
- Polynomial-algebra fact on R[t] (boundedness, finite-limit forces
  constant, finite-support corollary).
- Canonical decomposition forced by the framework's discrete symmetry
  (D_4 orbit decomposition at one layer, Z_3 cyclic structure on a
  3-vertex block, cubic Coxeter six-tetrahedra triangulation).

### 3. Literature search

WebSearch for the textbook hook. Cite standard results to:

1. Confirm the structural fact is textbook, not novel.
2. Identify the right named theorem to cite.
3. Avoid accidentally re-deriving incorrectly.

Cited literature is reference-only, NEVER load-bearing. No literature
numerical value enters as a derivation input. Citations live in
"Relation to literature" or "Cross-references" sections, not in the
proof.

### 4. Math search

Use `sympy` for symbolic verification, `scipy.special` for special
functions, `numpy` for numerical edge cases, plus explicit
counterexamples to confirm load-bearing assumptions are necessary.

Companion runner must:

- Symbolically verify every claimed identity.
- Numerically test on concrete instances.
- Run a counterexample showing breaking a named hypothesis breaks the
  identity (proves the hypothesis is load-bearing, not vacuous).
- End with a `PASS=N FAIL=M` summary line.

## Fallback hierarchy

Aim highest. Fall back only when the 4 exercises rule out higher
tiers. Each row in the table maps to one of the canonical templates.

| Tier | Shape | Retains as | Template to mirror |
|---|---|---|---|
| 1 | Pure abstract algebra, `deps=[]` | `retained` | `KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md` |
| 2 | Constrained abstract algebra, `deps=[]` | `retained` | `CKM_MAGNITUDES_STRUCTURAL_COUNTS_NARROW_THEOREM_NOTE_2026-05-02.md` |
| 3 | Standard rep theory, `deps=[]`, literature as background | `retained` | `KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md` |
| 4 | Carve-out with retained-grade deps | `retained_bounded` | Any of above + explicit dep list |
| 5 | Reclassification (edit `**Type:**` in source) | depends on new type | Edit existing note; mirror nothing new |
| 6 | Runner-artifact repair (self-contained runner) | row becomes re-audit candidate | Rewrite runner; don't touch source unless scope-narrowing |
| 7 | Deprioritization synthesis (claim_type meta) | `meta` | `QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md` |

## Required output sections

In order, in every narrow theorem source note:

1. Title.
2. Metadata block: Date, Type, Claim scope, Status authority, Runner.
3. Statement (abstract symbols, explicit equations).
4. Proof (algebraic, sympy-verifiable).
5. What this claims (enumerate T1, T2, ...).
6. **What this does NOT claim** — the carve-out boundary. Mandatory.
7. Cited dependencies (`None` if pure-abstract; or explicit
   retained-grade list).
8. Forbidden imports check (`No PDG values consumed.`, `No literature
   numerical comparators consumed.`, `No fitted selectors consumed.`,
   `No admitted unit conventions load-bearing on retention.`, `No
   same-surface family arguments.`).
9. Validation (runner output, `PASS=N FAIL=0` line).

## Anti-patterns (the doctrine forbids)

- **Definition-as-derivation**: defining a new symbol as a
  small-integer ratio and "showing" it matches data by name
  substitution. The audit-lane README §1 is built to detect this.
- **Numerical match without algebraic content**: runner reproduces a
  number but no symbolic identity is verified.
- **New repo vocabulary**: introducing new tags / new claim_types /
  new framings. Per MEMORY.md (2026-05-08) — the reviewer rejects
  these even when underlying content is correct.
- **Parent-promotion language**: stating that the narrow theorem
  "closes" or "retires" the parent. The parent's audit status stays
  what it was; the narrow theorem is a parallel artifact.
- **Markdown-link cross-references to other `.md` files where
  `deps=[]` is required**: the citation-graph builder extracts
  markdown links to `.md` files as deps. For Tier 1-3 (pure
  abstract), use plain-text canonical filenames in "Cross-references"
  and "Relation to parent" sections.

## Cycle-break dividend

In a small fraction of cases (2 of 27 in the 2026-05-10 campaign),
the carve-out also actually breaks an audit-graph cycle by stripping
reciprocal markdown links. Document this in the PR body but do NOT
count on it as the primary goal — the goal is the retainable narrow
theorem, the cycle break is incidental.

## Branch + PR hygiene

- Always use an isolated worktree (`isolation: "worktree"`).
- Single commit per narrow theorem + companion runner.
- PR title: `audit: positive closure attempt — <slug> (<reason
  selected>)`.
- PR body: cite the source-survey PR (e.g., #988 plaquette chain
  map, #1017 cycle-break analysis, #1019 publication-surface
  survey), name the 4-exercise findings briefly, report PASS count.

## Relation to other physics-loop references

- [`assumption-import-audit.md`](assumption-import-audit.md): the
  base audit protocol. The core-extraction technique builds on it
  by adding first-principles + literature + math + PR engineering.
- [`route-patterns.md`](route-patterns.md): the route-choice library.
  The core-extraction technique is a hybrid of `constructive
  theorem`, `exact runner`, and `import retirement` routes.
- [`literature-bridge-protocol.md`](literature-bridge-protocol.md):
  the protocol for honest literature import. The core-extraction
  technique uses literature for hooks only.
- [`long-running-execution.md`](long-running-execution.md): the
  campaign-budget doctrine. Parallel-agent batches of the
  core-extraction technique are the empirically-validated way to
  spend a multi-hour budget on stuck audit-graph clusters.
