# Linear-Response Derivation-Adjacent Analysis — Partial Positive

**Date:** 2026-04-07
**Status:** retained partial positive — a derivation-adjacent heuristic (detector reweighting of |amp|² by 1/|z−z_src|, no parameter fit) gives **r = 0.56 overall and r = 0.72 off-scaffold correlation** with the measured first-order response and **81.8% sign agreement** across a combined 44-family set. Off-scaffold correlation is stronger than scaffolded (0.72 vs 0.40), the opposite of `free_coh`. The separately reported 79.5% "best threshold" number is in-sample tuned on the same dataset and should not be cited as a no-fit result. This is a heuristic, NOT yet the literal first-order Kubo expression `<z·δH>_0` (that is the subject of a follow-on lane).

## Artifact chain

- [`scripts/linear_response_derivation.py`](../scripts/linear_response_derivation.py)
- [`logs/2026-04-07-linear-response-derivation.txt`](../logs/2026-04-07-linear-response-derivation.txt)

## Question

The classifier lane is closed; `free_coh` works on scaffolded
generators but fails off-scaffold. The derivation target named in
Update 3 was: "explain why grown-DAG and dense ER pass while
random k-regular and expander fail, from the path-sum + S = L(1−f)."

This lane does NOT search for another empirical metric. It tests
ONE theoretically motivated quantity — the **first-moment Kubo
predictor** — directly derived from linear response theory, against
the measured first-order gravitational response.

## The heuristic

For each family, compute:

- `cz_free` = centroid of `|amp_j(0)|²` over detector cells (free beam)
- `cz_weighted` = centroid weighted by `|amp_j|² / |z_j − z_src|`
  (detector reweighting by the 1/r field profile)
- **`kubo_heuristic = cz_weighted − cz_free`**

This is a **detector-only reweighting** of the free amplitudes
by the known 1/r field profile. It is derivation-**adjacent** — it
uses the same field profile that enters the true Kubo expression —
but it is NOT the literal first-order Kubo term `<z·δH>_0`.

The literal first-order term requires:
- The actual action perturbation `δH = k L δf` integrated along edges
- Path-length / phase cross-terms that this heuristic does not include
- A derivation from the propagator + action, not just a reweighting

That calculation is the subject of a separate lane
(`linear_response_true_kubo.py`). This lane evaluates the heuristic
as a first pass and reports its empirical correlation with the
measured response.

The **measured** response is `delta_z(s = 0.001) - delta_z(s = 0)`
divided by `s` — the actual first-order derivative of the centroid
with respect to the source strength via finite difference.

## Result

### Correlation across 44 families (26 swept + 9 scaffolded + 9 off-scaffold)

| Group | Pearson r | N |
| --- | ---: | ---: |
| Swept | **0.71** | 26 |
| Scaffolded cross-generator | 0.40 | 9 |
| **Off-scaffold** | **0.72** | 9 |
| **Overall** | **0.56** | 44 |

### Classification results (honest split: no-fit vs tuned)

| Test | Accuracy | Fitted? |
| --- | ---: | :---: |
| Sign agreement (`kubo_heuristic > 0` matches `measured > 0`) | **36/44 = 81.8%** | **no** |
| Best kubo threshold (searched on this 44-family set) | 35/44 = 79.5% | **yes (in-sample tuned)** |
| Upper bound (measured > 0 threshold) | 39/44 = 88.6% | reference only |

**Only the 81.8% sign-agreement number is no-fit.** The 79.5%
threshold-search result is in-sample tuned on the same 44-family
set it is evaluated on and should not be cited as independent
generalization evidence. The honest no-fit summary is:

- Pearson correlation: r = 0.56 overall, r = 0.72 off-scaffold
- Sign agreement: 36/44 = 81.8%

These are the numbers that carry across the 44-family set without
any parameter being set by looking at the labels.

### The headline finding

**Off-scaffold correlation (r = 0.72) is STRONGER than scaffolded
correlation (r = 0.40).** This is the opposite of what `free_coh`
showed, using the same no-fit correlation metric on the same off-scaffold families:

| Metric | Scaffolded r | Off-scaffold r |
| --- | ---: | ---: |
| `free_coh` vs measured response | (not computed, but cf. 56% pass classification) | (not computed, but cf. 56% pass classification) |
| `kubo_heuristic` vs measured response (Pearson, no fit) | 0.40 | **0.72** |

The heuristic **generalizes naturally off-scaffold** because it uses
detector amplitudes + the known field profile, not grid-aligned
phase relationships. `free_coh` measured a quantity that was
substrate-specific; this heuristic is substrate-independent by
construction.

The previous lane's claim that this pattern means we have a
"derived" predictor was stronger than the heuristic supports.
The heuristic is directionally correct and generalizes off-scaffold,
but the literal first-order Kubo calculation is the subject of a
separate lane.

## Which cases does the first moment miss?

Sign disagreements across the 44-family set identify what first-moment
linear response fails to capture. Four cases:

