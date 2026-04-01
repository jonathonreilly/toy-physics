# Synthesis Note: Gravity, Decoherence, and Topology on Discrete Causal DAGs

**Date:** 2026-04-01  
**Status:** architecture result; dynamic emergence still open

## The current claim

On discrete causal DAGs with path-sum propagation, the retained architecture is
now:

- **unitary layer:** corrected `exp(i k S_spent) / L^p × exp(-0.8 theta^2)`
- **non-unitary layer:** IF / CL reduced-description decoherence
- **geometric control parameter:** channel separation / imposed gap in the graph

The big result is no longer “one clever bath works.” It is:

- **the same graph family can support both gravity and decoherence**
- and the controlling variable is **topology**

## The two graph-family lessons

### 1. Dense random families

On the original dense random / uniform-like DAG lane:

- the corrected propagator retains gravity and Born-safe interference
- graph-local decoherence architectures still converge too much as graphs densify
- connection-bias feedback rules do not create lasting separation

That lane taught the diagnosis:

- CLT acts on amplitude flowing through any sufficiently connected graph
- weak connection biases are not enough

### 2. Gap-controlled modular families

On modular two-channel DAGs with an imposed gap:

- the IF / CL route gives stable decoherence
- gravity remains positive
- interference remains strong
- larger gaps strengthen both effects until connectivity eventually breaks

The asymptotic modular lane now supports:

- `pur_min ~ 0.93 ± 0.02` through the tested `N=100` range
- visibility still above `0.99`

So the bottleneck was not the reduced non-unitary framework itself.
It was the graph family.

## Joint unification result

The most important integrated result is the **joint gravity + decoherence**
phase diagram on the same graph family.

Current retained read from the wider-seed pass:

- every tested gap in `0.0 .. 5.0` passes the current joint criteria
- larger gap gives monotonically stronger gravity and stronger decoherence
- crosslink probability is subleading across the tested `0.0 .. 0.10` range

So the right language is not a narrow sweet spot anymore.
It is:

- **a broad unification window controlled by topological channel separation**

## What this means physically

The current architecture story is:

1. **Gravity** is a pure phase effect from the corrected propagator.
2. **Decoherence** is a reduced interaction effect that works when the graph
   preserves branch-distinguishing structure.
3. **Topology** controls whether those branch distinctions survive graph growth.

The shared condition is no longer “a better bath” or “a better local kernel.”
It is:

- **hard topological separation**

That is, branch-preserving geometry appears to be the minimal discrete
condition for having gravity, interference, and decoherence coexist cleanly.

## What failed

Seven dynamic-emergence approaches now fail in the same structural way:

- locality bias
- reinforcement
- repulsive placement
- pre-barrier amplitude feedback
- post-barrier slit-conditioned connection feedback
- distinguishability placement with weak feedback
- distinguishability placement with strong feedback

The common reason is now sharper:

- they all modify **connections**
- or create **uncontrolled node gaps**
- but the working barrier is a property of **where nodes are absent**
- and in the retained modular family that barrier has a specific scale and
  location, not just any amount of emptiness

So the next growth question is not another connection-probability sweep.
It is whether graph dynamics can generate a **self-regulating node-absence
barrier** with the right size and placement.

## What is established

1. The corrected propagator is the retained unitary core.
2. The IF / CL route is the retained non-unitary framework.
3. Gap-controlled modular topology is the first family where both gravity and
   decoherence work together.
4. The unification window is broad in gap, not a knife-edge tuning artifact.

## What is still open

1. **Dynamic emergence**
   The good topology is imposed, not generated.

2. **Self-regulating node placement / node removal dynamics**
   The natural next test is a rule that controls where nodes exist at all,
   rather than only how existing nodes connect, and that stabilizes the gap
   near the observed good scale instead of overshooting into disconnection.

3. **Boundary-condition interpretation**
   If that self-regulating rule never appears cleanly, the remaining serious
   alternative is that the gap should be treated as part of the effective
   spacetime boundary condition rather than something derivable from a simpler
   microscopic growth bias.

4. **Asymptotics**
   `pur_min ~ 0.93 ± 0.02` may be a true floor or a slowly drifting large-`N`
   regime; more seeds are still needed.

5. **Continuum interpretation**
   Channel separation still needs a cleaner bridge to emergent spacetime
   language.

## Honest assessment

This is now stronger than two disconnected toy wins.

The repo supports a single architectural sentence:

- **on discrete causal DAGs, gravity and decoherence can coexist when topology
  preserves branch separation**

The make-or-break open problem is whether the graph can create that
branch-preserving topology for itself at the right scale and location.
