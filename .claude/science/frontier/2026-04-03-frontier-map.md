# Frontier Map: 2026-04-03

## Coverage Summary
- Total scripts: 518
- Total log files: 271
- Mechanism families: 16+
- Confirmed results: 5 (publishable quantitative)
- Unvalidated observations: ~8 (higher-dim, emergence variants)
- Dead ends: 12+ (closed lanes)
- Emergence approaches tested: 9 (all fail asymptotically)

## Family Census

| Family | Scripts | Logs | Status |
|--------|---------|------|--------|
| Pocket wrap / suppressor | ~156 | ~99 | EXHAUSTED (Codex lane, extensive sweeps done) |
| Decoherence architectures | ~46 | ~42 | EXHAUSTED (14 architectures, CL bath retained) |
| Gravity / distance / mass | ~23 | ~25 | ACTIVE (distance law, mass scaling confirmed) |
| Higher-dim (3D/4D/5D) | ~31 | ~11 | ACTIVE (3D/4D positive, 5D marginal) |
| Field variants (causal, hybrid) | ~24 | ~8 | PARTIAL (source-projected lead, hybrid closed) |
| Directional b / source-projected | ~20 | ~16 | ACTIVE (bounded modular lead, distance trend) |
| Topology (modular, hierarchical) | ~12 | ~8 | CONFIRMED (modular DAG is retained family) |
| Emergence (9 approaches) | ~21 | ~5 | EXHAUSTED (connection/placement/removal all fail) |
| Dense prune / guard | ~8 | ~1 | CLOSED ASYMPTOTICALLY (intermediate-N only) |
| Nonlinear / layer norm | ~6 | ~1 | CONFIRMED (layer norm Born-clean, 12x prefactor) |
| Scaling law / ceiling | ~4 | ~40 | CONFIRMED (1/N universal, exponent -0.8 to -2.5) |
| Collapse / stochastic | ~2 | ~3 | CLOSED (positive exponent was k-band artifact) |
| Born rule | ~1 | ~1 | CONFIRMED (machine precision on linear + layer norm) |
| Joint / combined tests | ~2 | ~1 | CONFIRMED (gravity + decoherence coexist) |
| Infrastructure | ~14 | — | — |

## Parameter Space Coverage

### Well-covered
- N (graph layers): 8-200 (dense coverage)
- nodes_per_layer: 10, 15, 25, 40
- connect_radius: 2.0-5.0
- y_range: 6.0-18.0
- gap (modular): 0.0-8.0 in 0.5 steps
- k_band: [3,5,7] standard; some tests at single k
- seeds: 4-24 per point (24 is the standard)
- lambda (CL bath): 5-100 (saturates at 10)
- env_depth: 1-53 layers (no effect on ceiling)
- Dimensions: 2D, 3D, 4D, 5D tested

### Gaps in parameter space
1. **N > 200** — only collapse test went this high, and it was artifactual
2. **Very sparse graphs** (connect_radius < 2.0) — untested regime
3. **Very dense graphs** (nodes_per_layer > 50) — limited to 5D pilot
4. **Non-uniform k-band** — always used [3,5,7], never swept k itself
5. **Field strength** — always 0.1, never swept

## Observable Coverage

| Observable | Measured? | Across families? | Notes |
|------------|-----------|-----------------|-------|
| pur_min (D=0 purity) | Yes | All families | Primary decoherence metric |
| pur_cl (CL bath purity) | Yes | Most families | Bath-dependent decoherence |
| Gravity delta (deflection) | Yes | Uniform + modular | Paired per-seed SE |
| Born |I₃|/P (Sorkin) | Yes | Linear + all nonlinear | Corrected with -P(∅) |
| S_norm (bath contrast) | Yes | Most | Grows with N |
| Interference visibility | Yes | 2D, 3D | True V_gain weak at large N |
| Distance scaling (1/b) | Yes | 2D uniform | 1/b² in far field |
| Mass scaling (F∝M) | Yes | 2D uniform | alpha=0.82, noisy |
| Effective gap | Yes | Emergence tests | Node-absence measurement |
| Channel bias | Yes | Emergence tests | Same-half edge fraction |
| Overlap O = |<ψ_A|ψ_B>|² | Yes | Scaling law | Drives ceiling |
| 3D gravity | Yes | 3D modular | Weak signal |
| 4D decoherence | Yes | 4D dense modular | Best large-N lane |

