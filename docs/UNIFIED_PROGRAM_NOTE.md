# Unified Program Note

**Date:** 2026-04-04  
**Status:** canonical project-state and backlog note for the retained symmetry program

## One-line read

The project now has a single coherent direction:

- **symmetry-protected hard geometry with the standard linear propagator**

That is the architecture family that survives the corrected Born checks, keeps
positive gravity, and retains nontrivial decoherence / which-slit structure on
the same graphs.

## Canonical retained lanes

### 1. Flagship lane: exact mirror / `Z2`

This is the main synthesis headline.

- Born-clean at machine precision
- gravity-positive on the retained window
- nontrivial decoherence / slit separation
- retained through `N = 100`
- gravity wall at `N = 120`

Primary artifacts:

- [`docs/MIRROR_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_CHOKEPOINT_NOTE.md)
- [`docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md)

### 2. Clean validation card: exact 2D mirror

This is the cleanest low-dimensional same-family card.

Strongest retained row:

- `N = 60`
- `MI = 0.756118`
- `1 - pur_min = 0.4420`
- `d_TV = 0.8572`
- gravity `+2.5687`
- Born `1.08e-15`
- `k=0 = 0.00e+00`

Primary artifact:

- [`docs/MIRROR_2D_VALIDATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_2D_VALIDATION_NOTE.md)

### 3. Range / decoherence extension: `Z2 x Z2`

This is the strongest higher-symmetry extension.

- Born-clean at machine precision
- gravity-positive on the retained dense probe
- stronger decoherence and longer retained range than exact mirror
- retained through `N = 120`

Primary artifact:

- [`docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md)

### 4. Head-to-head result

The clean tradeoff is now frozen:

- **exact mirror** is the better **joint coexistence** lane
- **`Z2 x Z2`** is the better **decoherence / range** lane

Primary artifact:

- [`docs/SYMMETRY_HEAD_TO_HEAD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SYMMETRY_HEAD_TO_HEAD_NOTE.md)

## What is not retained as a core lane

### Structured mirror growth

This is the most important negative result from the recent audit pass.

- the geometry idea is physically interesting
- but the canonical linear validator is not Born-clean
- the dedicated linear scan found no review-safe Born-clean pocket

Primary artifacts:

- [`docs/STRUCTURED_MIRROR_RECONCILIATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/STRUCTURED_MIRROR_RECONCILIATION_NOTE.md)
- [`docs/STRUCTURED_MIRROR_BORNSAFE_SCAN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/STRUCTURED_MIRROR_BORNSAFE_SCAN_NOTE.md)

So structured mirror is currently:

- **interesting geometry result**
- **not a retained flagship architecture**

### Structured chokepoint bridge

This is the most important recent generated-symmetry reopening.

- structured placement now survives the canonical mirror-harness readout on a
  narrow retained slice
- Born stays machine-clean
- `k=0` stays at zero
- gravity stays positive on the retained rows
- decoherence remains below the ceiling on the largest retained row

Primary artifact:

- [`docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md)

So the safe read is:

- **generated symmetry is no longer purely negative/open**
- **the reopened bridge is bounded, not solved**

### Action-power branch

This is an explicit **axiom fork**, not an extension of the spent-delay
flagship.

- the same-harness 2D comparison is real
- the 3D close-slit barrier card is now retained for Born / MI / decoherence
- the 3D no-barrier distance / mass-response companion is retained
- the current ordered 3D barrier lane now has a bounded negative on attraction:
  weakening the field, densifying forward connectivity, and adding geometric
  jitter all still leave the sign away from mass on the tested slices
- no flagship claims are inherited automatically

Primary artifacts:

- [`docs/ACTION_POWER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ACTION_POWER_NOTE.md)
- [`docs/ACTION_POWER_3D_GRAVITY_SIGN_CLOSURE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ACTION_POWER_3D_GRAVITY_SIGN_CLOSURE_NOTE.md)

### Engineered non-symmetry lanes

Dense central-band + layer norm remains the strongest engineered benchmark
outside the symmetry program, but it is no longer the center of gravity of the
project.

## Bridge-objective scorecard

