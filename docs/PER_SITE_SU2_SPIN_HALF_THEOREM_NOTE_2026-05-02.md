# Per-Site Cl(3) Hilbert Carries the Unique j = 1/2 Spin Irrep of su(2)

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** on every framework site x ∈ Z^3, the per-site Hilbert space H_x
(uniquely the Pauli C² module by `axiom_first_cl3_per_site_uniqueness`) carries
exactly the j = 1/2 irreducible representation of the spin Lie algebra su(2).
The spin generators S_i := σ_i / 2 satisfy [S_i, S_j] = i ε_{ijk} S_k with
total Casimir S² = (3/4) I = j(j+1) I for j = 1/2, and S_z eigenvalues lie
in {-1/2, +1/2}. There is no other half-integer spin representation supported
on a per-site Hilbert.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r5-20260502`
**Cycle:** 3 (Block 3)
**Branch:** `physics-loop/positive-only-r5-block03-per-site-spin-half-20260502`
**Runner:** `scripts/per_site_su2_spin_half_check.py`
**Log:** `outputs/per_site_su2_spin_half_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
  — `effective_status: retained`. Provides:
  - **(U2)** Per-site Hilbert is the unique 2-dim faithful irreducible
    Cl(3) representation, unitarily equivalent to Pauli `(σ_1, σ_2, σ_3)`.

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Bivector → spin generator identification.** In any Clifford algebra
  Cl(p, q), the bivector subspace ∧²V closes under commutator into the spin
  Lie algebra so(p, q); for Cl(3, 0) this is so(3) ≅ su(2). This is the
  standard spin-group construction (Lawson–Michelsohn, *Spin Geometry*).
- **Casimir-element ↔ Lie-irrep label correspondence.** Standard fact: for
  a finite-dim irreducible representation of su(2), the quadratic Casimir
  S² acts as j(j+1) I, and 2j+1 = dim of the irrep.

Both are pure mathematical / Lie-algebraic facts; no admitted physics
conventions.

## Statement

Let H_x ≅ C² be the per-site Hilbert space at any site x ∈ Z^3 of the
framework, with Cl(3) generators acting as Pauli matrices `γ_i ↦ σ_i`
(retained per-site uniqueness). Define the spin generators

```text
    S_i  :=  σ_i / 2,        i ∈ {1, 2, 3}.                                 (1)
```

Then:

**(C1) su(2) Lie algebra.** S_i satisfy

```text
    [S_i, S_j]  =  i ε_{ijk} S_k                                             (2)
```

i.e. they are a basis for a su(2) Lie algebra acting on H_x.

**(C2) Casimir = 3/4 ⇒ j = 1/2.** The quadratic Casimir

```text
    S²  :=  S_1²  +  S_2²  +  S_3²  =  (3/4) I_2                            (3)
```

equals (3/4) · I uniformly on H_x. Identifying S² = j(j+1) I yields
j(j+1) = 3/4, hence j = 1/2.

**(C3) S_z spectrum = {±1/2}.** The diagonal generator S_3 has eigenvalues
±1/2 = ±j, matching the standard m ∈ {-j, ..., +j} ladder for j = 1/2.

**(C4) Irreducibility.** H_x is an irreducible su(2) module: there is no
nonzero proper invariant subspace. (Established by [S_1, S_2] having rank
= dim H_x = 2.)

**(C5) Uniqueness on per-site Hilbert.** Combining (C1)–(C4) with (U2):
the per-site Cl(3) Hilbert H_x is exactly the unique 2-dim spin-1/2 irrep
of su(2). Per-site matter content cannot carry any other spin label.

## Proof

### Step 1 — Pauli rep is the per-site Hilbert (cited)

By the retained per-site uniqueness theorem (U2), H_x ≅ C² with
γ_i ↦ σ_i. All subsequent statements are computations in this Pauli basis.

### Step 2 — su(2) Lie algebra (C1)

Direct computation of `[σ_i, σ_j]` in the Pauli basis gives `2i ε_{ijk} σ_k`.
Hence with `S_i = σ_i / 2`:

