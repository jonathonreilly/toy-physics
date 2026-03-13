# Discrete Alien-Physics Toy Model

This workspace contains a small runnable prototype for the event-network ontology.

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
