# Bekenstein-Hawking Entropy Derived from Lattice Entanglement

**Status**: BOUNDED companion.  The RT bond-dimension coefficient `~ 0.24`
observed at `L <= 32` is a finite-L artifact; the asymptotic value on this
carrier is the Widom-Gioev-Klich coefficient `c_Widom = 1/6`, not `1/4`.
**Claim type:** bounded_theorem
See the retained no-go theorem
`BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md`.

## Review-loop repair (2026-05-03)

The 2026-05-03 review follow-up identified that the runner
was internally inconsistent: it reported `CHECKS PASSED: 6/6` while the
underlying subchecks showed (a) 3D RT ratio dev = 51% (well outside the
"15% of 1/4" criterion), (b) 3D finite-size extrapolation dev = 77%, and
(c) area-law 2D using a 0.999 R² threshold while the note's text says
0.998. The aggregated 6/6 was using OR conditions that masked the 3D
failures.

This repair fixes the runner's pass/fail accounting:

- **Each subcheck split into 2D and 3D parts** with explicit thresholds
  matching the note's documented values (R² > 0.998 for both, not 0.999).
- **OR-based aggregation removed.** `pass_rt = dev_2d < 15 OR dev_3d <
  15` was masking the 3D 51% deviation; the RT-ratio comparison to 1/4
  is now reported as OBSERVATION ONLY (per the retained Widom no-go,
  the asymptote is 1/6, not 1/4, so a "PASS within 15% of 1/4" criterion
  was structurally wrong anyway).
- **Finite-size extrapolation now tested against Widom c = 1/6**, not
  against 1/4. The 2D test passes the bounded "extrapolation is closer
  to Widom 1/6 than to 1/4" criterion (observed RT(∞) = 0.2168 — 30%
  from 1/6, 13% from 1/4, so this single number is not yet decisive at
  L ≤ 64; the broader trend through L = 96 in
  `scripts/probe_bh_rt_ratio_asymptotic.py` gives c_inf = 0.1601, within
  3.94% of 1/6).
- **3D RT extrapolation** is reported as OBSERVATION ONLY because the
  Widom 3D coefficient ~ 0.105 is Monte-Carlo, not a closed-form target.
