# A2.5 — Single-Loop-Traversal Minimality Axiom — Audit-Grade Proposal + Hostile Review

**Date:** 2026-05-07
**Type:** axiom_proposal + hostile_review
**Claim type:** open_axiom (proposed framework refinement, conditional on review)
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.

## A2.5.1 Statement

**Proposed framework axiom A2.5 (single-loop-traversal locality).**

> Lattice operators in the framework's KS Hamiltonian, built from
> Cl(3)-primitive operations on link variables, are restricted to
> single-loop-traversal at the minimal-dimension lattice scale.
> Higher-degree single-plaquette operators (`Tr U^k` for k≥2,
> `(Tr U)^k` for k≥2) are admitted only as Symanzik-improvement
> corrections, not as primary lattice action terms.

**Effect under A2.5 + Block B continuum-matching constraint:** the
magnetic operator at each spatial plaquette is uniquely

```
M̂(U_p)  =  c · (1 − (1/N_c) Re Tr_F(U_p))
```

with `c` fixed by continuum matching (modulo the open `g_bare` gate),
i.e., **Wilson-form magnetic operator forced uniquely**. This eliminates
the 140% action-form spread observed in Block C.

## A2.5.2 What A2.5 admits vs what it forces

| Status | Item |
|---|---|
| **Admitted** | "Single-loop-traversal" is the minimality criterion |
| **Admitted** | "Minimal-dimension lattice scale" (Wilson-Symanzik) is the relevance criterion |
| **Forced** (under A2.5 + B.7 + Block B) | Magnetic operator = `Re Tr_F(U_p)` Wilson-form |
| **Forced** (under A2.5) | Higher characters (χ_(2,0), χ_(1,1), ...) cannot be the leading-dim magnetic term |
| **NOT forced** | `g_bare = 1` (separate open gate) |
| **NOT forced** | Multi-plaquette correlations (engineering, separate from action form) |

## A2.5.3 Why this is genuinely weaker than admitting Wilson directly

| Admit Wilson directly | Admit A2.5 |
|---|---|
| Specifies a particular functional form `S = β Σ (1 - Re Tr U/N_c)` | Specifies a locality structure |
| Contains the value `β = 6` baked in | Has no specific coupling value |
| Borrows from QFT convention | Derived from substrate primitives + dimension-counting |
| One specific theory | Family of theories (any single-loop-traversal action), with Wilson the parsimony-canonical member |
| Cannot derive Manton or HK | Manton/HK violate single-loop-traversal at higher dimensions; admitted as Symanzik corrections, not primary action |

The substantive content of A2.5: it tells you *how to construct lattice
operators from algebra primitives*, and the conclusion (Wilson-form is
forced at leading order) is a derived theorem (B.7), not an admitted
input.

## A2.5.4 Hostile review pass

I attack A2.5 from 5 angles. Each tries to show that A2.5 is either
(a) circular, (b) too weak to force Wilson, or (c) actually equivalent
to admitting Wilson.

### Attack 1 (circularity): "Single-loop-traversal IS Wilson"

**Claim:** A2.5 is just a fancy renaming of "use the Wilson plaquette
action." If the Cl(3) primitive operations naturally give `Re Tr_F(U_p)`,
then A2.5 just says "use the Cl(3) primitive answer," which is trivial.

**Response:** Distinguish three levels:

1. The **lattice operator vocabulary**: what operators can be written
   down. Wilson-as-axiom specifies `Re Tr_F(U_p)` only; A2.5 specifies a
   *family* — all operators that are degree-1 in U at single-plaquette,
   class functions, and Cl(3)-primitive.

2. The **selection within the family**: what's leading at the lattice
   scale. Under A2.5, this is forced by minimum-dimension counting,
   giving Wilson-form. Without A2.5, this is a free choice.

3. The **action functional**: what specific number to call "the
   action." Under A2.5, this is `Re Tr_F(U_p)` × coupling × volume
   factors. Under direct-Wilson admission, this is also `Re Tr_F(U_p)`
   × coupling × volume — but the COUPLING is a separate input.

