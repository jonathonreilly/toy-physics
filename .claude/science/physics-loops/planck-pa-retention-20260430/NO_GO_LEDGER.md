# No-Go Ledger

## PR #228 Carrier Derivation Verdict

Artifact:
`docs/PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md`

Audit verdict: `audited_renaming`.

Load-bearing failure:

```text
rank(P_A H_cell) = 4
```

was matched to the irreducible complex `Cl_4(C)` module, but the substrate
did not prove that `P_A H_cell` is the uniquely active invariant block.

## Substrate-To-P_A Forcing Attempt

Artifact:
`docs/SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`

Result: clean negative witness.

The Hamming-weight-three projector `P_3` is rank four, tensor-local,
complex-linear, and equivariant under the same spin/time/CPT actions. The
runner also enumerates 17 local rank-four equivariant projector classes.

Repair target left open: add an independently derived first-order
boundary/orientation law that excludes the Hodge-dual sector.

## First-Order Coframe Unconditionality Attempt

Artifact:
`docs/FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md`

Result: clean negative witness.

The Hodge-complement map exchanges `P_1` and `P_3`:

```text
* P_1 *^{-1} = P_3
```

while preserving spatial spin-lift equivariance, CPT grading, tensor-local
number algebra, and time parity up to the irrelevant central sign.

Repair target left open: a law that selects one-form normal incidence over
the Hodge-dual three-form surface carrier.

## Consequence

The remaining possible routes must derive a directionality/asymmetry not
already present in the symmetry package. Any route whose only distinction is
"first order is the boundary carrier" is circular.

## Boundary Orientation / Incidence Stretch

Artifact:
`docs/PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md`

Runner:
`scripts/frontier_planck_boundary_orientation_incidence_no_go.py`

Result: new negative witness, seeded into the audit queue as
`unaudited`.

The oriented primitive four-cell boundary has complementary descriptions:

```text
normal one-forms in P_1
oriented three-form faces / fluxes in P_3
```

The Hodge map gives an exact perfect pairing between them. Boundary incidence
therefore identifies `P_1` and `P_3`; it does not choose `P_1`. A cochain-
normal primitivity rule would select `P_A`, but that rule is the extra
boundary/orientation premise.

## Link-Local First-Variation Bypass

Artifact:
`docs/PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`

Runner:
`scripts/frontier_planck_link_local_first_variation_p_a_forcing.py`

Result: positive intrinsic candidate; current audit graph effective status is
conditional pending upstream authority cleanup/audit.

This does not overturn the no-gos above. It bypasses their surface. The no-gos
act on substrate symmetries, Hodge-dual boundary incidence, and abstract
"first-order" language. The new route uses the accepted microscopic action
surface:

```text
finite Grassmann / staggered-Dirac link-local action
  -> source differential dS_link(du_a)
  -> one-axis support P_1 = P_A.
```

The Hodge-dual `P_3` remains a valid face/flux representation, but it is not
in the fundamental one-link source differential domain. It is a Hodge image or
third-composite support.

Audit pressure retained in the ledger: if the audit treats the action-source
differential as an extra active-response premise rather than accepted
microscopic action structure, this route demotes to conditional support.
