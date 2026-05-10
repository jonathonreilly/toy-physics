# Wilson-Corrected V_taste Tree-Level Mean-Field Formula Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_wilson_corrected_v_taste_tree_level.py`](../scripts/frontier_wilson_corrected_v_taste_tree_level.py)

## Claim

On the canonical staggered Kogut-Susskind Dirac fermion plus Wilson
plaquette gauge action on `Z^3 + t` APBC at the minimal block
(`L = 2` in each of the four directions, `N_sites = 2^4 = 16`, mean-
field plaquette link `u_0`), the tree-level mean-field taste potential
with the Wilson term included is

```text
V_taste^W(m)
   =  - (1/2) · Σ_{k=0}^{4}  binomial(4, k) · log( (2 r k + m)^2 + 4 u_0^2 )       (1)
```

where:

- `r` is the Wilson coefficient (carried symbolically; not derived in
  this note);
- `binomial(4, k)` is the Hamming-weight class multiplicity from the
  staircase decomposition of the 16 BZ corners on `Z^3 + t` APBC, per
  [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md);
- `2 r k` is the Wilson mass shift on the Hamming-weight `k` class,
  also per the staircase note.

The first two derivatives at the Wilson-symmetric point `m = 0` are:

```text
dV^W/dm |_{m=0}
   =  - Σ_{k=0}^{4}  binomial(4, k) · ( 2 r k ) / ( 4 r^2 k^2 + 4 u_0^2 )         (2)

d^2 V^W / dm^2 |_{m=0}
   =  ( 1 / 4 ) · Σ_{k=0}^{4}  binomial(4, k) ·
         ( r^2 k^2 - u_0^2 ) / ( r^2 k^2 + u_0^2 )^2                             (3)
```

In the limit `r → 0` the formula (1) reduces to the existing tree-
level expression of
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) eq.
`[2]`, namely `V_taste(m) = -8 log(m^2 + 4 u_0^2)` (i.e. uniform
`N_taste = 16` degeneracy), and the curvature (3) reduces to
`d^2 V / dm^2 |_{m=0} = - 4 / u_0^2`, matching that note's eq. `[3]`.

This note records the explicit derivation of (1)–(3); it does **not**
compute the physical Higgs mass, does **not** locate the Wilson-shifted
extremum, and does **not** close the `+12%` Higgs gap chain.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| Per-corner Wilson eigenvalue at hw class `k`: real shift `2 r k`, imaginary part `±2 i u_0` from staggered anti-Hermiticity in mean field | staircase derivation [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md) + retained mean-field staggered anti-Hermiticity in [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) | already-admitted Wilson + staggered surface (cited upstream) |
| `\|λ + m·I\|^2` at hw class `k` equals `(2 r k + m)^2 + 4 u_0^2` | direct algebra on a complex eigenvalue with real part `2 r k + m` and imaginary part `±2 u_0` | no |
| Generating functional contribution per corner: `(1/2) log( (2 r k + m)^2 + 4 u_0^2 )` | standard `log\|det(D + m·I)\|^2` decomposition | no |
| Sum over corners weighted by `binomial(4, k)` from the staircase | staircase multiplicities | no |
| `V_taste^W(m) = -(1/2) Σ_k binomial(4, k) log( (2 r k + m)^2 + 4 u_0^2 )` | linearity + sign convention from the parent Higgs note | no |
| Differentiate `V_taste^W` w.r.t. `m`, evaluate at `m = 0` to obtain (2) | calculus | no |
| Differentiate again, evaluate at `m = 0` to obtain (3) | calculus | no |
| Limit `r → 0`: each `log(...)` becomes `log(m^2 + 4 u_0^2)`; multiplicity sum gives `Σ_k binomial(4, k) = 16`; recovers `V_taste(m) = -8 log(m^2 + 4 u_0^2)` | `Σ_k binomial(4, k) = 2^4 = 16` (already verified in the staircase note) | no |
| Limit `r → 0` of (3): each term `→ binomial(4, k) · (-1/u_0^2)`; sum `→ -16/u_0^2`; multiply by `1/4`, recover `-4/u_0^2` | binomial-coefficient sum identity | no |

Every load-bearing step is finite combinatorics, exact rational
arithmetic, or single-variable calculus on a known closed-form
expression. The Wilson plaquette form, staggered phases, link
unitaries, lattice scale `a`, plaquette numerical value `<P>`, mean-
field link `u_0` numerical value, and Monte Carlo machinery do not
appear as load-bearing inputs to the structural derivation of (1)–(3)
themselves. The Wilson coefficient `r` is carried symbolically (not
derived); `u_0` is also carried symbolically (admitted at the
upstream Wilson surface).

## Exact Arithmetic Check

The runner verifies the following with `fractions.Fraction` exact
rational arithmetic, using small rational test values
`u_0 → Fraction(8776, 10000)` and `r ∈ {0, 1/10, 1/2, 1, 2}`:

