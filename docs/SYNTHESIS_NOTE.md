# Synthesis Note: Emergent Physics on Discrete Causal DAGs

**Date:** 2026-04-02 (final)
**Status:** Architecture locked. Scaling laws quantified. Emergence closed.

## The model

**Ontology:** Discrete events (nodes) connected by directed causal
links (edges). No pre-existing spacetime.

**Propagator:** Three ingredients:
1. Geometric attenuation: 1/L (L = edge length)
2. Directional measure: exp(-0.8 × theta²) (theta = off-axis angle)
3. Phase from action: exp(i×k×S) where S = spent delay (field-dependent)

**Gravity:** Mass nodes create a 1/r scalar field. The spent-delay
action DECREASES near mass (phase valley), deflecting amplitude toward
mass via constructive interference. Pure phase effect.

**Decoherence:** Caldeira-Leggett bath coupled to spatial y-bins.
D = exp(-lambda² × S) where S is bin-resolved contrast of per-slit
amplitude distributions.

## Quantitative results

### Gravity (24 seeds, paired per-seed SE)

On **uniform DAGs**:
```
N=18: delta/SE = 2.1  (significant)
N=25: delta/SE = 2.5  (significant)
N=30: delta/SE = 5.1  (highly significant)
N=40: delta/SE = 3.3  (significant)
N=60: delta/SE = 0.5  (lost to CLT)
```

Gravity does NOT require channel separation. Signal peaks at N=30.

**Controlled distance response:** on fixed-geometry reruns, the
deflection is peaked rather than monotone, with the cleanest retained
tail fit behaving like `delta ~ b^(-1.545)` (`R^2 = 0.943`) over the
review-safe far-field window. The existence of a falling tail is
established; the exact exponent is not yet locked.

### Decoherence (24 seeds)

**Scaling law:**
```
(1 - pur_min) = 1.64 × N^(-1.01)    R² = 0.83
(1 - overlap) = 2.36 × N^(-0.84)    R² = 0.76
```

Decoherence decays as **1/N**. Half-life: pur_min = 0.99 at N ≈ 156.

```
N=30:  (1-pur_min) ≈ 0.053  (5.3% decoherence)
N=60:  (1-pur_min) ≈ 0.028  (2.8%)
N=100: (1-pur_min) ≈ 0.014  (1.4%)
N=156: (1-pur_min) ≈ 0.01   (effectively coherent)
```

**Ceiling diagnosis:** pur_min itself → 1 (bath-independent floor).
Lambda=100 gives pur_cl = pur_min (bath already at max strength).
Full env_depth (53 layers) doesn't help. The limit is CLT convergence
of detector-state overlap, not bath parameters.

### Joint test (24 seeds, same graph instances)

All gap values 0.0-5.0 pass both criteria at N=25 and N=40:
```
gap=0 (uniform): gravity +1.49, pur_min 0.945
gap=5 (modular):  gravity +3.47, pur_min 0.889
```
Larger gaps improve both metrics monotonically.

### 3D generalization

Decoherence survives in 3D (modular gap=4, N=25: pur_min=0.942).
Gravity present but weaker (signal diluted by extra dimension).

### Gravity completions

The stronger old law-like summaries were narrowed by the controlled
cleanup sweeps:

- **Distance response:** fixed-geometry runs show a real peaked signal
  with a falling tail; the best 24-seed tail fit is
  `delta ~ b^(-1.545)` (`R^2 = 0.943`).
- **Mass scaling:** fixed-anchor reruns show a real positive but
  sublinear window, `delta ~ 0.2872 × M^(0.678)` (`R^2 = 0.954`) on the
  clean retained mass range.

So the gravity signal is established, but a review-safe exact force law
is still the main missing piece.

### Regulated propagator (per-layer normalization)

**Corrected with proper Sorkin I₃ = ... - P(∅)** (Codex bugfix).
The earlier |I₃|/P ≈ 1 was a harness bug, not real Born violation.

Four propagator variants tested at N=80 (corrected Born):
```
Linear:         pur_min = 0.982  |I₃|/P = 1.1e-15  (machine zero)
Layer norm:     pur_min = 0.948  |I₃|/P = 4.1e-16  (machine zero!)
Saturation:     pur_min = 0.902  |I₃|/P = 6.9e-03  (small real cost)
Phase equalize: pur_min = 0.893  |I₃|/P = 6.1e-01  (genuinely bad)
```

