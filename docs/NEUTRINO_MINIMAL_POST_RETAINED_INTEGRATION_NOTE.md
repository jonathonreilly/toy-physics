# Neutrino Minimal Post-Retained Integration

**Date:** 2026-04-16  
**Status:** exact structural integration and handoff theorem on the current
post-retained neutrino branch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_minimal_post_retained_integration.py`

## Question

After the pure-retained neutrino lane closes negatively, and after the PMNS and
Majorana sides are each structurally reopened on their minimal positive
extensions, do those two positive lanes now fit into one coherent neutrino
program on this branch? If so, what exact object should be handed downstream to
the CP/leptogenesis work?

## Bottom line

Yes.

The current branch now carries one coherent **post-retained structural neutrino
package**.

On the PMNS side, the minimal extension gives:

- `K_fwd = C^2`
- `A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`
- `sigma = J_chi = -1/lambda_act`
- one-sided closure on the neutrino-active branch with `tau = 0`, `q = 0`

On the Majorana side, the minimal bridge gives:

- local source class `mu J_x`
- `k_B = 8`
- `k_A = 7`
- `eps/B = alpha_LM/2`

Those two sides already integrate into one exact pair-level neutrino interface:

`((tau, H_nu, H_e), (k_A, k_B, eps/B))`

On the current branch specialization that becomes:

- `tau = 0`
- `H_e` diagonal / monomial
- PMNS transport packet

  `P = |U_PMNS|^2`

  with exact packet

  `[[1/3, 1/2, 1/6],`
  ` [1/3,   0, 2/3],`
  ` [1/3, 1/2, 1/6]]`

- heavy texture scales

  `M_1 = B (1 - eps/B)`
  `M_2 = B (1 + eps/B)`
  `M_3 = A`

So the current transport-facing neutrino handoff is already exact:

`(P, M_1, M_2, M_3)`.

What remains open is no longer structural integration. It is:

- deriving both positive extensions from one unextended sole-axiom bank
- the downstream CP-kernel / washout closure

## Inputs

This capstone compresses:

- [PMNS_MINIMAL_EXTENSION_STRUCTURAL_CLOSURE_NOTE.md](./PMNS_MINIMAL_EXTENSION_STRUCTURAL_CLOSURE_NOTE.md)
- [PMNS_CLOSURE_STATUS_NOTE_2026-04-16.md](./PMNS_CLOSURE_STATUS_NOTE_2026-04-16.md)
- [NEUTRINO_MAJORANA_MINIMAL_BRIDGE_STRUCTURAL_CLOSURE_NOTE.md](./NEUTRINO_MAJORANA_MINIMAL_BRIDGE_STRUCTURAL_CLOSURE_NOTE.md)
- [NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md](./NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md)
- [DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md)

Those surfaces already prove:

1. the pure-retained neutrino last mile is exactly `(J_chi, mu)` and closes at
   `(0, 0)`
2. the PMNS structural lane is positively closed on the minimal extension
3. the Majorana structural lane is positively closed on the minimal bridge
4. the pair `(H_nu, H_e)` already determines the PMNS projector packet
5. the downstream flavored DM route consumes that packet together with the
   Majorana texture scales

So the remaining honest question is no longer whether the post-retained
positive lanes can be integrated at all.

## Exact theorem

### 1. Pure-retained neutrino is finished, but negatively

The exact remaining retained neutrino frontier is the pair

`(J_chi, mu)`,

and the current retained bank sets

`(J_chi, mu) = (0, 0)`.

So the pure-retained sole-axiom neutrino lane is done, but dead.

### 2. The PMNS side now exports a unique positive structural interface

On the minimal post-retained PMNS extension:

- the unique nonfree response kernel is `K_fwd = C^2`
- the exact active block is
  `A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C`
- the exact current is `sigma = J_chi = -1/lambda_act`
- the lower-level closure lands on the neutrino-active branch with `tau = 0`
  and `q = 0`

So the PMNS side already exports a unique positive pair-level interface.

### 3. The Majorana side now exports a unique positive structural interface

On the minimal post-retained Majorana bridge:

- the local source class is the pure-pairing ray `mu J_x`
- the heavy doublet anchor is `k_B = 8`
- the singlet placement is `k_A = 7`
- the exact split law is `eps/B = alpha_LM/2`

Equivalently in scale variables:

- `A = M_Pl * alpha_LM^7`
- `B = M_Pl * alpha_LM^8`
- `M_1 = B (1 - eps/B)`
- `M_2 = B (1 + eps/B)`
- `M_3 = A`

So the Majorana side already exports a unique positive texture interface.

### 4. The two sides integrate without new structural ambiguity

On the current PMNS positive closeout, the passive charged-lepton Hermitian
block is diagonal / monomial, while the active neutrino block is the
nontrivial carrier.

Therefore the PMNS pair-level interface reduces cleanly to the transport packet

`P = |U_PMNS|^2`

read from `(H_nu, H_e)`.

On the current branch this packet is exactly

`[[1/3, 1/2, 1/6],`
` [1/3,   0, 2/3],`
` [1/3, 1/2, 1/6]]`.

Together with the Majorana texture scales `(M_1, M_2, M_3)`, this is already
the exact transport-facing neutrino handoff to the downstream CP/leptogenesis
program.

## The theorem-level statement

**Theorem (Minimal post-retained structural integration of the neutrino
program on the current branch).**
Assume:

1. the pure-retained neutrino lane closes negatively at `(J_chi, mu) = (0, 0)`
2. the PMNS side is reopened by the minimal projected-cycle response extension
3. the Majorana side is reopened by the minimal Nambu / finite-bridge texture
   extension

Then the post-retained neutrino structural program is integrated with exact
interface

`((tau, H_nu, H_e), (k_A, k_B, eps/B))`.

On the current branch specialization this reduces transport-facing to

`(P, M_1, M_2, M_3)`,

where

- `tau = 0`
- `P = |U_PMNS|^2`
- `M_1 = M_Pl * alpha_LM^8 * (1 - alpha_LM/2)`
- `M_2 = M_Pl * alpha_LM^8 * (1 + alpha_LM/2)`
- `M_3 = M_Pl * alpha_LM^7`

Equivalently: the current branch no longer has a structural neutrino
integration problem. The remaining open work has moved upstream to unextended
axiom derivation and downstream to the CP/leptogenesis tail.

## What this closes

This closes the structural integration problem for the positive post-retained
neutrino lane:

- PMNS and Majorana no longer live as disconnected positive stories
- the exact pair-level interface is fixed
- the exact transport-facing handoff is fixed

So the neutrino branch can now hand one coherent package to downstream
CP/leptogenesis work.

## What this does not close

This note does **not** prove:

- a positive pure-retained sole-axiom neutrino derivation
- that the PMNS extension principle is already implied by the retained bank
- that the Majorana positive bridge is already implied by the retained bank
- the exact downstream CP-asymmetry kernel or washout closure
- full positive neutrino closure from one unextended bank

## Safe wording

**Can claim**

- pure-retained neutrino is closed negative
- post-retained PMNS and Majorana are each structurally closed positive
- those positive lanes now integrate into one exact neutrino handoff package
- the exact transport-facing handoff is `(P, M_1, M_2, M_3)`

**Cannot claim**

- that the whole neutrino program is already closed from the unextended axiom
- that the downstream CP/leptogenesis tail is already solved

## Command

```bash
python3 scripts/frontier_neutrino_minimal_post_retained_integration.py
```