(A) **Reduction at `r = 0`.** With `r = 0`, `V_taste^W(m)` evaluated at
several `m` values exactly equals `-8 · log(m^2 + 4 u_0^2)` (the
existing eq. `[2]` of the parent Higgs note). Because `log` is
transcendental, the comparison is at the level of the *coefficient
algebra*: with `r = 0`, the sum

```text
Σ_k binomial(4, k) · log( m^2 + 4 u_0^2 )  =  16 · log( m^2 + 4 u_0^2 )
```

so `V_taste^W |_{r=0}(m) = -8 · log(m^2 + 4 u_0^2)` matches the
parent formula exactly.

(B) **First derivative at `m = 0`.** With `r ≠ 0`, the closed-form
expression (2) evaluates to a non-zero rational function of
`(r, u_0)`. The runner verifies (2) symbolically against
direct differentiation of (1).

(C) **Second derivative at `m = 0`.** The closed-form expression (3)
is verified against direct second-differentiation of (1). At
`r = 0` the sum reduces to `(1/4) · Σ_k binomial(4, k) · (-1/u_0^2)`
`= (1/4) · (-16 / u_0^2) = -4 / u_0^2`. This is the reduction to
the parent Higgs note's `[3]`.

(D) **Leading-order `r → 0` correction.** Expand each term of (3) in
`r^2`. With `f(x) = (x - u_0^2) / (x + u_0^2)^2`, the Taylor expansion
at `x = 0` is

```text
f(0)   =  - u_0^2 / u_0^4  =  - 1 / u_0^2,
f'(0)  =  ( - x + 3 u_0^2 ) / ( x + u_0^2 )^3  |_{x=0}
       =  3 u_0^2 / u_0^6
       =  3 / u_0^4.
```

So `f(x) = -1/u_0^2 + (3 / u_0^4) · x + O(x^2)`. With `x = r^2 k^2`:

```text
( r^2 k^2 - u_0^2 ) / ( r^2 k^2 + u_0^2 )^2
   =  - 1 / u_0^2  +  ( 3 r^2 k^2 ) / u_0^4   +   O( r^4 ).
```

Summing with multiplicities `binomial(4, k)` and the moment

```text
Σ_{k=0}^{4}  binomial(4, k) · k^2  =  0·1 + 1·4 + 4·6 + 9·4 + 16·1  =  80,
```

gives

```text
Σ_k binomial(4, k) · f(r^2 k^2)
   =  16 · ( - 1 / u_0^2 )  +  3 · 80 · r^2 / u_0^4   +   O( r^4 )
   =  - 16 / u_0^2          +  240 r^2 / u_0^4        +   O( r^4 ).
```

Multiplying by the prefactor `1/4` from (3):

```text
d^2 V^W / dm^2 |_{m=0}
   =  - 4 / u_0^2   +   60 r^2 / u_0^4              +   O( r^4 ).             (4)
```

The runner verifies the moment `Σ_k binomial(4, k) k^2 = 80` and the
leading-order coefficient `60` at exact rational precision by direct
comparison of the closed-form (3) at small `r` with the Taylor
approximation `-4/u_0^2 + 60 r^2 / u_0^4`.

## Dependencies

- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the staircase multiplicities `binomial(4, k)` and Wilson mass
  shifts `2 r k` on the 16 BZ corners.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  for the parent tree-level `V_taste`, the mean-field setup
  (`u_0`, `4 u_0^2`, staggered anti-Hermiticity), the eq. `[2]` to
  which the `r = 0` limit reduces, and the +12% gap chain row 3
  (Wilson taste-breaking) that asserts a Wilson correction without
  computing it.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  for the staggered-Dirac realization gate context; this note inherits
  the gate's open-derivation status without closing it.
- `MINIMAL_AXIOMS_2026-05-03.md`
  for the framework axioms `A1` (`Cl(3)`) and `A2` (`Z^3`) and the
  recategorized open derivation targets.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the physical Higgs mass `m_H` numerical value;
- the location of the Wilson-shifted extremum `m^*` of `V_taste^W`;
- the curvature of `V_taste^W` at `m^*` (which is the actual physical
  Higgs-mass relation; this note computes `d^2 V / dm^2` at `m = 0`,
  which is the Wilson-broken **non**-extremum);
- the +12% Higgs gap chain in [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md);
- the assignment of the Higgs to a single Hamming-weight class (a
  separate bounded admission flagged in the gap chain row 3);
- the Wilson coefficient `r` (a separate normalization choice carried
  at the upstream Wilson surface);
- the plaquette mean-field link `u_0` numerical value;
- the staggered-Dirac realization gate;
- the `g_bare = 1` derivation;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_wilson_corrected_v_taste_tree_level.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: V_taste^W(m) = -(1/2) Σ_k binomial(4,k) log((2rk+m)^2 + 4u_0^2)
derived; reduces to V_taste(m) = -8 log(m^2 + 4u_0^2) at r=0; second-
derivative-at-m=0 leading correction = 60 r^2 / u_0^4 with binomial
moment Σ_k binomial(4,k) k^2 = 80.
```
