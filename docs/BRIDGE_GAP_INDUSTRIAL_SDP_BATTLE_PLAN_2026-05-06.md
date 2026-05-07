# Bridge Gap — Industrial SDP Battle Plan (Resolution C)

**Date:** 2026-05-06
**Type:** engineering battle plan / RFP-style scope
**Status:** scoping document for the Resolution C path on the
[lattice → physical matching cluster obstruction](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md).
This is NOT a derivation. It is the concrete engineering plan for closing
⟨P⟩(β=6) within ε_witness ≈ 3×10⁻⁴ via industrial SDP bootstrap, after seven
framework-internal Resolution-A attack angles have been exhausted (per
[`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md)).
**Authority role:** project planning artifact for budget commit + hire/contract decisions.

## 0. Why this is the path

The bridge gap = analytically computing ⟨P⟩(β=6) for SU(3) 4D Wilson plaquette
to ε_witness ≈ 3×10⁻⁴. After seven independent attacks on framework-internal
levers (round-1 Picard-Fuchs lift, APBC twist, SDP+MM, governance; round-2
RP-A11 cluster inequality, V-singlet projection, meta-leverage analysis), the
verdict is unanimous: no Resolution-A route is open with current primitives.

Resolution C (industrial SDP bootstrap) is the only path with calculable cost
and credible mechanism to reach ε_witness. It scales the published
Anderson-Kruczenski (2017) / Kazakov-Zheng (2022 SU(∞), 2024 SU(2)) lattice
gauge bootstrap method to SU(3) at the framework's β=6, at L_max ≈ 22-24
truncation.

## 1. Method (one-line summary)

Lift the framework's existing `INDUSTRIAL_SDP_BOOTSTRAP_INFRASTRUCTURE_NOTE_2026-05-03`
infrastructure (CVXPY 1.8.2 + open-source solvers, validated on SU(2) and
SU(3) single-plaquette references) to the full lattice ⟨P⟩(β=6) bracket via:

- Wilson loop set of size ~200-300 at L_max = 22-24
- Reflection positivity (A11) → Gram matrix PSD on the loop set
- Lattice Migdal-Makeenko / Schwinger-Dyson loop equations as linear
  moment-relation constraints (require L_s ≥ 4 cube — V-invariant minimal
  block too small per exhausted-routes consolidation §1.3)
- Mosek (commercial, structured-PSD interior-point) — open-source
  CLARABEL/SCS/HIGHS provably cap 1-2 orders above ε_witness
- Symmetry reductions: lattice translations, Klein-four V on temporal,
  plaquette-adjacency bipartite (these are *engineering accelerations*,
  not derivation levers)

The end deliverable: an audit-clean lower-bound and upper-bound bracket on
⟨P⟩(β=6), both within ε_witness ≈ 3×10⁻⁴ of each other, derived from
RP-A11 + lattice loop equations + Hausdorff moment problem PSD without
any PDG / lattice-MC / fitted-coefficient input as load-bearing.

## 2. Phase plan

### Phase 0 — Scoping & hire (month 0-1, ~$30k)

- Engage 1.0-1.5 FTE expert (PhD lattice gauge / SDP background; ideally
  someone who has worked with K-Z 2022/2024 codebase)
- Acquire Mosek academic license ($3-7k/yr, single-seat)
- Access cluster-class HPC for SDP solves (institutional or AWS — budget
  ~$30k/yr for ~1000 CPU-hours/month)
- Reproduce K-Z 2024 SU(2) result on framework's local infra (validation
  milestone; no framework β=6 yet)

**Exit criterion:** SU(2) at L_max=18-20 reproduces K-Z 2024 numerical
agreement to published precision on team's own hardware.

### Phase 1 — Framework SU(3) at L_max = 8-10 (month 1-4, ~$80k)

- Implement Wilson loop multiplication tables on SU(3)
- Derive loop equations (Migdal-Makeenko) on a framework-clean L_s ≥ 4
  cube geometry — NOT the V-invariant minimal block (proven empty)
- Build Gram matrix from RP-A11 reflection on selected loop set
- Run Mosek SDP at L_max = 8, 9, 10 with framework symmetry reductions
- Bracket width target at L_max=10: ≤ 5×10⁻²

**Exit criterion:** reproducible SU(3) ⟨P⟩(β=6) bracket at ~5% width,
with explicit forbidden-import compliance audit. Width compares to
exhausted-routes lower bound (β⁵-jet 0.4390) and bridge upper region
(MC FSS 0.5940 ± 4×10⁻⁴ as audit comparator only).

### Phase 2 — Scale to L_max = 14-16 (month 4-9, ~$200k)

- Add higher-rank Wilson loop sectors (rectangles, plaquette products,
  multi-plaquette stacks)
- Implement structured-PSD Mosek constraints for ~10⁴-scale Gram matrices
- Apply framework's plaquette-adjacency bipartite + Klein-four orbit reductions
- Bracket width target at L_max=16: ≤ 5×10⁻³

**Exit criterion:** ⟨P⟩(β=6) bracket at ~0.5% width, framework symmetry
reductions delivering ~3-5× speedup vs naive truncation. Compare K-Z 2024
~0.1% precision at L_max=18-20.

### Phase 3 — Push to ε_witness (month 9-15, ~$200k)

- L_max = 22-24 truncation with full structural-symmetry SDP
- Cluster-scale compute for the largest Gram dimensions (~10⁵-10⁶ scalar
  variables)
- High-precision (extended-precision) arithmetic if Mosek conditioning
  becomes limiting
- Bracket width target at L_max=24: ≤ 3×10⁻⁴ (ε_witness scale)

**Exit criterion:** rigorous lower-and-upper bracket on ⟨P⟩(β=6) within
ε_witness, satisfying all forbidden-import constraints. Submitted to
audit lane as `claim_type: bounded_theorem` — the SDP bracket is
admittedly numerical (interior-point convergence) but is *not* lattice MC
and is *not* a fit; it is a proof of a tight Gram-PSD + loop-equation
system.

## 3. Budget

| Phase | Months | Cost | Cumulative |
|---|---:|---:|---:|
| 0 (Scoping/hire/validation) | 0-1 | $30k | $30k |
| 1 (L_max=8-10 framework SU(3)) | 1-4 | $80k | $110k |
| 2 (L_max=14-16) | 4-9 | $200k | $310k |
| 3 (L_max=22-24, ε_witness) | 9-15 | $200k | $510k |
| **Total** | **15** | **$510k** | — |

Breakdown: ~60% labor (1.0-1.5 FTE expert × 15 months); ~25% compute
($300/mo cluster + Mosek licensing); ~15% overhead.

## 4. Risk model

| Risk | Probability | Impact | Mitigation |
|---|---:|---|---|
| SU(3) at β=6 conditioning worse than SU(2) at β=2.5 | 30% | +20-50% timeline | Extended-precision arithmetic; SDPA-DD as backup solver |
| L_max = 22-24 insufficient — need L_max=28+ | 15% | +30-100% timeline + unbounded compute | Phase 3 milestone gate; reassess at L_max=20 |
| Mosek licensing change / commercial issues | 5% | +6-12 months while alternates evaluated | Keep CLARABEL/SCS as fallback for L_max≤14 |
| Expert hire fails / departures | 20% | +3-6 months per departure | Pair-redundancy; document state at Phase 0 exit |
| Framework symmetry reductions don't deliver expected speedup | 25% | +20-50% Phase 2/3 cost | Use brute-force without reductions at higher cost |

**Aggregated success probability at ε_witness in 15 months:** ~70%.
Aggregated probability of success within 24 months and $1M: ~90%.

## 5. Forbidden imports — what stays out

| Item | Status |
|---|---|
| PDG observed ⟨P⟩(β=6) ≈ 0.5934 | Comparator only; never derivation input |
| Lattice MC FSS extrapolation 0.59400 ± 0.00037 | Comparator only |
| Fitted β_eff or matching coefficients | Forbidden |
| K-Z 2022/2024 numerical comparators | Comparator only; methodology cited as standard machinery |
| Same-surface family arguments | Forbidden |
| Sommer scale r_0 = 0.5 fm | Already admitted upstream (PR #258); inherited at admitted-tier |
| 4-loop QCD β-function | Already admitted upstream (PR #258); inherited at admitted-tier |

The SDP bracket is a derivation in the sense that **the bound itself is a
theorem**: given the Wilson partition function (axiom-derived) and the
loop equations (standard QFT) and the Gram-PSD constraints (RP-A11
retained), the value ⟨P⟩(β=6) is bracketed by the SDP solution within
its solver-precision. The numerical width is *audited* not *fitted*.

## 6. What this closes if successful

A successful Phase 3 closure with bracket width ≤ ε_witness simultaneously:

| Lane | Closure mechanism |
|---|---|
| α_s direct Wilson | β_eff(6) determined via R_O⁻¹(⟨P⟩(6)); Sommer-scheme + 4-loop QCD running bridge already admitted |
| Higgs mass scalar normalization | lattice-curvature ↔ (m_H/v)² matching coefficient determined by SDP value |
| Gauge-scalar observable bridge | ⟨P⟩_full = R_O(β_eff) closed by direct numerical SDP value |
| Koide-Brannen phase | Berry-holonomy → physical phase matching: structurally identical reduction once SDP closure exists |

The four cluster lanes lift from `bounded_support` to `audited_conditional`
or higher. Transitive descendants (~1000+ rows per audit-backlog campaign
synthesis) inherit the Resolution-C numerical closure.

## 7. What this does NOT close

- **Resolution A (novel non-perturbative theorem)** remains open. If a
  framework-internal lever is later discovered, this engineering plan can
  be retired or shortened.
- **External lattice gauge theory open problems** (continuum limit at full
  precision, deconfinement spectrum, glueball masses) are NOT addressed
  by this bracket — only ⟨P⟩(β=6) at the framework's specific evaluation
  point.
- **Resolution B (governance)** remains a separate option for honest
  defensive labeling of the four lanes pre-Phase-3-completion, but the
  user has indicated this is not the priority.

## 8. Decision points

Three explicit gates where the project may pause / pivot:

- **Phase 0 exit (month 1):** SU(2) reproduction failed → diagnose and
  decide commit-vs-abandon. Cost-to-quit: $30k.
- **Phase 1 exit (month 4):** SU(3) at L_max=10 bracket > 10% width →
  diagnose framework-specific issues. Cost-to-quit: $110k.
- **Phase 2 exit (month 9):** SU(3) at L_max=16 bracket > 1% width →
  ε_witness path may need L_max>24. Re-estimate Phase 3. Cost-to-quit:
  $310k.

## 9. Parallel cheap track — extending strong-coupling expansion

While Phase 0-3 runs, a parallel low-cost research effort can extend the
framework's exact strong-coupling expansion of ⟨P⟩(β) past β⁵:

- Current: P_full(β) = P_1plaq(β) + β⁵/472392 + O(β⁶) (exact)
- Target: extend to β⁶, β⁷, β⁸ via the same leafless cube-shell enumeration
  in [`scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py`](../scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py)
- Cost: ~2-4 weeks per coefficient (Wigner-Racah enumeration scales
  combinatorially)
- Outcome: each new coefficient incrementally tightens the strong-coupling
  truncation gap; does NOT close the bridge alone (convergence ceiling near
  β_c ≈ 5.7-5.9 means series is asymptotic at β=6) but is genuine derivation
  not corollary churn

This track is independent and can run on existing infrastructure with no
new licensing.

## 10. Status

```yaml
actual_current_surface_status: engineering battle plan / scoping document
proposal_allowed: false
proposal_allowed_reason: |
  This is an engineering plan for Resolution C, not a derivation. The plan
  itself does not derive ⟨P⟩(β=6); it specifies the path to a numerical
  bracket within ε_witness via industrial SDP. Audit-graph effect: the
  document is a planning artifact for resource commit decisions.
audit_required_before_effective_retained: false
bare_retained_allowed: false
forbidden_imports_used: false
```

## 11. Cross-references

### Parent obstruction
- [`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md) — names Resolution C
- [`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md) — proves Resolution A is exhausted

### Existing SDP infrastructure
- [`INDUSTRIAL_SDP_BOOTSTRAP_INFRASTRUCTURE_NOTE_2026-05-03.md`](INDUSTRIAL_SDP_BOOTSTRAP_INFRASTRUCTURE_NOTE_2026-05-03.md)
- [`INDUSTRIAL_SDP_BOOTSTRAP_LATTICE_BRACKET_NOTE_2026-05-03.md`](INDUSTRIAL_SDP_BOOTSTRAP_LATTICE_BRACKET_NOTE_2026-05-03.md)
- [`PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md`](PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md)
- [`PLAQUETTE_BOOTSTRAP_FRAMEWORK_SPECIFIC_POSITIVITY_NOTE_2026-05-03.md`](PLAQUETTE_BOOTSTRAP_FRAMEWORK_SPECIFIC_POSITIVITY_NOTE_2026-05-03.md)

### Existing parallel-track infrastructure (strong-coupling extension)
- [`GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md)
- [`scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py`](../scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py)

### Standard methodology references
- Anderson, M. & Kruczenski, M. (2017). "Loop equations and bootstrap methods in the lattice." Nucl. Phys. B 921, 702.
- Kazakov, V. & Zheng, Z. (2022). "Analytic and numerical bootstrap for one-matrix model and 'unsolvable' two-matrix model." JHEP 06 (2024) 030. [arXiv:2203.11360](https://arxiv.org/abs/2203.11360)
- Kazakov, V. & Zheng, Z. (2024). "Bootstrapping lattice gauge theories with Wilson action." [arXiv:2404.16925](https://arxiv.org/abs/2404.16925)
- Cho, P., Mazac, D., Pufu, S., Zheng, Z. (2025). "Lattice SU(3) bootstrap." JHEP 12 (2025) 033.
