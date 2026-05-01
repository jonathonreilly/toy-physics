# PMNS Graph-First Axis Alignment

**Status:** bounded - bounded or caveated result note
**Script:** [`frontier_pmns_graph_first_axis_alignment.py`](../scripts/frontier_pmns_graph_first_axis_alignment.py)

## Question

Can a genuinely graph-native selector on the `hw=1` corner triplet derive any
positive PMNS law without returning to the old full microscopic decomposition
route?

## Answer

Yes, partially.

The canonical cube-shift selector on the `hw=1` triplet has exactly three
coordinate-axis minima, each with residual `Z_2` stabilizer. Pushing that
selected axis onto the active Hermitian triplet lane forces the aligned law

`P_23 H P_23 = H`,

and therefore the active aligned Hermitian core

`H = [[a,b,b],[b,c,d],[b,d,c]]`.

## Theorem

**Theorem (graph-first axis alignment).**

On the graph-first `hw=1` route:

1. the normalized cube-shift selector has exactly three axis minima,
2. each selected axis has exact residual `Z_2` stabilizer,
3. residual `Z_2` invariance on the active Hermitian triplet lane forces
   `P_23 H P_23 = H`,
4. hence the active aligned Hermitian core is exactly
   `[[a,b,b],[b,c,d],[b,d,c]]`.

## What This Gives

This is a real positive native law:

- it derives weak-axis selection,
- it derives the aligned active Hermitian grammar,
- it does so from the graph-native `hw=1` corner structure rather than from
  the old PMNS packaging route.

## What It Does Not Yet Give

This route does **not** by itself determine:

- the aligned-core values `(a,b,c,d)`,
- which lepton sector carries the active block,
- the full off-seed microscopic value law.

So it is a positive partial closure route, not full closure.

## Role In The Overall Neutrino Lane

This route shows the microscopic no-go theorem is not saying “nothing further
can be derived natively.” A different native route can still produce genuine
partial laws.

The graph-first route derives:

- axis selection
- alignment

but leaves:

- aligned-core values
- active-sector choice

open.
