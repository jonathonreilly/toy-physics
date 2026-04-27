# Hubble Tension Structural Lock Theorem: Late-Time `H_0` Is a Single Scalar on the Retained Surface

**Date:** 2026-04-26
**Status:** proposed_retained/admitted-surface structural-support theorem on
`main`. The theorem locks the structural form of late-time observables on the
retained `w_Lambda = -1` plus admitted flat-FRW surface; it does **not**
predict a numerical value for `H_0` or close the Lane 5 matter bridge.
**Primary runner:** `scripts/frontier_hubble_tension_structural_lock.py`
**Lane:** 5 — Hubble constant `H_0` derivation
**Workstream:** `hubble-h0-20260426`

---

## 0. Statement

**Theorem (Hubble Tension Structural Lock).** Adopt:

- (P1) the retained dark-energy equation of state `w_Lambda = -1`
  (`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`);
- (P2) flat FRW cosmology with three non-interacting components
  (matter `w_m = 0`, radiation `w_r = 1/3`, dark energy `w_Lambda = -1`)
  satisfying `Omega_m,0 + Omega_r,0 + Omega_Lambda,0 = 1`.

The wider framework grounding (`Cl(3)` on `Z^3`, spectral-gap identity
`Lambda = 3/R_Lambda^2`, matter-bridge identity `Omega_Lambda =
(H_inf/H_0)^2`) supplies the *context* in which `w_Lambda = -1` is a
retained corollary rather than a separate axiom. The operational proof of
(★) uses only (P1) and (P2).

Then for every late-time scale factor `a in (a_recomb, 1]` (equivalently
redshift `z in [0, z_recomb)`), the Hubble parameter satisfies the exact
function identity

```text
H(a)^2 / H_0^2  =  Omega_r,0 a^-4 + Omega_m,0 a^-3 + Omega_Lambda,0     (★)
```

with `H_0 := H(a = 1)` and `(Omega_r,0, Omega_m,0, Omega_Lambda,0, H_0)`
constants in cosmic time.

**Lock corollary (no late-time `H_0(z)` running).** Define the "implied
`H_0` at scale factor `a`" by

```text
H_0_implied(a) := H(a) / sqrt( Omega_r,0 a^-4 + Omega_m,0 a^-3 + Omega_Lambda,0 ).
```

Then on the retained surface

```text
H_0_implied(a) = H_0     for every a in (a_recomb, 1].
```

In particular, every late-time distance-ladder, BAO, time-delay-lensing, or
any other `H(z)`-recovering measurement must read the same scalar `H_0`,
provided the measurement is reduced against the same retained
`(Omega_r,0, Omega_m,0, Omega_Lambda,0)` triple.

**Falsifier.** If independent late-time measurements reconstruct
distinguishable values of `H_0_implied(a)` after correctly accounting for
`(Omega_r,0, Omega_m,0, Omega_Lambda,0)`, then one of (P1)-(P2) is falsified
or at least one measurement carries an unmodeled systematic.

**Tension stance.** Any genuine Hubble tension between late-time
distance-ladder `H_0 ≈ 73 km/s/Mpc` and CMB-inferred `H_0 ≈ 67.4 km/s/Mpc`
**cannot be resolved by late-time modification of dark energy or gravity on
the retained surface**. Resolution must come from:

- **pre-recombination physics** (early dark energy, modified recombination,
  shifted `N_eff` before CMB release), which lies outside the scope of
  (P1)-(P3); or
- **systematic re-evaluation** of one of the measurement chains.

## 1. Retained inputs (all on `main`)

| Ingredient | Reference |
|---|---|
| `Cl(3)` on `Z^3` (one-axiom physical theory) | [MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md) |
| `Lambda = 3 / R_Lambda^2` spectral-gap identity | [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) |
| `w_Lambda = -1` dark-energy EOS | [DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md) |
| `H_inf = c / R_Lambda` scale identification | [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) |
| `Omega_Lambda = (H_inf/H_0)^2` matter-bridge identity | [OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md) |
| FRW kinematic forward reduction | [COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md) |
| Single-ratio inverse reconstruction | [COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md](COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md) |

The matter-bridge and inverse-reconstruction theorems do not enter the
proof of (★) but supply the wider context that motivates this theorem:
since the late-time bounded surface reduces to one open ratio, the
question "is late-time `H_0` measured consistently?" has a sharp,
single-scalar answer.

## 2. Proof of (★)

### 2.1 Continuity equations under (P1)-(P2)

For each non-interacting component `i in {m, r, Lambda}` with constant EOS
`w_i`, the local energy-conservation law

```text
d rho_i / dt + 3 H (1 + w_i) rho_i = 0
```

