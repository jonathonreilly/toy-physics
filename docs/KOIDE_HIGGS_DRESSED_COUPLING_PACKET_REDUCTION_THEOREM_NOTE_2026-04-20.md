# Koide Higgs-Dressed Coupling-Packet Reduction Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide, constructive transport avenue  
**Status:** exact coupling-data reduction on top of the self-energy coherence
theorem. This still does not derive Koide from retained framework data alone,
but it shows the coherent omitted-channel vector is already only a two-real
visible chamber packet.  
**Runner:** `scripts/frontier_koide_higgs_dressed_coupling_packet_reduction_theorem.py`

## Question

The self-energy coherence theorem reduced the remaining transport object to the
coherent omitted-channel coupling vector `g`. The natural next question is:

```text
how much free data is really left in g?
```

This note answers that.

## Bottom line

Very little.

The coherent omitted-channel vector is exactly

```text
g = [ lambda_+ + i/2,  lambda_- ]^T,
```

with

```text
lambda_+ = q_+* + delta_* - sqrt(8/3),
lambda_- = q_+* - delta_* + sqrt(8/3).
```

So once the retained fixed constants `sqrt(8/3)` and `Gamma = 1/2` are peeled
off, the entire coherent self-energy packet is already determined by a visible
two-real chamber packet `(lambda_+, lambda_-)`.

Equivalently,

```text
g g†
```

is not carrying a free complex-vector ambiguity. It is the rank-1 packet built
from those two real chamber links.

## Meaning

This sharpens the live transport object once more.

The previous note said:

```text
derive the coherent omitted-channel coupling vector g.
```

This note sharpens it to:

```text
derive the visible two-link chamber packet (lambda_+, lambda_-).
```

So the remaining transport problem is now two-real, visible, and explicit.

## Honest scope boundary

This note does **not** claim:

- a retained derivation of `(lambda_+, lambda_-)`,
- a retained derivation of `lambda_*`,
- a full retained derivation of Koide `Q = 2/3`.

It does claim a real reduction:

- the coherent omitted-channel vector is not an arbitrary complex datum,
- it is already a two-real visible chamber packet plus fixed constants.

That is narrower than the previous transport target.
