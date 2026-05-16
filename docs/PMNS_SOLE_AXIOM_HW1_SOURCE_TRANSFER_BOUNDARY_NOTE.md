# PMNS Sole-Axiom `hw=1` Source/Transfer Boundary

**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Date:** 2026-04-16  
**Revision:** 2026-05-07 - the runner instantiates the restricted
`Cl(3)` / `Z^3` `hw=1` packet, computes the projector-resolved identity sector
operator from joint translation characters, and verifies the resulting
trivial pack is rejected by the lower-level PMNS closure stack.  
**Revision:** 2026-05-16 - reframed to make the load-bearing step the
algebraic identity `sum_i P_i I_3 P_i = sum_i P_i = I_3` on the joint
character projectors, and added an explicit `Admitted-context inputs` section
declaring the carrier-construction admission and the lower-level closure
helper import that were previously implicit.  
**Script:** `scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py`

## Question

For the canonical `hw=1` sector operator admitted from the upstream PMNS
authority chain (see `Admitted-context inputs` below), does the algebraic
projector resolution on the `Cl(3)` / `Z^3` joint character triplet, followed
by native source insertion and graph-first forward transport, generate a pack
that is accepted by the retained PMNS closure stack?

## Answer

No.

The canonical `hw=1` sector operator on this triplet algebraically reduces to
the identity, so:

- the sole-axiom active resolvent is the identity on the `hw=1` triplet
- the sole-axiom passive resolvent is only a scalar multiple of the identity
- source insertion through the native site projectors therefore gives only the
  basis columns `e1,e2,e3`, up to the passive scalar weight
- graph-first forward transport fixes the ordered frame `E12,E23,E31`
- but that transport contributes only support/frame information, not nontrivial
  PMNS value data

So even this source-inserted transfer attack does not evade the free-profile
boundary, given the admitted carrier-construction identification.

## Admitted-context inputs

This note is bounded by two explicit admissions imported from upstream. These
are not derived inside the restricted packet of this note's runner; the
verdict scope is bounded accordingly.

1. **Carrier-construction admission.**  The identification

   ```
   D_act_hw1 := sum_i P_i  I_3  P_i,
   D_pass_hw1 := sum_i P_i  I_3  P_i,
   ```

   i.e. the statement that the active and passive sector operators on the
   `hw=1` triplet, in the zero-input free configuration, are the
   projector-resolved identity sector built from the joint character
   projectors `P_1, P_2, P_3`, is admitted from the upstream PMNS authority
   chain.  This is the same admission paid for by the sibling note
   [`PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md`](PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md)
   and explicitly disclaimed by the narrow bridge theorem runner
   `scripts/frontier_pmns_sole_axiom_free_point_identity_block_2026-05-16.py`,
   which states: "This runner exercises only finite-dimensional algebra; it
   does not derive the active-operator construction itself from the sole
   axiom.  The carrier derivation is the role of the upstream retained hw=1
   authority chain."  The present note inherits the same carrier admission.

2. **Lower-level PMNS closure-stack import.**  The retained PMNS closure
   stack used for the rejection step is imported through
   `frontier_pmns_lower_level_end_to_end_closure.close_from_lower_level_observables`,
   which is currently `support`-tier (audited_conditional, see
   [`PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md`](PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md)).
   The rejection conclusion ("the canonical hw=1 source/transfer pack is not
   on a one-sided minimal PMNS class") is closed locally by the
   `local_one_sided_minimal_pmns_rejection` check in the runner; the closure
   stack import provides a cross-check, not a load-bearing closure.

The load-bearing step of this note is the **algebraic** identity in section
"Exact content" below, not the carrier-construction admission and not the
closure-stack import.

## Exact content

The restricted packet computes the projector-resolved identity sector
operator algebraically from the joint character projectors.  It does not
hard-code `active_block = I3` or `passive_block = I3`; instead the runner
constructs the projectors `P_i` from `Cl(3)` / `Z^3` data and computes
`sum_i P_i I_3 P_i` step by step.

### 1. Axiom packet and source projectors

The runner first instantiates `Cl(3)` by Pauli generators
`gamma_1,gamma_2,gamma_3` and checks

`gamma_i gamma_j + gamma_j gamma_i = 2 delta_ij I`.

It then instantiates the `hw=1` `Z^3` character triplet

`(-1,+1,+1), (+1,-1,+1), (+1,+1,-1)`.

For the three commuting translation involutions `T_x,T_y,T_z`, the native
source projectors are computed as joint spectral projectors:

`P_chi = prod_a ((I + chi_a T_a) / 2)`.

For the three `hw=1` characters this gives exactly

`P_1 = E11`, `P_2 = E22`, `P_3 = E33`, and

`P_1 + P_2 + P_3 = I3`.

### 2. Identity sector blocks and resolvents

Under the carrier-construction admission named in
`Admitted-context inputs` above, the zero-input sole-axiom sector operator
on this triplet is the projector resolution of the identity.

**Load-bearing algebraic identity (Class A):** the runner computes, on the
projectors `P_i` constructed in section 1,

```
sum_i P_i I_3 P_i  =  sum_i P_i  =  I_3.
```

The first equality uses `P_i I_3 P_i = P_i^2 = P_i` (idempotency of each
projector).  The second equality is the projector resolution
`P_1 + P_2 + P_3 = I_3` already verified in section 1.  The runner verifies
each step (idempotency, mutual orthogonality, projector resolution, and the
chained identity) numerically rather than asserting the target value.  Under
the carrier-construction admission, this gives

`D_act = D_pass = sum_i P_i I_3 P_i = I_3`.

With the lower-level conventions used by the PMNS closure stack,

`R_act = (I - lambda_act (D_act - I))^-1 = I3`,

and

`R_pass = (I - lambda_pass D_pass)^-1 = (1 - lambda_pass)^-1 I3`.

Source insertion through the rank-one projectors gives the columns

`R_act e_i = e_i`,

and

`R_pass e_i = (1 - lambda_pass)^-1 e_i`.

Reconstructing the blocks from these response columns recovers exactly
`(I3, I3)`.

### 3. Transfer frame and closure rejection

Forward cycle transport of the native projectors gives the graph-first ordered
frame:

`E11 C = E12`, `E22 C = E23`, `E33 C = E31`.

This is support/frame data only. The runner checks locally that the
projector-derived free pack is not a one-sided minimal PMNS class: both
sector blocks are diagonal monomial blocks and neither has the active support
`I + C`. The
[PMNS lower-level closure stack](PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md)
is then invoked as a live consistency check and rejects the same pack for the
same reason.

## Consequence

This strengthens the bounded PMNS boundary statement, under the explicit
carrier-construction admission named above:

- not only do the lower-level response profiles stay trivial on the projector-
  resolved free pack
- even the canonical source-inserted / graph-first-transferred `hw=1` pack
  stays trivial

So the remaining blocker is not "we forgot to insert sources" or "we forgot to
use the graph-first transfer frame." Those routes are closed on the current
exact bank, conditional on the admitted carrier-construction identification.
A genuinely sole-axiom derivation of the carrier construction itself is the
role of the upstream retained `hw=1` authority chain and is out of the
restricted scope of this note.

## Verification

```bash
python3 scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py
```

Expected:

```text
PASS=37 FAIL=0
```
