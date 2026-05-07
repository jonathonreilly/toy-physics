# Plaquette V=1 Picard-Fuchs ODE: Rank-Bound Citation Note

**Date:** 2026-05-06
**Claim type:** bounded_theorem
**Status:** bounded support theorem; audit status is set only by the
independent audit lane.
**Companion notes:**
[`PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md) (the ODE)
and
[`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md)
(the partial minimality proof, pending the rank bound covered here)

## Audit gap addressed

The minimality-proof note (commit `2ea6e2bae`) closes the V=1 PF ODE
minimality conditional via six steps. Step 4 invokes the bound

> Bernstein rank bound for SU(N) Wilson character integrals: rank(J) ≤ N

(in the note's prose, with N = 3 written as "rk(SU(3)) = 3"; see
[Errata](#errata-on-the-companion-note) below for that wording fix).

The minimality theorem reads cleanly only if this rank bound is
externally attestable. This note investigates the literature, identifies
the closest available theorem statement, and then states honestly what
this allows the V=1 PF ODE minimality theorem to claim and what it does
not.

## Setup

```text
J(β) = ∫_{SU(3)} exp(β · Re Tr U / 3) dU,           J(0) = 1.
```

PR #541 produced an annihilating polynomial-coefficient differential
operator `L` of order 3 and coefficient degree 2:

```text
L = 6 β² ∂³  +  β(60 − β) ∂²  +  (−4β² − 2β + 120) ∂  −  β(β + 10) · 𝟙.
```

We need: **no operator of order ≤ 2 with polynomial coefficients of
ANY degree annihilates `J(β)`**, given that the order-3 operator `L`
exists.

## Investigation outcome

The literature search produced four relevant frameworks. Each is
strictly weaker than the clean rank-≤-3 bound the companion note
invokes; combining them gives a rigorous answer of a different shape.

### Framework A — Bernstein 1972 (existence only)

Bernstein's theorem on holonomic D-modules guarantees that `J(β)` is
annihilated by *some* non-zero polynomial-coefficient differential
operator. It does not bound the order. ([1])

### Framework B — Aomoto-Gelfand A-hypergeometric rank

The Aomoto-Gelfand framework gives a holonomic system attached to a
matrix `A` and parameter vector `β`, with rank equal to the normalized
volume of the corresponding polytope for generic parameters and rank
inequality `rank(M_A(β)) ≥ vol(A)` in the non-generic case. ([4],[2])

The framework requires a torus-action realization; the SU(3) Wilson
integral does not natively present as an A-hypergeometric system on a
toric variety, so this rank theorem does not directly apply. The
abstract Aomoto-Gelfand theorem on hypergeometric integrals on
configuration spaces of hyperplane arrangements similarly does not
cover the compact-Lie-group case.

### Framework C — Sabbah / Hotta-Takeuchi-Tanisaki (D-module direct image)

Sabbah's monograph and HTT chapter 5 give the direct-image construction
for D-modules, with rank-preservation under proper push-forward and a
Künneth-type bound under product. ([5],[6])

The Sabbah / HTT framework gives the **abstract existence** of a finite
holonomic rank for a parameter integral over a smooth proper algebraic
family, but does not give a closed-form rank bound `≤ N` for the
specific SU(N) Wilson integral.

### Framework D — Creative telescoping (Wilf-Zeilberger / Koutschan)

This is the framework that delivers an effective bound. Each modified
Bessel function `I_n(β/3)` is order-2 holonomic in β. The Bars 1980
identity ([3])

```text
J(β) = Σ_{k ∈ ℤ} det[I_{i−j+k}(β/3)]_{i,j=0,1,2}
```

writes `J(β)` as a sum (over `k`) of determinants of 3×3 matrices of
modified Bessel functions. By D-module closure under finite products
([7]) and the Bessel contiguous-shift recurrence

```text
I_{n+1}(z) = I_{n−1}(z) − (2n/z) I_n(z),
```

each `det` summand lies in a D-module of effective rank ≤ 2³ = 8 in
the worst case. The infinite sum over `k` converges in a strong
holonomic sense (each summand is exponentially small in `|k|` for
fixed β) and preserves holonomicity by direct image. Creative
telescoping ([7],[8]) then **algorithmically** produces the minimal
annihilator. The PR #541 derivation IS the Koutschan output for
this integrand, and the runner certificate `[B]` of the companion
note empirically verifies that no order-≤2 annihilator exists at
coefficient degree ≤ 12.

## What this gives us

Combining Frameworks A and D with the runner certificates, we obtain:

**Theorem (PF minimality, partial):** With `J(β)` and `L` as above,

(i) `L · J(β) = 0` as an analytic identity on `β ∈ ℝ_{≥0}` (Step 3 of
    companion note, deep certificate to Taylor depth 40).

(ii) Among all polynomial-coefficient differential operators of order
     ≤ 2 with coefficient degree ≤ 12, no annihilator of `J(β)` exists
     (Step 4 of companion note, rank certificate `[B]`).

(iii) Among all polynomial-coefficient differential operators of order
      3 with coefficient degree ≤ 2, the operator `L` is unique up to
      non-zero scalar multiple (Step 5 of companion note, rank
      certificate `[C]`).

What is NOT yet closed:

(✗) The companion note's prose claim "rank(J) ≤ 3 by Bernstein /
    Aomoto-Gelfand" with N=3 substituted as "rk(SU(3)) = 3" is
    **literature-incorrect** as stated. The Lie-group rank of SU(3) is 2,
    not 3. The correct statement is "matrix size N = 3", and the bound
    "order ≤ N = 3" is not a textbook theorem we have located, only a
    consequence of the Bessel-determinant + D-module closure argument
    in Framework D plus computation.

(✗) Therefore the lower-order exclusion at coefficient degree > 12
    relies on the EFFECTIVE bound from Framework D, not on a single
    abstract rank theorem. To close this rigorously we need either:

    (a) an explicit citation that the Bessel-determinant / D-module
        closure rank bound is `≤ 3` for the SU(3) case, or
    (b) a runner extension that pushes certificate `[B]` to higher
        coefficient degrees `d` and verifies stability of the rank
        gap at exactly `r = 3`.

## Honest assessment

The literature search did not produce a single named theorem in the
Aomoto-Gelfand or Sabbah/HTT corpus that bounds the holonomic rank of
the SU(N) Wilson character integral by `N`. Such a bound is
**plausible and consistent** with Framework D and the verified SU(2)
order-2 baseline, but it is **not a textbook citation**.

The companion note's existing certificates `[A]`-`[E]` give a
**finitely-checked unconditional theorem** at the coefficient-degree
level checked. The infinite-degree extension requires either:

  (a) **Algorithmic certificate.** A Koutschan-style creative
      telescoping run that explicitly produces the annihilator and
      certifies its order, with the certificate including a Gröbner
      basis terminator for the higher-coefficient-degree exclusion.
      This would close the gap WITHIN the framework's own toolkit
      without needing an external named theorem.

  (b) **Direct citation upgrade.** A focused literature/expert review
      to find a paper specifically about SU(N) one-link integrals with
      a clean order-N bound. The closest candidates are Andrews-Onofri
      1984 ([9], on q-hypergeometric structure of one-plaquette
      integrals) and the Forrester-Witte / Tracy-Widom Toeplitz-Painlevé
      tradition ([10], on U(N) integrals and Painlevé III/V structure),
      neither of which we have been able to verify gives the precise
      bound for the SU(3) case.

Neither (a) nor (b) is in scope for this 30-60 min focused task. The
closure here is therefore intermediate — it identifies the precise
nature of the gap and bounds it computationally, rather than closing
it via a single citation.

## Errata on the companion note

The companion note (`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`,
section "Bounded scope") writes the rank bound as `"rk(SU(3)) = 3"`.
This is a typo for `"matrix size N = 3"` — the Lie-group rank of SU(3)
is 2 (= number of independent Cartan generators). The bound asserted
should read `"order ≤ N = 3"` and is supported by Framework D plus
runner certificates `[B]`, `[C]`, `[E]`, not by a textbook
Aomoto-Gelfand rank theorem.

## Cited authorities

[1] **Bernstein, J. N.** "The analytic continuation of generalized
    functions with respect to a parameter." *Functional Analysis and
    its Applications*, 1972, 6(4): 273–285.

[2] **Aomoto, K. and Kita, M.** *Theory of Hypergeometric Functions*.
    Springer Monographs in Mathematics, 2011.

[3] **Bars, I.** "U(N) integral for the generating functional in
    lattice gauge theory." *Journal of Mathematical Physics*, 1980,
    21(11): 2678–2681.

[4] **Saito, M., Sturmfels, B., and Takayama, N.** *Gröbner
    Deformations of Hypergeometric Differential Equations*. Algorithms
    and Computation in Mathematics, vol. 6. Springer, 2000.

[5] **Sabbah, C.** *Hodge Theory, Singularities and D-modules*,
    lecture notes, 2007.

[6] **Hotta, R., Takeuchi, K., and Tanisaki, T.** *D-Modules,
    Perverse Sheaves, and Representation Theory*, Birkhäuser, 2008.

[7] **Wilf, H. S. and Zeilberger, D.** "Rational functions certify
    combinatorial identities." *Journal of the American Mathematical
    Society*, 1990, 3(1): 147–158.

[8] **Koutschan, C.** "Creative Telescoping for Holonomic Functions."
    In *Computer Algebra in Quantum Field Theory: Integration,
    Summation and Special Functions*, ed. C. Schneider, Springer,
    2013.

[9] **Andrews, G. E. and Onofri, E.** "Lattice Gauge Theory, Orthogonal
    Polynomials and q-Hypergeometric Functions." In *Special Functions:
    Group Theoretical Aspects and Applications*, eds. R. A. Askey et al.,
    Reidel, 1984: 163–188.

[10] **Forrester, P. J. and Witte, N. S.** "Application of the τ-function
     theory of Painlevé equations to random matrices: PVI, JUE, CyUE,
     cJUE and scaled limits." *Nagoya Mathematical Journal*, 174 (2004):
     29–114.

## Audit consequence

```yaml
claim_id: plaquette_v1_picard_fuchs_ode_rank_bound_citation_note_2026-05-06
note_path: docs/PLAQUETTE_V1_PICARD_FUCHS_ODE_RANK_BOUND_CITATION_NOTE_2026-05-06.md
runner_path: scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py
claim_type: bounded_theorem
claim_scope: >
  Honest assessment of the literature gap in the V=1 SU(3) PF ODE
  minimality argument. Identifies that no clean named rank-≤-N theorem
  exists in the Aomoto-Gelfand / Sabbah / HTT corpus for the specific
  SU(N) Wilson character integral, and that the effective bound comes
  from the Bessel-determinant + D-module closure (Framework D)
  combined with creative-telescoping algorithms. Provides errata on
  the companion note's "rk(SU(3)) = 3" wording.
proposes_addendum_for: plaquette_v1_picard_fuchs_ode_minimality_proof_note_2026-05-06
deps:
  - PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md
  - PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md
  - Bernstein 1972 (D-module holonomicity)
  - Bars 1980 (Bessel-determinant identity)
  - Wilf-Zeilberger 1990 / Koutschan 2013 (creative telescoping)
status_authority: independent audit lane
```

## Recommended follow-up

To CLOSE (not just bound) the V=1 PF ODE minimality conditional, two
paths exist, in order of effort:

1. **Algorithmic close (1-2 h):** Extend the existing minimality runner
   to push certificate `[B]` to coefficient degree d ≥ 24 and verify
   the rank gap remains intact. Add a separate Koutschan-style
   creative-telescoping check (using `sympy.holonomic` or similar) that
   produces the annihilator independently and certifies its order is
   exactly 3.

2. **Citation close (uncertain effort):** Locate a specific paper on
   SU(N) one-link integrals proving order = N. Andrews-Onofri 1984 and
   the Forrester-Witte Painlevé-tau corpus are the most plausible
   candidates but neither has been verified in this task.

This note classifies the deliverable as **PARTIAL** rather than
**UPGRADE-READY** because the gap is now precisely characterized but
not yet closed.

## Command

This note is documentation only — it adds no new runner. It refers to
the existing runner from the companion minimality note:

```bash
python3 scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py
```

Expected summary (unchanged):
```text
SUMMARY: CERTIFICATE PASS=5 FAIL=0
```
