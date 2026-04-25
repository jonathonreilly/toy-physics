# Planck Source-Unit Normalization Hostile Review

**Date:** 2026-04-25
**Status:** internal hostile review of the standalone source-unit theorem
**Reviewed theorem:**
[PLANCK_SOURCE_UNIT_NORMALIZATION_CLEAN_THEOREM_2026-04-25.md](./PLANCK_SOURCE_UNIT_NORMALIZATION_CLEAN_THEOREM_2026-04-25.md)
**Runner:**
`scripts/frontier_planck_source_unit_normalization_clean_theorem.py`

## Executive Verdict

The corrected theorem clears the previously identified `4 pi` mismatch only if
the submission explicitly distinguishes four objects:

```text
G_kernel = 1/(4 pi)          bare unit-delta Green coefficient,
C                             exterior monopole / normalized Gauss charge,
lambda                        possible mass-unit scale M_lambda=lambda C,
G_Newton,lat = 1            physical coefficient after c_cell fixes lambda=1.
```

Under that distinction, the conventional Planck closure is algebraically
complete:

```text
c_cell = 1/4 = 1/(4 G_Newton,lat),
G_phys = a^2 G_Newton,lat = a^2,
l_P^2 = G_phys,
a/l_P = 1.
```

The prior review finding is resolved because `c_cell` is no longer identified
with the raw Einstein-Hilbert prefactor. It is identified with the
boundary/Wald area coefficient. The bulk prefactor is

```text
1/(16 pi G_Newton,lat) = c_cell/(4 pi).
```

This is the correct action-to-area bookkeeping.

## Hostile Findings And Resolutions

### Finding 1: This may be a unit choice disguised as a theorem

**Pressure.** A reviewer may say the theorem merely chooses mass units so that
`G_Newton,lat = 1`, then declares the lattice spacing to be Planckian.

**Resolution.** The theorem does not choose `G_Newton,lat = 1` directly. It
keeps the free scale visible. Exterior observability and additivity prove only
`M_lambda = lambda C`, where `C` is the normalized Gauss charge / asymptotic
monopole coefficient. In that family `G_lambda = 1/lambda` and the
boundary-area coefficient is `1/(4G_lambda) = lambda/4`. The primitive carrier
then fixes `lambda = 1` because `c_cell = 1/4`. Only after that does
`q_bare = 4 pi M_phys` and `G_Newton,lat = 1` follow. This removes the
"you set G to one" attack.

### Finding 1b: Raw Gauss flux could be confused with normalized charge

**Pressure.** A bare unit delta has raw flux one, so a reviewer may object that
the theorem arbitrarily prefers a source with raw flux `4 pi`.

**Resolution.** The physical mass is not the raw flux of `phi`; it is the
normalized Gauss charge

```text
M_phys = -(1/(4 pi)) int n.grad(phi) dA.
```

For a positive Green response `phi -> C/r`, the oriented outward flux of
`grad phi` is `-4 pi C` and normalized charge is `C`. The bare unit delta has
`C = 1/(4 pi)`. The primitive area carrier then fixes the physical mass unit
to `M_phys = C`, so a unit Newton mass has `C = 1`. This is exactly the same
distinction as `G_kernel = 1/(4 pi)` versus `G_Newton,lat = 1`.

### Finding 2: The old `G_lat = 1/(4 pi)` statement conflicts with closure

**Pressure.** Mainline notes have called `1/(4 pi)` the lattice Newton
constant. If that wording is retained, the theorem is inconsistent and the
Planck map gives `a/l_P = 2 sqrt(pi)`.

**Resolution.** The submission must rename the old quantity:

```text
G_kernel = 1/(4 pi).
```

It is the bare Green-kernel coefficient for `q_bare = 1`. In the
one-parameter exterior-charge family, the old wording corresponds to

```text
lambda_bare = 4 pi,
G_bare = 1/(4 pi),
1/(4G_bare) = pi.
```

That conflicts with `c_cell = 1/4`. The physical coefficient after carrier
normalization is `G_Newton,lat = 1`.

### Finding 3: The EH prefactor/BH area coefficient conflation must stay fixed

**Pressure.** The earlier failed closure identified `c_cell = 1/4` with
`1/(16 pi G)` and then used it as `1/(4G)`.

**Resolution.** The revised theorem explicitly separates them:

```text
BH/Wald/Planck area coefficient = 1/(4G) = c_cell = 1/4,
EH bulk prefactor = 1/(16 pi G) = c_cell/(4 pi) = 1/(16 pi).
```

The submission should not call `c_cell` the raw EH prefactor.

### Finding 4: The source-unit theorem could smuggle standard continuum GR

