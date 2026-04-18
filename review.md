# Review: `review/koide-charged-lepton-for-main`

Reviewed branch tip: `db8df07c`

## Verdict

Not cleared for `main`.

This branch has real exact candidate-route progress and the representative
Koide runners replay cleanly, so this is not a runtime rejection. But it still
stops one selector law short of a retained charged-lepton promotion, and the
branch is not yet packaged like a narrow `main` landing branch.

## Replay

Representative Koide runners replay cleanly:

- `scripts/frontier_koide_circulant_character_bridge.py`
  -> `PASS=9 FAIL=0`
- `scripts/frontier_koide_selected_slice_frozen_bank_decomposition.py`
  -> `PASS=9 FAIL=0`
- `scripts/frontier_koide_microscopic_scalar_selector_target.py`
  -> `PASS=12 FAIL=0`
- `scripts/frontier_koide_taste_cube_cyclic_source_descent.py`
  -> `PASS=15 FAIL=0`

So the current blocker set is about science status and landing scope, not about
broken runners.

## Findings

### [P1] Main Koide derivation still depends on two explicit non-retained steps

The load-bearing Koide note is still conditional in exactly the place that
matters for a `main` promotion.

- `A1` is introduced as the Frobenius-sector equipartition assumption and is
  explicitly described as the one load-bearing non-axiom step that is not
  retained on the current surface.
- `P1` is introduced as the non-retained identification `lambda_k = sqrt(m_k)`.
- `Q = 2/3` is then derived only from `R1 + R2 + A1 + P1`.

That is real reduction work, but it is not a retained charged-lepton
derivation and not a main-ready closure.

Affected surface:
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`

### [P1] The branch review packet itself says this is not yet a main-promotion branch

The top-level charged-lepton packet is scientifically honest, but that honesty
is exactly why this branch should not be landed onto `main` as-is.

It says:

- this is a branch packet for review and consolidation,
- it is not a claim that charged leptons are already retained closed,
- the current endpoint is exact candidate-route closure,
- one irreducible microscopic scalar selector law still remains open,
- and the correct classification is "not yet a retained charged-lepton
  promotion."

That matches the actual science surface. It also means the branch name currently
promises more than the branch itself delivers.

Affected surface:
- `docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md`

### [P2] Branch is not scoped cleanly for a charged-lepton main landing

Even aside from the open selector law, this branch is not packaged like a
narrow charged-lepton landing branch.

- it carries an unrelated DM/PF attack memo,
- it does not touch the publication/control-plane files that would be required
  for a `main` landing,
- so even if the Koide packet were scientifically ready, this branch would
  still need cleanup and proper package weaving first.

Affected surfaces:
- `docs/DM_PF_COMPRESSED_ROUTE_ATTACK_PLAN_NOTE_2026-04-18.md`
- publication/control-plane surfaces are untouched on this branch

## Minimum Path To Main

1. Derive the final microscopic scalar selector law so the Koide route stops
   being candidate-route only.
2. Keep the branch scoped to charged leptons by removing unrelated DM/PF work.
3. Only after the science clears, weave the accepted packet through the repo
   publication/control-plane surfaces in a separate landing pass.
