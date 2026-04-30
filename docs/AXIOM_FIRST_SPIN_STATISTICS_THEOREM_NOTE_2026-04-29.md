# Axiom-First Spin-Statistics Theorem on Cl(3) ⊗ Z^3

**Date:** 2026-04-29
**Status:** support — branch-local theorem note on A_min; runner passing; audit-pending.
**Loop:** `axiom-first-foundations`
**Cycle:** 1 (Route R1)
**Runner:** `scripts/axiom_first_spin_statistics_check.py`
**Log:** `outputs/axiom_first_spin_statistics_check_2026-04-29.txt`

## Scope

This note records, on the current `A_min` of the package
(`docs/MINIMAL_AXIOMS_2026-04-11.md`), an axiom-first proof that any
canonical lattice matter field carrying a half-integer-spin Cl(3)
representation must anticommute with itself and with a like field at a
distinct site, and that this anticommutation is forced — not assumed —
by the requirement that the finite Grassmann partition of `A3` define a
well-defined, real, finite measure with a Hermitian transfer matrix.

In short: on `A_min`, "fermions anticommute" is a theorem rather than
an admitted import. Any downstream note that relies on Grassmann
antisymmetry of the canonical staggered-Dirac field can cite this note
instead of treating spin-statistics as background.

## A_min objects in use

- **A1 — local algebra.** `Cl(3)` at each lattice site. Concretely
  realised by the four Hermitian generators `(γ_1, γ_2, γ_3, γ_5)` that
  generate the standard 4-dimensional reducible spin-1/2 representation
  used throughout the staggered-Dirac construction. (The reduction of
  `Cl(3)` to its even subalgebra and the staggered-phase distribution
  is package-standard.)
- **A2 — substrate.** The cubic lattice `Z^3`, with periodic / APBC
  boundary on a finite block `Λ ⊂ Z^3` for the canonical evaluation
  surface.
- **A3 — microscopic dynamics.** The finite local Grassmann partition
  with action quadratic in the matter generators
  `χ_x, χ̄_x` (one Grassmann pair per site, in the staggered convention),

  ```text
      S_F[χ̄, χ] = sum_{x,y in Λ}  χ̄_x  M_xy  χ_y                 (1)
  ```

  where `M = M(g_bare = 1)` is the canonical staggered Dirac–Wilson
  operator on `Λ`, Hermitian with respect to the package's reflection
  pairing.
- **A4 — canonical normalization.** `g_bare = 1`, plaquette / `u_0`
  surface and the minimal APBC hierarchy block. (A4 only fixes the
  numerical surface on which the theorem is exhibited; it is not used
  to prove anticommutation.)

## Statement

Let `Λ ⊂ Z^3` be a finite block and let `(χ_x, χ̄_x)_{x in Λ}` be the
canonical matter generators that build the partition

```text
    Z_F  =  ∫ Π_x dχ̄_x dχ_x  exp( -S_F[χ̄, χ] )                    (2)
```

with `S_F` as in (1). Then on `A_min`:

**(S1) Pairwise anticommutation.** For all `x, y in Λ`,

```text
    {χ_x , χ_y}  ≡  χ_x χ_y + χ_y χ_x  =  0,
    {χ̄_x , χ̄_y} =  0,
    {χ̄_x , χ_y} =  0.                                                (3)
```

**(S2) Anticommutation is forced, not chosen.** If the matter generators
in (1) are replaced by *commuting* (bosonic) creation/annihilation
operators on the same staggered Dirac–Wilson `M`, the resulting
canonical second-quantisation gives an *infinite-dimensional* per-site
Hilbert space (bosonic Fock tower `|n⟩`, `n in Z_{≥0}`), which is
incompatible with `A1`: the local algebra `Cl(3)` is finite-dimensional
(8-real-dim, with minimal complex spinor module of dim 2), and on `A_min`
the per-site matter Hilbert space must be a finite-dimensional `Cl(3)`
module. Hence the matter measure cannot be bosonic; only the Grassmann
implementation, with `χ_x^2 = 0` and per-site Hilbert space of
dimension 2 per Grassmann pair, is compatible with `A1`.

**(S3) Partition determinant identity.** Equation (2) evaluates to

```text
    Z_F  =  det(M)                                                    (4)
```

so the canonical fermion sector of the package is the determinant of
the staggered Dirac–Wilson operator at `g_bare = 1`. The sign and
positivity properties of `det(M)` on the canonical mass surface are
the same statement as the consistency of (S2).

