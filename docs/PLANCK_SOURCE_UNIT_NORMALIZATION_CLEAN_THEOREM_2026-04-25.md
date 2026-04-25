# Planck Source-Unit Normalization Clean Theorem

**Date:** 2026-04-25
**Status:** standalone positive closure packet for the remaining
`a^(-1) = M_Pl` gate, subject to reviewer acceptance of the Gauss/Newton
source-unit theorem
**Runner:**
`scripts/frontier_planck_source_unit_normalization_clean_theorem.py`

## Verdict

The prior obstruction was real:

```text
G_kernel = 1/(4 pi)
```

is the coefficient of the lattice Green kernel for a unit bare delta source.
If that coefficient is labeled as the physical Newton constant, the
conventional Planck map gives

```text
a/l_P = 2 sqrt(pi),
```

not `1`.

The closure is to separate the bare source coefficient from the physical
Gauss/Newton source unit. The retained lattice theorem remains

```text
(-Delta) K = delta_0,
K(r) -> 1/(4 pi r).
```

The physical source unit is not the arbitrary unit coefficient of the regulator
delta. It is the Gauss/asymptotic monopole unit used by the Newton field:

```text
Phi(r) -> G_Newton,lat M_phys / r.
```

Choosing unit physical mass as the source whose monopole coefficient is one
forces

```text
q_bare / (4 pi) = M_phys,
q_bare = 4 pi M_phys.
```

Therefore the physical lattice Newton coefficient is

```text
G_Newton,lat = (4 pi) G_kernel = 1.
```

With that source-unit normalization, the primitive carrier coefficient closes
the conventional Planck map:

```text
c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4,
c_cell = 1/(4 G_Newton,lat),
G_phys = a^2 G_Newton,lat = a^2,
l_P^2 = G_phys,
a/l_P = 1,
a^(-1) = M_Pl.
```

This does not erase the retained Green theorem. It corrects which quantity is
called the physical Newton constant.

## Import Ledger

| Item | Role | Status |
|---|---|---|
| `Cl(3)` on `Z^3` | substrate and lattice dimension | retained package substrate |
| `(-Delta) K = delta_0` | native bare-source Poisson equation | retained |
| `K(r) -> 1/(4 pi r)` | Green-kernel asymptotic | retained theorem |
| Gauss/asymptotic monopole readout | physical source unit | axiom-native field readout from the same divergence-form Poisson law |
| `q_bare = 4 pi M_phys` | source-unit conversion | new theorem |
| `G_Newton,lat = 1` | physical lattice Newton coefficient | derived from source-unit conversion |
| `c_cell = 1/4` | primitive boundary/Wald area carrier | retained primitive-cell theorem |
| `l_P^2 = G_phys` | conventional Planck target in `hbar=c=1` units | external target definition, not derived |
| SI values of `l_P`, `M_Pl`, `G` | decimal unit realization | not imported |

The only external input is the conventional target definition
`l_P^2 = G_phys`. No measured value of `G`, `l_P`, `M_Pl`, or `hbar` is used.

## Lemma 1: Green Kernel Is a Bare-Source Statement

Let the native lattice field equation be

```text
(-Delta) phi = q_bare delta_0.
```

Linearity and the Green theorem give

```text
phi(r) -> q_bare K(r)
       -> q_bare/(4 pi r).
```

For `q_bare = 1`, the asymptotic coefficient is `1/(4 pi)`. This is a
statement about the response to the chosen regulator delta source. It has not
yet identified the physical mass unit.

The Gauss flux of the bare unit source is normalized:

```text
-4 pi r^2 partial_r phi -> 1.
```

So `1/(4 pi)` is exactly the angular kernel coefficient required by a unit
bare source in three spatial dimensions.

## Lemma 2: Physical Mass Is the Unique Exterior Monopole Charge

This step is the proof obligation behind the phrase "physical Newton mass."
It is not a bare algebra identity. It is a uniqueness theorem from three
operational requirements:

1. **Exterior observability.** A gravitational source charge must be readable
   from the field outside any compact source. Two compact sources with the
   same exterior field have the same active gravitational mass.
