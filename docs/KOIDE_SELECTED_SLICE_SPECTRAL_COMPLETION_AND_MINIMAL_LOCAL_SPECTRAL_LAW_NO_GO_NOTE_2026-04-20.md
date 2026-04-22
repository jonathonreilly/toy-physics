# Koide Selected-Slice Spectral Completion and Minimal Local Spectral-Law No-Go

**Date:** 2026-04-20  
**Status:** exact spectral-completion theorem plus exact low-complexity no-go
on the canonical selected-slice `2 x 2` carrier  
**Runner:** `scripts/frontier_koide_selected_slice_spectral_completion_and_minimal_local_spectral_law_no_go.py`

## Question

After the frozen-bank decomposition, the charged-lepton selected slice is
already reduced to one real coordinate

```text
K_Z3^sel(m) = K_frozen + m T_m^(K).
```

That still leaves a live scientific possibility:

> perhaps the canonical intrinsic spectral data of the selected-slice
> `2 x 2` `Z_3` doublet block already carry a simple exact selector law for the
> physical point.

This note tests that idea directly.

## Bottom line

It fails cleanly.

The canonical selected-slice `2 x 2` block is spectrally complete, but its
spectral data are sign-blind. Writing

```text
x = m - 4 sqrt(2) / 9 = Re K12,
```

the intrinsic spectral scalars satisfy

```text
Tr(K2)    = const,
det(K2)   = D_c - x^2,
Tr(K2^2)  = Q_c + 2 x^2,
Gap(K2)^2 = G_c^2 + 4 x^2.
```

So after the exact completion, the whole canonical spectral carrier still
collapses to one scalar:

```text
x^2.
```

That has two consequences:

1. the spectral carrier cannot distinguish the two reflected points
   `m` and `8 sqrt(2)/9 - m`;
2. on the physical first branch, where `x < 0` everywhere, the raw spectral
   scalars are strictly monotone and the natural low-complexity selector
   classes are ruled out.

So this route is not a hidden closure of Koide `Q = 2/3`. It is another exact
reparameterization of the same one-scalar gap.

## 1. Exact spectral completion of the selected `2 x 2` block

On the exact selected slice `delta = q_+ = sqrt(6)/3`, the `2 x 2` doublet
block is

```text
K2(m)
  = [ A                x - i sqrt(2)/3 ]
    [ x + i sqrt(2)/3  B               ]
```

with

```text
A = -sqrt(6)/3 - sqrt(3)/6 + 2 sqrt(2)/9,
B = -sqrt(6)/3 + sqrt(3)/6 + 2 sqrt(2)/9,
x = m - 4 sqrt(2)/9.
```

The runner proves the canonical spectral formulas exactly:

```text
Tr(K2)    = -2 sqrt(6)/3 + 4 sqrt(2)/9,
det(K2)   = -x^2 + 149/324 - 8 sqrt(3)/27,
Tr(K2^2)  =  2 x^2 + 347/162 - 16 sqrt(3)/27,
Gap(K2)^2 =  4 x^2 + 11/9.
```

and verifies the standard `2 x 2` identities

```text
Tr(K2^2)  = Tr(K2)^2 - 2 det(K2),
Gap(K2)^2 = Tr(K2)^2 - 4 det(K2).
```

So once the trace is known, the whole spectral carrier is equivalent to any
one of the remaining scalars above. There is no hidden second spectral degree
of freedom.

## 2. Reflection symmetry and sign-blindness

Because the spectral data depend only on `x^2`, they are exactly invariant
under the reflection

```text
m -> 8 sqrt(2)/9 - m
```

which flips `x -> -x`.

Equivalently, after subtracting the center values

```text
D_c = det(K2)|_(x=0),
Q_c = Tr(K2^2)|_(x=0),
G_c^2 = Gap(K2)^2|_(x=0),
```

the completed spectral coordinates satisfy

```text
D_c - det(K2)      = x^2,
Tr(K2^2) - Q_c     = 2 x^2,
Gap(K2)^2 - G_c^2 = 4 x^2.
```

So the completed spectral carrier is exact, but it is not an oriented point on
the selected line. It is only the sign-blind coordinate `x^2`.

## 3. Physical-branch consequence

The physical first branch runs from the positivity threshold `m_pos` to the
unphased endpoint `m_0`. The runner checks that the whole branch lies on the
same side of the reflection center:

```text
m_pos < m < m_0 < 4 sqrt(2)/9.
```

Hence

```text
x < 0
```

everywhere on the physical branch, so `x^2` is strictly decreasing as `m`
increases.

Therefore the raw spectral scalars are strictly monotone:

```text
det(K2)   increases,
Tr(K2^2)  decreases,
Gap(K2)^2 decreases.
```

The current physical point is interior in all three orderings. No single raw
completed spectral scalar selects it against the natural branch landmarks

```text
m_pos,  m_phys,  m_DA,  m_V,  m_0.
```

## 4. Minimal local spectral-law no-go

The theorem-grade no-go is stronger than “no single scalar worked.”

### 4.1 Affine laws

Any affine law in the completed raw spectral coordinates has the form

```text
L = alpha det(K2) + beta Tr(K2^2) + gamma Gap(K2)^2.
```

Since each coordinate is affine in `x^2`, the derivative is

```text
dL/dx = 2 x (-alpha + 2 beta + 4 gamma).
```

So on the physical branch:

- either `-alpha + 2 beta + 4 gamma = 0`, in which case `L` is constant;
- or `dL/dx` never vanishes, because `x != 0` on the branch.

Hence no nonconstant affine spectral law can be an exact interior selector on
the physical branch.

### 4.2 Coefficient-free monomial laws

Using the positive shifted spectral coordinates

```text
u1 = D_c - det(K2)      = x^2,
u2 = Tr(K2^2) - Q_c     = 2 x^2,
u3 = Gap(K2)^2 - G_c^2 = 4 x^2,
```

any coefficient-free monomial is

```text
u1^a u2^b u3^c = const * x^(2(a+b+c)).
```

So coefficient-free monomial spectral laws are again constant or strictly
monotone on the branch. They also cannot select an interior point.

### 4.3 Scale-normalized laws

Normalizing by `Tr(K2)` does not help, because `Tr(K2)` is already constant on
the whole selected slice. Scale-normalized spectral laws therefore reduce to
the same `x^2` carrier.

## 5. Scientific consequence

This closes another apparent Koide route cleanly.

The selected-slice `2 x 2` block does have an exact canonical intrinsic
spectral completion. But that completion:

- is sign-blind under `x -> -x`,
- collapses to one scalar `x^2`,
- and supports no natural exact low-complexity interior selector on the
  physical branch.

So the remaining Koide object is still not “find a spectral observable on the
selected slice.” That possibility is exhausted.

The real remaining object is still the same one named elsewhere:

```text
derive the microscopic oriented scalar m,
equivalently x = Re K12,
equivalently the selected-line scalar bridge kappa
from retained framework physics.
```

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_selected_slice_spectral_completion_and_minimal_local_spectral_law_no_go.py
```