integrates to

```text
rho_i(a) = rho_i,0 * a^(-3(1 + w_i)).                                (1)
```

Substituting the three values:

- matter: `rho_m(a) = rho_m,0 a^-3`,
- radiation: `rho_r(a) = rho_r,0 a^-4`,
- dark energy: `rho_Lambda(a) = rho_Lambda,0 a^0 = rho_Lambda,0` (using
  `w_Lambda = -1`, P1).

### 2.2 Flat Friedmann equation

For flat FRW with three non-interacting components,

```text
H(a)^2 = (8 pi G / 3) [rho_m(a) + rho_r(a) + rho_Lambda(a)].         (2)
```

Define the present-day critical density `rho_crit,0 = 3 H_0^2 / (8 pi G)`
and density fractions `Omega_i,0 = rho_i,0 / rho_crit,0`. Then (2) and the
component scalings (1) give

```text
H(a)^2 = H_0^2 * [Omega_r,0 a^-4 + Omega_m,0 a^-3 + Omega_Lambda,0].
```

Dividing both sides by `H_0^2` and recognizing that `Omega_r,0 + Omega_m,0
+ Omega_Lambda,0 = 1` by flatness yields exactly

```text
H(a)^2 / H_0^2 = Omega_r,0 a^-4 + Omega_m,0 a^-3 + Omega_Lambda,0.   (★)
```

`QED`

## 3. The lock corollary

Define

```text
F(a; Omega_r,0, Omega_m,0, Omega_Lambda,0)
   := Omega_r,0 a^-4 + Omega_m,0 a^-3 + Omega_Lambda,0.              (3)
```

By (★), `H(a)^2 = H_0^2 * F(a; ...)`, so

```text
H_0_implied(a) := H(a) / sqrt( F(a; Omega_r,0, Omega_m,0, Omega_Lambda,0) )
                = H_0                                                 (4)
```

for every `a in (a_recomb, 1]`. Hence the implied `H_0` is one and the same
scalar at every late-time epoch, given the retained triple `(Omega_r,0,
Omega_m,0, Omega_Lambda,0)`.

**Operational restatement.** Any late-time observation that reduces to an
`H(z)` measurement via the FRW kinematic identities (forward reduction
theorem 2026-04-24) and is then converted to `H_0` via (4) must yield the
same scalar.

## 4. Falsifier and Hubble tension stance

### 4.1 Sharp falsifier

The retained surface is falsified — at the structural level — if any pair
of independent late-time `H(z)` measurements, after each is reduced against
the same `(Omega_r,0, Omega_m,0, Omega_Lambda,0)`, yields distinguishable
`H_0_implied`.

Equivalently, if `w_Lambda(a)` exhibits a non-trivial late-time
`a`-dependence, then `rho_Lambda(a)` is no longer constant and (1) for the
DE component fails. The lock corollary fails by inserting an extra free
function `w(a)`.

So the falsifier is operational: **late-time z-dependent `H_0` running ⇔
`w_Lambda != -1` at late times ⇔ retained surface (P1) falsified**.

### 4.2 What the theorem does say about the Hubble tension

Empirically, distance-ladder local measurements give `H_0 ≈ 73.04 ± 1.04
km/s/Mpc` (Riess et al. 2022 SH0ES) while CMB-inferred values give
`H_0 ≈ 67.4 ± 0.5 km/s/Mpc` (Planck 2018). On the retained surface,

- both sets of measurements probe `H(z)` directly, but at different
  effective epochs;
- the distance-ladder chain reduces local low-`z` `H(z)` to `H_0` via (4);
- the CMB chain reduces `theta_*` (acoustic angular scale at recombination)
  through the *full* `z`-history including the pre-recombination expansion,
  which lies outside (P1)-(P3).

The structural lock theorem rules out late-time-only resolutions: anything
that proposes a late-time `w(z)`, modified late-time gravity at cosmological
scales, or late-time DE-matter coupling falsifies (P1) or (P2).

It does **not** rule out:

- pre-recombination modifications (early dark energy raising `H(z_recomb)`
  and shrinking the sound horizon `r_s`);
- modified recombination physics changing the Planck `theta_*` reduction;
- shifted `N_eff` *before* photon decoupling (consistent with retained
  `N_eff = 3.046` *after* the standard thermal correction; the theorem
  applies post-recombination only);
- systematic errors in either the local distance ladder or the CMB pipeline.

### 4.3 Public commitment

This theorem makes the framework's stance explicit: a Hubble tension in the
literature is, on the retained surface, a constraint on **early-time
physics or systematics**, not on late-time dynamics.

## 5. What the theorem closes and does not close

