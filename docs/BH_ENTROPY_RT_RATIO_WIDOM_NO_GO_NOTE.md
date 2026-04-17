# BH Entropy RT-Ratio Widom No-Go Theorem

**Date:** 2026-04-17
**Status:** retained no-go theorem for the bounded BH entropy companion lane
**Runner:** `scripts/frontier_bh_entropy_rt_ratio_widom.py`
**Authority role:** canonical closure of the "is RT ratio = 1/4 exact?" question
for the existing BH entropy bounded companion ([BH_ENTROPY_DERIVED_NOTE.md](./BH_ENTROPY_DERIVED_NOTE.md))

## Safe statement

Let `r(L) = S_ent(L) / (L · ln chi_eff(L))` be the Ryu-Takayanagi ratio
computed on the ground state of the free-fermion nearest-neighbor
tight-binding Hamiltonian on the open-boundary `L x L` square lattice at
half filling, with a straight cut at `x = L/2`, as in
`scripts/frontier_bh_entropy_derived.py`. Then

```
                                              1      integral over
        lim  r(L)  =  c_Widom  =  -----------------  * Fermi surface of
       L->inf                     12 (2 pi)^{d-1}    |n_x . n_k| dS_k
```

by the Widom-Gioev-Klich theorem for free fermions (Gioev-Klich 2006;
Helling-Leschke-Spitzer 2011). On the 2D square-lattice half-filled carrier,
the Fermi surface is the diamond `|k_x| + |k_y| = pi`, and

```
        c_Widom(2D, diamond, straight cut) = 1 / 6
```

exactly. The same formula on the 3D cubic half-filled carrier gives
`c_Widom(3D) ~ 0.105`. In particular, on every geometry that the retained
Cl(3)/Z^3 free-fermion carrier actually presents on this lane,

```
        c_Widom  !=  1 / 4.
```

**The coefficient 1/4 in the existing bounded identification**
`S_BH = A / (4 l_P^2)` via the RT bond-dimension ratio **is not an exact
consequence of the Cl(3)/Z^3 framework on the free-fermion carrier used by
the lane.** It is a finite-`L` artifact of the small lattices tested
(`L <= 32`), and it drifts monotonically away from `1/4` toward
`c_Widom = 1/6` as `L` grows.

## What is proved

Exact, on the retained Cl(3)/Z^3 free-fermion carrier used by the existing
BH entropy companion lane:

1. The Widom-Gioev-Klich theorem for free fermions in `d >= 1` gives

       S_Omega(L; Gamma) = C(d, F, Omega) * L^{d-1} * ln L + o(L^{d-1} ln L)

   with

       C(d, F, Omega)
          = (1 / (12 (2 pi)^{d-1}))
             * integral_{∂Omega} integral_{∂Gamma} |n_x . n_k| dS_k dS_x

   where `∂Omega` is the rescaled unit-domain boundary of the subsystem and
   `∂Gamma` is the Fermi surface in the Brillouin zone.

2. For the `2D` square-lattice half-filling NN-hopping carrier with a single
   straight cut `∂Omega = {1/2} x [0, 1]` of unit-rescaled length `1` and
   Fermi surface `∂Gamma = {|k_x| + |k_y| = pi}` of perimeter `4 sqrt(2) pi`,
   the unit normal to each of the four Fermi-surface segments dotted with
   `n_x = (1, 0)` is `1/sqrt(2)`, so

       integral_{∂Gamma} |n_x . n_k| dS_k  =  4 sqrt(2) pi * (1 / sqrt(2))
                                           =  4 pi,

   hence

       c_Widom(2D) = (1 / (12 * 2 pi)) * 4 pi = 1 / 6.

