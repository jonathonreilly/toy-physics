# Neutrino Sole-Axiom Full Closure Boundary

**Date:** 2026-04-16  
**Script:** `scripts/frontier_neutrino_sole_axiom_full_closure_boundary.py`

## Question
Does the retained neutrino lane close top-to-bottom from the sole axiom
`Cl(3)` on `Z^3` alone?

## Answer
No.

The current science branch now closes that question exactly.

On the retained Dirac/PMNS side:

- the sole axiom yields only the trivial free lower-level response profiles
- retained scalar deformation routes remain too small
- the only surviving positive carrier is the graph-first reduced oriented
  forward-cycle channel
- every point of that reduced channel is realized on the lower-level active
  response chain
- but the current exact bank does **not** select a unique value on that
  reduced channel

On the retained Majorana side:

- the lower-level charge-preserving response layer induces no anomalous Nambu
  block
- so the retained Majorana lane does not reopen there

Therefore full retained-neutrino closure from `Cl(3)` on `Z^3` alone is
blocked on the current exact bank.

## Exact Content

The theorem bundles the current exact endpoints into one retained-neutrino
closeout:

1. Sole-axiom lower-level PMNS response profiles are the trivial free ones.
2. Retained scalar deformation routes stay diagonal/scalar and are rejected by
   the one-sided PMNS closure stack.
3. The graph-first reduced oriented-cycle carrier is real and exact, but the
   current exact bank does not furnish a value-selection law on it.
4. The retained lower-level charge-preserving Majorana response layer has zero
   anomalous block.

## Consequence

The retained neutrino science lane is now closed honestly on the sole-axiom
question:

- the downstream closure machinery is exact once suitable lower-level data are
  supplied
- but the sole axiom itself does not supply a full positive retained-neutrino
  realization

Any further positive closure would require:

- genuinely new dynamics, or
- a further admitted extension

## Verification

```bash
python3 scripts/frontier_neutrino_sole_axiom_full_closure_boundary.py
```
