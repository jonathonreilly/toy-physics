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

### 3. Larger environment spaces fail if the coupling stays too deterministic

The most recent finite-env extensions sharpen the same point further. Qubit-per-mass and other enlarged-register variants do create much larger nominal environment spaces, but they still do **not** create enough occupied detector-state entropy to resist recoherence on larger graphs.

The important distinction is:

- **environment dimensionality** can be large
- while **environment entropy under the actual coupling law** stays low

In the tested architectures, the system-environment coupling is mostly a deterministic assignment:

- node label
- edge label
- angle bin
- qubit flip pattern
- cumulative bin update

That kind of coupling does not create a genuinely rich local superposition in the environment. It mostly routes amplitude into labels that the path sum then reconcentrates.

So the sharper current diagnosis is:

- the bottleneck is **not just env size**
- it is **the interaction law that sets the occupied env distribution**

The current working hypothesis is therefore slightly narrower than a pure
“entropy” story:

- larger env dimensionality alone does not help
- larger occupied env support alone also does not obviously help
- what matters is whether the interaction creates the right
  **branch-weight structure** at the detector after tracing

That is, the open problem is not just “more env states” and not yet
provably “more env entropy.” It is finding a local interaction law that
does not collapse back into either:

- deterministic bookkeeping, or
- a very thin spread over many weak env branches

## The sharpened problem

The decoherence architecture must live at a scale that avoids both failure modes:

- **too microscopic / label-like:** gets averaged away by path convergence
- **too macroscopic / field-like:** gets smoothed away by relaxation
- **too deterministic / bookkeeping-like:** creates large env spaces but the wrong occupied branch structure

The missing layer is probably **mesoscopic durable record formation**:

- local enough to retain branch-specific information
- extensive enough to grow with system size
- durable enough to implement Axiom 5 / Axiom 9 seriously
- structured enough to avoid compressing immediately into one or two dominant labels
- coupled richly enough to create real local system-environment branching, not just deterministic tagging
- shaped strongly enough that the traced detector state does not revert to the same high-purity limit

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
- genuinely local entangling couplings at mass interactions

**Why choose this**

- preserves the strongest part of the current model: linear transport and Born compatibility
- keeps the theory conservative
- stays closest to the existing unitary/open-system framing

**Risk**

- the same convergence problem may reappear in disguised form
- a “bigger bath” may still not help if the occupied support keeps collapsing onto a few dominant states
- even a genuinely entangling interaction may fail if it spreads amplitude too thinly across many weak env branches
- an open-system model without the right branch-weight structure may just reproduce the old failure in a larger state space

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
- substrate records that are created by a true local branching interaction rather than deterministic label assignment

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
- a purely deterministic scar-writing rule may still fail if it does not create the right occupied record balance after tracing

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
- prefer a mechanism with a genuinely nontrivial local interaction law, not just a larger deterministic record map

## Brainstorm: other interesting decoherence approaches

These are the most interesting remaining directions given the current evidence and axioms.

### 1. Graph-memory scars

Each traversed mass edge/cell writes a persistent local mark into the graph or its local state. Later amplitudes interact with those marks, and the detector distribution is computed after tracing over the unresolved scar configuration.

Why it is interesting:

- strongest Axiom 1 / 5 / 9 fit
- local and durable
- not compressed into one env label
- best if the scar-writing itself is branching / state-creating rather than simple deterministic tagging

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

### 9. Genuine local entangling coupling

At each mass interaction, the system amplitude couples to a local env degree of freedom through a true branching interaction, producing local system-env superposition rather than deterministic record assignment.

Why it is interesting:

- directly targets the new interaction-law bottleneck
- keeps the theory linear if modeled as a local unitary interaction
- is the clearest version of “real quantum environment coupling” within the toy

### 10. Multiscale record hierarchy

Records form at multiple scales at once: local edge/cell records, regional summaries, and slow persistent memory. The detector only sees the coarse outcome after tracing over the full hierarchy.

Why it is interesting:

- explicitly targets the “between path and field” scale gap
- may avoid both single-label convergence and far-field smoothing

### 11. Explicit local projection / collapse

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

4. **Local entangling-coupling prototype**
   - one local env degree of freedom per mass interaction site
   - interaction creates branch superposition instead of deterministic tagging
   - test whether the traced detector state develops a better branch-weight structure instead of just more weak env support

## Most recent narrowing

Two additional prototypes now sharpen the same conclusion:

- the simple local `cos/sin` entangling split is a clean failure
- the repaired fixed-kick substrate-memory realization is also a clean failure

But the substrate-memory lane itself is **not** ruled out in general. The
fixed-kick model only tests one realization:

- split at unrecorded mass nodes
- then apply a fixed downstream phase kick on outgoing edges from recorded nodes

That failure means this **specific** interaction law does not beat the
convergence problem. It does **not** show that all substrate-memory or
history-dependent record mechanisms fail.

The key point is not to test ten new ideas. It is to test **one mesoscopic durable-record or local-entangling architecture** whose interaction law is meaningfully different from both label-like bookkeeping and the already-failed fixed-kick entangling variants.