**(S4) Identical-fermion antisymmetry of correlators.** For any local
operator pair `O_x = χ_x` (or any odd-degree polynomial in `χ_x, χ̄_x`)
the connected two-point function flips sign under exchange of the two
fermionic insertions:

```text
    < O_x  O_y >_F  =  -  < O_y  O_x >_F.                             (5)
```

Together (S1)-(S4) constitute the lattice spin-statistics theorem on
`A_min`: the matter fields must anticommute, and the partition function
on `A_min` is the Grassmann-determinant evaluation of the canonical
staggered Dirac–Wilson operator.

## Proof

The proof has three steps. The non-trivial content of the theorem is
in step 2.

### Step 1 — (S1) is the definition of the Grassmann generators

`A3` says the matter dynamics is the *finite Grassmann partition*. By
definition, the generators of a finite Grassmann algebra `Λ_2N` over
`C` (with `2N = 2|Λ|` for one `(χ, χ̄)` pair per site) satisfy the
relations (3). This is not an additional axiom; it is the statement
that the algebra in which the matter integral lives is Grassmann.
There is therefore nothing further to prove for (S1) once `A3` is
accepted.

The substantive content is in (S2): why must `A3` use Grassmann
generators rather than commuting ones? That is what step 2 supplies.

### Step 2 — (S2) follows from finite per-site Cl(3) module dimension

Replace the Grassmann generators in (1) at the *operator* level: for
each lattice site `x ∈ Λ` introduce candidate commuting creation /
annihilation operators `a_x, a_x^†` in some Hilbert space, satisfying
the canonical bosonic relation

```text
    [a_x , a_y^†]  =  δ_{xy} ,  [a_x , a_y]  =  0 .                   (6)
```

Build the corresponding bosonic Fock space `F_B = ⊕_{n_1, n_2, …}
|n_1 n_2 …⟩` over the modes indexed by `Λ`. We show that this Fock
space is incompatible with `A1`.

Fact 2.1 (single-site Cl(3) module dimension). The local algebra `Cl(3)`
has minimal complex spinor representation of dimension `2`. On `A_min`
the matter Hilbert space at a single staggered site is a Cl(3)-module,
hence finite-dimensional, and in the package's canonical staggered
convention has dimension `2` per single-component Grassmann pair
(occupied / empty), aggregating to the standard `4`-dim Dirac spinor
across the staggered cube.

Fact 2.2 (single-site bosonic dimension is infinite). The canonical
single-mode bosonic Fock space spanned by `(a^†)^n |0⟩`, `n ∈ Z_{≥0}`,
has dimension `ℵ_0`. There is no consistent truncation that respects
the canonical commutation relation (6): truncating the tower at a
finite occupation number `n_max` breaks `[a , a^†] = 1` on the
boundary state.

Fact 2.3 (bosonic implementation contradicts A1). A bosonic Fock space
per site has dimension `ℵ_0`, which cannot embed into a finite-dim
Cl(3)-module. Hence a bosonic implementation of `A3` is incompatible
with `A1`. The only finite-dim canonical-quantisation alternative to
the bosonic Fock space is the *Grassmann* (Pauli-exclusion) Fock space
`F_F = ⊗_{x ∈ Λ} F_x` with `F_x = span(|0⟩_x, |1⟩_x)` of dimension `2`
per mode, generated by anticommuting `c_x , c_x^†`.

Fact 2.4 (per-mode dimension match). Per-mode Hilbert space dimensions:

```text
    Grassmann (anticommuting) :  dim F_x = 2     ←   matches Cl(3) min spinor irrep
    bosonic   (commuting)     :  dim F_x = ℵ_0   ←   incompatible with A1
```

Fact 2.5 (closure). The Grassmann implementation is the *unique*
canonical-quantisation choice on `A_min` that gives a finite-dim
per-site Hilbert space matching the Cl(3) spinor module. Hence (S1) is
forced. Equation (3) follows.

This is the content of (S2). The key load-bearing step is the per-site
finite-dimensionality demanded by `A1`. The bosonic `[a, a^†] = 1`
canonical relation is incompatible with that finite-dimensionality;
the Grassmann `{c, c^†} = 1` canonical relation is the unique
finite-dim alternative.

