# Opportunity Queue — Bridge Gap New Physics

**Date:** 2026-05-06

Ranked by retained-positive probability × runtime efficiency × structural
coherence with the parent new-physics opening.

| Rank | Block | Route | Retained-positive prob | Runtime | Independent of just-blocked? |
|---|---|---|---|---|---|
| 1 | 01 | R1.A bi-invariant metric → t | HIGH | 60-90m | N/A (first block) |
| 2 | 02 | R2.A single-plaquette closed form ⟨P⟩_HK,1plaq | HIGH (after 01) | 30-45m | Depends on 01 |
| 3 | 03 | R3.A Casimir-diagonal multi-plaquette closure | MEDIUM | 90-120m | Depends on 01, 02 |
| 4 | 04 | R4.A action-form uniqueness via O(a²) coefficients | MEDIUM | 60-90m | Depends on 01-03 |
| 5 | 04 | R4.B Cl(3) ⊗ Cl(3) → SU(4) ⊃ SU(3) × U(1) tensor exploration | LOW (high-EV speculative) | 90-120m | Independent — can run if 01-04 blocked |
| 6 | -- | Cube-shell strong-coupling enumeration to β⁶ (parallel cheap track) | LOW (incremental) | 60-90m | Independent — can run alongside HK chain |

## Promotion-value gate self-record (per skill workflow step 7)

The campaign goal is **"derive the framework's actual gauge action and
compute ⟨P⟩(6) under it,"** which is a retained-positive movement target
for the four cluster lanes. Therefore V1-V5 must be answered before each PR.

### V1-V5 self-record for Block 01 (R1.A) — pre-PR

| # | Question | Answer |
|---|---|---|
| V1 | What SPECIFIC verdict-identified obstruction does this PR close? | The cluster-obstruction parent's Resolution-A target ([`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](../../../../docs/LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md) §4): "novel non-perturbative matching theorem derivable from the framework's algebraic structure." Specifically: derives the framework's Brownian-time matching `t(β)`, which in Wilson is replaced by the imported convention. |
| V2 | What NEW derivation does this PR contain? | A derivation chain from canonical Cl(3) trace-form `Tr(T_a T_b) = δ_{ab}/2` (retained) → unique bi-invariant metric on SU(3) → Brownian-motion generator → small-U Wilson-HK matching → exact-rational `t(β) = N_c/β`, evaluated at framework's β = 6 to give `t(6) = 1/2`. This derivation chain is not currently retained as a single artifact in the project audit graph. |
| V3 | Could the audit lane already complete this from existing primitives + standard math? | Combining retained Tr-form + standard Menotti-Onofri 1981 small-U matching is a one-step combination. But the resulting closed-form `t(β=6) = 1/2` and its consequences for ⟨P⟩(6) have NOT been done in the project. The opening for doing it is documented in [`BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md). The audit lane could in principle do it; this loop does it. |
| V4 | Is the marginal content non-trivial? | Yes — gives a specific framework-derived value `t = 1/2` and downstream ⟨P⟩_HK,1plaq(6) = exp(-1/3) = 0.7165, which differs from Wilson's 0.4225 by ~70%. This decisively demonstrates the framework's actual derived ⟨P⟩(6) is *different* from the imported Wilson value. Either of the two values must be wrong, which is structurally consequential for all four cluster lanes' downstream values. |
| V5 | One-step variant of an already-landed cycle? | No. Closest prior cycle is `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02` which fixes Wilson β=6 from Tr-form. Block 01 does the analogous derivation for HK-side time t. The structural content (HK side instead of Wilson side) is genuinely distinct — not a relabeling. The new-physics opening note (2026-05-06) named this as the next step that hadn't been done. |

**V1-V5 verdict for Block 01: PASS.**

## Mid-loop refresh

Update this queue after each block completion / pivot. Maintain at least
3 ranked candidates if runtime > 2h remaining.
