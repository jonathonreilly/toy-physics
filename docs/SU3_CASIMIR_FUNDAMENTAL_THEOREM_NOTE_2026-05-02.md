# SU(3) Quadratic Casimir on Color Fundamental Equals 4/3

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the framework's SU(3)_c color group (acting on the retained
3-dim symmetric base subspace via Gell-Mann generators T^a = λ^a / 2) has
quadratic Casimir C_2 := Σ_a T^a T^a = (4/3) · I_3 on the fundamental "3"
representation. Equivalently, the universal "color charge squared" of a
color-triplet quark is 4/3, in normalization Tr[T^a T^b] = (1/2) δ^{ab}.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r6-20260502`
**Cycle:** 3 (Block 3)
**Branch:** `physics-loop/positive-only-r6-block03-su3-casimir-fundamental-20260502`
**Runner:** `scripts/su3_casimir_fundamental_check.py`
**Log:** `outputs/su3_casimir_fundamental_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  — `effective_status: retained`. Provides:
  - SU(3)_c acting on 3-dim symmetric base subspace as fundamental rep
  - Gell-Mann generators T^a = λ^a / 2 (Hermitian)
  - Trace orthonormality Tr[T^a T^b] = (1/2) δ^{ab}

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Schur's lemma.** On any irreducible representation of a Lie algebra,
  any operator commuting with all generators is a scalar multiple of the
  identity. Standard finite-dim Lie-algebra fact.
- **SU(N) Casimir formula C_2(N) = (N² - 1) / (2N).** Standard SU(N)
  representation-theoretic computation: for the fundamental of SU(N) in
  normalization Tr[T^a T^b] = (1/2) δ^{ab}, the quadratic Casimir is
  (N² - 1) / (2N). This evaluates to 4/3 at N = 3.

Both are pure mathematical facts; no admitted physics conventions.

## Statement

Let SU(3)_c be the framework's color group acting on the retained 3-dim
symmetric base subspace V_3 (cl3_color_automorphism_theorem) via the eight
Gell-Mann generators T^a = λ^a / 2 satisfying

```text
    Tr[T^a T^b]  =  (1/2) δ^{ab}.                                          (1)
```

Define the quadratic Casimir

```text
    C_2  :=  Σ_{a=1}^{8} T^a T^a.                                          (2)
```

Then on V_3 (the fundamental "3" representation):

**(K1) C_2 is central.** [C_2, T^b] = 0 for every Lie-algebra generator T^b.

**(K2) C_2 is a scalar multiple of identity.** By Schur's lemma applied
to the irreducible 3, there exists c_2(3) ∈ R such that
C_2 = c_2(3) · I_3.

**(K3) c_2(3) = 4/3.** Direct computation in the Gell-Mann basis gives

```text
    c_2(3)  =  (N² - 1) / (2N)  =  (9 - 1) / 6  =  4 / 3.                 (3)
```

**(K4) Universal "color charge squared" of color triplet.** The number 4/3
is the universal coefficient appearing in:
- one-gluon-exchange potential between color-triplet quarks
- one-loop quark self-energy color factor
- color factor for any color-singlet bilinear of two triplets

## Proof

### Step 1 — SU(3)_c on V_3 (cited)

By cl3_color_automorphism_theorem (retained), SU(3)_c acts on V_3 as
the fundamental "3" representation, with Gell-Mann generators T^a = λ^a / 2
in the standard basis (1).

### Step 2 — Centrality (K1)

By the defining su(3) Lie algebra [T^a, T^b] = i f^{abc} T^c, applying
to the Casimir:

```text
    [C_2, T^b]  =  Σ_a [T^a T^a, T^b]
                =  Σ_a (T^a [T^a, T^b]  +  [T^a, T^b] T^a)
                =  Σ_a (i f^{abc} T^a T^c  +  i f^{abc} T^c T^a)
                =  i f^{abc} (T^a T^c  +  T^c T^a).                       (4)
```

