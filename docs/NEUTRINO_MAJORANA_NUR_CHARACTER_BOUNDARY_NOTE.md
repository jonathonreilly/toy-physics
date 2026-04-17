# Neutrino Majorana `nu_R` Transfer-Character Boundary

**Date:** 2026-04-16  
**Script:** `scripts/frontier_neutrino_majorana_nur_character_boundary.py`

## Question
On the sole-axiom retained Majorana lane, can the lower-level transport /
transfer / response data on the unique anomaly-fixed `nu_R` line generate or
force a nonzero charge-`2` Majorana pairing law by themselves?

## Answer
No.

On the current exact bank, the retained `nu_R` support is a one-dimensional
line. That forces every projected linear observable on that support to be
scalar. So the sole-axiom transfer/holonomy family on `nu_R` is at most a
`U(1)` character family, and its lower-level response data remain scalar
resolvents.

After Nambu doubling, those scalar responses lift only to diagonal `2 x 2`
blocks. Their anomalous off-diagonal block vanishes identically.

Therefore the current sole-axiom bank still does not produce a nonzero
Majorana pairing law on the retained `nu_R` lane.

## Exact Content

The theorem proves:

1. the anomaly-fixed retained `nu_R` support is rank `1`
2. every projected microscopic operator on that support is exactly of the form
   `lambda P_{nu_R}`
3. the canonical transfer/holonomy data therefore form only a scalar `U(1)`
   character family
4. the induced lower-level responses are scalar resolvents
5. the associated Nambu lifts are diagonal and have zero anomalous block
6. the canonical charge-`2` Majorana primitive is not contained in that scalar
   Nambu-lift span

So the strongest next honest statement is not just “charge-preserving normal
response does not reopen Majorana.” It is:

> the whole sole-axiom transfer/response family on the retained `nu_R` line is
> scalar, so it cannot generate the required off-diagonal charge-`2` Nambu
> primitive.

## Consequence

This sharpens the blocker for full sole-axiom neutrino closure:

- the missing Dirac/PMNS object is still a nontrivial retained response law
- the missing Majorana object is now identified more precisely as a genuinely
  new off-diagonal charge-`2` primitive on the Nambu-doubled `nu_R` line

So the current exact bank does not merely fail to pick a Majorana amplitude. It
does not generate the correct kind of object on the retained `nu_R` line at
all.

## Verification

```bash
python3 scripts/frontier_neutrino_majorana_nur_character_boundary.py
```
