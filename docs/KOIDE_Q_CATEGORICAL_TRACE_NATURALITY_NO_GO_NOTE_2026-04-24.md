# Koide Q Categorical Trace/Naturality No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects categorical
trace/Morita naturality on the retained real `C_3` quotient as a derivation
of the normalized charged-lepton traceless source law.
**Primary runner:** `scripts/frontier_koide_q_categorical_trace_naturality_no_go.py`

---

## 1. Theorem Attempt

The strongest categorical route is:

> a retained categorical trace, Morita invariance, or naturality principle on
> the real semisimple `C_3` quotient might force equal total singlet/doublet
> block weights, hence `K_TL = 0`.

The executable result is negative. The retained quotient has two central
summands that are not isomorphic, so categorical automorphisms do not exchange
them. Naturality permits a one-parameter family of positive central trace
states.

---

## 2. Retained Real Quotient

The real `C_3` charged-lepton carrier splits as:

```text
P_plus  : rank 1 real singlet
P_perp  : rank 2 real doublet / complex-character pair
```

The two summands have different real dimensions and algebraic type. Therefore
the retained categorical automorphism group fixes each central idempotent
separately; it does not contain a retained exchange:

```text
P_plus <-> P_perp.
```

---

## 3. Positive Central Trace States

A general positive central trace state is determined by two positive weights:

```text
tau(P_plus) = w_plus
tau(P_perp) = w_perp.
```

Normalization fixes:

```text
w_plus + w_perp = 1,
```

but leaves the ratio:

```text
w_perp / w_plus
```

free. This residual ratio is the trace-state version of the open Koide
source/radius scalar.

---

## 4. Counterexamples

The runner checks three retained-natural positive trace states:

```text
equal_total_blocks : (w_plus, w_perp) = (1, 1) -> Q = 2/3, K_TL = 0
rank_hilbert_trace : (w_plus, w_perp) = (1, 2) -> Q = 1,   K_TL = 3/8
singlet_heavy      : (w_plus, w_perp) = (2, 1) -> Q = 1/2, K_TL = -3/8
```

All are positive and natural under the retained automorphisms because those
automorphisms do not exchange the two central summands. Only the first state
lands on the Koide leaf.

---

## 5. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or `K_TL = 0` as an assumption. Its failure is
structural:

```text
retained categorical naturality -> central trace-state simplex
```

not:

```text
retained categorical naturality -> w_plus = w_perp.
```

Adding an exchange or equal-total-block trace axiom would be exactly the
missing source-neutrality primitive in categorical language.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_categorical_trace_naturality_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_CATEGORICAL_TRACE_NATURALITY_NO_GO=TRUE
Q_CATEGORICAL_TRACE_NATURALITY_CLOSES_Q=FALSE
RESIDUAL_SCALAR=w_plus-w_perp_equiv_K_TL
RESIDUAL_TRACE_STATE=w_plus-w_perp_equiv_K_TL
```

---

## 7. Musk Simplification Pass

After the information-measure, RG/Ward, and categorical-trace no-gos, the
simplified live requirement is still one scalar:

```text
derive K_TL = 0.
```

Deleted as insufficient:

```text
canonical measure choice,
scalar fixed-point grammar,
categorical trace naturality without an exchange.
```

The smallest remaining proof target is no longer a broad variational
principle; it is a retained law that kills the single odd/equal-block residual
without importing that equality as a prior.

---

## 8. Boundary

This note does not reject categorical traces as support. It rejects only the
claim that retained categorical naturality already derives the equal-total
block trace state.

The remaining primitive is:

```text
w_plus = w_perp,
```

equivalently:

```text
K_TL = 0.
```
