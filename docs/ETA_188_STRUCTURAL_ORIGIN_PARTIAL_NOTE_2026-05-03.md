# Structural Origin of eta/eta_obs = 0.1888 — Partial Closing Note

Date: 2026-05-03
Type: partial closing of cycle 09 Obstruction 3 + falsification of four near-fit candidates
Claim type: bounded_theorem (structural decomposition with one isolated phenomenological factor)
Status: bounded-support (partial closing)
Cycle: 18 of retained-promotion 2026-05-02 → 2026-05-03 campaign
Branch: physics-loop/eta-188-structural-origin-2026-05-03

This document is a branch-local physics-loop artifact. Its `Status:` line is
not an audit-ratified retained status. Independent audit-lane review is still
required before the repo may treat any claim here as retained-grade.

## Executive summary

Cycle 09 catalogued FOUR candidate structural origins for the framework's
exact one-flavor leptogenesis result `eta/eta_obs = 0.18878592785...`:

  - `17/90`              consistent within 0.055%
  - `31/32 * sqrt(6)/(4*pi)` consistent within 0.025%
  - `(7/8)^(1/4) * sqrt(6)/(4*pi)` consistent within 0.138%
  - `sqrt(6)/(4*pi)`     consistent within 3.25%

The cycle-09 verdict was: `structural origin of 0.1888 ambiguous; multiple
near-fits consistent within sub-percent, none derived`.

This cycle (18) traces through the actual transport calculation in
`scripts/dm_leptogenesis_exact_common.py` (the `exact_package()`,
`kappa_axiom_reference()`, and surrounding chain) and identifies the EXACT
structural form:

```
eta/eta_obs = (516 / 53009) * Y0^2 * F_CP * kappa_axiom / eta_obs
```

Of these factors:

  - `516/53009` is a **pure rational** that closes from `g_*=427/4`,
    `g_S=43/11`, and `C_sph=28/79`, with `pi^4` and `zeta3` cancelling
    between `(s/n_gamma)` and `d_N`.
  - `Y0^2 = (g_weak^2/64)^2` is the unique **phenomenological import**
    (`g_weak = 0.653`, the bare weak coupling at the v_EW scale). This is
    the same residual already named in cycle 09 Obstruction 1 / cycle 12
    R2 / cycle 15 R1.
  - `F_CP = |cp1*f(x_23) + cp2*f(x_3)| / (16*pi)` is **structural on the
    PMNS chart**, with `cp1 = -sqrt(8/27)`, `cp2 = +sqrt(8)/9`, and
    `cp1/cp2 = -sqrt(3)` (from cycle 12 Obstruction 1 sharpening).
  - `kappa_axiom` is the transport-ODE solution functional of `K_decay`,
    structural except via its `Y0^2` dependency through `K_decay`.

The four cycle-09 near-fits are **falsified** as structural identifications:
none of them contains the actual structural factors (`516/53009`, `Y0^2`,
`F_CP`, `kappa_axiom`). Their sub-percent agreement with the actual value
is **numerical coincidence**, not structural derivation.

## The framework's transport calculation

The exact one-flavor radiation-branch transport in
`scripts/frontier_dm_leptogenesis_transport_status.py::part3_*` computes
the eta-ratio as:

```python
eta_ratio_direct = (
    S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT
    * pkg.epsilon_1 * kappa_direct / ETA_OBS
)
```

Reading the constants from `dm_leptogenesis_exact_common`:

| factor                  | symbolic form                              | value                       |
|-------------------------|--------------------------------------------|-----------------------------|
| `S_OVER_NGAMMA_EXACT`   | `(pi^4 / (45 * zeta3)) * g_S`              | `7.039433661546651`         |
| `C_SPH`                 | `28 / 79`                                  | `0.354430...`               |
| `D_THERMAL_EXACT`       | `135 * zeta3 / (4 * pi^4 * g_*)`           | `0.003901498367656259`      |
| `pkg.epsilon_1`         | `Y0^2 * \|cp1*f(x_23)+cp2*f(x_3)\|/(16*pi)`  | `2.4576198795840222e-06`    |
| `kappa_axiom`           | transport ODE solution(K_decay)            | `0.004829545290766509`      |
| `ETA_OBS`               | `6.12e-10`                                 | comparator only             |

Product: `0.18878592950193965` (eta/eta_obs).

## ABC pure-rational closure

The product `(s/n_gamma) * C_sph * d_N` simplifies dramatically because:

```
s/n_gamma = (pi^4 / (45 * zeta3)) * g_S
d_N      = 135 * zeta3 / (4 * pi^4 * g_*)
```

The `pi^4` and `zeta3` factors cancel exactly:

