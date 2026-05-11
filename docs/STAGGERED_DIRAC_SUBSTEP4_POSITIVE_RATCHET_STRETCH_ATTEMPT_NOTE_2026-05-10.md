# Staggered-Dirac Substep-4 Positive Ratchet Open Gate Note

**Date:** 2026-05-10
**Claim type:** open_gate
**Scope:** reviews whether the bounded substep-4 AC narrowing can be
ratcheted to a `positive_theorem` using the current source package alone.
The answer here is negative: the ratchet is still open because the
species-label readout needed by `AC_phi_lambda` is not derived by the
current package.
**Status authority:** source note only. Audit verdicts and effective status
are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_staggered_dirac_substep4_positive_ratchet.py`](../scripts/frontier_staggered_dirac_substep4_positive_ratchet.py)

## Boundary

The target surface is the bounded substep-4 narrowing note
[`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md).
That note separates the local AC content into `AC_phi`, `AC_lambda`, and
`AC_phi_lambda`. The remaining issue for this ratchet is the
`AC_phi_lambda` readout: identifying the framework three-fold
`hw=1` structure with the charged-lepton, quark, or neutrino species labels.

This note does not add a repo-wide axiom and does not treat the physical
`Cl(3)` local algebra on the `Z^3` spatial substrate as a new premise. It
also does not introduce `C_3`-breaking dynamics. Under those constraints,
the current package supplies no reviewed derivation of the required species
label readout.

## Salvaged Result

The durable part of this stretch attempt is a narrow open-gate boundary:

1. The direct central-label route fails inside the `M_3(C)` algebra carried
   by the `hw=1` three-fold structure. The companion runner verifies
   `Z(M_3(C)) = C * I_3`, so there are no nontrivial central projections
   available inside that algebra to label three classical species sectors.
2. The route/probe context already records several attacks on this readout
   problem, especially the AC-readout no-proper-quotient route
   [`A3_ROUTE5_NO_PROPER_QUOTIENT_SHARPENED_OBSTRUCTION_NOTE_2026-05-08_r5.md`](A3_ROUTE5_NO_PROPER_QUOTIENT_SHARPENED_OBSTRUCTION_NOTE_2026-05-08_r5.md)
   and the bounded BAE synthesis
   [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md).
   Those records are useful route-pruning evidence, but many of them remain
   unaudited, so this note does not promote their combined coverage to a
   retained no-go theorem.
3. The preserved-`C_3` interpretation in
   [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
   is consistent with the boundary: preserving the symmetry gives a
   three-fold structure, not a derived species-label ordering.

Therefore this note records an `open_gate`, not a status promotion for the
substep-4 theorem. A later positive ratchet would need one of the following:

- a reviewed theorem deriving the species-label readout from the current
  source package without adding a new axiom;
- explicit user approval for an admitted labeling premise, kept scoped as an
  import until retired by later science;
- a reviewed `C_3`-breaking dynamics result that supplies the readout.

## Runner Role

The runner is intentionally modest. It checks the finite matrix-algebra fact
that `M_3(C)` has only scalar central elements, and it keeps a bookkeeping
table showing that the current route/probe notes already name the major
recorded attacks on the readout problem. The bookkeeping table is not an
exhaustiveness proof and is not an audit verdict.

## Non-Claims

- No promotion of
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
  is proposed here.
- No observed masses, PDG values, fitted coefficients, or lattice Monte Carlo
  measurements are used.
- No new axiom, species-label axiom, or repo-wide vocabulary is admitted.
- No claim is made that all possible future readout routes are impossible.

## Reproduction

```bash
python3 scripts/frontier_staggered_dirac_substep4_positive_ratchet.py
```

Expected result: `PASS=4 FAIL=0`. A passing run supports only the open-gate
boundary above.