**Closes.**

- The exact functional identity (★) for late-time `H(a)` on the retained
  surface, derived from (P1)-(P3) without additional axioms.
- The lock corollary: `H_0_implied(a)` is a single scalar across the entire
  late-time epoch on the retained surface.
- A sharp falsifier for the retained surface in late-time observational
  data.
- A public manuscript-facing structural commitment: late-time-only
  resolutions of any genuine Hubble tension are forbidden.

**Does not close.**

- A retained derivation of the numerical value `H_0`. (Lane 5 main target.)
- A retained derivation of `R_Lambda` or equivalently `Omega_Lambda`. (The
  matter-bridge identity reduces the open numbers; the absolute scale anchor
  remains the Planck-lane gate.)
- The pre-recombination story (`z >= z_recomb`). The theorem applies only
  in the late-time epoch.
- The bounded `Omega_b` and `Omega_DM` cascade. Those depend on retiring
  `eta` and `alpha_GUT` (separate routes).

## 6. How this advances Lane 5

Before this theorem, the Lane 5 open-science tracker listed Phase 1 =
"5C: Hubble tension explicit stance" as Tier A and ~1 week of work. After
this theorem, that target is landed as a sharp
falsifier-bearing structural commitment on the retained/admitted surface.

The remaining Lane 5 closure targets are:

- 5A: `Omega_m` internal closure (matter bridge) — reduces to retiring
  `eta` and `alpha_GUT` from the bounded cascade.
- 5B: numerical `H_0` derivation — depends on 5A plus an absolute-scale
  anchor (`R_Lambda` from the Planck lane, or independent absolute-scale
  retainment).
- 5D: `Sigma m_nu` integration — depends on Lane 4 partial closure.

The structural lock theorem does not progress 5A, 5B, or 5D directly. It
adds Phase-1 (5C) as a proposed-retained/admitted-surface structural support
result.

## 7. Runner

**Path:** `scripts/frontier_hubble_tension_structural_lock.py`
**Paired log:** `logs/2026-04-26-hubble-tension-structural-lock.txt`

The runner verifies:

1. **Symbolic continuity (sympy):** for `w in {0, 1/3, -1}`, the continuity
   equation (1) gives `rho_i(a) = rho_i,0 a^{-3(1+w)}`. In particular `w =
   -1` gives `rho_Lambda(a) = rho_Lambda,0` exactly.
2. **Symbolic Friedmann (sympy):** combining (1) and (2) under flatness
   yields (★) exactly.
3. **Lock corollary (sympy):** the function `H_0_implied(a)` defined in (4)
   simplifies to the constant `H_0` for all `a > 0`.
4. **Numerical ΛCDM check (numpy):** plug Planck 2018 comparator
   `(Omega_r,0, Omega_m,0, Omega_Lambda,0, H_0) = (9.2e-5, 0.315, 0.685,
   67.4 km/s/Mpc)` and recover the standard `H(z)/H_0` curve over
   `z in [0, 1]`.
5. **Modified-DE stress test (numpy):** parametrize a late-time DE EOS
   `w(a) = -1 + delta` with `delta != 0`; integrate the energy conservation
   to get `rho_DE(a)`; show that `H_0_implied(a)` becomes `a`-dependent
   (i.e., the lock fails) precisely when `delta != 0`. This is the
   operational falsifier.

Expected: all five PASS. A FAIL on (1)-(3) flags a sympy-side regression;
a FAIL on (4)-(5) flags a runner-arithmetic bug.

## 8. Cross-references

- `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` — `Omega_Lambda =
  (H_inf/H_0)^2` reduction.
- `COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md`
  — inverse reconstruction certificates against the same single open ratio.
- `COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md` — forward
  FRW reduction.
- `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md` — retained `w = -1`.
- `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` — retained
  `Lambda = 3/R_Lambda^2`.
- `docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`
  — Lane 5 status; this note advances Phase 1 (5C).
- `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` §5 — proposed
  weave: cite the structural lock alongside the matter-bridge identity.
- `docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md` — proposed
  weave: revise Hubble tension framing to reflect the late-time lock.

## 9. Boundary

This theorem is structural, not numerical. It does not promote any cosmology
row to retained quantitative closure. It does not retire `H_0`, `T_CMB`,
`eta`, or `alpha_GUT` from the inputs ledger. It commits the framework's
manuscript-surface stance on the Hubble tension to a sharp, falsifiable
structural form.

External references are limited to standard FRW cosmology
(textbook; admitted convention) and observational comparators (Planck 2018,
SH0ES 2022; never derivation inputs). All derivation premises are
framework-internal retained items already on `main`.
