# PMNS Selector Three-Identity Support Proposal

**Date:** 2026-04-21
**Status:** support proposal on the current affine Hermitian chart. This is
not a retained closure claim.

## What this package does

This package records a compact proposed law on the affine Hermitian PMNS chart

```text
H(m, delta, q_+) = H_base + m T_M + delta T_Delta + q_+ T_Q
```

using the three equations

```text
Tr(H)       = Q_Koide = 2/3
delta * q_+ = Q_Koide = 2/3
det(H)      = E2 = sqrt(8)/3
```

On the current active-chamber working surface, the system solves numerically to

```text
(m, delta, q_+) = (2/3, 0.9330511..., 0.7145018...)
```

and the resulting PMNS observables are

```text
sin^2(theta_12) = 0.306178
sin^2(theta_13) = 0.022139
sin^2(theta_23) = 0.543623
sin(delta_CP)   = -0.990477
|Jarlskog|      = 0.033084
```

All three angles lie within the current NuFit 5.3 normal-ordering `1 sigma`
bands used by the runner.

## What this package does not do

This package does not promote the PMNS selector gate to retained closure.

Open scientific obligations remain:

1. Derive `delta * q_+ = Q_Koide` from retained framework structure rather than
   proposing it as a candidate selector law.
2. Derive `det(H) = E2` from retained framework structure rather than proposing
   it as a candidate selector law.
3. Replace the current numerical multi-start uniqueness evidence with a
   theorem-grade uniqueness argument on the relevant basin.
4. Keep the broader PMNS/DM gate honest: this proposal lives on the current
   active-chamber working surface and does not by itself settle the remaining
   source-sheet / selector-side open structure elsewhere in the package.

## Why it is still worth keeping

Even with those gaps, the proposal is still useful support:

- it gives a very small candidate law on the existing affine Hermitian chart;
- it ties two of the proposed equations directly to the already-supported Koide
  scalar `Q = 2/3`;
- it produces a concrete interior chamber point rather than a diffuse family;
- and it gives a falsifiable PMNS prediction packet already close to the
  measured values.

So the right reading is:

```text
interesting candidate point-selection law
!= retained theorem-grade closure
```

## Artifacts

- [PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md](/Users/jonreilly/Projects/Physics/docs/PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md)
- [frontier_pmns_selector_three_identity_support_2026_04_21.py](/Users/jonreilly/Projects/Physics/scripts/frontier_pmns_selector_three_identity_support_2026_04_21.py)

## Validation instructions

1. Read the note for the exact retained-vs-proposed boundary.
2. Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_selector_three_identity_support_2026_04_21.py
```

3. Confirm the runner only claims:
   - exact atlas/scalar identities already present on the chart,
   - a numerical solution of the proposed three-equation system,
   - numerical PMNS agreement at that solution,
   - and heuristic one-cluster evidence from the audited start box.

## Bottom line

This is a clean support proposal worth keeping in the PMNS support package
while the remaining closure obligations are worked in parallel.
