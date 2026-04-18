# Perron-Frobenius Wilson Dependency Audit

**Date:** 2026-04-18  
**Status:** exact science-only audit of which current PF-branch statements
depend on Wilson robustness, and which current-bank blockers remain even if the
Wilson-positive route is reopened or weakened  
**Script:** `scripts/frontier_perron_frobenius_wilson_dependency_audit_2026_04_18.py`

## Question

If the Wilson foundation is re-examined, which parts of the current
Perron-Frobenius branch actually depend on Wilson robustness, and which parts
already remain exact current-bank blockers independently of any positive Wilson
bridge?

## Bottom line

Wilson robustness matters **asymmetrically**.

What depends directly on Wilson robustness:

1. the Wilson one-clock positive parent object on the gauge surface;
2. the Wilson parent/compression theorem that links that parent object to the
   plaquette and `theta` descendants;
3. the entire positive step-2 Wilson source route, now sharpened to the local
   path-algebra target
   `Phi_chain : A_chain -> End(H_W)` on one physical adjacent two-edge chain.

What does **not** become positive merely by reopening Wilson:

1. the strongest canonical sole-axiom `hw=1` PMNS pack still remains trivial;
2. the PMNS-native fixed-slice two-holonomy theorem is a readout theorem, not a
   production theorem, and it explicitly uses no external Wilson or plaquette
   input;
3. the plaquette lane still has exact current-bank nonclosure theorems for
   framework-point beta data, including no finite sample-packet closure and no
   propagated-triple closure of the reduced cyclic bulk object.

So Wilson is the branch's main **positive reopening lever**, but not the only
load-bearing blocker on the branch.

## Exact Wilson-dependent surfaces

### 1. Step 1 is currently exact only on the Wilson gauge surface

From
[GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md):

- the retained Wilson surface already has one exact positive one-clock parent
  object;
- the plaquette source-sector law and the strong-CP `theta` law are already
  canonical descendants of that same Wilson parent object.

From
[PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md):

- step 1 is exact on the Wilson gauge surface,
- but not yet globally across the live retained sectors.

So if Wilson parent robustness changes, the exact step-1 surface must be
re-audited before any positive global PF-selector route remains honest.

### 2. The sharpened positive Wilson route is entirely Wilson-source-side

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md):

- the sharpest Wilson local constructive primitive is already exactly
  `Phi_chain : A_chain -> End(H_W)`.

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md):

- the whole Wilson compressed route is now exactly one minimal local
  path-algebra `2-edge + 3` certificate.

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-18.md):

- the current bank still does **not** realize that sharpest local Wilson
  algebra object.

So the branch's strongest remaining **positive** PF route is Wilson-dependent at
its sharpest local constructive layer.

### 3. Plaquette operator identifications also use Wilson structure

From
[GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_ONE_SLAB_ORTHOGONAL_KERNEL_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_ONE_SLAB_ORTHOGONAL_KERNEL_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md):

- `K_beta^env` is fixed as one exact Wilson/Haar one-slab integral.

From
[GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md):

- `B_beta(W)` is fixed as one exact local Wilson/Haar rim integral.

So the **positive operator interpretation** of the plaquette lane is also tied
to Wilson robustness.

## Exact current-bank blockers that do not become positive merely by reopening Wilson

### 1. The PMNS sole-axiom pack is still trivial

From
[PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md):

- the strongest canonical sole-axiom `hw=1` source/transfer pack still remains
  trivial, with derived active/passive blocks exactly `(I3, I3)`.

So a Wilson reopening does not by itself remove the PMNS-side nontrivial-pack
blocker.

### 2. PMNS-native readout is Wilson-free, but still only readout

From
[PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md):

- fixed `w` plus any two independent native holonomies reconstructs `chi`
  exactly,
- and the note explicitly says no external Wilson or plaquette input is
  involved.

But that same note also says the remaining blocker is production of nonzero
`J_chi = chi`, not readout.

So the PMNS-native lane is already partially independent of Wilson, but it does
not itself close the global PF selector.

### 3. The plaquette lane still has exact nonclosure theorems

From
[GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md):

- no finite marked-holonomy sample packet can by itself determine the full
  beta-side vector `v_6`.

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md):

- even fixed identity rim plus fixed propagated retained triple still does
  **not** determine the reduced cyclic bulk object.

So reopening Wilson does not by itself supply plaquette framework-point closure
either.

## Consequence map for the current PF branch

### Exact statement

The branch currently depends on Wilson robustness in the following exact sense:

- the strongest positive global-PF reopening route is Wilson-dependent;
- the strongest already-landed current-bank blockers are **not** exhausted by
  Wilson alone.

### Inference from the cited notes

If Wilson strengthens, the right reopening point is still the positive Wilson
route:

- one local path-algebra embedding `Phi_chain`,
- then the already isolated `3` scalar spectral identities.

If Wilson weakens, the branch does **not** become more open. Instead:

- the positive Wilson parent/source route must be re-audited,
- while the current negative global reading remains at least as negative,
  because PMNS triviality and plaquette nonclosure are still live blockers on
  the present bank.

This is an inference from the exact notes above, not a new theorem beyond them.

## What this closes

- one exact science-only map of which PF-branch statements are Wilson-dependent
- one exact separation between Wilson-positive reopening surfaces and other
  current-bank blockers
- one review-safe statement of how Wilson re-audit would affect the current PF
  branch

## What this does not close

- a Wilson robustness theorem
- a positive realization of `Phi_chain`
- a positive Wilson-to-PMNS descendant theorem
- plaquette framework-point beta closure
- a positive global sole-axiom PF selector

## Why this matters

This note makes the branch easier to review honestly.

It says the sharper thing:

- Wilson is the main positive reopening lever,
- but Wilson is not the only blocker on the branch,
- so a Wilson re-audit matters most for the **positive** PF route, not for the
  already-landed negative current-stack closure.
