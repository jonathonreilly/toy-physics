# Staggered-Dirac Direct Three-State Algebraic Support

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support for the direct three-state algebraic
surface inside a single `H_phys`. This note salvages the runner-backed
algebraic content only. It does not close the physical-species bridge,
does not assert a positive theorem, and does not identify the three
states as the framework's SM matter generations. The DHR route remains
misframed because Reeh-Schlieder + cluster decomposition are single-sector
inputs on the canonical surface, but replacing DHR with a direct algebraic
three-state calculation leaves a narrow species-identification bridge open.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** [`scripts/probe_three_states_direct_derivation.py`](../scripts/probe_three_states_direct_derivation.py)

## Question

Can the DHR-framed physical-species bridge be sharpened into a direct
three-state algebraic support statement inside the single reconstructed
physical Hilbert space, using RP-OS reconstruction, translation-character
data, and the no-proper-quotient result?

## Answer

**Partly.** The three hw=1 states are algebraically distinct states in
one `H_phys`, and the runner verifies their translation-character
separation and C_3 cyclic action. That salvages bounded algebraic support.
It does not by itself derive the physical-species / SM-generation reading.

## Setup

### Premises (A_min for substep 4 reformulated)

| ID | Statement | Class |
|---|---|---|
| BlockT3 | hw=1 BZ-corner triplet has M_3(C) algebra (translations + C_3[111]) with distinct joint translation characters | retained per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) and bounded support in [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| NQ | M_3(C) on hw=1 has no proper exact quotient | retained per [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md) |
| RP | A11 RP + OS reconstruction -> physical Hilbert space `H_phys` with unique vacuum `Omega` | retained per [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| RS | Reeh-Schlieder cyclicity: `A(O) Omega` dense in `H_phys` for any open region `O` | retained per [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md) |
| CD | Cluster decomposition + spectrum condition -> unique vacuum, no superselection sectors on canonical surface | retained per [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md) |
| LR | Lieb-Robinson microcausality | retained per [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |
| LN | Lattice Noether fermion-number Q̂ on H_phys | retained per [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md) |
| SC | Single-clock codimension-1 evolution (unitary one-parameter group) | retained per [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md) |

### Forbidden imports

- NO PDG observed values
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms
- **NO HK + DHR appeal (review identified this vocabulary as misframed)**

## Derivation

### Step 1: H_phys is a single Hilbert space with unique vacuum

By RP + OS reconstruction (retained): the framework's physical Hilbert
space `H_phys` is the GNS-like reconstruction from the OS positive
sesquilinear form, with global cyclic vacuum |Ω⟩.

By RS (retained): for any open region `O ⊂ Λ`, `A(O)|Ω⟩` is dense in
`H_phys`. The vacuum is cyclic AND separating for `A(O)'`.

By CD (retained): connected correlators decay exponentially; the
vacuum is unique on the canonical surface; **NO superselection sectors
on the canonical surface**.

Combined: `H_phys` is a SINGLE Hilbert space with a UNIQUE vacuum.
There are no separate sectors disconnected from the vacuum.

### Step 2: hw=1 triplet is a 3-dimensional subspace of H_phys

By BlockT3: the hw=1 BZ
corners (1,0,0), (0,1,0), (0,0,1) are three orthogonal momentum
eigenstates within `H_phys`, with distinct simultaneous-eigenvalues
under lattice translations T_x, T_y, T_z:

```
|(1,0,0)⟩: T_x = −1, T_y = +1, T_z = +1
|(0,1,0)⟩: T_x = +1, T_y = −1, T_z = +1
|(0,0,1)⟩: T_x = +1, T_y = +1, T_z = −1
```

These are three orthogonal STATES in H_phys, spanning a 3-dim
subspace `H_hw=1 ⊂ H_phys`.

### Step 3: M_3(C) algebra acts on H_hw=1 in the GNS image

By BlockT3 + NQ: the lattice translations T_x, T_y, T_z combined with
the C_3[111] cyclic generator generate the full M_3(C) algebra on
`H_hw=1`. The C_3 action is implemented by a unitary on `H_phys` through
the lattice automorphism / GNS representation. This note does not assert
that the C_3 generator is itself a local element of `A(Λ)`.

Specifically:
- T_x, T_y, T_z are lattice translation operators in the represented
  framework dynamics
- C_3[111] is the cyclic permutation `(1,0,0) → (0,1,0) → (0,0,1) →
  (1,0,0)` — a lattice-symmetry unitary on the hw=1 subspace

Both are single-Hilbert-space operators, not charged intertwiners between
separate DHR sectors.

### Step 4: Three states are in the same superselection sector

By Step 1, `H_phys` has a single superselection sector (the vacuum
sector). All three corner states `|(1,0,0)⟩, |(0,1,0)⟩, |(0,0,1)⟩` lie
in `H_phys`, hence in the same superselection sector.

The C_3[111] unitary (per Step 3) connects them:
`C_3[111] |(1,0,0)⟩ = |(0,1,0)⟩`, etc.

Thus the three corners are three connected quantum states inside the same
represented Hilbert space, not three separate DHR sectors.

### Step 5: Spectral distinctness gives algebraic separation

The three corners have DISTINCT joint translation eigenvalues (Step 2).
By the spectral theorem on H_phys (admissible standard math), states
with distinct simultaneous eigenvalues of commuting Hermitian
operators are ORTHOGONAL.

Distinct orthogonal eigenstates with the same algebraic M_3(C) structure
and different translation labels give a sharp three-state algebraic
separation. This is the bounded content checked here.

The physical-species reading, and especially the identification with SM
matter generations, is not derived by this algebraic separation alone.

### Step 6: Non-load-bearing phenomenology comparator

In the Standard Model, matter generations are distinct flavor states that
live in one Hilbert space and are not separate DHR superselection sectors.
This is a comparator only. This note does not derive masses, W-boson
couplings, Yukawa structure, or flavor-changing dynamics.

The comparator shows why the DHR-sector framing is the wrong vocabulary,
not that the direct three-state algebra has become a physical-species
theorem.

## Theorem 4-revised (Direct three-state algebraic support)

**Bounded theorem.** On A1+A2 + the bounded Grassmann/Kawamoto-Smit/
BZ-corner support chain + RP, RS, CD, LR, LN, SC + M_3(C) on hw=1 +
no-proper-quotient:

```
The hw=1 BZ-corner triplet of the staggered-Dirac realization on Z³
APBC gives three quantum-mechanically distinct states in the
RP-OS-reconstructed physical Hilbert space H_phys, characterized by:
  (a) distinct simultaneous-eigenvalues of T_x, T_y, T_z;
  (b) connected by the C_3[111] lattice-symmetry unitary in the
      represented hw=1 surface;
  (c) carrying M_3(C) algebra structure (irreducible, no proper
      quotient);
  (d) all in the same superselection sector (the unique vacuum sector
      per Reeh-Schlieder + cluster decomposition).

The physical-species / SM-generation identification remains an open
bridge and is not part of this bounded theorem.
```

**Proof.** Steps 1-6 above. ∎

## Comparison to prior Block 05 framing

| Aspect | Block 05 (DHR-framed) | Block 02-revised (direct three-state) |
|---|---|---|
| Hilbert space structure | "Three superselection sectors of H_phys" | One H_phys, three states within |
| Key machinery | HK + DHR superselection (misframed for this surface) | RP+RS+CD single-Hilbert-space framing |
| Admitted-context | Broad DHR semantics | Narrow species-identification bridge remains open |
| Status tier | bounded theorem with broad AC | bounded theorem support with narrower open bridge |
| SM phenomenology comparator | DHR sectors are the wrong vocabulary | Single-Hilbert-space states are at least vocabulary-compatible |
| Compatibility with cited primitives | Incompatible with RS+CD single-sector framing | Compatible as algebraic support |

## Audit boundary

This note should seed as `bounded_theorem`. It does not write an audit
verdict, an effective status, or a retained-grade closure claim. It should
not be used to promote the parent realization gate until the narrow
physical-species bridge is derived and independently audited.

## What this supports

- DHR vocabulary is not the right way to express the three-state surface on
  the RS+CD single-sector canonical surface
- The direct hw=1 algebra gives three translation-character-distinct states
  inside one `H_phys`
- The remaining bridge is narrowed to physical-species identification rather
  than broad DHR/HK machinery

## What this does NOT close

- Substep 4 of the parent realization gate as a positive theorem
- The physical-species / SM-generation identification
- Any parent synthesis or publication status
- The g_bare = 1 normalization gate (formerly axiom A4) — separate
  campaign target

## Cross-references

- Parent open-gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- BZ-corner algebraic support: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- RP A11: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Reeh-Schlieder: [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md)
- Cluster decomposition: [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Three-generation no-proper-quotient: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)

## Command

```bash
python3 scripts/probe_three_states_direct_derivation.py
```

Expected output: dependency-chain consistency check for the cited premises;
verification that three corner states are pairwise orthogonal under
translation eigenvalues; verification that C_3[111] generates a 3-cycle on
hw=1; and structural verification of the three-state-in-single-H_phys
algebraic support surface.
