# Staggered-Dirac Realization — Forcing-Gap Map (Block 01)

**Date:** 2026-05-07
**Type:** scoping / forcing-gap audit
**Claim type:** open_gate audit
**Status:** scoping note auditing the existing in-flight pieces of the
staggered-Dirac realization derivation chain. Maps which substeps
(1)-(4) of the open gate are already retained and which have explicit
forcing gaps requiring closure. Not a derivation; provides the
roadmap for Blocks 02-06 of this campaign.
**Authority role:** branch-local scoping note for the
staggered-dirac-realization-gate-20260507 physics-loop campaign.
Does not set audit verdict; provides closure roadmap.
**Loop:** staggered-dirac-realization-gate-20260507 (Block 01)
**Branch:** physics-loop/staggered-dirac-realization-gate-block01-20260507
**Parent open-gate:** [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)

## Goal

Per the parent open-gate note, closing the staggered-Dirac realization
gate requires forcing four substeps from A1 (Cl(3) local algebra) +
A2 (Z³ substrate):

1. **Grassmann fermion realization** (vs admitted as independent axiom)
2. **Staggered-Dirac kinetic structure** on Z³ (vs admitted)
3. **BZ-corner doubler structure** (8 corners → 1+1+3+3 by Hamming weight)
4. **Physical-species reading** of hw=1 triplet as three SM matter generations

This note audits each substep, identifies which retained pieces cover
it, and names the precise remaining forcing gap.

## Substep 1: Grassmann fermion realization

### What's retained

