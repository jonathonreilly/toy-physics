# Second-Order Kubo Extension — NEGATIVE (Boundary of Taylor-Expansion Approach)

**Date:** 2026-04-07
**Status:** proposed_retained negative — adding the second-order term `½·kubo₂·s²` to the first-order Kubo prediction does NOT explain the failing-family pathology. The linearity-regime subset stays at 15/44 families, residual sums actually grow slightly, and the documented failing families (`G2_asym_z`, `H1_ring`, `L1_longrange`, `OF9_stretched`, `K3_NL5`) either get worse, stay the same, or improve only marginally. This delineates the boundary of the Taylor-expansion line of attack: the first-order Kubo derivation is the dominant term in the linear regime but cannot be extended to the failing families by adding higher Taylor orders.
**Claim type:** positive_theorem

**Audit-conditional perimeter (2026-04-27):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
positive_theorem`, `independence = cross_family`, and load-bearing
step class `C`. The audit chain-closure explanation is exact: "The
live runner reproduces the second-order null result, but the note
extrapolates that finite computation into a boundary claim about
the Taylor-expansion approach and higher Taylor orders without a
convergence/no-go theorem." The audit-stated repair target
(`notes_for_re_audit_if_any`) is exact: "scope_too_broad: either
narrow the source claim to the computed second-order null result,
or add a theorem/computation bounding the Taylor remainder or
demonstrating non-convergence/non-analyticity for the failing
families, with the first-order and range-of-validity inputs
explicitly audited." The generated audit ledger remains the authority for any terminal status. Nothing in this edit
promotes audit status, narrows the source claim, or adds the
missing convergence theorem; the note continues to extrapolate
from the second-order replay to a Taylor-boundary diagnosis. The
**conditional perimeter** is therefore the gap between (a) the
actually replayed finite computation — second-order Kubo on the
44-family battery, with the residual / linearity-regime numbers
documented in §Result — and (b) the broader §"What this closes"
language about *all higher Taylor orders* and *all Taylor
expansions at s = 0*. Until either the source narrows to (a) or
adds a remainder/non-analyticity theorem covering (b), the safe
read of this note is the second-order replay and its three
structural categories (finite-size `K3_NL5`, structural cancellation
`G2_asym_z`, phase decorrelation `H1_ring` / `L1_longrange`) — not
a closed all-orders Taylor no-go. The §"What stands" list
explicitly preserves the first-order Kubo + range-of-validity
positives (sibling notes); those rows are independently audited.
See "Citation chain and audit-stated repair path (2026-05-10)"
below.

## Artifact chain

- [`scripts/linear_response_second_order_kubo.py`](../scripts/linear_response_second_order_kubo.py)
- [`logs/2026-04-07-linear-response-second-order-kubo.txt`](../logs/2026-04-07-linear-response-second-order-kubo.txt)

## Question

The first-order Kubo lane derived `d(cz)/ds` at s = 0 via a parallel
perturbation propagator `B_j = d(amp_j)/ds`. The range-of-validity lane
showed that on a strict linearity-regime subset (15/41 families,
selected without the F~M label), measured F~M is within 1.6% of 1.0.

The other 26/41 families fall outside the strict linear regime. They
have documented nonlinear ratio patterns:

- `G2_asym_z`: ratio flips sign 0.17 → 0.05 → −0.19 → −0.69
- `K3_NL5`: ratio ≈ 2 throughout (systematic factor of 2)
- `H1_ring`: ratio drifts 0.55 → 0.58 → 0.65 → 0.80
- `L1_longrange`: similar drifting pattern
- `OF9_stretched`: ratio crosses 1 from above

This lane tests whether **second-order Kubo** (the `s²` term in the
Taylor expansion at s = 0) explains those patterns.

## The derivation

For path P from source to detector node j with phase factor `T_P` and
perturbation factor `Q_P = Σ_edges (L_e / r_e)`:

```
amp_j(s) = Σ_paths T_P · exp(−i s k Q_P)

