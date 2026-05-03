# Minimal Framework Axioms (Restored)

**Date:** 2026-05-03
**Status:** current public framework memo for the `Cl(3)` / `Z^3` package
**Type:** meta
**Supersedes:** [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) (the
2026-04-11 file as it existed up to commit `0267ef09f`; the 2026-04-15
rewrite that silently inserted A3, A4, A5 axioms is being backed out by
this note).

## What this note does

This note **restores the framework's axiom set to the two true axioms** that
were originally approved (A1, A2 in the language of the April 15 rewrite —
which corresponded to the algebraic core of the April 11 "bundled modeling
ingredients" framing).

The April 15 rewrite (`24d698d94`, bundled into a YT/EW Higgs documentation
commit, not surfaced as a separate decision) silently promoted three
modeling-ingredient items to the status of framework axioms:

- the staggered-Dirac/Grassmann fermion realization,
- the physical-lattice reading,
- the `g_bare = 1` + `u_0` + APBC normalization surface.

The physical-lattice reading was later derived
(`PHYSICAL_LATTICE_NECESSITY_NOTE.md`) and removed (April 16). This note
removes the remaining two by recategorizing them as **open derivation
targets**, not framework axioms.

## The two framework axioms (true axioms)

1. **A1 — Local algebra:** the physical local algebra is `Cl(3)`.
2. **A2 — Spatial substrate:** the physical spatial substrate is the cubic
   lattice `Z^3`.

These two are self-contained, mathematically minimal, and have zero upstream
dependencies. Everything below the framework's surface is either:
- a closed derivation chain from A1+A2 (positive_theorem at retained tier),
- a bounded result with explicit named imports (bounded_theorem at
  retained_bounded tier), or
- an open derivation target with explicit closure path (open_gate).

## Items recategorized from "axiom" to "open derivation target"

### Open Gate G1: Grassmann staggered-Dirac dynamics

> "A1+A2 plus admissible mathematical infrastructure forces (or sufficiently
> constrains) the Grassmann staggered-Dirac realization, including the BZ
> corner doubler structure that maps to three SM matter generations."

**Status:** open derivation target (formerly axiom A3).

**In-flight supporting work:**
- `PHYSICAL_LATTICE_NECESSITY_NOTE.md` — closes the substrate-level
  physical-lattice reading on the accepted one-axiom Hilbert/locality
  /information surface (already retained as a downstream derivation
  rather than a separate axiom).
- `THREE_GENERATION_STRUCTURE_NOTE.md` — local algebraic/spectral content
  of the three-generation matter structure (retained, td=248).
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — exact observable-sector
  theorem on hw=1 triplet (retained, td=123).
