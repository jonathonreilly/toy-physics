# Staggered-Dirac Realization Forcing Theorem (Block 06 Synthesis)

**Date:** 2026-05-07
**Type:** bounded_theorem (synthesis of substeps 1-4)
**Claim type:** bounded_theorem
**Status:** branch-local synthesis theorem packaging the four substep
forcings (Blocks 02-05) into a single canonical-parent positive
theorem that closes the staggered-Dirac realization gate from A1+A2 +
retained primitives + admissible standard math machinery + admitted-
context AC. Replaces (when ratified by independent audit) the open-
gate parent
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
as the canonical parent identity for the staggered-Dirac realization
derivation chain.
**Authority role:** branch-local source-note proposal. Audit verdict
and effective status are set only by the independent audit lane.
**Loop:** staggered-dirac-realization-gate-20260507 (Block 06 synthesis)
**Branch:** physics-loop/staggered-dirac-realization-gate-block06-20260507
**PR status:** PR_BACKLOG (volume cap 5/24h reached at Block 05;
synthesis committed for future-campaign PR opening)

## Statement

**Theorem (Staggered-Dirac Realization Forcing).** A1 (Cl(3) local
algebra) + A2 (Z³ substrate) + admissible mathematical infrastructure
**force** (or sufficiently constrain, conditional on admitted-context
AC) the staggered-Dirac realization, including:

1. The matter measure is uniquely the Grassmann partition with one
   (χ_x, χ̄_x) Grassmann pair per site (Block 02, positive theorem,
   conditional on S2 re-audit)
2. The kinetic operator on Z³ APBC has the unique Kawamoto-Smit
   phase structure η_1=1, η_2(x)=(−1)^{x_1}, η_3(x)=(−1)^{x_1+x_2}
   up to global gauge (Block 03, positive theorem)
3. The 8 BZ corners decompose uniquely by Hamming weight as
   1+3+3+1, with the hw=1 triplet carrying the exact M_3(C) algebra
   (retained) with no proper quotient (retained)
   (Block 04, positive theorem)
4. The hw=1 triplet identifies via DHR superselection (admitted
   standard QFT machinery) as three physically distinct species
   sectors of the OS-reconstructed Hilbert space H_phys, mapping to
   three SM matter generations
   (Block 05, bounded theorem with admitted-context AC)

Combined: A1+A2 + retained primitives + admissible standard math +
admitted-context AC FORCE the staggered-Dirac realization with three
SM matter generations.

## A_min for the synthesis

```
A_min(staggered-Dirac realization) = {
  A1 (Cl(3) local algebra),
  A2 (Z^3 substrate),

  // Retained primitives (load-bearing):
  CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02 (per-site dim 2),
  AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29 (chirality-aware uniqueness),
  AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29 (S2; awaiting re-audit),
  FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02 (Z_2 grading),
  THREE_GENERATION_OBSERVABLE_THEOREM_NOTE (M_3(C) on hw=1),
  THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02,
  S3_TASTE_CUBE_DECOMPOSITION_NOTE,
  SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE,
  PHYSICAL_LATTICE_NECESSITY_NOTE,
  AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29 (RP A11),
  AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01,
  AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29,
  AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03,
  scripts/frontier_generation_rooting_undefined.py (no-rooting irreducibility),
  scripts/frontier_generation_fermi_point.py (1+1+3+3 spectral),

  // Admissible standard math machinery:
  Lie-algebra rep theory + Schur orthogonality,
  Brillouin zone / momentum-space analysis on Z^3,
  Standard staggered-fermion Kawamoto-Smit construction (1981),
  Bipartite-graph parity on Z^3,
  Pauli matrix algebra,
  Finite Grassmann calculus (Berezin, Slavnov-Faddeev),
  Bosonic Fock space construction,
  Haag-Kastler axiomatic local QFT framework,
  DHR superselection theory (Doplicher-Haag-Roberts),

  // Admitted-context (out-of-scope per GENERATION_AXIOM_BOUNDARY_NOTE):
  AC: Hilbert/no-proper-quotient semantics on accepted physical
      Hilbert surface (substep-4 conditional)
}
```

Forbidden imports:
- NO PDG observed values (no fermion masses, mixing angles, etc.)
- NO lattice MC values
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms (no-new-axiom rule)

## Synthesis chain (Blocks 02-05 in order)

