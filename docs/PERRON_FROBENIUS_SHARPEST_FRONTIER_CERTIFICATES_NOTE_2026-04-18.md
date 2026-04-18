# Perron-Frobenius Sharpest Frontier Certificates

**Date:** 2026-04-18  
**Status:** exact science-only sharpening of the remaining PF branch to its
current sharpest constructive/scalar certificates  
**Script:** `scripts/frontier_perron_frobenius_sharpest_frontier_certificates_2026_04_18.py`

## Question

After the Wilson generator reduction, the PMNS scalar production reduction, and
the plaquette Hankel reformulation, what is now the sharpest honest
reviewer-facing statement of the remaining PF frontier?

## Answer

The branch now sharpens to three certificates:

1. **Wilson positive reopening certificate**
   one local nilpotent-chain `1 + 1` certificate:
   - one local nilpotent chain generator on the physical adjacent two-edge
     chain,
   - and one cubic spectral identity
     `chi_(B_e)(lambda) = chi_(H_e)(lambda)`;
2. **PMNS-native scalar production certificate**
   one fixed-slice scalar holonomy discriminant
   `Delta_(phi1,phi2) > 0`;
3. **Plaquette first constructive scalar certificate**
   one first Hankel + `K` certificate.

That is the sharpest frontier decomposition now visible on the current bank.

## Setup

From
[PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md](./PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md):

- the remaining PF science had already been reduced to one Wilson certificate,
  one PMNS-native production certificate, and one plaquette scalar certificate.

The new point is that each of those three items has now been sharpened one
level further.

## Theorem 1: exact sharpest frontier decomposition of the current PF branch

On the current bank, the remaining PF frontier is now exactly the three
certificates listed above.

They are sharper than the previous decomposition because:

- the Wilson constructive object is no longer a path-algebra certificate but a
  single local generator plus one cubic spectral identity,
- the PMNS-native production object is no longer a holonomy-pair certificate
  but one scalar nonvanishing discriminant,
- the plaquette first constructive blocker is no longer just a first moment
  pair but one first Hankel + `K` certificate.

So the branch is now sharper than the earlier “minimal frontier certificates”
surface.

## Corollary 1: the positive reopening lever is still only Wilson

Among the three sharpest frontier certificates, only the Wilson certificate is
currently a positive reopening lever for a common sole-axiom PF selector.

The PMNS-native scalar certificate and the plaquette first-Hankel certificate
remain exact current-bank blockers.

## What this closes

- one sharper reviewer-facing decomposition of the remaining PF frontier
- one exact statement of the current sharpest Wilson / PMNS / plaquette objects

## What this does not close

- realization of the Wilson local generator certificate
- realization of the PMNS-native scalar discriminant certificate
- realization of the plaquette first Hankel certificate
- a positive global PF selector theorem

## Why this matters

This is the cleanest current statement of the branch.

The repo can now say:

- Wilson reopening is one local generator + one cubic characteristic-polynomial
  identity,
- PMNS-native production is one scalar nonvanishing certificate,
- plaquette non-Wilson closure already fails at one first Hankel + `K`
  certificate.

## Command

```bash
python3 scripts/frontier_perron_frobenius_sharpest_frontier_certificates_2026_04_18.py
```
