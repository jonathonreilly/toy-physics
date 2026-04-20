# Koide Higgs-Dressed Basin-Transfer No-Go Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide, constructive transport avenue  
**Status:** exact basin-indiscriminacy theorem on top of the chamber-pair
inversion theorem. This still does not derive Koide from retained framework
data alone. It shows the missing-axis Higgs-dressed transport route is not the
physical G1 selector: the same mechanism transfers to the excluded basin
competitors.  
**Runner:** `scripts/frontier_koide_higgs_dressed_basin_transfer_no_go_theorem.py`

## Question

The chamber-pair inversion theorem reduced the strongest surviving
Higgs-dressed transport route to the G1 chamber pair `(q_+*, delta_*)`.
The natural next question is:

```text
does the missing-axis transport mechanism itself distinguish the physical
G1 chamber point from the excluded basin competitors?
```

This note answers that.

## Bottom line

No.

On every currently known G1 chamber competitor that survives somewhere in the
PMNS search stack,

- Basin 1 `(det > 0, q_+ + delta > sqrt(8/3))`,
- Basin 2 `(det < 0, q_+ + delta > sqrt(8/3))`,
- Basin X `(det < 0, q_+ + delta > sqrt(8/3))`,
- the chamber-violating CP-conjugate point `(det > 0, q_+ + delta < sqrt(8/3))`,
- and the chamber-violating `C_neg` `q < 0` point `(det < 0, q_+ + delta < sqrt(8/3))`,

the exact missing-axis lift

```text
W_4(0) = diag(0, H(m, delta, q_+))
```

has the same basin-transfer signature:

1. exactly eight roots of the induced Koide equation `Q = 2/3`,
2. exactly one small positive root below `1`,
3. that small positive root has strong charged-lepton direction cosine
   `> 0.97` against the PDG `sqrt(m)` direction.

Numerically:

| Candidate | det(H) | chamber margin `q_+ + delta - sqrt(8/3)` | small positive root | direction cosine |
|---|---:|---:|---:|---:|
| Basin 1 | `+0.959174` | `+0.015856` | `0.015808703285` | `0.996266551503` |
| Basin 2 | `−70538.603772` | `+24.101007` | `0.726564569850` | `0.983548243463` |
| Basin X | `−20296.106451` | `+13.136270` | `0.452239666481` | `0.984786718568` |
| CP-conjugate | `+0.713983` | `−0.309593` | `0.016072878528` | `0.997463243272` |
| `C_neg q<0` | `−9.438189` | `−1.494093` | `0.042262176354` | `0.978818437415` |

The excluded CP-conjugate point actually has a **better** direction cosine
than Basin 1 on this transport route.

So the missing-axis Higgs-dressed transport construction is not the physical
basin selector. It transfers across the current G1 competitor set.

## Meaning

This closes an important loophole.

The previous note said:

```text
derive the G1 chamber pair (q_+*, delta_*) from retained physics,
because the transport packet is just an invertible repackaging of that pair.
```

This note sharpens that again to:

```text
the Higgs-dressed transport route cannot bypass the open G1 chamber/basin
selection program at all, because excluded basin competitors inherit the same
small-root mechanism.
```

So the live object is no longer "maybe transport itself secretly chooses the
physical basin." It does not. The remaining hard core is exactly the G1
selection stack:

- chamber / A-BCC,
- PMNS basin selection,
- or a deeper retained derivation of the physical G1 pin.

## Honest scope boundary

This note does **not** claim:

- a retained derivation of the physical G1 chamber pair,
- a retained derivation of `Q = 2/3`,
- a retained derivation of A-BCC or the PMNS observational pins.

It does claim a real no-go:

- the missing-axis Higgs-dressed transport avenue is basin-indiscriminate over
  the current G1 competitor set,
- it therefore cannot serve as the missing physical selector,
- and any Koide closure through this route inherits the open G1 chamber/basin
  problem rather than evading it.
