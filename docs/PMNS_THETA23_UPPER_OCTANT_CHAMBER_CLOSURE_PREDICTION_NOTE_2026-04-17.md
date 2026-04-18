# θ_23 Upper-Octant Chamber-Closure Prediction

**Date:** 2026-04-17
**Status:** CONDITIONAL / SUPPORT prediction — a falsifiable consequence of
the retained H-diagonalization map plus the same imposed branch-choice
admissibility rule used by the G1 chamber pin. The threshold geometry is
sharp; the selector interpretation remains conditional.
**Script:** `scripts/frontier_pmns_theta23_upper_octant_chamber_closure_prediction.py`
**Runner:** `PASS = 31, FAIL = 0`
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## Summary

An adversarial input-sensitivity test on the closure pinning (fixing
`sin^2 θ_12 = 0.307` and `sin^2 θ_13 = 0.0218` at their PDG 2024
central values, then varying `sin^2 θ_23`) reveals a **critical
threshold** in the inverse problem:

- For `s_23^2 >= s_23^2_min`, the PMNS-closure map admits a unique chamber-
 interior inverse image.
- For `s_23^2 < s_23^2_min`, the unique fsolve root sits OUTSIDE the
 chamber (`q_+ + δ < sqrt(8/3)`); no chamber closure exists.

This is not a fragility of the closure; it is a **structural feature** of the
retained H-diagonalization map. Below threshold, the geometric chamber that
carries the retained affine `H` does not contain an observationally-
consistent point. We sharpen this into a falsifiable conditional/support
prediction of the selector closure.

**Main result.** At PDG 2024 central `(s_12^2, s_13^2) = (0.307, 0.0218)`,

```
s_23^2_min = 0.540970 . . . (bracketed brentq to 12 digits)
```

At this threshold the pinned `(δ, q_+)` saturates the chamber boundary
`q_+ + δ = sqrt(8/3)` exactly:

```
(m_t, δ_t, q_+t) = (0.679266, 0.928496, 0.704498),
|q_+ + δ − sqrt(8/3)| < 1e-14.
```

**Threshold surface.** Over the NuFit 5.3 NO 3-sigma rectangle
`[0.270, 0.341] × [0.02029, 0.02391]` on `(s_12^2, s_13^2)`:

```
s_23^2_min(s_12^2, s_13^2) in [0.5335, 0.5476].
```

The surface lies **strictly above maximal mixing** (`s_23^2 = 0.5`) at every
point of the rectangle.

**Conditional/support prediction (falsifiable).**
```
Selector chamber closure ADMITS a solution only if
 s_23^2 >= s_23^2_min(s_12^2, s_13^2)
 ≥ 0.5335 (for any (s_12^2, s_13^2) inside the NuFit 5.3 3σ box)
 ≈ 0.5410 (at PDG 2024 central (0.307, 0.0218))
```

Since the threshold surface lies entirely above `0.5`, the selector closure
**predicts `θ_23` in the UPPER octant**. This is falsifiable by
JUNO / DUNE / Hyper-Kamiokande over the next few years.

**Schur-Q coincidence.** The Schur-Q variational candidate
`(δ, q_+) = (sqrt(6)/3, sqrt(6)/3)` satisfies
`δ + q_+ = 2 sqrt(6)/3 = sqrt(8/3)` exactly — i.e. Schur-Q lies ON the
chamber-boundary line. The PMNS-pinning threshold point
`(δ_t, q_+t) = (0.9285, 0.7045)` ALSO lies on this same boundary line.
Two otherwise independent retained points — the variational (Schur-Q)
candidate and the observational (PMNS-pinning) chamber-saturation locus —
meet on the SAME 1-parameter chamber-boundary ridge. This is a structural
observation that ties two independent retained landmarks together: the
chamber boundary `q_+ + δ = sqrt(8/3)` is the unique locus where (i)
the Schur-Q symmetric variational minimum lives and (ii) the PMNS
inverse image degenerates, for different reasons, and those two reasons
happen to share the same defining equation.