```
(s/n_gamma) * d_N = (1/45) * (135/4) * (g_S / g_*)
                  = (3/4) * (g_S / g_*)
```

Multiplying by `C_sph = 28/79`:

```
ABC = (3/4) * (28/79) * (g_S / g_*) = (21/79) * (g_S / g_*)
```

The framework primitives:

  - `g_*  = 28 + (7/8)*90 = 427/4`  (SM dofs at leptogenesis scale)
  - `g_S = 2 + (7/8)*6*(4/11) = 43/11`  (CMB dofs today)

Substituting:

```
ABC = (21/79) * (43/11) * (4/427)
    = (21 * 43 * 4) / (79 * 11 * 427)
    = 3612 / 371063
```

Note that `427 = 7 * 61`, so the common factor of 7 cancels:

```
ABC = 3612/7 / (371063/7) = 516 / 53009
```

This is the **pure-rational closing identification** of the leading
constant in the eta/eta_obs structure. The denominator `53009 = 79 * 11 *
61` carries the sphaleron, the entropy-conversion, and the SM-dof signature.
The numerator `516 = 4 * 3 * 43` carries the `g_S` numerator and the
`(135/45)*(1/4) = 3/4` from `d_N`-vs-`s/n_gamma` thermodynamics.

## Falsification of the four cycle-09 candidates

The four candidate near-fits agree numerically with `0.18878592...` to:

| candidate                  | value          | rel diff     |
|----------------------------|----------------|--------------|
| `17/90`                    | `0.18888889...`| `0.055%`     |
| `31/32 * sqrt(6)/(4*pi)`   | `0.18883254...`| `0.025%`     |
| `(7/8)^(1/4) * sqrt(6)/(4*pi)` | `0.18852394...`| `0.138%`  |
| `sqrt(6)/(4*pi)`           | `0.19492355...`| `3.252%`     |

**None of these is the actual structural form.** The framework computes
`0.1888...` to 12+ decimal digits via the explicit five-factor product;
each candidate's agreement with the exact framework value is at most ~3-4
decimal digits. The factor-of-1000 mismatch in precision rules out
structural identification.

Moreover, the four candidates contain factors that do NOT appear in the
framework's actual decomposition:

  - `17/90` introduces a 17 that does not arise from any framework
    primitive (g_* = 427/4, g_S = 43/11, C_sph = 28/79, alpha_LM, gamma=1/2,
    K00=2, etc.). It is a coincidental rational approximation.
  - `sqrt(6)/(4*pi)` is a generic geometric factor (volume of S^3 / surface
    area...) that is universal across many dimensional-analysis estimates;
    it does not isolate the framework's specific transport content.
  - The corrections `31/32` or `(7/8)^(1/4)` are introduced ad-hoc to
    improve fit — there is no derivation of these specific corrections
    from any framework theorem.

The actual structural form, by contrast, contains:

  - `516/53009`: traces directly to retained primitives `g_*`, `g_S`,
    `C_sph` with explicit `pi^4`/`zeta3` cancellation.
  - `Y0^2`: traces directly to the named phenomenological coupling
    `g_weak`.
  - `F_CP`: traces to PMNS chart constants `gamma`, `E1`, `E2`, `K00` and
    the loop-function values at `x_23`, `x_3`.
  - `kappa_axiom`: traces to the transport ODE under explicit decay/
    washout profiles.

## Phenomenological-import isolation

The unique non-structural factor in the entire chain is:

```
Y0 = g_weak^2 / 64 = (0.653)^2 / 64 = 0.0066626...
Y0^2 = 4.4391e-05
```

`g_weak = 0.653` is the bare weak coupling at the v_EW scale. It is a
phenomenological MS-bar-style quantity; the framework retains
`g_weak^2|lattice = 1/(d+1) = 1/4` from THREE independent authorities
(YT_EW Color Projection, SU2_WEAK_BETA C5, EW_LATTICE_COS_SQ C4) — see
cycle 15. But the running from the lattice scale to the v-scale (cycle 15
residual R1) is the named obstruction that prevents structural closure.

If `g_weak^2` instead took its lattice-scale retained value `1/4`, then
`Y0|lattice = 1/256 = 0.00390625` and `Y0^2|lattice = 1/65536`. The
eta/eta_obs would be:

```
(516/53009) * (1/65536) * F_CP * kappa_axiom / eta_obs
```

which is structural (no phenomenological import) but would compute a
different numerical value of eta/eta_obs. The phenomenological 0.653
versus the lattice-scale 1/2 is precisely the running residual.

## What the cycle 18 result settles

Cycle 09 Obstruction 3:
> "structural origin of 0.1888 ambiguous; multiple near-fits consistent
> within sub-percent, none derived"

