# DM Neutrino Odd-Circulant Current-Stack Zero Law

**Date:** 2026-04-15  
**Status:** exact current-stack theorem on the last local DM coefficient slot  
**Script:** `scripts/frontier_dm_neutrino_odd_circulant_current_stack_zero_law.py`

## Question

Given the exact local odd-slot theorem on the DM circulant family, what
activation law does the stack currently retained today assign to that slot?

## Bottom line

The current-stack law is the zero law:

`c_odd,current = 0`.

The reason is structural.

The current local DM bank is built from residual-`Z_2`-even data:

- the exact weak-axis `1+2` split `diag(a,b,b)`
- the even circulant bridge it induces
- Hermitian/scalar/equivariant functionals of that same even data

Any residual-`Z_2`-equivariant functional of a residual-`Z_2`-even input is
again residual-`Z_2` even, so its projection onto the unique odd circulant slot
vanishes.

Therefore the exact present-tense local coefficient law on the retained stack
is not “unknown.” It is the zero law.

## Theorem-level statement

**Theorem (Current-stack zero law for the odd circulant coefficient).** Assume
the exact weak-axis `1+2` local split, the exact even circulant bridge it
induces, and the retained support/Hermitian/scalar DM bank built as
residual-`Z_2`-equivariant functionals of that even data. Then the unique odd
circulant coefficient on the DM Hermitian kernel obeys

`c_odd,current = 0`.

Therefore any future positive DM coefficient law must introduce a genuinely new
residual-`Z_2`-odd bridge or activator.

## What this closes

This closes the present-tense activation question on the current stack.

The branch no longer needs to say:

- “the odd coefficient might already be hiding in the current bank”
- “maybe one more scalar/Hermitian functional turns it on”

Those routes are closed on the current retained stack.

## What this does not close

This note does **not** prove that no future extension can realize
`c_odd != 0`.

It proves that the present retained stack does not.

## Command

```bash
python3 scripts/frontier_dm_neutrino_odd_circulant_current_stack_zero_law.py
```

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_odd_circulant_current_stack_zero_law.py
```

Last run (2026-05-10): `PASS=6 FAIL=0` on the present worktree. The
runner exercises class A finite-dimensional algebra: residual-`Z_2`
parity assignment on representative even-input matrices in
`diag(a,b,b)` form and on circulant outputs of the form
`d I + c_even (S + S^2) + i c_odd (S - S^2)`, equivariance preservation
under explicit Hermitian/scalar functionals, and the `c_odd = 0`
projection on each constructed example.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing parity-preservation step relies on, in
response to the prior 2026-05-05 audit feedback's `missing_dependency_edge`
repair target (audit row:
`dm_neutrino_odd_circulant_current_stack_zero_law_note_2026-04-15`).
It does not promote this note or change the claim scope, which
remains the conditional structural conclusion that on the assumed
retained DM bank built from residual-`Z_2`-even data by residual-`Z_2`
equivariant Hermitian/scalar functionals, the unique odd circulant
slot satisfies `c_odd,current = 0`.

One-hop authority candidates cited:

- [`DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md)
  — audit row:
  `dm_neutrino_odd_circulant_z2_slot_theorem_note_2026-04-15`. Sibling
  source authority establishing the unique residual-`Z_2`-odd
  circulant slot
  `K = d I + c_even (S + S^2) + i c_odd (S - S^2)` with `c_odd` the
  unique residual-`Z_2`-odd coefficient under `P_23` exchange, which is
  the slot whose vanishing the present note records on the current
  retained bank. This supplies cited one-hop support on the unique
  odd-slot identification while independent audit decides chain impact.
- [`DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
  — audit row:
  `dm_neutrino_dirac_bridge_theorem_note_2026-04-15`. Sibling source
  authority on the local Dirac-structure algebra carrying the
  even-circulant bridge induced by the weak-axis split `diag(a,b,b)`,
  cited here as the upstream-source authority for the even-bridge
  premise the zero-law conclusion projects onto.
- [`DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md`](DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md)
  — audit row:
  `dm_neutrino_two_higgs_right_gram_bridge_note_2026-04-15`. Sibling
  candidate authority on the canonical Hermitian circulant kernel
  `K = Y^dag Y` that supplies the explicit even/odd circulant
  decomposition the present note projects onto. This is listed as a
  candidate dependency while independent audit decides whether it closes
  the edge.

Open class D registration targets named by the prior 2026-05-05 audit
feedback as `missing_dependency_edge`:

- A retained-grade source packet establishing the exact weak-axis
  `1+2` split, the induced even bridge, and the exhaustive
  characterization of the retained DM bank as residual-`Z_2`-even data
  remains required to lift the equivariance import to a chain-closing
  one-hop authority.
- A retained-grade theorem that the present DM observable bank is
  exactly the equivariant-Hermitian/scalar closure of the even-data
  inputs, rather than a representative subset, remains required to
  lift the bank-exhaustion premise.

## Honest auditor read

The 2026-05-05 independent audit on the previous note revision recorded
this row as conditional with load-bearing-step class A and
`chain_closes=False`, observing that the
equivariance-preservation algebra is valid on its own terms but that
the restricted packet imports the exact weak-axis split, the even
bridge, the odd-slot theorem, and the characterization of the retained
DM bank as assumptions rather than retained-grade inputs. The runner
`scripts/frontier_dm_neutrino_odd_circulant_current_stack_zero_law.py`
is registered with `runner_check_breakdown = {A: 6, B: 0, C: 0, D: 0,
total_pass: 6}` and verifies the conditional projection on
representative 3x3 examples (`PASS=6 FAIL=0` on 2026-05-10). The cite
chain above wires the odd-slot theorem source authority and the
Dirac-bridge source authority as one-hop sibling support and
explicitly registers the two missing-dependency-edge targets named by
the prior feedback's `notes_for_re_audit_if_any` field. After this
source edit, the independent audit lane owns any current verdict and
effective status; this addendum does not request promotion.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the prior audit feedback expected, the runner
that exercises the conditional projection, and the
missing-dependency-edge targets named by the prior feedback's
`notes_for_re_audit_if_any` field. It mirrors the live cite-chain
pattern used by the
`PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md` cluster
(commit `44da750e2`) and the
`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` cluster
(commit `8e84f0c23`). Vocabulary is repo-canonical only.