A2.5 forces (1) and (2) from primitives + dimension-counting; Wilson-
admission forces (1) and (3) directly. They are inequivalent: A2.5
admits `(Re Tr_F(U_p))^k` for k≥2 as Symanzik corrections, while
Wilson-admission excludes them by definition.

**Verdict:** Attack 1 fails. A2.5 is genuinely weaker than admitting
Wilson directly.

### Attack 2 (insufficient force): "A2.5 doesn't pin Wilson uniquely"

**Claim:** A2.5 says single-loop-traversal at minimum dimension. But
`Re Tr_F(U_p)` and `Im Tr_F(U_p) · 0` and `α · Re Tr_F(U_p) + β` (for
constants α, β) all qualify. The "α, β" freedom is real and not closed
by A2.5.

**Response:** The constants `α, β` are addressed elsewhere:

- `β` (overall offset): irrelevant to dynamics (constants don't affect
  ground state or `⟨P⟩`).
- `α` (overall normalization): forced by Block B continuum-matching
  constraint (`Σ_λ m_λ d_λ C_2(λ) = 8` for canonical Tr-form).

Under A2.5, `m_λ = 0` for λ ≠ (1,0), (0,1) (since higher characters
require multiple traversals or higher-degree polynomials). So the
constraint becomes `m_(1,0) · 2 · 3 · 4/3 = 8`, giving `m_(1,0) = 1`.
Magnetic operator is uniquely forced to be `(1/N_c) Re Tr_F(U_p)`.

**Verdict:** Attack 2 fails. Block B + A2.5 together close the
coefficient.

### Attack 3 (alternative single-traversal operators): "Manton is also single-traversal"

