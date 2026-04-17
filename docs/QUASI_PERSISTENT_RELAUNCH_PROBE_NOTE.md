# Quasi-Persistent Relaunch Probe Note

**Date:** 2026-04-04  
**Status:** bounded compression/control result; not a persistent-mass theorem

## Artifact chain

- Script: [`scripts/quasi_persistent_relaunch_probe.py`](/Users/jonreilly/Projects/Physics/scripts/quasi_persistent_relaunch_probe.py)
- Log: [`logs/2026-04-04-quasi-persistent-relaunch-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-quasi-persistent-relaunch-probe.txt)

This is the smallest honest probe I found that goes beyond a point-source
test-particle replay on the retained ordered-lattice family.

The experiment:

1. launch a point packet on a short ordered-lattice segment
2. propagate it freely to get a detector-layer packet profile
3. compress that outgoing profile to a smaller support
4. relaunch the compressed state
5. compare downstream free motion and weak-field response

The question is not whether the packet moves. The question is whether the
packet can be compressed into a *mesoscopic surrogate* that still behaves like
the same object on a second segment.

## Frozen result

Frozen on the retained `h = 0.5`, `W = 8`, `L = 6` ordered-lattice segment:

### Best square-window surrogate

- `square_r=7`
- support size: `225` sites
- capture fraction: `0.855`
- free-profile TV distance: `0.080`
- gravity-profile TV distance: `0.080`
- relative delta error: `0.077`

### Best top-N surrogate

- `topN=196`
- support size: `196` sites
- capture fraction: `0.835`
- free-profile TV distance: `0.082`
- gravity-profile TV distance: `0.082`
- relative delta error: `0.001`

## Safe Read

This is the cleanest bounded statement:

- the downstream response survives moderate support compression
- the surrogate must remain broad and mesoscopic to stay faithful
- sharp localization fails, so the object is not yet a true persistent mass

So the probe gives us:

- a real quasi-persistent surrogate on the retained ordered family
- a clear limit on how narrow that surrogate can be
- no closure on the inertial-mass problem

## Relation to the other controls

This probe should be read together with:

- [`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md)

Together they say:

- localized packets are re-identifiable
- compressed relaunch surrogates are viable if they stay broad enough
- the same story survives a 2D cross-family sanity check
- but none of this yet produces a persistent-pattern inertial theorem

## Best next move

The next honest step is to ask whether the compressed surrogate can survive
*another* relaunch stage without collapsing into an ordinary broad packet.

If that fails, the blocker remains:

- no self-maintaining inertial object
- no closed persistent-mass derivation
