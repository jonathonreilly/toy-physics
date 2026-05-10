# Area-Law Quarter Broader No-Go Note

**Date:** 2026-04-25
**Status:** audited_conditional no-go support theorem for Planck Target 2
**Runner:** `scripts/frontier_area_law_quarter_broader_no_go.py`

## Cited authorities (one-hop deps)

- [`BH_ENTROPY_DERIVED_NOTE.md`](BH_ENTROPY_DERIVED_NOTE.md) — `audited_conditional`.
  Records the bounded RT bond-dimension companion identification on the existing
  `Cl(3)/Z^3` free-fermion carrier; this no-go bounds the asymptotic Widom
  coefficient that companion approaches.
- [`BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md`](BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md)
  — `audited_conditional`. The single-carrier no-go that this note generalizes
  from one diamond / one cubic Fermi surface to the full simple-fiber Widom
  class.
- [`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
  — `audited_conditional`. Derives the action-side primitive coefficient
  `c_cell = Tr((I_16/16) P_A) = 1/4` on the primitive event cell. This is the
  Planck-side `1/4` that this no-go shows the simple-fiber Widom class cannot
  match by entanglement.
- [`PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md`](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
  — `audited_conditional`. Records the additive finite-boundary extension of
  the action-side `c_cell = 1/4` carrier and the conditional carrier-share
  identity matching `S_BH = A/(4 G_Newton,lat)` at `G_Newton,lat = 1`.

These citations make the no-go's gap structure explicit: the Planck-side
`c_cell = 1/4` is now derived (conditional on the bridge premise) from the
cited primitive-coframe theorem, while this note shows the simple-fiber Widom
class cannot match it on the entanglement side.

## Admitted-context literature input

The Widom-Gioev-Klich leading-log coefficient formula

```text
c_Widom(Gamma, e_x) = I_x(Gamma) / (12 (2*pi)^(d-1)),
I_x(Gamma) = integral_{partial Gamma} |n_k . e_x| dS_k
```

is admitted as universal physics input from the rigorous Widom-Sobolev line
(Gioev-Klich 2006; Helling-Leschke-Spitzer 2011), as already used by the cited
single-carrier no-go. This note does not re-derive the Widom-Gioev-Klich
asymptotic theorem; it imports it and uses purely combinatorial coarea/fiber
counting on top of it.

## Purpose

This note sharpens the retained BH entropy Widom no-go from one carrier to a
class statement. It does not say that no entanglement carrier can ever produce
`1/4`. It says that the broad simple-fiber Widom class available to the current
free-fermion/Schur-block lane cannot do it.

## Safe statement

Let `Gamma` be a translation-invariant free-fermion Fermi sea in the Brillouin
torus `T^d = [-pi, pi)^d`, `d >= 2`, and let the real-space cut be a flat
primitive boundary face with normal `e_x`. Assume:

1. `partial Gamma` is piecewise smooth away from measure-zero singular sets;
2. for almost every transverse momentum `q in T^(d-1)`, the fiber
   `{k_x : (k_x, q) in Gamma}` is empty, full, or a single interval in the
   `k_x` circle;
3. the RT/bond-rank normalization counts the same primitive boundary rank for
   each independent Schur or species block, so direct sums are normalized by the
   sum of their boundary `log chi` weights.

Then the Widom-Gioev-Klich leading-log coefficient satisfies

```text
c_Widom <= 1/6.
```

In particular, no carrier in this class can produce

```text
c_inf = 1/4.
```

The existing 2D half-filled NN carrier saturates the bound with `c_Widom=1/6`.
The existing 3D half-filled cubic carrier lies below it, at `~0.105`.

## The theorem

For a flat cut with unit rescaled boundary area, the Widom coefficient is

```text
c_Widom(Gamma, e_x)
  = I_x(Gamma) / (12 (2*pi)^(d-1)),

I_x(Gamma)
  = integral_{partial Gamma} |n_k . e_x| dS_k.
```

For almost every transverse momentum `q`, let

```text
N_Gamma(q) = #(partial Gamma intersect (S^1_x x {q})).
```

The coarea formula gives the fiber-count identity

```text
I_x(Gamma) = integral_{T^(d-1)} N_Gamma(q) dq.
```

Under the single-interval hypothesis, `N_Gamma(q) <= 2` almost everywhere:
one interval has two endpoints on the `k_x` circle, while an empty or full
fiber has none. Therefore

```text
I_x(Gamma) <= 2 (2*pi)^(d-1),
```

and hence

```text
c_Widom <= 2 (2*pi)^(d-1) / (12 (2*pi)^(d-1)) = 1/6.
```

But `c_Widom = 1/4` would require

```text
I_x(Gamma) = 3 (2*pi)^(d-1),
```

which is impossible in the simple-fiber class.

## Consequences by dimension

### 2D

For `d=2`,

```text
c_Widom = I_x / (24*pi).
```

The half-filled NN square-lattice Fermi surface is the diamond
`|k_x| + |k_y| = pi`. Its fibers have two crossings for almost every `k_y`,
so

```text
I_x = 4*pi,
c_Widom = 4*pi / (24*pi) = 1/6.
```

Arbitrary one-band NN fillings have at most the same two crossings per
`k_y` fiber, so they cannot exceed `1/6`. Reaching `1/4` would require
`I_x = 6*pi`, equivalently average crossing number `3` across the Brillouin
zone. Since simple closed one-interval fibers have crossing number at most
`2`, this cannot occur without multi-pocket or multi-band structure.

### 3D

For `d=3`,

```text
c_Widom = I_x / (48*pi^2).
```

A simple-fiber cubic carrier obeys

```text
I_x <= 8*pi^2,
c_Widom <= 1/6.
```

The retained half-filled cubic NN carrier only has crossings on the subset
`|cos k_y + cos k_z| < 1`, so its projected crossing measure is smaller and
the coefficient is `~0.105`, in agreement with the retained runner. Reaching
`1/4` would require `I_x = 12*pi^2`, again beyond the one-interval maximum.

## Schur/direct-sum descendants

If a finite Schur block or species stack is a direct sum of independent
simple-fiber Slater determinants, the leading entropy and the maximal
boundary-rank normalization both add:

```text
S_total ~ sum_alpha w_alpha c_alpha |partial A| log L,
S_max   ~ sum_alpha w_alpha |partial A| log L,
```

with positive weights `w_alpha = log chi_alpha`. The normalized coefficient is
therefore the convex average

```text
c_total = (sum_alpha w_alpha c_alpha) / (sum_alpha w_alpha).
```

If every block has `c_alpha <= 1/6`, then `c_total <= 1/6`. Thus finite-density
Schur-block bookkeeping does not promote the simple-fiber class to `1/4`.

This matches the species-universality check in
[BH_ENTROPY_DERIVED_NOTE.md](./BH_ENTROPY_DERIVED_NOTE.md): duplicating
species does not change the RT ratio when the boundary rank is counted
consistently.

## What remains outside the no-go

The theorem deliberately does not rule out:

- multi-pocket or multi-band free fermions whose `k_x` fibers have more than
  one occupied interval on positive transverse measure;
- a physically selected NNN or longer-range dispersion whose projected crossing
  multiplicity is exactly `3` in the Widom integral;
- non-Fermi-liquid states for which the Widom-Gioev-Klich hypothesis is not the
  right asymptotic theorem;
- gapped horizon/edge carriers with a strict area law and a separately derived
  entropy-per-face coefficient;
- topological sectors whose universal content is subleading but whose leading
  edge Hilbert-space dimension is fixed by an additional microscopic axiom.

Those are residual positive targets. They require more structure than the
current simple-fiber free-fermion or Schur-block lanes provide.

## Relation to the Planck `c_cell = 1/4`

The Planck conditional packet proves

```text
c_cell = Tr((I_16/16) P_A) = 1/4
```

as a primitive gravitational boundary/action coefficient, and the finite-patch
extension theorem proves its additive extension once that carrier
identification is accepted. This note shows that the simple-fiber Widom
entanglement class cannot be identified with that coefficient. The two `1/4`
surfaces remain structurally different unless a new entropy carrier theorem
bridges them.

### Authority-chain provenance

The action-side `c_cell = 1/4` is no longer asserted in this note: it is
imported from the cited
[`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
where it is derived (conditional on first-order coframe locality and unit
primitive response normalization, both also cited there) as the unique
source-free, additive, coframe-slot-symmetric, unit-normalized first-order
coframe boundary carrier coefficient. The cited
[`PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM`](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
then extends this single-cell coefficient to finite boundary patches and
records the conditional carrier-share matching with `A/(4 G_Newton,lat)`.

What this no-go adds, on top of that derived action-side `1/4`, is purely the
entanglement-side bound: under the simple-fiber hypothesis,

```text
c_Widom <= 1/6 < 1/4.
```

The no-go therefore does not depend on whether the action-side `1/4` is
ultimately retained or not. It is a clean class statement about which
entanglement carriers can match any putative `1/4` action-side target, and is
agnostic to the bridge premise the cited Planck notes carry.

## What this PR is NOT

This rigorization does **not**:

- derive the Widom-Gioev-Klich coefficient formula from `A_min`. That formula
  remains an admitted universal physics input on the same footing as in the
  cited single-carrier no-go.
- close the upstream `BH_ENTROPY_DERIVED_NOTE` / `BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE`
  conditional statuses. Those remain `audited_conditional` and this note
  inherits their conditional surface.
- promote audit status. The audit ledger is not modified; status descriptor
  alignment to `audited_conditional` matches the live audit ledger entry.

## Literature anchor

The logic here uses the free-fermion Widom coefficient from Gioev-Klich and
the rigorous Widom/Sobolev line used in the retained no-go. It is positioned
against the older black-hole entanglement and holographic literature:

- Bombelli, Koul, Lee, and Sorkin, "Quantum source of entropy for black holes,"
  Phys. Rev. D 34, 373-383 (1986).
- Srednicki, "Entropy and area," Phys. Rev. Lett. 71, 666-669 (1993).
- Ryu and Takayanagi, "Holographic Derivation of Entanglement Entropy from the
  anti-de Sitter Space/Conformal Field Theory Correspondence," Phys. Rev. Lett.
  96, 181602 (2006).
- Gioev and Klich, "Entanglement Entropy of Fermions in Any Dimension and the
  Widom Conjecture," Phys. Rev. Lett. 96, 100503 (2006).
- Brandao and Horodecki, "An area law for entanglement from exponential decay
  of correlations," Nature Physics 9, 721-726 (2013).
- Swingle, "Entanglement renormalization and holography," Phys. Rev. D 86,
  065007 (2012), and Pastawski, Yoshida, Harlow, and Preskill, "Holographic
  quantum error-correcting codes: toy models for the bulk/boundary
  correspondence," JHEP 06, 149 (2015).

## Package wording

Safe wording:

> The simple-fiber Widom class is closed negatively for Planck Target 2:
> any straight-cut free-fermion carrier with at most one occupied
> `k_x`-interval per transverse momentum fiber has `c_Widom <= 1/6`, and
> Schur/direct-sum descendants remain bounded by the same convexity argument.
> An exact `1/4` entanglement carrier therefore requires either
> multi-pocket/multi-interval Fermi geometry selected by a physical law or a
> gapped horizon-sector area law with a new primitive-boundary identification.

Unsafe wording:

> No entanglement carrier on `Cl(3)/Z^3` can ever produce `1/4`.

## Verification

Run:

```bash
python3 scripts/frontier_area_law_quarter_broader_no_go.py
```

The runner checks the fiber-count identity, the `1/6` upper bound in `2D` and
`3D`, the exact half-filled diamond saturation, the sub-saturation of the
retained cubic carrier, the impossibility of `1/4` in the simple-fiber class,
and the convexity of Schur/direct-sum descendants.

Current output:

```text
SUMMARY: PASS=24  FAIL=0
c_3D(midpoint quadrature) = 0.105064
```