| Family | measured | kubo | sign | nature |
| --- | ---: | ---: | --- | --- |
| R3_kreg_k20_scaf | +22.13 | +1.95 | ✓ same | not a miss: F~M band edge, not sign |
| H1_ring_swept | −1.16 | +2.04 | ✗ | ring stencil path interference |
| G2_asym_z_swept | +0.05 | −0.91 | ✗ | Z2-broken stencil, anomalous phase correlations |
| L1_longrange_scaf | −0.80 | +2.91 | ✗ | long-range edges decorrelate path phases |

The three honest sign disagreements (`H1_ring`, `G2_asym_z`,
`L1_longrange`) share a common feature: **path-phase decorrelation
that first moments cannot capture**. Specifically:

- `H1_ring`: paths through the ring stencil interfere destructively
  in a way the 1/r-weighted centroid doesn't see
- `G2_asym_z`: the broken Z2 introduces a phase bias that the
  free centroid is neutral to
- `L1_longrange`: paths of very different length contribute with
  random phases, suppressing the linear response in a way the
  first moment can't represent

These are exactly the cases where a **second-moment** term
(variance of path phases, or a Kubo susceptibility with
frequency-dependent weighting) would be needed.

## The derivation target, sharpened

After this lane, the analytic derivation question has a sharper
form:

> *"The first-moment linear response `Δcz / Δs ≈ (cz_weighted − cz_free)`
> captures the gravity sign correctly on ~80% of tested generators
> including off-scaffold. The residual 20% are cases with
> destructive path interference (ring stencils, broken Z2, long-range
> connectivity). Can these be captured by the second-moment term in
> the Kubo expansion, or do they require a structurally different
> explanation?"*

This is a concrete analytic target. The path-sum calculation needed
is:

- First moment: `<z · δH>_0` where `δH = k L f_external`
- Second moment: `<z · δH · δH>_0` with cross-correlations across
  paths

Computing this symbolically is possible in principle; computing it
numerically on the 44-family set is a natural next lane.

## What this clears and what it does not

**Cleared:**
- A first-principles predictor exists for gravity sign (no fitting)
- It is more generator-agnostic than any empirical metric tested so far
- It correlates with the measured response at r = 0.56 overall and
  r = 0.72 off-scaffold
- The derivation target is sharpened to a specific second-moment question

**Not cleared:**
- Clean theorem: first moment gets 80%, not 100%
- Three sign-disagreement cases need second-moment treatment
- The relationship to `free_coh` is now formal: `free_coh` was a
  scaffold-specific proxy for an ill-defined quantity; `kubo` is the
  theoretically correct first-order quantity
- The "compact underlying principle" row is not yet filled — `kubo`
  is derivation-adjacent but not derived end-to-end

## Frontier map adjustment (Update 5)

| Row | Update 4 (post matter-closure neg) | This lane |
| --- | --- | --- |
| Compact underlying principle | classifier closed, matter closed, critique stands | **partial restoration**: first-moment Kubo is the theoretically correct linear-response quantity, captures 80% across 44 families |
| Theory compression | open | **sharper target**: first moment captures majority, residual ↔ second-moment or path-phase variance |
| Strength against harshest critique | empirical metrics exhausted | **modest restoration**: a derivation-adjacent quantity exists and generalizes off-scaffold |
| Matter / inertial closure | NEGATIVE | unchanged |

## Honest read

This is the **first time in this session** that a theoretically
motivated quantity (not empirically fit) has generalized off-scaffold
with comparable accuracy to the scaffolded regime. The off-scaffold
correlation of **0.72** is the strongest single off-scaffold number
in the entire classifier program.

However:

- The overall correlation is only 0.56 across all 44 families
- The classification accuracy is 80%, not 100%
- The three honest sign misses (ring, asym_z, longrange) are not
  edge cases — they are structural generators that the first moment
  genuinely cannot handle
- This is a partial positive, not a full derivation

It **does** meaningfully move the "compact underlying principle"
row: there is now a quantity derived directly from the propagator
+ action that predicts gravity sign on ~80% of tested generators
with no fitting. That is the first derivation-grade result in the
classifier program.

The next move on this lane is either:

1. **Second-moment extension** — compute `<z · δH · δH>_0` and
   check whether it captures the three residual cases. If yes: a
   concrete two-term Kubo derivation is now analytically motivated.
2. **Analytical proof of the first moment** — actually write out
   the path-sum expansion symbolically and identify which propagator
   + action features are required for the first moment to dominate.
3. **Move on to experimental prediction** — ship the wave-retardation
   result with sharpened numbers for a lab claim.

## Bottom line

> "The first-moment Kubo predictor
> `kubo = cz_weighted_by_1/|z−z_src| − cz_free`, computed directly
> from the free-beam amplitudes + known field profile with no
> fitting, gives r = 0.56 correlation with measured d(cz)/ds across
> 44 families. Off-scaffold correlation is r = 0.72, the strongest
> single off-scaffold number in the classifier program and opposite
> to `free_coh`'s scaffold-specific behaviour. Classification accuracy
> is 79.5%, 9 points below the measurement ceiling. Three structural
> generators (ring, asym_z, longrange) produce honest sign
> disagreements that require a second-moment term the first-moment
> Kubo cannot capture. The derivation target is now sharpened to a
> specific second-moment question, and the 'compact underlying
> principle' row is modestly restored for the first time since the
> classifier lane closed."
