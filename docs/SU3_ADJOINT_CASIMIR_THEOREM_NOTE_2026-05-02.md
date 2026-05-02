# SU(3) Quadratic Casimir on Adjoint Equals N = 3

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the framework's SU(3)_c color group, in standard Gell-Mann
normalization Tr[T^a T^b] = (1/2) δ^{ab} (retained per cl3_color_automorphism),
has quadratic Casimir on the adjoint representation C_2(adj) = N = 3, where
N = 3 is the rank+1 / fundamental dimension. Equivalently, the gluon's
"color charge squared" in the framework is exactly 3.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r7-20260502`
**Cycle:** 1 (Block 1)
**Branch:** `physics-loop/positive-only-r7-block01-su3-adjoint-casimir-20260502`
**Runner:** `scripts/su3_adjoint_casimir_check.py`
**Log:** `outputs/su3_adjoint_casimir_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  — `effective_status: retained`. Provides:
  - SU(3)_c with Gell-Mann generators T^a = λ^a / 2
  - Trace orthonormality Tr[T^a T^b] = (1/2) δ^{ab}
  - Definition of f^{abc} via [T^a, T^b] = i f^{abc} T^c

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **Adjoint representation construction.** For any Lie algebra g, the
  adjoint rep ad : g → End(g) is defined by ad(X)(Y) = [X, Y]. In the
  basis T^a of g, the matrix elements are (ad(T^a))_{bc} = -i f^{abc}
  (with the conventional factor of -i so that the matrices are
  Hermitian when the basis T^a is). Standard Lie-algebra construction.
- **Schur's lemma.** On any irreducible representation of a Lie algebra,
  any operator commuting with all generators is a scalar multiple of the
  identity.

Both are pure mathematical facts; no admitted physics conventions.

## Statement

Let SU(3)_c be the framework's color group with Gell-Mann generators
T^a = λ^a / 2 in the fundamental "3" representation (cl3_color_automorphism,
retained), satisfying

```text
    [T^a, T^b]  =  i f^{abc} T^c,                                          (1)
    Tr[T^a T^b]  =  (1/2) δ^{ab}.                                          (2)
```

Define the **adjoint generators** acting on the 8-dim Lie algebra g = su(3)
by

```text
    (T^a_adj)_{bc}  :=  -i f^{abc}.                                        (3)
```

Then on the adjoint representation:

**(A1) Hermiticity.** Each T^a_adj is an 8x8 Hermitian matrix.

**(A2) su(3) Lie algebra closure.** [T^a_adj, T^b_adj] = i f^{abc} T^c_adj
(same structure constants as the fundamental).

**(A3) Trace normalization.** Tr[T^a_adj T^b_adj] = N · δ^{ab} = 3 · δ^{ab}.

**(A4) Adjoint Casimir is central.** C_2(adj) := Σ_a T^a_adj T^a_adj
satisfies [C_2(adj), T^b_adj] = 0 for every b.

**(A5) Schur scalar.** By Schur's lemma applied to the 8-dim adjoint
(irreducible for su(3)), C_2(adj) = c · I_8 for some scalar c.

**(A6) Casimir value.** c = N = 3, so

```text
    C_2(adj)  =  3 · I_8.                                                  (4)
```

**(A7) Ratio to fundamental.**

```text
    C_2(adj) / C_2(fund)  =  3 / (4/3)  =  9/4  =  2 N² / (N² - 1)         (5)
```

at N = 3, matching the standard SU(N) Casimir-ratio formula.

## Proof

### Step 1 — Color group structure (cited)

By cl3_color_automorphism_theorem (retained), SU(3)_c acts on the framework's
color triplet via Gell-Mann generators T^a = λ^a / 2 satisfying (1)–(2).

### Step 2 — Construct adjoint rep (A1, A2)

Define adjoint generators via (3). Hermiticity of T^a_adj follows from
the total antisymmetry of f^{abc}: f^{abc} = -f^{bac} = -f^{abc} only as
a complex transpose with -i factor flipped sign. Concretely:
(T^a_adj)*_{cb} = +i f^{acb} = -i f^{abc} = (T^a_adj)_{bc}, hence
(T^a_adj)^† = T^a_adj — establishing (A1).

su(3) Lie algebra closure on the adjoint is the **Jacobi identity** of
the Lie algebra applied to f^{abc}, which guarantees that
[ad(T^a), ad(T^b)] = ad([T^a, T^b]) — i.e. [T^a_adj, T^b_adj] = i f^{abc}
T^c_adj — establishing (A2).

### Step 3 — Trace normalization (A3)

Direct computation:

```text
    Tr[T^a_adj T^b_adj]  =  Σ_{c,d} (T^a_adj)_{cd} (T^b_adj)_{dc}
                        =  Σ_{c,d} (-i f^{acd}) (-i f^{bdc})
                        =  -Σ_{c,d} f^{acd} f^{bdc}
                        =  Σ_{c,d} f^{acd} f^{bcd}     (using f^{bdc} = -f^{bcd})
                        =  N δ^{ab}                                        (6)
```

