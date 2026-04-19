# Neutrino Package Note

**Date:** 2026-04-16  
**Status:** branch package note for the current neutrino lane on `main`-derived
work  
**Scope:** package the current neutrino science without promoting anything into
the atlas

## Bottom line

We now have one **exact post-retained observationally closed lane** on this
branch.

It is **not** the pure-retained lane. The pure-retained sole-axiom neutrino
question is still fully closed **negatively**.

The live positive lane is the exact charged-lepton-active
post-retained `N_e` lane packaged in
[NEUTRINO_POST_RETAINED_FULL_CLOSURE_NOTE_2026-04-16.md](./NEUTRINO_POST_RETAINED_FULL_CLOSURE_NOTE_2026-04-16.md)
and
[frontier_neutrino_post_retained_full_closure.py](../scripts/frontier_neutrino_post_retained_full_closure.py).

That closeout does four things:

1. the PMNS-assisted `N_e` source is fixed by the exact effective-action
   selector on the exact reduced domain
2. the selected `H_e` gives exact `eta/eta_obs = 1` on the favored column
3. the microscopic `D` completion is no longer a live hole, because the
   charged source-response law factors only through the Schur value `H_e`
4. the Majorana bridge is already fixed at
   `k_B = 8`, `k_A = 7`, `eps/B = alpha_LM/2`

What **is** fully closed is the pure-retained sole-axiom neutrino question:

- the exact remaining pure-retained PMNS object is `J_chi`
- the exact remaining pure-retained Majorana object is `mu`
- the exact remaining pure-retained neutrino frontier is therefore `(J_chi, mu)`
- the current pure-retained bank sets that pair to `(0, 0)`

So the pure-retained lane is finished, but it finishes **negatively**.

So the honest package split is now:

- pure-retained neutrino: **fully closed negative**
- live post-retained `N_e` lane: **structurally closed on the exact observational surface**
- pure-retained positive neutrino: **still not available**

## Package split

### 1. Pure-retained closeout

This is the clean sole-axiom closeout surface on the current retained bank:

- [NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md](./NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md)
- [NEUTRINO_SOLE_AXIOM_FULL_CLOSURE_BOUNDARY_NOTE.md](./NEUTRINO_SOLE_AXIOM_FULL_CLOSURE_BOUNDARY_NOTE.md)
- [frontier_neutrino_sole_axiom_full_closure_boundary.py](../scripts/frontier_neutrino_sole_axiom_full_closure_boundary.py)

That package should be read as:

- pure-retained PMNS closes negatively
- pure-retained Majorana closes negatively
- pure-retained neutrino closes negatively at the exact last-mile pair `(J_chi, mu) = (0, 0)`

### 2. Beyond-retained PMNS reopening package

This package sharpens the PMNS side all the way to a minimal extension
closeout:

- [PMNS_SIGMA_ZERO_NOGO_NOTE.md](./PMNS_SIGMA_ZERO_NOGO_NOTE.md)
- [PMNS_ACTIVE_RESPONSE_PACK_AXIOM_DERIVATION_NOTE.md](./PMNS_ACTIVE_RESPONSE_PACK_AXIOM_DERIVATION_NOTE.md)
- [PMNS_PROJECTED_CYCLE_RESPONSE_SOURCE_PRINCIPLE_NOTE.md](./PMNS_PROJECTED_CYCLE_RESPONSE_SOURCE_PRINCIPLE_NOTE.md)
- [PMNS_MINIMAL_EXTENSION_STRUCTURAL_CLOSURE_NOTE.md](./PMNS_MINIMAL_EXTENSION_STRUCTURAL_CLOSURE_NOTE.md)
- [frontier_pmns_sigma_zero_no_go.py](../scripts/frontier_pmns_sigma_zero_no_go.py)
- [frontier_pmns_active_response_pack_axiom_derivation.py](../scripts/frontier_pmns_active_response_pack_axiom_derivation.py)
- [frontier_pmns_projected_cycle_response_source_principle.py](../scripts/frontier_pmns_projected_cycle_response_source_principle.py)
- [frontier_pmns_minimal_extension_structural_closure.py](../scripts/frontier_pmns_minimal_extension_structural_closure.py)

Read this package in four steps:

1. the current pure-retained PMNS bank still gives `sigma = 0`, hence `J_chi = 0`
2. the exact missing microscopic theorem is the legitimacy of a nonfree active
   response pack on the existing `hw=1` carrier
3. if one adds the exact beyond-retained source principle that the microscopic
   active response on the graph-fixed `hw=1` triplet realizes the exact forward
   projected-cycle transport, then the unique admissible nonfree kernel is
   `K_fwd = C^2`, which forces exact nonzero
   `sigma = J_chi = -1/lambda_act`
4. so the minimal post-retained PMNS structural lane is positively closed,
   even though that extension principle is not yet derived from the
   pure-retained sole-axiom bank

So PMNS is no longer open in a vague way. It is closed negatively on the
pure-retained bank and reopened positively only by an explicit extension
principle.

