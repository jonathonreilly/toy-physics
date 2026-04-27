# R_base = 31/9 Group-Theory Derivation Theorem

**Date:** 2026-04-24
**Status:** proposed_retained exact support identity on the bounded dark-matter /
cosmology cascade surface. This note packages the exact rational identity
`R_base = 31/9` that was previously inline in
[`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`](COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md)
and [`OMEGA_LAMBDA_DERIVATION_NOTE.md`](OMEGA_LAMBDA_DERIVATION_NOTE.md).
It does not promote the full dark-matter-to-baryon ratio or the numerical
`Omega_Lambda` chain to retained closure.

**Primary runner:** `scripts/frontier_r_base_group_theory_derivation.py`

## Statement

On the retained graph-first `SU(3)` gauge structure with `N_c = 3`, the
retained electroweak `SU(2)_L` structure, and the admitted
Georgi-Glashow/GUT hypercharge normalization factor `3/5`, the structural
base factor used by the bounded dark-matter/cosmology cascade is

```text
R_base = (3/5) * [C_2(3) * dim(adj_3) + C_2(2) * dim(adj_2)]
                 / [C_2(2) * dim(adj_2)]
       = 31/9.
```

The exact inputs are:

| Input | Value | Status |
|---|---:|---|
| `C_2(SU(3)_fund)` | `4/3` | textbook Lie-algebra identity at `N = 3` |
| `C_2(SU(2)_fund)` | `3/4` | textbook Lie-algebra identity at `N = 2` |
| `dim(adj SU(3))` | `8` | `N^2 - 1` at `N = 3` |
| `dim(adj SU(2))` | `3` | `N^2 - 1` at `N = 2` |
| GUT normalization | `3/5` | retained/admitted from the hypercharge-identification lane |

No observed cosmological value enters the derivation of `R_base`.

## Exact Derivation

For `SU(N)` in the fundamental representation,

```text
C_2(N) = (N^2 - 1) / (2N),        dim(adj_N) = N^2 - 1.
```

Therefore

```text
C_2(3) = 4/3,          dim(adj_3) = 8,
C_2(2) = 3/4,          dim(adj_2) = 3.
```

The numerator and denominator are

```text
N = C_2(3) * dim(adj_3) + C_2(2) * dim(adj_2)
  = (4/3) * 8 + (3/4) * 3
  = 32/3 + 9/4
  = 155/12,

D = C_2(2) * dim(adj_2)
  = (3/4) * 3
  = 9/4.
```

Thus

```text
N/D = (155/12) / (9/4) = 155/27,
R_base = (3/5) * (155/27) = 465/135 = 31/9.
```

The last reduction uses `gcd(465, 135) = 15`.

## Equivalent Forms

The same identity may be written as

```text
R_base = 31/9
       = (3/5) * (155/27)
       = (3/5) * (1 + 128/27)
       = 3/5 + 128/45.
```

The `1 + 128/27` form separates the weak-sector denominator contribution
from the `SU(3)` over `SU(2)` Casimir-adjoint contribution.

## Scope

This theorem retains only the exact algebraic base factor. The following
remain separate:

- the native-axiom derivation of the GUT normalization factor `3/5`;
- the Sommerfeld factor `S_vis / S_dark`, which remains bounded through
  `alpha_GUT`;
- the full `Omega_DM / Omega_b` numerical ratio;
- the downstream `Omega_Lambda`, `Omega_m`, and late-time cosmology numerics;
- any uniqueness claim for dark-sector representations.

The result is therefore useful because it removes one stale inline assertion
from the cosmology cascade and replaces it with a named exact identity. It is
not a closure of the matter/cosmology bridge.

## Reproduction

```bash
python3 scripts/frontier_r_base_group_theory_derivation.py
```

The runner verifies the Casimir values, adjoint dimensions, exact numerator,
denominator, lowest-terms reduction, equivalent decompositions, and status
boundary checks using exact rational arithmetic.

## Cross-References

- [`COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md`](COSMOLOGY_FROM_MASS_SPECTRUM_NOTE.md)
- [`OMEGA_LAMBDA_DERIVATION_NOTE.md`](OMEGA_LAMBDA_DERIVATION_NOTE.md)
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md)