Cycle 18 settles:

  - **Structural form is explicit**: `(516/53009) * Y0^2 * F_CP * kappa_axiom / eta_obs`.
  - **Pure-rational ABC closure**: `516/53009` derived from `g_*`, `g_S`,
    `C_sph` with `pi^4 * zeta3` cancellation.
  - **Cycle-09 candidate near-fits are falsified** as structural origins;
    they are numerical coincidences.
  - **Phenomenological factor isolated**: `Y0^2 = (g_weak^2/64)^2`.

What remains open (named obstructions):

  - **O3a** (Y0^2 phenomenological): same residual as cycle 09 O1 /
    cycle 12 R2 / cycle 15 R1. Resolution requires `g_weak`-running
    from lattice to v-scale.
  - **O3b** (PMNS chart constants): `gamma=1/2` partially closed by
    cycle 16 (c_odd structural identification). `E1=sqrt(8/3)` and
    `E2=sqrt(8)/3` require v_even theorem retention (cycle 16 sub-B/sub-C,
    cycle 17 in progress).
  - **O3c** (kappa_axiom ODE): structural functional once Y0 is
    structural; no additional obstruction.

These are not new obstructions; they are the same residuals already named
in cycles 09, 12, 15, 16, 17. Cycle 18's contribution is reducing
"structural origin ambiguous" to "one named phenomenological factor plus
structural skeleton with explicit pure-rational sub-closure".

## Forbidden-import discipline

  - `eta_obs = 6.12e-10` used **only as comparator**, never as a
    derivation input. The 0.1888 value is computed from the framework's
    transport chain; the comparator is used only to express the final
    value as a dimensionless ratio.
  - `g_weak = 0.653` is **flagged as a named phenomenological import**,
    not consumed as a derivation input; it carries through the chain as
    the `Y0^2` factor whose phenomenological status is the residual
    obstruction.
  - No literature numerical comparators consumed.
  - No fitted selectors consumed.
  - No same-surface family arguments.
  - All other inputs (`g_* = 427/4`, `g_S = 43/11`, `C_sph = 28/79`,
    `M_PL`, `alpha_LM` via `PLAQ_MC`, PMNS chart constants `gamma=1/2`,
    `E1=sqrt(8/3)`, `E2=sqrt(8)/3`, `K00=2`, APBC factor `(7/8)^(1/4)`)
    are retained framework primitives.

## Reviewer notes

  - The `pi^4 * zeta3` cancellation between `s/n_gamma` and `d_N` is a
    mechanical consequence of the standard thermodynamic forms and not a
    framework-specific identity; reviewer should verify the algebra.
  - The pure-rational closure `516/53009 = 21*172/(79*4697)` uses
    `g_* = 427/4` exactly. If a different `g_*` were used (e.g.,
    accounting for additional BSM dofs at leptogenesis scale), the ABC
    rational would change. The framework's `g_* = 28 + (7/8)*90 = 427/4`
    is the SM-only count, retained.
  - The reduction `cp1/cp2 = -sqrt(3)` was already noted in cycle 12;
    cycle 18 carries this through into the F_CP loop sum.
  - Reviewer should cross-check against the parent runner
    `scripts/frontier_dm_leptogenesis_transport_status.py`; the cycle 18
    runner reproduces the same `0.18878592...` value via the
    structurally-decomposed form.

## Verification

```bash
python3 scripts/frontier_eta_188_structural_origin.py
# Expected: PASS=38 FAIL=0
```

The runner verifies:
  - Framework chain reproduces 0.1888 (parts 1).
  - ABC pure-rational closure 516/53009 (part 2).
  - Falsification of all four cycle-09 near-fits (part 3).
  - CP-package structural skeleton with cp1/cp2 = -sqrt(3) (part 4).
  - Phenomenological import isolation (part 5).
  - Full decomposition reproduces 0.1888 in structural form (part 6).
  - Counterfactual stability checks (part 7).
  - Obstruction residual summary (part 8).

## Honest claim type

This note is a **partial closing** of cycle 09 Obstruction 3 with a
**falsification component** for the four candidate near-fits.

  - Closing component: structural origin is now explicit; ABC sub-factor
    closes to pure rational `516/53009`.
  - Falsification component: cycle-09 candidate near-fits 17/90,
    31/32·√6/(4π), (7/8)^(1/4)·√6/(4π), and √6/(4π) are NOT the
    structural origin.
  - Remaining residual: `Y0^2` phenomenological import (cycle 09 O1 /
    cycle 12 R2 / cycle 15 R1 — same obstruction, not new).

Source-note status: bounded_theorem with one named phenomenological
admission. Independent audit ratification still required before any
retained-grade promotion.
