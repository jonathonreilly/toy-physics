# 3+1D SO(3,1) Boost Covariance of the Path-Sum 2-Point Function

**Date:** 2026-04-25
**Status:** proposed_retained exact theorem on the continuum-limit free-scalar
Hamiltonian-lattice surface, with explicit dim-6 cubic-harmonic LV bound
at finite `a`
**Script:** `scripts/frontier_lorentz_boost_3plus1d.py` (PASS=55, FAIL=0)
**Companions:**
[LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md),
`ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md`,
[EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)

## Audit-status note (2026-05-09)

The 2026-05-05 audit verdict (`audited_conditional`, chain_closes=false)
ratified the narrow free-scalar continuum-limit covariance core but
flagged that the full retained claim imports dim-6 LV inheritance,
CPT/P protection, and Planck-scale suppression from cited authorities
that are themselves not retained-grade. Specifically:

- [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
  is `audited_conditional` (now narrowed to bounded conditional
  structural-dispersion support per the PR #803 salvage).
- [LIGHT_CONE_FRAMING_NOTE.md](LIGHT_CONE_FRAMING_NOTE.md) is
  `audited_conditional` (Lieb-Robinson framing only; finite-`a` cone
  diagnostic now bounded via the PR #816 Crank-Nicolson companion).
- [LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md)
  is `audited_conditional` (blocked on the same emergent-Lorentz cite).
- `PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md` (see-also; converted
  from markdown link to backticked form 2026-05-10 to break citation
  cycle-0014, the 13-node anomaly_forces_time ring, and cycle-0015,
  the 14-node ring that adds the angular-kernel companion — the Planck
  pin status note is a status-tracking external lane reference, not a
  load-bearing input to Steps 1–8 of the proof below; the theorem
  itself operates on the free-scalar Hamiltonian-lattice continuum
  limit and does not import Planck-scale claims) is
  `audited_conditional` (current package pin, not yet a theorem).

Blocked-on: this 3+1D boost-covariance result therefore stays
audited-conditional until each of the four cited authorities advances
to retained-grade. The free-scalar Hamiltonian-lattice continuum core
(Steps 1–6 below, plus Step 8 combined SO(3,1) statement at the
free-scalar level) is unaffected by this status note; the change is
purely upstream propagation accounting on the dim-6 LV inheritance
(Step 7), CPT/P protection citations, and the Planck-suppression
phenomenological table.

## Theorem

**Theorem (3+1D SO(3,1) boost covariance, Phase 4).**
Let `W_lat(Δt, Δx⃗; a, m)` be the free-scalar Wightman 2-point function
on a 3+1D Hamiltonian lattice with spatial spacing `a` and bare mass `m`,

```text
W_lat(Δt, Δx⃗; a, m) = ∫_BZ d^3p/(2π)^3
                          * exp(-i E_lat(p) Δt + i p⃗·Δx⃗) / (2 E_lat(p)),
```

with the bosonic Laplacian dispersion

```text
E_lat^2(p) = m^2 + sum_i (4/a^2) sin^2(p_i a / 2).
```

Then in the continuum limit `a -> 0` with `(Δt, Δx⃗, m)` held fixed in
physical units,

```text
W_lat(Δt, Δx⃗; a, m)  ->  W_cont(s^2; m)
                          := m K_1(m sqrt(-s^2)) / (4π² sqrt(-s^2))
```

for spacelike separations `s^2 = Δt^2 - |Δx⃗|^2 < 0`. The continuum
limit `W_cont` depends on `(Δt, Δx⃗)` only through the SO(3,1) invariant
`s^2`, hence the path-sum 2-point function is fully SO(3,1) boost-
covariant in the continuum limit.

At finite `a > 0`, the leading boost-covariance violation is the
cubic-harmonic dim-6 LV correction inherited from
[EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md):
`W_lat` is `O_h`-covariant but not strictly SO(3,1)-covariant, with
finite-`a` violation suppressed as `(a^2 p^4)/E^2`. On the retained
hierarchy surface `a ~ 1/M_Pl` this is `(E/M_Pl)^2`, well below all
current experimental sensitivity.

This is the 3+1D analogue of
[LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md)
and **strictly extends** the dispersion-isotropy theorem: where the
dispersion theorem closes the on-shell relation `E^2(p)`, this closes
the **off-shell 2-point function** itself.

## Why this matters

The dispersion-isotropy theorem
[EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
(37/37 PASS) shows the leading dispersion is `E^2 = p^2` plus a
Planck-suppressed dim-6 cubic-harmonic correction. That is a statement
about the *on-shell relation* `E(p)`, not about the **two-point function**
`W(Δt, Δx⃗)`.

The Phase 4 theorem lifts the claim from on-shell to off-shell:

> The continuum-limit 2-point Wightman function on `Cl(3)/Z^3 x R` is
> exactly SO(3,1)-covariant, depends only on `s^2`, and has the closed
> form `m K_1(m sqrt(-s^2))/(4π² sqrt(-s^2))` for spacelike separations.

This converts the emergent-Lorentz program from "the dispersion is
isotropic at leading order with bounded LV corrections" into "the full
two-point correlator transforms as a Lorentz scalar in the continuum
limit". That is the relativistic-invariance statement Nature-class
referees expect to see.

## Proof structure

### Step 1 -- Microscopic spacetime symmetry is `O_h x Z`

The 3+1D `Z^3 x Z` lattice (Hamiltonian formulation: `Z^3` spatial,
continuous time evolution by the Laplacian) has microscopic spacetime
symmetry group

```text
G_micro = O_h (cubic point group, 48 elements) x R (time translations).
```

There is no microscopic boost. SO(3,1) is **non-compact** and cannot
live as a finite lattice automorphism. Boost covariance must emerge in
the continuum limit or not at all (cf. Bombelli-Henson-Sorkin 2009 for
the causal-set analogue with Poisson sprinkling).

### Step 2 -- Lattice dispersion is `O_h`-symmetric and parity-even

Direct verification (runner Part 1):

- `E_lat(p)` invariant under cubic permutations of `(p_x, p_y, p_z)`;
- `E_lat(p)` invariant under per-axis sign flips `p_i -> -p_i`;
- All 48 `O_h` group elements are exact symmetries.

Together with `CPT` and `P` exactness on even periodic `Z^3`
(`CPT_EXACT_NOTE`, retained), this forbids:

- dim-3 LV operators (CPT-odd, mass-like);
- dim-5 LV operators (P-odd);
- all CPT-odd SME coefficients.

The leading allowed lattice LV operator is therefore dim-6.

### Step 3 -- Continuum dispersion is the unique relativistic limit

Taylor-expanding `(4/a^2) sin^2(p_i a / 2)` for `p_i a << 1`:

```text
(4/a^2) sin^2(p_i a / 2) = p_i^2 - (a^2/12) p_i^4 + O(a^4 p_i^6).
```

Summing over `i = 1, 2, 3`:

```text
E_lat^2(p) = m^2 + |p⃗|^2 - (a^2/12) sum_i p_i^4 + O(a^4 p^6).
```

The leading correction `sum_i p_i^4` is the cubic harmonic at `l = 4`
(see EMERGENT_LORENTZ_INVARIANCE_NOTE Step 4 for the
`Σn_i⁴ = 3/5 + (4/5) K_4` decomposition with `K_4 = Y_{40} + sqrt(5/14)
(Y_{4,4} + Y_{4,-4})`).

In the strict continuum limit `a -> 0`, `E_lat^2 -> m^2 + |p⃗|^2`, the
unique `SO(3) x R`-invariant relativistic dispersion. The convergence is
`O(a^2)` (verified numerically: at `p = 0.5`, `m = 1`, `a = 0.01`, the
relative error matches the predicted `(a^2 p^4)/(12 E^2) = 4.17e-7` to
two significant figures).

Verified runner check 1.4: at `a = 0.5`, `p = 0.5`,
`E^2([100]) - E^2([111]) = -8.66e-4` matches the predicted
`-(a^2 p^4)/18 = -8.68e-4` to 0.3% (the cubic-anisotropy split between
axis and diagonal directions).

### Step 4 -- 3+1D Lorentz-invariant on-shell measure

Under SO(3,1) boost along an arbitrary unit vector `n̂` with rapidity `η`,

```text
(E', p⃗') = (cosh(η) E + sinh(η) (n̂·p⃗),
            sinh(η) E n̂ + p⃗ + (cosh(η) - 1)(n̂·p⃗) n̂),
```

the on-shell measure `d^3p / (2 E_p)` is invariant
(Liouville-invariant measure on the mass-shell hyperboloid). The
runner verifies (Part 2):

- mass-shell preserved `E'^2 - |p⃗'|^2 = m^2 = E^2 - |p⃗|^2` to machine
  precision under boosts along `[1,0,0]`, `[1,1,0]`, `[1,1,1]` (cubic
  diagonal), and arbitrary `[1, 0.5, 0.3]`;
- boost composition `B(η_1) B(η_2) = B(η_1 + η_2)` along the same axis
  (the non-Abelian structure for boosts along different axes appears as
  a Wigner rotation, also automatic);
- reverse boost `B(-η) B(η) = identity`.

### Step 5 -- Continuum 2-point function depends only on `s^2`

Substituting `(E, p⃗) -> (E', p⃗')` in the continuum integral

```text
W_cont(Δt, Δx⃗; m) = ∫ d^3p/(2π)^3 * exp(-i E(p) Δt + i p⃗·Δx⃗) / (2 E(p))
```

and using the invariant measure, the integral transforms covariantly to

```text
W_cont(Δt', Δx⃗'; m) = ∫ d^3p'/(2π)^3 * exp(-i E'(p') Δt' + i p⃗'·Δx⃗')
                          / (2 E'(p'))
```

with `(Δt', Δx⃗')` the SO(3,1) boost of `(Δt, Δx⃗)` by `-η n̂`. Therefore
`W_cont(Δt, Δx⃗) = W_cont(Δt', Δx⃗')`.

The closed form (standard 3+1D massive scalar Wightman function for
spacelike separation) is

```text
W_cont(Δt, Δx⃗; m) = m K_1(m sqrt(-s^2)) / (4π² sqrt(-s^2)),
                                          s^2 = Δt^2 - |Δx⃗|^2 < 0,
```

with `K_1` the modified Bessel function of the second kind. Manifestly
SO(3,1)-covariant.

The runner verifies (Part 3) this analytic form to relative error
`3.2e-9` against radial oscillatory quadrature across 5 spacelike radii.

### Step 6 -- Lattice -> continuum convergence (Euclidean Schwinger function)

Direct numerical verification of `W_lat -> W_cont` in Lorentzian signature
is hampered by Minkowski oscillation (the integrand `exp(-i E_lat Δt)`
oscillates rapidly over the BZ for `Δt > 0`). The standard lattice-QFT
workaround is the Euclidean Schwinger function

```text
G_E(τ, Δx⃗; m) = ∫_BZ d^3p/(2π)^3 * exp(-E_lat(p) τ + i p⃗·Δx⃗) / (2 E_lat(p)),
```

with continuum limit

```text
G_E_cont(τ, Δx⃗; m) = m K_1(m R)/(4π² R),    R = sqrt(τ^2 + |Δx⃗|^2),
```

which is SO(4)-rotation invariant. Lorentzian boost covariance of `W`
is equivalent to SO(4) Euclidean rotation invariance of `G_E` via Wick
rotation `t -> -i τ`, and `G_E` is well-conditioned numerically.

Runner Part 4 verifies:

| `a` | `|G_E_lat - G_E_cont|/G_E_cont` at `(τ, dx⃗) = (2, (1,0,0))` |
|-----|-------------------------------------------------------------|
| 0.4 | 2.40e-2                                                     |
| 0.2 | 5.39e-3                                                     |
| 0.1 | 1.34e-3                                                     |

Convergence is monotone, ratio per halving consistent with `O(a^2)`.

The SO(4) Euclidean rotation invariance is verified directly:
`G_E_lat(τ=2, dx=(1,0,0))` and `G_E_lat(τ=1, dx=(2,0,0))` (both at
Euclidean radius `R = sqrt(5)`) agree to relative spread `4.1e-3` at
`a = 0.2`, fully consistent with `O(a^2)` continuum convergence.

The Lorentzian `W_lat(Δt = 0, ·)` is also tested directly (no Minkowski
oscillation in the spacelike `Δt = 0` slice) and converges with the
same `O(a^2)` rate.

### Step 7 -- Cubic-harmonic LV at finite `a` (inherited from dispersion theorem)

At finite `a > 0`, the lattice 2-point function is *not* strictly
SO(3,1)-covariant: it inherits the dim-6 cubic-harmonic LV operator from
the lattice dispersion. Direct verification (runner Part 6, Euclidean):

| `a` | `|G_E([100]) - G_E([111])|` at `r = 1.5`, `τ = 1` |
|-----|---------------------------------------------------|
| 0.4 | 1.35e-4                                           |
| 0.3 | 1.18e-4                                           |
| 0.2 | 4.87e-5                                           |

The anisotropy decreases under `a`-refinement, with the smallest-`a`
relative anisotropy `1.9%` of the continuum value. The angular pattern
follows the cubic harmonic `K_4` with the factor-of-3 anisotropy
between axis `[1,0,0]` and diagonal `[1,1,1]/sqrt(3)` directions
(`f_4 = sum_i n_i^4 = 1` along axis, `1/3` along diagonal -- exact
ratio 3, verified to machine precision).

This is exactly the LV signature predicted by EMERGENT_LORENTZ_INVARIANCE,
now manifest at the 2-point function level.

### Step 8 -- Combined SO(3,1) statement

Steps 1-7 together prove the Phase 4 theorem:

> Octahedral cubic symmetry plus continuous time translation, combined
> with the relativistic continuum dispersion `E^2 = m^2 + |p⃗|^2`
> (recovered as the unique `a -> 0` limit), imply that the continuum-limit
> path-sum 2-point function is fully SO(3,1) boost-covariant, depending
> only on the invariant interval `s^2`, with closed form
> `m K_1(m sqrt(-s^2))/(4π² sqrt(-s^2))` for spacelike separations and
> finite-`a` LV correction at the dim-6 cubic-harmonic K_4 angular
> structure.

## What is and is not claimed

### What is claimed

- **Continuum limit, free scalar.** The free-scalar 2-point function on
  the 3+1D Hamiltonian lattice (`Z^3` spatial, continuous time)
  converges in the continuum limit to the standard SO(3,1)-covariant
  Wightman function.
- **Spacelike form.** For `s^2 < 0` the limit is exactly
  `m K_1(m sqrt(-s^2)) / (4π² sqrt(-s^2))`.
- **Mechanism.** The covariance follows from
  (a) `O_h`-symmetry and parity-evenness of the lattice dispersion,
  (b) `O(a^2)` convergence of the lattice dispersion to the relativistic
      dispersion,
  (c) SO(3,1) invariance of the on-shell Liouville measure `d^3p/(2 E_p)`,
  (d) standard Källén-Lehmann reduction in the continuum.
- **Finite-`a` LV correction.** Directly inherited from the dispersion
  theorem: dim-6, cubic harmonic `K_4` angular structure, factor-of-3
  anisotropy between `[100]` and `[111]/sqrt(3)`, Planck-suppressed on
  the retained `a ~ 1/M_Pl` hierarchy surface.
- **Decoupling from angular kernel.** Phase 4 lives entirely on the
  staggered/Laplacian Hamiltonian construction, which has no angular-
  kernel parameter. The directional-measure walk
  (`ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md`)
  does not enter.

### What is NOT claimed

- **Finite-`a` boost covariance.** The lattice 2-point function at any
  finite `a > 0` is NOT strictly SO(3,1)-covariant: it has explicit
  cubic-harmonic LV at the dim-6 level. Only the strict continuum limit
  is fully covariant.
- **Interacting theory.** The proof is for the free scalar; interactions
  may introduce loop-level lattice corrections that need separate
  treatment (standard lattice-QFT renormalisation).
- **Timelike Wightman form.** The runner verifies the spacelike Macdonald
  form. The timelike `s^2 > 0` form requires the standard `iε`
  prescription and gives Hankel functions, related to the spacelike
  result by analytic continuation.
- **Strict v=1 light cone at finite `a`.** Standard lattice-QFT result
  ([LIGHT_CONE_FRAMING_NOTE.md](LIGHT_CONE_FRAMING_NOTE.md)): the
  Lieb-Robinson cone at finite `a` differs from the strict cone by an
  exponentially small tail. Only the continuum limit recovers a strict
  cone, via the on-shell maximal velocity `v_max = 1` of the relativistic
  dispersion.
- **Promotion of Planck-pin to a theorem.** The retained
  `PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md` (see-also; converted
  from markdown link to backticked form 2026-05-10 to break citation
  cycle-0014 / cycle-0015 — this is a caveat / future-work reference
  about the Planck pin status, not a load-bearing premise of the Phase
  4 theorem)
  posture is that `a^(-1) = M_Pl` is a current package pin, not yet a
  theorem. Phase 4 inherits this caveat for any phenomenological
  conversion to physical units.

## Relation to existing notes

| Note                                      | Dimension | Covariance level             | This note's relation        |
|-------------------------------------------|-----------|------------------------------|-----------------------------|
| `EMERGENT_LORENTZ_INVARIANCE_NOTE`        | 3+1D      | dispersion isotropy          | strict extension            |
| `LORENTZ_BOOST_COVARIANCE_2D_THEOREM`     | 1+1D      | full SO(1,1) on 2-pt         | 3+1D analogue               |
| `ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO` | -         | Phase 3 decoupling           | applies (kernel irrelevant) |
| `LORENTZ_VIOLATION_DERIVED_NOTE`          | 3+1D      | bounded dim-6 LV companion   | unchanged (companion only)  |
| `LIGHT_CONE_FRAMING_NOTE`                 | -         | Lieb-Robinson framing        | unchanged                   |
| `LATTICE_NN_LIGHT_CONE_NOTE`              | -         | retired (topological only)   | unchanged                   |

This note **strictly extends** the dispersion theorem: every PASS check
in `frontier_emergent_lorentz_invariance.py` remains valid; this note
adds the off-shell 2-point function statement. It does NOT supersede
any retained note.

## Relation to the literature

- **Bombelli-Lee-Meyer-Sorkin 1987 / Bombelli-Henson-Sorkin 2009**
  (causal sets): SO(3,1) Lorentz invariance achieved at the lattice
  scale by Poisson sprinkling. Phase 4 instead proves the standard
  lattice-QFT continuum-limit version: full SO(3,1) on a regular `Z^3`
  lattice in the continuum limit, with explicit dim-6 LV at finite `a`.
- **Wiese; Rothe; Montvay-Münster** (lattice QFT references): the
  underlying lattice-QFT continuum-limit machinery is standard. This
  note is the rigorous statement of "continuum-limit Lorentz invariance"
  for the framework's path-sum 2-point function, with explicit closed
  form `m K_1/(4π²r)` and explicit characterisation of the leading
  finite-`a` LV correction.
- The combined statement -- exact SO(3,1) covariance of the continuum
  2-point function on `Cl(3)/Z^3` -- is the publication-grade upgrade
  from "isotropic dispersion" to "Lorentz-covariant correlators" that
  the boost-covariance Phase 4 program was designed to deliver.

## What this changes in the program

This theorem upgrades the "Lorentz from discrete" claim in `Cl(3)/Z^3`
from

> "the leading on-shell dispersion is isotropic, and the first LV
> correction is dim-6 Planck-suppressed" (dispersion-level, on-shell)

to

> "the continuum-limit 2-point function transforms as a Lorentz scalar
> under the full SO(3,1) group, with closed form
> `m K_1(m sqrt(-s^2))/(4π² sqrt(-s^2))` for spacelike separations and
> dim-6 cubic-harmonic K_4 LV at finite `a`" (correlator-level,
> off-shell)

The 1+1D and 3+1D statements together close the boost-covariance Phase
2/4 program. The Phase 3 angular-kernel question is closed as a no-go
plus decoupling. The full four-phase program lands the boost-covariance
upgrade for the emergent-Lorentz lane.

## Verification

```bash
python3 scripts/frontier_lorentz_boost_3plus1d.py
# PASS=55  FAIL=0
# Exit code: 0
```

The 55 checks span 8 parts:

| Part | Coverage                                                            | PASS |
|------|---------------------------------------------------------------------|------|
| 1    | 3D lattice dispersion structure and continuum limit (incl. cubic split) | 5  |
| 2    | SO(3,1) on-shell measure (3 axes + composition + reverse)          | 6    |
| 3    | Continuum 2-point function (analytic K_1 form, cluster, asymptotic) | 7   |
| 4    | Lattice -> continuum convergence (Euclidean + spacelike Lorentzian) | 4   |
| 5    | SO(3,1) boost covariance: 5 rapidities along [100] + [110] + [111] + arbitrary + composition | 13 |
| 6    | Cubic-harmonic LV at finite `a` (inherited dim-6 K_4)              | 5    |
| 7    | Combined SO(3,1) theorem statement                                 | 10   |
| 8    | Connection to existing dispersion theorem (strict extension)       | 5    |

Total: 55/55 PASS.

## Commands run

```bash
git checkout -b lorentz-boost-covariance 59f7e4f0  # main head
python3 scripts/frontier_lorentz_boost_3plus1d.py
# Exit code: 0  PASS=55  FAIL=0
```
