# Decoherence Decision Note

**Status:** architecture decision point
**Date:** 2026-04-01

## Current state

The current model now has a much cleaner split than it did at the start of this session:

- **Unitary layer:** the lead provisional propagator is corrected `1/L^p` transport with a directional path measure `exp(-0.8×θ²)`. It currently passes the tested 2D unitary guards:
  - Born
  - interference
  - `k=0→0`
  - gravity-scaling guardrail
  - bounded family transfer
- **Non-unitary layer:** no tested endogenous decoherence architecture scales correctly with graph size yet.

So the project is no longer bottlenecked by the propagator. It is bottlenecked by the **record / environment architecture**.

## What has been learned

Two broad decoherence routes have now failed for two different reasons.

### 1. Path-level label / record architectures fail by convergence

The tested node-label, edge-record, tensor, cumulative, directional-record, and related schemes all produce some small-graph detector-state mixing, but they wrong-scale on growing random DAGs. The common failure is:

- path multiplicity grows rapidly with graph size
- both slit branches eventually cover the same interaction region in many similar ways
- the amplitude-weighted distribution over record states converges
- the partial trace removes less and less

This is the current CLT-like failure mode.

### 2. Field-mediated decoherence fails by smoothing

The tested CA-oscillation / field-averaging route also failed. Rotating the active source cells through oscillation phases did **not** produce appreciable decoherence after field relaxation. The relevant lesson is narrower than “all field mechanisms are impossible,” but still important:

- the relaxed delay field is a **smoothed macroscopic observable**
- it responds mainly to the total source distribution
- fine internal rearrangements of the oscillating source are washed out before they reach the slit/detector region

So the tested field-mediated route failed by **Laplacian smoothing**, not by path convergence.

## The sharpened problem

The decoherence architecture must live at a scale that avoids both failure modes:

- **too microscopic / label-like:** gets averaged away by path convergence
- **too macroscopic / field-like:** gets smoothed away by relaxation

The missing layer is probably **mesoscopic durable record formation**:

- local enough to retain branch-specific information
- extensive enough to grow with system size
- durable enough to implement Axiom 5 / Axiom 9 seriously
- structured enough to avoid compressing immediately into one or two dominant labels

## Decision options

The next architecture decision is now clear enough to write down explicitly.

### Option A: Stay linear / open-system only

Keep the microscopic propagation linear and reversible, and continue searching for a scalable decoherence law entirely through tracing over additional degrees of freedom.

Candidate directions:

- true continuous bath variables
- local worldtube / region trace
- temporal-order or local-clock records
- local current / flux records
- unresolved microstate ensembles attached to mass cells

**Why choose this**

- preserves the strongest part of the current model: linear transport and Born compatibility
- keeps the theory conservative
- stays closest to the existing unitary/open-system framing

**Risk**

- the same convergence problem may reappear in disguised form
- a “bigger bath” may still not help if the occupied support keeps collapsing onto a few dominant states

**What would count as success**

- detector-state purity stops rising with graph size
- the mechanism remains local and extensive
- the propagator and Born package remain untouched

### Option B: Add mesoscopic durable record dynamics

Treat decoherence as the formation of **persistent local records in the substrate itself**, not as a tiny label attached to paths and not as a far-field change in the smoothed delay field.

Candidate directions:

- graph-memory “scars” written on traversed mass edges/cells
- topology-changing local records
- threshold-triggered local record bits
- region-local ancilla sheets / worldtubes with persistence
- local CA microstate coupling at the interaction site rather than through the relaxed far field

**Why choose this**

- fits the axioms best:
  - **Axiom 1:** reality is an evolving network
  - **Axiom 5:** arrow of time tied to durable records
  - **Axiom 9:** measurement is durable record formation
  - **Axiom 10:** prefer persistent local mechanisms
- naturally separates “record formation” from “field smoothing”
- gives a principled middle scale between path labels and relaxed fields

**Risk**

- introduces a larger design space
- can quietly become ad hoc if the record-writing rules are not tightly constrained
- may still act effectively like hidden collapse if the persistence is too strong

**What would count as success**

- record capacity grows with the interaction region
- branch-distinguishing information remains local and durable
- decoherence strengthens or at least does not weaken with graph size
- turning the record-writing off restores the unitary baseline

### Option C: Add explicit local projection / collapse

Introduce a genuinely irreversible map at mass interactions, for example a local projection of the amplitude into a mass-node interaction basis.

**Why choose this**

- directly attacks the convergence problem instead of trying to outgrow it
- avoids reliance on env-label diversity or far-field distinctions
- could produce strong decoherence with minimal extra state

**Risk**

