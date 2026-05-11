# Planck Source-Unit Normalization Support Theorem

**Date:** 2026-04-25
**Status:** proposed_retained support theorem on the conditional Planck packet;
not a standalone minimal-stack closure of `a^(-1) = M_Pl`
**Runner:**
`scripts/frontier_planck_source_unit_normalization_support_theorem.py`

## Inputs (cited authorities)

This note imports the primitive boundary/Wald carrier `c_cell = 1/4` and
its identification `c_cell = 1/(4 G_lambda)` as load-bearing premises.
The carrier itself is not derived in this note; it is imported from the
conditional Planck packet's primitive-cell theorem chain:

- [`AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md`](AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md)
  — minimal local-CAR assumptions under which the primitive parity-gate
  carrier is forced by the primitive boundary block itself.
- `AREA_LAW_COEFFICIENT_GAP_NOTE.md` (context recording only, backticked
  to avoid length-3 cycle — this note imports `c_cell = 1/4` from the
  primitive-coframe carrier theorem and its boundary-density extension,
  not from the coefficient-gap synthesis note; citation graph direction
  is *downstream synthesis → this support theorem*) — synthesises
  `c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4` across the conditional Planck
  packet authority chain.

The carrier-side identification `c_cell = 1/(4 G_lambda)` is the
Wald-Noether area-law reading on the same conditional Planck packet; it
is part of the same packet's external authority surface and is not
derived from physical `Cl(3)` on `Z^3` alone. This note explicitly flags
itself as not a standalone minimal-stack closure of `a^(-1) = M_Pl`; the
source-unit normalization clarifies the bare/Newton mass-unit accounting
once the carrier and its Wald reading are accepted.

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

The clean support result is to separate the bare source coefficient from the
physical Gauss/Newton source unit. The retained lattice theorem remains

```text
(-Delta) K = delta_0,
K(r) -> 1/(4 pi r).
```

The physical source unit is not the arbitrary unit coefficient of the regulator
delta. Exterior observability first gives a one-parameter family of possible
mass units:

```text
phi(r) -> C/r,
M_lambda = lambda C,
G_lambda = 1/lambda.
```

The bare-source label is one member of this family:

```text
M_bare = q_bare = 4 pi C,
lambda_bare = 4 pi,
G_bare = 1/(4 pi).
```

On the same conditional carrier surface already isolated on `main`, the
primitive boundary/Wald carrier fixes the remaining scale:

```text
c_cell = 1/4,
c_cell = 1/(4 G_lambda) = lambda/4,
lambda = 1.
```

Therefore the physical Newton source unit is the normalized Gauss/asymptotic
monopole unit:

```text
M_phys = C,
q_bare = 4 pi M_phys.
```

Therefore the physical lattice Newton coefficient is

```text
G_Newton,lat = (4 pi) G_kernel = 1.
```

With that source-unit normalization, the same carrier coefficient gives the
conventional Planck map:

```text
c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4,
c_cell = 1/(4 G_Newton,lat),
G_phys = a^2 G_Newton,lat = a^2,
l_P^2 = G_phys,
a/l_P = 1,
a^(-1) = M_Pl.
```

This does not erase the retained Green theorem. It corrects which quantity is
called the physical Newton constant on the conditional Planck carrier surface.
It sharpens the existing conditional-completion packet; it does not remove the
remaining minimal-stack blocker that the primitive boundary count still has to
be accepted or derived as the gravitational boundary/action carrier.

## Import Ledger

| Item | Role | Status |
|---|---|---|
| `Cl(3)` on `Z^3` | substrate and lattice dimension | retained package substrate |
| `(-Delta) K = delta_0` | native bare-source Poisson equation | retained |
| `K(r) -> 1/(4 pi r)` | Green-kernel asymptotic | retained theorem |
| Gauss/asymptotic monopole readout | exterior scalar source charge `C` | axiom-native field readout from the same divergence-form Poisson law |
| `M_lambda = lambda C` | possible source-unit family | derived from exterior observability and additivity |
| `c_cell = 1/4` | primitive boundary/Wald area carrier | retained primitive-cell theorem |
| `lambda = 1` | physical source-unit scale | derived by matching `c_cell = 1/(4G_lambda)` |
| `q_bare = 4 pi M_phys` | source-unit conversion | derived theorem |
| `G_Newton,lat = 1` | physical lattice Newton coefficient | derived from `lambda = 1` |
| `l_P^2 = G_phys` | conventional Planck target in `hbar=c=1` units | external target definition, not derived |
| SI values of `l_P`, `M_Pl`, `G` | decimal unit realization | not imported |

