# PMNS Oriented Cycle Selection Structure

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_pmns_oriented_cycle_selection_structure.py`

## Question

Once the oriented forward cycle channel has an exact native observable/value
law, what exact selection structure remains on that channel?

## Answer

Three exact statements survive:

- exact `C_3` covariance collapses the cycle channel to one complex slot
  `sigma C`
- at the sole-axiom free point, `sigma = 0`, so the sole axiom selects only the
  trivial cycle law on that exact `C_3`-covariant locus
- on the graph-first selected-axis route, the residual antiunitary symmetry
  reduces the cycle channel to the `3`-real subfamily
  `c_1 = conjugate(c_3)`, `c_2 real`

So the carrier and observable law are closed, and the remaining gap is only a
value-selection law on that reduced channel.

## Exact chain

### 1. Exact `C_3` covariance

Write the oriented forward-cycle block as

`A_fwd = c_1 E_12 + c_2 E_23 + c_3 E_31`.

Conjugation by the projected cycle operator `C` permutes the coefficients
cyclically:

`(c_1, c_2, c_3) -> (c_2, c_3, c_1)`.

Therefore the exact `C_3`-fixed locus is

`c_1 = c_2 = c_3 = sigma`,

equivalently

`A_fwd = sigma C`.

### 2. Sole-axiom free point

At the sole-axiom free point, the active block is the identity block `I_3`.
Its oriented-cycle coefficients vanish exactly, so

`sigma = 0`.

Therefore the sole axiom by itself does not select a nontrivial cycle value on
the exact `C_3`-covariant locus.

### 3. Graph-first selected-axis route

On the graph-first route, the strongest exact residual antiunitary reduction on
the cycle channel is

`A_fwd = P_23 A_fwd^dagger P_23`.

Its fixed locus is

- `c_1 = conjugate(c_3)`
- `c_2` real

So the graph-first selected-axis route reduces the cycle channel from three
complex coefficients to three real parameters:

- `Re c_1`
- `Im c_1`
- `c_2`

## Consequence

This is not a full value-selection law. It does not yet derive the values from
`Cl(3)` on `Z^3` alone.

What it does prove is that the remaining positive target is no longer vague:

> any future nontrivial retained PMNS law must select values on the reduced
> oriented-cycle channel, and on the graph-first route that channel is already
> only `3` real dimensional.

## Boundary

This is a selection-structure theorem, not a closure theorem.

It closes:

- the exact `C_3`-covariant cycle slot
- the exact sole-axiom free-point value on that slot
- the exact graph-first residual symmetry reduction

It does **not** yet derive a nontrivial cycle-value selection law from the sole
axiom.

## Command

```bash
python3 scripts/frontier_pmns_oriented_cycle_selection_structure.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope, which remains conditional algebra on the C3-fixed locus and the residual swap-conjugation fixed locus given the imported channel-law authority and the imported sole-axiom free-point and graph-first residual-antiunitary premises.

One-hop authorities cited:

- [`pmns_oriented_cycle_channel_value_law_note`](PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md)
  — currently `audited_clean` / `retained` (audit row:
  `pmns_oriented_cycle_channel_value_law_note`). This is the upstream
  retained authority for the native oriented-cycle observable / value law
  that the present note's selection-structure result post-composes with.

Open class D registration targets named by the 2026-05-05 audit verdict
as `missing_bridge_theorem`:

- The graph-first residual antiunitary condition `A_fwd = P_23 A_fwd^dag P_23`
  is imported as a premise, not derived inside the present note's restricted
  packet. Closing it would require a retained source note proving that the
  graph-first selected-axis route induces exactly this residual antiunitary
  reduction on the oriented forward-cycle channel.
- The sole-axiom free-point identification of the active block as the
  identity block `I_3` is imported as a premise, not derived inside the
  present note. Closing it would require a retained source note proving
  that at the sole-axiom free point the active block is exactly `I_3`,
  which then forces `sigma = 0` on the C3-covariant locus.

Both open class D items match the 2026-05-05 audit verdict's
`notes_for_re_audit_if_any` field exactly:
"add a retained bridge proving the graph-first residual antiunitary
condition and the sole-axiom free-point identity block within the
restricted dependency chain."

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with the
observation that the runner's A=8 algebraic checks (cyclic permutation
under C3, vanishing oriented-cycle coefficients on `I_3`, fixed locus of
the residual swap-conjugation map, generic-coefficient nonfixedness)
close on their own terms but are class A finite-dimensional algebra,
not first-principles derivations from the sole axiom. The cited upstream
authority `pmns_oriented_cycle_channel_value_law_note` is retained for
the native channel law, but the present note still imports the
graph-first residual antiunitary condition and the free-point identity-block
identification as premises not closed by the restricted packet. The cite
chain above wires those premises as explicit open class D registration
targets without altering the runner-checked content. Effective status
remains `audited_conditional`. The note's `audit_status` is unchanged by
this addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority the audit verdict expected and explicitly registers
the two open class D bridge-theorem targets named by the verdict's
`notes_for_re_audit_if_any` field. It mirrors the live cite-chain
pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `8e84f0c23`).
