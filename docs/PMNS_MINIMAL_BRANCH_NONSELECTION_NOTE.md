# PMNS Minimal-Branch Current-Atlas Nonselection Theorem

**Date:** 2026-04-15 (publication-state references narrowed 2026-05-01)
**Status:** support - structural or confirmatory support note
PMNS-producing branches
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_minimal_branch_nonselection.py`
(`PASS = 8, FAIL = 0`)

**2026-05-01 publication-state note:** The
`HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17`
upgraded `q_H = 0` to GAUGE (retained), the CKM lane was promoted to
retained quantitative closure, and the PMNS boundary packet was
rewritten as a thin redirect to the live retained-lane packet. The
publication-control wording the previous runner asserted ("CKM /
quantitative flavor open", "frozen-out exact review packet",
validation-map "Higgs `Z_3` universality" blocker line) was therefore
rotated out. The note's actual claim — branch isolation without
selection — is preserved by the live atlas rows for "PMNS
minimal-branch nonselection", "Neutrino Dirac two-Higgs canonical
reduction", "Charged-lepton two-Higgs canonical reduction", and the
companion "Lepton shared-Higgs universality underdetermination" plus
"Lepton shared-Higgs universality collapse" rows; the live gates note
keeps the universality lane open. The runner is narrowed to assert
against that current state; the underlying theorem is unchanged.

## Question

After isolating the exact minimal PMNS-producing branches,

- neutrino-side two-Higgs canonical branch
- charged-lepton-side two-Higgs canonical branch

does the current exact bank already select one of them or constrain its seven
canonical quantities?

## Bottom line

No.

The current exact bank has reached the following honest endpoint:

- the surviving minimal PMNS-producing branches are isolated
- their canonical reduction and parameter counts are known
- but the current atlas/package does **not** contain:
  - a retained Higgs-multiplicity selector
  - a retained shared-Higgs `Z_3` universality theorem
  - an exact bridge constraining the seven canonical quantities on either
    minimal branch

So the bank has isolation without selection.

## Atlas and package inputs

This theorem reuses:

- `Neutrino Dirac two-Higgs canonical reduction`
- `Charged-lepton two-Higgs canonical reduction`
- the PMNS boundary packet
- publication controls:
  - `DERIVATION_VALIDATION_MAP.md`
  - `PUBLICATION_MATRIX.md`
  - `CLAIMS_TABLE.md`
  - `GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md`

## Why this is an exact theorem rather than prose

The package already encodes three exact facts:

1. the minimal neutrino-side non-monomial branch exists and is canonical
2. the minimal charged-lepton-side non-monomial branch exists and is canonical
3. flavor closure remains open because Higgs-`Z_3` universality is still a
   remaining blocker

The current atlas therefore supports a precise theorem:

- branch isolation is present
- branch selection is not

This is not just narrative caution. It is a true current-bank boundary.

## The theorem-level statement

**Theorem (Current-atlas nonselection of minimal PMNS-producing branches).**
Assume the exact PMNS boundary packet, the exact neutrino-side two-Higgs
canonical reduction theorem, and the exact charged-lepton-side two-Higgs
canonical reduction theorem. Then:

1. the current exact bank isolates the minimal neutrino-side and
   charged-lepton-side PMNS-producing branches
2. the publication controls still record Higgs-`Z_3` universality / flavor
   selection as open
3. the current atlas contains no retained Higgs-multiplicity selector, no
   retained shared-Higgs `Z_3` universality theorem, and no exact bridge
   constraining the seven canonical quantities on either minimal branch

Therefore the current exact bank does not yet select among the surviving
minimal PMNS-producing branches and does not yet derive their canonical
invariants.

## What this closes

This closes the last honest structural ambiguity about the current branch state.

It is now exact that the remaining work is not:

- more branch hunting
- more support-class classification
- more parameter-count bookkeeping

It is instead one of:

- derive a selector theorem
- derive the seven canonical quantities on a chosen branch

## What this does not close

This note does **not** prove:

- that the selector theorem is impossible
- that the neutrino-side branch is preferred
- that the charged-lepton-side branch is preferred

It is a current-bank boundary theorem only.

## Command

```bash
python3 scripts/frontier_pmns_minimal_branch_nonselection.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `publication/ci3_z3/DERIVATION_ATLAS.md` (publication aggregator;
  backticked to avoid length-2 cycle — citation graph direction is
  *atlas → this_note*)
- [gauge_matter_closure_gates_2026-04-12](GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md)
