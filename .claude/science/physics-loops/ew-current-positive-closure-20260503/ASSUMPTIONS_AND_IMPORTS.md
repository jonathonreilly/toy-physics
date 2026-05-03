# Assumptions And Imports

## Allowed Framework Inputs

- `EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md`: defines
  `kappa_EW`, `K_EW(kappa_EW)`, and the no-go boundary for the Fierz/CMT/OZI
  packet.
- `EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`: exact color
  singlet/adjoint Fierz decomposition and the `8/9` channel fraction.
- `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`: bounded
  current-form context for a bilinear/point-split current; not promoted here
  as repo-wide axiom authority.
- Standard exact finite-dimensional trace algebra.

## Forbidden Inputs

- No QCD phenomenology as a selector.
- No fit to observed EW couplings.
- No use of empirical success at `kappa_EW = 0`.
- No assertion that CMT removes the singlet channel; existing runner evidence
  shows CMT scales singlet and adjoint uniformly.

## New Route-Specific Import Status

The route tests an internal-generator trace argument. It imports only exact
matrix trace arithmetic and then rejects the route because it acts on the wrong
factor: internal EW trace rather than color Fierz channel.
