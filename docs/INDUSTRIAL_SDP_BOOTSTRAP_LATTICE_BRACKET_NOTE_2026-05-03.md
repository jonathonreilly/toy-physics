# Industrial SDP Bootstrap — Lattice ⟨P⟩(β=6) Bracket Attempt

**Date:** 2026-05-03
**Type:** numerical CVXPY bracket attempt + named-obstruction stretch
**Claim scope:** apply the CVXPY-based SDP infrastructure validated in
block 01 (PR [#433](https://github.com/jonathonreilly/cl3-lattice-framework/pull/433))
to the actual lattice `⟨P⟩(β=6)` problem via multi-Wilson-loop moment
bootstrap. **Honest result: bracket is loose**, `[0.4225, 1.0]` — the
upper bound stays at the trivial support endpoint because no explicit
Migdal-Makeenko loop equations are implemented. This consolidates the
named obstruction from prior PRs [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420),
[#423](https://github.com/jonathonreilly/cl3-lattice-framework/pull/423):
**loop equations are the critical missing piece**, and CVXPY-based bracketing
without them does not improve over the bridge-support stack analytic
upper-bound candidate (0.59353).
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_industrial_sdp_bootstrap_block02.py`
**Run with:** `.venv/bin/python3 scripts/frontier_industrial_sdp_bootstrap_block02.py`

## 0. Question

Block 01 (PR [#433](https://github.com/jonathonreilly/cl3-lattice-framework/pull/433))
established the CVXPY infrastructure works on this framework. Can it
bracket the actual lattice `⟨P⟩(β=6) ≈ 0.5934` via multi-Wilson-loop
SDP at small L_max, even without explicit Migdal-Makeenko loop equations?

## 1. Setup

The bootstrap problem (CVXPY 1.8.2 + CLARABEL):

**Variables (real-valued):**
- `p1, p2, p3, p4` = `⟨P^k⟩` for k=1..4 (plaquette moments)
- `r1, r2` = `⟨R⟩, ⟨R²⟩` (1×2 rectangle Wilson loop)
- `q1, q2` = `⟨Q⟩, ⟨Q²⟩` (2×2 plaquette / quadrupole)
- `pr, pq, rq` = cross-correlators

**Constraints:**
- 3x3 Hankel PSD on plaquette moments
- Hausdorff-shifted PSD for `[a, b] = [-1/3, 1]` support
- 4x4 Gram matrix on `{1, P, R, Q}` PSD (RP-derived per Lemma BB1 of PR [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420))
- Support bounds: `p1, r1, q1 ∈ [-1/3, 1]`; `p2, r2, q2, p4 ∈ [0, 1]`
- Hausdorff monotonicity: `p4 ≤ p2`
- Area-law / perimeter inequalities: `r1 ≤ p2`, `q1 ≤ p4`
- Optional bridge-support lower bound: `p1 ≥ 0.4225` (admitted: mean-field
  correlation-raising — single-plaquette is a lower bound for confined
  lattice gauge)

## 2. Result

```text
Constraint set                                          min p1     max p1   width
─────────────────────────────────────────────────────  ────────  ────────  ──────
Pure PSD (no framework constraints)                    -0.3333    1.0000   1.3333
PSD + area-law                                         -0.3333    1.0000   1.3333
PSD + bridge-support lower bound (p1 ≥ 0.4225)          0.4225    1.0000   0.5775
PSD + bridge-support + area-law (full)                  0.4225    1.0000   0.5775
```

**Best bracket: `⟨P⟩(β=6) ∈ [0.4225, 1.0]`** — width 0.578.

Contains MC value 0.5934 ✓; contains bridge-support upper bound 0.59353 ✓.

## 3. Why the upper bound is trivial

The PSD + Hausdorff constraints alone are satisfiable by ANY valid
probability distribution on `[a, b]`. In particular, the **delta-distribution
at P = 1** (which gives `p1 = p2 = p3 = p4 = 1`) is a valid moment
sequence — its Hankel matrix is the all-ones matrix (rank 1, PSD).

So PSD + Hausdorff alone cannot bound `p1` strictly below 1. To get a
non-trivial upper bound, we need either:
- **Explicit lattice Migdal-Makeenko / Schwinger-Dyson loop equations**
  relating moments to coupling β
- OR **explicit area-law constraints** with strict inequalities tied to β
- OR **multi-Wilson-loop relations** at higher L_max with industrial SDP
  (e.g., Kazakov-Zheng 2022 at L_max=16 with Mosek)

The lower bound `0.4225` comes only from the admitted "mean-field
correlation-raising" assumption (lattice MC ≥ single-plaquette mean-field
in confined regime), not from the bootstrap.

## 4. Comparison with bridge-support stack and literature

| Approach | Bracket on `⟨P⟩(β=6)` | Width | Method |
|---|---|---|---|
| **This block 02 (CVXPY moment bootstrap)** | `[0.4225, 1.0]` | 0.578 | RP + Hankel + Hausdorff + 4x4 Gram + admitted area-law |
| Block 01 prior campaign analytical (PR [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420)) | `~0.35-0.48` (lower-bound estimate) | n/a | mixed-cumulant + strong-coupling LO |
| Bridge-support analytic upper-bound | `≤ 0.59353` (one-sided) | n/a | Perron-state reduction + 3D environment guess |
| Canonical lattice MC | `0.5934` (point) | 0 | full lattice MC |
| Kazakov-Zheng 2022 SU(∞) bracket near λ≈1.35 | `[0.59, 0.61]` | 0.02 | RP + Migdal-Makeenko + L_max=16 + SDP (Mosek) |
| Kazakov-Zheng 2024 SU(2) finite-N | 0.1% precision in physical range | 0.001 | same with finite-N adaptation |

**Honest assessment:** the CVXPY moment bootstrap from this block does
NOT provide a tighter bracket than the bridge-support stack's analytic
upper-bound candidate (0.59353). The bridge-support stack already
contains effectively the tightest analytic bound currently available
on this framework's surface; CVXPY without Migdal-Makeenko adds no
upper-bound information.

## 5. Sharper named obstruction (consolidated, after CVXPY infrastructure validation)

```text
[BOOTSTRAP-LOOP-EQUATION OBSTRUCTION (CONSOLIDATED, with industrial SDP)]:
  Even with industrial CVXPY SDP infrastructure now available (block 01,
  PR #433), the lattice ⟨P⟩(β=6) bracket from PSD + Hausdorff + framework-
  specific positivity is essentially [mean-field LB, 1.0]. The upper bound
  remains trivial without explicit Migdal-Makeenko loop equations, which
  was already identified as the critical missing piece in PRs #420 + #423.

  Tightening to industrial precision (~10⁻²) requires:
    (a) explicit Migdal-Makeenko / Schwinger-Dyson loop equations on
        framework's V-invariant minimal block (still not done — multi-month
        research project);
    (b) industrial SDP solver MOSEK at L_max ≥ 8-16 (CLARABEL/SCS
        precision insufficient; cvxpy infrastructure ready);
    (c) framework-specific positivity refinements from Cl(3) HS + V-invariance
        (block 02 of prior campaign showed this alone insufficient).

  Block 01 + 02 of THIS campaign (industrial-sdp-bootstrap-20260503)
  validate that the CVXPY infrastructure works and that, without loop
  equations, even industrial SDP cannot tighten the bracket below the
  bridge-support stack's analytic upper-bound candidate.
```

## 6. Honest status

```yaml
actual_current_surface_status: numerical bracket attempt + consolidated named-obstruction stretch
target_claim_type: open_gate
conditional_surface_status: bounded by missing Migdal-Makeenko derivation
hypothetical_axiom_status: null
admitted_observation_status: bridge-support mean-field lower bound (0.4225) admitted
claim_type_reason: |
  CVXPY infrastructure validated in block 01 (PR #433); applied here to
  the lattice problem with multi-Wilson-loop moment bootstrap. Honest
  result is a wide bracket [0.4225, 1.0] with trivial upper bound. The
  consolidated named obstruction (Migdal-Makeenko loop equations missing)
  is sharper because we now know that even industrial SDP doesn't help
  without them.
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Numerical bracket attempt with honest negative result (loose bracket).
  The CONSOLIDATED named obstruction (loop equations are critical)
  IS the value, but no closure is claimed.
```

## 7. What this note closes

- First numerical CVXPY-based lattice bracket attempt on `⟨P⟩(β=6)` for
  this framework
- Confirms that PSD + Hausdorff + framework-specific positivity alone do
  not improve over the bridge-support stack analytic upper-bound
- Sharpens the consolidated named obstruction (Migdal-Makeenko loop
  equations critical, even with industrial SDP infrastructure)
- Validates that the CVXPY infrastructure (block 01, PR [#433](https://github.com/jonathonreilly/cl3-lattice-framework/pull/433))
  works on the lattice problem (problem solves to optimal status)

## 8. What this note does NOT close

- The lattice `⟨P⟩(β=6)` value (famous open lattice problem)
- A non-trivial upper bound on `⟨P⟩(β=6)` from the bootstrap
- Migdal-Makeenko derivation on framework surface
- Industrial Kazakov-Zheng-precision (~10⁻²) brackets

## 9. Cross-references

- Block 01 of this campaign (CVXPY infrastructure): PR [#433](https://github.com/jonathonreilly/cl3-lattice-framework/pull/433)
- Infra unblocker: PR [#430](https://github.com/jonathonreilly/cl3-lattice-framework/pull/430) (cvxpy + venv)
- Verdict-named obstruction: [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- Prior bootstrap analytical (small-truncation): PR [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420), PR [#423](https://github.com/jonathonreilly/cl3-lattice-framework/pull/423)
- Bridge-support analytic upper-bound: `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`
- Sister obstruction: [`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
- Literature: Kazakov-Zheng [arXiv:2203.11360](https://arxiv.org/abs/2203.11360), [arXiv:2404.16925](https://arxiv.org/abs/2404.16925)
