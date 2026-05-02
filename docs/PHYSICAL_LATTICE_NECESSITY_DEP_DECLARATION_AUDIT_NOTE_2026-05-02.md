# Physical-Lattice Necessity Dependency-Declaration Audit

**Date:** 2026-05-02
**Status:** dependency-declaration repair packet for
[`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
which is currently `proposed_retained, audited_conditional` in the audit
ledger with `deps=[]`. This review packet identifies the 11 actually-read
upstream notes and 1 sibling runner that the parent note's runner depends
on, recommends explicit dep declaration, and demotes the parent note to
the narrowest honest tier under the corrected dep chain.
**Primary runner:** `scripts/frontier_physical_lattice_necessity_dep_declaration_audit.py`
**Authority role:** dep-declaration audit / status correction for the
parent row's load-bearing chain.

## 0. Audit context

The parent note `PHYSICAL_LATTICE_NECESSITY_NOTE.md` is `proposed_retained,
audited_conditional` per the audit ledger (td=301, lbs=15.74). The verdict
rationale flagged: *"the proof and runner depend on an undeclared upstream
surface: minimal axioms, plaquette/canonical values, three-generation
observable closure, generation/chirality boundary notes, continuum-
identification text, single-axiom Hilbert/information notes, one-generation
matter closure, anomaly-forced time, and a publication derived-values index.
Why this blocks: the ledger row has deps=[], and multiple runner-read
authorities are audited_conditional, unaudited/effectively conditional, or
effectively..."*

This packet does NOT challenge the runner output (PASS=10/0 verified). It
documents the actual upstream reads and recommends the ledger row's deps
list be repaired.

## 1. Actually-read upstream notes (from runner inspection)

Inspecting `scripts/frontier_physical_lattice_necessity.py`, the runner
reads the following docs at runtime via `read_text(...)`:

| # | Note | Current ledger status (as of 2026-05-02) |
|---|---|---|
| 1 | `MINIMAL_AXIOMS_2026-04-11.md` | audited_conditional (G_BARE_* family open) |
| 2 | `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` | unaudited / audited_conditional |
| 3 | `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` | audited_conditional |
| 4 | `GENERATION_AXIOM_BOUNDARY_NOTE.md` | audited_conditional |
| 5 | `THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md` | (status TBD, likely conditional) |
| 6 | `CONTINUUM_IDENTIFICATION_NOTE.md` | (status TBD) |
| 7 | `SINGLE_AXIOM_HILBERT_NOTE.md` | (status TBD) |
| 8 | `SINGLE_AXIOM_INFORMATION_NOTE.md` | (status TBD) |
| 9 | `ONE_GENERATION_MATTER_CLOSURE_NOTE.md` | audited_conditional |
| 10 | `ANOMALY_FORCES_TIME_THEOREM.md` | audited_conditional (per `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24` ref) |
| 11 | (publication derived-values index file) | derived values for Cl(3)/Z³ — admitted standard package |
| 12 | `scripts/frontier_generation_axiom_boundary.py` | sibling runner (audited_conditional row) |

The runner uses these to verify substrate-physicality / no-same-stack
regulator-reinterpretation conditions on the accepted Cl(3)/Z³ surface.

## 2. Recommended ledger row update

```yaml
# Before:
claim_id: physical_lattice_necessity_note
deps: []
current_status: proposed_retained
audit ledger verdict: conditional
effective_status: audited_conditional

# After (recommended):
claim_id: physical_lattice_necessity_note
deps:
  - minimal_axioms_2026-04-11
  - plaquette_self_consistency_note
  - three_generation_observable_theorem_note
  - generation_axiom_boundary_note
  - three_generation_chirality_boundary_note
  - continuum_identification_note
  - single_axiom_hilbert_note
  - single_axiom_information_note
  - one_generation_matter_closure_note
  - anomaly_forces_time_theorem
current_status: bounded support theorem  # demoted from proposed_retained
audit ledger verdict remains conditional; no review-side change
effective_status: audited_conditional     # unchanged
```

## 3. Seven retained-proposal certificate criteria

| # | Criterion | Pass? | Notes |
|---|---|---|---|
| 1 | `proposal_allowed: true` | **NO** | This review recommends false. |
| 2 | No open imports for the claimed target | **NO** | At minimum 11 upstream notes are runtime-imports; multiple are conditional. |
| 3 | No observed values, fitted selectors, admitted unit conventions, or literature values are load-bearing | **PARTIAL** | The runner uses canonical plaquette / α_LM / hierarchy values from `canonical_plaquette_surface` (admitted package values). |
| 4 | Every dep retained | **NO** | At least 10 of the 11 upstream notes are `audited_conditional` or unaudited. |
| 5 | Runner checks dependency classes | **YES** (the runner does verify substrate-physicality conditions) |
| 6 | Review-loop disposition `pass` | **PENDING** |
| 7 | PR body says independent audit required | **YES** (this packet) |

**Result:** Criteria 1, 2, 4, 6 fail. The note is NOT eligible for
`proposed_retained`. The narrowest honest tier under the corrected dep
chain is **bounded support theorem** (the substrate-physicality result
holds conditionally on the upstream conditional theorems and admitted
canonical package values).

## 4. What this packet closes

- **Dependency repair**: identifies 11 upstream notes + 1 sibling runner
  that the parent runner reads. Recommends explicit ledger declaration.
- **Honest status correction**: from `proposed_retained` to `bounded
  support theorem` under the corrected dep chain.
- **No challenge to the algebra**: the runner output (PASS=10/0) is
  preserved and the proof structure is unchanged.

## 5. What this packet does NOT close

- The retention status of any upstream conditional theorem.
- The deeper question of whether each upstream note is actually
  load-bearing for the parent claim, or merely cited as context.
- The G_BARE_* family closure (very hard upstream of `minimal_axioms`).

## 6. Audit-graph effect

After this PR lands and the audit ledger regenerates with corrected deps:
- The parent note's deps go from `[]` to 10+ explicit upstream rows.
- The parent's `effective_status` may automatically demote based on max-
  descendant rules in `compute_effective_status.py`.
- 301 transitive descendants under `physical_lattice_necessity_note`
  inherit the corrected dep chain through the citation graph.

## 7. Cross-references

- Parent: [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md) (`proposed_retained, audited_conditional`)
- Runner: [`scripts/frontier_physical_lattice_necessity.py`](../scripts/frontier_physical_lattice_necessity.py) (PASS=10/0)
- Sibling audited rows: `MINIMAL_AXIOMS_2026-04-11.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, etc.