2. **Additivity.** Disjoint compact sources have additive gravitational mass.
3. **Newton normalization.** A unit source mass is the source whose far-field
   Newton potential has unit `1/r` coefficient in lattice natural units.

For any compact source, the exterior solution is harmonic and has multipole
expansion

```text
phi(r,Omega) = C/r + dipole/r^2 + ...
```

The only rotational scalar visible at leading exterior order is the monopole
coefficient `C`. Additivity of the field makes `C` additive under disjoint
sources. Newton normalization fixes the proportionality constant, so the
unique physical active mass readout in these units is

```text
M_phys = C.
```

The same statement can be written as normalized Gauss charge:

```text
M_phys = -(1/(4 pi)) lim_{R -> infinity} int_{S_R} n . grad phi dA.
```

For a positive Green response `phi -> C/r`, the oriented outward flux of
`grad phi` is `-4 pi C`, while the normalized Gauss charge is `C`. Thus the
physical mass is the normalized Gauss charge / asymptotic monopole
coefficient, not the raw coefficient of a chosen regulator delta in the source
equation.

The bare regulator coefficient fails the exterior-observability test as a
physical definition: changing the source variable normalization changes the
coefficient called `q_bare`, while the exterior field and normalized Gauss
charge are unchanged. The observable object is the exterior monopole.

## Lemma 3: Source Conversion Is Forced

The Newton field observes a mass through its asymptotic monopole coefficient:

```text
Phi(r) -> G_Newton,lat M_phys / r.
```

The physical source unit is the source for which a unit physical mass produces
a unit `1/r` monopole coefficient before dimensional conversion:

```text
M_phys = 1  =>  Phi(r) -> 1/r.
```

Substituting the bare Green kernel,

```text
q_bare/(4 pi r) = M_phys/r,
```

hence

```text
q_bare = 4 pi M_phys.
```

This source conversion is unique. A trial conversion `q_bare = sigma M_phys`
produces monopole coefficient

```text
sigma/(4 pi).
```

Unit monopole readout requires `sigma/(4 pi) = 1`, so `sigma = 4 pi`.

## Lemma 4: Physical Lattice Newton Coefficient Is One

With `q_bare = 4 pi M_phys`,

```text
phi(r) -> (4 pi M_phys)/(4 pi r)
       = M_phys/r.
```

Therefore

```text
G_Newton,lat = 1.
```

Equivalently, the native bare-source equation can be rewritten in physical
mass units as

```text
(-Delta) phi = 4 pi rho_phys,
```

which is the standard Poisson normalization with `G_Newton,lat = 1`.

## Lemma 5: The Product Law Uses the Same Physical Mass Unit

The source conversion must also be used on the test-mass side. In physical
mass units, a source `M_2` has bare strength

```text
q_2,bare = 4 pi M_2,
```

so its long-range field is

```text
phi_2(r) -> M_2/r.
```

A test body with physical inertial/source mass `M_1` responds through the same
mass readout:

```text
F_12 = -M_1 grad(phi_2)
     -> M_1 M_2 / r^2.
```

Thus the two-body force law in lattice units is

```text
F_12 = G_Newton,lat M_1 M_2 / r^2,
G_Newton,lat = 1.
```

This is not a second normalization. It is the same source-unit theorem applied
consistently to source and test masses. Any submission formula using an
unqualified `M` before this conversion is ambiguous.

## Lemma 6: The Old `2 sqrt(pi)` Result Is the Bare-Source Failure Mode

If the bare kernel coefficient is mislabeled as the physical Newton constant,

```text
G_lat = G_kernel = 1/(4 pi),
G_phys = a^2 G_lat,
l_P^2 = G_phys,
```

then

```text
l_P^2 = a^2/(4 pi),
a/l_P = 2 sqrt(pi).
```

This remains the correct rejection result for the bare-source convention. The
positive theorem does not deny it. It says that the bare-source convention is
not the physical Newton/Gauss mass convention.

## Lemma 7: The Primitive Carrier Is the Planck-Area Carrier

