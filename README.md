# Discrete Alien-Physics Toy Model

This workspace contains a small runnable prototype for the event-network ontology.

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
- Cross-slit interference disappears when histories are separated by durable record sectors, without any appeal to consciousness, while single-slit diffraction remains inside each sector.
- A Hadamard-style reversible mixer preserves the 2-norm but not 1- or 4-norm totals, which is a useful reason the Born-style square survives the pressure test better than arbitrary power rules.
- Under boost-like frame mixing, `sqrt(dt^2 - dx^2)` is the only tested local scalar that remains invariant; the remaining action assumption is the choice to treat `dt - sqrt(dt^2 - dx^2)` as spent delay.

What is still cheating:

- The spatial graph geometry is still hand-authored.
- The gravity-like classical limit still assumes that histories extremize spent delay `dt - sqrt(dt^2 - ds^2)` rather than deriving that accounting rule from deeper dynamics.
- The delay field is now derived from an emergent persistent pattern, but the rule family and locality preferences used to choose among candidate patterns are still hand-chosen.
- Complex amplitudes are still assumed rather than derived.
- Consciousness is still outside the simulation; only record formation is present.

So this prototype does not replace physics. It is a compact testbed for checking which parts of the ontology can already be realized with a simple discrete model, and which parts are still axioms wearing different clothes.