| objective | current status | retained read |
|---|---|---|
| Born / pairwise interference | **strong** | exact mirror, exact 2D mirror, and `Z2 x Z2` are machine-clean on retained harnesses |
| Interference + which-slit structure | **strong** | exact mirror and exact 2D mirror retain large `d_TV` / MI advantages over matched random baselines |
| Gravity-like phase signal | **strong** | retained positive gravity on the exact mirror and exact 2D mirror families |
| `k=0` control | **strong** | retained symmetry lanes keep `k=0` at zero |
| Joint coexistence on one architecture | **strong** | exact mirror is the flagship same-graph coexistence lane |
| Slower decoherence washout | **strong but bounded** | exact mirror and `Z2 x Z2` clearly soften the ceiling, but the clean retained claim is bounded-window retention rather than a finished asymptotic theorem |
| Mass-law quality | **weak / bounded** | positive fitted windows exist, but no flagship symmetry lane has a promoted clean mass law |
| Distance-law quality | **negative structural result** | current connected random/symmetry architecture does not retain a review-safe `1/b`-style law |
| Continuum / refinement bridge | **promising but bounded** | raw NN is Born-clean through `h = 0.25`; deterministic rescale extends to `h = 0.0625`; RG-style gravity remains open |
| Generated / emergent symmetry | **reopened / bounded** | structured chokepoint bridge is retained on a narrow canonical slice, but no broad generated successor is promoted |

## Distance-law closure

The recent gravity-side closure matters for the roadmap.

Across the latest field-shape, coupling, scattering, focused-beam, and
waveguide-style probes, the distance-law problem now has a much cleaner read:

- the issue is **not** just that the retained `1/r` field is too shallow
- the issue is **not** fixed by `1/r^2`, localized kernels, or weaker coupling
- the issue is **not** fixed by simple focused-slit or waveguide-style tweaks

The best current mechanism reading is:

- amplitude spreads transversely across connected DAGs like a random walk
- that destroys sustained beam confinement in the mass direction
- without confinement, the current architecture gives a topological / flat
  gravity response rather than a clean geometric `1/b` law

So the project should treat distance law on the current flagship family as:

- **closed negative inside the current connected symmetry architecture**
- **open only under a different architecture class**, such as ordered /
  lattice-like transport or another beam-confining geometry

Useful references:

- [`docs/B_INDEPENDENCE_MECHANISM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/B_INDEPENDENCE_MECHANISM_NOTE.md)
- [`docs/MIRROR_2D_GRAVITY_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_2D_GRAVITY_LAW_NOTE.md)

### Ordered-lattice reopening

Recent lattice work changes the roadmap without changing the flagship story.

- the committed lattice-mirror script already shows a real
  **distance-dependent** effect with sign change and decaying far-field
  magnitude on a regular ordered graph:
  [`scripts/lattice_mirror_distance.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_mirror_distance.py)
- this supports the beam-confinement / ordered-transport explanation for why
  the random-connected symmetry lanes fail to retain a clean distance law

That stronger no-barrier lattice branch is now frozen in:

- [`docs/LATTICE_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_DISTANCE_LAW_NOTE.md)
- [`docs/LATTICE_FAMILY_VALIDATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_FAMILY_VALIDATION_NOTE.md)
- [`docs/LATTICE_SYMMETRY_UNIFICATION_DECISION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_SYMMETRY_UNIFICATION_DECISION_NOTE.md)
- [`docs/LATTICE_FIELD_STRENGTH_UNIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_FIELD_STRENGTH_UNIFICATION_NOTE.md)

The retained ordered-lattice read at the original standard-strength slice is:

- `|delta| ~= 23.5071 * b^(-1.052)`
- `R^2 = 0.9850`
- `k=0 = 0`
- barrier-lattice coexistence card at `N=40`:
  - `MI = 0.537`
  - `1 - pur_cl = 0.057`
  - `d_TV = 0.714`
  - gravity `-5.740`
  - Born `2.98e-16`

### Ordered-lattice weak-field reopening

The standard-strength one-harness decision is still a real negative result:

- the same-card gravity sign does not turn attractive on that fixed slice

But the ordered-lattice branch now also has a **narrow weak-field retained
pocket** on the same family:

- `max_dy = 5`
- slit families `narrow_center` or `wide_center`
- strengths `0.0005` to `0.001`

Canonical weak-field row:

- `max_dy = 5`
- `slit = wide_center`
- `strength = 0.0005`
- `MI = 0.617`
- `1 - pur_cl = 0.465`
- gravity at `b = 6`: `+0.163`
- Born companion `4.24e-16`
- `k = 0`
- all tested `b` values gravity-positive
- barrier-harness tail fit: `alpha = -1.00`, `R^2 = 0.93`

So the safe synthesis read is now:

- **distance law remains closed on the flagship connected symmetry family**
- **ordered / lattice geometry is a retained secondary branch for the
  distance-law question**
- **ordered lattice has both:**
  - a standard-strength same-family two-harness bridge
  - a narrow weak-field one-card pocket on the same family
  - a retained weak-field purity-scaling law on that pocket:
    `1 - pur_cl ~= 1.0467 * N^(-0.222)` on the retained rows
- **ordered lattice still does not displace exact mirror as the flagship
  coexistence architecture**

### Ordered-lattice 3D dense spent-delay branch

The ordered-lattice story is now stronger in 3D as well, but still bounded.

The retained dense 3D spent-delay card keeps:

- Born companion audit at machine precision
- `d_TV = 0.3785`
- `MI = 0.1414`
- decoherence `13.5%`
- positive sub-linear mass response: `alpha = 0.34`, `R² = 0.97`
- positive centroid-side distance decay: `b^(-1.62)`, `R² = 0.976`
- gravity-vs-length window that crosses from away to toward on the tested
  `N = 10, 12, 15` slice

The gravity-observable hierarchy matters here:

- `z = 2, 3, 4` are hierarchy-clean attraction
- `z = 5` is mixed / ambiguous

So the honest retained read is:

- **3D dense spent-delay is now a real bounded same-family branch**
- **it strengthens the ordered-lattice program**
- **it does not replace mirror as the flagship**
- **it is still safer to describe as a bounded attractive window than as a
  fully solved 3D theorem**

Primary artifact:

- [`docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md)

