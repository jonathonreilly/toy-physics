# HANDOFF — Cycle 21 PMNS Branch Selector

## What this cycle delivered

Cycle 21 of the follow-on campaign (parallel
agents on cycles 20, 21, 22) addressed Cycle 09 Obstruction 2
(branch selector ambiguity).

## Output

- **Note**: `docs/PMNS_BRANCH_SELECTOR_CP_SHEET_BLINDNESS_NOTE_2026-05-03.md`
- **Runner**: `scripts/frontier_pmns_branch_selector.py`
- **Loop pack**: `.claude/science/physics-loops/pmns-branch-selector-2026-05-03/`

## Output type

(c) — stretch attempt with named negative-structural obstruction.

## Key result

The framework's two partial η/η_obs predictions live on **different
theorem-frame surfaces**, not on a "shared selector space":

- **Branch A** (one-flavor reduced surface): η/η_obs = 0.18879
  computed from cycle 18's `(516/53009) · Y₀² · F_CP · κ_axiom`
  decomposition. This is NOT a selector output; it is a
  deterministic transport-chain numerical value on the reduced
  one-flavor surface.

- **Branch B** (PMNS-assisted off-seed source on N_e seed surface):
  η/η_obs = 1.0 from any of the four candidate selectors (min-info,
  observable-relative-action, transport-extremal, continuity-
  closure). All four are output of selectors with even objectives.

The CP-sheet blindness theorem proves all four Branch-B selectors
are even under δ → -δ while the source channel γ = x₁y₃ sin(δ)
is odd. So every Branch-B "winner" comes paired with its CP-
conjugate. **Branch B cannot uniquely select a baryogenesis
witness** under the current selector bank.

By exclusion, the only current-bank branch with a deterministic
unique numerical output already documented by prior transport/
decomposition surfaces is Branch A. **Cycle 21's result is an
open-gate structural exclusion of Branch B's parity-degenerate
selector bank**, modulo independent audit-lane treatment.

## Audit-lane handoff items

1. **Verify CP-sheet blindness applies to ALL FOUR selectors**.
   The runner does this symbolically. Reviewer should cross-check
   in `DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16`.

2. **Verify cycle 18's decomposition is on Branch A**.
   The cycle 18 note explicitly says "exact one-flavor radiation-
   branch transport on the reduced one-flavor surface".

3. **Verify the Branch A vs Branch B distinction**.
   The cycle 09 transport-status note documents both branches.

4. **Cross-check no new forbidden imports**.
   Cycle 21 introduces no derivation inputs not already in the
   prior-cycle dependency chain.

## Inherited obstructions (not new)

- cycle 09 O1 / cycle 12 R2 / cycle 15 R1: Y₀² phenomenological
  import.
- cycle 09 O3: α_LM mass scale.
- "Right-sensitive 2-real Z_3 doublet-block selector law": cycle
  09 transport-status open object.

## What cycle 21 leaves open

- A POSITIVE Branch-B selector (CP-odd objective) is not constructed.
- The Branch-A vs Branch-B frame question — i.e., "is the framework
  ontologically committed to the one-flavor reduced surface
  (Branch A) or to the PMNS-assisted three-flavor seed surface
  (Branch B)?" — is not closed; it is sharpened to "Branch B's
  current selector bank is parity-degenerate, so Branch A is
  uniquely deterministic under the current bank".
- The numerical mismatch `0.1888 ≠ 1.0` is NOT explained by cycle
  21 (and not the focus of this cycle); the discrepancy is
  inherited from upstream Y₀² and PMNS chart-constant residuals.

## Next exact action (post-cycle-21)

For the audit-lane:
- Review PR for cycle 21 against V1-V5 gate.
- Cross-check the parity-symbolic verification in the runner.

For the next physics-loop campaign (deferred):
- Tackle the right-sensitive 2-real Z_3 doublet-block selector
  law from minimal premises. This is the remaining open object.

## Concurrency note

Cycles 20 and 22 of this follow-on campaign are running in parallel
agents in OTHER worktrees. Cycle 21's branch is isolated to
`physics-loop/pmns-branch-selector-2026-05-03`. No shared files
modified outside the cycle-21 PR scope.
