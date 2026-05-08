# Synthesis Note: Emergent Physics on Discrete Causal DAGs

**Claim type:** meta

## Audit scope

This file is an **overview / index** of an earlier program-phase
synthesis. It is **not** a single retained theorem and **must not** be
audited as one. The auditor (`synthesis_note`,
`audit_status=audited_conditional`, `claim_type=meta`) flagged this row
as `scope_too_broad`. The auditor's repair target reads, verbatim:

> scope_too_broad: split this synthesis note into atomic retained
> claims and provide each claim's cited runner note, frozen runner
> source, stdout/certificate, and current audit-ledger row.

The minimal-scope response in this PR is to **relabel** this document
as an overview/index rather than to physically split it into atomic
retained-claim files. Splitting is editorial work that belongs in a
dedicated review-loop pass (it would create new audit rows, runner
manifests, and certificates per claim, none of which can be safely
fabricated here). Until that split is performed:

- This file makes **no** retained-claim assertions of its own.
- Every quantitative readout, table, and "established" / "publishable"
  enumeration below is **historical program memory only**.
- The retained-status surface is the audit ledger
  (`docs/audit/AUDIT_LEDGER.md`) plus the per-runner notes, **not**
  this file.
- Where a sub-claim has a dedicated audit-clean note, this index
  points to it; where it does not, it is marked as having no
  separate audit-clean claim yet.

### Per-claim index (sub-claims referenced in this synthesis)

The list below pairs each thematic sub-claim mentioned in this file
with the dedicated note(s) where its current audit-clean status, if
any, lives. Inclusion in this index is **not** a status assertion:
the live status is whatever the audit ledger row for the linked note
says today.

- **Gravity signal on uniform DAGs (peaked response, sublinear mass
  window, distance falloff)** — see
  [`GRAVITY_LAW_CLEANUP_NOTE.md`](GRAVITY_LAW_CLEANUP_NOTE.md),
  [`GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md`](GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md),
  [`HARD_GEOMETRY_GRAVITY_WINDOW_NOTE.md`](HARD_GEOMETRY_GRAVITY_WINDOW_NOTE.md).
  The narrative `F ∝ M`, `delta ~ b^(-1.93)`, and `5.1 SE @ N=30`
  rollups in this file are program-memory, not retained law.
- **Linear-path-sum decoherence ceiling, `(1 - pur_min) ≈ 1.64 × N^(-1.01)`** —
  see [`DECOHERENCE_DECISION_NOTE.md`](DECOHERENCE_DECISION_NOTE.md),
  [`DECOHERENCE_ACTION_INDEPENDENCE_NOTE.md`](DECOHERENCE_ACTION_INDEPENDENCE_NOTE.md),
  [`MATCHED_2D_4D_DECOHERENCE_NOTE.md`](MATCHED_2D_4D_DECOHERENCE_NOTE.md).
- **Layer-normalization as Born-safe regulator** — no separate
  audit-clean retained-claim note tracked here yet; treat as
  historical program memory.
- **Hard-geometry / mirror-chokepoint / channel separation as the
  joint-coexistence enabler** — see
  [`MIRROR_CHOKEPOINT_NOTE.md`](MIRROR_CHOKEPOINT_NOTE.md),
  [`MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md`](MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md),
  [`MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md`](MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md),
  [`HARD_GEOMETRY_GRAVITY_WINDOW_NOTE.md`](HARD_GEOMETRY_GRAVITY_WINDOW_NOTE.md).
- **Generated asymmetry-persistence as a gravity-side lane** — see
  the `ASYMMETRY_PERSISTENCE_*` family
  ([`ASYMMETRY_PERSISTENCE_BORN_NOTE.md`](ASYMMETRY_PERSISTENCE_BORN_NOTE.md),
  [`ASYMMETRY_PERSISTENCE_COLLAPSE_NOTE.md`](ASYMMETRY_PERSISTENCE_COLLAPSE_NOTE.md),
  [`ASYMMETRY_PERSISTENCE_JOINT_CARD_NOTE.md`](ASYMMETRY_PERSISTENCE_JOINT_CARD_NOTE.md),
  [`ASYMMETRY_PERSISTENCE_MASS_SCALING_NOTE.md`](ASYMMETRY_PERSISTENCE_MASS_SCALING_NOTE.md),
  [`ASYMMETRY_PERSISTENCE_MASS_WINDOW_NOTE.md`](ASYMMETRY_PERSISTENCE_MASS_WINDOW_NOTE.md),
  [`ASYMMETRY_PERSISTENCE_PILOT_NOTE.md`](ASYMMETRY_PERSISTENCE_PILOT_NOTE.md)).
