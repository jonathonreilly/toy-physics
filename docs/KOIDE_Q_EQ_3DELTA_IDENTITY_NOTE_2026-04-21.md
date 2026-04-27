# Q = p·δ Arithmetic Identity on the Current Koide Support-Route Values

**Date:** 2026-04-21
**Status:** proposed_retained arithmetic identity.
**Runner:** `scripts/frontier_koide_Q_eq_3delta_identity.py` — 16/16 PASS.

---

## Statement

Given the current Koide support-route values, the two retained values
satisfy a clean arithmetic identity:

```
Q = p · δ   where p = 3 is the Z_3 orbifold order

equivalently   Q = 3·δ   (numerically 2/3 = 3 · 2/9)
```

## Derivation

The identity follows from the two independent retained derivations
evaluated at their Z_3 axiomatic base:

- **δ = 2/p²** — from the Atiyah-Bott-Segal-Singer equivariant
  fixed-point formula for the APS η-invariant at an isolated Z_p
  fixed locus with tangent weights (1, p−1). At p = 3: δ = 2/9.
- **Q = 2/d** — from AM-GM on d-dimensional circulant isotype
  energies E_+ and E_⊥, which forces κ = 2 and hence Q = (1 + 2/κ)/d.
  At d = 3: Q = 2/3.
- **p = d = 3** — the Z_3 axiomatic base: the Z_3 isotypes that define
  d = 3 circulant generations ARE the same Z_3 as the C_3[111] cubic
  rotation subgroup that gives p = 3 in the APS formula. Both come
  from the retained C_3 ⊂ S_3 action on the Z³ lattice.

Combining: `Q/δ = (2/d)/(2/p²) = p²/d = p` (when p = d), so `Q = p·δ`.

## Why this matters

The Q and delta support routes are **not independent** derivations that
happen to both come out rational. They are **two faces of the same
retained Z_3 structure**:

- The delta support route derives the ambient `δ = 2/p²` value on the
  Z_p-orbifold side via APS η.
- The Q support route derives `Q = 2/d` on the d-dimensional-circulant
  side via AM-GM.
- The Z_3 axiomatic base forces p = d, linking the two values by
  Q = p·δ.

The identity `Q = 3·δ` is a cross-check of the combined framework: if
a reviewer accepts both the APS derivation of δ and the AM-GM
derivation of Q, the identity is immediate.

## Scope

This note covers ONLY the arithmetic bridge between the current Q and delta
support-route values. Consequences
of this identity for PMNS angles (Sum Rules, conservation laws under
(Q, δ)-parametrized deformations) are part of the separate PMNS lane
and are not included in this package.
