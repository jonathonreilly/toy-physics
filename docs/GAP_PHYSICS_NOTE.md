# Gap-as-Physics: Investigation Note

**Date:** 2026-04-02
**Branch:** claude/distracted-napier
**Status:** bounded - bounded or caveated result note

## Motivation

Nine attempts to dynamically generate the modular gap from local rules
failed. This investigation treats the gap as an object in its own right
and characterizes its properties.

## Experiments and results

### Exp 1: Gap stability under perturbation
Fill the gap with nodes at controlled densities.

| fill% | pur_cl (N=40) | S_norm | verdict |
|-------|---------------|--------|---------|
| 0     | 0.950         | 0.107  | baseline |
| 5     | 0.969         | 0.100  | mild degradation |
| 10    | 0.968         | 0.068  | S_norm drops |
| 25    | 0.984         | 0.044  | approaching uniform |
| 50    | 0.988         | 0.035  | nearly uniform |
| 100   | 0.992         | 0.028  | uniform ceiling |

**Finding:** Gradual degradation, no phase transition.

### Exp 2: Tapered gap profile
Gap width varies along causal direction.

**Finding:** All profiles (narrowing, widening, pinch, partial) within
~0.01 of uniform baseline. Gap location is weakly constrained.

### Exp 5a: Global amplitude penalty
Soft penalty `exp(-pen * exp(-y²/2σ²))` on all edges near y=0.

**Finding:** Works at N=40, collapses at N=60. Kills amplitude
throughput rather than creating channel separation.

### Exp 5b: Edge deletion (tension model)
Delete edges near y=0 with probability ~ tension.

**Finding:** Creates decoherence but breaks connectivity. At
sigma=2, tension=50: pur_cl=0.954 at N=40 but 0 connected seeds.

### Exp 5c: Cross-channel edge penalty
Penalize only edges crossing y=0, not all edges near y=0.

**Finding:** S_norm completely unchanged (0.0783 vs 0.0781 at N=25).
Single-slit amplitude still reaches all y-regions via within-channel
paths. Edge suppression alone cannot create which-path information.

### Exp 6: Physics-motivated node removal (D-threshold)
Remove nodes with low which-path distinguishability |D|.

**Finding:** |D| ≈ 0 for ALL nodes on uniform DAGs. 100% removal
at any threshold. The CLT bottleneck means no which-path information
exists at the node level before the gap creates it.

### Exp 3: Gap topology variants

| Variant | pur_cl (N=40) | Notes |
|---------|---------------|-------|
| hard-gap-4 | 0.950 | baseline |
| two-gap-w2-o2 | 0.938 | three channels, slightly better |
| angled-0.3 | 0.948 | tilted gap, matches baseline |
| angled-0.5 | 0.973 | steep tilt, mild degradation |
| gap-start-50% | 0.957 | partial: first half only |
| gap-end-50% | 0.975 | partial: last half only, weaker |
| bridge-1 | 0.954 | 1 bridge node/layer, robust |
| bridge-5 | 0.969 | 5 bridges, still works |

**Finding:** The gap is topologically robust. Angled gaps, partial
gaps, and bridged gaps all preserve decoherence. A few bridge nodes
do not break the effect.

### Exp 4: Gap codimension (2D gap in 3D)

| Variant | pur_cl (N=40) | pur_cl (N=60) |
|---------|---------------|---------------|
| no-gap | 0.967 | 0.980 |
| 1d-y4 | 0.951 | 0.969 |
| cyl-r4 | 0.958 | 0.958 |
| cyl-r6 | 0.928 | 0.953 |

**Finding:** Cylindrical exclusion (blocking z-leakage) gives
the best decoherence. Larger exclusion volume helps. Z-leakage
is real but modest.

## Six structural conclusions

### 1. The gap is about node absence
Edge suppression (cross-channel penalty) does not change S_norm.
Amplitude penalty kills throughput rather than creating separation.
Only removing nodes from the gap region creates which-path information.