- **Stochastic collapse as a bounded helper (not asymptotic rescue)** —
  no separate audit-clean retained-claim note for the collapse-as-rescue
  reading; treat as historical program memory. The sign/no-go boundary
  side is partially covered by
  [`ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md`](ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md).
- **3D / higher-dimensional generalization** — see
  [`SYNTHESIS_NOTE_3D.md`](SYNTHESIS_NOTE_3D.md) (itself flagged
  conditional in the audit ledger),
  [`DIMENSIONAL_GRAVITY_TABLE.md`](DIMENSIONAL_GRAVITY_TABLE.md),
  [`HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md`](HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md),
  [`MATCHED_2D_4D_DECOHERENCE_NOTE.md`](MATCHED_2D_4D_DECOHERENCE_NOTE.md).
  The "4D escapes the ceiling" and "Dimensional Selection Principle"
  sub-sections below are program memory, not retained law.
- **Full Axiom Chain Closure (2026-04-03) rollup** — no separate
  audit-clean note exists for the axiom-by-axiom closure as a single
  claim; treat as historical program memory.
- **Dimensional Selection Principle (d=3 uniqueness)** — no separate
  audit-clean retained-claim note exists for the uniqueness reading;
  treat as historical program memory.
- **Honest-assessment "seven publishable quantitative results"
  enumeration** — this is a *summary* of the items above and inherits
  their per-claim status. It is not itself a retained surface.

A future review-loop pass should physically split this document into
the atomic per-claim files implied above, register a runner manifest
and certificate per claim, and open one audit row per atomic claim.
That is **out of scope** for this conditional-row repair.

---

**Date:** 2026-04-03
**Status:** support - structural narrative / historical synthesis only
This note is **not** a current retained-claim surface. It is a running
synthesis from an earlier program phase, kept for narrative continuity
and route history. Several of its quantitative claims (especially the
"publishable quantitative results" enumeration in §"Honest assessment",
the §"Full Axiom Chain Closure (2026-04-03)" axiom-by-axiom rollup, and
the §"Dimensional Selection Principle" three-dimensional uniqueness
read) are not currently registered as retained theorems with named
runners. They are cited here as program memory, not as live claims.

For the current per-claim status surface, use the audit ledger
(`docs/audit/AUDIT_LEDGER.md`), the per-runner notes, and the
publication-package documents under `docs/publication/`. Where a
specific quantitative readout in this note has a current frozen
runner, it is also captured in its own dedicated note.

The remainder of this section preserves the running-synthesis status
language for historical reference; treat it as narrative, not as a
current retained-status statement.

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

## Current retained read

> **Index notice:** see the **Audit scope** block at the top of this
> file. Per that block, every bullet below is *historical program
> memory* and inherits status from the per-claim notes listed in the
> per-claim index, not from this file.

This note started as a running synthesis and still contains some historical
claims below. The review-safe current read is:

1. **Gravity signal is real** on uniform DAGs at intermediate `N`, with the
   strongest retained point at `N=30` (`5.1 SE`). What is **not** locked is a
   final gravity law: the fixed-geometry cleanup narrowed the distance story to
   a peaked response with a falling tail, and the fixed-anchor mass sweep
   supports a positive **sublinear** mass window rather than a hardened `F∝M`
   law.

2. **Linear-path-sum decoherence has a real ceiling.** The retained baseline is
   approximately
   ```
   (1 - pur_min) = 1.64 × N^(-1.01)
   ```
   with `R² = 0.83`. The most robust interpretation is that overlap convergence
   pushes the model back toward coherence at large `N`.

3. **Layer normalization is the strongest retained Born-safe regulator.**
   It gives a large finite-`N` prefactor shift without reliably changing the
   asymptotic direction. The strongest safe framing is “bounded ceiling shift,”
   not “ceiling escape.”

