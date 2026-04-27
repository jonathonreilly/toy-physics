# Hubble H_0 — Artifact Plan

**Workstream:** `hubble-h0-20260426`

## Cycle 1 — Route R4 (Hubble Tension Structural Lock)

**Artifact set:**

1. `docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`
   - Theorem statement, premise list, proof sketch, falsifier, scope.
   - Cross-references to retained `w = -1`, matter-bridge, inverse
     reconstruction.
2. `scripts/frontier_hubble_tension_structural_lock.py`
   - Symbolic verification (sympy): late-time `D_L(z)`, `D_A(z)`, `H(z)` are
     functions of `(Omega_r, Omega_m, Omega_Lambda, H_0)` only.
   - Numerical verification: scan `z in [0, 1]`, confirm `H(z)/H_0` is fixed
     by `(Omega_r, Omega_m, Omega_Lambda)` independent of any late-time
     parametric modification (zero-modification baseline reproduces ΛCDM).
   - Includes a parametric "modified late-time DE" stress test that confirms
     any non-trivial `w(z)` modification at `z < z_recomb` violates retained
     `w_Lambda = -1`.
3. `logs/2026-04-26-hubble-tension-structural-lock.txt`
   - Paired log of (2) with `PASS`/`FAIL` summary.

**Acceptance criteria:**

- Theorem statement is sharp: identifies retained premises, the function
  identity, and the falsifier.
- Runner PASSes all symbolic and numerical checks.
- Review-loop disposition recorded in `REVIEW_HISTORY.md`.

**Anti-pattern guard:**

- The theorem must NOT silently re-import any number it does not need
  (e.g., specific Planck-2018 values for `Omega_Lambda` are comparators in
  the runner, not premises in the theorem).
- The theorem must NOT claim a numerical value for `H_0`. It only locks the
  structural form of late-time observables.

## Cycle 2 (tentative) — Route R3 (Open-Number Reduction)

If Cycle 1 lands cleanly, Cycle 2 produces:

1. `docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`
2. `scripts/frontier_cosmology_open_number_reduction.py`
3. paired log

This formalizes the parameter-count statement that the bounded cosmology
surface has exactly two open structural numbers `(H_0, L)`.

## Cycle 3 (tentative) — Route R5 (eta retirement audit)

If runtime permits and Cycles 1-2 land, Cycle 3 produces:

1. `docs/HUBBLE_LANE_ETA_RETIREMENT_AUDIT_NOTE_2026-04-26.md`
2. cross-reference table identifying the minimal selector/normalization
   closure for the surviving DM leptogenesis branches

## Repo-wide weaving (not done in workstream — recorded in HANDOFF)

When this branch is later merged into `main` review pipeline:

- Update `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` §5
  (cosmology-windows row) to cite the structural lock theorem.
- Update `docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md` to
  reflect the new Hubble tension stance.
- Add an entry to `docs/publication/ci3_z3/CLAIMS_TABLE.md` (or equivalent)
  for the structural lock claim.
- Add the new theorem note to `docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`
  Section 4 scaffolding list.

These weaves are NOT applied in the workstream branch per skill
"science-only" delivery policy.
