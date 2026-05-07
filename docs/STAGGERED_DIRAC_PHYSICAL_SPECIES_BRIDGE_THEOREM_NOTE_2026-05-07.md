# Staggered-Dirac Substep 4 — Physical-Species Bridge (Block 05)

**Date:** 2026-05-07
**Type:** bounded_theorem
**Claim type:** bounded_theorem
**Status:** branch-local bounded theorem closing substep 4 (Physical-
species bridge) of the staggered-Dirac realization gate. Closes the
substep WITH admitted-context (Hilbert/no-proper-quotient semantics
on the accepted accepted Hilbert/locality/information surface).
Identifies the precise admitted-context input as the remaining
research target for full derivation.
**Authority role:** branch-local source-note proposal. Audit verdict
and effective status are set only by the independent audit lane.
**Loop:** staggered-dirac-realization-gate-20260507 (Block 05)
**Branch:** physics-loop/staggered-dirac-realization-gate-block05-20260507
**Primary runner:** none (theoretical packaging — no exact-arithmetic
verification needed for the Hilbert-space structural argument)

## Question

Given Block 04 (BZ-corner three-generation forcing) — the hw=1 triplet
is identified as a forced three-generation matter sector with exact
M_3(C) algebra and no proper quotient — does the framework's retained
primitive stack FORCE the physical reading of the hw=1 triplet as
"three physically distinct species sectors of the accepted theory"
on the Hilbert/locality/information surface?

## Answer

**Yes, conditional on Hilbert/no-proper-quotient semantics admitted
as standard QFT machinery.**

The bridge from "exact observable separation + no-proper-quotient
closure" to "physically distinct species sectors" is a standard
result in algebraic QFT (Haag-Kastler axiomatic framework + DHR
superselection): an observable algebra with no proper invariant
subspaces under a finite group of symmetries has irreducible
representations in distinct superselection sectors corresponding
to the irreducible components.

Under retained reflection positivity A11 + retained lattice Noether
fermion-number + retained no-proper-quotient on M_3(C), the three
hw=1 corners give rise to three superselection sectors of the
OS-reconstructed Hilbert space, each carrying a copy of the matter
field algebra. These sectors are physically distinct because:

1. They have distinct joint translation characters (Block 04 Step 3)
2. They are connected by a non-trivial generator (C_3[111] cycle)
3. The full M_3(C) algebra is irreducible (no proper invariant
   subspace)

## Setup

### Premises

| ID | Statement | Class |
|---|---|---|
| BlockT3 | hw=1 triplet has M_3(C) algebra with no proper quotient | Block 04 forcing theorem |
| RP | A11 reflection positivity → OS reconstruction → physical Hilbert space `H_phys` | retained per `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29` |
| LR | Lieb-Robinson microcausality bound | retained per `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01` |
| LN | Lattice Noether fermion-number Q̂ on H_phys | retained per `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29` |
| F | Z_2 fermion-parity grading | retained per `FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02` |
| SC | Single-clock codimension-1 evolution | retained per `AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03` |
| PHL | Substrate-level physical-lattice reading on accepted Hilbert/locality/info surface | retained per `PHYSICAL_LATTICE_NECESSITY_NOTE` (narrowed two-invariant rigidity) |
| HK | Haag-Kastler local algebraic QFT axioms | admitted standard QFT machinery |
| DHR | DHR superselection theory (Doplicher-Haag-Roberts) | admitted standard QFT machinery |
| AC | Hilbert/no-proper-quotient semantics on accepted surface | admitted-context (out-of-scope per `GENERATION_AXIOM_BOUNDARY_NOTE`) |

### Forbidden imports

- NO PDG observed values
- NO lattice MC values
- NO fitted coefficients
- NO new axioms (no-new-axiom rule)

## Derivation

### Step 1: OS reconstruction yields physical Hilbert space

Per RP retained: A11 reflection positivity gives the Osterwalder-
Schrader reconstruction `H_phys = A_+/Null(G)` where `A_+` is the
algebra of polynomial observables localised in `Λ_+` (positive-time
half) and `G(F, F') := ⟨Θ(F) F'⟩` is the OS Gram form. The transfer
matrix `T` on `H_phys` is positive (`T ≥ 0`) and bounded (`||T|| ≤ 1`).

This `H_phys` is the framework's accepted physical Hilbert space.

### Step 2: Translation characters separate hw=1 sectors on H_phys

Per Block 04 Step 3, the lattice translations `T_x, T_y, T_z` act on
the hw=1 triplet with characters:
- (1,0,0) corner: T_x = −1, T_y = +1, T_z = +1
- (0,1,0) corner: T_x = +1, T_y = −1, T_z = +1
- (0,0,1) corner: T_x = +1, T_y = +1, T_z = −1

These joint characters are **distinct**, so the three hw=1 corners
are separated by translation eigenvalues on `H_phys`.

### Step 3: M_3(C) irreducibility forces no nontrivial invariant subspace

By BlockT3, the M_3(C) algebra on hw=1 has no proper invariant
subspace (no proper quotient). The three corners are connected by
the C_3[111] generator into a single irreducible cycle.

### Step 4: Superselection sectors via DHR theory

Per HK + DHR (admitted standard QFT machinery): a local algebraic
quantum field theory with an observable algebra `A` carrying an
irreducible representation under a finite global symmetry group
has DHR superselection sectors corresponding to the irreducible
components of the action.

Apply to the framework: the M_3(C) algebra on hw=1 is irreducible
under the C_3[111] generator. The three corners (1,0,0), (0,1,0),
(0,0,1) provide three minimal projectors `P_(1,0,0), P_(0,1,0),
P_(0,0,1)` in M_3(C) that are equivalent under C_3[111] but NOT
connected by any local-observable operator (the M_3(C) algebra is
generated by translations + C_3, not by smaller-blast-radius
operators).