4. **Hard geometry is the shared enabler.** Dense central-band removal,
   generated asymmetry-persistence, and the mirror chokepoint lane all support
   Born-safe bounded coexistence pockets. Dense central-band remains the best
   joint coexistence lane. Mirror chokepoint now retains through `N = 100`
   on the dense boundary scan, with a weak canonical boundary fit and a
   gravity wall at `N = 120`. The higher-symmetry `Z2 x Z2` lane is the best
   decoherence-side symmetry lead, while generated asymmetry-persistence
   remains the strongest gravity-side-alone lane. This is the most promising
   current architecture family.

5. **Collapse is a bounded helper, not a retained asymptotic rescue.**
   After the corrected Born/collapse hardening pass, collapse still helps in
   some hard-geometry pockets, but it does not presently support a clean
   exponent-changing claim.

6. **4D remains interesting but provisional.** The tracked 4D+LN artifact chain
   supports bounded finite-`N` improvement, but the stronger “4D gravity” and
   “4D champion coexistence” claims are not currently retained as artifact-backed
   results.

## Quantitative results (historical running summary)

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

**Distance scaling:** delta peaks at b ≈ 6 (half beam width),
falloff in far field: delta ~ b^(-1.93) (near 1/b²).
At b = 30: delta ≈ 0 (gravity vanishes at 2.5× beam width).

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

**Mass scaling:** delta = 0.13 × M^0.82 (alpha ≈ 1, consistent with F∝M).
Saturates at M>8 when mass covers half the layer.

**Distance scaling:** Peak deflection at b ≈ 6 (half beam width).
Falloff: delta ~ b^(-1.93) in far field (near 1/b²).
Zero at b = 30 (2.5× beam width).

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

> **Index notice:** see the **Audit scope** block at the top of this
> file. The items listed below are *historical program memory*; their
> live retained status is whatever the per-claim notes in the
> per-claim index report today.

1. **Gravity signal:** retained on uniform DAGs at intermediate `N`, with the
   strongest artifact-backed row at `N=30` (`5.1 SE`). The exact distance-law
   and mass-law story remains narrowed by the later fixed-geometry and
   fixed-anchor cleanup sweeps.

2. **Linear decoherence ceiling:** retained as an overlap-driven large-`N`
   limit with baseline scaling close to `1/N`.

3. **Born-safe regulation:** per-layer normalization is the strongest retained
   bounded regulator. It improves finite-`N` decoherence while remaining
   machine-clean on the corrected harness in the retained lanes.

4. **Hard geometry / channel separation:** the strongest current family.
   Dense central-band hard geometry remains the best joint coexistence pocket.
   Mirror chokepoint now freezes a retained bounded pocket through `N = 60`.
   Generated asymmetry persistence remains the strongest gravity-side-alone
   lane.

5. **Collapse:** retained only as a bounded helper inside hard-geometry
   pockets. It is not presently a hardened asymptotic rescue.

6. **Higher-dimensional lanes:** still exploratory. The tracked 4D+LN result
   is a bounded finite-`N` improvement, not a locked dimensional escape theorem.

7. **Emergence-facing growth lane:** the retained grown-graph density result
   favors a density optimum near `npl≈30`; dense grown graphs fail because the
   CLT dominates. This remains the best emergence-facing growth constraint,
   but it is not a better joint lane than the hard-geometry families above.

## Current lane ranking

1. Best engineered joint lane: dense central-band + layer norm.
2. Best symmetry-protected lane: mirror chokepoint / Z2-protected transfer.
3. Best decoherence-side symmetry lane: `Z2 x Z2`.
4. Best gravity-side lane: generated asymmetry-persistence + layer norm.
5. Best emergence-facing lane: grown-graph density optimum near `npl≈30`.

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

Gravity survives on combined propagator:
  LN+gap=4, N=50: delta=+1.57 (3.4 SE)

Effective range: pur_min=0.90 at N≈101, pur_min=0.99 at N≈1375.

### Stochastic collapse at mass nodes

Random dephasing at mass nodes (p_collapse=0.2, MC over realizations):

Born: |I₃|/P = 2.3e-5 (practically clean).

