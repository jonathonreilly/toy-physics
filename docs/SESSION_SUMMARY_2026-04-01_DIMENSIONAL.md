# Session Summary: Dimensional Extension & Distance Law Investigation
**Date:** 2026-04-01
**Branch:** claude/gracious-pasteur
**Status:** Investigation complete. All experimental avenues closed.

## What was accomplished

17 commits exploring the model's behavior in 3D, 4D, and 5D, plus
a thorough investigation of the distance scaling question.

## Established results (HIGH confidence)

### 3D gravity
- Attraction confirmed on uniform and modular 3D DAGs (t up to 8.5)
- **Mass scaling alpha ~ 0.58** in 3D continuum limit (converges with density)
- F ~ sqrt(M) at optimized parameters (alpha = 0.52)
- k=0 → zero (pure phase effect), field sign controls direction

### 3D decoherence
- CL bath achieves **pur_cl = 0.955 at N=80** (2D gives 0.987)
- CLT ceiling delayed ~2x in N vs 2D
- S_norm stays bounded (0.07-0.30) through N=100
- Modular gap=3 optimal for large-N

### 3D unification
- Gravity + decoherence + Born rule coexist on same 3D modular DAGs
- Born rule: I_3/P = 3e-16 with chokepoint barriers
- Interference proxy signal confirmed (strict visibility metric not applied)

### 4D gravity
- **alpha = 1.07 on gap=5** (F ~ M achievable with optimized params)
- Mass scaling increases monotonically with spatial dimension
- Alpha is parameter-dependent, not a pure function of dimension
- The (d-1)/2 formula was tested and NOT confirmed

### 4D decoherence
- pur_cl = 0.904 at N=20 (strongest decoherence in the model)
- Limited to N=30 (computational cost)

### Continuum limit
- Alpha converges to ~0.58 in 3D as node density increases
- Spread of 0.083 at high density — proper continuum limit exists for mass scaling

## Distance scaling: thoroughly closed

b-independence of the gravitational force is structural in the linear
path-sum + phase valley architecture. Tested and closed:

| Avenue | Result |
|---|---|
| Propagator power sweep (p=0 to 2) | Flat for all p |
| Node density scaling (15-120/layer) | Flat at all densities |
| Locality-shell graphs (7 families) | Flat for all families |
| Regular 3D lattice | Flat (shift/b ~ constant) |
| Causal field propagation | **RETRACTED** — artifact of moving mass window |

### Root cause (derived)
The Laplacian-relaxed field permeates the entire graph (f > 0 everywhere).
The graph-averaged field depends on total mass count, not mass position.
Paths preserve transverse position (not scrambling), but the extended
field means all paths feel similar phase perturbation.

### Causal field retraction
Initial tests showed apparent ~1/b with decay=0.5. Two confounds:
1. Moving y-window changed source count/geometry with b
2. Positive-only power law fit inflated apparent trend

Fixed-mass verification on main: both Laplacian (shift ~ b^0.461)
and causal (shift ~ b^1.013) show no falloff.

## Methodological lessons

1. **Moving mass windows confound b-sweeps.** Fixed-mass controls
   are essential for distance scaling tests.

2. **Positive-only power law fits** can create apparent trends from
   noise. Include negative and near-zero points in fits.

3. **Per-dimension parameter tuning** inflates dimensional progression
   patterns. Unified parameters give more honest (weaker) results.

4. **Skip-layer edges** in random DAGs allow paths to bypass barriers,
   breaking the Sorkin test. Chokepoint barriers required for Born rule.

5. **"All four coexist"** requires precise metrics. The 3D result uses
   an interference proxy; the 4D result uses a companion Born graph.

## Caveats on specific results

- **4D alpha=1.07:** Uses connect_radius=4.5, gap=5 (optimized).
  Unified parameters give alpha=0.64 in 4D. Alpha is parameter-dependent.

- **4D strict visibility:** Not verified under hardest metric. The
  detector profile keyed on raw float y saturates to 1.0/0.0.

- **5D:** Graphs too sparse with current node counts. Signal unreliable.

- **3D interference:** Joint test uses max|P_both - P_A - P_B|/mean_classical,
  which is a proxy, not the strict visibility-gain metric.

## Scripts delivered (this session)

### 3D
- `three_d_gravity_modular.py` — attraction, distance, mass scaling
- `three_d_mass_scaling_focus.py` — 24-seed mass scaling
- `three_d_sanity_k0.py` — sanity checks
- `three_d_decoherence.py` — CL bath (N=10-40)
- `three_d_decoherence_large_n.py` — scaling (N=15-80)
- `three_d_joint_test.py` — gravity+decoh+Born+interference
- `three_d_born_rule_debug.py` — Born rule debug
- `three_d_born_rule_fixed.py` — threshold-free propagation
- `three_d_born_rule_chokepoint.py` — chokepoint fix
- `three_d_linearity_check.py` — direct linearity verification
- `three_d_large_n_confirm.py` — N=20-100 joint confirmation

### 4D/5D
- `four_d_gravity.py` — 4D gravity and mass scaling
- `four_d_decoherence.py` — 4D CL bath scaling
- `dimensional_scaling_law.py` — unified d=1-4 comparison

### Distance scaling investigation
- `continuum_limit_3d.py` — alpha convergence with density
- `propagator_power_sweep.py` — p-sweep (closed avenue)
- `locality_shell_gravity.py` — 7 locality families (closed)
- `lattice_gravity_distance.py` — regular lattice (closed)
- `path_sampling_analysis.py` — path sampling mechanism
- `field_localization_test.py` — field localization variants
- `causal_field_gravity.py` — causal field (RETRACTED)
- `causal_field_tuning.py` — decay tuning (RETRACTED)
- `causal_field_full_test.py` — causal field characterization

### Analyses
- `.claude/science/analyses/three-d-gravity-2026-04-01.md`
- `.claude/science/analyses/three-d-decoherence-2026-04-01.md`
- `.claude/science/analyses/three-d-joint-test-2026-04-01.md`
- `.claude/science/analyses/dimensional-progression-2026-04-01.md`
- `.claude/science/analyses/dimensional-scaling-law-2026-04-01.md`
- `.claude/science/derivations/b-independence-2026-04-01.md`
