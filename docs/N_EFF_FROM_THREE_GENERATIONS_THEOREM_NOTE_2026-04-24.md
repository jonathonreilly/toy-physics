# N_eff From Retained Three Generations

**Date:** 2026-04-24

**Status:** proposed_retained/admitted structural support theorem on the cosmology
surface. The retained framework fixes the number of light active neutrino
flavours to three. The standard cosmology correction from non-instantaneous
decoupling and finite-temperature QED, and the photon-temperature input used to
turn this into `Omega_r,0`, are not derived here.

**Primary runner:** `scripts/frontier_n_eff_from_three_generations.py`

## Statement

On the retained matter-content surface,

```text
N_active = N_generations * N(nu_L per generation) = 3 * 1 = 3.
```

With standard thermal-history bookkeeping this gives the usual Standard Model
effective radiation count

```text
N_eff = 3 + Delta_N_eff,std = 3 + 0.046 = 3.046.
```

The retained heavy right-handed neutrino slots do not add relativistic
radiation at BBN, matter-radiation equality, or recombination temperatures on
the retained Majorana scale. Thus the framework-side structural contribution
is the active count `3`; the `0.046` correction and the conversion into
`Omega_r,0` are standard cosmology inputs.

## Inputs

| Ingredient | Status |
| --- | --- |
| three retained generations | retained in `THREE_GENERATION_STRUCTURE_NOTE.md` |
| one `nu_L` in each retained lepton doublet | retained in `ONE_GENERATION_MATTER_CLOSURE_NOTE.md` |
| one neutral `nu_R` slot per generation | retained one-generation completion; also witnessed by the B-L anomaly-freedom packet if B-L is gauged |
| retained lightest right-handed Majorana scale `M_1 ~= 5.32e10 GeV` | retained neutrino atmospheric-scale / staircase package |
| standard correction `Delta_N_eff,std = 0.046` | external standard cosmology |
| `T_CMB`, `h`, and `Omega_gamma,0` for `Omega_r,0` | observational/standard cosmology inputs |

## Derivation

The retained three-generation note fixes three physical generation sectors.
The retained one-generation matter closure has one left-handed neutrino in the
lepton doublet:

```text
L_L = (nu_L, e_L).
```

Therefore the retained light active neutrino count is

```text
N_active = 3.
```

The retained one-generation completion also contains neutral right-handed
singlets `nu_R`. These are not extra light active radiation species. On the
retained Majorana staircase,

```text
M_1 ~= 5.32e10 GeV.
```

Against representative cosmological temperatures,

```text
M_1 / T_BBN       ~= 5.3e13      for T_BBN ~= 1 MeV,
M_1 / T_eq        ~= 6.6e19      for T_gamma(eq) ~= 0.8 eV,
M_1 / T_today     ~= 2.3e23      for T_CMB ~= 2.725 K.
```

An equilibrium relativistic contribution from the retained `nu_R` sector is
therefore absent at the relevant BBN/CMB-era readout temperatures. This does
not derive the full reheating or decoupling history; it only records that the
retained heavy singlets are not light radiation degrees of freedom.

The standard cosmology correction then gives

```text
N_eff = N_active + Delta_N_eff,std
      = 3 + 0.046
      = 3.046.
```

## Radiation-Density Cross-Check

The standard radiation-density conversion is

```text
Omega_r,0 = Omega_gamma,0
            [1 + N_eff (7/8) (4/11)^(4/3)].
```

Using `T_CMB ~= 2.725 K`, `h ~= 0.674`, and `N_eff = 3.046` gives

```text
Omega_r,0 ~= 9.20e-5.
```

That is the same radiation-density input used by the matter-radiation equality
identity:

```text
1 + z_mr = Omega_m,0 / Omega_r,0.
```

With supplied `Omega_m,0 = 0.315`, this gives the same comparator readout

```text
z_mr ~= 3423.
```

This is a consistency chain, not a native derivation of `Omega_m,0`,
`Omega_r,0`, or `T_CMB`.

## Observational Comparator

The standard readout

```text
N_eff = 3.046
```

is consistent with the listed Planck-2018 comparator

```text
N_eff = 2.99 +/- 0.17.
```

The comparison is post-derivation. No observed `N_eff` value is used to obtain
the retained active-neutrino count.

## Scope

This note claims:

- the retained matter package fixes three light active neutrino flavours;
- retained heavy `nu_R` slots are not light relativistic radiation at
  BBN/CMB-era temperatures;
- the standard correction turns the retained active count into
  `N_eff = 3.046`;
- this supports the `Omega_r,0 ~= 9.2e-5` input used in the
  matter-radiation equality consistency check.

This note does not claim:

- a native-axiom derivation of the standard `0.046` correction;
- a native-axiom derivation of `T_CMB`, `h`, or `Omega_gamma,0`;
- a full reheating, neutrino-decoupling, BBN, or sound-horizon calculation;
- exclusion of partly thermalized or nonstandard dark-radiation sectors by
  theorem alone;
- a new absolute neutrino-mass prediction beyond the retained neutrino package.

## Reproduction

```bash
python3 scripts/frontier_n_eff_from_three_generations.py
```

Expected result:

```text
TOTAL: PASS=21, FAIL=0
```

The runner uses the Python standard library only.

## Cross-References

- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  - retained three-generation matter structure.
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  - retained one-generation matter content.
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)
  - independent anomaly witness for the neutral `nu_R` slot when B-L is gauged.
- [`NEUTRINO_MASS_DERIVED_NOTE.md`](NEUTRINO_MASS_DERIVED_NOTE.md)
  - retained Majorana scale and atmospheric neutrino package.
- `MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` (downstream consumer in same lane; cross-reference only — not a one-hop dep of this note)
  - equality-redshift identity using the resulting standard radiation density.
