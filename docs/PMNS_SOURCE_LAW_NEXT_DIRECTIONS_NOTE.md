# PMNS Source-Law Next Directions

Date: 2026-04-16

## Current State

On the current branch, the retained PMNS lane is sharply closed up to one
missing source theorem.

- The reduced carrier is already exact.
- The native readout is already exact.
- The native `C3` character closure is already exact.
- The selector on an admitted fixed-`sigma` surface is already locally exact.
- The current sole-axiom `hw=1` bank still produces only the trivial free
  active response pack, so `sigma = 0` and `J_chi = 0`.

The exact new boundary is:

- on the reduced retained PMNS family, `sigma` is exactly the forward odd
  transport mean
- a nonzero `sigma` surface would require only one nontrivial active response
  pack on the existing `hw=1` carrier
- the current bank still does not produce that response pack

So the PMNS question is no longer “how do we read or select the reduced
values?” but “what new axiom-native source principle could produce a nontrivial
active response pack at all?”

## Ranked Directions

### 1. Active response-pack source principle

Target:
derive a sole-axiom law that produces a nontrivial active response pack on the
existing `hw=1` carrier, hence a nonzero forward odd mean `sigma`.

Why this is best:

- It is the narrowest exact missing theorem left on PMNS.
- It does not ask for a new PMNS carrier.
- It does not ask for a new selector.
- It aligns exactly with the new boundary:
  nonzero `sigma` is equivalent to a nontrivial active response pack.

Current support:

- [frontier_pmns_nonzero_sigma_response_pack_boundary.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_nonzero_sigma_response_pack_boundary.py>)
- [frontier_pmns_active_four_real_source_from_transport.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_active_four_real_source_from_transport.py>)
- [frontier_pmns_hw1_source_transfer_boundary.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_hw1_source_transfer_boundary.py>)

Current blocker:

- the current sole-axiom `hw=1` source projectors still give only the basis
  columns, so the derived active kernel stays free

Assessment:

- best route
- still hard
- success probability about `35%`

### 2. Non-averaged transport source law

Target:
upgrade the existing transport laws from seed-pair / branch-bit recovery to a
full microscopic source law for the active off-seed response data.

Why it is plausible:

- direct transport already gives exact positive data
- `sigma` is exactly the forward odd transport mean on the reduced family
- non-averaged transport already recovers the active source once a nontrivial
  response pack is supplied

Why it is weaker than route 1:

- current direct transport laws are still blind to the full 5-real
  corner-breaking source
- this route looks more like a reformulation of route 1 than an independent
  source principle

Current support:

- [frontier_pmns_corner_transport_active_block.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_corner_transport_active_block.py>)
- [frontier_pmns_transfer_operator_dominant_mode.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_transfer_operator_dominant_mode.py>)
- [frontier_pmns_nonzero_sigma_response_pack_boundary.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_nonzero_sigma_response_pack_boundary.py>)

Current blocker:

- orbit-averaged and dominant-mode transport still collapse away the off-seed
  source

Assessment:

- live but derivative
- success probability about `25%`

### 3. Character-holonomy dynamical source route

Target:
reinterpret the exact native `C3` holonomy family as a dynamical source law,
not only a readout law, so the nontrivial character amplitude is generated
directly.

Why it is tempting:

- the `C3` character triple already closes the reduced values exactly
- the remaining PMNS blocker is exactly one nontrivial character amplitude

Why it is currently weak:

- all current `C3` and holonomy theorems are readout/closure theorems
- they reconstruct nontrivial values once given, but do not produce them from
  the current bank

Current support:

- [frontier_pmns_c3_character_holonomy_closure.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_c3_character_holonomy_closure.py>)
- [frontier_pmns_c3_character_mode_reduction.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_c3_character_mode_reduction.py>)
- [frontier_pmns_c3_nontrivial_current_boundary.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_c3_nontrivial_current_boundary.py>)

Current blocker:

- no current theorem turns the native character triple into a microscopic
  source mechanism on the retained `hw=1` response family

Assessment:

- coherent but mostly a repackaging of the same missing source
- success probability about `20%`

### 4. Graph / commutant selector upgrade

Target:
upgrade the graph-first axis law plus projected commutant selector bundle into
a full PMNS source/value law.

Why it is lowest-ranked:

- this route is already close to exhausted
- it fixes axis, frame, `tau`, and `q`, but is constant on the reduced cycle
  family

Current support:

- [frontier_pmns_graph_first_axis_alignment.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_graph_first_axis_alignment.py>)
- [frontier_pmns_graph_first_cycle_frame_support.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_graph_first_cycle_frame_support.py>)
- [frontier_pmns_graph_commutant_cycle_value_boundary.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_graph_commutant_cycle_value_boundary.py>)
- [frontier_pmns_commutant_eigenoperator_selector.py](</Users/jonBridger/CI3Z2 Main/scripts/frontier_pmns_commutant_eigenoperator_selector.py>)

Current blocker:

- the route is already theorem-grade value-blind on the reduced family

Assessment:

- near-dead as a positive source route
- success probability about `10%`

## Recommendation

The next PMNS program should be:

1. treat the missing theorem exactly as a nontrivial active response-pack
   source principle
2. use transport and character machinery only as diagnostics and readouts
3. do not spend more time trying to upgrade graph/commutant selectors into a
   value law

The concrete next script should be:

- `scripts/frontier_pmns_active_response_pack_source_principle.py`

Its theorem target should be:

- any positive PMNS reopening beyond the current retained bank is equivalent to
  adjoining one new axiom-native source principle that produces a nontrivial
  active response pack on the existing `hw=1` carrier
- once that pack exists, `sigma`, `J_chi`, and the selected `C3` branch are
  already handled by the current stack