### Nearest-neighbor refinement

The nearest-neighbor lattice is now the cleanest refinement-side branch.

- raw NN refinement is Born-clean through `h = 0.25`
- deterministic rescale extends the Born-clean window to `h = 0.0625`
- MI, `1-pur_cl`, and `d_TV` converge smoothly under that deterministic
  schedule
- gravity remains positive but fades toward zero under finer refinement

This is a real refinement branch, but it is still a **bounded** one:

- the raw kernel overflows at `h = 0.125`
- RG-style strength scalings are suggestive but still ambiguous
- a finished continuum / renormalization theorem is not retained yet
- `k=0 = 0` on this branch should be read as a sanity property of the pure
  phase coupling path, not as strong independent evidence by itself

## Single unified approach

The project no longer needs to choose between many competing stories.

The retained program is:

1. **Use exact imposed symmetry as the main architecture**
2. **Use exact mirror as the flagship lane**
3. **Use exact 2D mirror as the clean validation card**
4. **Use `Z2 x Z2` as the stronger decoherence / retained-range extension**
5. **Use raw nearest-neighbor refinement as the current continuum-side bridge**
6. **Treat generated symmetry as a reopened but bounded bridge problem, not as a solved lane**

## Highest-value next wins

For short-horizon worker execution, use
[`docs/OVERNIGHT_WORK_BACKLOG.md`](/Users/jonreilly/Projects/Physics/docs/OVERNIGHT_WORK_BACKLOG.md)
as the concrete task queue. The priorities below remain the canonical
program-level roadmap.

### Priority 1. Flagship synthesis card

Produce one compact repo-facing card for:

- exact mirror
- exact 2D mirror
- `Z2 x Z2`
- structured mirror as the negative/open successor

Goal:

- make the flagship story impossible to misread

### Priority 2. Symmetry mechanism note

Turn the current intuition into a tighter mechanism statement:

- why exact symmetry preserves sectors
- why that slows rank-1 convergence
- why `Z2 x Z2` improves the decoherence side further

Goal:

- move the symmetry story from “good empirical architecture” toward “clear
  transfer-product mechanism”

### Priority 3. Generated-symmetry bridge

This is the highest-value open science problem.

Question:

- can a local growth rule generate exact-enough symmetry while staying
  Born-clean on the canonical harness?

Goal:

- upgrade the program from **imposed symmetry** to **generated symmetry**

### Priority 4. Flagship gravity-law clarification

Do not keep trying to rescue the distance law inside the current connected
symmetry architecture.

Instead:

- either close the mass-law question narrowly on the flagship lane
- or document cleanly that the flagship lane is a coexistence architecture,
  not a law-quality gravity architecture

### Priority 5. Ordered-lattice branch

The recent lattice result means this is no longer just a hypothetical future
branch. It is now the main secondary frontier if distance law remains a key
bridge objective.

Immediate goal:

- reconcile the sign-changing barrier lattice result with the retained
  no-barrier `|delta| ~ 1/b` branch
- decide whether the ordered branch can inherit enough symmetry structure to
  unify distance law with the flagship coexistence story

Longer-term goal:

- test whether an ordered / lattice-like geometry can inherit enough of the
  symmetry program to become a true extension rather than a separate side
  branch

This branch is still architecturally separate from the current flagship:

- ordered / lattice-like transport
- beam-confining waveguide or crystal geometry
- another architecture where transverse spreading is suppressed by design

This should still be treated as a **next-generation architecture**, not as a
tweak to the current exact-mirror program.

## Bottom line

The project now has a real unified core:

- **exact symmetry-protected linear graph physics**

Within that core:

- **exact mirror** is the flagship
- **exact 2D mirror** is the cleanest validation card
- **`Z2 x Z2`** is the best extension
- **structured/grown symmetry** is still the main unsolved bridge
- **distance law** is no longer an active tweak problem on the current
  architecture; it is a separate architecture problem