**Pressure.** A hostile reviewer may say the theorem imports the standard
Poisson equation `(-Delta) phi = 4 pi G rho` from outside the stack.

**Resolution.** The proof should be ordered from the retained native equation:

```text
(-Delta) phi = q_bare delta_0,
K(r) -> 1/(4 pi r).
```

Only after deriving `lambda = 1` and `q_bare = 4 pi M_phys` should the text
rewrite the same equation as

```text
(-Delta) phi = 4 pi rho_phys.
```

That rewrite is an output of the source-unit theorem, not an input.

### Finding 5: The inertial/test-mass side must use the same source readout

**Pressure.** The proof fixes source mass. Newton's product law also needs the
test-mass response to use the same physical mass convention.

**Resolution.** The theorem now adds an explicit two-body lock. A source
`M_2` has `q_2,bare = 4 pi M_2`, so `phi_2 -> M_2/r`. A test body with the
same physical mass readout obeys

```text
F_12 = -M_1 grad(phi_2) -> M_1 M_2/r^2.
```

The physical force law is written only after both source and test response are
expressed in `M_phys` units. Any formula that still uses a bare `M` is
ambiguous and should be updated before submission.

### Finding 6: The finite primitive carrier cannot derive `pi`

**Pressure.** If the text suggests the `16`-state primitive cell derives
`4 pi`, the claim is false. Finite trace coefficients are rational.

**Resolution.** The theorem must keep the sources separate:

```text
c_cell = 1/4        from finite primitive counting,
4 pi                from retained continuum/lattice Green asymptotic,
lambda = 1          from matching c_cell = lambda/4,
q_bare = 4 pi M     after carrier normalization.
```

The finite carrier supplies the quarter coefficient only.

### Finding 7: The result is not an SI Planck-length prediction

**Pressure.** A reviewer will reject any claim that the theorem predicts the
decimal SI values of `G`, `l_P`, `M_Pl`, or `hbar`.

**Resolution.** The theorem closes the natural-unit lattice relation
`a/l_P = 1`. SI realization still requires the usual external unit conventions
and measured constants. The submission must not advertise an SI decimal
derivation.

### Finding 8: The theorem depends on the primitive boundary carrier premise

**Pressure.** Exterior observability and additivity alone do not give
`G_Newton,lat = 1`; they leave the scale `lambda` free. If the primitive
carrier is not accepted as the boundary/Wald area carrier, the source-unit
closure cannot fix that scale.

**Resolution.** The submission must keep the proof chain explicit:

```text
primitive carrier theorem => c_cell = 1/4,
exterior-source theorem   => M_lambda = lambda C, G_lambda = 1/lambda,
area-carrier theorem      => lambda = 1,
source-unit theorem       => q_bare = 4 pi M_phys, G_Newton,lat = 1,
area coefficient           => 1/(4G_Newton,lat) = 1/4,
unit map                   => a/l_P = 1.
```

If the primitive carrier is not accepted as the boundary/Wald area carrier, the
Planck closure remains conditional on that carrier premise.

## Required Submission Updates

Before harsh external review, update the submitted text as follows:

1. Replace physical `G_lat = 1/(4 pi)` with bare
   `G_kernel = 1/(4 pi)`.
2. Add the exterior-charge theorem: physical Newton mass is the normalized
   Gauss charge / asymptotic monopole coefficient up to a scale
   `M_lambda = lambda C`.
3. Show that the primitive area carrier fixes that scale:
   `c_cell = 1/(4G_lambda) = lambda/4`, hence `lambda = 1`.
4. Add the source-conversion theorem statement `q_bare = 4 pi M_phys`.
5. Introduce `G_Newton,lat = 1` only after the `lambda = 1` proof.
6. Change any sentence saying `c_cell` equals the EH prefactor to say
   `c_cell` equals the boundary/Wald/Planck-area coefficient.
7. State the EH prefactor as `c_cell/(4 pi)`.
8. Mark every mass/source symbol as `q_bare`, `rho_phys`, or `M_phys`.
9. Include the explicit fallback calculation
   `G_kernel = 1/(4 pi) => a/l_P = 2 sqrt(pi)`.
10. Avoid SI decimal claims and avoid saying the finite cell derives `pi`.

## Backpressure Verdict

After the above corrections, the theorem is review-ready as a clean closure on
its stated premises. It is not a broad literature claim and does not need
repo-wide weaving to stand. The remaining external decision is sharply
localized:

```text
Does the primitive boundary/Wald carrier legitimately fix lambda=1 in the
exterior monopole charge family?
```

If yes, the `4 pi` gap is closed and the Planck map gives `a/l_P = 1`. If no,
the theorem fails cleanly and the standing result remains `a/l_P = 2 sqrt(pi)`
on the bare-source surface.
