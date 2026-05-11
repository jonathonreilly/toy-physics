# PMNS Selector-Bank Nonrealization

**Date:** 2026-04-15
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** support - structural or confirmatory support note
the remaining PMNS selector gap
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_selector_bank_nonrealization.py` (PASS=10 FAIL=0 on current main; the runner now reads `HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md` for the q_H datum, accepts both ASCII and unicode q_H notation)

## Cited authorities (one hop)

The 2026-05-03 citation-graph repair registers the load-bearing one-hop
deps referenced in plain text above as proper markdown links so the
audit-graph builder picks up the edges.

- [`HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md`](HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md)
  — supplies the Higgs `Z_3` datum `q_H ∈ {0, +1, -1}` that the
  nonrealization runner reads for its primary check.

## Question

After checking the atlas bank axiom-first, do the existing exact selector tools
already realize the missing PMNS selector under another name?

## Bottom line

No.

The current exact selector bank contains real selector tools, but they act on
other domains:

- graph-axis selection on the cube-shift triplet
- temporal-orbit selection on the APBC circle
- scalar-axis selection on the EWSB quartic surface

The remaining PMNS selector question lives on a different exact data set:

- the Higgs `Z_3` datum `q_H in {0,+1,-1}`
- the minimal neutrino-side versus charged-lepton-side PMNS branch bit

No current retained selector theorem bridges those domains.

So the selector gap is not hiding elsewhere in the bank under another exact
selector name.

## Atlas and axiom inputs

This theorem reuses:

- `Graph-first selector`
- `Hierarchy bosonic-bilinear selector`
- the exact `EWSB quartic selector` statement carried in the hierarchy/CKM lane
- `Neutrino Higgs Z_3 underdetermination`
- `PMNS minimal-branch nonselection`

## Why this is stronger than just saying “still open”

The bank now contains multiple exact selector tools, so “the selector is still
open” could in principle mean either:

1. there is no selector machinery yet, or
2. selector machinery exists but does not yet touch the PMNS datum

The current theorem proves the second.

## Selector domains already present in the bank

### Graph-first selector

The graph-first selector acts on the canonical cube-shift triplet

`H(phi) = sum_i phi_i S_i`

and selects axis minima in that graph-source space.

### Bosonic-bilinear selector

The hierarchy bosonic-bilinear selector acts on APBC temporal support and
selects the unique minimal resolved orbit

`L_t = 4`.

### Quartic EWSB selector

The exact quartic selector in the hierarchy/CKM lane acts on scalar-axis
directions and breaks `S_3 -> Z_2`.

## Why none of these closes the PMNS selector

The PMNS selector question is not:

- which graph axis is selected
- which APBC temporal orbit is selected
- which scalar axis minimizes the quartic potential

It is:

- which Higgs `Z_3` datum is realized on the lepton Yukawa lane
- and, on the minimal-branch assumption, whether the neutrino or
  charged-lepton sector is the first non-monomial lepton lane

The current bank still has:

- `q_H` underdetermined in `{0,+1,-1}`
- minimal PMNS-producing branches isolated but not selected

No retained bridge theorem maps the existing selector outputs into that PMNS
branch datum.

## The theorem-level statement

**Theorem (Current-bank nonrealization of the PMNS selector).** Assume the
current exact selector bank given by the graph-first selector, the hierarchy
bosonic-bilinear selector, and the exact quartic selector statement on the
hierarchy/CKM lane, together with the exact Higgs-`Z_3` underdetermination and
PMNS minimal-branch nonselection theorems. Then:

1. the current bank contains exact selector tools
2. those tools act on graph-axis, temporal-orbit, and scalar-axis domains
3. the current bank still leaves the Higgs `Z_3` datum and minimal PMNS branch
   unselected

Therefore none of the existing exact selector tools realizes the missing PMNS
branch selector.

## What this closes

This closes the “maybe the selector is already in the bank under another name”
escape route.

It is now exact that:

- the current bank is not missing selector technology in general
- it is missing the specific bridge selector needed for the lepton/PMNS lane

## What this does not close

This note does **not** prove:

- that a PMNS selector theorem is impossible
- which minimal branch nature picks
- the seven canonical quantities on either branch

It is a current-bank boundary theorem only.

## Command

```bash
python3 scripts/frontier_pmns_selector_bank_nonrealization.py
```


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