### 2. The gap creates information, not preserves it
Node-level distinguishability |D| is zero on uniform DAGs. The hard
gap creates the which-path information that the CL bath then measures.
This is a chicken-and-egg: no local observable exists to threshold on
before the gap exists.

### 3. The gap is topologically robust
Angled gaps (up to slope 0.5), partial gaps (50% coverage), and
gaps with up to 5 bridge nodes per layer all preserve decoherence.
The gap doesn't need to be perpendicular, complete, or perfectly sealed.

### 4. Larger exclusion helps
Cylindrical gap (excluding a tube in y-z) outperforms 1D gap
(excluding a band in y only). More excluded volume means less
cross-channel amplitude leakage.

### 5. Degradation is gradual
Filling the gap with nodes produces smooth pur_cl increase with no
sharp transition. The gap is a quantitative mechanism: more gap
means more decoherence.

### 6. Gravity and decoherence co-improve under moderate removal
Removing nodes near y=0 (|y|<1.5 to |y|<3) simultaneously strengthens
both gravity (grav_t rises from +1.6 to +3.7 at N=80) and decoherence
(pur_cl drops from 0.979 to 0.962). The amplitude concentration in
channels helps the phase-valley mechanism. Only excessive removal
(|y|<4, 33% nodes) weakens gravity from connectivity loss.

### 7. The Born/decoherence Pareto frontier
No tested mechanism simultaneously preserves Born at machine precision
AND breaks the 1/N decoherence ceiling:

| Mechanism | Born |I₃|/P | Decoh scaling | Best use |
|-----------|------|------|-----------|
| Linear + \|y\| | 1e-17 | 1/N (3x better) | Born-compliant architecture |
| Layer norm | 0.5-0.9 | N^(-0.4) | Demonstrates trade-off |
| Collapse p=0.2 | 0.03 | N^(+0.2) | Best decoherence, marginal Born |

The CLT produces BOTH Born compliance and the 1/N ceiling. Breaking
one breaks the other. This is the fundamental constraint of linear
path-sum models on connected graphs.

### Exp 18: Dense pocket scaling (N=40-100)
LN+|y| on dense chokepoint (npl=60, connect_radius=3.0):
- Born: machine precision (2e-16 to 4e-16) at ALL N
- Purity: stable ~0.5 through N=100 (no 1/N ceiling!)
- Gravity: FAILS (dense geometry too narrow for phase valley)

|y|-removal is what makes LN Born-safe. LN alone: Born=0.14-0.30.

Connect_radius sweep reveals the architectural constraint:
- r=3.0: Born perfect, gravity noisy/absent
- r=3.5: Born=0.67 (destroyed)
- r=5.0: Born=1.0 (destroyed), gravity=+1.14

The Born-safe and gravity-safe radius ranges DON'T OVERLAP.
This is the geometric CLT/Born trade-off: path multiplicity that
enables gravity also causes LN to violate Born.

## Reconciliation with main (2026-04-03)

Several branch findings have been superseded by main:

1. **Collapse positive exponent retracted on main** — the N^(+0.21)
   scaling was a k-band averaging artifact. At N=200, collapse
   decoherence shrinks to ~0. The 1/N ceiling is universal.

2. **Dense central-band pocket found on main** — LN+|y|+collapse
   is Born-clean at machine precision on a specific dense geometry
   (npl=60, y_cut=2.0, connect_radius=3.0). N=60 gives purity=0.55
   with gravity positive. This resolves the Pareto frontier for
   that specific family.

3. **Our Born check (Exp 14) used random chokepoint DAGs** — the
   dense central-band geometry avoids the Born violation we found.
   Born compliance is family-dependent, not universal.

What survives from this branch:
- Gap characterization (Exps 1-6): node absence, gradual, robust
- |y|-removal concept → adopted as y_cut in main
- Co-improvement finding (Exp 12) → consistent with main
- Pareto frontier concept → refined by main (family-specific escape)

