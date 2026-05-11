# Wilson-Shifted V_taste Extremum at Leading Order in r — Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_wilson_vtaste_extremum_leading_order_in_r.py`](../scripts/frontier_wilson_vtaste_extremum_leading_order_in_r.py)

## Claim

Working with the Wilson-corrected tree-level mean-field taste potential

```text
V_taste^W(m)
   =  - (1/2) · Σ_{k=0}^{4}  binomial(4, k) · log( (2 r k + m)^2 + 4 u_0^2 )       (1)
```

derived in
[`WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`](WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md)
(landed in the same review-loop batch), the Wilson-shifted extremum
`m^*` of `V_taste^W` and the curvature at `m^*` are:

```text
m^*       =  - 4 r       (exact, all orders in r),                              (2)

d^2 V^W / dm^2  |_{m = m^*}
          =  - 4 / u_0^2   +   ( 12 r^2 ) / u_0^4   +   O( r^4 ).                (3)
```

The exact identity `m^* = -4r` holds by an exchange symmetry of (1):
under the index relabeling `k → 4 - k`, the multiplicities
`binomial(4, k)` are invariant (`binomial(4, k) = binomial(4, 4-k)`)
while `(2 r k + m)` paired with `(2 r (4 - k) + m)` shift symmetrically
around `(4 r + m)`. Setting `m = m^* = -4 r` makes the pair shifts
`±2 r (k - 2)` antisymmetric while the multiplicity weights are
symmetric, so every pair contribution to `dV^W/dm` cancels term-by-
term, giving `dV^W/dm |_{m=-4r} = 0` identically (not perturbatively).
The leading-order derivation via the binomial-moment identity
`Σ_{k=0}^{4} binomial(4, k) · k = 32` (with `Σ binomial(4, k) = 16`)
delivers the same value `δm = -4 r` and is documented in the proof-
walk below as the constructive route to the same result.

The curvature correction `+12 r^2 / u_0^4` in (3) is leading-order in
`r` (with explicit `O(r^4)` remainder); it follows from the centered
binomial-moment identity

```text
Σ_{k=0}^{4}  binomial(4, k) · ( k - 2 )^2  =  16,                               (4)
```

i.e. the variance of `k` under the binomial distribution
`binomial(4, k) / 16`. The 5× reduction relative to the curvature
correction at `m = 0` (which is `+ 60 r^2 / u_0^4`, derived in the
sister `V_taste^W` note) reflects the fact that `Σ binomial(4, k) · k^2
= 80` and `Σ binomial(4, k) · (k - 2)^2 = 80 - 32^2 / 16 = 80 - 64 = 16`.

This note records the exact extremum location `m^* = -4r` and the
leading-order curvature there. It does **not** compute the physical
Higgs mass, does **not** sum the perturbative curvature expansion in
`r` to all orders, and does **not** close the +12% Higgs gap chain.

**Radius of convergence note.** The leading-order curvature expansion
`+12 r^2 / u_0^4` comes from Taylor-expanding
`f(x) = (x - u_0^2) / (x + u_0^2)^2` at `x = 0`, with `x = (k-2)^2 r^2`.
The Taylor series has radius of convergence `u_0^2`, so the expansion
is reliable when `(k-2)^2 r^2 << u_0^2`, i.e. `r << u_0 / 2` for the
dominant `k = 0, 4` corners. At `r = O(u_0)` the all-orders sum is
needed; the leading-order curvature is no longer a good approximation
in that regime. The runner exhibits this breakdown at `r = 1/2` and
`r = 1` for `u_0 ≈ 0.8776`.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| `dV^W/dm = -Σ_k binomial(4, k) · (2rk + m) / ((2rk + m)^2 + 4 u_0^2)` | direct differentiation of (1); already in the sister `V_taste^W` note | no |
| Setting `dV^W/dm = 0` at leading order, denominators `(2rk + m)^2 + 4u_0^2 → 4 u_0^2` (each `(2rk + m)^2` is `O(r^2)` at the leading-order shift) | calculus on a finite sum | no |
| Reduced equation: `Σ_k binomial(4, k) · (2rk + δm) = 0` for the leading shift `δm` | linearity of the leading-order condition | no |
| Solve: `2r · Σ_k binomial(4, k) · k + δm · Σ_k binomial(4, k) = 0` | binomial-moment identity `Σ binomial(4, k) · k = 32` and state count `Σ binomial(4, k) = 16` | no |
| Leading shift: `δm = -2r · 32 / 16 = -4r`, i.e. `m^* = -4r + O(r^3)` | finite arithmetic | no |
| Curvature at `m = m^*`: `d^2 V^W / dm^2 \|_{m = -4r} = (1/4) · Σ_k binomial(4, k) · ((k-2)^2 r^2 - u_0^2) / ((k-2)^2 r^2 + u_0^2)^2` (from (3) of the sister `V_taste^W` note evaluated at `m = -4r` so that `(2rk + m) → 2r(k-2)`) | calculus | no |
| Taylor expand each `(x - u_0^2) / (x + u_0^2)^2` at `x = (k-2)^2 r^2`: `(-1/u_0^2) + (3 / u_0^4) · x + O(x^2)` | scalar Taylor expansion (already verified in the sister `V_taste^W` note) | no |
| Sum with multiplicities: leading term `(Σ binomial(4, k)) · (-1/u_0^2) = 16 · (-1/u_0^2)`; subleading term `3 r^2 / u_0^4 · Σ binomial(4, k) · (k-2)^2` | binomial-moment identity (4) | no |
| Centered binomial moment: `Σ_{k=0}^{4} binomial(4, k) · (k - 2)^2 = 16` (variance of `k` under binomial distribution `binomial(n=4, p=1/2)`, so variance `= n p (1-p) = 1`, and the sum is `n p (1-p) · 2^n = 1 · 16 = 16`) | binomial-moment identity (standard combinatorics) | no |
| Multiply by `1 / 4` prefactor: `d^2 V^W / dm^2 \|_{m=-4r} = -4/u_0^2 + (3 · 16 / 4) · r^2 / u_0^4 + O(r^4) = -4/u_0^2 + 12 r^2 / u_0^4 + O(r^4)` | finite arithmetic | no |
| Compare to `m = 0`: `Σ_k binomial(4, k) · k^2 = 80`, giving `+ 60 r^2 / u_0^4`; ratio is `60 / 12 = 5`, i.e. the shift to the actual extremum reduces the leading curvature correction by a factor of `5` (= moment ratio `80 / 16`) | binomial-moment ratio | no |

