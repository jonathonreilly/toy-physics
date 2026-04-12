# Nature Science Backlog

**Date:** 2026-04-12
**Purpose:** Prioritized work items to increase Nature acceptance probability
**Current P(Nature):** ~60%

## Priority 1: Literature anomaly search
**Impact:** +10-15% if match found
**Cost:** Low (research only)

Search for existing experimental anomalies that match framework predictions:
- Big G scatter: does the framework's finite-size correction predict the pattern?
- Short-range gravity deviations (Adelberger, Kapner): lattice corrections?
- Sinha I₃ measurement: tighter bounds since 2010?
- GRANIT neutron bouncer: any deviation from Schrödinger?
- Gravity-induced decoherence bounds (Pikovski 2015, Xu 2020): match our rate?
- Any tabletop gravity experiment with unexplained systematics

**Target:** Find 1-2 existing measurements where the framework either explains an anomaly or tightens a bound.

## Priority 2: d_s = 3 dynamical selection
**Impact:** +15-20% if it works
**Cost:** Medium (1 hour compute)

Test whether self-consistency of propagator + field SELECTS d_s = 3:
- Run full self-consistent iteration on graphs with d_s = 1, 2, 3, 4, 5
- Check if all three (attractive gravity + β=1 + I₃=0) only coexist at d_s = 3
- If yes: "why is space 3-dimensional?" answered from first principles
- This would be Nature-guaranteed if it works

**Script:** frontier_dimension_selection.py
**Note:** DIMENSION_SELECTION_NOTE.md

## Priority 3: Post-dict the hierarchy problem
**Impact:** High if ratio comes out right
**Cost:** Medium

Compute the gravity/EM coupling ratio from the framework:
- Gravity enters as self-consistent Poisson response (coupling G)
- EM enters as U(1) phase (coupling e)
- Their ratio G/e² ~ 10⁻³⁶ in nature
- Can we compute this from graph structure?
- If the ratio depends on graph spacing in a specific way, that constrains the spacing

**Script:** frontier_hierarchy_ratio.py
**Note:** HIERARCHY_RATIO_NOTE.md

## Priority 4: Background independence
**Impact:** +5-10%
**Cost:** Medium

Show that effective geometry ≠ input graph:
- Place a strong mass on a graph
- Show the effective connectivity (subgraph with nonzero propagator amplitude) changes
- The emergent geometry responds to matter
- "The graph is the input, but the geometry is the output"

**Script:** frontier_background_independence.py
**Note:** BACKGROUND_INDEPENDENCE_NOTE.md

## Priority 5: Tensor network / AdS-CFT connection
**Impact:** +3-5%
**Cost:** Low (analytical argument + small computation)

Make the connection explicit:
- Path-sum propagator on a graph IS a tensor network
- Area-law entropy (R²=0.9996) is a tensor network property
- The gravitational field modifies bond dimensions
- Connection to Swingle, Ryu-Takayanagi, ER=EPR literature

**Script:** frontier_tensor_network_connection.py
**Note:** TENSOR_NETWORK_CONNECTION_NOTE.md

## Priority 6: Foundational axiom reduction
**Impact:** Medium (strengthens theoretical claims)
**Cost:** High (deep theoretical work)

Reduce from ~5-6 assumptions to truly 2:
- Start with ONLY "quantum systems with pairwise interactions"
- Derive graph structure from self-consistency
- Derive propagator structure from unitarity
- Derive field equation from self-consistency
- The graph itself emerges from quantum mechanics

**Note:** AXIOM_REDUCTION_NOTE.md

## Probability projections

| Scenario | P(Nature) |
|---|---|
| Current | ~60% |
| + literature anomaly match | ~70-75% |
| + d_s=3 selection | ~80% |
| + both | ~85% |
| + diamond lab data | ~90% |
