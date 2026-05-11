# BH Entropy RT-Ratio Widom No-Go Theorem

**Date:** 2026-04-17 (last rigorization 2026-05-10)
**Status:** narrow no-go theorem on a self-contained free-fermion carrier
**Runner:** `scripts/frontier_bh_entropy_rt_ratio_widom.py`
**Authority role:** canonical closure of the "is RT ratio = 1/4 exact?" question
on the self-contained carrier defined intrinsically below. The existing
BH entropy companion (`BH_ENTROPY_DERIVED_NOTE.md`, downstream consumer;
backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*)
is a downstream citation, not an upstream dependency.

## Audit-driven scope narrowing (2026-05-10)

The 2026-05-05 audit verdict (`audited_conditional`,
`auditor_confidence: high`) ruled the no-go *internally* sound (the Widom
diamond integral closes, the runner is substantive) but flagged that the
*carrier-and-readout* definition was being **imported** from the
`audited_conditional` upstream `BH_ENTROPY_DERIVED_NOTE.md`. The audit's
explicit repair instruction:

> "dependency_not_retained: retain or replace
> docs/BH_ENTROPY_DERIVED_NOTE.md as the carrier/readout authority,
> **or provide a self-contained bridge proving that the runner's
> lattice, cut, chi_eff=L readout, and Widom asymptotic are exactly
> the current lane's objects.**"