The branch should therefore be read as:

- pure-retained PMNS: **closed negative**
- post-retained PMNS structural lane: **closed positive on the minimal extension**
- full neutrino program: **still open**

### 3. Beyond-retained Majorana reopening package

This package sharpens the Majorana side much further than the pure-retained
closeout:

- [NEUTRINO_MAJORANA_PURE_RETAINED_MU_IMPOSSIBILITY_NOTE.md](./NEUTRINO_MAJORANA_PURE_RETAINED_MU_IMPOSSIBILITY_NOTE.md)
- [NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md](./NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md)
- [NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md)
- [NEUTRINO_MAJORANA_MINIMAL_BRIDGE_STRUCTURAL_CLOSURE_NOTE.md](./NEUTRINO_MAJORANA_MINIMAL_BRIDGE_STRUCTURAL_CLOSURE_NOTE.md)
- [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md)
- [frontier_neutrino_majorana_pure_retained_mu_impossibility.py](../scripts/frontier_neutrino_majorana_pure_retained_mu_impossibility.py)
- [frontier_neutrino_majorana_nambu_source_principle.py](../scripts/frontier_neutrino_majorana_nambu_source_principle.py)
- [frontier_neutrino_majorana_source_ray_theorem.py](../scripts/frontier_neutrino_majorana_source_ray_theorem.py)
- [frontier_neutrino_majorana_endpoint_exchange_midpoint_theorem.py](../scripts/frontier_neutrino_majorana_endpoint_exchange_midpoint_theorem.py)
- [frontier_neutrino_majorana_adjacent_singlet_placement_theorem.py](../scripts/frontier_neutrino_majorana_adjacent_singlet_placement_theorem.py)
- [frontier_neutrino_majorana_residual_sharing_split_theorem.py](../scripts/frontier_neutrino_majorana_residual_sharing_split_theorem.py)
- [frontier_neutrino_majorana_minimal_bridge_structural_closure.py](../scripts/frontier_neutrino_majorana_minimal_bridge_structural_closure.py)
- [frontier_dm_neutrino_atmospheric_scale_theorem.py](../scripts/frontier_dm_neutrino_atmospheric_scale_theorem.py)

Read this package in six steps:

1. the current pure-retained Majorana bank gives `mu = 0`
2. if one adds the exact beyond-retained Nambu source principle, the local
   charge-`2` direction is forced into the admissible source grammar
3. inside that admitted family, the genuinely new one-generation source
   direction reduces to the pure-pairing ray `mu J_x`
4. the minimal finite bridge fixes the doublet anchor `k_B = 8`
5. the exact weak-axis adjacency and residual-sharing lift fix
   `k_A = 7` and `eps/B = alpha_LM/2`
6. so the minimal post-retained Majorana structural lane is positively closed,
   and the current diagonal benchmark already predicts the atmospheric scale
   without fitting `m_3`

So Majorana is no longer the branch’s structural pacing item.

What still does **not** close is:

- a positive pure-retained Majorana derivation
- full PMNS / solar / flavor closure
- a fully settled downstream CP-kernel and washout package

The branch should therefore be read as:

- pure-retained Majorana: **closed negative**
- post-retained Majorana structural lane: **closed positive on the minimal bridge**
- full neutrino program: **still open**

### 4. Exact last-mile compression

This is the branch’s clean combined neutrino frontier statement:

- [NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md](./NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md)
- [frontier_neutrino_two_amplitude_last_mile.py](../scripts/frontier_neutrino_two_amplitude_last_mile.py)

This is the right compression to keep in mind:

- PMNS blocker: `J_chi`
- Majorana blocker: `mu`
- neutrino blocker: `(J_chi, mu)`

### 5. Post-retained structural integration package

This is the positive post-retained integration surface now available on the
branch:

- [NEUTRINO_MINIMAL_POST_RETAINED_INTEGRATION_NOTE.md](./NEUTRINO_MINIMAL_POST_RETAINED_INTEGRATION_NOTE.md)
- [frontier_neutrino_minimal_post_retained_integration.py](../scripts/frontier_neutrino_minimal_post_retained_integration.py)

Read this package as:

1. the PMNS side exports a unique positive one-sided interface
   `tau = 0` together with the pair-level Hermitian data
2. the Majorana side exports a unique positive texture interface
   `k_A = 7`, `k_B = 8`, `eps/B = alpha_LM/2`
3. together they reduce to one exact transport-facing handoff
   `(P, M_1, M_2, M_3)`

So the post-retained neutrino program is no longer missing a structural
integration theorem. The remaining open work is upstream axiom derivation and
downstream CP/leptogenesis closure.

### 6. Post-retained observational closure package

This is the new exact positive promotion surface:

- [NEUTRINO_POST_RETAINED_FULL_CLOSURE_NOTE_2026-04-16.md](./NEUTRINO_POST_RETAINED_FULL_CLOSURE_NOTE_2026-04-16.md)
- [frontier_neutrino_post_retained_full_closure.py](../scripts/frontier_neutrino_post_retained_full_closure.py)

