# Koide Higgs-Dressed Omitted-Channel Self-Energy Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide, constructive transport avenue  
**Status:** exact Schur/self-energy sharpening on top of the transport
susceptibility theorem. This still does not derive Koide from retained
framework data alone, but it localizes the entire local transport correction to
one omitted-channel self-energy.  
**Runner:** `scripts/frontier_koide_higgs_dressed_omitted_channel_self_energy_theorem.py`

## Question

The transport susceptibility theorem reduced the local gap to one small
backreaction term in the reached principal `2 x 2` block. The natural next
question is:

```text
does that backreaction come from generic reached-sector dynamics, or from one
more specific microscopic source?
```

This note answers that.

## Bottom line

It comes from one omitted channel.

Let the retained missing-axis Hermitian `H_*` be partitioned as:

```text
H_* =
  [ m_0   g† ]
  [ g    H_r ],
```

where:

- `m_0` is the omitted `T2[011]` scalar channel,
- `H_r` is the reached `2 x 2` block on `(T2[110], T2[101])`,
- `g` is the coupling vector from the omitted channel to the reached sector.

Then the exact reached transport block is not merely a principal block of the
full resolvent in some opaque sense. It is exactly the Schur-complement
resolvent

```text
B_full(lambda)
  = (lambda I - H_r - Sigma_omit(lambda))^(-1),
Sigma_omit(lambda) = g g† / (lambda - m_0).
```

So the full local transport correction is carried by a single rank-1 omitted
channel self-energy.

Numerically:

- if one removes `Sigma_omit`, the local branch near `lambda_*` no longer
  passes through the physical origin; its local intercept is
  `~ 6.84 x 10^(-4)`,
- the decoupled reached-sector slope is `~ 1.00032`,
- the full physical slope is `~ 0.95921`.

So the omitted-channel self-energy is what both:

1. shifts the local branch onto the physical origin,
2. lowers the slope from near-1 bare tracking to the observed `alpha`.

## 1. Visible microscopic data

The omitted-channel coupling vector is already visible inside `H_*`:

```text
g = [ lambda_+ + i/2,  lambda_- ]^T
```

in the reached ordering `(T2[110], T2[101])`, with

```text
lambda_+ = q_+* + delta_* - sqrt(8/3) = Re(H_*[1,3]),
lambda_- = q_+* - delta_* + sqrt(8/3) = H_*[1,2].
```

So the omitted-channel correction is not an abstract hidden matrix. It is a
rank-1 self-energy built from an already-visible two-link chamber packet plus
the fixed imaginary half-gamma phase.

## 2. Structural consequence

This sharpens the constructive target again.

The previous note said:

```text
derive the small reached-block backreaction term.
```

This note sharpens it to:

```text
derive the omitted-channel self-energy Sigma_omit(lambda)
```

from retained physics, because that self-energy is what generates the full
local backreaction.

So the live transport object is now even more concrete:

- one omitted channel,
- one rank-1 self-energy,
- one local Koide correction.

## 3. Honest scope boundary

This note does **not** claim:

- a retained derivation of the self-energy term from microscopic framework
  physics;
- a retained derivation of `lambda_*`;
- a full retained derivation of Koide `Q = 2/3`.

It does claim a real reduction:

- the local backreaction is not generic reached-sector complexity;
- it is carried by one explicit omitted-channel self-energy;
- the remaining transport problem is now localized to that self-energy term.

That is narrower than the previous transport target.
