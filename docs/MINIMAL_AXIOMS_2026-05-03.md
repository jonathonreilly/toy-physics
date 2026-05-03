# Minimal Framework Axioms (Restored)

**Date:** 2026-05-03
**Status:** current public framework memo for the `Cl(3)` / `Z^3` package
**Type:** meta
**Supersedes:** `MINIMAL_AXIOMS_2026-04-11.md` (the
2026-04-11 file as it existed up to commit `0267ef09f`; the 2026-04-15
rewrite that introduced A3, A4, A5 as additional axioms is being backed
out by this note).

## What this note does

This note **restores the framework's axiom set to the two axioms** that
were originally approved (A1, A2 in the language of the April 15 rewrite —
which corresponded to the algebraic core of the April 11 "bundled modeling
ingredients" framing).

The April 15 rewrite (`24d698d94`, bundled into a YT/EW Higgs documentation
commit and not surfaced as a separate axiom-set decision) promoted three
modeling-ingredient items to the status of framework axioms:

- the staggered-Dirac/Grassmann fermion realization,
- the physical-lattice reading,
- the `g_bare = 1` + `u_0` + APBC normalization surface.

The physical-lattice reading was later derived
(`PHYSICAL_LATTICE_NECESSITY_NOTE.md`) and removed (April 16). This note
removes the remaining two by recategorizing them as **open gates**, not
framework axioms.

## The two framework axioms

1. **A1 — Local algebra:** the physical local algebra is `Cl(3)`.
2. **A2 — Spatial substrate:** the physical spatial substrate is the cubic
   lattice `Z^3`.

These two are self-contained, mathematically minimal, and have zero upstream
dependencies. Everything below the framework's surface is either:
- a closed derivation chain from A1+A2 (`claim_type: positive_theorem`,
  `effective_status: retained`),
- a bounded result with explicit named admissions (`claim_type:
  bounded_theorem`, `effective_status: retained_bounded`), or
- an open gate with explicit closure path (`claim_type: open_gate`).

## Items recategorized from "axiom" to open gate

These two items were previously listed as axioms A3 and A4. They are
now recategorized as **open gates**, using the existing `claim_type:
open_gate` machinery, with the canonical parent note (where one exists)
identified explicitly and the supporting derivation chain enumerated.

The naming convention follows the existing repo pattern: refer to each
gate by its canonical parent note name. No new abstract gate labels are
introduced.

### Staggered-Dirac realization derivation target (formerly axiom A3)

> "A1+A2 plus admissible mathematical infrastructure forces (or
> sufficiently constrains) the Grassmann staggered-Dirac realization,
> including the BZ corner doubler structure that maps to three SM
> matter generations."

**Canonical parent note:** *not yet packaged*. Currently no single
canonical parent note for this derivation target — the pieces are
spread across multiple existing notes. Packaging a single canonical
parent note is itself part of the follow-up work this restructure
exposes.

**In-flight supporting work** (the existing derivation pieces):
- `PHYSICAL_LATTICE_NECESSITY_NOTE.md` — closes the substrate-level
  physical-lattice reading on the accepted one-axiom Hilbert/locality/
  information surface (already retained as a downstream derivation
  rather than a separate axiom).
- `THREE_GENERATION_STRUCTURE_NOTE.md` — local algebraic/spectral
  content of the three-generation matter structure (retained, td=248).
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — exact observable-sector
  theorem on hw=1 triplet (retained, td=123).
