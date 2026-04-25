# Koide Q Source-Free Closure Candidate - Nature-Grade Review

**Date:** 2026-04-24
**Reviewed artifact:** `docs/KOIDE_Q_SOURCE_FREE_CLOSURE_THEOREM_NOTE_2026-04-24.md`
and `scripts/frontier_koide_q_source_free_closure_theorem.py`
**Reviewer verdict:** Does not pass as a retained closure theorem. It is a
valid conditional theorem and a useful audit target, but it does not derive
the physical source law.

---

## 1. Decision

The candidate should not be accepted as a closure of the charged-lepton Koide
`Q = 2/3` bridge.

The algebraic chain is correct:

```text
K = 0 -> Y = I_2 -> E_+ = E_perp -> kappa = 2 -> Q = 2/3.
```

The no-hidden-source audit is also correct:

```text
K != 0
```

on the trace-normalized carrier is a one-real selector input in source
coordinates.

The failure is conceptual rather than algebraic: the proposed theorem closes
the bridge by explicitly retaining the missing law `K = 0`. That is exactly
the primitive the April 22 support stack identified as open. A Nature-grade
closure must derive that law from already retained structure, or from a new
principle whose independent physical necessity is established. The current
candidate does neither.

---

## 2. What Survives

The following parts are acceptable as support:

- the normalized second-order carrier has trace `2` and removes common scale;
- the exact reduced generator is `W_red(K) = log det(I + K)`;
- the dual source equation is `K = Y^(-1) - I`;
- the zero-source point is unique and equals the Koide point;
- any nonzero normalized source is equivalent to importing a selector datum.

These results are valuable because they make the remaining target sharp and
falsifiable.

---

## 3. Principal Objection

The proof contains the missing physics as an assumption:

```text
physical selector has no added external selector source, K = 0.
```

No retained local symmetry, source grammar, variational rule, anomaly
condition, gauge constraint, or charged-lepton-specific observable law is
shown to forbid the nonzero source family. Since nonzero source is precisely
the one-dimensional selector freedom, this is not a minor gap. It is the
whole bridge.

The candidate therefore has the form:

```text
If the physical law is K = 0, then Q = 2/3.
```

That statement is true, but it is not yet:

```text
Retained Cl(3)/Z^3 charged-lepton physics forces K = 0.
```

---

## 4. Required Revision

To pass, the branch needs one of the following:

1. derive `K = 0` from a retained charged-lepton source grammar;
2. show that all allowed physical sources are pure trace and therefore carry
   no `Q`-relevant traceless component;
3. derive a block-exchange, real-irrep-democracy, anomaly, or gauge principle
   that forces the traceless source to vanish;
4. prove an exhaustion theorem: every retained source class already present in
   the package has zero traceless component on the normalized second-order
   carrier.

Without one of those, the source-free candidate remains a conditional support
theorem.

---

## 5. Immediate Next Step

The next useful move is not to keep insisting on full `K = 0`. On the
trace-normalized carrier, the trace component is a Lagrange-multiplier gauge
for the normalization constraint. The physical selector burden is only the
traceless component:

```text
K_TL = (K_+ - K_perp) / 2.
```

The next reviewable theorem should prove:

```text
K = 0 on Tr(Y)=2 is stronger than needed;
Q = 2/3 requires exactly K_TL = 0.
```

That does not close `Q`, but it reduces the remaining primitive from two source
coordinates to one physically load-bearing scalar.

---

## 6. Review Outcome

Status assigned by this review:

```text
SOURCE_FREE_CLOSEOUT_AS_RETAINED_Q_CLOSURE = FAIL
SOURCE_FREE_CLOSEOUT_AS_CONDITIONAL_SUPPORT = PASS
NEXT_Q_TARGET = DERIVE_K_TL_EQUALS_ZERO
```

This review does not alter package status. The full Koide lane remains open:
`Q` still needs a physical traceless-source law, and `delta` still needs the
physical Brannen-phase bridge.
