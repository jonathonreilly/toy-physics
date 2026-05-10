# Continuum / Asymptotic Bridge Note

---

**This is a synthesis/overview note. It does not establish any retained claim.**
For retained claims, see the per-claim notes referenced from the
`## Audit scope` block below.

---

**Status:** support / historical synthesis only — does not propagate retained-grade
**Date:** 2026-04-01
**Claim type:** meta
**Claim scope:** support / historical synthesis only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no
**Purpose:** Separate finite-size artifacts from potentially retained
discrete structure. Gate C of the review-hardening backlog.

## Audit scope (relabel 2026-05-10)

This file is an **overview / classification synthesis** of which DAG
and lattice results survive scaling/refinement. It is **not** a
single retained theorem and **must not** be audited as one. The audit
ledger row for `continuum_bridge_note` classified this source as
conditional/bounded with auditor's repair target:

> missing_dependency_edge: add one-hop retained authorities or a
> primary cached runner for the DAG large-N and lattice h-refinement
> tables, then re-audit the narrowed survival/retraction claims.

The minimal-scope response in this PR is to **relabel** this document
as an overview/classification synthesis rather than to materialize
the missing one-hop authorities or cached runners here. Those steps
belong in dedicated review-loop or per-claim audit passes. Until
that work is done:

- This file makes **no** retained-claim assertions of its own.
- The "what survives" / "what weakens" / "what is a discrete-family
  artifact" classifications, lattice-continuum-limit tables, RG
  scaling readouts, distance-law refinement narrative, and
  retained/provisional/retracted summary tables below are
  **historical program memory only**.
- The retained-status surface for any DAG-survival or lattice-
  refinement claim is the audit ledger
  (`docs/audit/AUDIT_LEDGER.md`) plus the per-claim notes for each
  underlying gravity, Born, decoherence, mass-scaling, distance-law,
  and emergence sub-claim, **not** this synthesis.
- Retained-grade does **NOT** propagate from this synthesis note to
  any sub-claim, classification verdict, or successor runner.

### Per-claim pointers

The classification verdicts in this file map to dedicated per-claim
notes where the live status, if any, lives:

- **Phase-valley gravity (DAG + lattice)** — consult per-claim
  gravity notes (e.g. `GRAVITY_LAW_CLEANUP_NOTE.md`,
  `GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md`).
- **Born rule (linear path-sum chokepoint)** — consult per-claim
  Born notes.
- **CL-bath decoherence floor** — consult per-claim decoherence
  notes (e.g. `DECOHERENCE_DECISION_NOTE.md`).
- **Mass scaling (3D vs 4D)** — consult per-claim mass-scaling
  notes.
- **Lattice continuum limit (MI / decoherence / d_TV)** — consult
  per-claim lattice-refinement notes.
- **Distance-law (DAG vs lattice)** — consult per-claim distance-
  law notes for the current matched-width replay status.
- **Asymptotic emergence (gap dynamics)** — consult per-claim
  emergence / dense+prune notes.
- **Strict visibility gain (vanishing artifact)** — consult per-
  claim visibility-gain notes.

The live status of each sub-claim is whatever the audit-ledger row
for the corresponding linked note says today, not what this
synthesis records.

For any retained claim about continuum / scaling / refinement
survival, audit the corresponding dedicated note as a separate scoped
claim — not this overview synthesis.

## What survives size growth

### Gravity (phase valley deflection)

| Dimension | N range tested | Signal at large N | Verdict |
|---|---|---|---|
| 2D modular | N=25-40 | delta=+2.5 at N=40 | Survives |
| 3D modular gap=3 | N=20-100 | t=+2.98 at N=100 | **Survives (weakening)** |
| 4D modular gap=3 | N=20-40 | t=+9.32 at N=40 | Survives (limited range) |

**Scaling behavior:** Gravity signal weakens at large N but stays
positive and significant through the tested range. At N=100 in 3D
(t=2.98), the signal is still above 2 SE. The weakening is gradual,
not a sharp cutoff.

**Verdict: SURVIVES.** Gravity is not a finite-size artifact.

### Decoherence (CL bath purity)

| Dimension | Best pur_cl | N range | Large-N trend |
|---|---|---|---|
| 2D modular | 0.885 (N=30) | N=12-100 | Stable ~0.94 for N≥40 |
| 3D modular | 0.849 (N=40-100) | N=12-100 | Stable ~0.85 |
| 4D modular gap=3 | 0.890 (N=80) | N=40-100 | Stable ~0.92 |
| 4D modular gap=5 | 0.911 (N=40) | N=40-100 | Stable ~0.94 |