```text
    [S_i, S_j]  =  (1/4) [σ_i, σ_j]  =  (1/4) · 2i ε_{ijk} σ_k
                =  (i / 2) ε_{ijk} σ_k  =  i ε_{ijk} (σ_k / 2)
                =  i ε_{ijk} S_k                                             (4)
```

This is the defining commutation relation of su(2) — establishing (C1).

### Step 3 — Casimir computation (C2)

Each `σ_i² = I` (square of Pauli matrix is identity), so

```text
    S_i²  =  σ_i² / 4  =  I / 4                                              (5)
```

and

```text
    S²  =  S_1²  +  S_2²  +  S_3²  =  3 · (I / 4)  =  (3/4) I.              (6)
```

By the Casimir-Lie-irrep correspondence: for su(2) acting irreducibly with
Casimir = j(j+1), here j(j+1) = 3/4. Solving the quadratic
`j² + j - 3/4 = 0` gives `j ∈ {1/2, -3/2}`. Spin labels are non-negative,
so j = 1/2 — establishing (C2).

### Step 4 — S_z spectrum (C3)

`S_3 = σ_3 / 2 = diag(1/2, -1/2)` has eigenvalues exactly `±1/2`. These
are the m = ±j ladder rungs for j = 1/2 — establishing (C3).

### Step 5 — Irreducibility (C4)

If H_x had a nonzero proper invariant subspace V, then dim V = 1, and V
would be a common eigenline of every S_i. But [S_1, S_2] = i S_3 ≠ 0, so
no such common eigenline exists. Equivalently, the rank of [S_1, S_2] = i S_3
is 2 (full rank), so the only invariant subspaces of the action are 0 and
all of H_x — establishing (C4).

### Step 6 — Uniqueness statement (C5)

By (C1)–(C4), H_x carries an irreducible su(2) representation of dimension
2 with j = 1/2. The j = 1/2 irrep is unique up to unitary equivalence
(Schur, applied to the unique 2-dim irrep of su(2)). Per-site Hilbert is
fully exhausted by this representation; there is no room for additional
spin content at the site level. ∎

## Hypothesis set used

- `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained):
  provides Pauli per-site rep.
- Bivector spin-generator construction (mathematical, admitted-context).
- Casimir ↔ irrep label correspondence (Lie-algebra, admitted-context).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained per-site uniqueness theorem.

## Corollaries

C1. **Framework matter content is spin-1/2 at every site.** This pins down
the spin label of any "elementary fermion" carried by a single Cl(3) site
on Z^3: it must be exactly j = 1/2.

C2. **Higher-spin matter requires extending the local algebra.** A spin-1
or spin-3/2 elementary fermion would need a per-site Hilbert of dimension
≥ 3 (i.e. 2j+1 ≥ 3). But per-site Hilbert is exactly 2-dim by (U2).
Therefore no higher-spin elementary fermion fits in the framework's per-site
Cl(3) module — any higher-spin content must come from composite (multi-site)
states or from extending Cl(3) at the algebra level (which would change A_min).

C3. **Spin-statistics input.** The "matter is spin-1/2" load-bearing input
to `axiom_first_spin_statistics_theorem_note_2026-04-29` is now derived as
a per-site representation-theoretic fact, not a stipulation.

C4. **Spin-orbit coupling structure.** Any rotation generator R_i acting on
multi-site states decomposes as orbital part L_i (spatial Z^3) + spin part
σ_i / 2 per site. The spin contribution is universal and j = 1/2.

C5. **No spin-0 elementary scalar at site level.** A per-site Hilbert
carrying j = 0 would have to be 1-dimensional (2j+1 = 1). But per-site
Hilbert is 2-dim. Therefore there is no fundamental scalar matter at a
single Cl(3) site; all spin-0 content must be multi-particle composites.

## Honest status

Positive theorem on the framework's per-site Hilbert space, derived
from a single retained one-hop dependency by elementary Lie algebra and
finite-dimensional representation-theoretic computation.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Per-site Cl(3) Hilbert ≅ unique j=1/2 irrep of su(2); no other per-site spin content possible."
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29 (retained)
admitted_context_inputs:
  - bivector → spin generator identification (Clifford → spin Lie algebra)
  - Casimir ↔ irrep label correspondence (Schur / standard Lie algebra)
```
