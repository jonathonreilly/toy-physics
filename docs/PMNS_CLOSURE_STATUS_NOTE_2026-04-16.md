# PMNS Closure Status

**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_closure_status.py`

## Question

On the current branch, is the PMNS lane already structurally closed from the
retained bank, merely blocked, or extension-dependent? And what is the minimal
honest handoff object to the downstream CP/leptogenesis lane?

## Bottom line

The strongest honest overall status on this branch is:

- `pure-retained bank`: blocked
- `overall branch`: extension-dependent

More precisely:

1. the current pure-retained sole-axiom bank is still exactly blocked at
   `sigma = J_chi = 0`
2. the current exact axiom bank still does **not** derive the missing
   nontrivial active response pack from source/projector/frame data alone
3. there is now one exact beyond-retained extension principle that closes PMNS
   positively and uniquely:

   - `K_fwd = C^2`
   - `A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`
   - `sigma = J_chi = -1 / lambda_act`

So PMNS is not structurally positive from the retained bank itself, but it is
also no longer a vague dead end. The branch now contains a minimal exact
extension theorem that closes the remaining hole.

## Exact status split

### 1. Pure-retained status is blocked

The existing PMNS obstruction stack now closes cleanly:

- [PMNS_SIGMA_ZERO_NOGO_NOTE.md](./PMNS_SIGMA_ZERO_NOGO_NOTE.md)
- [PMNS_ACTIVE_RESPONSE_PACK_AXIOM_DERIVATION_NOTE.md](./PMNS_ACTIVE_RESPONSE_PACK_AXIOM_DERIVATION_NOTE.md)
- [PMNS_SOURCE_LAW_NEXT_DIRECTIONS_NOTE.md](./PMNS_SOURCE_LAW_NEXT_DIRECTIONS_NOTE.md)

Those files together prove:

- all current retained PMNS source routes still give `sigma = 0`
- the current retained readout stack therefore still gives `J_chi = 0`
- the unconstrained native effective action also stays at the seed
- graph-fixed transport frame data are exact, but they still do not become a
  genuine microscopic response pack on the retained bank

So the retained lane is not positive.

### 2. The minimal positive theorem is now an extension theorem

The positive side is now equally sharp:

- [PMNS_PROJECTED_CYCLE_RESPONSE_SOURCE_PRINCIPLE_NOTE.md](./PMNS_PROJECTED_CYCLE_RESPONSE_SOURCE_PRINCIPLE_NOTE.md)

Once one imposes the exact extension principle

> the microscopic active response on the graph-fixed `hw=1` triplet must
> realize the exact forward projected-cycle transport

the closure is immediate and unique:

- the unique nonfree kernel is `K_fwd = C^2`
- the exact response law forces
  `A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`
- that point is already the covariant PMNS closure point
- hence `sigma = J_chi = -1 / lambda_act`
- with the retained passive free pack unchanged, the one-sided PMNS lane
  closes exactly on the neutrino-active branch

This is not a proof that the retained bank was secretly positive. It is an
exact beyond-retained-stack source theorem.

### 3. Why the branch is extension-dependent, not selector-closed

The current selector stack still does not produce the positive point by itself:

- [frontier_pmns_effective_action_selector_boundary.py](../scripts/frontier_pmns_effective_action_selector_boundary.py)
- [frontier_pmns_projected_cycle_sector_family_selector_nogo.py](../scripts/frontier_pmns_projected_cycle_sector_family_selector_nogo.py)

Those boundaries show:

- the unconstrained action minimizes at the seed
- on the exact cycle family `A(a,b) = a I + b C`, the same action also gives
  zero on the degenerate unitary walls
- admissible reopening points, including the forced `A_fwd`, have strictly
  positive action

So the selector alone still does not choose the reopening point. The positive
closeout comes from the source principle, not from the current selector acting
by itself.

That is exactly why the overall status is `extension-dependent`.

## Minimal downstream handoff

The PMNS branch should hand off the smallest stable object that the
CP/leptogenesis lane can actually consume.

The exact interface is:

- stable handoff: `(tau, H_act)`
- on the current positive closeout: `tau = 0` and `H_act = H_nu`

Why this is enough:

- the projected-cycle source principle closes on a one-sided PMNS branch
- the passive charged-lepton Hermitian block is then diagonal/monomial
- so the downstream packet depends only on the active Hermitian block, up to
  passive ordering

This matches the existing downstream interface reductions:

- [DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md)

If a downstream consumer needs only flavored transport weights, it can reduce
further to

`P_i(alpha) = |U_PMNS(alpha,i)|^2`

from `H_act`. But the clean PMNS-to-CP/leptogenesis interface should stay at
the active Hermitian block plus the branch bit.

## Status line

Use this wording:

> On the current branch, pure-retained PMNS is blocked at `sigma = J_chi = 0`.
> The strongest honest overall PMNS finish is extension-dependent: one exact
> beyond-retained projected-cycle response principle closes PMNS uniquely on
> the neutrino-active branch with `K_fwd = C^2`,
> `A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`, and
> `sigma = J_chi = -1 / lambda_act`. The minimal downstream handoff is the
> one-sided active Hermitian block `H_act` together with the branch bit `tau`
> (here `tau = 0`, so `H_act = H_nu`).

## Command

```bash
python3 scripts/frontier_pmns_closure_status.py
```