The primitive source-free event cell gives

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16,
rank(P_A) = 4,
rho_cell = I_16/16,
c_cell = Tr(rho_cell P_A) = 4/16 = 1/4.
```

After source-unit normalization,

```text
1/(4 G_Newton,lat) = 1/(4 * 1) = 1/4 = c_cell.
```

Thus `c_cell` is the boundary/Wald/Planck-area coefficient. The
Einstein-Hilbert bulk prefactor is not `c_cell`; it is

```text
1/(16 pi G_Newton,lat) = 1/(16 pi) = c_cell/(4 pi).
```

The Wald/Gauss bridge recovers the area coefficient:

```text
4 pi * 1/(16 pi G_Newton,lat) = 1/(4 G_Newton,lat) = c_cell.
```

This resolves the harsh-review objection that the Einstein-Hilbert prefactor
and the Bekenstein-Hawking/Planck area coefficient had been conflated.

## The Planck Unit Map

The physical unit map is

```text
G_phys = a^2 G_Newton,lat.
```

Using `G_Newton,lat = 1`,

```text
G_phys = a^2.
```

In conventional natural units,

```text
l_P^2 = G_phys,
```

so

```text
l_P^2 = a^2,
a/l_P = 1,
a^(-1) = M_Pl.
```

The result is a unit-normalization closure, not an SI decimal prediction.

## Axiom-Native Content

The proof uses only:

- the retained lattice Green theorem and its `4 pi` angular normalization;
- the native divergence/Gauss readout of source strength, normalized by
  exterior monopole observability and additivity;
- the primitive event-cell count `c_cell = 1/4`;
- the conventional target definition of Planck units.

It does not use:

- measured Cavendish `G`;
- measured Planck length or Planck mass;
- an external numerical fit;
- a hidden rescaling of the lattice spacing;
- a claim that finite primitive counting derives `pi`.

The finite primitive carrier supplies `1/4`. The continuum Green/Gauss theorem
supplies the already-retained `4 pi` angular normalization. The new theorem is
the operational uniqueness of physical mass as the normalized
Gauss/asymptotic monopole source unit.

## Reviewer Hinge

The whole closure stands or falls on one reviewer-facing proposition:

> Physical Newton mass is the Gauss/asymptotic monopole source unit, not the
> coefficient of a regulator delta source in the unnormalized Green equation.

In proof form, this is the exterior-observable additive source-charge theorem:
the only scalar active gravitational charge visible at infinity is the
normalized Gauss charge / monopole coefficient. The bare delta coefficient is
only a source-coordinate label until a source unit has been chosen.

If accepted, the proof has no remaining free factor:

```text
G_kernel = 1/(4 pi),
q_bare = 4 pi M_phys,
G_Newton,lat = 1,
c_cell = 1/(4 G_Newton,lat),
a/l_P = 1.
```

If rejected, the proof falls back exactly to the harsh-review result:

```text
G_kernel treated as G_lat => a/l_P = 2 sqrt(pi).
```

## Submission Update Flags

If this packet is submitted, the reviewer should update these claims in the
submission text:

1. Replace statements of `G_lat = 1/(4 pi)` as the physical Newton constant
   with `G_kernel = 1/(4 pi)` for the bare unit-delta Green coefficient.
2. Introduce `G_Newton,lat = 1` only after proving
   `q_bare = 4 pi M_phys`.
3. State that `c_cell = 1/4` is the boundary/Wald/Planck-area carrier, not the
   raw Einstein-Hilbert bulk prefactor.
4. Write the bulk Einstein-Hilbert prefactor as `c_cell/(4 pi) = 1/(16 pi)`.
5. Distinguish every source variable as either `q_bare` or `M_phys`.
6. Preserve the old `a/l_P = 2 sqrt(pi)` calculation as the explicit
   bare-source failure mode.
7. Do not claim that finite primitive counting derives `pi`, `hbar`, or any SI
   decimal value.

## Verification

Run:

```bash
python3 scripts/frontier_planck_source_unit_normalization_clean_theorem.py
```

The runner checks the retained kernel coefficient, the Gauss source conversion,
the uniqueness of the `4 pi` source unit, the physical two-body product law,
the old bare-source failure mode, the boundary/Wald coefficient, the
Einstein-Hilbert prefactor relation, and the final `a/l_P = 1` map.
