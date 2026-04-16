# Baryogenesis Closure-Gate Note

**Date:** 2026-04-16
**Status:** bounded main-branch closure-gate note
**Script:** `scripts/frontier_baryogenesis_closure_gate.py`

## Safe statement

Baryogenesis is **not** closed on the current `main` package surface.

What is already present on the retained framework surface is narrower and
cleaner:

- the electroweak `SU(2)` sector gives the required sphaleron-style
  `B+L`-violating / `B-L`-preserving structure
- the promoted CKM package supplies a nonzero weak-sector CP invariant
  `J = 3.331e-5`
- the anomaly-forced `3+1` and physical-lattice matter package provide the
  spacetime and species structure on which any EW baryogenesis calculation
  would have to run

So the unresolved step is no longer "does the framework have baryon violation
or CP violation at all?" It is:

> can the same retained electroweak surface produce a strong-enough
> out-of-equilibrium electroweak transition and transport/washout history to
> generate the observed baryon-to-photon ratio `η = 6.12e-10`?

That is the live baryogenesis gate.

## What this note does

This note packages the lane in the most reviewer-safe way currently supported
by `main`:

1. it makes the already-closed `B`-violation and weak-CP pieces explicit
2. it isolates the remaining missing electroweak transition / transport object
3. it records the exact dependency of the cosmology lane on that object

The quantitative target for that missing object is recorded separately in
[BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md](./BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md).
The next derivation-side reduction of that target is recorded in
[BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md](./BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md).
The next same-surface scalar-sector target is recorded in
[BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md](./BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md).
The graph-first selector derivation of the relevant portal scale is recorded in
[BARYOGENESIS_SELECTOR_PORTAL_NOTE.md](./BARYOGENESIS_SELECTOR_PORTAL_NOTE.md).
The resulting multiplicity / screening boundary is recorded in
[BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md](./BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md).

It does **not** claim a first-principles computation of the electroweak phase
transition, sphaleron rate, or baryon transport coefficients.

## Exact ingredients already on `main`

### 1. Sphaleron-style `B+L` violation is structurally present

On the retained one-generation taste surface:

- baryon number `B` is `1/3` on the six triplet states and `0` on the two
  singlets
- lepton number `L` is `1` on the two singlets and `0` on the six triplets
- `B` fails to commute with the electroweak `SU(2)` algebra
- the linear `B-L` anomaly cancels exactly

This is the electroweak sphaleron structure needed for the first Sakharov
condition:

- `B+L` can be violated by electroweak nonperturbative processes
- `B-L` remains protected

The canonical structural witness on `main` is still
[PROTON_LIFETIME_DERIVED_NOTE.md](./PROTON_LIFETIME_DERIVED_NOTE.md), but the
new runner extracts only the baryogenesis-relevant piece.

### 2. Weak-sector CP violation is quantitatively present

The promoted CKM package on `main` gives

- `|V_us| = 0.22727`
- `|V_cb| = 0.04217`
- `|V_ub| = 0.003913`
- `delta = 65.905 deg`
- `J = 3.331e-5`

on the current retained framework surface, with no fitted CKM observables or
observed quark masses entering the canonical route.

So the second Sakharov condition is already present on the same package
surface. Baryogenesis no longer lacks a nonzero CP-odd invariant.

The authority note is
[CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md).

## The remaining gate

The unresolved object is the electroweak nonequilibrium bridge:

- the strength of the relevant electroweak transition
- the surviving sphaleron rate across that transition
- the transport / diffusion conversion from the weak CP source into a frozen
  baryon asymmetry

This note treats that whole object as one missing same-surface computation.

The scalar-side part of that object is now much sharper than before:

- the exact graph-first selector surface fixes the portal scale
  `kappa_sel = 6 lambda_H`
- the exact real selector manifold by itself gives only two orthogonal scalar
  modes and therefore only about half the required cubic enhancement
- any surviving old taste-scalar route must therefore realize an additional
  effective doubling mechanism with screening milder than about `5%` to `6%`

It is cleaner to say:

