# Koide Q Cyclic-Compression Scalar-Blind No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_cyclic_compression_scalar_blind_no_go.py`  
**Status:** executable no-go for deriving the charged-lepton selector scalar
from exact `dW_e^H` cyclic compression alone

## Theorem Attempt

The exact `dW_e^H` compression theorem is one of the strongest positive
surfaces left in the `Q` lane.  It says that the generic Hermitian
charged-lepton source packet compresses canonically to three cyclic response
channels:

```text
(r0, r1, r2).
```

The attempted theorem in this cycle was:

> exact cyclic compression plus retained `C3` covariance and scale
> normalization forces the remaining microscopic selector scalar, hence
> supplies the missing source/radius law.

The audit rejects that theorem.  The compression is exact and useful, but it
does not derive the remaining scalar.

## Route Ranking

1. **Cyclic-compression source scalar:** strongest fresh `Q` route after the
   semigroup and delta endpoint audits, because it attacks the source law
   directly at the compressed response level.
2. **What if compression already deletes the missing primitive?** inversion of
   the previous assumption that a source law must be added after compression.
3. **Scale-normalized response ratio:** test whether fixing the denominator
   `d_sum - x_sum` forces the signed cyclic `Y` sum.
4. **Quadratic `C3` source law:** ask whether covariance fixes the coefficient
   ratio in a response-level scalar action.
5. **Delta endpoint bridge:** already audited this cycle; leaves endpoint
   selection free.

## Exact Compression

For a generic Hermitian source packet with diagonal, real off-diagonal, and
imaginary off-diagonal coefficients, the cyclic projector keeps exactly:

```text
d_sum = d1 + d2 + d3,
x_sum = x12 + x23 + x13,
y_sum = y12 + y23 - y13.
```

The retained cyclic basis responses are:

```text
r0 = d_sum,
r1 = 2 x_sum,
r2 = 2 y_sum.
```

So the Koide-relevant source data is indeed compressed from nine real
Hermitian channels to three cyclic channels.

## Obstruction

The remaining selected-line scalar is the exact ratio

```text
rho = sqrt(3) * r2 / (2 r0 - r1)
    = sqrt(3) * y_sum / (d_sum - x_sum).
```

Scale normalization can set

```text
d_sum - x_sum = 1,
```

but then

```text
rho = sqrt(3) * y_sum.
```

The signed cyclic `Y` sum is still free.

The runner exhibits the exact counterfamily:

```text
y_sum = 0   -> rho = 0,
y_sum = 1/3 -> rho = sqrt(3)/3,
y_sum = 2/3 -> rho = 2 sqrt(3)/3.
```

All three preserve the exact compressed-source form.

## Covariance Review

A generic `C3`-allowed quadratic source law at this reduced level still has a
free coefficient ratio:

```text
alpha (2 d_sum - 2 x_sum)^2 + beta (2 y_sum)^2.
```

No retained `C3` equation fixes `beta/alpha`.  Choosing that coefficient ratio
would be another expression of the missing source/radius law.

## Hostile Review

This no-go does **not** use:

- `K_TL = 0`;
- `K = 0`;
- `P_Q = 1/2`;
- `Q = 2/3`;
- `delta = 2/9`;
- PDG masses;
- the observational `H_*` pin.

The result is strictly symbolic source-channel algebra.  It does not demote
the cyclic-compression theorem; it prevents over-promoting that theorem as a
Koide closeout.

## Executable Result

```text
PASSED: 11/11

KOIDE_Q_CYCLIC_COMPRESSION_SCALAR_BLIND_NO_GO=TRUE
Q_CYCLIC_COMPRESSION_CLOSES_Q=FALSE
RESIDUAL_SCALAR=rho=sqrt(3)*r2/(2*r0-r1)
```

## Consequence

The `Q` bridge is again reduced to a single scalar, now on the compressed
source-response carrier:

```text
derive rho from retained charged-lepton source grammar.
```

Without such a retained source grammar, cyclic compression remains strong
support but not a Nature-grade closure.
