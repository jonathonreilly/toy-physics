# Planck-Scale Derivation Program

**Date:** 2026-04-23  
**Status:** science-program / package-boundary audit
**Primary audit runner:** `scripts/frontier_planck_scale_program_audit.py`

## Verdict

Opening audit verdict, before the later direct route:

On the then-current accepted package surface, the repo did **not** derive the
absolute lattice spacing `a` or the Planck identification

`a^(-1) = M_Pl`.

The present package can derive lattice-unit or dimensionless objects such as

`a v = (7/8)^(1/4) * alpha_LM^16`

and gravity normalization in lattice units such as

`G_N = 1/(4 pi)`,

but it still needs one physical unit map to convert those results into SI/GeV.

The branch-local status after the later direct route is sharper:

- on the authorized one-axiom information / Hilbert / locality semantics
  surface, the direct finite-cell route derives `a = l_P`;
- the result should still not be stated as an unqualified theorem of the older
  minimal ledger alone.

## Current Canonical Direct Route

The current strongest surviving exact route is no longer best described by the
older "boundary pressure" language.

The direct branch-local entrypoint is now:

- [PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md](./PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md)
- [PLANCK_SCALE_ONE_AXIOM_CONSERVATIVE_SEMANTICS_BRIDGE_THEOREM_2026-04-23.md](./PLANCK_SCALE_ONE_AXIOM_CONSERVATIVE_SEMANTICS_BRIDGE_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_THEOREM_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_NATIVE_STOP_CONDITIONS_AUDIT_2026-04-23.md](./PLANCK_SCALE_NATIVE_STOP_CONDITIONS_AUDIT_2026-04-23.md)

That note reformulates the surviving Planck lane as a direct finite-cell
coefficient chain:

1. exact time-locked local cell `C^16`;
2. exact minimal one-step worldtube packet `P_A`;
3. on the authorized one-axiom semantics surface, the physical primitive cell
   carries the source-free default datum
   `rho_cell = I_16 / 16`;
4. exact worldtube-packet coefficient

   `c_wt = Tr(rho_cell P_A) = 1/4`;

5. direct worldtube-to-boundary counting is already closed:

   `c_cell(rho) = Tr(rho P_A)`;

6. so the remaining package-boundary statement is:

   the one-axiom information / Hilbert / locality surface is authorized as
   conservative local state semantics for this lane.

So the direct route is no longer primarily a search for the right scalar
"pressure." The remaining question is whether the physical primitive cell has a
canonical source-free default datum and, if so, whether that datum is the
tracial state.

After the one-axiom conservative semantics bridge, the route closes on that
authorized semantic surface. It should still not be presented as an
unqualified theorem of the older minimal ledger alone.

The older scalar Schur/free-energy notes remain useful as negative controls,
but they should now be read as historical exploratory packaging rather than the
cleanest canonical statement of the surviving route.

## Active Theorem Lanes

This branch opens the Planck-derivation question as three parallel theorem
lanes with one canonical entrypoint and disjoint science-only work products.

### Lane 1: Gravity/action unit-map theorem

Primary target:

> derive or sharply narrow the missing physical unit map between the retained
> discrete gravity/action stack and the textbook Einstein-Hilbert family.

Branch-local work products:

- `docs/PLANCK_SCALE_GRAVITY_ACTION_UNIT_MAP_LANE_2026-04-23.md`
- `scripts/frontier_planck_gravity_action_unit_map_lane.py`

### Lane 2: Horizon entropy coefficient theorem or no-go

Primary target:

> either find a framework-native horizon carrier with exact `1/4` coefficient
> or prove a broader no-go for the admitted carrier class.

Branch-local work products:

- `docs/PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md`
- `scripts/frontier_planck_horizon_entropy_lane.py`

### Lane 3: One-axiom information/action quantum theorem

Primary target:

> determine whether the irreducible information-flow object can carry the
> missing physical unit map, or else produce a clean obstruction.

Branch-local work products:

- `docs/PLANCK_SCALE_INFORMATION_ACTION_QUANTUM_LANE_2026-04-23.md`
- `scripts/frontier_planck_information_action_quantum_lane.py`

## Physical-Lattice Update

Once the lattice is taken as physical, the direct route sharpens materially.

The exact time-locked `C^16` block is no longer just a convenient support
carrier. It is the primitive local physical cell. That resolves the old object
ambiguity and makes the remaining issue much narrower:

- not "is there really a cell to attach a state to?"
- but "what is the source-free default datum of that real primitive cell?"

