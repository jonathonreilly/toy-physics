# PMNS Graph-First Fixed-Slice Two-Holonomy Production Boundary

**Date:** 2026-04-17  
**Status:** exact production-boundary reduction on the PMNS-native fixed-slice lane  
**Script:** `scripts/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_2026_04_17.py`

## Question

After the new fixed-slice two-holonomy collapse theorem, what exactly remains
of the PMNS-native sole-axiom production problem for nonzero

`J_chi = chi`?

## Answer

The remaining PMNS-native blocker is now exactly:

> a sole-axiom law that produces a **nontrivial fixed-slice native holonomy
> pair**

for any independent angle pair on the graph-first reduced family.

Equivalently, it is exactly:

> a sole-axiom law that produces **nonzero** `chi = J_chi`.

The current bank still does **not** realize that source law.

## Exact reduction

On the graph-first reduced family

`A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31`,

the native holonomy law is

`h_phi = 2 u cos(phi) + 2 v sin(phi) + w`.

So on a fixed slice `w = w0`, any independent angle pair
`(phi_1, phi_2)` with

`sin(phi_2 - phi_1) != 0`

gives

```text
[h_phi1 - w0]   [2 cos(phi_1)  2 sin(phi_1)] [u]
[h_phi2 - w0] = [2 cos(phi_2)  2 sin(phi_2)] [v].
```

This matrix is invertible, so:

- the fixed-slice holonomy pair determines `(u, v)` exactly
- therefore it determines `chi = u + i v` exactly
- and conversely `chi = 0` if and only if the holonomy pair is the trivial
  slice value pair
  `((h_phi1, h_phi2) = (w0, w0))`

So after fixed-slice readout closure, the remaining production object is no
longer “some current law.” It is exactly a nontrivial fixed-slice holonomy-pair
source law.

## Canonical native `C3` form

For the canonical native pair

- `phi_1 = 0`
- `phi_2 = 2 pi / 3`

one has

```text
h_0        = 2 u + w0
h_(2pi/3)  = -u + sqrt(3) v + w0
```

and hence

```text
u   = (h_0 - w0)/2
v   = (h_0 + 2 h_(2pi/3) - 3 w0)/(2 sqrt(3))
chi = (h_0 - w0)/2 + i (h_0 + 2 h_(2pi/3) - 3 w0)/(2 sqrt(3)).
```

So in the canonical native basis,

`chi != 0`

if and only if

`(h_0, h_(2pi/3)) != (w0, w0)`.

That is the exact fixed-slice PMNS-native production target.

## Current-bank boundary

The current exact PMNS-native bank still does **not** supply this.

What is already exact:

- the current retained sole-axiom native routes still force `J_chi = 0`
- one-angle selector/holonomy data still do not collapse `chi`
- two independent native holonomies now reconstruct `chi` exactly on the
  fixed-slice readout side
- the three-flux / `C3` holonomy closures are still readout closures, not
  sole-axiom production laws for nontrivial values

Therefore the current PMNS-native frontier is no longer readout.
It is production of a nontrivial fixed-slice holonomy pair itself.

## Consequence

This sharpens the PMNS-native frontier one level further.

Before:

> derive a sole-axiom law that actually produces nonzero `J_chi = chi`

Now:

> derive a sole-axiom law that produces a nontrivial fixed-slice native holonomy
> pair, equivalently nonzero `chi = J_chi`

That is the strongest honest next theorem surface on the PMNS-native production
front of the current bank.

## Boundary

This theorem does **not** prove a new production law.

It proves:

- exact equivalence between nonzero fixed-slice PMNS-native current production
  and nontrivial fixed-slice holonomy-pair production
- the sharper current-bank statement that no such sole-axiom source law is yet
  present on the current PMNS-native bank

It does **not** prove:

- a Wilson descendant theorem
- a plaquette theorem
- a step-3 compatibility theorem

## Verification

```bash
python3 scripts/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_2026_04_17.py
```
