# Top-Yukawa Source-to-Higgs Legendre/SSB Bridge Note

**Date:** 2026-05-01  
**Status:** exact subderivation / open bridge; no retention proposal  
**Runner:** `scripts/frontier_yt_source_higgs_legendre_ssb_bridge.py`  
**Certificate:** `outputs/yt_source_higgs_legendre_ssb_bridge_2026-05-01.json`

## Purpose

The Ward repair audit identified source/HS normalization and SSB VEV division
as one of the open physical-readout bridges.  This note isolates the part that
can be closed without new physics: once a canonical Higgs doublet coefficient
is available, the SSB readout does not add an extra hidden factor.

It does not derive the source-to-canonical-Higgs normalization.  That remains
the next hard residual.

## Setup

Let the tree-level scalar/trilinear coefficient be

```text
c = 1/sqrt(N_c N_iso) = 1/sqrt(6).
```

For a canonical Higgs doublet in unitary gauge,

```text
H = (0, (v + h)/sqrt(2)).
```

The doublet Yukawa term gives

```text
L_Y = - y (v + h)/sqrt(2) * tbar t.
```

Therefore

```text
m = y v / sqrt(2),
y = sqrt(2) m / v,
g_{htt} = y / sqrt(2) = m / v.
```

The SSB convention changes the mass and physical `h t t` vertex readout, but
it does not change the doublet Yukawa coefficient `y`.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_source_higgs_legendre_ssb_bridge.py
# SUMMARY: PASS=7 FAIL=0
```

The runner checks three arbitrary VEV values and verifies that
`sqrt(2) m / v` always returns the same doublet coefficient.  With the
conditional unit source normalization `kappa_H = 1`, the coefficient remains

```text
y = 0.408248290463863 = 1/sqrt(6).
```

## What This Closes

This closes only the SSB bookkeeping substep:

```text
canonical doublet coefficient y -> mass m -> sqrt(2) m/v = y
```

No additional factor is introduced by VEV division once the canonical Higgs
doublet coefficient is known.

## What Remains Open

The source-to-canonical-Higgs normalization is still not derived.  If the scalar
source creates a canonical Higgs field with normalization `kappa_H`, then the
readout is

```text
y_readout = c * kappa_H.
```

SSB algebra cannot determine `kappa_H`.  That requires an independent theorem
from the Legendre transform/two-point residue of the scalar source.

Remaining open imports:

| Open import | Role |
|---|---|
| source-to-canonical-Higgs normalization | determines `kappa_H` |
| scalar carrier map | proves the source field is the physical Higgs fluctuation |
| chirality and species selector | maps scalar bilinear to `Q_L H q_R` |
| LSZ residue | gives the physical external scalar leg |

## Non-Claims

- This note does not identify a scalar source with `H_unit` by definition.
- This note does not derive `kappa_H`.
- This note does not use observed top mass or observed Yukawa values.
- This note does not promote the Ward theorem or PR #230 to retained closure.