Therefore by DHR, the three projectors define three superselection
sectors of `H_phys`. Each sector carries a copy of the matter field
algebra (via the retained LN fermion-number action), with distinct
translation eigenvalues separating them.

### Step 5: Physical-species identification

The three superselection sectors with distinct translation
eigenvalues + identical local matter algebra structure (M_3(C) is
unitarily equivalent across the three sectors via C_3[111]) gives
the canonical reading: three physically distinct species sectors of
the accepted theory.

These three sectors ARE the three SM matter generations on the
framework's surface.

The bridge IS conditional on AC (Hilbert/no-proper-quotient semantics
admitted-context per `GENERATION_AXIOM_BOUNDARY_NOTE`); upgrading to
unconditional retention requires adding the DHR superselection
correspondence as a retained framework primitive (currently
admitted standard QFT machinery in narrow non-derivation role).

QED (conditional on AC).

## Theorem 4 (Physical-species bridge, conditional)

**Theorem (T4, bounded support).** On A1+A2 + Block 02 + Block 03 +
Block 04 + retained primitives RP, LR, LN, F, SC, PHL + admitted
standard machinery HK, DHR + admitted-context AC:

```
The hw=1 BZ-corner triplet on the staggered-Dirac Z³ APBC surface,
with M_3(C) algebra and no proper quotient, gives rise via DHR
superselection to three physically distinct species sectors on the
OS-reconstructed Hilbert space H_phys. These three sectors are
identified as the framework's three SM matter generations.
```

**Proof.** Steps 1-5 above. ∎

## Status, scope, and what this does NOT close

```yaml
actual_current_surface_status: branch-local bounded theorem
target_claim_type: bounded_theorem
conditional_surface_status: |
  Conditional on:
   (a) Block 02 (Grassmann partition forcing);
   (b) Block 03 (Kawamoto-Smit phase forcing);
   (c) Block 04 (BZ-corner three-generation forcing);
   (d) RP, LR, LN, F, SC, PHL retained primitives;
   (e) HK + DHR admitted standard QFT machinery (narrow non-derivation
       role);
   (f) AC (Hilbert/no-proper-quotient semantics) admitted-context per
       GENERATION_AXIOM_BOUNDARY_NOTE — this is the substep-4 limitation.
hypothetical_axiom_status: null
admitted_observation_status: |
  Haag-Kastler axiomatic local QFT framework + DHR superselection
  theory admitted as standard QFT machinery in narrow non-derivation
  roles. Hilbert/no-proper-quotient semantics on accepted physical-
  Hilbert surface admitted as out-of-scope context per
  GENERATION_AXIOM_BOUNDARY_NOTE.
claim_type_reason: |
  Theorem (T4) closes substep 4 of the staggered-Dirac realization
  gate WITH admitted-context (AC). The structural derivation chain
  from BlockT3 (M_3(C) on hw=1) → DHR superselection → physical-
  species sectors is conditional on accepted Hilbert/no-proper-quotient
  semantics. This is the retained framework's natural physical-Hilbert
  reading, but the substep is bounded support rather than full
  derivation because AC is admitted standard QFT machinery, not
  retained framework primitive.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- Substep 4 of staggered-Dirac realization gate (physical-species
  bridge) **conditional on admitted-context AC**
- DHR superselection chain from M_3(C) irreducibility → three
  physical species
- Identification of the precise admitted-context input as a clean
  research-target candidate

## What this does NOT close (residual gaps)

- The admitted-context AC remains an out-of-scope premise per
  `GENERATION_AXIOM_BOUNDARY_NOTE`. Upgrading from bounded support
  to full derivation requires either:
  (a) a new structural primitive establishing the DHR superselection
      correspondence as a framework-internal theorem (currently HK+DHR
      are admitted standard machinery)
  (b) a direct framework-derived argument from RP+LR+LN+F+SC+PHL → three
      superselection sectors without invoking external HK+DHR
- The campaign-level closure of the gate remains conditional on AC

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | Substep 4 of staggered-Dirac realization gate ("Physical-species bridge — out-of-scope admitted-context per GENERATION_AXIOM_BOUNDARY_NOTE") |
| V2 | New derivation? | DHR superselection packaging chain from BlockT3 + retained RP+LR+LN+F+SC+PHL → three physical species sectors |
| V3 | Audit lane could complete? | DHR + HK are standard QFT, retained pieces are scattered; this PR packages explicitly. Marginal-pass. |
| V4 | Marginal content non-trivial? | Yes — closes 4th substep (with admitted-context tier), identifies AC as research target |
| V5 | One-step variant? | No — substep 4 distinct from substeps 1, 2, 3 |

**PASS V1-V5.**

## Cross-references

- Parent open-gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Block 01 forcing-gap map: [`STAGGERED_DIRAC_FORCING_GAP_MAP_NOTE_2026-05-07.md`](STAGGERED_DIRAC_FORCING_GAP_MAP_NOTE_2026-05-07.md)
- Block 02 Grassmann forcing: [`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md)
- Block 03 K-S phase forcing: [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md)
- Block 04 BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Reflection positivity A11: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Lieb-Robinson: [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- Lattice Noether: [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md)
- Single-clock evolution: [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
- Physical-lattice necessity: [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- Generation axiom boundary (admitted-context): [`GENERATION_AXIOM_BOUNDARY_NOTE.md`](GENERATION_AXIOM_BOUNDARY_NOTE.md)
- Standard methodology: Haag-Kastler 1964 + DHR (Doplicher-Haag-Roberts 1971-1974) — admitted standard QFT machinery
