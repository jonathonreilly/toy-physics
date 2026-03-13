# Discrete Alien-Physics Toy Model

This workspace contains a small runnable prototype for the event-network ontology we built in conversation.

## Model Axioms

This toy model is built around a compact "alien" ontology:

- Reality is an evolving network of events and influence relations.
- Stable objects are persistent self-maintaining patterns in that network.
- Space is inferred from influence neighborhoods and signal delays.
- Duration is local update count along a pattern's history.
- The arrow of time is the direction of increasing durable record formation.
- Free systems follow the locally simplest allowed continuation.
- Inertia is undisturbed natural continuation.
- Gravity is natural continuation in a distorted continuation structure.
- Measurement is the formation of durable records that separate previously combinable alternatives.
- Consciousness is part of the wider ontology as a high-order record-integrating self-model, but it is not simulated here.

## Primitives

The code models the following toy primitives:

- `Event e`: a local change.
- `Link e -> e'`: an allowed influence from one event to another.
- `delta(e,e')`: delay on that influence.
- `k(e,e')`: compatibility weight for that influence.
- `History h`: an ordered chain of linked events.
- `W(h)`: the total weight of a history.
- `R`: a durable record state.
- `S`: a stable self-maintaining pattern in the event network.
- `tau_S(h)`: the internal update count of pattern `S` along history `h`.

## Toy Rules

- Reality evolves by extending compatible histories.
- Free evolution follows the locally best-compatible histories.
- Geometry is inferred from the delay and coupling structure, not assumed first.
- Duration is local update count, not a universal background.
- Dense stable patterns modify local delays, compatibilities, and update rates.
- Alternatives without durable records can combine.
- Alternatives tagged by different durable records cannot combine.
- Conscious systems are part of the wider framework as record-integrating predictive processes, but this prototype only models durable records, not consciousness itself.

Run it with:

```bash
python3 /Users/jonreilly/Projects/Physics/toy_event_physics.py
```

What it does:

- Extracts a classical-looking limit from the same shared local rule by following stationary-action geodesics on the async graph.
- Derives the local delay field from an emergent persistent pattern whose late-time occupancy sources graph-load under neighbor averaging, with the initial disturbance and self-maintenance rule jointly selected by searching interior one-node seeds against a compact rule family.
- Infers causal order from positive local delays on a graph, then orients propagation by that inferred causal order instead of a global step counter.
- Runs a small robustness sweep across rectangular, tapered, and skewed graphs, with hard or wrapped vertical boundaries and compact or extended local rule families.
- Models `measurement` as durable record formation in a two-slit-style path network.
- Uses one shared local edge rule for the causal-shell graph, the asynchronous continuation model, and the slit graph.
- Makes the local rule explicit through a small set of postulates and a derived `LocalRule` object.
- Pressure-tests two of the biggest cheats:
  - why `positive weights only` are too weak for interference
  - why the `square rule` is less arbitrary once reversible linear mixing is required
  - which local scalar remains stable under boost-like frame mixing

What the script shows:

- The same local rule can be used to extract stationary-action geodesics while still inferring causal order from local delays.
- With a proper-time-style action derived from the same delay field, those geodesics bend inward in a gravity-like way instead of merely routing around a slow region.
- The delay field itself now emerges from a local graph-relaxation rule: the code searches over interior one-node seeds and simple update rules, grows each candidate into an orbit, and lets the most localized stable non-boundary component source the decaying load profile.
- A local-delay graph can recover an inferred causal order without assigning all nodes the same global step number.
- The robustness sweep is now stronger than before: a minimal reduced compact family survives all six tested scenarios, and the extended family also survives all six.
- The compact-family repair is informative rather than ad hoc: the hard-topology winners under the full compact family are `skew-hard -> S[2,3]/B[3]` and `skew-wrap -> S[3,4]/B[1,3]`, which first repairs the compact family to `{3}, {1,3}, {2,3}, {3,4}`.
- Exhaustive minimization inside that repaired family shows one motif is still redundant, so the actual surviving compact subset is just `{1,3}, {2,3}, {3,4}`.
- One-by-one ablation of that three-option subset then shows all three remaining motifs are indispensable in the current sweep: removing `{1,3}` breaks `skew-wrap`, removing `{2,3}` breaks `taper-wrap`, and removing `{3,4}` causes the broadest collapse.
- A deeper mechanism ablation sharpens the story further: removing the delay field collapses the effect, and weakening field relaxation breaks the hardest wrapped skew case, so the field side looks genuinely load-bearing.
- The honest weak spot is now clearer too: replacing the proper-time-style action with plain coordinate delay weakens the sweep, but a bare link-length action still passes the current robustness metric, which means the action principle is not yet uniquely selected by the present tests.
- A final action-response discriminator closes most of that gap: once the benchmark also requires the distorted geodesic to move relative to the free geodesic, the spent-delay action with relaxed field propagation is the only named mechanism that both survives all six scenarios and keeps positive wrapped-case path response.
- A broader retained-weight family sweep then sharpens the remaining ambiguity: the low-weight half of the family fails the combined benchmark, while only the high-weight end survives, with the strongest wrapped-case response at the full spent-delay point `w = 1.0`.
- With that repair in place, `extended` still produces the larger average boundary-delay span, while the reduced `compact` family keeps a slightly larger average center gap.
- The earlier `skew-wrap` miss is now understood as a legacy reduced-family coverage bug, not as a deep compact-vs-extended ontology split.
- The failure-mode story is still useful history: before the repair, skewed cases mostly failed by producing empty or fragmented candidate patterns, not by hitting the boundary filter, which pointed more toward pattern formation than boundary selection.
- Cross-slit interference disappears when histories are separated by durable record sectors, without any appeal to consciousness, while single-slit diffraction remains inside each sector.
- A Hadamard-style reversible mixer preserves the 2-norm but not 1- or 4-norm totals, which is a useful reason the Born-style square survives the pressure test better than arbitrary power rules.
- Under boost-like frame mixing, `sqrt(dt^2 - dx^2)` is the only tested local scalar that remains invariant; the remaining action assumption is the choice to treat `dt - sqrt(dt^2 - dx^2)` as spent delay.

What is still cheating:

- The spatial graph geometry is still hand-authored.
- The gravity-like classical limit still assumes that histories extremize spent delay `dt - sqrt(dt^2 - ds^2)` rather than deriving that accounting rule from deeper dynamics.
- The delay field is now derived from an emergent persistent pattern, but the rule family and locality preferences used to choose among candidate patterns are still hand-chosen.
- The robustness sweep budget is also hand-chosen: smaller graphs, reduced rule families, and shorter persistence windows trade completeness for runtime.
- Complex amplitudes are still assumed rather than derived.
- Consciousness is still outside the simulation; only record formation is present.

So this prototype does not replace physics. It is a compact testbed for checking which parts of the ontology can already be realized with a simple discrete model, and which parts are still axioms wearing different clothes.