The current branch answer is:

- counting side: closed;
- factor-of-two / packet lift: closed;
- local object: anchored;
- generic reduced-vacuum reclassification: boxed out as the wrong object class;
- only live issue: source-free default-datum semantics on the physical cell.

## Review Bar

These lanes are only worth promoting if they improve the current package
boundary honestly. For each lane, the acceptable outcomes are:

- a retained no-import theorem candidate;
- a sharp impossibility/no-go that rules out the lane cleanly;
- or a precise reduction that shows why `a^(-1) = M_Pl` should remain a pinned
  observable rather than a derived scale.

## Current Lane Results

After opening the three theorem targets as explicit branch-local lanes, the
current honest read is:

- **Lane 1: gravity/action unit-map** remains the only serious live derivation
  route, but it is still a pinned-observable lane on current evidence. The
  current admitted family now carries a sharper scale-ray no-go: it fixes a
  positive unit ray rather than an absolute anchor; see
  [PLANCK_SCALE_GRAVITY_ACTION_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_GRAVITY_ACTION_UNIT_MAP_LANE_2026-04-23.md)
  and
  [PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md).
- **Lane 2: horizon entropy** closes to a sharper no-go on the current
  admissible carrier family: the retained class is Widom-class, not exact
  `1/4` class; see
  [PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md](./PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md).
- **Lane 3: information/action quantum** remains structurally suggestive but
  still speculative/open; no retained theorem yet converts that object into
  the missing physical unit map; see
  [PLANCK_SCALE_INFORMATION_ACTION_QUANTUM_LANE_2026-04-23.md](./PLANCK_SCALE_INFORMATION_ACTION_QUANTUM_LANE_2026-04-23.md).

So the branch-level program verdict is now sharper than the opening audit:

- the best live route is still the gravity/action unit-map theorem, but the
  current admitted family alone cannot close it because it is homogeneous
  along a positive scale ray;
- the current horizon-entropy carrier family should be treated as ruled out
  for exact `1/4`;
- the information/action route is a future bridge candidate, not a current
  closure theorem.
- the current same-surface candidate menu is now explicitly exhausted by
  [PLANCK_SCALE_UNIT_BEARING_CANDIDATE_CLASSIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIT_BEARING_CANDIDATE_CLASSIFICATION_THEOREM_2026-04-23.md):
  any future no-import Planck derivation must add a new unit-bearing
  observable, with the strongest surviving theorem classes now narrowed to
  boundary-density and per-cell action/information-quantum routes.
- the first-principles action route is now also reduced sharply by
  [PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md](./PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md):
  bare `Cl(3)` on `Z^3` points naturally to a Planck-order elementary cell,
  but exact `a = l_P` lives or dies on one elementary coefficient theorem
  `a^2 / l_P^2 = 8 pi q_* / eps_*` on a minimal plaquette/hinge process.
- the same-defect linear holonomy subclass is now reduced further by
  [PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md):
  if the elementary action phase is read linearly from a resolved `Spin(3)`
  holonomy weight on that same defect, then
  `a^2 / l_P^2 = 8 pi |m|` with `m in (1/2) Z`, so exact conventional
  `a = l_P` is impossible on that whole class and the minimal spinorial
  coefficient is the exact rationalized value `a^2 / l_P^2 = 4 pi`.
- the canonical gauge-invariant same-defect holonomy scalar is now also
  narrowed by
  [PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md):
  on the minimal cubical defect `eps = pi/2`, the normalized
  `Spin(3)` character-deficit class has exact floor
  `a^2 / l_P^2 = 16 - 8 sqrt(2) ~= 4.68629`, so even that canonical
  gauge-invariant local holonomy class cannot force exact conventional
  `a = l_P`.

## Current Repo Facts

The current load-bearing facts are:

1. **Hierarchy route stops at a lattice-unit object.**  
   The current hierarchy formulas can fix a lattice-unit or dimensionless
   quantity, but they still need an external identification to turn that into
   an absolute GeV scale. That obstruction is reproduced directly by the audit
   runner `scripts/frontier_planck_scale_program_audit.py`.

2. **Gravity route stops at lattice units.**  
   [GRAVITY_CLEAN_DERIVATION_NOTE.md](./GRAVITY_CLEAN_DERIVATION_NOTE.md)
   derives `G_N = 1/(4 pi)` in lattice units, but says SI conversion still
   requires one physical calibration.