The only external input is the conventional target definition
`l_P^2 = G_phys`. No measured value of `G`, `l_P`, `M_Pl`, or `hbar` is used.
This theorem is therefore a support theorem for the existing conditional
Planck packet, not a replacement for the current package pin.

The later Target 3 Clifford phase bridge supplies a sufficient carrier route
under the primitive metric-compatible coframe-response premise. Under that
conditional bridge, this support theorem becomes the source-unit leg of the
structural Planck packet:

```text
c_Widom = c_cell = 1/4,
G_Newton,lat = 1,
a/l_P = 1.
```

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

## Lemma 2: Exterior Observability Leaves One Source-Scale `lambda`

This is the proof obligation behind the phrase "physical Newton mass."
Exterior field data alone does not prove `M_phys = C`; it proves only that
active gravitational mass is proportional to the exterior monopole
coefficient. The proportionality must be kept explicit until the primitive
boundary-area carrier fixes it.

The exterior-source theorem uses two operational requirements:

1. **Exterior observability.** A gravitational source charge must be readable
   from the field outside any compact source. Two compact sources with the
   same exterior field have the same active gravitational mass.
2. **Additivity.** Disjoint compact sources have additive gravitational mass.

For any compact source, the exterior solution is harmonic and has multipole
expansion

```text
phi(r,Omega) = C/r + dipole/r^2 + ...
```

The only rotational scalar visible at leading exterior order is the monopole
coefficient `C`. Additivity of the field makes `C` additive under disjoint
sources. Therefore any exterior-observable additive active mass readout has
the form

```text
M_lambda = lambda C
```

for a constant `lambda > 0`. The same exterior scalar can be written as
normalized Gauss charge:

```text
C = -(1/(4 pi)) lim_{R -> infinity} int_{S_R} n . grad phi dA.
```

For a positive Green response `phi -> C/r`, the oriented outward flux of
`grad phi` is `-4 pi C`, while the normalized Gauss charge is `C`.

The bare regulator coefficient fails the exterior-observability test as a
canonical physical definition: changing the source variable normalization
changes the coefficient called `q_bare`, while the exterior field and
normalized Gauss charge are unchanged. The observable object is the exterior
monopole coefficient `C`; the remaining question is which `lambda` the
gravitational area carrier selects.

For a point source,

```text
C = q_bare/(4 pi),
M_lambda = lambda q_bare/(4 pi),
q_bare = (4 pi/lambda) M_lambda.
```

The associated Newton coefficient in the mass unit `M_lambda` is

```text
phi(r) -> C/r = M_lambda/(lambda r),
G_lambda = 1/lambda.
```

The old bare-source convention corresponds to `M_bare = q_bare`, so

```text
lambda_bare = 4 pi,
G_bare = 1/(4 pi).
```

This is exactly the harsh-review failure mode.

## Lemma 3: Primitive Area Carrier Fixes `lambda = 1`