- `frontier_generation_rooting_undefined.py` — proves no proper taste
  projection preserves Hamiltonian Cl(3) on Z^3 (no-rooting; retained).
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` — older reduced-stack witness
  preserved for boundary documentation.

**Closure status:** partial. Pieces of an "A3 follows from A1+A2"
argument exist across the notes above. They have not been packaged as a
single canonical parent note. **Open derivation target.**

**Lanes that depend on this gate:** any lane whose derivation defines
fermion fields, fermion-number operators, fermion correlators, fermion
bilinears, or staggered Dirac action (essentially every lane that
touches matter content). These lanes should be reviewed as
`bounded_theorem` surfaces with "staggered-Dirac realization derivation
target (parent note: pending packaging — see in-flight supporting work
above)" listed in `admitted_context_inputs` until the gate closes.

### g_bare = 1 derivation target (formerly axiom A4)

> "A1+A2 (+ closure of the staggered-Dirac realization target) forces
> `g_bare = 1` by canonical Cl(3) connection normalization; the Wilson
> plaquette coefficient `β = 2 N_c = 6` follows."

**Canonical parent note:** `G_BARE_DERIVATION_NOTE.md`
— `claim_type: positive_theorem`, `audit_status: audited_conditional`.
Codex-named repair targets: missing primary runner, A → A/g rescaling
freedom, constraint-vs-convention ambiguity. The April 15 rewrite
labeled this as "by fiat with consilience"; the derivation chain
below was already in progress at that time.

**In-flight supporting work** (the existing g_bare derivation chain):
- `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` — Cl(3)
  → End(V) → su(3) → Wilson chain. Claims 1, 2 PROVED (canonicity up
  to finite outer automorphism). Claim 3 PARTIAL: forces `β = 2 N_c =
  6` given Wilson action functional form.
- `G_BARE_RIGIDITY_THEOREM_NOTE.md` — operator-algebra rigidity route
  (audited_conditional).
- `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md` — 1PI two-Ward closure
  route (audited_conditional).
- `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md` —
  load-bearing Rep-B independence statement (audited_conditional).
- `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md` —
  off-surface same-1PI pinning theorem (audited_conditional).
- `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md` — closes
  the Grassmann/spectral dynamical-fixation class negatively (unaudited).
- `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md` —
  bounded narrow theorem on the canonical-convention reading
  (retained_bounded).

**Closure status:** partial. Multiple closure routes exist; each has
named remaining residuals captured in the parent note's audit
verdict. **Open derivation target.**

**Lanes that depend on this gate:** any lane that produces quantitative
gauge predictions (`α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`,
etc.) by fixing `g_bare = 1` without independently deriving it. These
lanes should be reviewed as `bounded_theorem` surfaces with "g_bare = 1
derivation target (parent: G_BARE_DERIVATION_NOTE.md)" listed in
`admitted_context_inputs` until that note's audit verdict closes clean.

## What this means for the existing science stack

Recategorization uses **existing framework vocabulary only** — the
`claim_type` enum (positive_theorem / bounded_theorem / no_go / open_gate
/ decoration / meta) plus `admitted_context_inputs` already does the
work. No new tier labels are introduced.

### Lanes that close on A1+A2 alone

Target review typing: `positive_theorem`. Once the independent audit lane has
an `audited_clean` verdict and retained-grade dependencies, the pipeline
derives `effective_status: retained`. These rows have zero open-gate
admissions in `admitted_context_inputs`:

- `cl3_per_site_uniqueness` (only A1)
- `cl3_color_automorphism` (A1+A2)
- the Z_3 Fourier diagonalization on hw=1 (PR #413; rides on retained
  three-generation chain via A1+A2 only)
- per-site Pauli group structure
- per-site su(2) spin-1/2 algebra (R5 Block 03)
- no-per-site γ_5 chirality (R6 Block 01)
- structural Z^3 lattice geometry results

### Lanes that depend on the staggered-Dirac realization gate

Target review typing until the gate closes: `bounded_theorem`, with
`admitted_context_inputs` listing the staggered-Dirac realization derivation
target (currently undischarged). Once such a row has an `audited_clean`
bounded-theorem verdict and retained-grade dependencies, the pipeline derives
`effective_status: retained_bounded`:

- `coleman_mermin_wagner` (needs Hamiltonian)
- `cpt_exact` (needs staggered structure)
- `lattice_noether` (needs action)
- `spin_statistics` (needs Grassmann)
- three-generation, baryon/meson singlet, fermion-parity Z_2,
  Q̂ integer spectrum, hopping bilinear, etc.

When this gate closes, these lanes become eligible for independent audit or
repo-governance retagging as `positive_theorem`; the review loop must not
rewrite auditor-owned `claim_type` fields by implication.

### Lanes that depend on both gates

Target review typing until both gates close: `bounded_theorem`, with
`admitted_context_inputs` listing both the staggered-Dirac realization
derivation target and the g_bare = 1 derivation target (canonical parent:
`G_BARE_DERIVATION_NOTE.md`):

- All `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2` quantitative
  results (`y_t` lane, EW lane, Higgs lane, etc.).

When both gates close, these lanes become eligible for independent audit or
repo-governance retagging as `positive_theorem`.

## Comparison with prior framing

**Prior framing (April 15 → May 2):**
> "Framework has 4 axioms (Cl(3), Z³, Grassmann staggered Dirac, g_bare = 1)."

**Restored framing (this note, restoring April 11 intent):**
> "Framework has 2 axioms (Cl(3), Z³). The fermion realization and gauge
> normalization are open gates (the staggered-Dirac realization gate and
> the g_bare = 1 derivation gate with parent
> `G_BARE_DERIVATION_NOTE.md`) with partial closure already in progress
> via 6+ notes. Every quantitative prediction that depends on those gates is
> reviewed as `bounded_theorem` with the open gates named in
> `admitted_context_inputs`. Closing those gates makes the affected lanes
> eligible for independent audit or repo-governance retagging as
> `positive_theorem`."

The framework's parameter reduction under this framing:
**19 SM numerical parameters → 2 framework axioms + 2 named open
gates**, with explicit closure paths for each gate.

## Mathematical infrastructure (ordinary)

The current package uses ordinary mathematical infrastructure after the
two framework axioms are fixed:

- spectral analysis
- lattice Monte Carlo / plaquette evaluation on the accepted surface
- perturbative low-energy EFT running where the package explicitly labels
  the bridge as bounded or bridge-conditioned

Those tools do not promote a bounded lane to retained on their own. A bounded
lane remains bounded unless the statement is scope-tightened or the named
derivation targets close and an independent audit/governance pass retags the
row. The audit pipeline recomputes `effective_status`; it does not silently
invent a new `claim_type`.

## What This File Is Not

- not a route-history document
- not a replacement for the publication matrix
- not a claim that DM, CKM, or Koide gates are already closed
- not a unilateral re-axiomatization — this restores the April 11 framing
  the user originally approved

## Citation-graph note

This note has no upstream dependencies. Plain-text references to in-flight
supporting work above are pointers for readers, not load-bearing
deps. The supporting notes themselves are downstream consequences (the
two derivation targets are open-gate
closure attempts), not upstream axioms.