### Substep 1 (Block 02): Grassmann partition forcing — POSITIVE THEOREM

A1 + A2 + retained per-site Cl(3) dim 2 + spin-statistics S2:

```
Bosonic 2nd-quantization on Cl(3) site → infinite-dim Fock per site
Per-site Cl(3) dim 2 retained → finite-dim per site forced
Therefore: bosonic INCOMPATIBLE, Grassmann FORCED.
```

Conditional on S2 re-audit at retained tier (currently support; the
2026-05-03 chirality-aware repair of upstream Cl(3) per-site
uniqueness has fixed the dependency).

### Substep 2 (Block 03): Kawamoto-Smit phase forcing — POSITIVE THEOREM

A1 + A2 + Block 02 + Cl(3) chirality + sublattice parity ε(x) =
(−1)^{x_1+x_2+x_3} + Pauli algebra:

```
Block 02 forces single-mode Grassmann per site (not 2-component spinor)
→ spin-diagonalization is forced
→ T(x) = σ_1^{x_1} σ_2^{x_2} σ_3^{x_3} (unique up to gauge)
→ T†(x) γ_μ T(x+μ̂) = η_μ(x) · I_2
→ η_1=1, η_2(x)=(−1)^{x_1}, η_3(x)=(−1)^{x_1+x_2}
```

Verified PASS=24/0 on all 8 unit-cell sites × 3 directions in exact
arithmetic (sympy Pauli algebra).

### Substep 3 (Block 04): BZ-corner three-generation forcing — POSITIVE THEOREM

Block 03 + APBC + standard staggered BZ-corner spectrum:

```
Kawamoto-Smit kinetic on Z^3 APBC → 8 BZ corners (taste cube)
Hamming-weight grading → 1+3+3+1 decomposition (counting fact)
hw=1 triplet has retained M_3(C) algebra (translations + C_3[111])
No proper quotient (retained)
→ hw=1 IS the three-generation triplet
```

Verified PASS=5/0 on structural decomposition checks.

### Substep 4 (Block 05): Physical-species bridge — BOUNDED THEOREM

Block 04 + RP A11 + Lieb-Robinson + Lattice Noether + admitted Haag-
Kastler/DHR + admitted-context AC:

```
RP A11 → OS reconstruction → physical Hilbert space H_phys
Block 04 translation characters separate hw=1 sectors on H_phys
M_3(C) irreducibility (retained no-proper-quotient) → no nontrivial invariant subspace
DHR superselection (admitted standard QFT) → three superselection sectors
Conditional on AC (Hilbert/no-proper-quotient semantics admitted-context)
→ Three physically distinct species = three SM matter generations
```

## Combined closure status

| Substep | Block | Status | Conditional on |
|---|---|---|---|
| 1. Grassmann | 02 | positive_theorem | S2 re-audit |
| 2. K-S phases | 03 | positive_theorem | Block 02 |
| 3. BZ-corner three-gen | 04 | positive_theorem | Block 03 |
| 4. Physical-species | 05 | bounded_theorem | AC admitted-context |

**Net status: synthesis BOUNDED THEOREM** — substeps 1-3 are positive
theorems (conditional on S2 re-audit), substep 4 is bounded with
admitted-context AC. Full retained-tier promotion requires:
- S2 re-audit at retained tier (independent audit lane work)
- AC upgrade to retained primitive OR direct framework-derived
  derivation of DHR correspondence (research target)

## Replacement of the open-gate parent

Once this synthesis theorem is independently audited and effectively
retained, it should REPLACE
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
as the canonical parent identity for the staggered-Dirac realization
derivation chain. Lanes that depend on staggered-Dirac (matter content,
anomaly cancellation, three generations, hypercharges, Yukawa, Higgs,
etc.) can then cite this synthesis as a positive-theorem upstream
dependency rather than admitting the gate as `admitted_context_inputs`.

The audit-graph effect of full retention:
- ~488 LHCM-related rows + ~248 three-generation rows + many fermion-
  touching lanes' downstream descendants would reclassify from
  `bounded_theorem` (with staggered-Dirac as admitted-context) to
  `positive_theorem` upstream-of-staggered-Dirac.
- The g_bare = 1 normalization (formerly axiom A4) inherits this
  closure for the gauge sector's coupling derivation chain.

## What this synthesis closes

