# Claude Execution Instructions

**Date:** 2026-04-12  
**Branch:** `claude/youthful-neumann`  
**Purpose:** use Claude time on execution and theorem-hunting, not on review. Codex will review the outputs afterward.

## Mission

Attack the remaining **high-impact open gates** for the full paper.

Work from the current audited state on `codex/review-active`, not from older broader claims.

## Current audited state you should assume

Closed enough to use in the paper backbone:

- exact native `Cl(3)` / `SU(2)`
- graph-first `SU(3)` structural closure
- anomaly-forced `3+1` closure on the **single-clock** theorem surface
- full-framework one-generation matter closure:
  - spatial graph gives left-handed gauge/matter structure
  - derived time gives chirality
  - anomaly cancellation fixes the right-handed singlet completion on the SM branch

Still open and high-value:

1. **Generation physicality**
2. **`S^3` compactification / cap-map uniqueness**
3. **DM relic mapping**
4. **Renormalized `y_t` matching**

Lower priority / bounded:

- CKM is still bounded on the Higgs-charge step
- gauge couplings are still bounded

## Priority order

1. `generation physicality`
2. `S^3 compactification`
3. `DM relic mapping`
4. `renormalized y_t`
5. `CKM` only if you can materially tighten the Higgs-charge step without stalling 1-4

## What counts as a real advance

### 1. Generation physicality

What would count as closure:

- a theorem or near-theorem that the `Z_3` orbit sectors are **physical matter families**, not just taste orbits
- or a sharp impossibility / obstruction theorem showing the current surface cannot do better without a new ingredient

What does **not** count:

- more orbit numerology
- more loose Wilson-entanglement rhetoric
- model-dependent hierarchy fits presented as proof of generation identity

Best acceptable outputs:

- a new theorem note stating the exact theorem or exact obstruction
- a script with only computed checks, no unconditional theorem-grade `PASS` on modeled assumptions

### 2. `S^3` compactification / cap-map uniqueness

What would count as closure:

- a theorem that the graph-to-closed-manifold compactification is forced, not merely minimal/canonical

What does **not** count:

- “finite regular graph means closed manifold” by assertion
- boundary-free rhetoric without a derived topological identification step

Best acceptable outputs:

- theorem note with exact assumptions
- script that checks only the actually computable pieces and clearly marks any still-external theorem input

### 3. DM relic mapping

What would count as closure:

- a derivation from graph-native quantities to the physical relic-law variables
  - graph dilution rate -> `3H`
  - graph equilibrium quantity -> `n_eq(T)` or equivalent
  - graph freeze-out threshold -> `x_F = m/T_F`

What does **not** count:

- just another Sommerfeld computation
- Boltzmann/Friedmann freeze-out with renamed variables

Best acceptable outputs:

- a theorem note on the graph-native freeze-out law and physical map
- a script whose final status explicitly separates:
  - native law closed
  - physical cosmology map closed or still open

### 4. Renormalized `y_t` matching

What would count as closure:

- a real derivation of the renormalized matching step replacing the current open
  `Z_Y(\mu) = Z_g(\mu)` gap

What does **not** count:

- repeating the bare theorem
- fitting the observed top mass or calling the IR result “close enough”

Best acceptable outputs:

- theorem note
- script focused on the renormalized identity only

## Required output format for every lane

For each serious attempt, produce **both**:

1. a note in `docs/`
2. a runnable script in `scripts/`

Naming pattern:

- `docs/<LANE>_THEOREM_NOTE.md`
- `scripts/frontier_<lane>.py`

Every note must contain exactly these sections:

1. `Status`
2. `Theorem / Claim`
3. `Assumptions`
4. `What Is Actually Proved`
5. `What Remains Open`
6. `How This Changes The Paper`
7. `Commands Run`

Every script must:

- end with a clear `PASS=n FAIL=m` summary
- avoid unconditional `True` theorem checks unless the item is explicitly labeled as a supporting remark
- separate:
  - exact checks
  - bounded/model checks
  - imported assumptions

## Required review packet

Before you ask Codex to review, create:

- `docs/CODEX_REVIEW_PACKET_2026-04-12.md`

That packet must list for each lane you touched:

- file paths changed
- exact commands run
- final script exit code
- claimed status: `closed`, `bounded`, or `open`
- one paragraph explaining why the claim is not overstated

This packet is mandatory. The point is to let Codex review only the deltas.

## Guardrails

- Do not silently widen the theorem assumptions.
- If a theorem depends on one extra assumption, state it explicitly.
- If a step is only model-level, call it `bounded`, not `closed`.
- If you find an obstruction theorem, that is a useful result. Document it cleanly instead of forcing closure language.
- Do not spend cycles beautifying prose before the theorem surface is right.

## Fast handoff targets

If you need one-liners for the paper while working:

- **Time lane:** closed on the single-clock theorem surface.
- **RH matter:** closed at the full-framework level, not from the spatial graph alone.
- **Generations:** still open until you can close physicality, not just orbit structure.

## Immediate ask

Start with the highest-value open gate:

1. generation physicality
2. `S^3` compactification

Only then move to DM relic mapping and renormalized `y_t`.