3. **Action normalization still consumes observation at the last step.**  
   [ACTION_NORMALIZATION_NOTE.md](./ACTION_NORMALIZATION_NOTE.md)
   fixes the dimensionless action coefficient only after defining `G` from
   observation.

4. **Current entropy carrier does not land the Planck coefficient.**  
   [BH_ENTROPY_DERIVED_NOTE.md](./BH_ENTROPY_DERIVED_NOTE.md) and the retained
   no-go theorem behind it say the current free-fermion entanglement carrier
   asymptotes to `1/6`, not the black-hole coefficient `1/4`.

5. **The old vacuum-energy route is not the right mechanism.**  
   [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](./COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
   explicitly says the positive cosmology surface is the `S^3` spectral-gap
   route, not a UV vacuum-energy sum that would back out the lattice spacing.

## Candidate Routes

### Route A: Hierarchy-to-Planck closure

Goal:

> derive the absolute scale `a^(-1)` from the hierarchy lane itself.

Current status:

- **blocked on a clean obstruction**
- the accepted hierarchy theorem is only `a v`
- no current theorem fixes `a` from the hierarchy chain

Decision:

- do **not** spend more time rearranging the same hierarchy formulas
- this route should only be reopened if a genuinely new absolute-scale theorem
  appears

### Route B: Gravity / action unit-map theorem

Goal:

> derive the physical unit map between the discrete gravitational action and
> the textbook Einstein-Hilbert normalization without importing measured `G`
> or `M_Pl`.

Current status:

- **best open route**
- not closed
- not globally blocked by a retained no-go, but the current admitted family
  now has a scale-ray no-go and therefore cannot finish the job by itself

Why this is the best candidate:

- the gravity stack already derives the right dimensionless structure
- the remaining gap is exactly the missing physical unit map
- the new scale-ray theorem clarifies the real target: add one genuinely
  non-homogeneous unit-bearing same-surface observable
- if this route lands, it should also clean up hierarchy, EW, Higgs, and any
  other GeV-valued lane at once

Load-bearing notes:

- [GRAVITY_CLEAN_DERIVATION_NOTE.md](./GRAVITY_CLEAN_DERIVATION_NOTE.md)
- [ACTION_NORMALIZATION_NOTE.md](./ACTION_NORMALIZATION_NOTE.md)
- [UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md](./UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md)
- [PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md)

### Route B2: Same-defect `Spin(3)` holonomy coefficient

Goal:

> test whether the exact coefficient could come from the actual elementary
> curvature holonomy on the same plaquette/hinge process.

Current status:

- **reduced / no-go for the linear resolved-weight class**
- minimal same-process spinorial candidate lands `a^2 / l_P^2 = 4 pi`
- exact conventional `a = l_P` is impossible on that class
- the canonical gauge-invariant character-deficit class on the minimal cubical
  defect also misses exact Planck, with exact floor
  `a^2 / l_P^2 = 16 - 8 sqrt(2)`

Decision:

- do **not** keep chasing linear resolved-weight holonomy as the exact Planck
  law
- if a holonomy route survives, it must be nonlinear or use a different
  carrier/readout than a resolved `Spin(3)` weight angle

Load-bearing note:

- [PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md)

### Route C: Horizon entropy / area-law theorem

Goal:

> derive the exact black-hole coefficient `1/4` from a discrete horizon entropy
> carrier and thereby identify the physical cell size with `l_P`.

Current status:

- **blocked on the current carrier**
- the current free-fermion entanglement carrier gives `1/6`, not `1/4`

Decision:

- current carrier is a no-go
- the only way this route survives is to find a genuinely different horizon
  entropy carrier, not to keep reusing the current Widom asymptote

Load-bearing note:

- [BH_ENTROPY_DERIVED_NOTE.md](./BH_ENTROPY_DERIVED_NOTE.md)

### Route D: Vacuum-energy / cosmological-constant spacing derivation

Goal:

> derive `a` from a UV vacuum-energy sum or cosmological constant scaling.

Current status:

- **wrong mechanism on the current repo read**
- the positive cosmology lane is IR/geometric (`S^3` spectral gap), not a UV
  spacing derivation

Decision:

- do not promote this route as the main Planck derivation program

Load-bearing note:

- [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](./COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)

### Route E: One-axiom information / action quantum route

Goal:

> show that the irreducible graph-unitary / information-flow object carries one
> fundamental action or information quantum per elementary cell, and then tie
> that quantum to the gravity/action normalization or horizon area density.

Current status:

- **open and speculative**
- no retained theorem yet ties conserved information flow to a physical unit
  map or to the `1/4` horizon coefficient

Why it matters:

- if a no-import derivation exists at all, it likely needs a genuinely
  framework-native source of physical units
- this is the one route in the repo that plausibly could supply such a source

Load-bearing note:

- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)

