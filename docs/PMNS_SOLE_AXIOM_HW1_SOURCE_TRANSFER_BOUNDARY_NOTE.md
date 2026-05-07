# PMNS Sole-Axiom `hw=1` Source/Transfer Boundary

**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Date:** 2026-04-16  
**Revision:** 2026-05-07 - the runner now instantiates the restricted
`Cl(3)` / `Z^3` `hw=1` packet and computes the identity resolvents directly.
**Script:** `scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py`

## Question

If we derive the canonical `hw=1` source/transfer pack itself from the sole
axiom `Cl(3)` on `Z^3`, do native source insertion and graph-first forward
transport generate a nontrivial PMNS pack?

## Answer

No.

The strongest canonical sole-axiom `hw=1` source/transfer construction stays
trivial:

- the sole-axiom active resolvent is the identity on the `hw=1` triplet
- the sole-axiom passive resolvent is only a scalar multiple of the identity
- source insertion through the native site projectors therefore gives only the
  basis columns `e1,e2,e3`, up to the passive scalar weight
- graph-first forward transport fixes the ordered frame `E12,E23,E31`
- but that transport contributes only support/frame information, not nontrivial
  PMNS value data

So even this source-inserted transfer attack does not evade the free-profile
boundary.

## Exact content

The restricted packet now closes the contested derivation inside the runner.
It does not set `active_block = I3` and `passive_block = I3` as starting
definitions.

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

The zero-input sole-axiom sector operator on this triplet is the projector
resolution of the identity:

`D_free = sum_i P_i I_hw1 P_i = sum_i P_i = I3`.

Thus the active and passive sector blocks are not imported value data; they
are the two copies of this projector-derived free sector:

`D_act = D_pass = D_free = I3`.

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

This strengthens the sole-axiom PMNS boundary:

- not only do the sole-axiom lower-level response profiles stay trivial
- even the strongest canonical source-inserted / graph-first-transferred
  `hw=1` pack stays trivial

So the remaining blocker is not “we forgot to insert sources” or “we forgot to
use the graph-first transfer frame.” Those routes are now closed on the current
exact bank as well.

## Verification

```bash
python3 scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py
```

Expected:

```text
PASS=22 FAIL=0
```