The structure constants f^{abc} are totally antisymmetric in (a,b,c)
(standard SU(N) property), and T^a T^c + T^c T^a is symmetric in (a,c).
Antisymmetric × symmetric summed over (a, c) vanishes. Hence
[C_2, T^b] = 0 for every b — establishing (K1).

### Step 3 — Schur ⇒ scalar (K2)

By Schur's lemma applied to the irreducible representation V_3:
any operator commuting with every generator of the Lie algebra acts as
a scalar multiple of the identity on V_3. Hence C_2 = c_2(3) · I_3 for
some c_2(3) ∈ R — establishing (K2).

### Step 4 — Casimir value (K3)

Compute c_2(3) directly:

```text
    Tr[C_2]  =  Σ_a Tr[T^a T^a]  =  Σ_a (1/2) δ^{aa}  =  Σ_{a=1}^{8} (1/2)
            =  4.                                                          (5)
```

But also Tr[c_2(3) · I_3] = c_2(3) · 3. Equating:

```text
    c_2(3) · 3  =  4    ⇒    c_2(3)  =  4 / 3.                            (6)
```

This matches the standard SU(N) formula c_2(N) = (N² - 1) / (2N) at N = 3:
(9 - 1) / 6 = 4/3 — establishing (K3).

### Step 5 — Universal color charge (K4)

In any one-gluon-exchange diagram between two color-triplet quarks, the
color factor at the vertices is Σ_a T^a T^a applied to the quark line,
which is C_2 = 4/3. This is the universal "color charge squared" coefficient
appearing in:
- the static QQ̄ potential V(r) = -(4/3) α_s / r  (Coulomb-like)
- one-loop quark self-energy ∝ (4/3) g_s²
- any color-singlet bilinear projection involving two triplets

The number 4/3 is therefore the universal multiplicative color factor of
the framework's color-triplet matter content. ∎

## Hypothesis set used

- `cl3_color_automorphism_theorem` (retained): provides SU(3)_c on V_3
  with Gell-Mann normalization (1).
- Schur's lemma (mathematical, admitted-context).
- SU(N) Casimir formula (mathematical, admitted-context).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained color automorphism theorem.

## Corollaries

C1. **Universal color charge of quark = 4/3.** Every quark mode in the
framework carries the same color charge squared 4/3. This is independent
of flavor, generation, electric charge, weak isospin, or any other
quantum number — it is purely a color group-theoretic invariant.

C2. **One-gluon-exchange Coulomb coefficient.** The static color-singlet
qq̄ potential at lowest order is V(r) = -(4/3) α_s / r, where the 4/3
factor comes directly from C_2(3). Any framework computation of bound-state
quarkonium spectra inherits this coefficient.

C3. **One-loop quark mass renormalization color factor.** The fermion
self-energy diagram with one gluon exchange gives a multiplicative
color factor C_2(3) = 4/3 in the renormalization, contributing to the
running of quark masses.

C4. **Color factor for cross sections.** Any 2 → 2 quark scattering
cross section computation involves products / sums of T^a T^b traces,
all of which can be reduced to combinations of C_2(3) = 4/3 and the
adjoint Casimir C_2(8) = 3 (separate companion).

C5. **Confinement-relevant color factor.** The "string tension" coefficient
in lattice QCD calculations of the static potential picks up the same 4/3
from the color triplet structure, even though the long-distance physics
is genuinely non-perturbative.

## Honest status

Positive theorem on the framework's SU(3)_c color algebra acting on the
fundamental triplet, derived from a single retained one-hop dependency
by elementary Lie-algebra computation in the Gell-Mann basis. The runner
exhibits Hermitian generators, trace orthonormality, su(3) Lie algebra
closure, Schur scalar property of C_2, exact value 4/3, and agreement
with the SU(N) formula at N = 3.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "SU(3)_c quadratic Casimir on fundamental V_3 = 4/3 in standard Gell-Mann normalization."
upstream_dependencies:
  - cl3_color_automorphism_theorem (retained)
admitted_context_inputs:
  - Schur's lemma (Lie-algebra representation theory)
  - SU(N) Casimir formula C_2(N) = (N² - 1) / (2N) (standard)
```
