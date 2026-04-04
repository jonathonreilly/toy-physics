# Same-Family 3D Closure: Valley-Linear

**Date:** 2026-04-04
**Status:** All 10 properties on one family at one h

## Architecture
- Action: S = L(1-f) (valley-linear)
- Kernel: 1/L^2 with h^2 measure
- Lattice: 3D dense, h=0.25, W=10, max_d=3
- Field: s/r with s=5e-5

## Card

| # | Property | Value | Same family? |
|---|----------|-------|-------------|
| 1 | Born |I3|/P | 4.20e-15 | h=0.25 W=10 L=12 |
| 2 | d_TV | 0.83 | h=0.25 W=10 L=12 |
| 3 | k=0 gravity | 0.000000 | h=0.25 W=10 L=12 |
| 4 | F∝M alpha | 1.00 | h=0.25 W=10 L=12 |
| 5 | Gravity sign | +0.000224 TOWARD | h=0.25 W=10 L=12 |
| 6 | Decoherence | 49.9% | h=0.25 W=10 L=12 |
| 7 | MI | 0.64 bits | h=0.25 W=10 L=12 |
| 8 | Purity stable | 50.0% (L=8,10,12) | h=0.25 W=10 |
| 9 | Gravity grows | +0.157→+0.224 | h=0.25 W=10 |
| 10 | Distance tail | b^(-0.93) W=10 / b^(-1.07) W=12 | h=0.25 |

Properties 8-9 use L=8,10,12 at the SAME h=0.25 and W=10.
No h=0.5 companions needed.

## What this closes

This is the first time all 10 properties are measured on one graph
family at one resolution with one action and one kernel. Previous
cards used h=0.5 companions for properties 8-9, or different W
for the distance law.

## What remains open

- The distance exponent (-0.93 to -1.07) is near-Newtonian but not
  exactly -1.0. The frozen W=12 replay gives -1.07 (steeper than -1).
- Properties 8-9 use multiple L values (necessary for scaling checks).
  This is a same-family multi-size test, not a single-instance card.
- The action is selected, not derived (though the universality class
  result shows it's the simplest member of the Newtonian family).