### Unmeasured / under-measured
1. **Entanglement entropy** — never computed (would complement purity)
2. **Mutual information** between slit label and detector — never computed
3. **Path length distribution** — never measured directly
4. **Phase distribution at detectors** — only measured indirectly via overlap
5. **Connectivity spectrum** (eigenvalues of adjacency) — never computed

## Confirmed Results (code-supported, corrected)

1. Gravity: 5.1 SE at N=30, 1/b² far-field, F∝M (alpha=0.82)
2. Decoherence: (1-pm) ~ C×N^(-alpha), alpha ∈ [-2.5, -0.8], sign universal
3. Layer norm: Born-clean (4e-16), 12x prefactor shift
4. Combined stacking: (1-pm) = 5.88×N^(-0.88), R²=0.946
5. Joint coexistence: gravity 3.4 SE on combined propagator

## Unvalidated Observations

1. 4D modular decoherence stays bounded through N=100 (needs strict visibility)
2. 5D dense pilot shows narrow positive window (density-sensitive)
3. Source-projected field survives 32-seed audit (bounded modular only)
4. Mass-path guard validated on same-graph control (narrow)
5. 3D mass scaling (provisional, did not cleanly recover power law)
6. Layer norm at N=80 (pur_min=0.948, needs 24-seed confirmation)
7. Gravity on 3D modular (signal present but weak, needs more seeds)
8. Exponent universality (weakly universal, CV=0.39)

## Dead Ends (do not revisit)

1. 1/delay^p attenuation — produces repulsion
2. Connection-bias emergence (5 variants) — CLT defeats all
3. Placement-bias emergence (3 variants) — wrong gap size/location
4. Node removal — intermediate-N only, ceiling returns at N=80
5. Stochastic collapse — positive exponent was k-band artifact
6. Continuous epsilon nonlinearity — no useful Pareto point
7. Phase equalization — Born destroyed (|I₃|/P = 0.6)
8. Saturation propagator — small Born cost (7e-3), marginal improvement
9. All 14 CL bath/kernel alternatives on uniform DAGs — fail
10. G2 coarse-grained propagator — kills interference
11. Smart prune vs adaptive prune — not an improvement under controls
12. Hierarchical alpha — collapses under fixed-position control

## Top 5 Highest-Value Gaps

### 1. Analytical derivation of the 1/N ceiling
**Why:** The exponent is always negative but varies [-2.5, -0.8] with
graph parameters. A derivation from the path-sum structure would:
(a) prove decoherence is a finite-size effect, (b) predict the
exponent from connectivity/extent ratio, (c) be the capstone
theoretical result tying everything together.
**Feasibility:** Theoretical — needs pen-and-paper CLT argument on
DAG path sums. The numerical data (12 parameter settings) provides
the target.
**Effort:** Theoretical work, not computation.

### 2. 4D decoherence as the asymptotic escape
**Why:** 4D dense modular DAGs show decoherence bounded away from 1
through N=100 (per Codex's higher-dim work). If 4D genuinely changes
the exponent (not just prefactor), this is the first real escape from
the 1/N ceiling. The 2D universality test showed the exponent depends
on connectivity — 4D increases effective connectivity.
**Feasibility:** Scripts exist (four_d_decoherence_large_n.py). Need
to push to N=200 and fit the exponent properly.
**Effort:** 1-2 hours computation.

### 3. k-dependence of the exponent
**Why:** All tests use k-band [3,5,7] and average. The exponent might
depend on k. Single-k scaling laws could reveal whether the ceiling
is a high-k or low-k phenomenon, which would inform the physics.
**Feasibility:** Easy — rerun clt_ceiling_scaling with single k values.
**Effort:** Quick (< 1 hour).

### 4. Layer norm + modular + 4D triple combination
**Why:** Layer norm (12x prefactor), modular gap (channel separation),
and 4D (increased connectivity) are three independent improvements.
If they stack in 4D as they do in 2D, the effective range could
extend to N > 10,000.
**Feasibility:** Needs adaptation of 4D scripts to include layer norm.
**Effort:** Moderate (2-3 hours).

### 5. Mutual information between slit label and detector position
**Why:** Purity measures total coherence loss. Mutual information
measures HOW MUCH information about which-slit is available at the
detector. This is the physically relevant quantity for decoherence.
If MI decays differently from purity, the physics story changes.
**Feasibility:** Needs new code (compute conditional distributions).
**Effort:** Moderate (new script, ~2 hours).
