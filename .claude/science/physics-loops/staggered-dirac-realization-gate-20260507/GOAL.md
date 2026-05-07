# Staggered-Dirac Realization Gate Closure (12h Campaign)

**Slug:** staggered-dirac-realization-gate-20260507
**Started:** 2026-05-07
**Runtime budget:** 12h unattended
**Mode:** campaign
**Worktree:** `/Users/jonreilly/Projects/Physics/.claude/worktrees/lucid-shamir-41757b`

## High-level goal

Close the **staggered-Dirac realization gate** (formerly axiom A3 per
[`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md)).
Per the open-gate parent
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](../../../../docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md),
the gate requires forcing four substeps from A1 (Cl(3) local algebra)
+ A2 (Z³ substrate):

1. Forcing the Grassmann fermion realization on the A1+A2 surface
   (rather than admitting it as an independent axiom)
2. Forcing the staggered-Dirac kinetic structure on Z³ from A1+A2
3. Forcing the BZ-corner doubler structure (8 corners → 1+1+3+3 by
   Hamming weight)
4. Forcing the physical-species reading of the hw=1 triplet as three
   SM matter generations on the accepted Hilbert/locality/information
   surface

Pieces of (1)-(4) exist scattered across multiple notes. Closure
requires either a single canonical proof packet running (1)-(4)
end-to-end on A1+A2, or a coordinated chain of retained-grade
theorems that together discharge each step.

## Block plan (12h budget, ~90m deep blocks)

### Block 01: Assumption ledger + forcing-gap map (~60m)
- Audit existing pieces: `AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`,
  `CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`,
  `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, etc.
- Map which substeps (1)-(4) are already covered by retained theorems
  and which have explicit forcing gaps
- **Hypothesis to verify**: Spin-statistics theorem (S2) already gives
  Grassmann-forcing from finite per-site Cl(3) dim 2; obstruction 1 is
  effectively closed but needs explicit packaging citation chain.

### Block 02: Substep (1) — Grassmann partition forcing (~60-90m)
Package the spin-statistics theorem's (S2) argument as the explicit
forcing of substep 1: bosonic Fock incompatible with finite-dim Cl(3)
module → Grassmann is the unique consistent matter measure on A1+A2.

### Block 03: Substep (2) — Kawamoto-Smit phase forcing (~90m)
Hardest of the four. Show that A1+A2 + Cl(3) chirality (sublattice
parity ε(x) = (−1)^{x+y+z}) + per-site Pauli realization FORCES
specific Kawamoto-Smit phases η_1=1, η_2(n)=(−1)^{n_1}, η_3(n)=(−1)^{n_1+n_2}
(modulo gauge/equivalence). Use `frontier_generation_rooting_undefined.py`
irreducibility result + chirality grading from `FERMION_PARITY_Z2_GRADING_THEOREM`.

### Block 04: Substep (3) — BZ-corner three-generation forcing (~90m)
Show A1+A2 + staggered-Dirac structure FORCES the 8-corner BZ
doubling decomposition `1 + 3 + 3 + 1` by Hamming weight, with the
hw=1 triplet identified as three matter generations. The retained
`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE` covers exact-irreducibility
of the hw=1 M_3(C) algebra; closure step is forcing the BZ corner
decomposition itself from A1+A2 + staggered-Dirac.

### Block 05: Substep (4) — Physical-species bridge (~60-90m)
Step from "exact observable separation + no-proper-quotient closure"
to "physically distinct species sectors of the accepted theory" on
Hilbert/locality/information surface.

### Block 06: Single canonical parent packaging (~60m)
If Blocks 02-05 close all four substeps: synthesize into a single
canonical-parent positive theorem `STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_2026-05-07`
that runs the chain end-to-end. Replaces `STAGGERED_DIRAC_REALIZATION_GATE_NOTE`
as the canonical parent identity.

If any substep doesn't close: produce a sharp obstruction note
identifying the precise remaining gap as a clean axiom-addition
target.

### Block 07+ (if runtime remains)
- **SM-fermion taste-vertex assignment** (Block 05's open question
  from the bridge-gap campaign): does the staggered-Dirac realization
  identify which gl(1) commutant U(1) factor corresponds to U(1)_Y?
- Cross-validation runners
- Round-2 hostile review

## Hard constraints (forbidden imports)

- NO PDG observed values
- NO lattice MC empirical measurements as derivation inputs
- NO fitted matching coefficients
- NO same-surface family arguments
- NO load-bearing literature numerical comparators
- Standard machinery (Lie-algebra rep theory, Schur orthogonality,
  Brillouin zone analysis, Kawamoto-Smit construction, spectral analysis,
  finite Grassmann calculus) is admissible standard machinery in
  narrow non-derivation roles

## Hard wording bans (per controlled vocabulary + skill protocol)

- No bare `retained` / `promoted` in branch-local Status: lines
- No `retained branch-local`, `would become retained`, `promote to retained`
- Use `bounded support theorem`, `exact support theorem`, `open`,
  `no-go`, `demotion`, `proposed_retained` (audit-ready proposal only)

## Stop conditions

- 12h runtime exhausted
- Corollary exhaustion
- Volume cap: 5 PRs / 24h
- Cluster cap: judgment-based evaluator at PR ≥ 3 in
  `staggered_dirac_*` family (per new PR #624 governance)
- Global queue exhaustion

## Cross-references

- Parent open-gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](../../../../docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md)
- Per-site dim 2: [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
- Cl(3) per-site uniqueness: [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](../../../../docs/AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
- Spin-statistics: [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](../../../../docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md) — KEY PIECE
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](../../../../docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Three-generation no-proper-quotient: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](../../../../docs/THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
- Three-generation structure: [`THREE_GENERATION_STRUCTURE_NOTE.md`](../../../../docs/THREE_GENERATION_STRUCTURE_NOTE.md)
- Physical-lattice necessity: [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](../../../../docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- Fermion parity Z_2 grading: [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](../../../../docs/FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md)
- CPT exact: [`CPT_EXACT_NOTE.md`](../../../../docs/CPT_EXACT_NOTE.md)
- No-rooting irreducibility: `scripts/frontier_generation_rooting_undefined.py`
- Sister bridge-gap exhausted-routes: [`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md) (different lane; cited as no-go memory)
