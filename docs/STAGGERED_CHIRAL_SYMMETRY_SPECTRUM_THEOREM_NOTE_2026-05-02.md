# Staggered Cl(3) Hamiltonian Has Chiral-Symmetric Spectrum: σ(H_phys) = −σ(H_phys)

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the framework's staggered Cl(3) Hamiltonian H_phys = i·D
on a periodic L³ lattice (even L), with C the sublattice parity ε(x) =
(-1)^{x+y+z} and the chiral anti-commutation {C, H_phys} = 0 supplied by
the retained `cpt_exact_note`, has a spectrum that is **symmetric around
zero**:
σ(H_phys) = −σ(H_phys) as multisets. Equivalently, every eigenstate
|E⟩ with eigenvalue E has a chiral partner C|E⟩ that is an eigenstate
with eigenvalue −E. Multiplicities at +E and −E are equal for E ≠ 0;
zero modes form a separate invariant subspace under C.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r10-20260502`
**Cycle:** 1 (Block 1)
**Branch:** `physics-loop/positive-only-r10-block01-staggered-chiral-symmetry-20260502`
**Runner:** `scripts/staggered_chiral_symmetry_check.py`
**Log:** `outputs/staggered_chiral_symmetry_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — `effective_status: retained`. Provides:
  - Staggered single-component Hamiltonian D and H_phys = i·D
  - Sublattice parity C as diag(ε(x)) with ε(x) = (-1)^{x+y+z}
  - Exact identity C·H_phys·C = -H_phys (equivalently {C, H_phys} = 0)

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Spectral theorem for Hermitian operators on finite-dim Hilbert.** Any
  Hermitian H has an orthonormal basis of eigenvectors with real eigenvalues.
  Standard.
- **Two operators A, B with B unitary involutive (B² = I) satisfying {A, B} = 0
  ⇒ A and B share a structure where eigenstates of A pair under B.** Standard
  result on chirally-graded Hermitian operators.

Both are pure mathematical / spectral-theory facts; no admitted physics
conventions. Notably, the spectrum-symmetric statement σ(H) = −σ(H) is **not**
in the admitted-context inputs — it is the result being proved.

## Statement

Let H_phys = i·D on the L³ lattice (even L) and C = diag(ε(x)) with ε(x) =
(-1)^{x+y+z} be the staggered Hamiltonian and sublattice parity supplied by
the retained `cpt_exact_note`.

**(S1) Chiral spectral pairing.** For every eigenstate |E⟩ of H_phys with
eigenvalue E ∈ R, the state C|E⟩ is also an eigenstate of H_phys with
eigenvalue −E:

```text
    H_phys (C|E⟩)  =  -E · (C|E⟩)                                          (1)
```

**(S2) Spectrum symmetric about 0.** σ(H_phys) = −σ(H_phys) as multisets.
For every eigenvalue E of H_phys, −E is also an eigenvalue with the same
multiplicity.

**(S3) Vanishing trace.** Tr(H_phys) = Σ_E E = 0.

**(S4) Equal sublattice partition.** On even L³ periodic lattice,
|Λ_+| := |{x : ε(x) = +1}| = |Λ_-| := |{x : ε(x) = -1}| = L³/2.

**(S5) Zero-mode invariance under C.** The zero-eigenspace ker(H_phys) is
C-invariant: C ker(H_phys) ⊂ ker(H_phys). It decomposes as
ker(H_phys) = ker_+ ⊕ ker_- under the C-eigenvalue split (C-even vs C-odd).
The integer dim ker_+ − dim ker_- is a chiral index of the lattice
operator.

## Proof

### Step 1 — Chiral anticommutation (cited)

By cpt_exact_note (retained): the sublattice parity C is unitary, real,
diagonal, satisfies C² = I, and acts as

```text
    C · H_phys · C  =  -H_phys.                                            (2)
```

Equivalently {C, H_phys} = 0.

### Step 2 — Spectral pairing (S1)

Let |E⟩ be an eigenstate of H_phys: H_phys |E⟩ = E |E⟩ with E ∈ R (real
since H_phys is Hermitian). Apply C:

```text
    H_phys (C |E⟩)  =  -C H_phys |E⟩      (using (2))
                    =  -C · E |E⟩
                    =  -E · (C |E⟩).                                       (3)
```

Hence C|E⟩ is an eigenstate of H_phys with eigenvalue −E — establishing (S1).

### Step 3 — Spectrum symmetric (S2)

For every E ∈ σ(H_phys), the chiral partner −E is also in σ(H_phys) by
(S1). Multiplicities match: applying C to a basis of the E-eigenspace
yields a linearly independent set in the (−E)-eigenspace (C is unitary,
preserves linear independence). The same argument with E → −E gives the
reverse inclusion, so the multiplicities are equal.