**Claim:** Manton's geodesic distance squared, `d²(U_p, I)`, is a
single-traversal class function (it's a function of `U_p`, not `U_p^k`).
So Manton qualifies under A2.5 too — A2.5 doesn't distinguish Wilson
from Manton.

**Response:** This is the strongest attack. Let me address carefully.

`d²(U, I)` is the squared bi-invariant geodesic distance, defined as

```
d²(U, I)  =  ||log U||²
         =  -Tr_F((log U)²)  [up to constants]
```

`log U` is *not* a Cl(3)-primitive operation. It requires the
exponential map's inverse, which is well-defined only on a
neighborhood of the identity and requires Riemannian-manifold
structure on SU(3). The Cl(3) algebra provides multiplication and
trace; it does NOT provide `log` or its inverse, the exponential,
as primitive operations.

So `d²(U, I)` is not a polynomial in Cl(3)-primitive operations.
It is in the *closure* of Cl(3) operations under analytic functions
(infinite series in `log U`), which is a distinct construction.

To make Manton-form available as a primitive operator, we'd need to
add Riemannian structure (the bi-invariant metric) as an extra
admitted primitive. A2.5 specifically rules this out: only algebraic
Cl(3) operations.

**Verdict:** Attack 3 fails *if* "Cl(3)-primitive" excludes infinite
power series. This is a defensible interpretation but should be
sharpened in the audit-grade write-up.

### Attack 4 (nonlocal operators): "Long-range operators are also Cl(3)-primitive"

**Claim:** A2.5 restricts to single-plaquette. But longer Wilson loops
(2x1 rectangles, 1x2 rectangles, twisted plaquettes) are also gauge-
invariant Cl(3)-primitive scalars. They're degree-1 in their respective
holonomies. Why aren't they admitted?

**Response:** "Single-loop-traversal at the minimal-dimension lattice
scale" excludes them on dimension grounds. A 2x1 Wilson loop has
operator dimension at least `(2·1)·4 = 8` (versus dim-4 for 1x1
plaquette), so it's a Symanzik improvement term, not a primary action
term.

Equivalently: **the smallest closed loop on Z³ is the 1x1 plaquette**.
Any other loop is built from multiple plaquettes (via Stokes-like
relations) or has a strictly larger area.

**Verdict:** Attack 4 fails for elementary plaquettes; attack succeeds
for "elementary loop" being something other than 1x1 plaquette. This
sharpens A2.5's scope: it specifies the *minimal* gauge-invariant loop
as 1x1 plaquette, which is a Z³ substrate-locality fact.

### Attack 5 (representation theory): "There are non-fundamental but single-traversal Cl(3) primitives"

**Claim:** The Cl(3) algebra has not just the spinor (fundamental) trace
but also higher-rank traces (e.g., `Tr_(2,0)` on the symmetric
tensor square of the spinor rep). These are single-traversal in
the gauge holonomy but use a different rep. They're Cl(3)-primitive
in the sense that they're built from Cl(3) generators acting on a
constructed rep.

**Response:** Higher-rank reps are NOT primitive Cl(3) operations.
They're constructions:
- `(Sym² V_F) = V_(2,0) ⊕ ...` requires defining the symmetric tensor
  square, choosing a basis, and projecting.
- The trace `Tr_(2,0)` is then trace in this constructed rep.

The Cl(3) algebra primitive operations are: product, conjugation,
grade-0 projection, fundamental (spinor) trace. Higher-rank reps
require additional construction not built into Cl(3) primitives.

So `Tr_(2,0)(U_p)` is NOT a Cl(3)-primitive single-traversal scalar.
It's a constructed object that requires admitting `Sym² V_F` as a
separate framework primitive — which it is not.

**Verdict:** Attack 5 fails *if* "primitive operations" exclude derived
representation constructions. This is again defensible but should be
explicit in the audit write-up.

## A2.5.5 Audit-grade scope

After the hostile-review pass, A2.5 survives provided two scope
clarifications:

1. **Cl(3)-primitive operations are bounded to: algebra product,
   Clifford conjugation, grade-0 projection, fundamental (spinor)
   trace.** They explicitly exclude:
   - Infinite power series (e.g., `log U`, `exp U`)
   - Higher-rank rep constructions (e.g., `Sym² V_F`, `V_(2,0)` traces)
   - Riemannian structures (e.g., bi-invariant metrics)

2. **Single-loop-traversal at minimal-dimension means: degree-1
   polynomial in `U_p, U_p^{-1}` over the elementary 1x1 plaquette of
   Z³**. Larger loops, multi-plaquette compositions, and higher powers
   of `U_p` are admitted as Symanzik improvements, not primary action
   terms.

With these scope clarifications, A2.5 forces Wilson-form magnetic
operator uniquely (B.7) modulo the open `g_bare` gate.

## A2.5.6 Risks

Even after the hostile-review pass, two risks remain:

### Risk 1: A2.5 may be subsumed by a stronger principle

If a deeper Cl(3) algebraic argument (algebra cohomology, single-irrep
locality theorem, or substrate-coboundary) forces single-loop-traversal
*from A1+A2 alone*, then A2.5 is downstream-derived rather than
admitted. This would be the cleanest closure but is currently open.

### Risk 2: The "primitive operations" definition is itself a convention

The list (product, conjugation, grade-0 projection, fundamental trace)
is *natural* but not strictly forced by A1. Adding any of:
- `(Sym² V_F)` reps
- `log` / `exp` maps
- Bi-invariant metrics

would invalidate A2.5's force. The audit should specifically test
whether any of these admissions creep into the framework via
downstream derivations.

## A2.5.7 Recommendation

Promote A2.5 to **proposed framework axiom** with the scope clarifications
in A2.5.5. Submit for independent audit lane review.

If audited clean, A2.5 closes the action-form ambiguity to the level of
the open `g_bare` gate. The bridge gap then reduces to:
- `g_bare = 1` closure (existing open gate, partial)
- Multi-plaquette / thermodynamic extrapolation (engineering)

Both are substantively narrower than the original "what is the gauge
action" question.

If audited not-clean, the framework either:
- Admits Wilson directly (Resolution B governance, the user explicitly
  rejected this), OR
- Continues searching for a stronger Cl(3)-derived forcing principle.
