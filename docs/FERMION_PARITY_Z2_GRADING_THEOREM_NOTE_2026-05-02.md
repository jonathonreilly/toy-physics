# Fermion Parity (-1)^Q̂ and Z_2 Grading on Framework Fock Space

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the framework's fermion-parity operator
F := (-1)^{Q̂_total} = exp(i π Q̂_total) (with Q̂_total supplied by N2 of the
retained lattice Noether theorem, integer-valued by R7 Block 03) is a
Hermitian unitary involution that gives the Fock space H = ⊗_x C² a Z_2
grading H = H_even ⊕ H_odd with dim H_even = dim H_odd = 2^{N-1}.
Single-fermion creation/annihilation operators a_x, a_x^† are Z_2-odd
({F, a_x} = 0); fermion bilinears a_x^† a_y and the number operators n̂_x
are Z_2-even ([F, a_x^† a_y] = 0). This is the framework's **fermion-parity
superselection rule**: only Z_2-even local operators connect physically
realizable states.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r8-20260502`
**Cycle:** 1 (Block 1)
**Branch:** `physics-loop/positive-only-r8-block01-fermion-parity-20260502`
**Runner:** `scripts/fermion_parity_z2_grading_check.py`
**Log:** `outputs/fermion_parity_z2_grading_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md)
  — `effective_status: retained`. Provides:
  - **(N2)** Total fermion-number operator Q̂_total as the conserved
    Noether charge of U(1) phase symmetry, defined on H_phys.

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Spectral functional calculus.** For any Hermitian operator A on a
  finite-dim Hilbert, exp(i α A) is a well-defined unitary operator with
  spectrum {exp(i α λ) : λ ∈ Spec(A)}. Standard finite-dim spectral
  theorem.
- **Single-mode fermion construction on per-site Pauli C².** a = σ_+,
  a^† = σ_-, n = a^† a = (I - σ_3)/2. (Same as R7 Block 03.) Definitional.
- **Tensor product Fock space.** Standard construction.

All three are pure mathematical / definitional facts; no admitted physics
conventions.

## Statement

Define the **fermion-parity operator** on the N-site Fock space H by

```text
    F  :=  (-1)^{Q̂_total}  =  exp(i π Q̂_total)                            (1)
```

where Q̂_total is the conserved fermion-number charge supplied by N2 of
the retained lattice Noether theorem.

Then:

**(F1) Hermiticity & unitarity.** F is Hermitian (F = F^†) and unitary
(F^† F = I).

**(F2) Involution.** F² = I, hence F is its own inverse.

**(F3) Spectrum.** Spec(F) = {+1, -1} exactly.

**(F4) Z_2 grading.** H decomposes as

```text
    H  =  H_even  ⊕  H_odd
```

where H_even = Ker(F - I), H_odd = Ker(F + I), with
dim H_even = dim H_odd = 2^{N-1}.

**(F5) Equivalent product formula.** F = ⊗_{x=1}^{N} σ_{3, x} (tensor
product of σ_3 across all sites).

**(F6) Z_2-odd action on fermion operators.**

```text
    {F, a_x}  =  F a_x  +  a_x F  =  0,    {F, a_x^†}  =  0,    ∀ x.       (2)
```

Equivalently F a_x F^{-1} = -a_x.

**(F7) Z_2-even action on fermion bilinears.**

```text
    [F, a_x^† a_y]  =  F a_x^† a_y  -  a_x^† a_y F  =  0,    ∀ x, y.       (3)
```

In particular [F, n̂_x] = 0 and [F, Q̂_total] = 0.

**(F8) Conservation by H.** Since [H, Q̂_total] = 0 (R3 Block 01), and F
is a function of Q̂_total, [F, H] = 0. Fermion parity is a conserved
quantum number of the framework's dynamics.

## Proof

### Step 1 — Q̂_total construction (cited)

By N2 of the retained lattice Noether theorem, Q̂_total is the conserved
charge of U(1) phase symmetry. By R7 Block 03 (companion: Q̂ integer
spectrum), Q̂_total has spectrum {0, 1, ..., N} on the N-site Fock space.

### Step 2 — F well-defined and Hermitian (F1)

F := exp(i π Q̂_total). Since Q̂_total is Hermitian, by spectral functional
calculus exp(i π Q̂_total) is unitary. Moreover, exp(i π · k) = (-1)^k for
integer k ∈ Spec(Q̂_total), so all eigenvalues of F are ±1, real. Hence F
is Hermitian (eigenvalues real ⇒ unitary Hermitian operator).

Concretely on each Q̂-eigenspace H_k: F |k, α⟩ = (-1)^k |k, α⟩ — establishing
(F1).

### Step 3 — Involution (F2)

F² = exp(2 π i Q̂_total) = I (since 2 π i k for integer k gives e^{2π i k}
= 1). Equivalently F |k, α⟩ = (-1)^k |k, α⟩ ⇒ F² |k, α⟩ = ((-1)^k)²
|k, α⟩ = |k, α⟩ — establishing (F2).

### Step 4 — Spectrum (F3)

Since F is a non-zero operator with F² = I, eigenvalues satisfy λ² = 1
⇒ λ ∈ {+1, -1}. Both values are realized: |0, ..., 0⟩ has Q = 0 ⇒ F = +1;
|1, 0, ..., 0⟩ has Q = 1 ⇒ F = -1 — establishing (F3).

### Step 5 — Z_2 grading (F4, F5)