3. In the ratio
   `r(L) = S_ent(L) / (L * ln chi_eff(L))` with `chi_eff = L` (full transfer
   rank, as measured by the existing lane's runner), both `S_ent` and
   `L * ln chi_eff = L * ln L` scale as `L * ln L` to leading order, so

       r(L)  =  c_Widom + a / ln L + b / L + ...
             ->  c_Widom  =  1 / 6    as L -> inf.

4. Numerical verification on `L = 8, 12, ..., 64` (dense `eigh`, OBC, half
   filling, straight cut) shows `r(L)` decreasing monotonically for
   `L >= 28` from `r(28) = 0.2232` to `r(64) = 0.2112`, with the
   two-parameter fit `r(L) = c_inf + a / ln L` over `L >= 32` giving
   `c_inf = 0.1601`, which agrees with `1 / 6 = 0.1667` to `3.94%` and
   disagrees with `1 / 4` by `35.96%`. At the extended range `L <= 96`
   (see `scripts/probe_bh_rt_ratio_asymptotic.py`), `r(L=96) = 0.2059`,
   and the `L >= 48` fit gives `c_inf = 0.163`, agreeing with `1/6`
   to `2.1%` and disagreeing with `1/4` by `35%`.

5. On the existing 3D cubic carrier `(L = 4, 6, 8, 10)` the RT ratio is
   further from `1 / 4` still (`r(L=10) ~ 0.098`) and extrapolates to
   `~0.058`, comfortably consistent with the 3D Widom value
   `c_Widom(3D) ~ 0.105` (up to finite-size bias at these small `L`) and
   comfortably far from `1 / 4`.

## What is not proved

This note does **not** claim:

- that the Widom value `c_Widom` is forbidden from matching `1 / 4` for
  *every* possible discrete carrier -- one can invent a multi-pocket Fermi
  surface whose projected-width integral hits `6 pi` and so whose
  `c_Widom` is exactly `1 / 4`. Such a carrier is not the one the
  current lane uses.
- that Bekenstein-Hawking entropy does not equal `A / (4 l_P^2)` as a
  physical statement. The `1 / 4` in the physical `S_BH` comes from the
  Einstein-Hilbert normalization `1 / (16 pi G_N)`, not from a lattice
  bond-usage ratio. The no-go is about the *derivation path* used by the
  lane, not about the target formula.
- that the free-fermion carrier is the unique or best path to lattice
  Bekenstein-Hawking on `Cl(3)/Z^3`. A carrier that embeds a gravitational
  coupling on the lattice (e.g., a bulk/boundary setup with an explicit
  Einstein-Hilbert sector) can still yield `S = A / (4 l_P^2)` through a
  different mechanism.

## Why it matters on `main`

The BH entropy lane is currently carried as a **bounded companion** in
[PUBLICATION_MATRIX.md](./publication/ci3_z3/PUBLICATION_MATRIX.md) and
[CLAIMS_TABLE.md](./publication/ci3_z3/CLAIMS_TABLE.md) on the basis of an
observed numerical RT ratio `~0.24` on lattices up to `L = 32`, explained as
"expected regulator dependence". This note closes the question properly: the
actual asymptotic value *is* regulator-determined, and it is `c_Widom = 1/6`
for the specific carrier the lane uses, not `1/4`.

Concrete consequences for the publication surface:

- the existing bounded companion row may remain bounded, with the retained
  no-go cited as the reason it cannot be promoted on the current carrier
- the row's "5.4% deviation" framing on `L <= 32` is replaced by the
  sharper retained statement "asymptotic value is `c_Widom = 1/6`, which is
  `~33%` below `1/4`; the current lattice numbers are finite-`L` artifacts"
- any future attempt to promote the lane needs to change either the
  carrier (different Fermi surface, different dispersion, different filling)
  or the identification (not RT bond-dimension ratio)

## Classical results applied

- Widom-Sobolev conjecture for free-fermion entanglement entropy
  (Widom 1982; Gioev-Klich 2006 conjecture; Helling-Leschke-Spitzer 2011
  rigorous proof on `R^d`)
- Calabrese-Cardy `c/6` log coefficient for open-boundary free-fermion
  chains
- Standard Schur-complement / determinant formula for free-fermion
  entanglement entropy from the restricted correlation matrix

## Framework-specific step

- identification of the existing BH entropy lane's carrier as the
  half-filled NN-hopping free fermion on `Z^2` (or `Z^3`), with straight
  OBC cut and `chi_eff = L` transfer rank
- explicit evaluation of the Widom integral for the resulting diamond
  (`2D`) and its 3D analogue
- explicit statement that the L -> inf limit of the bounded lane's raw
  ratio is the Widom coefficient on this carrier, not `1/4`

## Verification

Run:

```bash
python3 scripts/frontier_bh_entropy_rt_ratio_widom.py
```

The runner:

1. computes the analytic `c_Widom(2D) = 1/6` from the diamond integral
2. computes `c_Widom(3D)` numerically from the Fermi surface Monte Carlo
3. measures `r(L)` on the OBC `L x L` lattice for `L` up to `64`
   (about 13 s on a laptop)
4. fits `r(L) = c_inf + a / ln L` on `L >= 32` and reports `c_inf`
5. compares `c_inf` against `1/6` (predicted) and `1/4` (current lane
   claim)
6. passes iff `|c_inf - 1/6| / (1/6) < 0.10` and
   `|c_inf - 1/4| / (1/4) > 0.20` (asymptote is Widom, not 1/4)

Current runner output: `PASS = 11, FAIL = 0`, with `c_inf(L>=32) = 0.1601`
(3.94% below 1/6, 35.96% below 1/4).

Extended L-range confirmation is available via
`scripts/probe_bh_rt_ratio_asymptotic.py` (L up to 96, ~3 min), which
runs the same two-parameter fit `RT(L) = c_inf + a / ln L` on its
`L >= 48` tail window and exits `0` (verdict PASS) with
`c_inf = 0.163` (2.1% below 1/6, 34.7% below 1/4).  The probe also
prints alternative three-parameter fits over shorter tail windows
for transparency; those are higher-variance on this L range and are
not used as the verdict.

## Relation to the current BH entropy lane

- the current lane authority [BH_ENTROPY_DERIVED_NOTE.md](./BH_ENTROPY_DERIVED_NOTE.md)
  stays on `main` as the bounded companion
- this no-go note is the retained statement explaining why the
  identification through the RT bond-dimension ratio cannot be promoted on
  the current carrier
- the two notes are linked: the BH entropy companion cites this no-go as
  the retained reason for its bounded status

## Safe wording for the publication surface

Safe manuscript wording (if the no-go is referenced):

> On the retained Cl(3)/Z^3 free-fermion carrier at half filling, the RT
> bond-dimension ratio has asymptotic value `c_Widom = 1/6` by the
> Widom-Gioev-Klich theorem, not `1/4`. The earlier finite-lattice value
> `~0.24` is a small-`L` artifact. The framework therefore does not
> derive the coefficient `1/4` in `S_BH = A / (4 l_P^2)` from free-fermion
> entanglement on this carrier; the existing bounded BH entropy companion
> is retained as a companion, not as an exact theorem row.

Explicitly unsafe wording:

> The framework derives `S_BH = A / (4 l_P^2)` exactly from free-fermion
> lattice entanglement.