- `frontier_generation_rooting_undefined.py` — proves no proper taste
  projection preserves Hamiltonian Cl(3) on Z^3 (no-rooting);
  retained.
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` — older reduced-stack witness
  preserved for boundary documentation.

**Closure status:** partial. The pieces of an "A3 follows from A1+A2" argument
exist across multiple notes (no-rooting, three-generation observable,
physical-lattice necessity). They have not been packaged as a single clean
G1 closure theorem. **Open derivation target.**

**Lanes that ride on G1 (currently undischarged):** any lane whose
derivation defines fermion fields, fermion-number operators, fermion
correlators, fermion bilinears, or staggered Dirac action (this is
essentially every lane that touches matter content). These lanes should be
typed `bounded_theorem` with G1 listed as an admitted context input until
G1 closes — at which point they upgrade to `positive_theorem`.

### Open Gate G2: g_bare = 1 normalization

> "A1+A2 (+ G1 closure) forces `g_bare = 1` by canonical Cl(3) connection
> normalization; the Wilson plaquette coefficient `β = 2 N_c = 6` follows."

**Status:** open derivation target (formerly axiom A4).

**In-flight supporting work** (the derivation chain already exists; the
April 15 rewrite mislabeled this as "by fiat with consilience"):
- `G_BARE_DERIVATION_NOTE.md` — parent derivation (audited_conditional;
  Codex-named repair targets: missing primary runner, A → A/g rescaling
  freedom, constraint-vs-convention ambiguity).
- `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` — Cl(3) →
  End(V) → su(3) → Wilson chain. Claims 1, 2 PROVED (canonicity up to
  finite outer automorphism). Claim 3 PARTIAL: forces `β = 2 N_c = 6`
  given Wilson action functional form.
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

**Closure status:** partial. Multiple closure routes exist; each has named
remaining residuals. **Open derivation target.**

**Lanes that ride on G2 (currently undischarged):** any lane that produces
quantitative gauge predictions (`α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`,
`g_2`, etc.) by fixing `g_bare = 1` without independently deriving it.
These lanes should be typed `bounded_theorem` with G2 listed as an
admitted context input until G2 closes.

## What this means for the existing science stack

Lanes split into three tiers under the restored axiom set:

### Tier S (closed on A1+A2 alone, no open-gate riders)

These lanes use only Cl(3) algebra and Z^3 lattice geometry. They are
`positive_theorem` at `retained` tier under A1+A2 alone:

- `cl3_per_site_uniqueness` (only A1)
- `cl3_color_automorphism` (A1+A2)
- the Z_3 Fourier diagonalization on hw=1 (PR #413; rides on retained
  three-generation chain via A1+A2 only)
- per-site Pauli group structure
- per-site su(2) spin-1/2 algebra (R5 Block 03)
- no-per-site γ_5 chirality (R6 Block 01)
- structural Z^3 lattice geometry results

### Tier B-G1 (bounded; rides on Open Gate G1)

These lanes need the staggered/Grassmann realization but don't use
quantitative gauge normalization:

- `coleman_mermin_wagner` (needs Hamiltonian)
- `cpt_exact` (needs staggered structure)
- `lattice_noether` (needs action)
- `spin_statistics` (needs Grassmann)
- three-generation, baryon/meson singlet, fermion-parity Z_2,
  Q̂ integer spectrum, hopping bilinear, etc.

These should be typed `bounded_theorem` with admission "Open Gate G1
(staggered Dirac realization) currently undischarged."

### Tier B-G2 (bounded; rides on both G1 and G2)

These lanes produce quantitative gauge predictions:

- All `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2` quantitative
  results (`y_t` lane, EW lane, Higgs lane, etc.).

These should be typed `bounded_theorem` with admissions "Open Gate G1
+ Open Gate G2 currently undischarged."

## Reception story

**Old framing (April 15 → May 2):**
> "Framework has 4 axioms (Cl(3), Z³, Grassmann staggered Dirac, g_bare = 1)."
> Reviewer reaction: regulator choices presented as axioms.

**New framing (this note, restoring April 11 intent):**
> "Framework has 2 axioms (Cl(3), Z³). The fermion realization and gauge
> normalization are explicit open derivation targets (G1, G2) with
> partial closure already in flight via 6+ notes. Every quantitative
> prediction is typed `bounded_theorem` with the open targets named as
> admitted context inputs. Closing G1, G2 promotes those lanes to
> `positive_theorem`."
> Reviewer reaction: framework is honest about what's open; structural
> results don't depend on regulator choices.

This makes the framework's actual reduction visible: **19 SM numerical
parameters → 2 framework axioms + 2 named open derivation targets**, with
explicit closure paths for each open target.

## Mathematical infrastructure (ordinary)

The current package uses ordinary mathematical infrastructure after the
two framework axioms are fixed:

- spectral analysis
- lattice Monte Carlo / plaquette evaluation on the accepted surface
- perturbative low-energy EFT running where the package explicitly labels
  the bridge as bounded or bridge-conditioned

Those tools do not promote a bounded lane to retained on their own; that
requires either Open Gate G1/G2 closure (which upgrades the lane's
`claim_type`) or scope-tightening on the bounded statement itself.

## What This File Is Not

- not a route-history document
- not a replacement for the publication matrix
- not a claim that DM, CKM, or Koide gates are already closed
- not a unilateral re-axiomatization — this restores the April 11 framing
  the user originally approved

## Citation-graph note

This note has no upstream dependencies. Plain-text references to in-flight
G1 and G2 supporting work above are pointers for readers, not load-bearing
deps. The supporting notes themselves are downstream consequences (G1, G2
closure attempts), not upstream axioms.