The last step is the standard SU(N) identity Σ_{c,d} f^{acd} f^{bcd} =
N δ^{ab}, which can be derived from the orthogonality of f^{abc} as
structure constants in the trace-normalized basis. Numerically: for SU(3),
this evaluates to 3 δ^{ab} — establishing (A3).

### Step 4 — Centrality (A4)

By the same antisymmetric-symmetric vanishing argument as for the
fundamental Casimir (R6 Block 03):

```text
    [C_2(adj), T^b_adj]  =  Σ_a [T^a_adj T^a_adj, T^b_adj]
                        =  i f^{abc} (T^a_adj T^c_adj  +  T^c_adj T^a_adj)
```

f^{abc} is totally antisymmetric in (a, b, c); the symmetric combination
(T^a T^c + T^c T^a) is symmetric in (a, c). Antisymmetric × symmetric
summed over (a, c) vanishes — establishing (A4).

### Step 5 — Schur scalar (A5)

The adjoint representation of su(3) on its own Lie algebra is irreducible.
By Schur's lemma, the Casimir C_2(adj), commuting with every T^b_adj,
must be a scalar multiple of the 8x8 identity: C_2(adj) = c · I_8 for
some c ∈ R — establishing (A5).

### Step 6 — Casimir value (A6)

Take the trace:

```text
    Tr[C_2(adj)]  =  Σ_a Tr[T^a_adj T^a_adj]
                  =  Σ_{a=1}^{8} N · δ^{aa}
                  =  N · 8                                                 (7)
```

But also Tr[c · I_8] = 8 c. Equating:

```text
    8 c  =  8 N    ⇒    c  =  N  =  3.                                    (8)
```

Hence C_2(adj) = 3 · I_8 — establishing (A6).

### Step 7 — Ratio to fundamental (A7)

C_2(fund) = (N² - 1) / (2 N) = 4/3 (R6 Block 03) for N = 3. Therefore

```text
    C_2(adj) / C_2(fund)  =  N · 2 N / (N² - 1)  =  2 N² / (N² - 1)
                          =  2·9/8  =  9/4.                                (9)
```

This matches the standard SU(N) Casimir-ratio formula — establishing (A7). ∎

## Hypothesis set used

- `cl3_color_automorphism_theorem` (retained): provides SU(3)_c with
  Gell-Mann generators in the fundamental.
- Adjoint representation construction (mathematical, admitted-context).
- Schur's lemma (mathematical, admitted-context).

No fitted parameters. No observed values. No physics conventions admitted
beyond the retained color automorphism theorem.

## Corollaries

C1. **Universal "color charge squared" of a gluon = 3.** In the framework's
adjoint of SU(3)_c, every gluon mode carries the color-Casimir value 3,
independent of which of the eight color components it lives in.

C2. **Three-gluon vertex color factor.** The g_s f^{abc} structure of the
three-gluon vertex contributes a color factor controlled by f^{abc} and
the adjoint Casimir; numerical evaluation involves C_2(adj) = 3.

C3. **One-loop gluon self-energy color factor.** The gluon self-energy
diagram with one gluon loop has color factor C_2(adj) = 3, contributing
to the running of the gauge coupling.

C4. **β-function color factors.** The leading-order β-function of QCD,
β_0 = (11/3) C_2(adj) - (4/3) T_F · n_f, has the C_2(adj) = 3 prefactor
on the gluonic contribution. With n_f flavors of color-triplet quarks
and T_F = 1/2: β_0 = 11 - (2/3) n_f, the standard SU(3)_c gluonic
contribution.

C5. **Companion to fundamental result (R6 Block 03).** Together with
C_2(fund) = 4/3, this completes the basic Casimir table for SU(3)_c
on the framework's standard color content. The two values are the
multiplicative constants appearing throughout perturbative QCD color
algebra.

C6. **No accidental color symmetry.** The fact that C_2(adj) ≠ C_2(fund)
(specifically 3 ≠ 4/3) confirms that quark and gluon representations
are *genuinely distinct* irreducible representations of SU(3)_c, with
the adjoint not splittable as a sum of fundamentals.

## Honest status

Positive theorem on the framework's SU(3)_c Casimir on the adjoint, derived
from a single retained one-hop dependency by elementary Lie-algebra
computation. The runner exhibits Hermitian generators, Lie algebra closure
on the adjoint, trace orthogonality with normalization N, Schur scalar
property of C_2, exact value 3, and consistency with the SU(N) ratio
formula at N = 3.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "SU(3)_c quadratic Casimir on adjoint = N = 3 in standard Gell-Mann normalization."
upstream_dependencies:
  - cl3_color_automorphism_theorem (retained)
admitted_context_inputs:
  - adjoint representation construction (Lie-algebra)
  - Schur's lemma (Lie-algebra representation theory)
```
