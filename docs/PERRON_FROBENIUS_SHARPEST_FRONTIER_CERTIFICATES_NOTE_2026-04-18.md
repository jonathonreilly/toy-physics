# Perron-Frobenius Sharpest Frontier Certificates

**Date:** 2026-04-18  
**Status:** exact science-only sharpening of the PF frontier to its current
sharpest constructive/scalar certificates; these certificates are now all
negatively closed on the present bank, but they remain the sharpest frontier
decomposition for future reopening attempts  
**Script:** `scripts/frontier_perron_frobenius_sharpest_frontier_certificates_2026_04_18.py`

## Question

After the Wilson generator reduction, the PMNS scalar production reduction, and
the plaquette Hankel reformulation, what is now the sharpest honest
reviewer-facing statement of the remaining PF frontier?

## Answer

The branch sharpens to three certificates:

1. **Wilson current-bank frontier certificate**
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

That is the sharpest frontier decomposition now visible on the branch.

After the later full current-bank closure theorem, all three certificates are
now negatively closed on the present bank. They still identify the smallest
constructive/scalar objects that any stronger future science would have to
reopen.

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

## Corollary 1: the sharpest future-theory reopening lever is still Wilson

On the present bank, none of the three sharpest frontier certificates is
realized positively.

But under stronger future science, Wilson remains the main plausible reopening
lever.

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

- Wilson reopening under stronger science is one local generator + one cubic
  characteristic-polynomial
  identity,
- PMNS-native production is one scalar nonvanishing certificate,
- plaquette non-Wilson closure already fails at one first Hankel + `K`
  certificate.

## Command

```bash
python3 scripts/frontier_perron_frobenius_sharpest_frontier_certificates_2026_04_18.py
```
