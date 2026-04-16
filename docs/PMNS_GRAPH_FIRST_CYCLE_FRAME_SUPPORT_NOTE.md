# PMNS Graph-First Cycle Frame Support

**Status:** exact support theorem, not a value-selection theorem  
**Script:** [`frontier_pmns_graph_first_cycle_frame_support.py`](../scripts/frontier_pmns_graph_first_cycle_frame_support.py)

## Question

Does graph-first axis selection plus graph-first SU(3) integration canonically
order or frame-fix the oriented-cycle basis strongly enough to support a future
value law?

## Answer

Yes, as a support theorem.

The graph-first selector has exactly three axis minima, each with residual
`Z_2` stabilizer. Once one axis is selected, the graph-first SU(3) integration
on that axis canonically fixes the selected-axis fiber/base split and the
residual swap on the complementary base. Together these data determine the
canonical oriented-cycle frame

`E12, E23, E31`

via forward transport from the diagonal projectors:

`E11 C = E12`, `E22 C = E23`, `E33 C = E31`.

So the oriented-cycle basis is not floating freely. It is frame-fixed by the
graph-first route strongly enough to state future cycle-value laws in an
invariant way.

## Theorem

**Theorem (graph-first cycle-frame support).**

On the graph-first PMNS `hw=1` route:

1. the normalized cube-shift selector has exactly three axis minima,
2. each selected axis has exact residual `Z_2` stabilizer,
3. graph-first SU(3) integration on a selected axis canonically fixes the
   fiber/base split and the residual swap on the complementary base,
4. the diagonal projectors transported by the canonical forward cycle give the
   unique ordered oriented-cycle frame `E12, E23, E31`,
5. this frame is strong enough to support a future value law, but it does not
   itself select the cycle coefficients.

## What This Gives

This is the exact structural support needed before any future coefficient or
value law on the cycle channel:

- the carrier is fixed,
- the basis ordering is fixed,
- the residual symmetry is explicit,
- the remaining freedom is only in the coefficients.

So the route is a real support theorem for a future value law.

## What It Does Not Yet Give

This route does **not** determine the values `(u, v, w)` on the reduced cycle
channel, and it does **not** provide a positive selector for those values.

The remaining open problem is therefore a value-selection law, not a frame
selection law.

