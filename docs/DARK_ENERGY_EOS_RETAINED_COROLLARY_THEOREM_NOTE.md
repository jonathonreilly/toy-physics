# Dark-Energy EOS Retained Structural Corollary

**Date:** 2026-04-18
**Status:** proposed **retained structural corollary** + **bounded quantitative
continuation**. This note is the promotion-target write-up; the publication
matrix and claims table are left unchanged pending reviewer acceptance.
**Script:** `scripts/frontier_dark_energy_eos_retained_corollary.py`
**Upstream authorities:**
[`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md),
[`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md),
[`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md),
[`DARK_ENERGY_EOS_NOTE.md`](DARK_ENERGY_EOS_NOTE.md)

## Role

This note asks one narrow question:

> on the retained `S^3` + spectral-gap surface, is the dark-energy equation of
> state `w = -1` exactly, independent of the cosmology-scale identification
> that keeps the numerical value of `Lambda` bounded?

It does **not** reopen the cosmology-scale identification blocker. It does
**not** promote the numerical `Lambda` value. It does **not** touch the
matter-content bridge behind present-day `Omega_Lambda`. Its scope is exactly
the EOS value `w`, nothing else.

The scientific content is already present in
[`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
under "`w = -1` is the same mechanism". The contribution of this note is to
separate that statement into its own dual-status row, using the architecture
already established by
[`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md)
and
[`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md).

## Theorem

Let the retained surface carry:

1. retained `S^3` spatial topology on the accepted `PL S^3 x R` carrier
   (authority:
   [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md),
   [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md));
2. the scalar-Laplacian first eigenvalue
   `lambda_1(S^3_R) = 3 / R^2`
   as a geometric invariant of the topology and overall scale (standard
   result; the coefficient `3` is the exact `d = 3` value for `S^3`);
3. the same-surface spectral-gap vacuum identification
   `Lambda = lambda_1(S^3_R) = 3 / R^2`
   used by the canonical cosmology-companion lane (authority:
   [`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md));
4. a fixed radius `R` (i.e. the topology is not dynamically rescaled by
   cosmic evolution; only topology change or a non-isometric deformation can
   shift `lambda_1`).

**Theorem.** Under conditions (1)–(4), the dark-energy density is exactly
time-independent,

  `rho_Lambda(t) = (c^4 / (8 pi G)) * Lambda = (3 c^4) / (8 pi G R^2) = const`,

and therefore the dark-energy equation of state is

  `w = -1   exactly`,

with CPL parameters `w_0 = -1`, `w_a = 0`. The retained lattice-discretization
correction is a constant shift `|delta Lambda / Lambda| = (1/4)(a/R)^2`
(authority:
[`DARK_ENERGY_EOS_NOTE.md`](DARK_ENERGY_EOS_NOTE.md), Part 2), hence carries
no additional time dependence and does **not** shift `w`.

**Proof.** Conditions (1)–(3) give `Lambda = 3/R^2`. Condition (4) gives
`d R / d t = 0`, so `d Lambda / d t = 0` and `d rho_Lambda / d t = 0`. The
continuity equation for any cosmological fluid is

  `d rho / d t + 3 H (1 + w) rho = 0`,

which for `rho = rho_Lambda > 0` and `d rho_Lambda / d t = 0` forces
`(1 + w) = 0`, i.e. `w = -1`. Equivalently, `w = -1 - (1/3) d ln rho / d ln a`
and `d ln rho_Lambda / d ln a = 0`. The retained lattice correction enters as
`Lambda_eff = (3/R^2)(1 - (1/4)(a/R)^2)`, which is `a(t)`-independent when the
fundamental lattice spacing `a = l_P` and topology scale `R` are both fixed,
so `d rho_Lambda / d t = 0` is preserved. □

## What Is Retained Exactly

- The spectral-gap coefficient `3` on `S^3`: exact, pure mathematics on the
  retained topology.
- The `1 / R^2` scaling: exact geometric invariant.
- The continuity-equation map
  `d rho / d t = 0  ==>  w = -1`: standard FRW result on the retained smooth
  target (authority:
  [`UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`](UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md)).
- The retained lattice-correction bookkeeping: constant shift, not a
  time-dependent drift (authority:
  [`DARK_ENERGY_EOS_NOTE.md`](DARK_ENERGY_EOS_NOTE.md)).
- Independence of the corollary from the cosmology-scale identification:
  `w = -1` follows from `R` being fixed, not from `R` having any particular
  value. The cosmology-scale identification fixes only the numerical value of
  `Lambda`, not whether `w = -1`.

## What Remains Bounded

The promotion target of this note is strictly the EOS value `w`. The
following are **not** upgraded by this note:

- the numerical value of `Lambda`: remains the bounded/conditional companion
  recorded in
  [`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md);
- present-day `Omega_Lambda`: remains gated on the matter-content bridge per
  [`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md);
- spectral tilt `n_s`, graviton mass, and the remaining cosmology companion
  rows: unchanged, still bounded/conditional;
- first-principles derivation of the cosmological-scale matching: unchanged,
  still the honest remaining gap.

## Dual-Status Architecture

This note follows the template already used on `main`:

- retained structural corollary:
  `w = -1` exactly on the retained `S^3` + spectral-gap + fixed-`R` surface
  (this note);
- bounded quantitative continuation:
  numerical `Lambda = 3 / R_Lambda^2` still conditional on the
  cosmology-scale identification
  (authorities:
  [`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md),
  [`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)).

Analogous rows already on `main`:

- retained `T = 0` confinement + bounded `sqrt(sigma) ~ 465 MeV`
  ([`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md));
- retained `d_n(QCD) = 0` + bounded `d_n(CKM) ~ 10^-33 e cm`
  ([`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md)).

## Safe Claim Boundary

What this lane supports:

- on the retained `S^3` + spectral-gap + fixed-`R` surface, the dark-energy
  density is exactly time-independent and `w = -1` is exact;
- CPL parameters `w_0 = -1`, `w_a = 0` to all orders on that surface;
- retained lattice-discretization corrections are constant and do not shift
  `w`.

What this lane does **not** support:

- promotion of the numerical `Lambda` value;
- closure of the cosmology-scale identification;
- closure of the matter-content bridge behind `Omega_Lambda`;
- a first-principles derivation that the retained spectral gap **is** the
  vacuum-energy mechanism, rather than being identified with it on the
  companion surface.

The scope of the corollary is therefore the EOS value `w`, conditional on the
retained identification `Lambda = lambda_1(S^3)` that is already used by the
cosmology companion stack.

## Observational Falsifiability

This is a clean binary prediction. DESI, Euclid, and SPHEREx are actively
constraining the CPL `(w_0, w_a)` plane:

- DESI DR1 (2024): `w_0 = -0.55 +/- 0.21`, `w_a = -1.30 +0.70/-0.60`
  (2-3 sigma hint of dynamical DE, systematics not excluded);
- DESI DR2 (2025): tension reduced, trending toward `(w_0, w_a) = (-1, 0)`;
- DESI final (2026-2027): expected `~1%` precision on `w_0`.

Any `> 5 sigma` detection of `w != -1` or `w_a != 0` falsifies the
spectral-gap vacuum identification used by the retained corollary. Any
detection of `w < -1` at any epoch is independently a phantom-crossing
falsification.

Retained framework corrections to `w = -1`:

- lattice-discretization drift bound: `|delta w| < (1/4)(l_P / R_H)^2
  ~ 2 x 10^-123` under any conceivable evolution of `a/R`;
- higher-`k` mixing: excluded on the fixed-topology + fixed-`R` surface;
- topological phase transitions: would produce a discontinuity, not a smooth
  CPL drift.

So the framework prediction is `w = -1` to at least `10^-120`, well below any
observational sensitivity.

## Proposed Publication Matrix Row Upgrade

This note does not modify
[`PUBLICATION_MATRIX.md`](publication/ci3_z3/PUBLICATION_MATRIX.md) or
[`CLAIMS_TABLE.md`](publication/ci3_z3/CLAIMS_TABLE.md). Those changes are
reviewer-gated and belong to the publication control plane. For reviewer
reference, the proposed edit to the `Dark energy EOS w` row of the
quantitative component stack is:

| Quantity / lane | Framework result | Status | Current publication decision |
|---|---|---|---|
| Dark energy EOS `w` | `w = -1` exact on retained `S^3` + spectral-gap + fixed-`R` surface; numerical `Lambda` still bounded | retained structural corollary + bounded quantitative continuation | retained corollary may appear on the flagship / SI surface; numerical `Lambda` stays the existing bounded/conditional companion |

This mirrors the existing "CKM-only neutron EDM on the retained `theta_eff = 0`
surface" row.

## Commands Run

```bash
python3 scripts/frontier_dark_energy_eos_retained_corollary.py
```
