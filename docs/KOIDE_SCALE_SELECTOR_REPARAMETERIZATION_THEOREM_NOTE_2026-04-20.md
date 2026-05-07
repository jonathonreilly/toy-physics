# Koide Scale-Selector Reparameterization Theorem

**Date:** 2026-04-20  
**Status:** exact support / assumption-escape closeout on the charged-lepton Koide lane  
**Primary runner:** `scripts/frontier_koide_scale_selector_reparameterization_theorem.py`

## Scope

This note formalizes the strongest `M1`-style escape hatch from the current
selected-line Koide lane: the near-miss scale condition

```text
u v w = 1.
```

At first sight this looks like a possible native selector law for the physical
point `m_*`. The issue is whether the `u` in that condition is native selected
line data, or whether it already builds in the Koide relation.

It already builds in the Koide relation.

## The theorem

On the current selected line, the two native slots are

```text
v = Re(exp(H_sel(m))_{22}),
w = Re(exp(H_sel(m))_{11}).
```

The third slot used in the current Koide lane is

```text
u_small(v,w)
  = 2(v+w) - sqrt(3(v^2 + 4vw + w^2)).
```

This is not the native diagonal entry `Re(exp(H_sel(m))_{00})`. It is the
small root of the Koide completion identity, and it satisfies

```text
Q(u_small^2, v^2, w^2) = 2/3
```

identically.

Therefore every scalar built from `(u_small, v, w)` already lives on the
imposed Koide cone. In particular, `u_small v w` is **not** a pre-Koide native
forcing law. It is a scalar reparameterization on the already-completed Koide
lane.

## Native-vs-completed numerical separation

At the current physical selected point `m_* = -1.160469470087`, the runner
finds:

```text
native diagonal triple:    (x00, v, w) = (1.743731242408, 1.519073029007, 6.227744111005)
completed Koide triple:    (u,   v, w) = (0.105595212600, 1.519073029007, 6.227744111005)
Q_native     = 0.490021427531
Q_completed  = 0.666666666667
```

So the near-miss scale law does not read native diagonal physics. It reads a
Koide-completed surrogate slot.

## Near-miss consequences

Even after that honesty pass, the product condition is still interesting as a
support probe. The runner verifies:

- `u_small v w = 1` has exactly one physical-branch crossing,
- that crossing is

  ```text
  m_prod = -1.160256656687,
  |m_prod - m_*| = 2.1281e-04,
  ```

- the resulting amplitude direction has
  `cos-sim = 0.999999999021` to the PDG `sqrt(m)` direction,
- among the tested simple trace targets `Tr(exp(k H_sel(m))) = N_c^j`, none
  lands as close as this product condition,
- but the product condition still does not equal the current selected point,
  and it is only near, not identical, to the current `kappa_*` witness.

## Meaning

The `u v w = 1` near-miss is real support, but it is not an independent
closure route:

- it already assumes the Koide completion through `u_small`,
- it therefore cannot derive `Q = 2/3` natively,
- and even as a reparameterization it lands only near `m_*`, not on it.

So the `M1` escape hatch is also closed as a genuine derivation route. The
remaining charged-lepton gap is still one microscopic selector law, not a
hidden scale identity.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_selected_line_cyclic_response_bridge_note_2026-04-18](KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
- [koide_gamma_orbit_observable_selector_generator_line_note_2026-04-18](KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md)
- `koide_eigenvalue_q23_surface_theorem_note_2026-04-20` — SIBLING
  assumption-escape closeout theorem (M2-style; this note is the M1-style
  companion). Reference is backticked rather than markdown-linked because
  the two notes are sibling closeouts on the same charged-lepton Koide lane,
  and the existing edge from eigenvalue_q23 → this note (in that note's
  Audit dep repair links) is the kept direction. A markdown link here
  would create a length-2 cycle.