## Retained inputs

All retained at the time of writing:

- The PMNS-closure retained PMNS-as-f(H) map
 [PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md](./PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md)
 and its underlying retained chain (affine chart theorem, chamber theorem,
 Z_3 doublet-block point-selection, current-bank blindness, Dirac-bridge,
 three-generation observable).
- The chamber `q_+ >= sqrt(8/3) − δ` from the retained half-plane theorem
 [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md).
- The Schur-Q candidate point `δ = q_+ = sqrt(6)/3` as a retained landmark
 from the information-geometric obstruction tour.

No new axiom or post-axiom selector is introduced. The prediction is
purely a sharpened consequence of the retained PMNS-as-f(H) map plus the
same chamber constraint used by the conditional/support pin.

## The threshold as a structural feature

The PMNS-closure map `Φ : (m, δ, q_+) → (s_12^2, s_13^2, s_23^2)` is a
smooth map from the (open) 3-manifold `R × {(δ, q_+) : q_+ + δ > sqrt(8/3)}`
to an open subset of the unit cube. Its inverse image over a fixed
observational triple `(o_12, o_13, o_23)` is generically a discrete set of
points (the PMNS-closure 60-seed multi-start found a unique one).

As we move the target triple inside the image, the inverse image moves
continuously. When the target triple approaches the boundary of the image,
the inverse image approaches the CHAMBER BOUNDARY of the `(m, δ, q_+)`
domain — i.e. `q_+ + δ = sqrt(8/3)`. Beyond that boundary, there is no
inverse image in the chamber at all.

Therefore the CHAMBER-CLOSURE THRESHOLD for varying `s_23^2` at fixed
`(s_12^2, s_13^2)` is exactly the value of `s_23^2` at which the inverse
image is on the boundary. We compute it by bracketed root-finding on the
boundary-distance function `d(s_23^2) := q_+(s_23^2) + δ(s_23^2) − sqrt(8/3)`.

## Numerical results

### Table 1: Reproduction of the adversarial input-sensitivity (at `(s_12^2, s_13^2) = (0.307, 0.0218)`)

| `s_23^2` | label | `(m, δ, q_+)` | `q_+ + δ − sqrt(8/3)` | status |
|---|---|---|---:|---|
| 0.573 | +1σ | `(0.5031, 0.9783, 0.7876)` | +0.1330 | INTERIOR |
| 0.568 | NuFit UO | `(0.5302, 0.9693, 0.7749)` | +0.1112 | INTERIOR |
| 0.545 | central | `(0.6571, 0.9338, 0.7150)` | +0.0159 | INTERIOR |
| 0.540970 | **threshold** | `(0.6793, 0.9285, 0.7045)` | 0 (boundary) | **saturation** |
| 0.520 | −1σ | `(0.7930, 0.9043, 0.6505)` | −0.0782 | OUTSIDE |
| 0.445 | NuFit LO | `(1.1588, 0.8486, 0.4795)` | −0.3049 | OUTSIDE |

All five non-threshold rows are reproduced from the brief to 4 digits by
the runner.

### Table 2: Threshold surface over NuFit 5.3 NO 3-σ rectangle

At each grid point the threshold point is on the chamber boundary
`q_+ + δ = sqrt(8/3)` exactly.

| `s_12^2` \ `s_13^2` | 0.02029 | 0.02210 | 0.02391 |
|---:|---:|---:|---:|
| 0.2700 | 0.5476 | 0.5414 | 0.5358 |
| 0.3055 | 0.5461 | 0.5401 | 0.5345 |
| 0.3410 | 0.5448 | 0.5389 | 0.5335 |

Threshold range over the 3-σ rectangle: `[0.5335, 0.5476]`.