Read this package as:

1. the exact `N_e` effective-action selector fixes a unique positive PMNS lane
2. that selected `H_e` gives exact `eta/eta_obs = 1` on the favored column
3. the remaining microscopic `D` completion is spectator-inert once `H_e` is
   fixed, by exact Schur factoring
4. the exact Majorana bridge already lives on the same lane

So the branch is no longer just “structurally integrated.” It now has one
exact post-retained lane closed on the observational surface
`eta/eta_obs = 1`.

For the PMNS-assisted selector sub-lane specifically, the live authority
surface is now the reduced-domain selector package in
[DM_LEPTOGENESIS_PMNS_NE_SELECTOR_CLOSURE_AUTHORITY_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_NE_SELECTOR_CLOSURE_AUTHORITY_NOTE_2026-04-16.md),
rather than the older weaker “support-only” reading.

### 7. Observation-free normalization boundary

This is the new exact boundary on what still blocks a predictive
observation-free close:

- [DM_LEPTOGENESIS_PMNS_OBSERVATION_FREE_NORMALIZATION_BOUNDARY_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_OBSERVATION_FREE_NORMALIZATION_BOUNDARY_NOTE_2026-04-16.md)
- [frontier_dm_leptogenesis_pmns_observation_free_normalization_boundary.py](../scripts/frontier_dm_leptogenesis_pmns_observation_free_normalization_boundary.py)

Read this package as:

1. the current closure source can be rewritten as a local stationary point of
   a one-parameter observation-free free-energy family
2. transport extremality alone overshoots
3. the natural unit-scale free-energy law underproduces
4. the coefficient `a` in that free-energy family is still not derived from
   the current bank
5. current bounded observation-free searches do not upgrade that local rewrite
   into a theorem-grade global selector

So the remaining exact scientific weakness is now precise:
the observation-free normalization/value law is still open.

## New derivations on this branch

These are the new derivations that materially changed the neutrino picture:

- `PMNS sigma-zero no-go`:
  pure-retained PMNS now closes at `sigma = 0`, hence `J_chi = 0`
- `PMNS minimal-extension structural closure`:
  the post-retained PMNS lane now compresses to
  `K_fwd = C^2`,
  `A_fwd = (1 + 1/lambda_act)I - (1/lambda_act)C`,
  `sigma = J_chi = -1/lambda_act`
- `Majorana pure-retained mu impossibility`:
  pure-retained Majorana now closes at `mu = 0`
- `Majorana minimal-bridge structural closure`:
  the post-retained Majorana lane now compresses to
  `mu J_x`, `k_B = 8`, `k_A = 7`, `eps/B = alpha_LM/2`
- `Neutrino minimal post-retained integration`:
  the positive PMNS and Majorana lanes now integrate into one exact handoff
  package `(P, M_1, M_2, M_3)`
- `Neutrino post-retained full closure`:
  the exact `N_e` selector gives `eta/eta_obs = 1`, the microscopic `D`
  completion is quotiented by Schur invariance, and the already-fixed Majorana
  bridge closes the live post-retained lane on the observational surface
- `DM leptogenesis PMNS observation-free normalization boundary`:
  the remaining exact weakness is now the missing normalization/value law that
  would replace the `eta/eta_obs = 1` surface
- `Neutrino two-amplitude last-mile reduction`:
  the whole retained neutrino frontier is exactly `(J_chi, mu)`
- `PMNS projected-cycle response source principle`:
  the smallest exact positive PMNS reopening principle now visible on the
  branch is transport-realizing response on the graph-fixed `hw=1` triplet

## Exact answer to “are we done?”

If the question is:

> is the **pure-retained sole-axiom neutrino question** now closed?

Then the answer is:

**yes**. It is done, and it closes **negatively**.

If the question is:

> do we now have a **full positive neutrino lane on this branch**?

Then the answer is:

**yes**, but only on the current exact observational closure surface.

If the question is:

> is the **pure-retained sole-axiom lane** now positive?

Then the answer is:

**no**.

So the updated package conclusion is:

- pure-retained neutrino: **fully closed negative**
- live post-retained `N_e` lane: **exact observationally closed positive**
- pure-retained positive neutrino: **still unavailable**

## Explicit follow-up for later

One review-facing follow-up is still worth carrying as an explicit to-do:

- build a fully validated interval-global certificate on the reduced
  PMNS-assisted `N_e` closure manifold

That follow-up should be read correctly:

- it is **not** a new neutrino-structure gap
- it is **not** a reopened PMNS/Majorana branch-selection problem
- it is a certification-style upgrade on top of the already packaged exact
  reduced-domain selector lane summarized in
  [DM_LEPTOGENESIS_PMNS_NE_SELECTOR_CLOSURE_AUTHORITY_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_NE_SELECTOR_CLOSURE_AUTHORITY_NOTE_2026-04-16.md)

So the current neutrino package can be landed for review now, with the
interval-global certificate carried as the next explicit hardening task rather
than as a blocker to packaging this branch.