- Substeps 1-4 of the staggered-Dirac realization gate are
  individually addressed (substeps 1-3 positive, substep 4 bounded
  with admitted-context)
- A single canonical-parent synthesis theorem packages the full
  derivation chain
- Replacement target for the open-gate parent identified

## What this synthesis does NOT close

- The S2 re-audit (independent audit lane work; chirality-aware
  upstream repair has fixed the dependency, audit pending)
- The AC admitted-context upgrade (research target — either as new
  structural primitive or as direct framework-derived DHR
  correspondence)
- The g_bare = 1 normalization gate (formerly A4; separate campaign)
- SM-fermion taste-vertex assignment for hypercharge identification
  (Block 05 of the bridge-gap-new-physics-20260506 campaign's open
  question; this synthesis enables but does not close it)

## Cross-references

### Substep deliverables (this campaign)
- Block 01 forcing-gap map: [`STAGGERED_DIRAC_FORCING_GAP_MAP_NOTE_2026-05-07.md`](STAGGERED_DIRAC_FORCING_GAP_MAP_NOTE_2026-05-07.md)
- Block 02 Grassmann forcing: [`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md)
- Block 03 K-S phase forcing: [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md)
- Block 04 BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Block 05 physical-species bridge: [`STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md)

### Replaces
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md) — open-gate parent identity (to be retired upon synthesis ratification)

### Foundational primitives
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) — A1+A2 retained
- [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) — per-site dim 2 retained
- [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) — Cl(3) per-site uniqueness chirality-aware
- [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md) — spin-statistics S2 (load-bearing for Block 02)

### Standard methodology references
- Kawamoto, N. & Smit, J. (1981). Nucl. Phys. B192, 100 — staggered fermion construction
- Berezin, F. (1966) — finite Grassmann calculus
- Haag, R. & Kastler, D. (1964) — local algebraic quantum field theory
- Doplicher, S., Haag, R. & Roberts, J. E. (1971-1974) — DHR superselection
- Streater, R. F. & Wightman, A. S. (1964) — spin-statistics in QFT

## Status

```yaml
actual_current_surface_status: branch-local synthesis theorem (bounded support)
target_claim_type: bounded_theorem
conditional_surface_status: |
  Conditional on:
   (a) Block 02 substep-1 forcing (S2 re-audit pending);
   (b) Block 03 substep-2 forcing (positive, chained);
   (c) Block 04 substep-3 forcing (positive, chained);
   (d) Block 05 substep-4 bridge (bounded with AC admitted-context);
   (e) Standard math machinery + retained primitive stack.
hypothetical_axiom_status: null
admitted_observation_status: |
  AC (Hilbert/no-proper-quotient semantics) admitted-context per
  GENERATION_AXIOM_BOUNDARY_NOTE. Standard math machinery (Lie-algebra
  rep theory, Schur orthogonality, BZ-corner analysis, Kawamoto-Smit
  construction, bipartite-graph parity, Pauli algebra, finite Grassmann
  calculus, bosonic Fock construction, HK + DHR) all admitted as
  standard machinery in narrow non-derivation roles.
claim_type_reason: |
  Synthesis of Blocks 02-05 (substeps 1-4 of the staggered-Dirac
  realization gate) into a single canonical-parent theorem. Substeps
  1-3 positive theorems; substep 4 bounded with admitted-context AC.
  Net synthesis tier is bounded support theorem. Promotion to retained
  positive_theorem requires S2 re-audit + AC upgrade.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The staggered-Dirac realization gate ITSELF (parent open-gate STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03), via packaging substeps 1-4 |
| V2 | New derivation? | Single canonical-parent synthesis theorem packaging Blocks 02-05 into one closure chain. Replacement target for open-gate parent. |
| V3 | Audit lane could complete from existing primitives? | Pieces (Blocks 02-05) just landed in this campaign; audit lane could not have packaged this synthesis without those substep theorems. |
| V4 | Marginal content non-trivial? | Yes — closes a gate that was open since 2026-05-03 axiom-reset. High-blast-radius (every fermion lane). |
| V5 | One-step variant? | No — synthesis is a different content type (canonical-parent meta-theorem) from the substep theorems. |

**PASS V1-V5.** However, per the volume cap (5 PRs/24h on goal-
specific target), this synthesis is committed but PR opening is
deferred to a future campaign.
