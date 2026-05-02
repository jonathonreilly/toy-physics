# Koide Cyclic Wilson 3-Response Law — Narrow Conditional Theorem

**Date:** 2026-05-02
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_koide_cyclic_wilson_3_response_narrow.py`

## Claim scope (proposed)

> **Given** any local Wilson first-variation `dW` on the Hermitian image of the
> C₃[111]-covariant adjacent-chain path algebra, the cyclic descendant
> `H_cyc = (r₀/3) B₀ + (r₁/6) B₁ + (r₂/6) B₂` is determined by exactly three
> real responses `r_i = dW(B_i)`, `i ∈ {0,1,2}`, where `(B₀, B₁, B₂) = (I, C+C², i(C−C²))`
> with `C` the retained forward cycle on the charged-lepton triplet.

The boundary is the conditional **given** clause. This theorem **does not**
claim:

- that a local Wilson first-variation actually exists for physical charged
  leptons;
- that the cyclic projection captures the physical observable structure;
- that the resulting scalar equation `2 r₀² = r₁² + r₂²` is necessarily the
  Koide relation (that identification is a separate downstream claim);
- closure of the broader Koide lane.

The audit row's previously-named "claim boundary until fixed" was:
*"it is safe to claim the conditional algebraic reduction: given a local
Wilson first variation on the adjacent-chain image, cyclic projection
yields exactly three responses and Koide becomes the scalar equation
2 r₀² = r₁² + r₂²."* This narrow theorem is that exact safe scope.

## Declared audit dependency (one-hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md`](KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md) | pipeline-derived; may be audit-pending after dependency-graph strengthening | supplies the C₃[111]-covariant adjacent-chain path algebra and its cyclic Hermitian basis |

No other authority is cited as load-bearing.

## Load-bearing step (class A)

```text
H ∈ span_R(B₀, B₁, B₂)         (cyclic Hermitian sub-algebra of the adjacent-chain image, from declared dep)
dW(H) = α₀ r₀ + α₁ r₁ + α₂ r₂   (linearity of dW)
H_cyc reconstruction:
  H_cyc = (r₀/3) B₀ + (r₁/6) B₁ + (r₂/6) B₂
```

Verification: the Frobenius-dual pairings `<B_i, H_cyc>` recover the response
data `(r₀, r₁, r₂)`. This is class (A) algebra once the cyclic-basis dependency
is accepted. The retained family status is not asserted by this source note; it
is pipeline-derived after independent audit of this row and its dependency
chain.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_cyclic_wilson_3_response_narrow.py
```

The runner verifies, at exact rational precision via Python `Fraction`
on a 3×3 representation:

1. Cyclic Hermitian basis `(B₀, B₁, B₂)` spans the cyclic Hermitian
   subspace of the C₃-covariant matrix algebra (3 real dimensions out
   of the 6 real dimensions of Herm(3)).
2. For an arbitrary linear functional `dW`, the three responses
   `(r₀, r₁, r₂)` uniquely determine the projection of `dW` onto the
   cyclic Hermitian dual.
3. Reconstruction `H_cyc = (r₀/3) B₀ + (r₁/6) B₁ + (r₂/6) B₂` gives the
   unique cyclic Hermitian element with response triple `(r₀, r₁, r₂)`.
4. The Koide scalar equation `2 r₀² = r₁² + r₂²` is verified as a single
   constraint on the response space (a 2-sphere section), NOT claimed
   to hold for physical charged leptons.

## Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  conditional algebraic reduction: given a local Wilson first-variation on the
  C₃[111]-covariant adjacent-chain image, cyclic projection yields exactly
  three real responses determining H_cyc; physical-observable identification
  out of scope.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
```

Audit status is set only by the independent audit lane. This note is safe to
land as an unaudited, graph-visible bounded theorem candidate; retained-family
effective status requires independent audit of this row and retained-grade
closure of its declared dependency chain.

## What this theorem closes

The conditional algebraic reduction the audit named as the safe scope.
This is a stand-alone bounded theorem candidate on the Koide cyclic compression
surface. Its audit outcome remains pending.

## What this theorem does NOT close

- Existence of the local Wilson first-variation for physical charged
  leptons (out of scope; conditional premise).
- Identification of the scalar equation `2 r₀² = r₁² + r₂²` with the
  physical Koide relation (separate downstream claim).
- The broader Koide lane (separate sister theorems).

## Cross-references

- KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md — parent row with a
  conditional audit verdict; this narrow theorem carves out the audit's named
  safe scope as a standalone claim row. The parent is not load-bearing for the
  narrow lemma.
- [`KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md`](KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md) — declared load-bearing dependency.
