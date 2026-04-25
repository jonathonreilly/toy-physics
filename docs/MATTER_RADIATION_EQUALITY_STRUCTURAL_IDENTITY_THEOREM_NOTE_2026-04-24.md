# Matter-Radiation Equality Structural Identity Theorem

**Date:** 2026-04-24

**Status:** retained/admitted structural-identity theorem on the cosmology
support surface. This is the early-time companion to
[`COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md`](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md).
The identity itself is exact once flat FRW and standard matter/radiation
equations of state are admitted. The numerical redshift readout is
input-conditioned on present-day `Omega_m,0` and observational `Omega_r,0`;
it is not a native-axiom prediction for those density fractions.

**Primary runner:** `scripts/frontier_matter_radiation_equality_structural_identity.py`

## Statement

On the retained/admitted flat-FRW cosmology surface with pressureless matter
and radiation,

```text
w_m = 0,        rho_m(a) = rho_m,0 a^(-3),
w_r = 1/3,      rho_r(a) = rho_r,0 a^(-4),
```

matter-radiation equality obeys the exact identity

```text
(MR)  1 + z_mr = Omega_m,0 / Omega_r,0
```

or equivalently

```text
a_mr = Omega_r,0 / Omega_m,0.
```

The identity is independent of `H_0`, `Omega_Lambda,0`, and `alpha_s(v)`.
It depends only on the two present-day density fractions whose ratio it uses.

## Inputs

| Ingredient | Status |
| --- | --- |
| flat FRW | admitted cosmology layer used by the current cosmology package |
| matter EOS `w_m = 0` | standard late-time matter assumption |
| radiation EOS `w_r = 1/3` | standard relativistic-radiation assumption |
| `Omega_m,0` for numerical readout | bounded/observation-conditioned cosmology input |
| `Omega_r,0` for numerical readout | observational CMB-temperature + relativistic-species input |

The retained spectral-gap `Lambda` identity and the retained `w=-1` dark-energy
corollary are not needed for (MR). They enter the adjacent late-time FRW
kinematic theorem, not the matter-radiation equality derivation.

## Derivation

The density fractions at scale factor `a` can be written as

```text
Omega_m(a) = [Omega_m,0 a^(-3)] / E(a)^2,
Omega_r(a) = [Omega_r,0 a^(-4)] / E(a)^2,
```

where `E(a) = H(a)/H_0`. Their ratio cancels the common `E(a)^2`
denominator:

```text
Omega_m(a) / Omega_r(a)
  = [Omega_m,0 a^(-3)] / [Omega_r,0 a^(-4)]
  = (Omega_m,0 / Omega_r,0) a.
```

Matter-radiation equality is `Omega_m(a_mr) = Omega_r(a_mr)`, so

```text
(Omega_m,0 / Omega_r,0) a_mr = 1,
a_mr = Omega_r,0 / Omega_m,0,
1 + z_mr = 1/a_mr = Omega_m,0 / Omega_r,0.
```

This is the whole theorem. No late-time dark-energy parameter enters.

## Numerical Readout

Using the standard comparator values

```text
Omega_m,0 = 0.315,
Omega_r,0 = 9.2e-5,
```

gives

```text
1 + z_mr = 0.315 / 9.2e-5 = 3423.913...,
z_mr     = 3422.913...
```

The CMB-inferred comparator `z_mr = 3387 +/- 21` differs by about `+1.1%`
or about `1.7 sigma` on this simple readout.

This comparison should be read as a consistency check after the density
fractions are supplied. The theorem does not derive `Omega_m,0`, `Omega_r,0`,
`T_CMB`, the sound horizon, or photon-decoupling physics.

## Relation To Late-Time FRW Kinematics

Together with the late-time FRW kinematic theorem, the structural redshift
sequence is:

| Event | Structural identity | Comparator readout |
| --- | --- | ---: |
| matter-radiation equality | `1 + z_mr = Omega_m,0/Omega_r,0` | `z_mr = 3423` |
| photon decoupling | atomic/recombination physics, not retained here | `z_rec ~ 1090` |
| acceleration onset | late-time K2 quartic / `(2 Omega_Lambda/Omega_m)^(1/3)` limit | `z_* ~ 0.632` |
| matter-Lambda equality | `1 + z_mLambda = (Omega_Lambda/Omega_m)^(1/3)` | `z_mLambda ~ 0.296` |

Thus the current package now has named structural identities for both the
early matter-radiation transition and the late matter-Lambda/acceleration
transitions. The early identity is not gated by the open `H_inf/H_0` bridge;
its numerical readout is instead gated by `Omega_m,0` and `Omega_r,0`.

## Radiation-Density Check

For the standard thermal history,

```text
Omega_r,0 = Omega_gamma,0 [1 + N_eff (7/8) (4/11)^(4/3)].
```

With `T_CMB ~= 2.725 K`, `h ~= 0.674`, and `N_eff = 3.046`, this gives
`Omega_r,0 ~= 9.2e-5`, matching the value used above. The framework's retained
three-generation matter structure is consistent with three active neutrino
flavours; that active-count support is packaged separately in
`N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md`. This note does not
derive the standard thermal-history correction, the observed CMB temperature,
or the photon-density conversion.

## Scope

This note claims:

- the exact FRW/EOS identity `1 + z_mr = Omega_m,0 / Omega_r,0`;
- independence from `H_0`, `Omega_Lambda,0`, and `alpha_s(v)`;
- a standard comparator readout `z_mr ~= 3423` after supplying
  `Omega_m,0 = 0.315` and `Omega_r,0 = 9.2e-5`;
- consistency with the retained three-generation matter structure through the
  standard `N_eff ~= 3` radiation-density input.

This note does not claim:

- a native-axiom derivation of `Omega_m,0`;
- a native-axiom derivation of `Omega_r,0`, `T_CMB`, or the standard
  `N_eff` thermal correction;
- a prediction of photon decoupling `z_rec`;
- a sound-horizon, BAO, CMB acoustic-peak, or BBN calculation;
- a promoted numerical cosmology package.

## Reproduction

```bash
python3 scripts/frontier_matter_radiation_equality_structural_identity.py
```

Expected result:

```text
TOTAL: PASS=14, FAIL=0
```

The runner uses the Python standard library only.

## Cross-References

- [`COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md`](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md)
  - late-time matter/Lambda kinematic companion.
- [`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`](COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md)
  - bounded matter-density cascade context.
- [`R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`](R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)
  - exact support identity inside the bounded DM/cosmology cascade.
- [`N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md`](N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md)
  - active-neutrino-count support for the standard `N_eff = 3.046` radiation input.
- [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
  - retained `w=-1` late-time companion.
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  - retained three-generation matter structure.
