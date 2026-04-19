# PMNS Projected-Cycle Response Source Principle

**Date:** 2026-04-16  
**Status:** exact beyond-retained-stack PMNS source-principle theorem on the
main-derived neutrino lane  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_projected_cycle_response_source_principle.py`

## Question

After the pure-retained PMNS bank is exhausted, is there a smallest exact
extension principle that forces a nontrivial active response pack on the
existing `hw=1` carrier rather than adding arbitrary reduced-cycle values by
hand?

## Bottom line

Yes.

On the graph-fixed `hw=1` triplet, the projected forward cycle is the exact
operator `C`. If the microscopic active response is required to realize that
exact forward transport on the ordered response basis, then the unique
admissible nonfree response kernel is

`K_fwd = C^2`.

Passing from response kernel to active block by the exact active-response law

`A = I + (I - K^{-1}) / lambda_act`

then forces

`A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`.

That block is already the `C_3`-covariant point on the exact projected-cycle
family `A(a,b) = a I + b C`, so it gives

- `sigma = -1 / lambda_act`
- `J_chi = -1 / lambda_act`

exactly, and the one-sided PMNS lane closes with the retained passive free
pack.

So the PMNS source-law hole now has one exact beyond-retained-stack closure
principle:

> require the microscopic active response on the graph-fixed `hw=1` triplet to
> realize the exact forward projected-cycle transport.

## Inputs

This theorem sits downstream of five exact branch surfaces:

- [PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md](./PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md)
- [PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md](./PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md)
- [PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- [PMNS_ACTIVE_RESPONSE_PACK_AXIOM_DERIVATION_NOTE.md](./PMNS_ACTIVE_RESPONSE_PACK_AXIOM_DERIVATION_NOTE.md)
- [PMNS_ORIENTED_CYCLE_REDUCED_CHANNEL_NONSELECTION_NOTE.md](./PMNS_ORIENTED_CYCLE_REDUCED_CHANNEL_NONSELECTION_NOTE.md)

Those notes already prove:

1. the ordered forward cycle frame on the `hw=1` triplet is fixed exactly
2. the active response law from a lower-level pack is exact
3. the current pure-retained bank still stops at the free pack
4. if one upgrades transported frame data into a genuine response pack, PMNS
   reopens immediately
5. every point on the reduced cycle family is already realizable once such a
   pack is supplied

So the next honest move is no longer to search for another readout. It is to
state the smallest exact source principle that upgrades transport data into a
microscopic response pack.

## Exact theorem

### 1. The graph-fixed forward transport kernel is exact

On the ordered `hw=1` basis, the projected forward cycle is

`C = [[0,1,0],[0,0,1],[1,0,0]]`.

Transporting the ordered basis response columns one forward step on column
labels gives

`K_fwd = C^2`.

That kernel is:

- unitary
- nonfree
- cubic: `K_fwd^3 = I`

So it is the exact forward transport kernel on the ordered response basis.

### 2. Forward orientation makes the kernel unique

The exact cycle kernels on this ordered triplet are

- `I`
- `C`
- `C^2`.

Under the exact response law

`A = I + (I - K^{-1}) / lambda_act`,

these give:

- `K = I` -> the free block `A = I`
- `K = C` -> a backward-support block on `I + C^2`
- `K = C^2` -> a forward-support block on `I + C`

So once:

1. nontriviality excludes the free kernel, and
2. the graph-fixed forward carrier is required,

the unique admissible nonfree response kernel is `K_fwd = C^2`.

### 3. The response law then forces one exact PMNS block

Substituting `K_fwd = C^2` into the exact response law gives

`A_fwd = I + (I - C) / lambda_act`

equivalently

`A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`.

This is already of the exact projected-cycle form `A(a,b) = a I + b C` with

- `a = 1 + 1/lambda_act`
- `b = -1 / lambda_act`.

### 4. The forced block is already the covariant PMNS closure point

On the exact projected-cycle family, the PMNS readouts satisfy

- `sigma = b`
- `J_chi = b`

at the `C_3`-covariant point where all forward-cycle coefficients agree.

For `A_fwd`, all three forward-cycle coefficients are exactly `-1/lambda_act`,
so

- `sigma = -1/lambda_act`
- `J_chi = -1/lambda_act`.

The same block reproduces `K_fwd` under the active-response law and closes the
one-sided PMNS lane with the retained passive free pack.

## The theorem-level statement

**Theorem (PMNS projected-cycle response source principle on the graph-fixed
`hw=1` triplet).**
Assume:

1. the exact graph-fixed ordered forward cycle frame on the `hw=1` triplet
2. the exact active-response law
3. the physical extension principle that the microscopic active response must
   realize the exact forward projected-cycle transport on that ordered basis

Then:

1. the unique admissible nonfree response kernel is `K_fwd = C^2`
2. the active block is forced to
   `A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`
3. that block is already the `C_3`-covariant point on the exact projected-cycle
   family
4. therefore `sigma = J_chi = -1/lambda_act` exactly
5. and the one-sided PMNS lane closes with the retained passive free pack

So the missing positive PMNS object is no longer “some arbitrary nontrivial
response pack” once this extension principle is imposed. It is the exact
transport-realizing response kernel on the graph-fixed triplet.

## What this closes

This closes one specific beyond-retained-stack question:

- is there a smallest exact PMNS source principle that forces a nontrivial
  active response pack on the existing `hw=1` carrier?

Answer: yes.

The new exact principle is:

> the microscopic active response on the graph-fixed `hw=1` triplet must
> realize the exact forward projected-cycle transport.

That is the first exact positive PMNS source-principle step beyond the
transport-blind pure-retained bank.

## What this does not close

This note does **not** prove:

- that the current pure-retained bank already derives this principle
- that transport-realizing response is unavoidable without adding any new
  source principle
- any Majorana positive reopening
- a pure-retained positive neutrino closeout

So this is an exact PMNS extension theorem, not a proof that the pure-retained
bank was secretly already positive.

## Safe wording

**Can claim**

- there is one exact beyond-retained-stack PMNS source principle that forces a
  nontrivial active response pack on the existing `hw=1` carrier
- that principle uniquely selects the forward cycle response kernel `K_fwd=C^2`
- the exact response law then forces the covariant PMNS block
  `A_fwd=(1+1/lambda_act)I-(1/lambda_act)C`
- on that block `sigma` and `J_chi` are both exactly `-1/lambda_act`
- the one-sided PMNS lane closes exactly with the retained passive free pack

**Cannot claim**

- the current pure-retained PMNS bank already implies this principle
- the neutrino program is fully positive without any extra source principle
- Majorana has been reopened positively by this theorem

## Command

```bash
python3 scripts/frontier_pmns_projected_cycle_response_source_principle.py
```