**Correction (N=200 test):** The apparent positive exponent (+0.21)
was dominated by k-band averaging, not the collapse mechanism itself.
When the collapse-specific contribution is isolated (collapse minus
no-collapse baseline at each N):

```
N=25:  collapse adds +0.070 to 1-pur
N=80:  collapse adds +0.021
N=200: collapse adds +0.002
```

The collapse-specific decoherence SHRINKS with N, following the same
CLT-driven convergence as the CL bath. More mass encounters at larger
N doesn't help because the per-encounter dephasing effect diminishes
as amplitudes become more uniform.

The positive total (1-pur) growing at large N comes from k-band
averaging (different k values produce different ψ, and the average ρ
is increasingly mixed), not from the collapse mechanism.

### Dimensional scaling: 4D escapes the ceiling

The decoherence exponent depends critically on dimension (definitive):

| d_spatial | alpha | R² | seeds | pur_min=0.99 at N |
|-----------|-------|-----|-------|-------------------|
| 1 (2D) | -1.01 | 0.83 | 24 | ~156 |
| 2 (3D) | ~-0.7 | — | limited | ~500 |
| 3 (4D) | **-0.178** | **0.84** | **24** | **~2.4 million** |
| 4 (5D) | **+0.11** | 0.19 | 12 | **never** |

From 2D to 5D, the exponent goes from -1.0 to +0.1.
In 5D, decoherence doesn't decay at all.

The exponent also depends on wavenumber k (2D):
```
k=3:  alpha = -0.32  (shallowest)
k=10: alpha = -2.52  (steepest)
```

### Analytical derivation: alpha ~ alpha_0 / d_spatial

Semi-analytical argument (see docs/EXPONENT_DERIVATION.md):
```
d=1 (2D): predicted -1.50, measured -1.01
d=2 (3D): predicted -0.75, measured ~-0.70  ← good match
d=3 (4D): predicted -0.50, measured -0.178  ← flatter than predicted
d=4 (5D): predicted -0.375, measured +0.11  ← even flatter
```

The 1/d prediction captures the trend but underestimates the
improvement. The actual dimensional effect is stronger than 1/d.

### Gravity-decoherence dimensional trade-off

Born on 4D+LN: machine zero (5e-16). Clean.
4D joint coexistence (N=25, field=0.5): gravity 4.0 SE + 16% decoherence.
4D gravity at default field (0.1): flat — signal diluted by
extra transverse dimensions.

The extra dimensions that help decoherence (more independent path
channels) hurt gravity (amplitude spread over more directions).
This is a real physics trade-off, not a parameter-tuning issue.

## What is NOT established

1. **4D gravity** — the 4D+LN propagator preserves Born but gravity
   is too weak to detect with 12 seeds. Either needs more seeds,
   stronger field coupling, or the physics genuinely trades off
   gravity strength for decoherence scalability in higher dimensions.

2. **Dynamic emergence** — 9 approaches tested, all fail. The gap
   may be a boundary condition on emergent spacetime.

3. **Continuum limit** — the power-law scaling suggests a connection
   to decoherence rates in quantum gravity, but the formal bridge
   is not built.

## Honest assessment

> **Index notice:** see the **Audit scope** block at the top of this
> file. The "seven publishable quantitative results" enumeration
> below is *historical program memory* and is **not** a retained
> theorem-set surface. Each item inherits status from its per-claim
> note in the per-claim index above.

This is a reduced computational model with seven publishable quantitative results:

1. **Gravity from phase:** deflection via phase valley mechanism,
   5.1 SE on uniform DAGs, 1/b² distance scaling, F∝M.

2. **Decoherence from CL bath:** (1-pur_min) ~ C×N^(-0.7 to -0.9).
   Clean mechanism (bin-resolved field contrast). R²=0.72-0.90.

3. **Regulated propagator:** per-layer normalization is Born-clean
   (|I₃|/P = 5e-16) and shifts the ceiling prefactor ~12x.

4. **Combined stacking:** layer norm + modular topology are
   complementary. pur_min = 0.619 at N=25 (38% decoherence, 6x
   over baseline). Effective range extends from N≈235 to N≈1355.

