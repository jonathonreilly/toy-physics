# Koide `C_3` Singlet-Extension Reduction Theorem

**Date:** 2026-04-20  
**Status:** exact reduction of the open `4 x 4` singlet/baryon route to one scalar Schur law on the charged-lepton selected slice  
**Runner:** `scripts/frontier_koide_c3_singlet_extension_reduction_theorem.py`

## Question

The remaining-open-imports register still left alive one possible route for
closing Koide `Q = 2/3` from the selected-slice scalar potential:

> perhaps a `4 x 4` `(hw = 1 + singlet/baryon)` microscopic extension adds a
> retained correction that moves the selected-slice minimum from
> `m_V ~= -0.433` to the physical point `m_* ~= -1.16044`.

Can that route be stated more sharply than “some non-uniform `4 x 4`
correction might exist”?

## Bottom line

Yes.

Any `C_3[111]`-equivariant singlet extension of the selected slice collapses,
after Schur reduction, to **one scalar law** on the trivial Fourier mode:

```text
K_eff(m) = K_sel(m) - lambda(m) J,
J = 11^T = 3 P_+.
```

So the `4 x 4` route does **not** produce an arbitrary new `m`-dependent matrix
law. It only adds one scalar Schur correction `lambda(m)` multiplying the
trivial-mode projector.

For the fixed-coupling subclass (`lambda(m) = lambda` constant), the extended
selected-slice potential is still exactly cubic:

```text
V_lambda(m)
  = V0(lambda)
  + [ 9 lambda^2 / 2 - 3 lambda - 4 sqrt(2)/3 + 35/24 + 2 sqrt(6)/3 ] m
  + 3(1-lambda) m^2 / 2
  + m^3 / 6.
```

Demanding that the branch-local physical selected point

```text
m_* = -1.160443440065
```

be the positive-branch minimum gives exactly two constant solutions:

```text
lambda_- = -0.652587605113,
lambda_+ =  0.5456253117.
```

If the singlet channel is positive (so `lambda = |beta|^2 / eps >= 0`), only
the second is physical. Therefore the fixed-coupling `4 x 4` route is reduced
to **one exact positive number**

```text
lambda_* ~= 0.5456253117
```

not to a vague search over non-uniform microscopic corrections.

## Input stack

This note sharpens:

1. [KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md](./KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md)
2. [KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md](./KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
3. [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
4. [KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md](./KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md)

## Theorem 1: every `C_3`-equivariant singlet coupling is trivial-mode only

Let `C` be the retained `3 x 3` cycle on the charged-lepton triplet and let
`c in C^3` be the coupling from a singlet state into that triplet. If the
singlet is `C_3`-trivial and the full `4 x 4` parent is `C_3`-equivariant, then

```text
C c = c.
```

Writing `c = (c1, c2, c3)^T`, this means

```text
c3 - c1 = c1 - c2 = c2 - c3 = 0,
```

so

```text
c = beta (1,1,1)^T
```

for one complex scalar `beta`.

Hence the singlet couples only through the trivial Fourier direction. The
matrix

```text
J = 11^T
```

satisfies

```text
J^2 = 3J,
CJ = JC = J,
```

so `P_+ = J/3` is exactly the trivial-character projector.

## Corollary 1: Schur reduction gives one scalar correction

Write the selected slice as

```text
K_sel(m) = K_frozen + m T_m
```

with the exact selected-slice direction

```text
T_m =
[1 0 0]
[0 0 1]
[0 1 0].
```

Consider a `4 x 4` singlet extension

```text
K_tilde(m) =
[ eps     c^dagger ]
[ c       K_sel(m) ]
```

with `c = beta (1,1,1)^T`. If `eps != 0`, the Schur complement on the triplet is

```text
K_eff(m)
  = K_sel(m) - c eps^(-1) c^dagger
  = K_sel(m) - lambda J,
lambda = |beta|^2 / eps.
```

So the entire `4 x 4` route reduces to one scalar `lambda`. Nothing else
survives the equivariant reduction.

## Corollary 2: the `m`-direction is unchanged

For any two selected-slice points `m1`, `m2`,

```text
K_eff(m2) - K_eff(m1) = (m2 - m1) T_m.
```

So the singlet extension does **not** create a new matrix-valued
`m`-dependence. It only renormalizes the frozen bank by `-lambda J`.

If one allows the microscopic singlet couplings themselves to vary with `m`,
the whole route is still only one scalar law

```text
lambda = lambda(m).
```

That is the strongest honest reduction of the `4 x 4` route.

## Theorem 2: fixed singlet couplings give an exact one-parameter cubic potential

For the fixed-coupling subclass (`lambda` constant), define

```text
K_lambda(m) = K_sel(m) - lambda J.
```

Then the same selected-slice scalar action

```text
V_lambda(m) = Tr(K_lambda^2)/2 + Tr(K_lambda^3)/6
```

expands exactly as

```text
V_lambda(m)
  = V0(lambda)
  + [ 9 lambda^2 / 2 - 3 lambda - 4 sqrt(2)/3 + 35/24 + 2 sqrt(6)/3 ] m
  + 3(1-lambda) m^2 / 2
  + m^3 / 6.
```

Hence

```text
dV_lambda/dm
  = 9 lambda^2 / 2
  - 3 (m+1) lambda
  + m^2 / 2
  + 3m
  - 4 sqrt(2)/3
  + 35/24
  + 2 sqrt(6)/3.
```

The singlet route therefore does **not** create a new functional class. It only
adds one parameter to the same cubic selected-slice potential.

## Corollary 3: the branch-local physical point fixes one unique positive constant

On the current exact branch-local Koide route, the actual selected-line phase
bridge gives the physical first-branch point

```text
delta = 2/9  ->  m_* = -1.160443440065.
```

Solving

```text
(dV_lambda/dm)(m_*) = 0
```

gives the exact pair

```text
lambda_±(m_*)
  = m_*/3 + 1/3
    ± sqrt(-144 m_* - 48 sqrt(6) - 69 + 96 sqrt(2)) / 18.
```

Numerically,

```text
lambda_- = -0.652587605113,
lambda_+ =  0.5456253117.
```

If the singlet energy is positive, then `lambda = |beta|^2 / eps >= 0`, so the
negative root is excluded. The fixed-coupling route is therefore reduced to
one exact positive parameter:

```text
lambda_* ~= 0.5456253117
```

At this value, the companion critical point lies below the positivity threshold
`m_pos`, so `m_*` is the **only** stationary point on the physical first
branch.

## Why this matters

This is the right update to the `Q = 2/3` open-import story:

- the `4 x 4` singlet/baryon route is not an open-ended matrix search,
- it is not a hidden high-dimensional selector family,
- and it is not “some generic non-uniform correction.”

It is exactly:

```text
derive the singlet Schur scalar lambda(m),
or in the fixed-coupling subclass derive lambda_* ~= 0.5456253117.
```

That is much smaller and more honest than the previous wording.

## What this does and does not close

### Established here

1. every `C_3`-equivariant singlet extension reduces to one scalar Schur law on
   `J = 3 P_+`;
2. fixed singlet couplings preserve a cubic selected-slice potential with exact
   `lambda`-dependent coefficients;
3. the branch-local physical point requires one unique positive constant
   `lambda_*`.

### Not established here

- no derivation of `lambda(m)` or `lambda_*` from the retained microscopic
  lattice action;
- no claim that the fixed-coupling subclass is the correct physical subclass;
- no promotion of Koide `Q = 2/3` to retained derivation on current main.

So this note **shrinks** the remaining import. It does not remove it.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_c3_singlet_extension_reduction_theorem.py
```
