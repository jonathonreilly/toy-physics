# Dark-Energy EOS Retained Structural Corollary

**Date:** 2026-04-18
**Status:** proposed **retained structural corollary** on the companion-lane
spectral-gap vacuum identification. This note is the promotion-target
write-up; the publication matrix and claims table are left unchanged pending
reviewer acceptance.
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
separate that statement into a standalone retained-corollary row for the
EOS `w`, following the structural-corollary-with-named-conditioning
precedent of
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
   cosmic evolution; rescaling `R` or a non-isometric deformation of the
   round metric would shift `lambda_1`, neither is retained on `main`).

In what follows we write `a_sc(t)` for the FRW scale factor and `l_P` for the
fundamental lattice spacing, to keep those separate from the S^3 radius `R`.

**Theorem.** Under conditions (1)–(4), the dark-energy density is exactly
time-independent,

  `rho_Lambda(t) = (c^4 / (8 pi G)) * Lambda = (3 c^4) / (8 pi G R^2) = const`,

and therefore the dark-energy equation of state is

  `w = -1   exactly`,

with CPL parameters `w_0 = -1`, `w_a = 0`. The retained lattice-discretization
correction is a constant shift `|delta Lambda / Lambda| = (1/4)(l_P / R)^2`
(authority:
[`DARK_ENERGY_EOS_NOTE.md`](DARK_ENERGY_EOS_NOTE.md), Part 2), hence carries
no additional time dependence and does **not** shift `w`.

**Proof.** Conditions (1)–(3) give `Lambda = 3 / R^2`. Condition (4) gives
`d R / d t = 0`, so `d Lambda / d t = 0` and `d rho_Lambda / d t = 0`. The
continuity equation for any cosmological fluid on the retained smooth FRW
target is

  `d rho / d t + 3 H (1 + w) rho = 0`,

which for `rho = rho_Lambda > 0` and `d rho_Lambda / d t = 0` forces
`(1 + w) = 0`, i.e. `w = -1`. Equivalently,
`w = -1 - (1/3) d ln rho / d ln a_sc` and
`d ln rho_Lambda / d ln a_sc = 0`. The retained lattice correction enters as
`Lambda_eff = (3 / R^2) * (1 - (1/4)(l_P / R)^2)`, which is
`a_sc(t)`-independent when `l_P` and `R` are both fixed constants, so
`d rho_Lambda / d t = 0` is preserved. □

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

## Relationship to Other Cosmology Rows

The EOS value `w` and the numerical `Lambda` value already sit in **distinct
rows** of
[`PUBLICATION_MATRIX.md`](publication/ci3_z3/PUBLICATION_MATRIX.md). This note
asks only for the `Dark energy EOS w` row to move. The `Cosmological constant
Lambda` row is unchanged and stays `bounded/conditional` as recorded in
[`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md).
The matter-content bridge behind present-day `Omega_Lambda`
([`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md))
is also unchanged. So the package-level picture after promotion would read:

- **retained structural corollary (new):**
  `w = -1` exactly on the retained `S^3` + spectral-gap + fixed-`R` surface;
- **bounded/conditional (unchanged):**
  numerical `Lambda`, present-day `Omega_Lambda`, spectral tilt `n_s`,
  graviton mass, and the cosmology-scale identification itself.

Precedent structural-corollary promotions already on `main`:

- retained `T = 0` confinement of graph-first SU(3), with `sqrt(sigma)` kept
  bounded
  ([`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md));
- retained `d_n(QCD) = 0` on the `theta_eff = 0` surface, with `d_n(CKM)`
  kept bounded
  ([`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md)).

The difference from those precedents: CKM-EDM and confinement each bundle
an exact retained component (`d_n(QCD) = 0`, `T = 0` confinement) with a
bounded numerical continuation on *the same observable* (`d_n(CKM)`,
`sqrt(sigma)`). Here the EOS `w` is the whole observable — its retained
value is `-1` exactly, with no separate bounded numerical continuation on
that same observable. The bounded parts live in the adjacent `Lambda` and
`Omega_Lambda` rows.

## Safe Claim Boundary

What this lane supports:

- on the retained `S^3` + spectral-gap + fixed-`R` surface, the dark-energy
  density is exactly time-independent and `w = -1` is exact;
- every Taylor coefficient of `w(a_sc)` in `(1 - a_sc)` vanishes except the
  constant `-1`; in particular the CPL parameters are `w_0 = -1`, `w_a = 0`
  exactly;
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
companion-lane identification `Lambda = lambda_1(S^3)` that is already used
by the cosmology companion stack.

## Observational Falsifiability

This is a clean binary prediction. DESI, Euclid, and SPHEREx are actively
constraining the CPL `(w_0, w_a)` plane. The exact SN compilation changes the
central values; across the combinations used in DESI DR1 (2024) and DR2
(2025), the published BAO + CMB + Type Ia SN posteriors showed a persistent
`2-4 sigma` preference for `(w_0, w_a) != (-1, 0)` depending on which SN
sample is combined. The DR2 update did not collapse that tension to LCDM;
it held or modestly strengthened for most combinations. DESI final (2026-2027)
is forecast to reach a few-percent absolute precision on `w_0`.

Any `> 5 sigma` detection of `w_0 != -1` or `w_a != 0` falsifies the
spectral-gap vacuum identification used by the retained corollary. Any
detection of `w < -1` at any epoch is independently a phantom-crossing
falsification.

Retained framework corrections to `w = -1`:

- lattice-discretization drift bound: `|delta w| < (1/4)(l_P / R)^2
  ~ 3 x 10^-123` at the vacuum scale `R ~ R_H`, under any conceivable
  evolution of `l_P / R` consistent with both being fixed constants;
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
quantitative component stack (matrix section B), matching the existing
9-column schema, is:

| Quantity / lane | Workstream | Framework result | Observation / comparator | Claim-strength status | Import class | Current publication decision | Authority / best source | Frozen-out ref |
|---|---|---|---|---|---|---|---|---|
| Dark energy EOS `w` | spectral-gap cosmology | `w = -1` exactly on retained `S^3` + spectral-gap + fixed-`R` surface; CPL `(w_0, w_a) = (-1, 0)` | observationally near `-1`, DESI BAO + CMB + SN posteriors show persistent 2-4 sigma preference for `w != -1` depending on SN combination | retained structural corollary (companion-surface conditional) | retained `S^3` topology + retained spectral gap `lambda_1 = 3/R^2` + companion-lane spectral-gap vacuum identification `Lambda = lambda_1(S^3_R)` + fixed `R` | retained corollary may appear on the flagship / SI surface; numerical `Lambda` stays the existing bounded/conditional companion row | this note + [DARK_ENERGY_EOS_NOTE.md](../../DARK_ENERGY_EOS_NOTE.md) + [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) | `F04` |

The adjacent `Cosmological constant Lambda` row and the remaining cosmology
companion rows are **not** proposed for change.

This row framing mirrors the existing "CKM-only neutron EDM on the retained
`theta_eff = 0` surface" row in that the retention is structurally exact but
carries a named companion-surface conditioning (there: the EFT bridge; here:
the spectral-gap vacuum identification).

## Commands Run

```bash
python3 scripts/frontier_dark_energy_eos_retained_corollary.py
```