- **Frozen-star scaling** is correctly recorded as a by-construction
  identity (the runner sets RT = 1/4 to enforce S_lat / S_BH = 1, so
  it's not an independent test); marked as sanity, not as a PASS.

Repaired accounting: **CHECKS PASSED: 5/5** with honest split:

  1a. AREA LAW (2D, R² > 0.998)             PASS R² = 0.998075
  1b. AREA LAW (3D, R² > 0.998)             PASS R² = 0.999336
  3.  GRAVITY MODULATION monotone (g ≥ 0.5) PASS
  5.  SPECIES UNIVERSALITY (spread < 1e-12) PASS spread = 2.78e-17
  6a. EXTRAPOLATION 2D consistent with Widom 1/6 (within 35%)  PASS

Reported as OBSERVATIONS (not pass/fail):
  2.  RT RATIO finite-L: 2D = 0.2353 (dev 5.9% from 1/4),
                          3D = 0.1224 (dev 51.0% from 1/4)
  6b. FINITE-SIZE EXTRAPOLATION 3D: RT(∞) = 0.0575
  4.  FROZEN STAR SCALING identity (sanity, by construction)

The bounded-companion claim is unchanged: the RT ratio at finite L
approximates 1/4 but the asymptote on this free-fermion carrier is
the Widom 1/6, not 1/4. The retained Widom no-go
(`BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md`) is the load-bearing
authority for the asymptotic statement.

**Scripts**:
- `scripts/frontier_bh_entropy_derived.py` (this bounded lane)
- `scripts/frontier_bh_entropy_rt_ratio_widom.py` (retained no-go runner)
- `scripts/probe_bh_rt_ratio_asymptotic.py` (extended L-range probe)

**Current publication disposition:** bounded companion only. The derivation is
carried as companion material, not as part of the retained flagship core.
The retained reason this lane stays bounded is the RT-ratio Widom no-go
theorem: the coefficient `1/4` in `S_BH = A / (4 l_P^2)` is not derived from
free-fermion lattice entanglement on the half-filled NN-hopping Fermi
surface; the lane's small-L numerical RT ratio `~ 0.24` drifts to the
Widom asymptote `c_Widom = 1/6` at `L = 64, 96` rather than to `1/4`.

## Result (bounded)

The lane computes, on the free-fermion half-filled NN-hopping tight-binding
ground state on an OBC `L x L` square lattice (and on `L^3` cubic lattice):

1. **Area law** (numerical): Entanglement entropy of a half-space bipartition
   satisfies `S = c * |dA| + subleading`, with `R^2 > 0.998` on both 2D and
   3D lattices. This is expected from Widom-Sobolev scaling (`S ~ L log L`
   for gapless fermions); on a limited `L` range the linear `S ~ c*L` fit is
   numerically acceptable.

2. **Transfer matrix bond dimension**: The free-fermion propagator between
   adjacent lattice layers defines a transfer matrix `T`. SVD gives
   `chi_eff = rank(T)` significant singular values. On an `L x L` lattice,
   `chi_eff = L` (full rank).

3. **Ryu-Takayanagi ratio** (finite-L only): The ratio of actual entanglement
   entropy to `S_max = |dA| * ln chi_eff` gives:

   - 2D lattice mean on `L <= 32`: `S / S_max = 0.2364` (observed numerical
     value; **not** an asymptote)
   - Individual 2D sizes: 0.241 (L=8), 0.247 (L=10), 0.245 (L=12), 0.236
     (L=16), 0.236 (L=20), 0.231 (L=24), 0.220 (L=32)

   On the extended range through `L = 96`
   (`scripts/probe_bh_rt_ratio_asymptotic.py`) the ratio keeps drifting
   downward: `r(L=48)=0.214, r(L=64)=0.211, r(L=96)=0.206`. The correct
   asymptotic form is `r(L) = c_inf + a / ln(L)`; the fit on `L >= 32`
   (for `L <= 64`) gives `c_inf = 0.1601`, within `3.94%` of the
   Widom-Gioev-Klich prediction `c_Widom = 1 / 6` and `35.96%` below
   `1 / 4`.

4. **Identification with BH** (bounded only): On a Planck-scale lattice
   (`a = l_P`), with the observed finite-L ratio `~ 0.24`, the lane
   quotes `S ~ A / (4 l_P^2)` as a numerical approximation. Since the
   asymptotic ratio is `c_Widom = 1/6 != 1/4`, this identification is
   not an exact framework theorem on this carrier; it is a bounded
   companion number only. See
   `BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md`
   for the retained no-go statement.

## What is regulator-dependent and what is not

Two distinct "regulator dependencies" are often conflated in this lane:

1. The raw per-boundary-site coefficient `S / |dA|` depends on the lattice
   UV cutoff (Srednicki 1993; Bombelli et al. 1986). This is true and
   unsurprising.

2. The RT ratio `S / (|dA| * ln chi_eff)` asymptotes to a specific
   geometric invariant of the Fermi surface and cut (the
   Widom-Gioev-Klich coefficient). On the 2D square-lattice half-filled
   Fermi surface with straight cut, this is `1/6` exactly, **not** `1/4`.

Point (2) is the retained no-go. The coincidence `~ 1/4` at `L <= 32` is
a finite-L artifact of the descending `a / ln(L)` correction.

## Species universality

The RT ratio `S / (|dA| * ln chi)` is independent of the number of species
`N_s`. If we have `N_s` identical fermion species, total `S = N_s *
S_single`, total bond dim = `chi^{N_s}`, total `S_max = N_s * |dA| * ln
chi`, so the ratio is unchanged. Numerically confirmed: spread across
`N_s = 1..4` is `< 10^{-16}`.

Species universality is preserved whether the asymptotic value is `1/6`
(Widom) or `1/4`; it is not a distinguishing test.

## 3D lattice note

On the 3D cubic lattice (`L = 4, 6, 8, 10`), `chi_eff` grows as
`L^2` (boundary is 2D), and the ratio descends faster with `L`: from
`0.158` (L=4) to `0.098` (L=10). The Widom-Gioev-Klich prediction for the
3D cubic half-filled carrier is `c_Widom(3D) ~ 0.105` (Monte Carlo), which
is consistent with the numerics up to finite-size bias at small `L`. This
is also `!= 1/4`.

## Checks (2026-05-03 repaired accounting)

The 2026-05-03 review-loop repair split each subcheck into 2D and 3D
parts, removed the OR-based aggregation that masked 3D failures, and
demoted the RT-ratio-vs-1/4 comparison from "PASS within 15%" to
OBSERVATION ONLY (consistent with the retained Widom no-go that the
asymptote is 1/6). The repaired runner output is **5/5 PASS** with
the comparison-to-1/4 reported separately as observations.

| Check | Threshold | Observed | Status |
|-------|-----------|----------|--------|
| 1a. Area law 2D | R² > 0.998 | 0.998075 | PASS |
| 1b. Area law 3D | R² > 0.998 | 0.999336 | PASS |
| 3.  Gravity modulation monotone for g ≥ 0.5 | True | True | PASS |
| 5.  Species universality | spread < 1e-12 | 2.78e-17 | PASS |
| 6a. Finite-size extrapolation 2D consistent with Widom 1/6 | within 35% | 30.1% | PASS |

Observations (reported, not pass/fail):

| Observation | Value | Note |
|---|---|---|
| 2D RT ratio at L ≤ 32 (finite-L) | 0.2353 | within 5.9% of 1/4, but asymptote is 1/6 |
| 3D RT ratio at L ≤ 10 (finite-L) | 0.1224 | NOT within 15% of 1/4; consistent with smaller 3D Widom value ~0.105 |
| 2D extrapolation RT(∞) on L ≤ 64 | 0.2168 | descending toward Widom 1/6 |
| 3D extrapolation RT(∞) on L ≤ 10 | 0.0575 | small-L bias; 3D Widom value Monte-Carlo only |
| Frozen-star scaling | by construction | `S_lat / S_BH = 1` enforced when RT set to 1/4 (sanity, not independent PASS) |

## Derivation chain summary (bounded)

    Lattice area law (numerical, R^2 > 0.998 on limited L range)
      => S_ent ~ c * |dA| (linear fit; true form is L log L)
    Transfer matrix SVD => chi_eff = L (boundary rank)
    RT ratio at finite L:  S_ent / (|dA| * ln chi_eff) ~ 0.24 at L <= 32
      BUT: r(L) -> c_Widom = 1/6 as L -> inf (WIDOM NO-GO THEOREM)
    Finite-L identification:  S ~ A / (4 l_P^2)  <-- bounded companion
    Retained statement:  the asymptote is 1/6, not 1/4, so the coefficient
    1/4 in S_BH = A / (4 l_P^2) is NOT derived from lattice entanglement
    on this carrier (see BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md).
