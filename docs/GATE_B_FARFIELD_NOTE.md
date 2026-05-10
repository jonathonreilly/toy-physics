# Gate B Far-Field: Grown Geometry at h=0.5

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** frozen bounded numerical harness positive on the declared
far-field rows for the runner-defined h=0.5 family. Full-physics Gate B
far-field closure (deriving the source law, propagation/readout map, and
TOWARD/F~M criterion from accepted primitives) is **not** closed by this
note.
**Status authority:** independent audit lane only.
**Script:** [`scripts/gate_b_farfield_harness.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_farfield_harness.py) (PASS=4, all C-class)

## Audit boundary (2026-05-10)

The independent audit verdict on this row is `audited_conditional`. The
substantive runner output (36/36 TOWARD with mean F~M=1.00 across all four
drift/restore rows on z={3,4,5}, twelve seeds per row) is supported by a
non-print-only harness that genuinely constructs the geometry, propagates
amplitudes, computes valley-linear actions, and aggregates centroid shifts.

What is **not** closed in this note is the bridge from accepted primitives to
the physical "Gate B far-field gravity" reading. The harness assumes:

- a specific *growth rule* (template previous layer + Gaussian drift +
  restoring force toward grid + NN connectivity from grid labels);
- a specific *source law* (1/r field perturbation from each test mass);
- a specific *propagation kernel* (1/L^2 with `h^2` measure);
- a specific *valley-linear action* `S = L (1 - f)`; and
- a specific *readout criterion* (z-centroid shift TOWARD test mass plus
  linear `F ~ M` scaling at the tested z-rows)

as the operational gravity observable on this lattice family. None of those
ingredients is derived from the framework's accepted primitives in this
note's source packet. The harness verifies a bounded numerical statement
*assuming* that ingredient list is the right physical-gravity readout.

This note's load-bearing claim is therefore narrowed to the bounded numerical
harness-output statement on the declared scope, with the physical-gravity
bridge recorded as an admitted-context input that has to close upstream
before "Gate B far-field" closure can propagate.

## Artifact chain

- [`scripts/gate_b_farfield_harness.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_farfield_harness.py)
- [`logs/2026-04-05-gate-b-farfield-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-farfield-harness.txt)
- [`scripts/gate_b_grown_distance_law.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_distance_law.py)
- [`logs/2026-04-05-gate-b-grown-distance-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-distance-law.txt)
- `docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md` (sibling artifact in same Gate B
  lane; cross-reference only — not a one-hop dep of this note)
- [`scripts/gate_b_grown_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_joint_package.py)
- [`logs/2026-04-05-gate-b-grown-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-joint-package.txt)
- `docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md` (sibling artifact in same Gate B
  lane; cross-reference only — not a one-hop dep of this note)

## Admitted-context inputs (not closed by this note)

These are operational ingredients used by the runner that have to close
upstream before the "Gate B far-field gravity" reading can propagate:

- *growth rule:* template previous layer + Gaussian drift + restoring force
  toward grid + NN connectivity from grid labels (parametrized by
  `(drift, restore)`)
- *source law:* `1/r` field perturbation from each test mass located at the
  declared z-mass position
- *propagation kernel:* `1/L^2` two-slit kernel with `h^2` measure
- *valley-linear action:* `S(path) = L_path (1 - f_path)` with `L_path` the
  bounded valley length and `f_path` the path-fraction-on-valley score
- *readout criterion:* z-centroid shift TOWARD the test mass plus a linear
  `F ~ M` slope across `M = 1, 2, 3` at the declared z-rows

The bounded-positive harness numbers reported below assume that ingredient
list as the physical-gravity readout.

## Result

| drift | restore | TOWARD | F∝M |
|-------|---------|--------|-----|
| 0.3 | 0.5 | 36/36 (100%) | 1.00 |
| 0.2 | 0.7 | 36/36 (100%) | 1.00 |
| 0.1 | 0.9 | 36/36 (100%) | 1.00 |
| 0.0 | 1.0 | 36/36 (100%) | 1.00 |

12 seeds × 3 z-masses (z=3,4,5) = 36 tests per row.

## Growth rule

Template previous layer + Gaussian drift + restoring force toward grid +
NN connectivity from grid labels. Valley-linear action S=L(1-f), 1/L^2
kernel with h^2 measure.

## Bounded interpretation (scope-narrowed)

On the runner-defined h=0.5 family with the admitted-context ingredients
listed above, the harness reports `100%` TOWARD-z-centroid plus linear
`F ~ M = 1.00` at all four tested drift/restore levels for `z = 3, 4, 5`,
twelve seeds per row, including the noisiest (`drift = 0.3, restore = 0.5`).
That is the bounded numerical statement this note supports.

This does NOT close Gate B for the full parameter space: the v6
frozen replay at near-field parameters (z=1.0-2.0) remains mixed
(67-92%). The far-field rows are clean; the near-field rows are not.

It also does NOT close the physical-gravity reading even on the far-field
rows. The harness verifies that under the chosen growth rule, source law,
kernel, action, and readout, the lattice produces the harness-defined
TOWARD/F~M signature. Whether those ingredients are the framework's
retained physical gravity observable is the open Gate B question, not a
conclusion of this note's bounded numerical replay.

## What this says about Gate B

The growth rule, under the admitted-context source law and readout, produces
the harness-defined TOWARD/F~M signature in the declared far-field window.
The near-field mixing is a property of the beam optics at close mass
positions, not a growth-rule failure — the same mixing appears on the fixed
lattice at near-field z-values.

The honest Gate B read on this row: **bounded harness-defined far-field
positive on the declared rows, near-field mixed (same as the fixed lattice),
and the missing primitive-to-physical-gravity bridge keeps full Gate B open
upstream.**

## Companion transfer read (2026-04-05)

The dedicated companion replays now support a stronger but still bounded read
on the retained moderate-drift row (`drift = 0.2`, `restore = 0.7`):

- far-field sign remains `20/20` TOWARD on the bounded distance-law replay
- far-field `F∝M = 1.00` is frozen in the main far-field harness
- the distance-law companion keeps a positive declining tail close to the exact
  grid on the tested `z = 3..7` window:
  - exact grid: `b^(-0.90)`, `R^2 = 0.855`
  - grown geometry: `b^(-0.83)`, `R^2 = 0.884`
- the joint Born / interference / decoherence companion stays extremely close
  to the exact grid:
  - exact grid: Born `2.12e-15`, `d_TV = 0.787`, `MI = 0.568`,
    decoherence `49.4%`
  - grown geometry: Born `2.19e-15`, `d_TV = 0.811`, `MI = 0.569`,
    decoherence `49.4%`

The safe combined statement is:

- on the retained moderate-drift `h = 0.5` generated-geometry family, the
  fixed-lattice far-field harness signature transfers well enough to count
  as a real bounded numerical positive on the declared rows
- near-field rows, the broader generated-geometry parameter space, and the
  primitive-to-physical-gravity bridge all remain open, so this still does
  **not** close full Gate B

## One-step h = 0.25 scaling companion

A bounded moderate-drift replay on the same generated-geometry family now
survives one refinement step to `h = 0.25`.

Read it through:

- `docs/GATE_B_H025_FARFIELD_NOTE.md` (sibling refinement artifact;
  cross-reference only — not a one-hop dep of this note)
- `docs/GATE_B_H025_DISTANCE_LAW_NOTE.md` (sibling refinement artifact;
  cross-reference only — not a one-hop dep of this note)
- `docs/GATE_B_H025_JOINT_PACKAGE_NOTE.md` (sibling refinement artifact;
  cross-reference only — not a one-hop dep of this note)

Safe read:

- this upgrades the bounded numerical result from a coarse-family far-field
  positive to a one-step refinement-stable positive on the same moderate-drift
  family, under the same admitted-context ingredients
- it still does **not** close full Gate B (the primitive-to-physical-gravity
  bridge remains the upstream blocker)

## Repair target for full Gate B closure (D-class gap, deferred)

To promote this row past `audited_conditional`, an upstream theorem is
needed that derives the source law, the propagation/readout map, and the
far-field Gate B criterion from accepted primitives — with a runner that
*constructs* rather than *assumes* that bridge. That theorem does not exist
on `main` today; it is recorded here as a real D-class derivation gap, not
an import-redirect. Until it lands, this row remains a bounded numerical
harness statement on the runner-defined family.