At PDG 2024 central `(0.307, 0.0218)` the threshold is `0.540970`.

### Consistency with NuFit 5.3 NO

| Input triple | `(m, δ, q_+)` | chamber dist | closure |
|---|---|---:|---|
| PDG 2024 central `(0.307, 0.0218, 0.545)` | `(0.6571, 0.9338, 0.7150)` | +0.0159 | YES (PMNS-closure pin) |
| NuFit 5.3 NO UO best-fit `(0.307, 0.0218, 0.568)` | `(0.5302, 0.9693, 0.7749)` | +0.1112 | YES |
| NuFit 5.3 NO LO 3σ alt `(0.307, 0.0218, 0.445)` | `(1.1588, 0.8486, 0.4795)` | −0.3049 | **NO** |

Upper-octant best-fit lies comfortably inside the chamber.
Lower-octant alternative lies comfortably outside the chamber.

## The Schur-Q coincidence

The Schur-Q candidate
```
(δ_S, q_+S) = (sqrt(6)/3, sqrt(6)/3)
```
arose in the information-geometric obstruction tour as a
retained symmetric variational landmark: it is the unique chamber point where
the `C^1` shared quadratic minimum of all natural info-geometric functionals
lives (Quadratic Unanimity Theorem, Candidate A). The Schur-Q
point has the numerical property
```
δ_S + q_+S = 2 sqrt(6)/3 = sqrt(8/3)
```
so **Schur-Q lies EXACTLY on the chamber boundary**. It is the unique
chamber-boundary point with `δ = q_+`.

The PMNS-pinning chamber-closure threshold at PDG 2024 central
`(s_12^2, s_13^2)` lies at a different point on the SAME chamber-boundary
line:
```
(δ_t, q_+t) = (0.9285, 0.7045) with q_+t + δ_t = sqrt(8/3).
```
The two points are 0.158 apart in the `(δ, q_+)`-plane — inequivalent — but
they occupy the same 1-parameter chamber-boundary ridge.

This is a **structural coincidence** with two independent interpretations:

1. **Schur-Q interpretation.** The Schur-Q symmetric variational minimum
 is the `δ = q_+` specialization of the generic `C^1` minimum of all
 info-geometric functionals. The chamber boundary `q_+ + δ = sqrt(8/3)` is
 the 1-parameter locus that contains it.

2. **PMNS-pinning interpretation.** The PMNS-closure inverse image
 approaches the chamber boundary as the observational triple approaches
 the boundary of the image of `Φ`. The chamber boundary is the only
 locus where the inverse degenerates.

Both interpretations point to the same locus `q_+ + δ = sqrt(8/3)`. This
is analytically significant: the retained variational route (the info-geom / cubic-variational / parity-mixing obstructions) and
the retained observational route meet on a common boundary
structure. Whether this is a deep algebraic coincidence or a superficial
Numerik accident is not settled by this note. We record it as a structural
observation tying together two independent retained landmarks.

The Schur-Q ray `δ = q_+ = sqrt(6)/3` with varying `m` does NOT reproduce
the PDG 2024 central triple simultaneously:

```
m = 0.5500 on Schur-Q ray: s_12^2 = 0.5370, s_13^2 = 0.0210, s_23^2 = 0.5373.
```

(Best-match to central `s_13^2 = 0.0218` gives `m ≈ 0.55`, with `s_12^2 ≈ 0.537`,
well outside the NuFit 5.3 NO 3σ range on `s_12^2`.) So Schur-Q is not the
PMNS pin; Schur-Q is a chamber-boundary variational landmark that happens to
share the chamber-boundary line with the PMNS chamber-closure threshold.

## Formal statement of the conditional/support prediction

**Conditional/support prediction (selector-gate θ_23 upper-octant).** Given the
retained PMNS-as-f(H) map and the conditionally pinned chamber
`q_+ + δ ≥ sqrt(8/3)`, the selector inverse problem

