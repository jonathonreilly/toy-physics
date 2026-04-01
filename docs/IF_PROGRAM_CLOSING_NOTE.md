# IF Decoherence Program: Uniform-DAG Closure and Topology Outcome

**Date:** 2026-04-01
**Status:** uniform-architecture search closed; IF / CL route retained on gap-controlled topology

## What was retained

The **influence-functional (IF)** formulation is still the retained
reduced-description framework for decoherence in this repo.

What survived:

- Hermiticity checks
- baseline recovery (`alpha = 0 -> purity = 1`)
- partial agreement with explicit slot-resolved fresh-ancilla bookkeeping
- clean reduced-density formulation without explicit environment-state blow-up

The IF framework itself was **not** the bottleneck.

## What closed on the old lane

The original uniform-random / dense-connected DAG search is now cleanly
diagnosed.

What failed there:

- node / edge / y-bin / angle labels
- larger finite registers
- entangling local env variants
- fixed-kick substrate memory
- fresh-ancilla proxies and local-observable IF kernels
- connection-feedback growth rules meant to induce channeling

Common failure:

- as the graph gets sufficiently connected, both slits access almost the same
  local interaction region
- amplitude-weighted branch statistics converge
- tracing removes less than expected
- connection-bias feedback cannot rescue this, because CLT acts on amplitude
  flowing through any sufficiently connected graph

So the closed result is:

- **the old local-architecture search on dense connected graph families is not
  the right frontier anymore**

## What changed after the topology pivot

Changing only the graph family changed the outcome.

On modular / gap-controlled DAGs:

- the same IF / CL machinery yields stable decoherence
- the old both-slits-open contrast proxy remains high
- gravity still works on the same family
- larger imposed gap gives stronger gravity and stronger decoherence until
  connectivity breaks

The older small-sample “narrow sweet spot” story has now been replaced by a
broader modular-family read:

- tested gaps `0.0..5.0` keep positive gravity and `pur_cl < 0.96`
- larger imposed gaps generally strengthen both phenomena until connectivity
  breaks

One scope note still matters here:

- once the large-`N` script is upgraded to a true single-vs-double-slit
  visibility gain, that gain is only weak at `N=12`, near-zero by `N=18`, and
  gone or slightly negative by `N>=25`

So the current repo-facing claim is:

- **the IF / CL route works when the topology preserves branch separation**

## What remains open

The remaining problem is no longer “find another bath.”
It is:

- **how to generate the right hard topological gap dynamically**

Seven local emergence attempts now fail for the same structural reason:

- they only modify **connections**
- or create **gaps with the wrong size / location**
- but the retained barrier is a property of **node absence at the right place**

That points to a sharper next frontier:

1. self-regulating node-placement rules
2. node-removal / non-permanence rules that can stabilize a slit-centered gap
   as a genuine local hard-gap law rather than a global pruning surrogate;
   fixed-threshold and adaptive-quantile deletion are now bounded positives in
   3D, but deletion-only pruning on a connected graph is still a closed
   asymptotic lane
3. other dynamics that can create or maintain regions with no nodes at the
   right scale
4. or, if those fail cleanly, treating the gap as part of the effective
   boundary condition rather than a simpler derivative growth rule

That is a different class of test from the earlier connection-probability
feedback sweeps.

## Decision

Keep:

- corrected `1/L^p` transport
- directional path measure `exp(-0.8 theta^2)`
- IF / CL reduced-description machinery

Do **not** reopen broad bath/kernel architecture search on dense connected
random DAGs.

Next decisive question:

- **can graph dynamics create or maintain the node-absence barriers that the
  working modular topology currently imposes by hand, at the right scale and
  location, in a way that remains valid past `N=60`?**