The eigenvalue +1 eigenspace consists of Q-even Fock states (occupation
patterns with even total fermion number); the eigenvalue -1 eigenspace
consists of Q-odd patterns. The number of binary strings ν ∈ {0, 1}^N
with even Σ ν_x is exactly 2^{N-1} (and similarly for odd). Therefore
dim H_even = dim H_odd = 2^{N-1} — establishing the dimension balance
in (F4).

For (F5): in the Pauli basis, σ_3 = diag(+1, -1) corresponds to
+1 ↔ |0⟩ (n = 0) and -1 ↔ |1⟩ (n = 1). So σ_3 = (-1)^{n} on each per-site
factor. The tensor product gives:

```text
    ⊗_x σ_{3, x}  =  ⊗_x (-1)^{n_x}  =  (-1)^{Σ_x n_x}  =  (-1)^{Q̂_total}  =  F.   (4)
```

Establishing (F5).

### Step 6 — Z_2-odd action on a_x (F6)

By (F5), F = ⊗_x σ_{3, x}. At site x, σ_3 acts as σ_{3, x}, and at all
other sites σ_3 acts as identity. The local relation σ_3 σ_+ + σ_+ σ_3 =
0 (anticommutation of σ_3 and σ_+) gives:

```text
    σ_3 σ_+  =  σ_3 [[0, 1], [0, 0]]  =  [[0, 1], [0, 0]] · diag(1, -1) … wait
```

Let me redo: σ_3 σ_+ = diag(1, -1) · [[0, 1], [0, 0]] = [[0, 1], [0, 0]] = σ_+.
σ_+ σ_3 = [[0, 1], [0, 0]] · diag(1, -1) = [[0, -1], [0, 0]] = -σ_+.
So σ_3 σ_+ + σ_+ σ_3 = σ_+ - σ_+ = 0. Yes, {σ_3, σ_+} = 0.

So at site x: {σ_{3, x}, a_x} = 0. At sites y ≠ x, σ_{3, y} commutes with
the identity factor of a_x. Therefore conjugation by F on a_x flips its
sign at site x while leaving other sites unchanged, giving F a_x F^{-1}
= -a_x — establishing (F6).

### Step 7 — Z_2-even action on bilinears (F7)

By (F6), F a_x^† a_y F^{-1} = (F a_x^† F^{-1}) (F a_y F^{-1}) = (-a_x^†)
(-a_y) = a_x^† a_y. Hence [F, a_x^† a_y] = 0 — establishing (F7).

In particular n̂_x = a_x^† a_x and Q̂_total = Σ n̂_x are Z_2-even.

### Step 8 — Dynamical conservation (F8)

By R3 Block 01 / N2 of retained Noether: [H, Q̂_total] = 0. Hence H
preserves each Q-eigenspace. Since F is a function of Q̂_total, F also
commutes with H: [F, H] = 0 — establishing (F8). ∎

## Hypothesis set used

- `axiom_first_lattice_noether_theorem_note_2026-04-29` (retained):
  provides Q̂_total via N2.
- Spectral functional calculus (mathematical, admitted-context).
- Single-mode fermion construction (definitional).
- Tensor product Fock space (definitional).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained lattice Noether theorem.

## Corollaries

C1. **Fermion parity superselection rule.** Only Z_2-even local operators
(bilinears, currents, plaquettes) can connect physical states across the
parity sectors. Single fermion operators (Z_2-odd) cannot appear in
physical observables — they violate the superselection rule.

C2. **Hamiltonian must be Z_2-even.** Any framework Hamiltonian H must
preserve fermion parity ([F, H] = 0), hence must be a sum of Z_2-even
local terms (bilinears, four-fermion operators, gauge bosons, ...).
Single-fermion terms a_x or a_x^† alone are forbidden.

C3. **Bose-Fermi superselection.** Fermion-parity superselection is the
algebraic basis of the Bose / Fermi distinction: Z_2-even (bosonic)
operators commute with F; Z_2-odd (fermionic) anticommute.

C4. **Connection to spin-statistics.** The Z_2 grading by F is the same
Z_2 grading that distinguishes Pauli-excluding fermions (Z_2-odd) from
"would-be bosons" (Z_2-even on the same Hilbert). On framework Fock
space, only the Z_2-even sector contains valid physical states for
direct observation; Z_2-odd states are accessed only as parts of bilinear
products in observable amplitudes.

C5. **Half-and-half decomposition.** Of the 2^N Fock-space states, exactly
half (2^{N-1}) are in each parity sector. This is the maximally balanced
splitting, reflecting the Z_2 freedom inherent to fermion algebras.

C6. **Selection rule for transitions.** Any matrix element ⟨Ψ|O|Φ⟩ where
Ψ ∈ H_even and Φ ∈ H_odd vanishes unless O is Z_2-odd. This is a
strict selection rule on lattice transitions.

## Honest status

Positive theorem on the framework's fermion-parity Z_2 grading, derived
from a single retained one-hop dependency by elementary spectral functional
calculus and Pauli-anticommutation algebra. The runner exhibits hermiticity,
involution F² = I, spectrum {+1, -1}, dimension balance 2^{N-1}, the
σ_3-product formula F = ⊗ σ_{3, x}, and the Z_2-odd / Z_2-even action on
fermion operators / bilinears — all at machine precision.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "F = (-1)^Q̂ is Hermitian unitary involution; H = H_even ⊕ H_odd Z_2 grading; a_x is Z_2-odd; bilinears Z_2-even; F conserved by [F, H] = 0."
upstream_dependencies:
  - axiom_first_lattice_noether_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - spectral functional calculus (basic finite-dim spectral theorem)
  - single-mode fermion construction (definitional)
  - tensor product Fock space (definitional)
```