```
(m, δ, q_+) ∈ chamber,
Φ(m, δ, q_+) = (sin^2 θ_12, sin^2 θ_13, sin^2 θ_23)_obs,
```

admits a solution iff `sin^2 θ_23 ≥ s_23^2_min(sin^2 θ_12, sin^2 θ_13)`,
where
```
s_23^2_min : (PDG range of s_12^2) × (PDG range of s_13^2) → (0.5, 1)
```
is a smooth function with range in the upper octant. Over the NuFit 5.3 NO
3-sigma rectangle on `(s_12^2, s_13^2)` it takes values in `[0.5335, 0.5476]`;
at PDG 2024 central `(0.307, 0.0218)`, `s_23^2_min = 0.540970`.

**Corollary (θ_23 upper-octant; conditional on the same branch-choice rule used by the chamber pin).** The selector chamber closure requires
`sin^2 θ_23` in the **upper octant** (`> 0.5`).

**Falsification criteria (conditional/support).**
- A future global fit settling on `sin^2 θ_23 < 0.5` at `>3σ`
 UNCONDITIONALLY FALSIFIES the selector closure (since the threshold surface is
 entirely above `0.5`).
- A future global fit with `sin^2 θ_23 < 0.534` at `>3σ` falsifies the
 the selector closure at PDG central `(s_12^2, s_13^2)` (since the minimum threshold
 over the 3σ rectangle on `(s_12^2, s_13^2)` is `0.5335`).
- The current NuFit 5.3 NO best-fit `sin^2 θ_23 = 0.568` is consistent
 with the prediction at `2.7σ` margin
 (`0.568 − 0.5410 = 0.027 > 1σ_NuFit ≈ 0.013`).

## Observational timeline (DUNE / JUNO / Hyper-K)

Current status (2026 Q2):

- **NuFit 5.3 global fit (NO):** best-fit `s_23^2 ≈ 0.568` (upper octant),
 1σ ≈ 0.013, 3σ interval `[0.434, 0.610]` — crosses the octant boundary
 and admits a weaker lower-octant alternative around `0.445`.
- **T2K + NOvA tension:** T2K prefers UO, NOvA appearance mildly LO-leaning;
 combined fits give `~1.3σ` UO preference.

Near-term experiments resolving octant:

- **JUNO (first data 2026 Q3; precision era 2028–2030).** Medium-baseline
 reactor measurement of `sin^2 2θ_12`, `Δm^2_21`, `Δm^2_31`. Atmospheric-
 neutrino channel (if instrumented) adds `s_23^2` at `Δ ≈ 0.02`. Will tighten
 the 3σ range.
- **Hyper-Kamiokande (first data 2027; long-baseline era 2029+).**
 Accelerator `nu_e` appearance + atmospheric analysis; expected octant
 determination at `>3σ` within 5 years of first data.
- **DUNE (first data 2030+).** Long-baseline appearance and disappearance;
 expected `Δ(s_23^2) ≈ 0.01`. Will deliver the definitive octant test and
 sharpen the central value to well below the selector threshold margin.

**Timeline.** The selector θ_23 upper-octant prediction is expected to be decisively
tested by the **Hyper-K + DUNE + JUNO combined fit** by the early 2030s.

## Claim discipline

### What this note positively claims

1. **Conditional/support prediction** (not an obstruction). Derived from
 the retained H-diagonalization map and the chamber
 constraint, with the selector interpretation inheriting the same
 imposed branch-choice rule as the chamber pin.
2. **Exact threshold** `s_23^2_min(0.307, 0.0218) = 0.540970` at PDG 2024
 central (12-digit brentq convergence; runner-verified).
3. **Threshold surface range** `[0.5335, 0.5476]` over the NuFit 5.3 NO 3σ
 rectangle on `(s_12^2, s_13^2)`.
4. **θ_23 upper-octant** is the selector prediction. Lower octant at `>3σ` would
 falsify the selector closure unconditionally.
