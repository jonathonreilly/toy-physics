# Koide Brannen Callan-Harvey Candidate Note (2026-04-22)

## Scope

This note records a concrete **candidate physical-bridge route** for the
charged-lepton Brannen phase `δ = 2/9`.

It does **not** close the physical bridge. The remaining open theorem is still:

> why the physical selected-line Berry phase on the charged-lepton `CP^1`
> carrier is the descended ambient anomaly / APS quantity.

What this route adds is a sharper physical proposal for how such a bridge
could work on the accepted physical-lattice reading of the framework.

## 1. What the route uses

The route packages the following already-landed ingredients:

- the accepted framework statement that `Cl(3)` on `Z^3` is the physical
  theory;
- retained anomaly arithmetic on the `3+1` single-clock surface;
- the retained three-generation identification of the body-diagonal fixed
  sites;
- the ambient `2/9` topological/anomaly value already isolated by the APS /
  ABSS support stack.

From these it identifies a concrete candidate descent geometry:

- ambient carrier: `3+1` physical spacetime with the `Z_3` body-diagonal fixed
  locus;
- candidate physical descent object: Callan-Harvey anomaly inflow onto the
  body-diagonal generation carrier;
- target observable: the selected-line Berry phase on the charged-lepton
  `CP^1` carrier.

## 2. What is genuinely useful here

This route does isolate one valuable physical statement:

```text
Tr[Y^3]_{q_L} per generation = (2d) · (1/d)^3 = 2/d^2 = 2/9   at d = 3
```

That gives a natural per-generation ambient anomaly coefficient on the same
`2/9` value as the Brannen lane.

So the route is not just another numerology match. It gives a specific
candidate mechanism:

1. ambient anomaly coefficient `2/9` on the physical lattice;
2. anomaly descent onto the body-diagonal generation carrier;
3. pullback or identification of that descended quantity with the
   selected-line Berry phase.

## 3. What is still missing

The branch that proposed this route claimed the following bridge equation:

```text
δ_Berry = (anomaly inflow rate) × (1D integration length)
```

and then specialized it to

```text
δ = (2/9) × 1 = 2/9 rad.
```

That is exactly the point that is still **not** derived.

Two load-bearing steps remain open:

1. **Berry/inflow map**
   There is not yet a retained theorem identifying the charged-lepton
   selected-line Berry phase with a Callan-Harvey inflow current or its
   descended holonomy.

2. **Unit descent normalization**
   There is not yet a retained theorem proving that the relevant descent
   length/normalization factor is exactly `1`.

So this route is best read as:

- a concrete physical candidate for the missing bridge,
- not the bridge theorem itself.

## 4. Status of the route

This route should be classified as:

- **bridge-conditioned support candidate**

not as:

- retained closure,
- derived physical-bridge theorem,
- or a public status change.

## 5. Artifacts

### Note

- `docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`

### Runner

- `scripts/frontier_koide_brannen_callan_harvey_candidate.py`

## 6. Bottom line

The useful science here is not “the Brannen bridge is solved.”

It is:

- the route now has a concrete physical-lattice anomaly-descent candidate;
- the per-generation anomaly coefficient on that route is exactly `2/9`;
- the remaining gap is no longer vague:
  it is the theorem identifying the selected-line Berry phase with that
  descended anomaly object, with the correct normalization.