**Scaling behavior:** Decoherence stabilizes to a family-dependent
floor. It does NOT collapse to pur_cl=1 through the tested range
on any modular family. The 3D floor (~0.85) is lower than 2D (~0.94).

**Important caveat:** The strict single-vs-double-slit visibility
gain (V_gain) is effectively flat at large N (~+0.005 for N≥40 in 3D).
The purity metric retains signal but the strictest interference-based
metric does not.

**Verdict: PARTIALLY SURVIVES.** Purity-based decoherence is stable.
Strict visibility gain does not survive.

### Born rule

| Dimension | I_3/P | N tested | Verdict |
|---|---|---|---|
| 2D grid | 4.7e-16 | N=40 | Machine precision |
| 3D chokepoint | 3e-16 | N=20-40 | Machine precision |
| 4D chokepoint | ~1e-16 | N=15-25 | Machine precision |

**Verdict: SURVIVES.** Born rule is exact for linear path-sum with
chokepoint barriers, at all tested sizes. This is a mathematical
property of linear amplitude propagation, not a finite-size effect.

### Mass scaling

| Dimension | Alpha | Convergence | Verdict |
|---|---|---|---|
| 3D (d=2 spatial) | 0.58 | YES (spread 0.083) | **Converges** |
| 4D (d=3 spatial) | 0.35-1.64 | NO (spread > 0.3) | **Does not converge** |

**Verdict: PARTIALLY SURVIVES.** 3D mass scaling has a proper
continuum limit (alpha → 0.58). 4D does not — alpha remains
parameter-sensitive across tested densities.

## What weakens with size

### Distance scaling (b-dependence)

b-independent at all sizes, all dimensions, all graph families.
This is structural, not a finite-size artifact. Tested at densities
from 15 to 120 nodes/layer with no change.

**Verdict: STRUCTURAL LIMITATION.** Does not weaken because it
was never there.

### Emergence (self-regulating gap)

| Rule | Useful N window | Large-N fate |
|---|---|---|
| Fixed threshold (2D) | N=40 marginal | CLT kills at N=80 |
| Fixed threshold (3D) | N=50 | Over-prunes at N=60 |
| Adaptive quantile (3D uniform) | **N=80** | Fails at N=100 |
| Adaptive quantile (3D hierarchical) | **N=80** | delta=-0.023 |
| Imposed modular gap | N=80 (3D), N=100 (4D) | Stable in range |

**Updated verdict: PARTIALLY SURVIVES through N=80 (sparse base) and
N=120 (dense base npl=60).** The adaptive quantile rule sustains
decoherence improvement on uniform 3D DAGs. Dense+prune extends the
window to N=120 (delta=-0.015, all seeds valid). Gravity is preserved
under pruning (t=4.0 vs 3.3 unpruned).

Birth/death and amplitude-guided growth did not improve over pruning.
Slit-conditioned growth failed (measurement incompatible with grown
topology). Dense+prune is the strongest retained emergence result.

**Caveats from review:**
- The smart-prune vs adaptive-quantile comparison does not actually
  compare two distinct algorithms (both call the same function)
- Mass scaling claims on pruned graphs are retracted (mass-position
  confound confirmed)
- The hierarchical alpha=0.71 is exploratory (not fixed-position clean)

### Strict visibility gain

In 3D modular gap=3, the strict single-vs-double-slit visibility
gain averages +0.005 for N≥40 — effectively zero. The broader
detector-profile contrast stays high, but the strictest metric
doesn't survive size growth.

**Verdict: VANISHES.** Strict visibility gain is a finite-size
artifact on the retained family.

## What is a discrete-family artifact

### 4D mass exponent

The alpha=1.07 ("F~M") result at one density point (npl=25, gap=5)
does not survive density variation. Alpha ranges from 0.35 to 1.64
across tested densities at gap=5. The "Newtonian" claim was a
parameter-specific result, not a universal feature.

### Preferential attachment gravity

Gravity works on uniform, hierarchical, and modular DAGs but fails
on preferential-attachment DAGs at N≥20. The hub_boost threshold
(~2.0) is family-specific — it's a property of the connectivity
distribution, not the propagator.

## Summary table

