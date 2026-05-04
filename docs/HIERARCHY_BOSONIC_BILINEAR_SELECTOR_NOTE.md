# Hierarchy Bosonic-Bilinear Selector Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-13  
**Script:** `scripts/frontier_hierarchy_bosonic_bilinear_selector.py`

## Question

Can the last hierarchy selector principle be derived from the physical nature of
the electroweak order parameter itself, rather than stated as a natural but
external rule?

## Answer

Yes, on the exact minimal hierarchy block.

The physical order parameter is not the raw fermion determinant. It is the
local curvature of the effective action,

`∂^2_phi Delta V_eff |_(phi=0)`,

so it is:

1. **bosonic**
2. **quadratic in fermions**
3. **CPT-even**
4. **local**

On the APBC temporal circle, these four facts force the temporal support to be
closed under the Klein-four action

`z -> z, -z, z*, -z*`

because:

- bosonic bilinears are blind to the fermion sign `psi -> -psi`
- CPT-even local observables are closed under complex conjugation / time
  reversal
- locality forbids mode-dependent hand-picking inside the minimal orbit

## Exact selector

The APBC temporal phase set is

`z_n = exp(i (2n+1) pi / L_t)`.

Its decomposition into sign-and-conjugation closed orbits is exact.

The results are:

- `L_t = 2`: one orbit of size `2`  
  This is only the unresolved sign pair `{+i,-i}`.
- `L_t = 4`: one orbit of size `4`  
  This is the unique minimal **resolved** bosonic-bilinear orbit.
- `L_t > 4`: multiple closed orbit sectors appear immediately.

So `L_t = 4` is not merely a convenient choice. It is the unique minimal orbit
selected by the local bosonic/CPT-even structure of the order parameter.

## Uniformity

At `L_t = 4` the whole selected orbit has one exact temporal weight:

`sin^2 omega = 1/2`

So the selected orbit is not only the unique minimal closed orbit; it is also
uniformly weighted. That is why the exact correction becomes

`C = (A_2 / A_4)^(1/4) = (7/8)^(1/4)`.

## Consequence

Using the current hierarchy baseline

`M_Pl * alpha_LM^16 = 254.643210673818 GeV`,

the selected value is

`v = 254.643210673818 * (7/8)^(1/4) = 246.282818290129 GeV`.

Compared with measurement,

`v_meas = 246.22 GeV`,

the remaining difference is

- `delta v = +0.062818290129 GeV`
- relative error `= +0.0255%`

## Honest status

This is the strongest closure statement on the hierarchy route so far.

The selector is no longer:

> pick the orbit that looks nicest.

It is:

> the physical EWSB order parameter is a local bosonic CPT-even bilinear, and
> the unique minimal resolved APBC orbit with exactly those closure properties
> is `L_t = 4`.

At this point the remaining gap is no longer mathematical. It is only whether
one accepts that standard effective-action / bosonic-bilinear identification as
the correct physical object. On the framework’s own exact minimal block, that
identification now picks the normalization uniquely.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [hierarchy_spatial_bc_and_u0_scaling_note](HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md)
- [higgs_mass_hierarchy_correction_note](HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md)