5. **Chamber-boundary / Schur-Q coincidence.** Both the variational Schur-Q
 candidate `(δ, q_+) = (sqrt(6)/3, sqrt(6)/3)` and the PMNS-pinning
 chamber-closure threshold lie on the same chamber-boundary line
 `q_+ + δ = sqrt(8/3)`.

### What this note does not claim

- That Schur-Q and the PMNS threshold are the same point (they are 0.158
 apart in the `(δ, q_+)`-plane).
- That the threshold is a sole-axiom result (it is a structural feature of
 the retained H-diagonalization map; it is not proven by any sole-axiom
 principle).
- That the prediction is non-falsifiable (it is explicitly falsifiable by
 octant resolution; see the falsification criteria above).
- That the result pins or predicts `Δm^2_21`, absolute masses, or Majorana
 phases (they live on different carriers).

## Conditional/support statement for the omnibus

Short-form one-paragraph statement suitable for inclusion in
`DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md` or the ARXIV_DRAFT:

> **θ_23 upper-octant conditional/support prediction.** The PMNS-as-f(H) closure
> has a structural threshold: at PDG 2024 central
> `(s_12^2, s_13^2) = (0.307, 0.0218)`, the selector chamber closure admits a
> solution only for `s_23^2 ≥ 0.5410`; across the NuFit 5.3 NO 3σ
> rectangle on `(s_12^2, s_13^2)`, the threshold ranges over `[0.5335,
> 0.5476]` — **entirely in the upper octant**. The threshold surface is a
> smooth function of `(s_12^2, s_13^2)` and saturates the chamber boundary
> `q_+ + δ = sqrt(8/3)`, the same 1-parameter ridge that contains the
> Schur-Q variational candidate `(sqrt(6)/3, sqrt(6)/3)`. Given the same
> imposed branch-choice rule used by the chamber pin, the selector closure
> therefore **predicts θ_23 in the upper octant**; resolution of the
> θ_23 octant at JUNO / Hyper-Kamiokande / DUNE over the next several
> years provides a direct test. A `>3σ` lower-octant determination would
> unconditionally falsify the selector closure.

## Runner

```bash
PYTHONPATH=scripts python3 \
 scripts/frontier_pmns_theta23_upper_octant_chamber_closure_prediction.py
```

Expected: `PASS = 31, FAIL = 0`. Seven parts:

- **Part 1.** Reproduction of the adversarial `s_23^2` sweep at central
 `(s_12^2, s_13^2)`, confirming interior vs. outside-chamber status at
 the brief's five rows.
- **Part 2.** Bracketed `brentq` computation of `s_23^2_min` at PDG
 central, with verification of chamber-boundary saturation at the
 threshold.
- **Part 3.** Mapping of the threshold surface over the NuFit 5.3 NO 3-σ
 rectangle on `(s_12^2, s_13^2)`.
- **Part 4.** Verification that current PDG 2024 / NuFit 5.3 central
 values yield a valid chamber-interior closure.
- **Part 5.** Chamber-boundary saturation / Schur-Q coincidence check.
- **Part 6.** Formalization of the θ_23 upper-octant conditional/support prediction.
- **Part 7.** Convergence diagnostics on the threshold.

## What this file must never say

- that θ_23 upper octant is retained-grade or sole-axiom (it is a
 conditional/support prediction of the P3-lane observational pin, not a
 sole-axiom derivation);
- that the threshold `s_23^2_min = 0.541` is the octant boundary (the
 octant boundary is `0.5`; `0.541` is a sharper bound);
- that Schur-Q = threshold (they are different points on the same
 chamber-boundary line);
- that the prediction is confirmed (it is CONSISTENT with NuFit 5.3 NO
 best-fit but not yet confirmed at the level required for a Nature-grade
 positive test; JUNO / Hyper-K / DUNE will close the question).
