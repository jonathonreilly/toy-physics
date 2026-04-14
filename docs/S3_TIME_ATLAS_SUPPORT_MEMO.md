# Route 2 Atlas Support Memo

**Date:** 2026-04-14  
**Scope:** support rows in the derivation atlas that can plausibly feed the missing Route-2 time-coupling / curvature law

## Verdict

Route 2 is already kinematically clean:

- `S^3` topology is exact
- anomaly-forced time is exact
- the background target is `PL S^3 x R`

The missing object is still the exact **dynamics bridge** from that background to a GR/Regge metric law. The atlas does contain useful reusable machinery for that bridge, but only one part of it is currently exact enough to be primary support.

## Support ranking

### 1. `ANOMALY_FORCES_TIME_THEOREM.md`

**Atlas row:** `Anomaly-forced time`

**Why it matters:** this is the exact time input for Route 2. It fixes the clock direction and removes any ambiguity about whether the route should be built on a single-time `3+1` background.

**Usefulness for the final law:** primary.  
**Claim class:** retained; zero-input structural.

### 2. `OH_SCHUR_BOUNDARY_ACTION_NOTE.md`

**Atlas row:** `Restricted Schur boundary action`

**Why it matters:** this is the exact microscopic boundary Hamiltonian on the current restricted strong-field class. It is the closest exact discrete-action object in the atlas that can be transported slice-by-slice along the Route-2 background.

**Usefulness for the final law:** primary.  
**Claim class:** retained restricted theorem; zero-input structural.

### 3. `OH_STATIC_CONSTRAINT_LIFT_NOTE.md`

**Atlas row:** `Restricted static-constraint lift`

**Why it matters:** this is the exact local `shell -> 3+1` lift on the current bridge surface. It is the cleanest exact local bridge statement in the atlas and is the natural companion to the Schur boundary action.

**Usefulness for the final law:** primary.  
**Claim class:** retained restricted support; zero-input structural.

### 4. `S3_GENERAL_R_DERIVATION_NOTE.md`

**Atlas row:** `S^3` general-`R` extension

**Why it matters:** this gives the exact spatial background family, not just a one-off compactification. Route 2 needs this because the dynamics bridge has to live on a reusable `PL S^3` background, not a single hand-picked size.

**Usefulness for the final law:** primary background support.  
**Claim class:** retained support; zero-input structural.

### 5. `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`

**Atlas row:** `Observable principle`

**Why it matters:** this is the main exact “how to get an action/observable from the axiom” tool in the atlas. It does not itself give Route 2 gravity, but it is the best reusable template if the final bridge is an exact action or exact observable rather than a direct residual fit.

**Usefulness for the final law:** indirect but important.  
**Claim class:** retained; zero-input structural.

### 6. `S3_BOUNDARY_LINK_THEOREM_NOTE.md` and `S3_CAP_UNIQUENESS_NOTE.md`

**Atlas rows:** `S^3 boundary-link theorem`, `S^3 cap uniqueness`

**Why they matter:** these stabilize the Route-2 background choice. They help justify that the kinematic target really is the clean `S^3` compactification family and not a different closure.

**Usefulness for the final law:** background selection only.  
**Claim class:** retained support; zero-input structural.

## Rows that are useful but not bridge-makers

These atlas rows are exact or bounded, but they do not supply the missing Route-2 law:

- `Poisson self-consistency`
- `Newton lattice Green function`
- `WEP / time-dilation corollaries`
- `Generation axiom boundary`
- `Three-generation matter structure`
- `Hierarchy` rows
- `Flavor / Yukawa` rows
- `DM` rows
- `Companion` rows such as graviton mass, decoherence, proton lifetime, Lorentz violation, monopole, and frozen-star echo results

They are legitimate framework tools, but they are not the missing time-coupling / curvature theorem for Route 2.

## Dead ends for the final Route-2 law

### Poisson self-consistency

This is a weak-field fixed-point result. It is not a path to the Route-2 spacetime bridge because it does not supply the exact `PL S^3 x R` dynamics law.

### Newton lattice Green function

This gives inverse-square weak-field behavior. It is useful as a gravity calibration tool, but it does not build the missing time-coupling/curvature law.

### WEP / time-dilation corollaries

These are downstream weak-field consequences of the action. They do not determine the Route-2 dynamics bridge.

### Matter, hierarchy, flavor, DM, and companion lanes

These are all useful framework sectors, but they are orthogonal to the missing Route-2 bridge. They should not be treated as hidden sources of the final gravity law.

## What the final law needs from the atlas

The final Route-2 law would need a combination of atlas tools, not a single row:

1. `S3_GENERAL_R_DERIVATION_NOTE.md` for the exact spatial background family.
2. `ANOMALY_FORCES_TIME_THEOREM.md` for the exact single-clock time factor.
3. `OH_SCHUR_BOUNDARY_ACTION_NOTE.md` for the exact microscopic slice Hamiltonian.
4. `OH_STATIC_CONSTRAINT_LIFT_NOTE.md` for the exact local shell-to-`3+1` lift.
5. `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` if the final bridge is best expressed as an exact action or exact observable.

That combination is enough to support a theorem-grade bridge attempt. It is not yet enough to close the bridge, because the atlas still lacks an exact object that turns the exact slice generator into full GR curvature dynamics.

## Bottom line

The atlas support for Route 2 is real and concentrated:

- exact kinematic background support: yes
- exact boundary-action support: yes
- exact local `3+1` shell lift: yes
- exact dynamics bridge: still missing

So the correct use of the atlas is to build the final law out of:

- `S^3` background
- anomaly-forced time
- Schur boundary action
- static conformal lift
- observable-principle machinery if needed

Everything else is either background-only support or a dead end for the missing Route-2 curvature law.