### Route F: Compact-object / discrete horizon counting

Goal:

> derive a horizon-area cell law or minimal radius theorem from the exact
> compact-object side and use that to fix the physical spacing.

Current status:

- **open but immature**
- existing compact-object and echo notes still either assume `a = l_Planck`
  or leave the decisive astrophysical exponent conditional

Load-bearing note:

- [EVANESCENT_BARRIER_AMPLITUDE_SUPPRESSION_THEOREM_NOTE.md](./EVANESCENT_BARRIER_AMPLITUDE_SUPPRESSION_THEOREM_NOTE.md)

## Program Order

If we actually want a no-import Planck derivation, the program order should be:

1. **Primary theorem target:** gravity/action unit-map theorem  
   Derive the physical unit conversion from the accepted gravity/QG stack
   itself.

2. **Secondary theorem target:** new horizon entropy carrier  
   Either derive the exact `1/4` coefficient on a new carrier or prove a
   broader no-go.

3. **Bridge theorem target:** one-axiom information/action quantum  
   Tie the elementary graph-unitary object to one irreducible action or
   entropy quantum.

4. **Compact-object follow-on:** discrete horizon counting / minimal-radius
   theorem  
   Use this only if the earlier steps begin to land.

## Concrete Theorem Targets

The program becomes real only if we phrase it as theorem work, not just a wish
list. The best concrete targets are:

### Target 1: Gravity/action unit-map uniqueness theorem

Candidate statement:

> the accepted discrete gravitational bilinear/action family admits a unique
> physical unit map to the canonical Einstein-Hilbert-style action family,
> with no external `G`, `M_Pl`, or `l_P` input.

What it would need:

- one dimensionless normalization already supplied by the gravity stack;
- one internal criterion replacing the current observational SI calibration;
- a proof that any alternative unit map either breaks the accepted gravity
  action equivalence or introduces an external scale by hand.

Why it matters:

- if this lands, the Planck scale should fall out once for the whole repo, not
  lane by lane.

### Target 2: Horizon entropy coefficient theorem or no-go

Candidate statement:

> there exists a framework-native horizon entropy carrier whose asymptotic
> coefficient is exactly `1/4`, or else every admitted carrier in a defined
> class misses `1/4`.

What it would need:

- a new carrier beyond the current free-fermion Widom one;
- a precise admissible-carrier class;
- either an exact `1/4` theorem or a broader impossibility theorem.

Why it matters:

- this is the cleanest route to tying a microscopic cell size to Planck area.

### Target 3: One-axiom information/action quantum theorem

Candidate statement:

> the irreducible graph-unitary / conserved-information-flow object carries one
> exact action or entropy quantum per elementary cell, and that quantum fixes
> the physical unit map on the gravity side.

What it would need:

- a precise action or information density attached to the elementary carrier;
- a bridge from that density to geometric action or horizon area;
- no observational normalization at the last step.

Why it matters:

- this is the only clearly framework-native source of physical units visible in
  the current one-axiom notes.

## Go / No-Go Criteria

We should say the Planck scale is **derived** only if one of the following is
proved without observed `G`, `M_Pl`, or `l_P` imports:

1. an exact gravity/action theorem that fixes the physical unit map;
2. an exact horizon entropy theorem that lands the coefficient `1/4`;
3. an exact information/action-quantum theorem that forces one cell to carry
   the Planck unit.

If none of those lands, the package should instead say:

> `a^(-1) = M_Pl` is a pinned observable / framework scale, and all absolute
> GeV or meter rows consuming it are calibrated companions rather than
> no-import derivations.

## Current Package Recommendation

Current honest package boundary:

- retain lattice-unit / dimensionless theorems such as `a v`
- treat `a^(-1) = M_Pl` as a pinned observable
- mark every absolute GeV or meter row consuming it as calibrated / companion
- keep the Planck-derivation program as a separate open science target rather
  than silently folding it into existing retained rows

## Bottom Line

The current repo does **not** have a hidden near-finished derivation of
`a = l_Planck`.

The strongest available next move is:

> attack the gravity/action unit-map problem directly.

If that does not move, the right package posture is not to keep pretending the
derivation is one theorem away everywhere. It is to pin `a^(-1) = M_Pl`
openly and keep the derivation program separate.
