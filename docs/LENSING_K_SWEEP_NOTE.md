# Lensing Slope vs k (Phase Coupling): k-Dependent (Conditional Diagnostic)

**Date:** 2026-04-09 (status line narrowed 2026-04-28 per audit-lane verdict)
**Status:** bounded conditional diagnostic — the lensing slope oscillates between +0.58 and −1.43 across `k·H ∈ {0.5, ..., 5.0}` on a single Fam1 setup with three seeds per `k·H` value. The k-sweep runner/cache are named in the artifact chain; the wave-interference-mechanism inference is still stronger than the k-sweep table alone supports without registered kernel/mode analysis. Not a tier-ratifiable framework theorem.

## Setup

- Fam1 grown DAG, H=0.25, 3 seeds per k·H value
- 3 DAGs pre-grown, reused across all k values
- b ∈ {3, 4, 5, 6}, 8 k·H values from 0.5 to 5.0

## Result

| k·H | k | Mean slope | σ | R² range | kubo(b=3) | Notes |
| ---: | ---: | ---: | ---: | --- | ---: | --- |
| 0.5 | 2.0 | **+0.58** | 0.02 | 0.29–0.32 | +4.49 | **Sign flip — repulsive** |
| 1.0 | 4.0 | **−1.42** | 0.01 | 0.92–0.94 | +9.40 | Peak attraction |
| 1.5 | 6.0 | −1.17 | 0.03 | 0.98–0.99 | +5.12 | Shallower |
| 2.0 | 8.0 | −1.25 | 0.05 | 0.99 | +5.39 | Near eikonal |
| 2.5 | 10.0 | **−1.39** | 0.03 | >0.997 | +5.70 | Previous "invariant" |
| 3.0 | 12.0 | −1.15 | 0.10 | 0.99 | +5.32 | Shallower again |
| 4.0 | 16.0 | −1.43 | 0.48 | 0.11–0.99 | +0.99 | Very noisy |
| 5.0 | 20.0 | N/A | — | — | −7.9 | **All repulsive** |

Total slope range: **2.02** (from +0.58 to −1.43). Strongly k-dependent.

## Key findings

### 1. The slope oscillates with k

The slope is not monotone in k — it bounces between steep (−1.42) and shallow (−1.15) with a period of roughly Δ(k·H) ≈ 1.5. This is the signature of **partial-wave interference**: different k values excite different transverse modes of the lattice, and those modes interfere constructively or destructively with the 1/r potential's Fourier components.

### 2. Sign flip at low and high k

At k·H = 0.5 (low coupling), ALL three seeds give positive slopes — the beam deflects AWAY from the mass. At k·H = 5.0 (high coupling), all kubos are negative (also repulsive, but in a different sense — the kubo is negative meaning the centroid moves opposite to the expected direction). Only the intermediate range k·H ∈ {1.0, ..., 4.0} gives attractive deflection with clean power-law fits.

### 3. The −1.40 is not fundamental

The slope −1.40 at k·H = 2.5 was treated as a phenomenological invariant in earlier notes. This sweep shows it is one point on an oscillatory curve. The slope at k·H = 1.0 is −1.42 (equally good R², tighter σ), and at k·H = 1.5 is −1.17. There is no reason to privilege k·H = 2.5 over k·H = 1.0 except that it's the configuration the model has been using.

### 4. The eikonal gap oscillates

The eikonal predicts slope −1.275 (k-independent). The gap to the lattice oscillates:

| k·H | Gap |
| ---: | ---: |
| 0.5 | +1.86 (wrong sign entirely) |
| 1.0 | −0.14 |
| 1.5 | +0.11 |
| 2.0 | +0.03 |
| 2.5 | −0.12 |
| 3.0 | +0.12 |

The gap changes sign with period ~1.5 in k·H. At k·H = 2.0, the eikonal is nearly exact (gap = 0.03). At k·H = 1.0 and 2.5, the lattice is steeper than the eikonal. At k·H = 1.5 and 3.0, it's shallower. This is a classic interference oscillation.

## Implications

### For the "combined lensing invariant"

The invariant kubo(b) ≈ 29·b^(−1.40) is **configuration-specific**, not a structural prediction. It holds only at k·H = 2.5. At other k values, the slope is different. The earlier notes should be read as "at the reference configuration k·H=2.5, the slope is −1.40" — not as a property of the propagator.

### For the eikonal comparison

The eikonal (−1.275) is the k-independent geometric baseline. The wave correction oscillates around it. At some k values (k·H ≈ 2.0) the lattice matches the eikonal perfectly. At others it deviates by up to ±0.15. The earlier "eikonal gap" of 0.13 was the oscillation amplitude at k·H = 2.5, not a fixed correction.

### For the mechanism

The k-dependence confirms the deflection is a **wave-interference phenomenon**, not a geometric-optics effect. The oscillation period Δ(k·H) ≈ 1.5 corresponds to a phase shift of ~1.5 rad per edge, which is roughly π/2 — the half-cycle of a standing-wave pattern. This suggests the deflection arises from interference between paths that differ by ~π/2 in accumulated phase at the potential.

### For the project

The honest characterization is:

> "The propagator produces k-dependent gravitational deflection that
> oscillates between attractive and repulsive with period Δ(k·H) ≈ 1.5.
> At the reference configuration k·H=2.5, the slope is −1.40. This is
> a wave-interference effect, not a geometric invariant."

## Artifact chain

- [`scripts/lensing_k_sweep.py`](../scripts/lensing_k_sweep.py)
- [`logs/runner-cache/lensing_k_sweep.txt`](../logs/runner-cache/lensing_k_sweep.txt)
  (SHA-pinned audit-lane cache; see `docs/audit/RUNNER_CACHE_POLICY.md`)

## Bottom line

> "The lensing slope oscillates between +0.58 and −1.43 across k·H ∈
> {0.5..5.0} with period ~1.5. At k·H=0.5 deflection is repulsive;
> at k·H=5.0 all seeds are repulsive. The −1.40 at k·H=2.5 is one
> point on this oscillatory curve, not a fundamental constant. The
> eikonal gap oscillates in sign, confirming the correction is wave-
> interference, not geometric. The propagator's gravitational response
> is a k-dependent interference phenomenon."

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, high criticality, 124 transitive
descendants):

> Issue: the previous diagnostic rests on a numerical k-sweep
> over one Fam1 setup with three seeds per k*H value, but the audit
> ledger registers no primary runner/output for
> `scripts/lensing_k_sweep.py` or its log. Why this blocks: a hostile
> auditor cannot reproduce the reported slope range, sign flips, R^2
> ranges, seed spread, or eikonal-gap oscillation from registered
> evidence; additionally, the inference that the correction is a
> wave-interference mechanism is stronger than the table alone unless
> supported by registered kernel/mode analysis.

## What this note does NOT claim

- A framework-level theorem about lensing-slope k-dependence beyond
  the single Fam1 sweep.
- That the wave-interference mechanism interpretation is supported by
  registered kernel / mode analysis; only the slope table is
  reported.
- That the fixed artifact pointer by itself supplies registered kernel /
  mode analysis or closes the lane.

## What would close this lane (Path A future work)

A future stronger status would require:

1. Registering `scripts/lensing_k_sweep.py` and its deterministic
   output as the primary runner with PASS thresholds for slopes,
   signs, and seed spread.
2. Registering the eikonal baseline and adjoint-kernel / mode
   analysis used to infer the wave-interference mechanism.
3. Extending or explicitly bounding the family / seed coverage.