Every load-bearing step is finite combinatorics, scalar calculus, or
exact rational arithmetic. The Wilson plaquette form, staggered phases,
link unitaries, lattice scale `a`, plaquette numerical value `<P>`, and
the mean-field link `u_0` numerical value do not appear as load-
bearing inputs to (2) or (3). The Wilson coefficient `r` is carried
symbolically; `u_0` is also carried symbolically (admitted at the
upstream Wilson surface).

## Exact Arithmetic Check

The runner verifies, at exact rational precision via `fractions.Fraction`:

(A) **Binomial moments:**

```text
Σ_{k=0}^{4}  binomial(4, k)         =  16,
Σ_{k=0}^{4}  binomial(4, k) · k     =  32,
Σ_{k=0}^{4}  binomial(4, k) · k^2   =  80,
Σ_{k=0}^{4}  binomial(4, k) · (k-2)^2  =  16.
```

The variance identity `Σ binomial(4,k) · (k-2)^2 = 80 - 32^2 / 16 = 80 - 64 = 16`
is verified by direct evaluation.

(B) **Leading-order shift:** symbolic substitution of `m = δm` into the
leading-order reduced equation yields `δm = -4r` exactly:

```text
2 r · Σ_k binomial(4, k) · k  +  δm · Σ_k binomial(4, k)
   =  2 r · 32  +  δm · 16  =  0   ⇒   δm = -4 r.
```

(C) **Leading-order curvature at `m = -4r`:** evaluate the closed-form
expression

```text
(1/4) · Σ_{k=0}^{4} binomial(4, k) · ( (k-2)^2 r^2 - u_0^2 ) /
                                      ( (k-2)^2 r^2 + u_0^2 )^2
```

at small `r` and verify against the Taylor approximation
`-4/u_0^2 + 12 r^2 / u_0^4`. Comparing the closed-form value at
`r = 1/100` with the two candidate approximations
`-4/u_0^2 + 12 r^2 / u_0^4` and `-4/u_0^2 + 60 r^2 / u_0^4` shows that
the `12`-coefficient approximation is correct (smaller residual by
multiple orders of magnitude in `r^2`).

(D) **Reduction at `r = 0`:** at `r = 0`, the extremum is at
`m^* = 0` and the curvature is `-4 / u_0^2`. This matches the parent
Higgs note's eq. `[3]` (`d^2 V / dm^2 |_{m=0} = -4/u_0^2`). The runner
checks this reduction at exact rational precision.

(E) **Ratio of corrections:** the runner verifies that the
`m = 0` and `m = -4r` leading-correction coefficients differ by the
ratio `Σ binomial(4, k) · k^2  /  Σ binomial(4, k) · (k-2)^2  =  80 / 16  =  5`,
matching the structural identity `60 / 12 = 5`.

## Dependencies

- [`WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`](WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md)
  for the explicit `V_taste^W` formula (1) and its first two
  derivatives (this note's load-bearing input). This dependency landed
  in the same review-loop batch; the runner remains tolerant of
  pre-merge validation order.
- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the staircase multiplicities `binomial(4, k)` and Wilson mass
  shifts `2 r k`.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  for the parent tree-level `V_taste`, the mean-field setup, and the
  `r = 0` curvature `-4/u_0^2` to which (3) reduces.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  for the staggered-Dirac realization gate context; this note inherits
  the gate's open-derivation status without closing it.
- `MINIMAL_AXIOMS_2026-05-03.md`
  for the framework axioms `A1` (`Cl(3)`) and `A2` (`Z^3`).

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the physical Higgs mass `m_H` numerical value;
- the `V_taste^W` extremum `m^*` to all orders in `r` (this note gives
  only the leading-order shift `-4r`; the next-order correction is
  `O(r^3)` and is not computed here);
- the curvature at `m^*` to all orders in `r` (this note gives only
  the leading-order Taylor coefficient `+12 r^2 / u_0^4`; the next-
  order correction is `O(r^4)` and is not computed here);
- the +12% Higgs gap chain in [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md);
- the assignment of the Higgs to a single Hamming-weight class (a
  separate bounded admission flagged in
  [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md));
- the Wilson coefficient `r` (a separate normalization choice carried
  at the upstream Wilson surface);
- the plaquette mean-field link `u_0` numerical value;
- the staggered-Dirac realization gate;
- the `g_bare = 1` derivation;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_wilson_vtaste_extremum_leading_order_in_r.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: m^* = -4r EXACTLY (k → 4-k reflection symmetry on binomial(4,k)
makes dV^W/dm |_{m=-4r} identically zero, all orders).
d^2V^W/dm^2 |_{m=-4r} = -4/u_0^2 + 12 r^2/u_0^4 + O(r^4).
Leading-r^2 coefficient pinned to 12 by direct extraction at r → 0.
5× smaller than at m=0 (variance vs raw second moment: 16 vs 80).
```
