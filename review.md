# Review Note: `claude/angry-chatelet-2dc78c`

## Status (2026-04-17, tip `2f464afd`)

**Do not merge as-is.**

This branch fixes the earlier silent overpromotion: the authority note now
separates retained structural identities (SI1-SI3) from the new P-AT proposal,
and the rewritten runner is explicit about that split. The current blocker is
different and narrower:

- the branch now tries to land a **framework-level proposal with review
  pending** directly into the live package, reviewer guide, README, and arXiv
  surfaces;
- the new runner still validates only the consequences of a hand-written 3x3
  texture, not its claimed realization as a framework primitive on the
  retained `hw=1` / `K_R` surface;
- one of the downstream support notes is now stronger than its own primary
  runner.

So the problem is no longer "hidden assumption promoted as retained theorem."
The problem is "proposal not yet theorem-grade, but already wired through the
live publication/manuscript surfaces as if it belongs there."

## Current blockers

### 1. Publication surfaces now carry a review-pending proposal as live package content

The branch is explicit that P-AT is a **new framework proposal with review
pending**, which is honest. But it still lands that proposal directly in the
live publication inventory and manuscript-facing surfaces:

- `docs/publication/ci3_z3/PUBLICATION_MATRIX.md`
- `docs/publication/ci3_z3/ARXIV_DRAFT.md`
- `docs/publication/ci3_z3/README.md`
- `docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md`
- root `README.md`

That is not clean publication control. A review-pending primitive can live in a
branch-local proposal note or a work-history/review packet, but it should not
be woven into the live package/manuscript/reviewer front door until it either:

1. is accepted as retained and properly certified, or
2. is demoted to branch-local proposal history rather than live package state.

Right now the branch mixes:

- **Layer 1:** truly retained SI1-SI3 content, which is fine to land;
- **Layer 2:** a proposal still under framework-level review, which is not yet
  clean to land in the live arXiv/package/front-door surfaces.

### 2. The new runner does not certify P-AT as a framework primitive on the retained surface

The authority note says P-AT is **on the retained `hw=1` down-type mass
matrix**, and motivates it by the atlas bilinear tensor carrier `K_R` on
`Q_L`. But the primary runner does not audit either of those load-bearing
claims.

What the runner actually does:

- directly constructs a hand-written symmetric `3x3` ansatz
  `M_d(1,2)=sqrt(m_d m_s)`, `M_d(2,3)=m_s^(5/6) m_b^(1/6)`, `M_d(1,3)=0`;
- diagonalizes that ansatz numerically;
- shows the expected hierarchical ratios approach `1`;
- then defines the identification surface `(I1)-(I2)` algebraically and checks
  it against itself.

What it does **not** do:

- verify that the ansatz is realized by or embedded in the retained `Z_2`,
  `hw=1` normal form;
- verify that the `(2,3)` texture follows from the claimed atlas carrier
  `K_R`;
- derive the identification surface from an independently certified framework
  construction rather than from a chosen ansatz plus algebra.

That is enough for "proposal with promising numerics," but not enough for
"framework primitive ready to be wired into the live package."

### 3. The five-sixths support note now outruns its own primary runner

`docs/CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md` now says:

- the retained structural origin of `5/6` is the atlas `1+5` projector split,
  not the Casimir;
- under P-AT the bridge is leading-order exact;
- the bridge identity is exact on the bridge-identity theorem surface.

But its declared primary runner `scripts/frontier_ckm_five_sixths_bridge_support.py`
still does only the old bounded support job:

- exact `C_F - T_F = 5/6`;
- `|V_cb| = alpha_s(v)/sqrt(6)`;
- bounded self-scale numerical comparison.

It does **not** audit:

- the atlas-projector origin of `5/6`;
- the P-AT primitive;
- the leading-order hierarchical exactness claim.

So this note/runner pair is internally misaligned on the current tip.

## Validation status

I replayed the rewritten primary runner successfully:

- `scripts/frontier_ckm_dual_bridge_identity.py`:
  `RETAINED PASS=16`, `P-AT PASS=9`, `BOUNDED PASS=3`, `FAIL=0`

Sibling runners also replay cleanly:

- `frontier_mass_ratio_ckm_dual.py`: `PASS=23`, `FAIL=0`
- `frontier_ckm_five_sixths_bridge_support.py`: `EXACT PASS=5`, `BOUNDED PASS=7`, `FAIL=0`
- `frontier_ckm_atlas_axiom_closure.py`: `PASS=40`, `FAIL=0`

So this is **not** a runtime rejection. It is a publication/evidence-surface
rejection.

## Clean salvage path

Either of these would make the branch mergeable:

1. **Conservative landing path**
   - land only Layer 1 (retained SI1-SI3) updates on `main`;
   - keep P-AT in branch-local proposal/work-history/review material, not in
     the live package/manuscript/front-door surfaces;
   - realign `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md` with its actual runner.

2. **Full proposal-to-package path**
   - add real certification that P-AT sits on the retained `hw=1` / `K_R`
     surface;
   - make the primary runner audit that framework realization rather than just
     diagonalizing a chosen ansatz;
   - then land the package/manuscript wiring after that evidence exists.

Until then, the branch is an honest and interesting proposal, but it is still
not a clean `main` landing.
