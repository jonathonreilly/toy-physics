# Block B.7 — Forcing Wilson-Form Magnetic Operator from Cl(3) Primitive Operations

**Date:** 2026-05-07
**Type:** working block-derivation note (intermediate); the structural
content is consolidated and refined in
[`A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md`](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md)
and definitively settled in
[`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md) (continuum-level
derivation; finite-β residual is parsimony, not load-bearing).
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.

## Goal

Find a first-principles principle that pins the magnetic operator
`M̂(U_p)` to Wilson-form (single-fundamental-trace), eliminating the
140% action-form spread observed in Block C.

The principle proposed here: **the magnetic operator must be expressible
in Cl(3)-primitive operations only, applied at single-loop traversal**.

## B.7.1 What Cl(3) primitive operations are

The Cl(3) algebra `(8-dim ℝ-algebra ≅ M_2(ℂ))` provides the following
primitive operations, all forced by axiom A1:

| Primitive | Notation | Type |
|---|---|---|
| Algebra product | `x · y` | binary |
| Identity element | `1` | nullary |
| Clifford conjugation | `x → x̃` (reverses grade-1 and grade-3) | unary |
| Grade-0 projection (scalar part) | `⟨x⟩₀` | unary, → ℝ |
| Spinor / fundamental trace | `Tr_F(x) := 2⟨x⟩₀` (since spinor rep is 2-dim) | unary, → ℂ |

These are the operations the framework provides directly at A1. Anything
else is non-primitive — it requires either:
- Additional axioms (e.g., higher-rep tensor products),
- External imports from rep theory (e.g., projector to `(2,0)` irrep),
- Polynomial constructions from primitives (which may or may not be
  natural).

## B.7.2 What gauge-invariant scalars are buildable

A "gauge-invariant scalar built from a single closed loop" is a function
of the holonomy `U_p ∈ SU(3)` (where SU(3) sits inside the Cl(3)
unit-spinor group via the framework's derivation on the 3D symmetric base)
expressible as:

```
f(U_p)  =  P(U_p, U_p^{-1}, Tr_F, ⟨·⟩₀, ·, ~)
```

for some "polynomial" `P` in the primitive operations. We require:

- (i) **Single-loop traversal**: `U_p` appears with combined degree 1,
  modulo cyclic rearrangement around the loop. (Going around the loop
  twice would be `U_p²`; that violates single-loop.)
- (ii) **Cyclic invariance**: under cyclic permutation of products
  (since the loop has no preferred starting vertex).
- (iii) **Hermiticity**: `f` is real-valued (forced by RP).

## B.7.3 Forcing theorem

**Theorem (B.7).** Under conditions (i)–(iii), the unique gauge-invariant
scalar built from primitive Cl(3) operations on `U_p` is

```
f(U_p)  =  α  ·  Re Tr_F(U_p)  +  β  ·  ⟨1⟩₀
        =  α  ·  Re Tr_F(U_p)  +  β
```

for real constants `α, β`. The constant `β` is irrelevant to dynamics;
the dynamical content is uniquely the **Wilson-form** scalar
`Re Tr_F(U_p)`.

**Proof sketch.**

By condition (i), `f` is degree-1 in `U_p` and degree-1 in `U_p^{-1}` at
most. Polynomials in primitive operations of degree ≤ 1 in `U_p`
(treating `U_p^{-1}` as an independent variable for the moment) are
spanned by:

1. Constants (degree 0): `c · 1`, `c ∈ ℝ`
2. `Tr_F(U_p)`, `Tr_F(U_p^{-1})` (degree 1 in `U_p` or `U_p^{-1}`)
3. `Tr_F(A · U_p · B)` for various `A, B ∈ Cl(3)` constants

By cyclic invariance (ii), case 3 reduces to `Tr_F(A · B · U_p)` which
is `Tr_F(C · U_p)` for `C = A · B`. For this to be gauge-invariant
under SU(3) acting on the 3D symmetric base — `U_p → g U_p g^{-1}` —
we need `C` to commute with all SU(3) generators on the 3D base. By
Schur on the irreducible fundamental, `C` is a scalar multiple of identity.
Therefore, case 3 reduces to `Tr_F(U_p)`.

By Hermiticity (iii), the real combination of `Tr_F(U_p)` and
`Tr_F(U_p^{-1}) = Tr_F(U_p^*)` is `Re Tr_F(U_p)`.

Thus `f(U_p) = α Re Tr_F(U_p) + β`. ∎

## B.7.4 What this rules out

| Operator | Why ruled out under B.7 conditions |
|---|---|
| `Re Tr_F(U_p²)` | violates condition (i) — degree 2 in `U_p` |
| `\|Tr_F(U_p)\|²` | violates (i) — degree 2 (one `U_p`, one `U_p^{-1}`, but also gives `Re Tr_F(U_p) · Re Tr_F(U_p)` not single-loop trace) |
| `χ_(2,0)(U_p)` | requires `Tr_F(U_p²)`, violates (i) |
| `χ_(1,1)(U_p)` | requires `Tr_F(U_p) Tr_F(U_p^{-1}) - 1`, violates (i) |
| Heat-kernel `-log P_t(U_p)` | non-polynomial; not a primitive Cl(3) operation |
| Manton `d²(U_p, I)` | requires bi-invariant geodesic distance (Riemannian structure), not Cl(3)-primitive |
| Higher-`d_λ` characters in general | All require multiple `Tr_F` or higher-power constructs |

## B.7.5 Caveats — what B.7 does NOT close

B.7 admits the constants `α, β`. The continuum-matching argument from
Block B fixes `α` (modulo the open `g_bare = 1` gate); `β` is
gauge-irrelevant. So B.7 + Block B + g_bare gate closure → unique
magnetic operator.

But B.7 makes one **unverified** assumption that needs scrutiny:

> "Single-loop traversal" — that the magnetic operator is degree-1
> in `U_p`, treating multiple traversals as a separate operator.

This is a **locality / minimality** statement. It is *natural* but not
forced by A1+A2 alone. If we admit higher-degree single-plaquette
operators (`Tr_F(U_p²)` etc.), the action-form ambiguity reopens at
higher operator dimension.

A stronger forcing argument would derive single-loop-traversal from a
deeper Cl(3) structural principle. Possible candidates:

- (a) **Cohomological**: closed loops of length 1 form a Cl(3) cocycle
  basis; higher-length loops are coboundaries (?). Speculative.
- (b) **Spin-network minimality**: in a Cl(3)-recoupling spin-foam,
  single-traversal plaquettes carry the lowest non-trivial weight;
  multi-traversals are higher-order corrections.
- (c) **Operator-dimension counting** at the lattice scale: `Re Tr_F(U_p)`
  is dim-4 (matches `(1/2g²) Tr F²` continuum); `Re Tr_F(U_p²)` is dim-8
  or higher (Symanzik-irrelevant). Standard, but not Cl(3)-specific.

## B.7.6 What B.7 establishes vs admits

| Status | Statement |
|---|---|
| **Established** (under conditions i–iii) | The unique single-loop-traversal Cl(3)-primitive gauge-invariant scalar of `U_p` is `Re Tr_F(U_p)` |
| **Established** | Higher SU(3) characters require either multi-traversal or non-primitive operations |
| **Admitted** | "Single-loop traversal" is the right minimality condition (not derived from A1+A2 directly) |
| **Admitted** | Continuum-matching coefficient `α` from Block B (open gate `g_bare=1`) |

## B.7.7 Forcing strength assessment

**B.7 is a parsimony-canonical argument that becomes a uniqueness theorem
under one additional axiom: "single-loop-traversal" minimality.**

That additional axiom is *natural* and matches standard physics intuition
(simplest plaquette = simplest loop = single traversal), but is not a
consequence of A1+A2 alone.

If this minimality axiom is admitted, the framework's magnetic operator
is **uniquely Wilson-form** and the bridge gap reduces to:
- `g_bare = 1` open gate (closure status: partial)
- Multi-plaquette/thermodynamic extrapolation (engineering)

If this minimality axiom is rejected, the action-form ambiguity stands
at the level Block C found numerically: 140% spread.

## B.7.8 Recommendation

Promote single-loop-traversal minimality to an explicit framework
"locality axiom" or "operator-dimension axiom":

> **A2.5 (proposed locality refinement):** Lattice operators built from
> Cl(3) primitives are restricted to single-loop-traversal at the
> minimal-dimension lattice scale. Higher-degree single-plaquette
> operators are admitted as Symanzik-improvement corrections, not as
> primary lattice action.

With A2.5 admitted, B.7 closes the action-form ambiguity. Without it,
the ambiguity persists and the bridge gap requires either Resolution B
(governance) or a stronger structural theorem.

A2.5 is **much weaker** than admitting Wilson directly. Wilson admits
a specific functional form. A2.5 admits only a locality structure that
forces the form via B.7. The new-physics content is that A2.5 is
defensible from substrate locality arguments in a way that "admit
Wilson" is not.