5. **Joint coexistence:** same propagator, same graphs, broad
   parameter window. The first reduced computational model (to our knowledge) where
   gravity and decoherence emerge from a single discrete structure.

6. **Dimensional escape:** 4D modular DAGs show exponent -0.22
   (near flat) vs 2D's -1.58. k=3 gives -0.32, k=10 gives -2.52.

7. **4D + LN combined:** the strongest configuration (R²=0.961):
   ```
   (1-pur_min) = 1.77 × N^(-0.53)
   pur_min=0.90 at N≈220, pur_min=0.99 at N≈16,500
   ```
   Three improvements stack: LN (prefactor 12x), gap (prefactor 3x),
   4D (exponent -0.53 vs -1.58). Effective range 70x over 2D baseline.

The model's limitation in 2D: the 1/N ceiling with exponent ~-1.5.
In 4D with regulation: the exponent halves to -0.53, extending the
effective range to N≈16,500. The ceiling is a low-dimensional
artifact, not a fundamental property of path-sum propagation.

## Full Axiom Chain Closure (2026-04-03)

> **Index notice:** see the **Audit scope** block at the top of this
> file. The axiom-by-axiom rollup below is *historical program
> memory*; no audit-clean note exists for this rollup as a single
> claim.

ALL axioms now close on locally-grown geometric DAGs:

| Axiom | Implementation | Status |
|-------|---------------|--------|
| 1 (network) | grow_geometric_dag(d_growth=3) | Closed |
| 2 (patterns=mass) | Amplitude concentration → 1/r field | Closed (3.1 SE) |
| 3 (space inferred) | Parent + random offset in d dims | Closed |
| 6 (continuation) | Radius-based edges | Closed |
| 8 (gravity) | Phase valley in emergent field | Closed (2.0 SE) |
| 9 (records=barrier) | Amplitude-density damping | Closed |

Results on fully emergent 4D grown graphs (N=30, 20 seeds):
```
pur_min = 0.967 (3.4% decoherence)
gravity = +0.442
N=18: pur_min = 0.949 (5.1% decoherence)
```

Nothing imposed. Everything from axioms.

## Dimensional Selection Principle (2026-04-03)

> **Index notice:** see the **Audit scope** block at the top of this
> file. The d=3 uniqueness reading below is *historical program
> memory*; no audit-clean note exists for the uniqueness reading.

d=3 transverse dimensions (3+1 spacetime) is the UNIQUE dimension
where both gravity and decoherence coexist on grown event-networks:

| d | decoherence | gravity | joint g×d |
|---|------------|---------|-----------|
| 1 | 0.6% | wrong sign | 0 |
| 2 | 2.3% | +0.05 | 0.001 |
| **3** | **3.5%** | **+0.52** | **0.018** |
| 4 | 4.7% | wrong sign | 0 |
| 5 | 4.4% | wrong sign | 0 |

d=3 is 15× higher than the next candidate (d=2) on the joint
figure of merit. The selection mechanism:
- d<3: not enough path diversity for decoherence
- d>3: too much amplitude dilution for gravity
- d=3: the unique balance point

This is a selection principle derivable from the model's axioms:
the dimension of emergent space is determined by the requirement
that both gravity-like deflection and decoherence-like record
formation can emerge from the same path-sum structure.

## Integration with Codex Mirror Lane

Two complementary approaches:

| | Grown geometric (ours) | S4 mirror (Codex) |
|---|---|---|
| Decoherence | 7.5% | 27% |
| Gravity | 2.5 SE | 7.2 SE |
| Born | 4e-16 | 3e-15 |
| Imposed? | Nothing | Graph structure |
| Axiom chain | Fully closed | Partially closed |

The gap (7.5% vs 27%) = cost of emergence. Approximate symmetry
from growth is weaker than exact structural Z₂ symmetry.

Dense grown graphs fail (npl=80 → 0.02% decoherence) because
CLT dominates. Sweet spot: npl≈30. Exact symmetry works at
any density because it structurally preserves slit separation.

## Remaining Open Questions

The open question: does a growth law exist where nodes fail to
nucleate in low-distinguishability regions? This is causal set
dynamics, not parameter sweeping, and requires theoretical work
beyond the computational program completed here.