[`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md)
(S2) — KEY RESULT.

Statement (paraphrased): if matter generators in the partition (1) are
replaced by *commuting* (bosonic) creation/annihilation operators on
the same staggered Dirac–Wilson `M`, the resulting canonical second-
quantisation gives an *infinite-dimensional* per-site Hilbert space
(bosonic Fock tower), which is incompatible with A1: the local
algebra Cl(3) is finite-dimensional, with minimal complex spinor
module of dim 2 (per `CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02`).
Hence the matter measure CANNOT be bosonic; only the Grassmann
implementation, with `χ_x² = 0` and per-site Hilbert space of
dimension 2 per Grassmann pair, is compatible with A1.

### Status

**Effectively closed in principle, packaging gap remains.**

The spin-statistics theorem provides the forcing argument. However:
- The note is current support tier ("awaiting re-audit after upstream
  repair")
- It cites Cl(3) per-site uniqueness via the chirality-aware repair
  (2026-05-03), which depends on `CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02`
  (retained 2026-05-02)
- The dependency chain is consistent post-repair, but the note has
  not been re-audited to retained-tier

### Block 02 task

Package the spin-statistics S2 argument as the explicit substep-1
forcing theorem for the staggered-Dirac realization gate. Two
deliverables:
1. Re-state S2 specifically as "A1+A2 + finite Cl(3) dim 2 → matter
   measure must be Grassmann (forcing, not compatibility)"
2. Verify the Cl(3) per-site uniqueness dependency post-repair

## Substep 2: Staggered-Dirac kinetic structure / Kawamoto-Smit phases

### What's retained

- `frontier_generation_rooting_undefined.py` — proves no proper
  Cl(3)-preserving taste projection on the irreducible C^8 surface
  (no-rooting theorem, three independent obstructions)
- [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md)
  — fermion parity F = (−1)^{Q̂_total} = ⊗_x σ_{3,x} provides the global
  Z_2 grading
- [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
  — exact BZ-corner / taste-cube bridge
- [`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`](S3_TASTE_CUBE_DECOMPOSITION_NOTE.md)
  — full taste-cube C^8 ~= 4 A_1 + 2 E under S_3 permutations of taste indices

### What's NOT retained

- A FORCING argument from A1+A2 + retained primitives → specific
  Kawamoto-Smit phases η_1=1, η_2(n)=(−1)^{n_1}, η_3(n)=(−1)^{n_1+n_2}
- A FORCING argument from the local Pauli realization on each Cl(3)
  site to the specific staggered hopping structure on Z³ links

The Kawamoto-Smit phases are currently established as ONE consistent
realization (per the no-rooting irreducibility on C^8), but the
forcing from A1+A2 to that specific realization is missing.

### Open question

Standard staggered-fermion theory derives Kawamoto-Smit phases from
requiring the kinetic operator anticommute with the **sublattice
parity** ε(x) := (−1)^{x_1+x_2+x_3}. This is a GEOMETRIC Z_2 grading
on Z³, distinct from the operator-level Fermion parity F retained in
`FERMION_PARITY_Z2_GRADING_THEOREM`.

The forcing chain candidate:
- Geometric ε(x) is forced from A2 + Z³ structure (admissible standard
  math: bipartite-graph parity on Z³)
- {ε, M_KS} = 0 chirality anticommutation is forced from Cl(3) chirality
  central pseudoscalar `ω = γ₁γ₂γ₃` per-site assignment to ε(x) (link)
- Solving {ε, M_KS} = 0 + Cl(3) per-site Pauli realization + Z³
  link structure → unique η_μ(n) up to gauge

### Block 03 task

Derive (or sharply bound) the Kawamoto-Smit phase forcing from this
chain. Two attack routes:

**R2.A (primary):** chirality-anticommutation `{ε, M_KS} = 0` reduces to
a finite linear-algebra problem on the four sublattices labeled by
(n_1, n_2 mod 2). Solve for η_μ(n) up to gauge.

**R2.B (alternative):** start from BZ-corner output (1+1+3+3) and
work backwards (consistency check, not forcing).

## Substep 3: BZ-corner three-generation forcing

### What's retained

- `scripts/frontier_generation_fermi_point.py` — Spectral / orbit
  structure: exact `1 + 1 + 3 + 3` corner structure on the BZ corners
  of staggered Z³ APBC
- [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  — exact M_3(C) algebra on retained hw=1 triplet (translations T_x,
  T_y, T_z with characters diag(−1,+1,+1) etc + C_3[111] cycle generate
  full M_3(C))
- [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
  — no proper exact quotient of M_3(C) on hw=1 (narrowed)
- [`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`](S3_TASTE_CUBE_DECOMPOSITION_NOTE.md)
  — full taste-cube decomposition under S_3

### What's NOT retained

- A FORCING argument that the staggered-Dirac kinetic structure on Z³
  + Cl(3) chirality grading FORCES the BZ-corner labeling by Hamming
  weight (1+1+3+3)
- A forcing argument that the hw=1 triplet specifically corresponds
  to the SU(3)-color triplet vs. some other 3-dim structure

### Status

**Substantially retained at the algebraic / observable level.** The
1+1+3+3 corner structure is computed on the retained surface (counting
fact on `{0, π}^3`). The hw=1 M_3(C) algebra and no-proper-quotient
are retained. What's missing is the FORCING from A1+A2 + Block 03's
Kawamoto-Smit forcing → the 1+1+3+3 specific labeling.

### Block 04 task

Package the forcing argument: A1+A2 + Kawamoto-Smit (Block 03 output)
+ S_3 taste decomposition + chirality grading → unique 1+1+3+3 BZ
corner structure with hw=1 = three-generation triplet.

## Substep 4: Physical-species bridge

### What's retained

- [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
  — substrate-level physical-lattice reading on the accepted
  Hilbert/locality/info surface (narrowed two-invariant rigidity)
- [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
  — no proper quotient on hw=1
- [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
  — A11 RP: transfer matrix + OS reconstruction (Hilbert-space surface)
- [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
  — Lieb-Robinson: locality structure
- [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md)
  — fermion-number Q̂ on H_phys

### What's NOT retained

- The bridge from "exact observable separation + no-proper-quotient
  closure" to "physically distinct species sectors of the accepted
  theory"
- This step is OUT-OF-SCOPE in `GENERATION_AXIOM_BOUNDARY_NOTE.md`
  (admitted-context)

### Block 05 task

Package the observable-descent + no-proper-quotient + RP A11 +
Lieb-Robinson + lattice Noether into a single closure step that
upgrades the algebraic three-generation from "observable separation"
to "physical species." Honest scope: this may not fully close, in
which case identify the precise remaining gap as a clean axiom-
addition target.

## Forcing-gap map summary

| Substep | Retained primitives | Forcing argument status | Block target |
|---|---|---|---|
| 1. Grassmann | Cl(3) per-site dim 2; Spin-statistics S2 | EFFECTIVELY CLOSED — needs packaging | Block 02 |
| 2. Kawamoto-Smit | No-rooting irred; Fermion parity Z_2; S_3 taste decomp; site-phase cube intertwiner | OPEN — needs explicit chirality-anticommutation derivation | Block 03 |
| 3. BZ-corner 1+1+3+3 | Spectral 1+1+3+3; M_3(C) on hw=1; no-proper-quotient | SUBSTANTIALLY RETAINED — needs forcing-from-Block-03 packaging | Block 04 |
| 4. Physical species | Physical-lattice necessity; observable theorem; RP A11; Lieb-Robinson; lattice Noether | OPEN with admitted-context — may need new structural primitive | Block 05 |

## Estimated closure probability

| Block | Closure probability |
|---|---|
| Block 02 (substep 1 packaging) | HIGH — pieces all retained, just packaging |
| Block 03 (substep 2 phase forcing) | MEDIUM — finite linear-algebra problem, may have multi-parameter family |
| Block 04 (substep 3 BZ-corner packaging) | HIGH — pieces retained, just packaging |
| Block 05 (substep 4 species bridge) | LOW-MEDIUM — admitted-context gap, may need new structural input |
| Block 06 (canonical parent synthesis) | HIGH if Blocks 02-05 close |

**Overall campaign probability of full gate closure: MEDIUM** —
hinges on Block 03 (Kawamoto-Smit forcing) and Block 05 (physical-
species bridge). If both close, the gate closes; if either has an
honest obstruction, the campaign produces a sharper open-gate note.

## Status

```yaml
actual_current_surface_status: scoping / forcing-gap audit
target_claim_type: open_gate audit
conditional_surface_status: |
  Conditional on:
   (a) the cited retained primitives being correctly identified;
   (b) the four substeps as stated in the parent open-gate note
       being exhaustive (not missing a hidden substep);
   (c) the forcing-gap classifications being correct (further
       blocks may reveal additional gaps).
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  This is a scoping note auditing the existing pieces of the staggered-
  Dirac realization derivation chain. It does not derive any new
  result; it maps the four substeps to retained primitives and
  identifies remaining gaps. Useful as the campaign roadmap and
  audit-lane reference.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- Maps the four substeps of the staggered-Dirac realization gate to
  retained primitives
- Identifies which substeps are EFFECTIVELY closed (substep 1) vs
  OPEN (substep 2 forcing) vs SUBSTANTIALLY retained (substep 3
  packaging) vs ADMITTED-CONTEXT (substep 4 species bridge)
- Provides the campaign roadmap for Blocks 02-06

## What this does NOT close

- Any of the four substeps (Block 01 is scoping, not derivation)
- The gate itself (closure requires Blocks 02-06)

## Cross-references

- Parent open-gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Loop pack: `.claude/science/physics-loops/staggered-dirac-realization-gate-20260507/`