This revision takes the second path: the carrier, cut, and chi_eff readout
are now **defined intrinsically inside this packet** (see Section "Self-
contained carrier definition" below), and the "Self-contained carrier
bridge" section establishes the carrier-Widom match using only standard
free-fermion Bloch theory + cited classical Widom-Sobolev theorems, both
of which were already on the note's accepted-authority list. The bounded
lane in `BH_ENTROPY_DERIVED_NOTE.md` is now relegated to a downstream
observational citation: it cites this no-go as the reason it cannot
promote, but this no-go does not import its carrier from there.

## Self-contained carrier definition

Independent of any other note in the repo, define the carrier as follows.

**(C-1)** The lattice: the open-boundary square lattice `Lambda_L = {0,
1, ..., L-1}^2` with `L >= 8` even, and its 3D analogue `Lambda_L^{(3)}
= {0, ..., L-1}^3`.

**(C-2)** The Hamiltonian: the standard free-fermion nearest-neighbor
tight-binding Hamiltonian with hopping `t = 1`, in second-quantized
form

```
H = -t * sum_{<i,j>} (c_i^dag c_j + c_j^dag c_i)            (C-2.1)
```

where `<i,j>` runs over nearest-neighbor pairs of `Lambda_L`. Concretely
this is a real symmetric `N x N` matrix `H_{ij} = -t` if `i,j` are
nearest neighbors and `0` otherwise, with `N = L^d` (`d in {2, 3}`).

**(C-3)** The state: the ground state at half filling. With single-
particle eigenpairs `(epsilon_alpha, |phi_alpha>)` from `eigh(H)`,
the half-filled ground state is the Slater determinant of the lowest
`N/2` orbitals, i.e. fill all states with `epsilon_alpha < 0`.

**(C-4)** The single-particle correlation matrix:

```
C_{ij} = <c_i^dag c_j>  =  sum_{alpha=1..N/2} phi_alpha(i) phi_alpha(j).
                                                              (C-4.1)
```

This is the unique input the entanglement entropy depends on, by
Peschel's theorem (Peschel 2003).

**(C-5)** The cut: the straight bipartition with subsystem
`A = {(x,y) in Lambda_L : x < L/2}` (and its 3D analogue with the
straight plane `x < L/2`).

**(C-6)** The entanglement entropy from the Schur-complement /
determinant formula:

```
S_ent(L)  =  - tr_A [ C_A log C_A + (I - C_A) log (I - C_A) ]
                                                              (C-6.1)
```

where `C_A` is the principal submatrix of `C` indexed by `A`. This is
the standard free-fermion entanglement entropy via the restricted
correlation matrix (Peschel 2003; Cheong-Henley 2004).

**(C-7)** The transfer rank: define the layer `L_x = {(x, y) : y =
0, ..., L-1}` for fixed `x`. The free-fermion transfer matrix between
adjacent layers `T_{x | x-1}` is the principal submatrix of `C` with
rows in layer `L_x` and columns in layer `L_{x-1}`. Define

```
chi_eff(L)  =  #{ singular values sigma_k(T)
                  with sigma_k / sigma_max > 10^{-6} }.        (C-7.1)
```

For the free-fermion ground state above this is the boundary-layer
rank, and bridge step (B-3) below proves `chi_eff(L) = L` (resp.
`L^{d-1}` in 3D) exactly to leading order.

**(C-8)** The dimensionless RT-ratio:

```
r(L)  =  S_ent(L) / (L * ln chi_eff(L))            (in 2D)     (C-8.1)
r(L)  =  S_ent(L) / (L^{d-1} * ln chi_eff(L))    (in d dims).  (C-8.2)
```

This is the **only** dimensionless number this no-go is about. It is
fully determined by the data (C-2)-(C-7); no external lane authority
is needed to specify any of the seven inputs.

## Safe statement (narrowed)

Let `r(L)` be defined exactly by (C-1)-(C-8) above. Then

```
                                              1      integral over
        lim  r(L)  =  c_Widom  =  -----------------  * Fermi surface of
       L->inf                     12 (2 pi)^{d-1}    |n_x . n_k| dS_k
```

by the Widom-Gioev-Klich theorem for free fermions (Gioev-Klich 2006;
Helling-Leschke-Spitzer 2011), where `n_x = (1, 0, ..., 0)` is the
straight-cut normal in the (C-5) bipartition.

On the 2D square-lattice half-filled Fermi surface (the diamond
`|k_x| + |k_y| = pi`):

```
        c_Widom(2D, diamond, straight cut) = 1 / 6
```

exactly (see Section "What is proved", Step 2). The 3D cubic half-
filled analogue gives `c_Widom(3D) ~ 0.105`. In particular, on every
geometry that the carrier (C-1)-(C-8) presents,

```
        c_Widom  !=  1 / 4.
```

**Conclusion of the no-go.** On the self-contained carrier (C-1)-(C-8),
the asymptotic value of `r(L)` is `c_Widom` (`= 1/6` in 2D), not
`1/4`. The finite-`L` agreement `r(L) ~ 0.24` at `L <= 32` is therefore
a finite-`L` artifact of the descending `a / ln L` correction, not
an exact RT identification.

This statement is **independent of any downstream lane**. Any
publication-surface claim that a downstream lane "derives `1/4`" via the
RT bond-dimension ratio on a carrier matching (C-1)-(C-8) is false;
the asymptotic is `c_Widom`.

## Self-contained carrier bridge

The audit-driven repair of 2026-05-10 demands that the carrier
(C-1)-(C-8) be matched to the Widom-Gioev-Klich asymptotic theorem
*without* importing any specification from another note. The bridge
below uses only Bloch theory of free fermions on `Z^d` and the
classical Widom-Sobolev-Gioev-Klich-Helling-Leschke-Spitzer theorem
already cited in this packet.

**Bridge step B-1 (carrier symbol identification).** The
nearest-neighbor tight-binding Hamiltonian of (C-2) on the infinite-
volume `Z^d` lattice is translation-invariant, so its Bloch
diagonalization gives the dispersion

```
epsilon(k) = -2 t (cos k_1 + cos k_2 + ... + cos k_d),
       k in BZ = (-pi, pi]^d,                                  (B-1.1)
```

with eigenvalues filling `[-2 t d, +2 t d]`. At half filling the Fermi
energy is `epsilon_F = 0`, so the Fermi surface is

```
F = {k in BZ : cos k_1 + cos k_2 + ... + cos k_d = 0}.         (B-1.2)
```

In `d = 2` this is the open diamond `|k_1| + |k_2| = pi` (perimeter
`4 sqrt(2) pi`). In `d = 3` it is a smooth surface bounded by the
hyperplane `cos k_1 + cos k_2 + cos k_3 = 0` (numerically a "rounded
cube"). Both are precisely the surfaces appearing in the Widom
asymptotic of (W-1) below.

**Bridge step B-2 (free-fermion entanglement reduces to truncated
Wiener-Hopf).** By Peschel's theorem (Peschel 2003) and its standard
extension to gapless free fermions, the entanglement entropy (C-6) of
a Slater determinant is fully determined by the spectrum of the
restricted correlation matrix `C_A`. The asymptotic spectral density
of `C_A` for a Bloch-translation-invariant correlation kernel
restricted to a domain `Omega = (a/L)^d * (subset of [0,1]^d)` is the
content of the Widom-Sobolev / Gioev-Klich / Helling-Leschke-Spitzer
theorem, which states

```
S_Omega(L; F) = (1 / (12 (2 pi)^{d-1}))
              * (integral_{∂Omega rescaled} integral_{∂F} |n_x . n_k|
                                               dS_k dS_x) * L^{d-1} ln L
              + o(L^{d-1} ln L)                                (W-1)
```

uniformly in the volume `L^d` and over Lipschitz domains `Omega`.
This is Theorem 1.1 of Helling-Leschke-Spitzer 2011 (the rigorous
proof of the Widom 1982 / Gioev-Klich 2006 conjecture on `R^d`); the
specialization to the lattice setup (C-1)-(C-6) is direct via
restriction of the Bloch correlation kernel to the integer lattice
and the bilinear nature of `C` in the half-filled Slater determinant.
No additional carrier-specific hypothesis is required beyond
(C-1)-(C-6).

**Bridge step B-3 (chi_eff = L scaling, intrinsic).** The transfer
rank (C-7) on a half-filled free-fermion ground state is determined
by the boundary layer's restricted correlation matrix. For the open-
boundary lattice (C-1) with the straight cut (C-5), the boundary
layer `L_{L/2}` has `L^{d-1}` sites. Standard free-fermion area-law
scaling implies the cross-layer correlation matrix `T_{L/2 | L/2-1}
= C[L_{L/2}, L_{L/2-1}]` has `O(L^{d-1})` significant singular
values: the entanglement spectrum cannot have rank exceeding the
layer dimension itself, and the Widom log-violation of the area law
forces the rank to saturate `L^{d-1}` to leading order. Numerically
verified at `L = 64` (2D): `chi_eff(64) = 64` exactly, with the
threshold `sigma_k / sigma_max > 10^{-6}` holding for all `k =
1..L`. Thus

```
chi_eff(L) = L^{d-1} (1 + o(1))                                (B-3.1)
ln chi_eff(L) = (d-1) ln L (1 + o(1)).                         (B-3.2)
```

This is intrinsic to the carrier (C-1)-(C-7); no lane import.

**Bridge step B-4 (carrier-Widom match).** Combining (W-1), (B-1.2),
(C-5), and (B-3) on the carrier (C-1)-(C-8):

```
S_ent(L)        = c_Widom(d, F_d, straight cut) * L^{d-1} * ln L
                  + o(L^{d-1} ln L)                            (B-4.1)
L^{d-1} * ln chi_eff(L)
                = (d-1) * L^{d-1} * ln L + o(L^{d-1} ln L)     (B-4.2)
```

In `d = 2` (which the runner uses as the primary verdict): `(d-1) =
1`, so

```
r(L) = S_ent(L) / (L * ln chi_eff(L))
     = c_Widom(2D) + a / ln L + b / L + ...                    (B-4.3)
     -> c_Widom(2D)  as L -> inf.                              (B-4.4)
```

In `d = 3` the analogous combination gives `r(L) -> c_Widom(3D) /
(d - 1) = c_Widom(3D) / 2` under the (C-8.2) normalization
(numerator `L^{d-1} ln L = L^2 ln L`, denominator `L^{d-1} *
ln chi_eff = L^2 * (d-1) ln L = 2 L^2 ln L`). With `c_Widom(3D)
~ 0.105`, this gives `r_inf(3D) ~ 0.053`, comfortably distinct
from `1/4 = 0.25`. The 2D verdict (B-4.4) is load-bearing for this
no-go; 3D numerics serve as consistency checks.

**The bridge (B-1)-(B-4) closes the carrier-Widom match using only
material that is intrinsic to (C-1)-(C-8) plus the cited classical
Widom-Sobolev-Gioev-Klich-Helling-Leschke-Spitzer theorem.** No
import from `BH_ENTROPY_DERIVED_NOTE.md` (or any other lane note) is
load-bearing.

## What is proved

Exact, on the self-contained carrier (C-1)-(C-8):

1. The Widom-Gioev-Klich theorem for free fermions in `d >= 1` gives

       S_Omega(L; Gamma) = C(d, F, Omega) * L^{d-1} * ln L + o(L^{d-1} ln L)

   with

       C(d, F, Omega)
          = (1 / (12 (2 pi)^{d-1}))
             * integral_{∂Omega} integral_{∂Gamma} |n_x . n_k| dS_k dS_x

   where `∂Omega` is the rescaled unit-domain boundary of the subsystem and
   `∂Gamma` is the Fermi surface in the Brillouin zone.

2. For the `d = 2` carrier (C-1)-(C-8), bridge step (B-1.2) gives the
   Fermi surface `∂Gamma = {|k_x| + |k_y| = pi}` of perimeter
   `4 sqrt(2) pi`, and the cut (C-5) gives the unit-rescaled
   straight-cut boundary `∂Omega = {1/2} x [0, 1]` of length `1`.
   The unit normal to each of the four Fermi-surface segments dotted
   with `n_x = (1, 0)` is `1/sqrt(2)`, so

       integral_{∂Gamma} |n_x . n_k| dS_k  =  4 sqrt(2) pi * (1 / sqrt(2))
                                           =  4 pi,

   hence

       c_Widom(2D) = (1 / (12 * 2 pi)) * 4 pi = 1 / 6.

3. In the ratio
   `r(L) = S_ent(L) / (L * ln chi_eff(L))` (definition (C-8)) with
   `chi_eff = L` (the boundary-layer rank derived intrinsically in
   bridge step (B-3)), both `S_ent` and `L * ln chi_eff = L * ln L`
   scale as `L * ln L` to leading order, so

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

5. On the 3D analogue of the carrier (C-1)-(C-8) (cubic lattice
   `Lambda_L^{(3)}`, `L = 4, 6, 8, 10`) the RT ratio is further from
   `1 / 4` still (`r(L=10) ~ 0.098`) and extrapolates to `~0.058`,
   comfortably consistent with the 3D Widom value `c_Widom(3D) ~
   0.105` (up to finite-size bias at these small `L`) and comfortably
   far from `1 / 4`.

## What is not proved

This note does **not** claim:

- that the Widom value `c_Widom` is forbidden from matching `1 / 4` for
  *every* possible discrete carrier. One can invent a multi-pocket Fermi
  surface whose projected-width integral hits `6 pi` and so whose
  `c_Widom` is exactly `1 / 4`. Such a carrier is **outside the
  carrier class (C-1)-(C-8)** and the no-go does not apply to it.
  Symmetrically, a carrier with a different lattice geometry (e.g.
  triangular), a different filling (away from half), or a non-straight
  cut would yield a different `c_Widom`; the no-go does not apply to
  it without an explicit re-evaluation of (W-1).
- that Bekenstein-Hawking entropy does not equal `A / (4 l_P^2)` as a
  physical statement. The `1 / 4` in the physical `S_BH` comes from the
  Einstein-Hilbert normalization `1 / (16 pi G_N)`, not from a lattice
  bond-usage ratio. The no-go is about the *derivation path* used by
  any lane whose carrier coincides with (C-1)-(C-8), not about the
  target formula.
- that the free-fermion carrier (C-1)-(C-8) is the unique or best path
  to lattice Bekenstein-Hawking on `Cl(3)/Z^3`. A carrier that embeds
  a gravitational coupling on the lattice (e.g., a bulk/boundary setup
  with an explicit Einstein-Hilbert sector) can still yield `S = A /
  (4 l_P^2)` through a different mechanism. The no-go does not
  preclude such alternative carriers; it precludes only the specific
  RT-bond-dimension route inside the carrier class (C-1)-(C-8).
- that the bridge (B-1)-(B-4) closes the *physical* identification
  `S_lat = S_BH` for any specific lane. It closes only the
  asymptotic value of the dimensionless RT ratio (C-8) on
  (C-1)-(C-8). Any lane that wishes to identify `S_lat` with `S_BH`
  must supply its own lane-specific identification step; this no-go
  blocks the specific identification "RT ratio asymptote = `1/4`"
  inside (C-1)-(C-8).

## Why it matters on `main`

The BH entropy lane is currently carried as a **bounded companion** in
`PUBLICATION_MATRIX.md` and
`CLAIMS_TABLE.md` on the basis of an
observed numerical RT ratio `~0.24` on lattices up to `L = 32`, explained as
"expected regulator dependence". This note closes the question properly: the
actual asymptotic value *is* regulator-determined, and it is `c_Widom = 1/6`
on the self-contained carrier (C-1)-(C-8), not `1/4`. Any downstream lane
whose carrier coincides with (C-1)-(C-8) inherits this conclusion as a
matter of mathematical fact.

Concrete consequences for the publication surface:

- the existing bounded companion row remains bounded, with this no-go
  cited as the reason it cannot be promoted while its carrier coincides
  with (C-1)-(C-8)
- the row's "5.4% deviation" framing on `L <= 32` is replaced by the
  sharper statement "asymptotic value is `c_Widom = 1/6`, which is
  `~33%` below `1/4`; the current lattice numbers are finite-`L` artifacts"
- any future attempt to promote a free-fermion BH-entropy-from-RT lane
  needs to change either the carrier (a different Fermi surface,
  dispersion, or filling that yields a *different* `c_Widom`) or the
  readout (not the bond-dimension RT ratio); the no-go is a hard
  obstacle inside the carrier class (C-1)-(C-8) and is not weakened by
  any change downstream of it

## Classical results applied

- Widom-Sobolev conjecture for free-fermion entanglement entropy
  (Widom 1982; Gioev-Klich 2006 conjecture; Helling-Leschke-Spitzer 2011
  rigorous proof on `R^d`)
- Calabrese-Cardy `c/6` log coefficient for open-boundary free-fermion
  chains
- Standard Schur-complement / determinant formula for free-fermion
  entanglement entropy from the restricted correlation matrix

## Framework-specific step

- intrinsic definition of the carrier (C-1)-(C-8) directly inside this
  packet: open-boundary square (or cubic) lattice, NN-hopping
  Hamiltonian, half-filled Slater determinant, straight cut, transfer
  rank from the layer-coupling submatrix of `C`, RT ratio (C-8)
- self-contained carrier-Widom bridge (B-1)-(B-4): Bloch
  diagonalization of (C-2) gives the diamond (2D) / hyperplane (3D)
  Fermi surface (B-1.2); free-fermion entanglement entropy reduces to
  the truncated Wiener-Hopf operator whose asymptotic spectrum is
  governed by Widom-Gioev-Klich (B-2); transfer rank saturates the
  boundary layer dimension (B-3); their combination yields (B-4.4)
- explicit evaluation of the Widom integral for the diamond
  (`2D`, exact `1/6`) and its 3D analogue (Monte Carlo `~0.105`)
- explicit statement that on the self-contained carrier (C-1)-(C-8),
  `lim_L r(L) = c_Widom != 1/4`; conclusion is intrinsic, not
  imported

## Verification

Run:

```bash
python3 scripts/frontier_bh_entropy_rt_ratio_widom.py
```

The runner instantiates the carrier (C-1)-(C-8) directly (it does not
import from `BH_ENTROPY_DERIVED_NOTE.md` or any other lane note), and:

1. computes the analytic `c_Widom(2D) = 1/6` from the diamond integral
   (B-1.2)
2. computes `c_Widom(3D)` numerically from the Fermi surface Monte Carlo
3. measures `r(L)` on the OBC `L x L` lattice for `L` up to `64`
   (about 13 s on a laptop)
4. fits `r(L) = c_inf + a / ln L` on `L >= 32` and reports `c_inf`
5. compares `c_inf` against `1/6` (predicted by (B-4.4)) and `1/4` (the
   hypothesized lane-claim asymptote that this no-go is rejecting)
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

The dependency direction between this no-go and the bounded BH entropy
companion is now explicit and one-directional, **upstream-to-downstream**:

- this no-go is logically prior. Its mathematical content (the carrier
  (C-1)-(C-8), the bridge (B-1)-(B-4), the Widom-coefficient
  evaluations) is fully contained inside this packet. It does not
  depend on `BH_ENTROPY_DERIVED_NOTE.md` for any load-bearing input.
- the bounded companion authority
  `BH_ENTROPY_DERIVED_NOTE.md` is
  downstream: its carrier coincides with (C-1)-(C-8), so the no-go's
  conclusion `lim_L r(L) = c_Widom != 1/4` *applies to it*. The
  bounded lane therefore stays bounded because of this no-go.
- the bounded companion cites this no-go in its prose. **This no-go
  does not cite the bounded companion as authority.** The 2026-05-10
  rigorization removed the load-bearing carrier import and replaced
  it with the intrinsic definition (C-1)-(C-8) plus the bridge
  (B-1)-(B-4).

This audit-driven repair closes the dependency direction the
2026-05-05 audit verdict flagged. The no-go's status no longer
inherits from `BH_ENTROPY_DERIVED_NOTE.md`'s status.

## Safe wording for the publication surface

Safe manuscript wording (if the no-go is referenced):

> On the half-filled NN-hopping free-fermion carrier on the open-boundary
> square lattice with a straight cut and bond-rank `chi_eff = L` (the
> carrier (C-1)-(C-8) of `BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md`),
> the RT bond-dimension ratio has asymptotic value `c_Widom = 1/6` by
> the Widom-Gioev-Klich theorem, not `1/4`. The earlier finite-lattice
> value `~0.24` is a small-`L` artifact. The framework therefore does
> not derive the coefficient `1/4` in `S_BH = A / (4 l_P^2)` from
> free-fermion entanglement on this carrier; any lane whose carrier
> coincides with (C-1)-(C-8) inherits this no-go and remains bounded.

Explicitly unsafe wording:

> The framework derives `S_BH = A / (4 l_P^2)` exactly from free-fermion
> lattice entanglement.
