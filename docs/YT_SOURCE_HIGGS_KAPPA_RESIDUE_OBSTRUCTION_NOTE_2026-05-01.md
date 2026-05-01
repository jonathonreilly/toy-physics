# Top-Yukawa Source-Higgs Kappa Residue Obstruction Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / open bridge; no retention proposal  
**Runner:** `scripts/frontier_yt_source_higgs_kappa_residue_obstruction.py`  
**Certificate:** `outputs/yt_source_higgs_kappa_residue_obstruction_2026-05-01.json`

## Purpose

The source/SSB bridge reduction showed that EWSB bookkeeping does not add an
extra factor once a canonical Higgs doublet coefficient is known.  The remaining
normalization is `kappa_H`: the map from the source-normalized scalar
coefficient to the canonical Higgs-doublet coefficient.

This note proves that `kappa_H = 1` is not selected by group counts and SSB
algebra alone.  A scalar two-point residue or equivalent LSZ theorem is
required.

## Setup

The source-normalized scalar coefficient is fixed by the familiar count:

```text
c_source = 1/sqrt(N_c N_iso) = 1/sqrt(6).
```

But the physical doublet coefficient depends on the unresolved source-to-field
normalization:

```text
y_doublet = c_source * kappa_H.
```

The current Ward repair has not derived `kappa_H`.  It is exactly the scalar
source/canonical-field normalization gap.

## Countermodel Check

The runner evaluates several `kappa_H` values:

| `kappa_H` | `y_doublet` |
|---:|---:|
| `0.5` | `0.204124145231932` |
| `sqrt(8/9)` | `0.384900179459751` |
| `1` | `0.408248290463863` |
| `2` | `0.816496580927726` |

All of these retain the same `N_c = 3`, `N_iso = 2`, and source coefficient
`1/sqrt(6)`.  All satisfy the SSB identity

```text
sqrt(2) m / v = y_doublet.
```

Therefore group-count arithmetic plus SSB bookkeeping cannot select
`kappa_H = 1`.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_source_higgs_kappa_residue_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```

## Consequence

The Ward physical-readout repair is now narrowed:

```text
derive scalar source two-point residue / LSZ normalization
        -> determine kappa_H
        -> then the tree-level coefficient can be read as a physical doublet y
```

Without that residue theorem, setting `kappa_H = 1` is a normalization choice,
not a derivation.

## Non-Claims

- This note does not derive `kappa_H = 1`.
- This note does not identify the source scalar with `H_unit` by definition.
- This note does not use observed top mass or observed Yukawa values.
- This note does not promote the Ward theorem or PR #230 to retained closure.