| Property | Finite-size artifact? | Survives scaling? |
|---|---|---|
| Gravity (attraction) | No | Yes (weakening) |
| Born rule | No | Yes (exact) |
| CL bath purity floor | No | Yes (family-dependent) |
| Mass scaling (3D) | No | Yes (converges to 0.58) |
| Cross-family gravity | No | Yes (4/5 families) |
| Distance law (b-indep) | No | N/A (structural) |
| Strict visibility gain | **Yes** | **No (vanishes at large N)** |
| Mass scaling (4D) | **Partially** | **Doesn't converge** |
| Emergence (gap dynamics) | **Partially** | **Sustains to N=80, wall at N=100** |

## Lattice continuum limit (2026-04-04 update)

The lattice architecture provides a genuine h→0 refinement lane that the
random DAG architecture does not. This is a complementary exploratory lane,
not a replacement.

### Lattice results that survive refinement

| Property | 2D (1/L) | 3D (1/L^2) | 4D (1/L^3) |
|---|---|---|---|
| Born | < 6e-16 at all h | < 4e-15 at all h | 1.3e-15 |
| MI | → 0.95 at h=0.25 | → 0.66 at h=0.25 | 0.32 (h=1 only) |
| Decoherence | → 50% at h=0.25 | → 50% at h=0.25 | TBD |
| d_TV | → 0.99 at h=0.25 | → 0.83 at h=0.25 | 0.58 |
| Gravity (TOWARD) | Strengthens | Strengthens on the current branch | stronger persistence candidate than lower powers |
| Distance tail | b^(-1.08) at h=0.5 | post-peak tail is retained and b-dependent, but matched-width comparisons currently stay shallow rather than steepen toward `-2` | TBD |

The 3D column now also has a frozen `h=0.25` eight-property script-level card
on `main`; this is a trust-building conversion, not a closed theorem.

### Dimension-dependent kernel

The imported kernel branch currently suggests a stronger persistence rule:

- lower powers can look attractive on short lattices
- `p = d-1` is the strongest current empirical candidate for a kernel whose
  gravity signal persists more cleanly as lattice length grows

That is stronger than the earlier 2D-only picture, but weaker than a
selection theorem. In particular:

- the 4D evidence is still bounded
- the local transfer-norm probe on `main` does **not** uniquely single out
  `p = d-1`
- the transfer-norm story is still under reconciliation

### What the lattice changes about the distance law

The random DAG distance law was b-independent (structural limitation).
The lattice distance law is b-DEPENDENT, but the current 3D `1/L^2` read is
more honest and more limited than the earlier steepening narrative:
- there is a clean post-peak declining tail on the widened retained `h=0.25`
  probe
- the earlier cross-width “steepening toward `-2`” read was confounded by
  comparing different lattice widths and fit windows
- on the current matched-width replay, the 3D tail is still non-Newtonian and
  currently looks shallower rather than steeper under refinement

This does NOT rescue the random DAG distance law. It provides an
alternative architecture where distance law works.

### Architecture-dependent kernel (important caveat)

The dimension-dependent kernel is LATTICE-SPECIFIC:
- On random DAGs, all kernel powers give similar noisy gravity
- On mirror DAGs, 1/L outperforms 1/L^2
- The kernel selection mechanism (transfer norm marginality) requires
  the regular lattice structure with h→0 limit

### RG scaling

At fixed field strength s=5e-5, gravity magnitude diverges as h^(-0.48).
RG scaling s ~ h^0.92 stabilizes the magnitude. The distance exponent
is independent of s — it is a geometric lattice property.

## What this means for the model

The retained results are:
1. Phase-valley gravity (survives on DAGs AND lattices)
2. Born rule (exact, mathematical, all architectures)
3. CL bath decoherence floor (stable on DAGs, converges on lattice)
4. 3D mass scaling continuum limit (alpha → 0.58 on DAGs)
5. Cross-family robustness (4 of 5 DAG families)
6. **NEW: Distance law on lattice** (current exploratory 3D branch has a
   real post-peak declining tail, but the stronger “steepens toward `-2`”
   wording is now retracted)
7. **NEW: Lattice continuum limit** (MI, decoherence, d_TV all converge)

The provisional/retracted results are:
1. 4D "F~M" mass scaling on DAGs (parameter-sensitive)
2. Strict visibility gain (vanishes at large N)
3. Asymptotic emergence (N=80 on 3D, wall at N=100)
4. **RETRACTED: 3D 1/L gravity** (lattice artifact at h=1.0)

The structural limitations are:
1. Distance law on random DAGs (b-independent, structural)
2. CLT convergence on random DAGs (defeats all emergence rules)
3. Dimension-dependent kernel not derived from axioms (empirical and still
   under transfer-norm reconciliation)