The primitive source-free event cell gives

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16,
rank(P_A) = 4,
rho_cell = I_16/16,
c_cell = Tr(rho_cell P_A) = 4/16 = 1/4.
```

For a Newton coefficient `G_lambda = 1/lambda`, the conventional
boundary/Wald/Planck-area coefficient in lattice units is

```text
1/(4 G_lambda) = lambda/4.
```

The primitive carrier premise identifies this coefficient with `c_cell`:

```text
c_cell = lambda/4.
```

Since `c_cell = 1/4`,

```text
lambda = 1.
```

Thus the physical active mass selected by the primitive area carrier is

```text
M_phys = M_lambda=1 = C.
```

Substituting `lambda = 1` into the source conversion gives

```text
q_bare = 4 pi M_phys.
```

This is no longer a free choice to set `G=1`. It is the unique member of the
exterior-charge family compatible with the primitive boundary/Wald area
carrier. The bare-source convention `lambda = 4 pi` would give
`1/(4G_bare) = pi`, not `c_cell = 1/4`.

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

which is the standard Poisson normalization with `G_Newton,lat = 1`. That
rewrite is an output of the exterior-charge plus primitive-carrier theorem,
not an imported starting convention.

## Lemma 5: Source Conversion Is Unique After `lambda = 1`

A trial source conversion `q_bare = sigma M_phys` produces monopole
coefficient

```text
sigma/(4 pi).
```

After the primitive carrier has fixed `M_phys = C`, unit physical mass has
`C = 1`. Thus

```text
sigma/(4 pi) = 1,
sigma = 4 pi.
```

## Lemma 6: The Product Law Uses the Same Physical Mass Unit

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

## Lemma 7: The Old `2 sqrt(pi)` Result Is the Bare-Source Failure Mode

If the bare source label is used as the physical Newton mass,

```text
lambda_bare = 4 pi,
G_bare = 1/(4 pi),
G_phys = a^2 G_bare,
l_P^2 = G_phys,
```

then

```text
l_P^2 = a^2/(4 pi),
a/l_P = 2 sqrt(pi).
```

This remains the correct rejection result for the bare-source convention. The
positive theorem does not deny it. It says the primitive area carrier rejects
`lambda_bare = 4 pi` because it would give the boundary area coefficient
`1/(4G_bare) = pi`, not `c_cell = 1/4`.

## Lemma 8: EH/BH Bookkeeping After Source Normalization

After Lemma 3 fixes `lambda = 1`,

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
  exterior monopole observability and additivity up to an explicit scale
  `lambda`;
- the primitive event-cell count `c_cell = 1/4`;
- the conventional target definition of Planck units.

It does not use:

- measured Cavendish `G`;
- measured Planck length or Planck mass;
- an external numerical fit;
- a hidden rescaling of the lattice spacing or source mass;
- a claim that finite primitive counting derives `pi`.

The finite primitive carrier supplies `1/4`. The continuum Green/Gauss theorem
supplies the already-retained `4 pi` angular normalization. The new theorem is
that the exterior monopole family `M_lambda = lambda C` has its remaining
scale fixed by the primitive boundary/Wald carrier: `c_cell = lambda/4`, so
`lambda = 1`.

## Reviewer Hinge

The whole closure stands or falls on one reviewer-facing proposition:

> The primitive boundary/Wald carrier fixes the exterior monopole mass scale
> `lambda` to `1`; physical Newton mass is then the normalized
> Gauss/asymptotic monopole unit, not the coefficient of a regulator delta
> source in the unnormalized Green equation.

In proof form, this is the exterior-observable additive source-charge theorem:
the only scalar active gravitational charge visible at infinity is proportional
to the normalized Gauss charge / monopole coefficient. The primitive carrier
then fixes the proportionality. The bare delta coefficient is only a
source-coordinate label until that carrier normalization has been applied.

If accepted, the proof has no remaining free factor:

```text
G_kernel = 1/(4 pi),
M_lambda = lambda C,
c_cell = lambda/4,
lambda = 1,
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
2. Introduce the exterior monopole family `M_lambda = lambda C`, with
   `G_lambda = 1/lambda`.
3. Use the primitive carrier to fix `lambda`:
   `c_cell = 1/(4G_lambda) = lambda/4 = 1/4`.
4. Introduce `G_Newton,lat = 1` and `q_bare = 4 pi M_phys` only after proving
   `lambda = 1`.
5. State that `c_cell = 1/4` is the boundary/Wald/Planck-area carrier, not the
   raw Einstein-Hilbert bulk prefactor.
6. Write the bulk Einstein-Hilbert prefactor as `c_cell/(4 pi) = 1/(16 pi)`.
7. Distinguish every source variable as either `q_bare` or `M_phys`.
8. Preserve the old `a/l_P = 2 sqrt(pi)` calculation as the explicit
   bare-source failure mode.
9. Do not claim that finite primitive counting derives `pi`, `hbar`, or any SI
   decimal value.

## Verification

Run:

```bash
python3 scripts/frontier_planck_source_unit_normalization_support_theorem.py
```

The runner checks the retained kernel coefficient, the explicit `lambda`
source-scale family, the primitive-carrier selection `lambda = 1`, the Gauss
source conversion, the uniqueness of the `4 pi` source unit, the physical
two-body product law, the old bare-source failure mode, the boundary/Wald
coefficient, the Einstein-Hilbert prefactor relation, and the final
`a/l_P = 1` map.