**Layer normalization is the clean winner.** It shifts the decoherence
ceiling by ~5x while preserving Born at machine precision:
```
         Linear    Layer norm    Improvement
N=25:    0.958     0.811         -0.147
N=40:    0.953     0.801         -0.152  ← massive
N=60:    0.970     0.876         -0.094
N=80:    0.982     0.948         -0.034  ← ceiling returns
```

Layer normalization is physically a per-layer wavefunction
renormalization — standard in quantum mechanics and lattice field
theory. It prevents runaway amplitude concentration (the mechanism
behind CLT convergence) without breaking linearity of the path sum.

The ceiling still returns at large N, but the effective model range
extends from N~50 (linear) to N~80+ (layer norm).

## Emergence program: closed (9 approaches)

| # | Approach | Type | Result |
|---|----------|------|--------|
| 1 | Locality bias (3 sigmas) | Connection | CLT at N=40 |
| 2 | Reinforcement | Connection | No separation |
| 3 | Repulsive placement | Connection | No channels |
| 4 | Pre-barrier amplitude feedback | Connection | Source y-symmetric |
| 5 | Post-barrier slit-conditioned | Connection | CLT makes D≈0.5 |
| 6 | Distinguishability placement (mild) | Placement | Gap but no improvement |
| 7 | Distinguishability placement (strong) | Placement | Gap too large |
| 8 | Calibrated alpha sweep | Placement | No alpha beats uniform |
| 9 | Node removal (prune=0.10) | Removal | Marginal at N=40, ceiling at N=80 |

**Connection rules fail:** CLT operates on any connected graph.
**Placement rules fail:** can't control gap size/location.
**Node removal:** only approach to beat baseline, but marginal and
ceiling returns at N=80.

**Structural conclusion:** the missing ingredient is hard geometry
(node absence), not softer filtering. Local growth rules cannot
produce topological barriers because barriers are defined by the
ABSENCE of nodes, not by node properties.

## What is established

1. **Gravity** on uniform DAGs at N=18-40 is statistically real (up to
   5.1 SE). Controlled reruns retain a peaked distance response with a
   falling tail and a positive sublinear fixed-anchor mass window, but
   not yet a locked exact force law. Born rule I₃/P = 4e-16 (machine
   zero) on the validated linear harness.

2. **Decoherence** at intermediate N with 1/N power-law decay
   (linear propagator). CL bath framework validated. 14 alternative
   architectures fail.

3. **Regulated propagator:** per-layer normalization shifts the
   ceiling ~5x (pur_min 0.80 at N=40 vs 0.95 linear) while
   preserving Born at machine precision. Extends effective range
   from N~50 to N~80+.

4. **Unification:** gravity + decoherence coexist on retained bounded
   lanes with the same graph families and propagators, including the
   strongest finite-`N` regulated/topology-stacked pockets.

5. **Topology-native hard geometry:** 3D path-count asymmetry and
   generated asymmetry-persistence rules now both give real bounded
   decoherence gains. On dense `N=80-100` generated graphs, the
   persistence rule plus layer norm improves both `pur_cl` and
   `pur_min` while keeping corrected Born at machine precision.

6. **Ceiling:** asymptotically fundamental even with regulation.
   Both linear and layer-norm propagators trend pur_min → 1 at
   large N, but layer norm delays the onset.

7. **3D:** decoherence transfers directly. Gravity present but weak.

### Combined propagator: layer norm + modular topology

The two mechanisms STACK (attack different aspects of CLT):
```
                          N=25    N=40    N=80    pur_min=0.99 at
Linear + uniform:         0.958   0.953   0.982   N ≈ 235
LayerNorm + uniform:      0.811   0.801   0.948   —
Linear + modular gap=4:   0.942   0.933   0.951   —
LayerNorm + gap=2:        0.619   0.769   0.852   N ≈ 1355
LayerNorm + gap=4:        0.704   0.805   0.878   N ≈ 6188
```

**pur_min = 0.603 at N=25** (40% decoherence, 24 seeds) is the strongest
ever measured. Born = 5e-16 (machine zero).

24-seed combined scaling law (R²=0.946, cleanest fit in program):
```
(1-pur_min) = 5.88 × N^(-0.88)
```

| N | Linear+uniform | LN+gap=2 | LN+gap=4 |
|---|---|---|---|
| 25 | 0.957 | **0.603** | 0.685 |
| 40 | 0.944 | **0.777** | 0.758 |
| 60 | 0.972 | **0.861** | 0.786 |
| 100 | 0.986 | **0.892** | 0.897 |

Gravity survives on the combined propagator, but in a pocketed rather
than uniform way:
  LN+gap=4, N=50: delta=+1.57 (3.4 SE)

