# Spectral-Dimension / CDT Quantitative Audit

**Status:** bounded-retained, but only in a narrow proxy sense

## Scope

I audited the current spectral / continuum scripts in this repo:

- [`scripts/frontier_3d_continuum_spectrum.py`](/Users/jonreilly/Projects/Physics/scripts/frontier_3d_continuum_spectrum.py)
- [`scripts/frontier_spectral_on_lattice.py`](/Users/jonreilly/Projects/Physics/scripts/frontier_spectral_on_lattice.py)
- [`scripts/frontier_spectral_on_lattice_fluxnorm.py`](/Users/jonreilly/Projects/Physics/scripts/frontier_spectral_on_lattice_fluxnorm.py)

These scripts are the closest current proxy for the CDT / spectral-dimension lane in this tree.

## What survives

The strongest honest quantitative statement is not a full CDT match. It is:

- the first nonzero spectral gap in the continuum-spectrum proxy is stable under refinement:
  - `E_2 / E_1 = 1.0032` at `h = 1.0`
  - `E_2 / E_1 = 1.0000` at `h = 0.5`
- the higher extracted ratios move upward with refinement, but they still do not approach the square-box mode ratios in a quantitatively complete way:
  - `E_4 / E_1 = 1.2068 -> 1.8814`
  - `E_6 / E_1 = 1.3058 -> 1.9275`
  - the box predictions remain much larger (`2.5`, `4.0`, `5.0`, ...)
- spectral averaging on the retained ordered lattice is not a stable CDT-style quantitative match:
  - raw coherent broad spectra are all `AWAY`
  - flux-normalized broad spectra become all `TOWARD`
  - the sign therefore depends on normalization, so the result is not a robust universal claim

## Retainable claim

The retainable claim is:

- **UV -> IR flow exists**
- **the lowest spectral gap shows a stable degeneracy-like ratio near `1.0` under refinement**
- **there is no current retained quantitative CDT match beyond that**

That is the honest endpoint of the current scripts. The lane does not yet support a stronger statement such as a full CDT-style quantitative dimensional match.

## Bottom Line

If this note is used in the retained docs, it should be read as a **bounded negative / narrow positive**:

- positive: a stable first-gap degeneracy proxy under refinement
- negative: no robust quantitative match to CDT beyond the existence of spectral flow