> baryogenesis currently reduces to one open electroweak transition/transport
> gate

than to pretend the lane is either already closed or still missing all three
Sakharov ingredients.

## Normalization against the observed asymmetry

The observed baryon-to-photon ratio is

`η_obs = 6.12e-10`.

Using the promoted CKM invariant as the retained CP witness,

`η_obs / J = 1.837e-5`.

This number is **not** itself a theorem of baryogenesis dynamics. It is a
bookkeeping normalization:

- the framework already supplies a weak CP invariant of order `1e-5`
- the missing electroweak transition / transport bridge must convert that
  source into the final asymmetry with a net efficiency of order `1e-5`

That is the correct scale of the remaining gap on the current package surface.

## Relation to the cosmology lane

The existing bounded cosmology companion in
[OMEGA_LAMBDA_DERIVATION_NOTE.md](./OMEGA_LAMBDA_DERIVATION_NOTE.md) still
imports `η` from observation.

Once `η` is derived on the same retained surface, the rest of that chain is
already organized:

`η -> Ω_b -> R -> Ω_DM -> Ω_m -> Ω_Λ`.

So closing the baryogenesis gate would immediately upgrade the matter-content
bridge behind the present-day `Ω_Λ` lane.

## Historical route target

The current cosmology lane carries a **historical bounded target**

`v(T_c) / T_c ~ 0.52`

for the taste-scalar electroweak transition. That number is useful as route
history, but it is not promoted here as a retained theorem. Until a dedicated
same-surface EWPT runner exists, the honest claim remains that the transition
/ transport object is open.

## What this closes

This note closes the narrower but important reviewer question:

> "What exactly is still missing for baryogenesis on `main`?"

Answer:

- not baryon violation
- not weak CP violation
- not the one-generation / `3+1` matter scaffold
- only the electroweak transition / transport computation

## What this does not close

This note does **not** claim:

- a first-principles electroweak phase-transition calculation
- a first-principles sphaleron-rate calculation on the retained lattice
- a quantitative baryon transport solution
- a derived `η`
- promoted `Ω_Λ` closure from first principles

## Validation

- [frontier_baryogenesis_closure_gate.py](./../scripts/frontier_baryogenesis_closure_gate.py)
- [BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md](./BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md)
- [BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md](./BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md)
- [BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md](./BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md)
- [BARYOGENESIS_SELECTOR_PORTAL_NOTE.md](./BARYOGENESIS_SELECTOR_PORTAL_NOTE.md)
- [BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md](./BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md)
- [frontier_baryogenesis_ewpt_washout_target.py](./../scripts/frontier_baryogenesis_ewpt_washout_target.py)
- [frontier_baryogenesis_finite_t_reduction.py](./../scripts/frontier_baryogenesis_finite_t_reduction.py)
- [frontier_baryogenesis_taste_scalar_cubic_target.py](./../scripts/frontier_baryogenesis_taste_scalar_cubic_target.py)
- [frontier_baryogenesis_selector_portal.py](./../scripts/frontier_baryogenesis_selector_portal.py)
- [frontier_baryogenesis_selector_multiplicity_screening.py](./../scripts/frontier_baryogenesis_selector_multiplicity_screening.py)
- [frontier_omega_lambda_derivation.py](./../scripts/frontier_omega_lambda_derivation.py)

Current runner state:

- `frontier_baryogenesis_closure_gate.py`: expected `PASS>0`, `FAIL=0`
- `frontier_baryogenesis_ewpt_washout_target.py`: expected `PASS>0`, `FAIL=0`
- `frontier_baryogenesis_finite_t_reduction.py`: expected `PASS>0`, `FAIL=0`
- `frontier_baryogenesis_taste_scalar_cubic_target.py`: expected `PASS>0`, `FAIL=0`
- `frontier_baryogenesis_selector_portal.py`: expected `PASS>0`, `FAIL=0`
- `frontier_baryogenesis_selector_multiplicity_screening.py`: expected `PASS>0`, `FAIL=0`
- `frontier_omega_lambda_derivation.py`: existing bounded cosmology companion