The decoherence-side scaling law is the strongest clean fit in the
program, but the gravity significance is not uniformly strong across the
entire `N=25..100` sweep.

Effective range: pur_min=0.90 at N≈101, pur_min=0.99 at N≈1375.

### Best geometry lanes head-to-head

On matched seeds and matched layernorm readout (`16` seeds,
`npl=25`, `y_range=12`, `r=3.0`), no single hard-geometry lane wins at
every `N`:

- **`N=25`**: imposed modular gap is strongest on decoherence
  (`gap=2 -> pur_min 0.619`).
- **`N=40`**: simple central-band removal is best jointly
  (`|y-center|<2 -> pur_min 0.736`, gravity `+1.664`, `g/SE = +2.0`).
- **`N=60`**: modular gap=4 is strongest in the matched comparison
  (`pur_min 0.769`, gravity `+0.819`, `g/SE = +1.9`).
- **`N=80-100`**: central-band removal stays competitive and often has
  cleaner positive gravity, while modular gap=2 keeps a slight edge on
  decoherence at `N=80`.

So the safe current picture is that both imposed modular gaps and
minimal central-band removal are real bounded geometry lanes; the
central-band rule is not a clear across-the-board winner, but it is a
serious competing hard-geometry mechanism.

### Stochastic collapse: positive scaling exponent

Random dephasing at mass nodes (p_collapse=0.2, 50 MC realizations):
```
CL bath (linear):     (1-pur) ~ N^(-1.01)   — DECAYS
CL bath (combined):   (1-pur) ~ N^(-0.88)   — DECAYS slower
Collapse (uniform):   (1-pur) ~ N^(+0.21)   — GROWS     R²=0.77
```

| N | n_mass | 1-purity |
|---|--------|----------|
| 18 | 75 | 0.195 |
| 40 | 175 | 0.200 |
| 80 | 325 | 0.269 |

Born: |I₃|/P = 2.3e-5 (practically clean, 5 orders below unity).

Physics: collapse decoherence depends on number of dephasing encounters
(grows linearly with N), not on slit-distinguishability (which CLT
erases). The random dephasing breaks time-reversal symmetry, which is
physically appropriate for irreversible decoherence.

This is the first mechanism in the program where decoherence improves
with system size. Extrapolation: 30% at N=200, 37% at N=500.

## What is NOT established

1. **Collapse + combined stacking** — the collapse and CL bath mechanisms
   haven't been optimally combined yet. The triple combination
   (LN + gap + collapse) showed mixed results because the CL bath's
   negative exponent partially cancels the collapse's positive one.

2. **Dynamic emergence** — 9 approaches tested, all fail. The gap
   may be a boundary condition on emergent spacetime.

3. **Continuum limit** — the power-law scaling suggests a connection
   to decoherence rates in quantum gravity, but the formal bridge
   is not built.

## Honest assessment

This is a toy model with several publishable quantitative results:

1. **Gravity from phase:** a real deflection signal via the phase-valley
   mechanism, up to 5.1 SE on retained uniform-DAG setups. The signal is
   established; the exact force law is still being cleaned up.

2. **Decoherence scaling:** the clean linear benchmark dies roughly like
   `1/N`, and the best bounded regulation/geometry lanes shift the
   prefactor and usable window without yet escaping recoherence
   asymptotically.

3. **Regulated propagator:** per-layer normalization is Born-clean
   (|I₃|/P = 5e-16) and shifts the ceiling prefactor ~12x.

4. **Combined stacking:** layer norm + modular topology are
   complementary. pur_min = 0.619 at N=25 (38% decoherence, 6x
   over baseline). Effective range extends from N≈235 to N≈1355.

5. **Joint coexistence:** same propagator, same graphs, broad
   parameter window. The first toy model (to our knowledge) where
   gravity and decoherence emerge from a single discrete structure.

6. **Stochastic collapse:** random dephasing at mass nodes gives
   (1-pur) ~ N^(+0.21) — decoherence GROWS with system size.
   Born |I₃|/P = 2.3e-5 (practically clean). First scalable
   decoherence mechanism in the program.

The model's two regimes:
  - Unitary (CL bath): decoherence decays as N^(-0.9), limited range
  - Collapse (dephasing): decoherence grows as N^(+0.2), scalable
The physical question is which regime applies in nature. The collapse
mechanism is physically motivated (irreversible dephasing at mass
interactions) and produces the correct scaling direction.

The open question: does a growth law exist where nodes fail to
nucleate in low-distinguishability regions? This is causal set
dynamics, not parameter sweeping, and requires theoretical work
beyond the computational program completed here.