### Exp 19-20: k-band artifact + path-count bath
**Exp 19:** LN+|y| single-k purity = 1.000000. All non-collapse
"decoherence" from LN was k-band averaging artifact. Only collapse
creates genuine single-k mixing.

**Exp 20:** Path-count bath coupling S_path = 0.4-0.6 (10x larger
than y-bin S_norm, doesn't CLT-converge). But purity improvement is
modest because the CL bath saturates when D→0. The remaining purity
floor is set by the OVERLAP OF SINGLE-SLIT DETECTOR DISTRIBUTIONS,
not the bath coupling.

**Structural insight:** The CLT convergence of single-slit detector
distributions is the fundamental limit. It's upstream of any bath
formula — changing the coupling (y-bin to path-count) or the
propagator (linear to LN) cannot fix it. The only way to lower the
floor is to make single-slit distributions genuinely different at
the detector, which the CLT prevents on connected graphs.

## Implications for the project

The gap cannot be generated from local amplitude-based rules because
the information it creates (which-path distinguishability) does not
exist before the gap does. This is a **topological boundary condition**
on the allowed event space.

The robustness findings (conclusions 3-5) are physically interesting:
the gap doesn't need fine-tuning. It works when tilted, partial,
leaky, or extended to higher codimension. This suggests the relevant
feature is **channel separation** (a topological property) rather than
**gap geometry** (a metric property).

The remaining open question: can channel separation be reframed as
a **selection rule on event persistence** (axiom 2) rather than an
imposed geometric constraint? The D-threshold experiment (Exp 6)
shows this cannot be done via amplitude-based observables on uniform
graphs. A different observable — perhaps topological (path connectivity,
community structure) rather than amplitude-based — would be needed.

## Additional experiments (post-synthesis)

### Exp 9: Topological path-count asymmetry — POSITIVE
Path-count asymmetry |pA-pB|/(pA+pB) is spatially structured on
uniform DAGs and DOES NOT CLT-converge to zero (unlike amplitudes).
Removing low-asymmetry nodes creates decoherence:

| N | thresh | pur_cl | S_norm | rem% | vs baseline |
|---|--------|--------|--------|------|-------------|
| 40 | 0.1 | 0.923 | 0.349 | 16% | 0.990 baseline |
| 40 | 0.2 | 0.920 | 0.351 | 19% | beats hard-gap (0.950) |
| 50 | 0.3 | 0.915 | 0.243 | 26% | 0.962 baseline |
| 60 | 0.1 | 0.941 | 0.179 | 13% | beats hard-gap (0.955) |

First emergence mechanism that: (1) uses graph topology not amplitudes,
(2) works on uniform DAGs, (3) scales through N=60, (4) beats hard gap.

### Exp 9b: Large-N scaling (NPL=50)
At higher node density, path-count pruning scales through N=100:

| N | prune-0.05 | uniform | hard-gap |
|---|-----------|---------|----------|
| 40 | 0.927 | 0.960 | 0.948 |
| 60 | 0.931 | 0.974 | 0.971 |
| 80 | 0.960 | 0.987 | 0.973 |
| 100 | 0.977 | 0.985 | 0.957 |

Effect weakens at large N but remains present through N=100.
S_norm stays elevated (~0.15) vs uniform (~0.04) at all N.

### Exp 10: Locality test — mechanism is NOT local
Local proxies (1-hop y-balance, 2-hop y-balance) correlate weakly
with global path-count asymmetry (r=0.17-0.22). Pruning by local
proxies barely improves over baseline. The global pruning requires
full path enumeration from both slits.

At N=80: global-0.10 pur_cl=0.968 >> 1hop-0.30=0.984 ≈ uniform=0.987.

The simple geometric proxy |y|<3 approaches the global result at
large N (0.963 at N=80), suggesting the mechanism converges to
geometric node removal at scale.

**Final structural conclusion:** The gap is a topological boundary
condition. The correct observable for generating it (path-count
asymmetry) requires non-local information. No local self-maintenance
rule can replicate it because the which-path distinction is determined
by the non-local barrier/slit structure.

### Exp 11: Joint gravity+decoherence coexistence (24 seeds)
|y|<2 removal gives the best joint coexistence at N=80:
grav_t=+3.65, pur_cl=0.963, 9/24 seeds with both positive gravity
and pur_cl<0.98. k=0 control passes at all N.

### Exp 12: |y|-removal threshold sweep
Full sweep |y|<{0.5..4.0} at N=25..100. Key finding: **gravity and
decoherence improve simultaneously** up to |y|<3.0. Removal
concentrates amplitude in channels where the phase valley is strongest.

| N | best thresh | grav_t | pur_cl | joint |
|---|------------|--------|--------|-------|
| 40 | 4.0 | +2.64 | 0.943 | 9/24 |
| 60 | 4.0 | +2.93 | 0.971 | 10/24 |
| 80 | 3.0 | +3.26 | 0.968 | 10/24 |

The gravity-decoherence trade-off is NOT a trade-off at moderate
thresholds. Both phenomena benefit from channel concentration.

### Exp 13: Layer normalization + |y|-removal — RETRACTED
LN + |y|<2 gave N_half=85,571 with strong joint coexistence.
**RETRACTED by Exp 14:** LN destroys Born rule (|I3|/P=0.38-0.88
on chokepoint barriers). The decoherence improvement is real but
the propagator breaks pairwise interference.

### Exp 14: Born rule check — LN fails
Three-slit Sorkin test on chokepoint 3D DAGs:

| mode | |I3|/P | verdict |
|------|--------|---------|
| linear | 2e-16 | PASS (machine precision) |
| linear+\|y\| | 1e-17 | PASS (machine precision) |
| LN | 0.51-0.88 | FAIL |
| LN+\|y\| | 0.38-0.45 | FAIL |

**Best Born-compliant combined: linear + |y|<2 at N=80**
grav_t=+3.65, pur_cl=0.963, 9/24 joint seeds.
Subject to 1/N CLT ceiling.

### Exp 7: Gap + intermittent normalization
Intermittent amplitude normalization (K=5,10,20) has zero effect on
CL bath purity. The CL bath formula uses S_norm = sum|ba-bb|^2/(NA+NB),
which is invariant under global rescaling. The gap and intermittent
norm operate on orthogonal aspects: gap controls which-path information,
norm controls amplitude concentration.

### Exp 8: Cylindrical gap scaling (N=12-60)
cyl-r6 retains (1-pur_cl) floor ~0.05-0.07 vs no-gap ~0.02-0.03.
But scaling is noisy (R²<0.35) with no clean 1/N power law on 3D
modular DAGs. Z-leakage blocking helps the prefactor, not the
scaling exponent.

## Scripts

| Script | Experiment |
|--------|-----------|
| gap_stability_perturbation.py | Exp 1 |
| gap_tapered_profile.py | Exp 2 |
| gap_tension_stability.py | Exp 5a, 5b |
| gap_cross_channel_penalty.py | Exp 5c |
| gap_penalty_scaling.py | Exp 5b scaling |
| gap_node_persistence.py | Exp 6 |
| gap_topology_variants.py | Exp 3 |
| gap_codimension.py | Exp 4 |
| gap_intermittent_norm.py | Exp 7 |
| gap_cylindrical_scaling.py | Exp 8 |
| gap_topological_asymmetry.py | Exp 9 |
| gap_pathcount_large_n.py | Exp 9b |
| gap_local_asymmetry.py | Exp 10 |
| gap_joint_coexistence.py | Exp 11 |
| gap_y_removal_sweep.py | Exp 12 |
| gap_layernorm_combined.py | Exp 13 (RETRACTED) |
| gap_ln_born_check.py | Exp 14 |
| gap_gravity_quantitative.py | Exp 15 |
| gap_collapse_combined.py | Exp 16 |
| gap_collapse_born_check.py | Exp 17 |
