# SU(3) Gauge-Scalar Bridge Campaign: Salvage + Z_3 APBC Probe + Open Spec Question

**Date:** 2026-05-04
**Claim type:** bounded_theorem + meta
**Status:** consolidates 9 PRs of campaign work into a single salvage artifact, marks the wrong-geometry sub-campaign as retracted, and ships a Z_3 APBC probe that confirms the L_s=2 cube does not close under any natural APBC implementation.
**Primary runner:** `scripts/frontier_su3_cube_z3_apbc_attempt_2026_05_04.py`
**Prior PRs covered:** [#501](https://github.com/jonathonreilly/cl3-lattice-framework/pull/501), [#502](https://github.com/jonathonreilly/cl3-lattice-framework/pull/502), [#503](https://github.com/jonathonreilly/cl3-lattice-framework/pull/503), [#506](https://github.com/jonathonreilly/cl3-lattice-framework/pull/506), [#507](https://github.com/jonathonreilly/cl3-lattice-framework/pull/507), [#509](https://github.com/jonathonreilly/cl3-lattice-framework/pull/509), [#510](https://github.com/jonathonreilly/cl3-lattice-framework/pull/510), [#511](https://github.com/jonathonreilly/cl3-lattice-framework/pull/511), [#512](https://github.com/jonathonreilly/cl3-lattice-framework/pull/512)

## 0. Headline

This salvage artifact consolidates 9 PRs of campaign work, retracts wrong-geometry claims, salvages genuine science, and adds a concrete Z_3 APBC probe.

**Verdict on the bridge:**
- The L_s=2 cube under all tried implementations (PBC, Z_3 symmetric APBC, Z_3 1-direction APBC, Z_3 cocycle APBC) gives `P(6) ∈ [0.42, 0.43]`, far from bridge target `0.5935` (gap ≥ 543× ε_witness).
- The L_s=3 PBC cube exact tensor-network is **infeasible** (treewidth ≥ 29, intermediate `8^30 ~ 10^28`).
- The campaign cannot close the bridge from existing primitives + L_s=2 cube alone.

**Required next step (not done in this PR):** framework-author to specify what "L_s=2 APBC" actually means at the implementation level, OR provide the exact APBC convention (e.g., specific Z_3 cocycle structure, fractional twist, open-boundary projection). Without spec, the closure path is blocked at a documentation gap, not a math gap.

## 1. Campaign retrospective

### 1.1 Genuine science to keep

| Source | Finding | Status |
|---|---|---|
| [#501](https://github.com/jonathonreilly/cl3-lattice-framework/pull/501) Block 5 | L_s=2 PBC candidate ansatz `P = 0.4291` verified; standard Wilson `+−+−` convention has degenerate link multiplicities at L_s=2 | KEEP |
| [#502](https://github.com/jonathonreilly/cl3-lattice-framework/pull/502) | Counterfactual Pass methodology + no-new-axiom rule | KEEP (methodology) |
| [#503](https://github.com/jonathonreilly/cl3-lattice-framework/pull/503) | 4 closed-form Wilson approximations all far-misses at β=6 (gap ≥ 564× ε_witness) | KEEP |
| [#506](https://github.com/jonathonreilly/cl3-lattice-framework/pull/506) | Naive Haar MC has sign-problem variance at L=3 (integrand magnitude ~1e-100 vs MC noise ~1) | KEEP (negative result) |
| [#511](https://github.com/jonathonreilly/cl3-lattice-framework/pull/511) | Counterfactual pass identified framework target = L_s=2 APBC, not L_s=3 PBC | KEEP (critical) |
| [#512](https://github.com/jonathonreilly/cl3-lattice-framework/pull/512) | L_s=2 APBC under existing implementation gives same `P = 0.4291` as PBC | KEEP |
| **THIS PR** | Z_3 APBC variants (symmetric, 1-direction, cocycle) all give `P ≈ 0.42`, none close | NEW |

### 1.2 Engineering on wrong geometry — partial retraction

The following PRs attacked **L_s=3 PBC**, which PR #511 identified as NOT the framework's stated target (which is L_s=2 APBC):

| Source | Original claim | Retraction |
|---|---|---|
| [#507](https://github.com/jonathonreilly/cl3-lattice-framework/pull/507) | "TN contractor POC for L_s=3 PBC; treewidth ≤ 9 → 2 GB intermediate fits 4 GB" | RETRACT: treewidth estimate was wrong (PR #510 showed actual TW ≥ 29). Geometry was wrong (L_s=3 PBC, not L_s=2 APBC). The singlet-basis algorithm and cube geometry encoder are reusable infrastructure. |
| [#509](https://github.com/jonathonreilly/cl3-lattice-framework/pull/509) | "Greedy contraction empirically fails at step 82 with 65 TB intermediate on L_s=3 PBC" | KEEP AS NEGATIVE RESULT but note geometry was wrong. The custom 2-at-a-time greedy contractor with index-remap workaround is reusable infrastructure. |
| [#510](https://github.com/jonathonreilly/cl3-lattice-framework/pull/510) | "Treewidth ≥ 29 for L_s=3 PBC link adjacency graph; refutes #507's `8^9` estimate" | KEEP AS NEGATIVE RESULT but note geometry was wrong. The min-degree / min-fill elimination heuristics are reusable infrastructure. |

The L_s=3 PBC findings are still TRUE for L_s=3 PBC — they're just not directly relevant to the framework's stated L_s=2 APBC target. The negative engineering data and infrastructure remain useful; the targeting was off.

### 1.3 Why the wrong geometry persisted for 4 PRs

Recorded in feedback memory `feedback_run_counterfactual_before_compute.md`:
- User's task framing anchored on L=2 PBC giving 0.4291
- Framework roadmap docs say "L_s=2 APBC" but I skimmed past
- Existing runner blurred APBC vs PBC (titled APBC, encoded PBC)
- Engineering tunnel vision: each PR internally consistent, never re-grounded
- Counterfactual Pass methodology built mid-campaign without applying to in-flight lanes

## 2. Z_3 APBC probe (this PR's new content)

### 2.1 Approach

For SU(3), the natural anti-periodic boundary condition is a Z_3 center twist: each boundary-crossing link picks up a factor `ω = e^(2πi/3)` (or `ω̄`). Three variants tested:

- **PBC** (reference): no phase factors, `P = 0.4291049969`.
- **APBC-symmetric**: Z_3 twist on all 3 spatial directions. Per plaquette: 4 boundary-wrap links contribute `ω^(4k) = ω^k` (4 mod 3 = 1) where `k = (p−q) mod 3`. Over 12 plaquettes: `ω^(12k) = 1`. Cancels globally.
- **APBC-1dir**: Z_3 twist on 1 spatial direction only. Per plaquette: phase depends on whether plaquette is in the affected planes.
- **Cocycle**: non-trivial Z_3 cocycle, phase per plaquette = `ω^(k(k+1)/2)`. Tests non-uniform twist.

### 2.2 Results

| Variant | `P(6)` | Gap to `0.5935` |
|---|---:|---:|
| PBC (reference) | `0.4291049969` | `0.1644` = `543× ε_witness` |
| APBC-symmetric | `0.4291049969` | `0.1644` = `543× ε_witness` (cancels exactly) |
| APBC-1dir | `0.4191656069` | `0.1744` = `575× ε_witness` (moves AWAY from target) |
| Cocycle | `0.4291049969` | `0.1644` (cancels) |

**No Z_3 APBC variant closes the bridge or even moves toward the target.**

### 2.3 Why Z_3 APBC variants cancel globally

The L_s=2 cube has trivial Z_3 cohomology in the natural sense: every closed loop on the periodic L=2 lattice wraps an integer number of times around each spatial direction. Uniform Z_3 phase factors (per direction) multiply to an integer power of `ω`, which cancels for closed configurations.

Non-trivial APBC effects would require:

(a) **Non-uniform twist** (different phase per plaquette type). The 1-direction variant achieves this but moves AWAY from target.
(b) **Non-Z_3 boundary projection** (e.g., embedding SU(3) ↪ U(2), or some discrete gauge orbifold). Beyond Z_3 center.
(c) **Open boundary** (not all links wrap). Would not be a CUBE then — a different geometry.

Each of these options is a **framework-specification question**, not derivable from primitives.

## 3. The actual blocker

The campaign cannot derive `<P>(β=6) = 0.5934` from existing primitives + L_s=2 cube under any natural APBC implementation. The blocker is one of:

1. **APBC implementation specification gap**: framework docs say "L_s=2 APBC" but don't specify which APBC. Need framework-author to clarify.
2. **Geometry insufficiency**: L_s=2 is structurally too small (correlation length at β=6 in SU(3) is much larger than 2 lattice spacings); need L_s ≥ 3 with correct framework-specified BC.
3. **Hidden import**: the framework's prediction chain may implicitly use the MC value somewhere; without identification of this implicit import, derivation is impossible.

**Most likely blocker:** (1) and (2) combined. The framework's V-invariant minimal block is L_s=2 APBC by spec, but its quantitative value at β=6 may not be the bridge target — the framework may be using ONLY the *support envelope* `[0.4225, 0.5935]` as a derivation surface, with the actual `<P>` value being an admitted observable comparator.

If the latter, the gauge-scalar bridge no-go theorem ([`docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)) is the correct framing: **the bridge is fundamentally not derivable** from the current Wilson-framework primitive stack. Closure requires adding a new retained primitive (the exact L_s ≥ 3 cube data, OR an external import accepting the bounded-retained ceiling).

## 4. Path forward toward an actual solve

Three concrete options:

### 4.1 Option A: framework-author specification

**Effort:** depends on framework-author availability.
**Action:** ask user/framework-author to specify the exact APBC implementation. If a non-trivial APBC variant exists in the framework's intent, implement it and re-run. May give a different `P` value.

### 4.2 Option B: accept import → bounded retained → retire

**Effort:** 1 PR per import-retirement attempt; multiple PRs over weeks.
**Action:** explicitly accept the canonical MC value `<P>(β=6) = 0.5934` as a NAMED IMPORT with role "spectral measure for the L_s≥3 cube, used as bounded-support comparator only". This produces a **bounded retained** result. The next step in the lane becomes the import-retirement audit (per the no-new-axiom rule from PR #502).

This is the legitimate path forward per the methodology: import → bounded retained → retire.

### 4.3 Option C: expand framework scope to include `<P>` as observable definition

**Effort:** 1 governance PR + framework-wide audit.
**Action:** if the framework's actual primitive surface implicitly defines `<P>` via the MC computation (which produces 0.5934), make this explicit. The bridge then closes by definition rather than derivation. This requires a governance decision; not a science action.

## 5. Recommendation

**Option B** is the highest-value short-term move that respects the no-new-axiom rule:

1. Open an "import acceptance" PR that names `<P>(β=6) = 0.5934 ± δ` as a bounded-retained import for the gauge-scalar bridge lane.
2. Per the no-new-axiom rule, this caps the lane's headline status at **bounded retained** (not retained).
3. Queue the import-retirement audit as the next work in this lane.
4. The retirement audit would attempt to derive the value from L_s ≥ 3 cube data; if that fails, the lane stays at bounded retained.

**Option A** is necessary if the framework actually has a non-trivial APBC spec we haven't tried. User input required.

**Option C** is a governance pivot, not a science move. Out of scope for this campaign.

## 6. Theorem statement

**Bounded theorem (L_s=2 cube under Z_3 APBC variants).** The runner
`scripts/frontier_su3_cube_z3_apbc_attempt_2026_05_04.py` evaluates the
L_s=2 cube source-sector Perron value under four boundary-condition
variants:

- PBC (no phase): `P(6) = 0.4291049969`
- APBC-symmetric (Z_3 on all 3 directions): `P(6) = 0.4291049969`
- APBC-1dir (Z_3 on 1 direction): `P(6) = 0.4191656069`
- Cocycle (quadratic Z_3 phase): `P(6) = 0.4291049969`

All variants give `P` in `[0.42, 0.43]`, far from the bridge support
upper candidate `0.5935306800` (gap ≥ 543× ε_witness). No tested Z_3
APBC variant closes the gauge-scalar bridge.

The L_s=2 closed cube has trivial Z_3 cohomology for uniform twists
(global phase cancellation). Non-trivial APBC effects would require
either non-uniform twist, non-Z_3 boundary projection, or open-boundary
geometry — each of which is a framework-specification question, not
derivable from primitives.

## 7. Scope

### 7.1 In scope

- Consolidation / salvage narrative for 9-PR campaign.
- Retraction (in narrative, not destructive) of wrong-geometry sub-campaign.
- Z_3 APBC probe with 4 variants (PBC, symmetric, 1-direction, cocycle).
- Identification of the actual blocker: framework-spec or import-retirement.

### 7.2 Out of scope

- Closing the gauge-scalar bridge.
- Implementing arbitrary framework-specified APBC variants without spec.
- L_s ≥ 3 actual cube computation.
- Import acceptance (Option B above) — would need its own PR.

### 7.3 Not making the following claims

- Does NOT promote bridge parent chain.
- Does NOT compute or constrain `<P>(β=6)`.
- Does NOT close any PR destructively (the L_s=3 PBC PRs remain open as
  honest negative engineering findings on the wrong geometry).

## 8. Audit consequence

```yaml
claim_id: su3_bridge_campaign_salvage_2026-05-04
note_path: docs/SU3_BRIDGE_CAMPAIGN_SALVAGE_2026-05-04.md
runner_path: scripts/frontier_su3_cube_z3_apbc_attempt_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03  # PR #501
  - su3_wilson_closed_form_fanout_theorem_note_2026-05-04          # PR #503
  - su3_bridge_counterfactual_pass_2026-05-04                       # PR #511
  - su3_cube_full_rho_perron_2026-05-04                              # PR #512
  - gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03
verdict_rationale_template: |
  Salvage / consolidation artifact closing 9 PRs of bridge campaign work
  into a coherent narrative + Z_3 APBC probe + path-forward statement.

  Z_3 APBC variants (symmetric, 1-direction, cocycle) at L_s=2 cube
  all give P ≈ 0.42, no closure. Global Z_3 phase cancellation on the
  closed cube prevents uniform twists from changing the result.

  Verdict: L_s=2 cube under any natural APBC variant cannot close the
  bridge. Path forward: (A) framework-author APBC spec clarification,
  or (B) import → bounded retained → retire (recommended).

  The L_s=3 PBC sub-campaign (PRs #506, #507, #509, #510) is on the
  WRONG geometry per PR #511's counterfactual finding, but the
  engineering data are honest and the infrastructure (singlet basis
  builder, custom greedy contractor, treewidth heuristics) is reusable
  for future framework-spec-correct work.

  Does not promote bridge parent chain. Does not compute <P>(beta=6).
  No forbidden imports. Saved as feedback memory:
  feedback_run_counterfactual_before_compute.md.
```

## 9. Cross-references

All campaign PRs:
- [#501](https://github.com/jonathonreilly/cl3-lattice-framework/pull/501) Wigner Blocks 4+5 (L_s=2 PBC verdict)
- [#502](https://github.com/jonathonreilly/cl3-lattice-framework/pull/502) Methodology: Counterfactual Pass + no-axiom rule
- [#503](https://github.com/jonathonreilly/cl3-lattice-framework/pull/503) Closed-form fan-out (4 rule-outs)
- [#506](https://github.com/jonathonreilly/cl3-lattice-framework/pull/506) Haar MC sign-problem (wrong geometry)
- [#507](https://github.com/jonathonreilly/cl3-lattice-framework/pull/507) TN POC (wrong geometry)
- [#509](https://github.com/jonathonreilly/cl3-lattice-framework/pull/509) Greedy contractor failure (wrong geometry)
- [#510](https://github.com/jonathonreilly/cl3-lattice-framework/pull/510) Treewidth ≥ 29 (wrong geometry)
- [#511](https://github.com/jonathonreilly/cl3-lattice-framework/pull/511) Counterfactual pass: framework target is L_s=2 APBC
- [#512](https://github.com/jonathonreilly/cl3-lattice-framework/pull/512) Full-ρ Perron at L_s=2: APBC ≡ PBC under existing impl

Bridge no-go theorem (background):
- `docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`

Methodology (PR #502):
- `docs/ai_methodology/skills/physics-loop/references/assumption-import-audit.md`

## 10. Command

```bash
python3 scripts/frontier_su3_cube_z3_apbc_attempt_2026_05_04.py
```

Expected runtime: ~15 seconds. Expected summary:

```text
SUMMARY: THEOREM PASS=1 SUPPORT=1 FAIL=0
```