- this is a major theory choice
- it introduces nonlinearity or explicit non-unitarity at the microscopic level
- it raises immediate Born-consistency and interpretation questions
- it is the hardest option to justify as “emergent” rather than “inserted”

**What would count as success**

- local projection law with clear trigger conditions
- Born/interference recovered when projection is off
- scalable decoherence when projection is on
- a coherent axiom-level justification for why projection is fundamental

## Recommended choice

The best next step is **Option B first**.

Reason:

- it is the best match to the current axioms
- it directly targets the gap between path-level tags and smoothed fields
- it keeps the current unitary transport intact
- it postpones the biggest conceptual jump (`collapse`) until there is stronger evidence that a substrate-memory route cannot work

So the recommended next architecture is:

- keep the directional-measure propagator fixed
- stop trying to make the propagator solve decoherence
- prototype one **durable local record** mechanism that lives on the graph substrate itself

## Brainstorm: other interesting decoherence approaches

These are the most interesting remaining directions given the current evidence and axioms.

### 1. Graph-memory scars

Each traversed mass edge/cell writes a persistent local mark into the graph or its local state. Later amplitudes interact with those marks, and the detector distribution is computed after tracing over the unresolved scar configuration.

Why it is interesting:

- strongest Axiom 1 / 5 / 9 fit
- local and durable
- not compressed into one env label

### 2. True region/worldtube trace

Instead of labeling paths, treat the whole mass-interaction region as an unresolved subsystem and trace over all internal region histories. This would be a real spatial/influence-functional decoherence mechanism rather than the current last-exit-node surrogate.

Why it is interesting:

- sits between path and field scales
- physically closer to how open subsystems are treated in continuum theory

### 3. Local CA microstate coupling at interaction sites

Do not let the CA affect the detector only through the relaxed field. Instead, let path traversal sample the local CA microstate directly when it passes a mass cell or mass edge.

Why it is interesting:

- avoids Laplacian smoothing
- keeps the mass’s internal dynamics relevant
- still endogenous to the substrate

### 4. Topology-changing records

Measurement-like interaction writes a local topological change into the graph: edge pruning, edge creation, or local rewiring near the traversed mass region. The record is the changed graph itself.

Why it is interesting:

- the project already has evidence that topology-changing record operators can strongly reshape visibility
- this is naturally durable

### 5. Temporal-order / local-clock records

Distinguish branches by **when** they interact with local mass microstates, not just where. A local clock or phase variable at each mass cell could store arrival-order information.

Why it is interesting:

- slit branches may converge spatially while still differing temporally
- uses causal ordering rather than geometric separation

### 6. Local current / flux bath

Record a local tensor or vector of amplitude flow through the mass region instead of a node or edge label. Decoherence would come from tracing over unresolved current configurations.

Why it is interesting:

- more structured than labels, less smoothed than the relaxed scalar field
- may capture the branch differences that survive after simple reachability converges

### 7. Threshold-triggered record bits

A mass cell writes a durable bit only when the accumulated local amplitude/current crosses a threshold. This makes record creation nonlinear and event-like without immediately requiring a full collapse law.

Why it is interesting:

- naturally measurement-like
- can create irreversibility without a global projection postulate

### 8. Unresolved microstate ensemble per mass cell

Each mass cell carries hidden internal microstates that couple locally to traversing amplitude. Decoherence arises by tracing over those unresolved local microstates, not over a single shared env tag.

Why it is interesting:

- a more realistic open-system picture
- could be continuous or high-dimensional without global binning

### 9. Multiscale record hierarchy

Records form at multiple scales at once: local edge/cell records, regional summaries, and slow persistent memory. The detector only sees the coarse outcome after tracing over the full hierarchy.

Why it is interesting:

- explicitly targets the “between path and field” scale gap
- may avoid both single-label convergence and far-field smoothing

### 10. Explicit local projection / collapse

Keep this as the final fallback if all substrate-memory approaches fail.

Why it is interesting:

- simplest route to strong decoherence
- strongest theory cost

## Suggested next experiments

Do **not** reopen a broad sweep. Run one bounded prototype from the recommended option:

1. **Graph-memory scar prototype**
   - local persistent record written on traversed mass edges/cells
   - trace over scar configuration
   - test purity vs graph size

2. **Local CA microstate coupling prototype**
   - traversal samples local oscillation state directly at interaction sites
   - no relaxed-field mediation
   - test whether decoherence survives graph growth

3. **True region/worldtube trace prototype**
   - trace over all histories inside a bounded interaction region
   - compare against the current D4 surrogate

The key point is not to test ten new ideas. It is to test **one mesoscopic durable-record architecture** that is meaningfully different from both label-like envs and smoothed field mediation.