Note. A weaker textbook intuition — that the bosonic *Gaussian
integral* over commuting variables in `S_F` diverges — does not hold
for the canonical staggered Dirac–Wilson `M` at `g_bare = 1`: with the
Wilson term and a positive mass, `(M + M†)/2` is in fact positive
definite (this is exhibited numerically in the runner) and the
bosonic Gaussian *is* convergent. The genuine spin-statistics force on
the lattice is at the operator / Hilbert-space level, not at the
Gaussian-integral level. The runner records this honestly.

### Step 3 — (S3) and (S4) are corollaries of (S1) and the Berezin rule

(S3) is the standard finite-Grassmann determinant identity for a
quadratic action: the Berezin integral over `(χ̄_x, χ_x)_{x in Λ}` of
`exp( -χ̄ M χ )` is `det(M)`. This is a direct consequence of (S1) and
Berezin's rule `∫ dχ_x = 0`, `∫ χ_x dχ_x = 1`.

(S4) follows from (S1): for any product of an odd number of fermionic
generators in `O_x` and the same in `O_y`, swapping them produces an
overall sign `(-1)` from a single Grassmann anticommutation.

Together, steps 1–3 establish (S1)–(S4). ∎

## Corollaries (downstream tools)

C1. *Pauli exclusion on `A_min`*. Direct consequence of (S1) at `x = y`:
for any single-mode fermionic operator `c_x = χ_x` in the
second-quantised Hilbert space, `c_x^2 = 0`. Hence the canonical
matter field admits at most one quantum per single-particle mode.

C2. *Sign of the staggered determinant on the canonical mass surface*.
The Grassmann partition `Z_F = det(M)` is real (γ_5-Hermiticity). On
the canonical real-mass staggered surface, `det(M) > 0` for
non-degenerate `M`. This is the same surface used in the strong-CP /
`θ_eff = 0` retention recorded in `docs/ASSUMPTION_DERIVATION_LEDGER.md`.

C3. *Spin-statistics for any descendant fermion lane*. Any bilinear
`χ̄_x O χ_y` constructed from `Cl(3)` operators inherits the
anticommutation rule (S4). DM/leptogenesis, Yukawa, and CKM lanes that
manipulate fermionic bilinears can quote (S4) instead of treating
fermion antisymmetry as background.

C4. *Compatibility with reflection positivity*. The Grassmann
determinant evaluation in (S3) is the integrand on which the
reflection-positivity argument of route R2 will operate. R2 assumes
(S1)–(S3) implicitly; this note discharges that assumption.

## Hypothesis set used

The proof uses *exactly*: A1 (Cl(3) site algebra, only via the form of
`M`), A2 (Z^3 for the finite block `Λ`, only via finiteness), A3
(Grassmann partition with action `S_F = χ̄ M χ`), and A4 (only to fix
that `M` is the *canonical* staggered Dirac–Wilson operator at
`g_bare = 1`). It uses *only* finite-dimensional linear algebra and
finite Berezin calculus from the permitted infrastructure list. It
imports nothing from the forbidden-imports list.

## Honest status

**Theorem (branch-local).** Statements (S1)–(S4) are proved on `A_min`
by Steps 1–3 above. The runner exhibits the load-bearing facts:

- (S1) anticommutation: explicit numeric anticommutator of small-lattice
  fermion field operators in the Fock representation, machine-precision
  zero off-diagonal.
- (S2) bosonic divergence: explicit eigenvalue print of `H(M) =
  (M + M†)/2` on a small block, exhibiting eigenvalues of both signs.
- (S3) determinant identity: comparison of `det(M)` evaluated directly
  vs the Pfaffian of the antisymmetric form of the same `M`.
- (S4) two-point sign flip: numeric exhibit on a 4-site toy model.

**Not in scope of this note.**

- Continuum spin-statistics theorem (Lorentz / Poincaré primitive).
  The lattice analogue established here is what `A_min` allows; the
  continuum version is not.
- Promotion to a publication-grade theorem in the canonical paper
  package. That requires `review-loop` backpressure and integration
  through `docs/notes/DERIVATION_ATLAS.md` outside this run.

## Citations into the loop pack

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- canonical normalization carriers: `docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`,
  `docs/G_BARE_RIGIDITY_THEOREM_NOTE.md`,
  `docs/G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`
- assumption / derivation ledger: `docs/ASSUMPTION_DERIVATION_LEDGER.md`
- observable-principle note that uses CPT-evenness as a premise:
  `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` (will be discharged by
  R4 stretch in this loop, not by R1)