A_j = amp_j(0)         = Σ T_P
B_j = (d amp_j/ds)|₀   = −ik Σ T_P Q_P
C_j = (d² amp_j/ds²)|₀ = −k² Σ T_P Q_P²
```

The recurrence for `C_j` follows from expanding `(Q_{P_i} + L_e / r_e)²`
along each incoming edge. With `g_e = −ik · L_e / r_e`:

```
C_j = Σ_{i→j} [C_i + 2·g_e·B_i + g_e²·A_i] · exp(ikL) · w · h²/L²
```

All three propagators (A, B, C) run in a single pass — same path-sum
structure, same O(edges) cost.

The second-order prediction for the centroid response is:

```
predicted_delta_cz(s) ≈ kubo₁ · s + (1/2) · kubo₂ · s²

where
  kubo₁ = (d cz/ds)|₀  via A and B
  kubo₂ = (d² cz/ds²)|₀  via A, B, and C (chain rule):
        = (N₂ − 2·kubo₁·T₁ − cz₀·T₂) / T₀
```

with `N₁, N₂, T₁, T₂` the corresponding numerator/total derivatives
expressed via `2 Re[A* B]`, `2 Re[A* C] + 2 |B|²`, etc.

## Result

### Linearity regime (max |ratio − 1| < 0.10 at all 4 strengths)

| Selection | Count |
| --- | ---: |
| First-order Kubo only | **15/44** |
| First + second-order Kubo | **15/44** |
| **Growth** | **+0 families** |

The strict linearity regime does **not grow** with the second-order
extension. None of the failing families are brought into the linear
regime by adding the `s²` term.

### Aggregate residuals at s = 0.008

| Order | sum \|residual\| | median \|residual\| |
| --- | ---: | ---: |
| First-order only | 5.6090 | 0.003385 |
| First + second-order | 5.7221 | 0.003258 |

Sum of absolute residuals **grows** by 2% with the second-order term.
Median residual barely improves. The second-order term does not
provide a consistent reduction in the prediction error across the
44-family set.

### Per-family pathology

The six families with documented nonlinear ratio patterns:

| Family | kubo₁ | kubo₂ | 1st-order ratios | 2nd-order ratios | verdict |
| --- | ---: | ---: | --- | --- | --- |
| `G1_asym_y` | +2.69 | +6.14 | 1.25 → 1.29 | 1.25 → 1.27 | tiny improvement |
| `G2_asym_z` | +0.31 | −26.0 | 0.17 → −0.69 | 0.18 → **−1.04** | **worse at large s** |
| `H1_ring` | −2.12 | −60.8 | 0.55 → 0.80 | 0.54 → 0.72 | slightly better |
| `K3_NL5` | +0.27 | +0.08 | 2.12 → 1.89 | 2.12 → 1.89 | **no change** |
| `L1_longrange` | −1.36 | −57.3 | 0.59 → 0.70 | 0.58 → 0.60 | mixed |
| `OF9_stretched` | −0.05 | +3.64 | 1.27 → 1.03 | 1.33 → **1.50** | **worse** |

## Three structural categories of failure

The failing families fall into three distinct nonlinear regimes,
**none** of which is fixed by adding a Taylor series term at s = 0:

### 1. Finite-size / boundary cases — `K3_NL5`

`K3_NL5` has NL = 5 (only 5 layers). The Kubo expansion assumes the
propagator has reached an asymptotic regime where the path-sum
structure is well-defined. With only 5 layers, the propagator is
dominated by boundary effects and never enters that regime.
`kubo₂ = 0.08` is essentially zero — the second-order correction
is negligible — but the measured ratio sits at ~2 throughout. The
factor of 2 is a finite-size offset, not a Taylor-series correction.
**No order of Taylor expansion at s = 0 will fix this.**

### 2. Structural cancellation — `G2_asym_z`

`G2_asym_z` has broken Z2 in the measurement axis. The first-order
linear term is very small (`kubo₁ = 0.31`, vs ~5 for healthy families),
so the response is dominated by destructive interference cancelling
the leading term. The second-order term `kubo₂ = −26.0` is large in
magnitude but in the wrong sign regime: at s = 0.008 the corrected
prediction overshoots from −0.69 to **−1.04**. The Taylor series at
s = 0 has poor convergence here because the small linear coefficient
puts the higher-order terms in a sign-cancellation regime.

### 3. Phase decorrelation — `H1_ring`, `L1_longrange`

Both have large `|kubo₂|` (~−60) and ratio patterns that drift
smoothly with s in a non-Taylor-analytic way. The structural drift
(from 0.55 to 0.80 for `H1_ring`, from 0.59 to 0.70 for `L1_longrange`)
is consistent with **path-phase decorrelation**: paths with very
different lengths contribute to the response with random relative
phases, and the resulting integral does not have a clean
power-series expansion in s. These need a non-perturbative path-sum
treatment, not more Taylor terms.

## What this closes

This is a **clean negative** that delineates the boundary of the
Kubo-Taylor approach:

- The first-order Kubo derivation works on the **linearity regime**:
  15 / 41 families where the linear term dominates and the higher-order
  Taylor corrections are small. On these, F~M ≈ 1 (mean |F~M − 1| =
  0.0069) and gravity sign is correctly predicted.
- The second-order Kubo extension does **not** generalize the
  derivation to the other 26 / 41 families. Adding more Taylor terms
  at s = 0 would not work either, because the failing families'
  nonlinearities are not analytic perturbations of the linear regime
  — they are structural (finite size, cancellation, decorrelation).
- The remaining failing families need **structurally different
  treatments**: finite-size corrections for `K3_NL5`, full path-sum
  for the structural-cancellation cases, non-perturbative path-phase
  analysis for the decorrelation cases.

## What stands

The first-order Kubo lane and the linearity-regime range-of-validity
lane are **unaffected** by this negative. They derive:

- Gravity sign: 42/44 sign agreement, r = 0.97 correlation across all
  44 families (true-Kubo lane)
- F~M ≈ 1: 15/15 families in the strict linearity regime, mean
  |F~M − 1| = 0.0069 (range-of-validity lane)

These are the retained positives. This lane (second-order Kubo) does
not extend them, but it also does not undermine them.

## Frontier map adjustment (Update 7)

| Row | Update 6+ (after range-of-validity) | This lane |
| --- | --- | --- |
| Compact underlying principle | first-order Kubo derives sign + F~M on linear regime | **bounded**: 15 / 41 is the maximum reach of Kubo-Taylor approach |
| Theory compression | first-order derived; second-order open | **second-order does NOT extend the derivation; structural treatment needed for failing families** |
| Strength against harshest critique | analytic expression on linear regime | unchanged |

## Honest read

This is a **negative** but a clean and informative one. It says:

- The Kubo Taylor expansion at s = 0 has a **bounded reach** — about
  37% of the cross-generator family set, exactly the linearity-regime
  subset already characterized.
- Higher-order Taylor terms at s = 0 do not extend that reach,
  because the failing families' nonlinearities are not analytic
  perturbations of the linear term.
- The remaining derivation work must be **structurally different**:
  either finite-size corrections, full non-perturbative path-sum, or
  a different analytic framework (e.g., expansion around a different
  basepoint, or transfer-matrix spectral analysis).

It does **not** invalidate the first-order Kubo derivation. It tells
us where that derivation reaches and where it ends.

## What to attack next

1. **Born preservation derivation** — the Born condition `|I₃|/P < 1e-10`
   in the battery is a direct consequence of propagator linearity in
   the sources. This is a one-line proof that adds a third battery
   condition to the derivation column. Cheap and clean.
2. **Experimental prediction card for wave-retardation** — the
   physics flagship lane that's closest to a lab claim. Different
   scorecard column entirely.
3. **Non-perturbative path-sum analysis** for the failing families —
   structurally bigger than the Kubo lane; would need a new
   computational framework.

Of the three, (1) is the smallest and most certain to add a result.
(2) is the highest-leverage column move. (3) is the deepest but most
expensive.

## Bottom line

> "Adding the second-order Kubo term `½·kubo₂·s²` to the first-order
> prediction does not extend the derivation past the linearity regime.
> The strict linearity-regime subset stays at 15/44 (zero growth), the
> aggregate residual at s=0.008 actually grows by 2%, and the documented
> failing families (`G2_asym_z`, `H1_ring`, `K3_NL5`, `L1_longrange`,
> `OF9_stretched`) either get worse, stay the same, or improve only
> marginally with the second-order correction. The failing families
> fall into three structural categories — finite-size effects,
> destructive cancellation of the linear term, and path-phase
> decorrelation — none of which are fixed by more Taylor terms at
> s = 0. The Kubo Taylor approach has a bounded reach of about 37% of
> the cross-generator family set; the first-order Kubo derivation
> stands on that subset and does not extend further by this method."

## Citation chain and audit-stated repair path (2026-05-10)

The audit verdict (2026-04-27, see top of note) flags that the
note "extrapolates [the] finite computation into a boundary claim
about the Taylor-expansion approach and higher Taylor orders
without a convergence/no-go theorem." The cited authority chain
on this row is registered explicitly below so the audit-graph
one-hop edges from the source note to its load-bearing inputs
are visible.

| Cited authority | File / log | Role on this row |
|---|---|---|
| Active runner | [`scripts/linear_response_second_order_kubo.py`](../scripts/linear_response_second_order_kubo.py) | computes the third parallel propagator `C_j = d^2(amp_j)/ds^2` at s = 0 via the same path-sum recurrence, evaluates `kubo_2 = d^2(cz)/ds^2|_0`, runs four battery strengths `s in {0.001, 0.002, 0.004, 0.008}`, and writes the per-family residual / ratio table cited in §Result |
| Frozen runner output | [`logs/2026-04-07-linear-response-second-order-kubo.txt`](../logs/2026-04-07-linear-response-second-order-kubo.txt) | preserves the linearity-regime count (15/44 first-order vs 15/44 first+second-order), the aggregate residual (5.6090 vs 5.7221), and the per-family kubo_1 / kubo_2 / ratio rows for the six families enumerated in the per-family pathology table |
| Audit-lane runner cache | [`logs/runner-cache/linear_response_second_order_kubo.txt`](../logs/runner-cache/linear_response_second_order_kubo.txt) | runner-cache copy referenced by the audit-lane replay verifying the second-order null result |
| Sibling first-order Kubo runner | [`scripts/linear_response_true_kubo.py`](../scripts/linear_response_true_kubo.py) | the literal first-order `<z*deltaH>_0` computation cited in §"What stands"; its closure is the input under which §"What this closes" defends the bounded 15/44 linearity reach |
| Sibling first-order Kubo log | [`logs/2026-04-07-linear-response-true-kubo.txt`](../logs/2026-04-07-linear-response-true-kubo.txt) | preserved log for the sibling [`docs/LINEAR_RESPONSE_TRUE_KUBO_NOTE.md`](LINEAR_RESPONSE_TRUE_KUBO_NOTE.md) |
| Generator inputs | `scripts/universality_classifier.py`, `scripts/independent_generators_heldout.py`, `scripts/global_coherence_off_scaffold.py` | the same three import surfaces enumerating the 26 swept + 9 scaffolded + 9 off-scaffold families used by the runner |
| Repo baseline anchor | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `unaudited` / `meta` repo-baseline terminology anchor for the linear path-sum architecture |

The audit-stated repair path (verbatim from the audit
`notes_for_re_audit_if_any`) is to either (i) **narrow the source
claim** to the computed second-order null result on the 44-family
battery, or (ii) **add a theorem or computation bounding the
Taylor remainder or demonstrating non-convergence / non-analyticity**
for the failing families. Path (i) would require sharpening the
§"What this closes" and §"Honest read" wording from "all Taylor
terms at s = 0" / "the Kubo-Taylor approach has a bounded reach"
to a strictly second-order statement, with the all-orders extrapolation
withdrawn. Path (ii) would require a third-or-higher-order computation
or an analytic remainder bound; neither is supplied here. Until one
lands, the regenerated ledger leaves this row for independent audit,
and the safe read is the second-order replay (computed §Result) plus
the three structural
categories (finite-size, structural cancellation, phase decorrelation)
that the second-order replay observes — not an all-orders Taylor
no-go. The acknowledged residual is the absence of a remainder /
non-analyticity theorem covering Taylor orders beyond two; everything
else (the second-order recurrence, the kubo_1 / kubo_2 numbers, the
zero growth of the strict linearity-regime subset) is supported by
the listed cited authorities.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not promote audit
status, hand-author audit JSON, narrow the source text, or add the
missing convergence theorem. The §"What this closes" / §"What this
does not close" boundary continues to apply: the second-order replay
result is supported, but the broader Taylor-boundary statement
remains audit-conditional until a remainder bound or higher-order
extension lands.
