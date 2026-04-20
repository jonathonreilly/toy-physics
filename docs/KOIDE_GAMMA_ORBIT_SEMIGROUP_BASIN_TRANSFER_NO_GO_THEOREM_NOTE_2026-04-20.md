# Koide `Gamma`-Orbit Semigroup Basin-Transfer No-Go Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide, positive one-clock semigroup avenue  
**Status:** exact basin-indiscriminacy theorem on top of the positive
one-clock semigroup reduction. This does not derive Koide from retained
framework data alone. It shows that the semigroup witness route also transfers
across the excluded G1 competitors, so it is not the physical basin selector.  
**Runner:** `scripts/frontier_koide_gamma_orbit_semigroup_basin_transfer_no_go.py`

## Question

The positive one-clock semigroup theorem proved that, once one chooses the
Hermitian generator `G`, the full repeated-step family is forced into

```text
X_beta = exp(beta G).
```

The live witness then inserted the G1 chamber pin

```text
G = H_* = H(m_*, delta_*, q_+*).
```

The natural next question is:

```text
does that semigroup witness itself distinguish the physical Basin 1 chamber pin
from the excluded G1 competitors?
```

This note answers that.

## Bottom line

No.

On the same current G1 competitor set used in the transport no-go

- Basin 1,
- Basin 2,
- Basin X,
- the chamber-violating CP-conjugate point,
- and the chamber-violating `C_neg q<0` point,

the exact same semigroup construction works:

1. `exp(H)` is positive Hermitian,
2. the small branch turns positive at one sharp threshold `beta_c in (0,1)`,
3. optimizing the small branch on `beta in [beta_c, 1]` gives an exact Koide
   point `Q = 2/3`,
4. after one overall scale fit, the resulting direction matches the PDG
   `sqrt(m)` direction to the same near-machine precision on every candidate.

Numerically:

| Candidate | `beta_c` | `beta_*` | direction cosine | max relative `sqrt(m)` error after one scale |
|---|---:|---:|---:|---:|
| Basin 1 | `0.593363519623` | `0.633571941814` | `0.999999999989318` | `2.158649e-04` |
| Basin 2 | `0.391974917787` | `0.477092957848` | `0.999999999989318` | `2.325728e-04` |
| Basin X | `0.348978842387` | `0.416008018245` | `0.999999999989209` | `2.430998e-04` |
| CP-conjugate | `0.662280852495` | `0.708262239265` | `0.999999999988905` | `1.900725e-04` |
| `C_neg q<0` | `0.694482817953` | `0.794426532647` | `0.999999999989337` | `2.284642e-04` |

The direction-cosine spread across the whole competitor set is only
`~ 4.3 x 10^(-13)`.

So the semigroup witness route does not pick Basin 1. It transfers across the
same G1 competitor set almost perfectly.

## Meaning

This closes another live-looking loophole.

Before this note, the one-clock semigroup route still looked like a plausible
independent positive Koide avenue, conditional only on the G1 chamber pin.
After this note, that reading is gone.

The correct reading is:

```text
the one-clock semigroup witness is a transport-style transfer mechanism on top
of the G1 chamber data, not a selector of that data.
```

So this route does not bypass the open G1 chamber/basin selection program
either.

## Honest scope boundary

This note does **not** claim:

- a retained derivation of the physical G1 chamber pin,
- a retained derivation of `Q = 2/3`,
- a retained exclusion of the competitor set from charged-lepton data alone.

It does claim a real no-go:

- the exact semigroup witness is not unique to Basin 1,
- excluded G1 competitors carry essentially the same witness,
- therefore the semigroup avenue inherits the open G1 chamber/basin problem
  rather than solving it.