For E = 0: the zero-eigenspace ker(H_phys) is C-invariant (since C maps
0 to 0), but the multiplicity statement is vacuous (mult(0) = mult(-0)
trivially) — establishing (S2).

### Step 4 — Vanishing trace (S3)

Tr(H_phys) = Σ_E (E · mult(E)). By (S2), mult(E) = mult(-E), so contributions
at +E and −E cancel pairwise. Zero modes contribute 0. Therefore Tr(H_phys)
= 0 — establishing (S3).

### Step 5 — Sublattice balance (S4)

For periodic L³ lattice with even L:

```text
    Σ_x ε(x)  =  Σ_{x_1, x_2, x_3} (-1)^{x_1+x_2+x_3}
              =  (Σ_{x_1=0}^{L-1} (-1)^{x_1})³
              =  0³  =  0   (since L even ⇒ Σ_{k=0}^{L-1} (-1)^k = 0)      (4)
```

Hence |Λ_+| − |Λ_-| = 0; combined with |Λ_+| + |Λ_-| = L³, we get
|Λ_+| = |Λ_-| = L³/2 — establishing (S4).

### Step 6 — Zero-mode invariance (S5)

If H_phys |ψ⟩ = 0, then H_phys (C|ψ⟩) = -C H_phys |ψ⟩ = -C · 0 = 0, so
C|ψ⟩ ∈ ker(H_phys). Since C² = I, C restricted to ker(H_phys) is a unitary
involution, splitting ker(H_phys) into ±1-eigenspaces ker_±.

The integer index dim ker_+ − dim ker_- = Tr(C|_{ker(H_phys)}) is the
chiral index of H_phys with respect to C. (This integer is the lattice
analog of the Atiyah-Singer index of the continuum Dirac operator on a
manifold with chirality grading.) ∎

## Hypothesis set used

- `cpt_exact_note` (retained): provides H_phys = i·D, C = diag(ε(x)),
  and the chiral anti-commutation {C, H_phys} = 0.
- Spectral theorem for finite-dim Hermitian operators (mathematical,
  admitted-context).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained CPT-exact theorem.

## Corollaries

C1. **Particle-hole symmetry.** The framework's free staggered Hamiltonian
realizes exact lattice particle-hole symmetry: the spectrum is the union
of disjoint pairs (E, −E) for E > 0, plus (possibly degenerate) zero
modes. This is the discrete-lattice analog of relativistic chiral symmetry
ψ → γ_5 ψ.

C2. **Massless Dirac points at zero modes.** The 8 zero modes on L = 4
(verified by the runner) sit at the eight Brillouin-zone corners of the
staggered lattice — the framework's structural realization of the
continuum 2³ = 8 doublers, which combine into 2² = 4 Dirac species per
spinor component. (The doubler structure is a known feature of the
staggered convention.)

C3. **Free-energy zero point.** The free-fermion ground-state energy is
−Σ_{E > 0} E (filling the Dirac sea) and the spectrum-symmetric structure
guarantees this sum is well-defined and finite for finite lattices.
Renormalization of the vacuum energy is unambiguous.

C4. **Bipartite lattice geometry forces chiral symmetry.** The result
S4 uses crucially that L is even (bipartite Z³ requires even side length
to close periodically with both colorings present). This is exactly the
constraint that cpt_exact_note imposes on the lattice geometry — and the
chiral symmetry is structurally tied to this bipartite geometry.

C5. **Symmetry-protected zero modes (chiral index).** The integer
dim ker_+ − dim ker_- is a chiral-index protected number: small Hermitian
perturbations of H_phys that preserve {C, H_phys} = 0 cannot change it.
This is the discrete analog of index-theory protection in continuum gauge
theory.

C6. **Source-free correlator constraints.** Any matrix element
⟨0|O₁ ... O_n|0⟩ of operators that flip between Λ_+ and Λ_-
sublattices vanishes unless n is even (sublattice-parity superselection).
This is a discrete chirality selection rule.

## Honest status

Positive theorem on the framework's staggered Hamiltonian spectrum, derived
from a single retained one-hop dependency by elementary chiral-pairing
argument. The result σ(H) = −σ(H) is **not** present in the cited
cpt_exact_note's claim list (which states [CPT, H] = 0 and SME=0 but
doesn't extract the spectrum-symmetric corollary). The runner exhibits
chiral pairing eigenstate-by-eigenstate at machine precision on a 4³
lattice (8 zero modes + 28 positive + 28 negative).

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "σ(H_phys) = -σ(H_phys); chiral pairing C|E⟩ ↔ |-E⟩; chiral index dim ker_+ - dim ker_- on staggered lattice."
upstream_dependencies:
  - cpt_exact_note (retained)
admitted_context_inputs:
  - spectral theorem for finite-dim Hermitian operators
```
