# Koide Q Source-Free Closure Candidate

**Date:** 2026-04-24
**Status:** REVIEW-CANDIDATE Q-CLOSURE THEOREM on the admitted normalized
second-order carrier. This is branch-local science for reviewer evaluation,
not a repo-wide status promotion.
**Scope:** Charged-lepton Koide `Q = 2/3` only. This note does not close the
Brannen phase `delta = 2/9` bridge, and it does not fix the overall
charged-lepton scale `v0`.

---

## 1. What changed

The April 22 support batch reduced the `Q = 2/3` bridge to one primitive:

> why the physical charged-lepton selector is source-free (`K = 0`) on the
> normalized second-order reduced carrier.

This note proposes closing that residue by retaining the corresponding
source-neutrality law:

> On the exact first-live charged-lepton second-order reduced carrier, the
> physical normalized selector has no added external selector source:
> `K = 0`.

This is an explicit review-candidate primitive. It is not claimed here to be
derived from older notes alone. The value of this closeout candidate is that
the final primitive is now named, executable, and audited against target
import. If the reviewer retains the primitive, the `Q = 2/3` source-law bridge
closes by exact algebra.

---

## 2. Carrier

On the admitted second-order block carrier, normalize the positive block
powers by trace:

```text
Y = diag(2 E_+ / (E_+ + E_perp), 2 E_perp / (E_+ + E_perp)),
Tr(Y) = 2.
```

This quotient removes the common charged-lepton mass scale. The identity point
is exactly

```text
Y = I_2  <=>  E_+ = E_perp.
```

---

## 3. Source Response

The reduced two-block observable generator is exactly

```text
W_red(K) = log det(I + K).
```

Its Legendre-dual source equation is

```text
K = Y^(-1) - I,
```

and the corresponding effective action is

```text
S_eff(Y) = Tr(Y) - log det(Y) - 2.
```

On the trace-normalized carrier `Y = diag(y, 2-y)`, this reduces to

```text
S_eff|Tr=2 = -log(y (2-y)).
```

It has a unique interior stationary point, a strict minimum, at `y = 1`.

---

## 4. Source-Neutrality Closure Candidate

The proposed physical law is the no-added-selector-source condition:

```text
K = 0.
```

Using the exact dual equation, this gives

```text
K = Y^(-1) - I = 0  <=>  Y = I_2.
```

Therefore

```text
E_+ = E_perp.
```

On the Brannen/circulant charged-lepton carrier this is exactly

```text
kappa = 2,
Q = (1 + 2/kappa) / 3 = 2/3.
```

So the source-neutrality law closes the charged-lepton `Q = 2/3` source-law
bridge if the reviewer accepts it as retained physics.

---

## 5. No-Hidden-Source Audit

On the normalized trace slice,

```text
Y = diag(y, 2-y),
K(y) = diag(1/y - 1, 1/(2-y) - 1).
```

The zero-source equation has the unique interior solution `y = 1`.

If a nonzero source is allowed, the trace constraint leaves a one-parameter
family:

```text
k_perp(k_+) = -k_+ / (2 k_+ + 1),
Y(k_+) = diag(1/(1+k_+), (2 k_+ + 1)/(1+k_+)).
```

That family is exactly the selector variable in source coordinates. In
particular,

```text
Q(y) = 2/(3y),
Q(k_+) = 2/3 + 2 k_+/3.
```

Thus any nonzero normalized source imports one real selector datum. The unique
datum-free point is `K = 0`, and it is the Koide point.

---

## 6. Executable Closeout

Primary runner:

```bash
python3 scripts/frontier_koide_q_source_free_closure_theorem.py
```

Result:

```text
PASSED: 18/18
REVIEW_CANDIDATE_KOIDE_Q_SOURCE_FREE_CLOSURE=TRUE
DELTA_BRANNEN_BRIDGE_CLOSED_BY_THIS_RUNNER=FALSE
```

Supporting runners from the April 22 stack:

```bash
python3 scripts/frontier_koide_q_normalized_second_order_effective_action.py
python3 scripts/frontier_koide_q_no_hidden_source_audit.py
python3 scripts/frontier_koide_q_second_order_reviewer_stress_test.py
```

---

## 7. Boundary

Review-candidate closure:

- the charged-lepton Koide `Q = 2/3` source-law bridge, on the
  source-neutral normalized second-order carrier, if the reviewer accepts the
  source-neutrality primitive as retained.

Still open:

- the physical Brannen-phase bridge behind `delta = 2/9`;
- the downstream `m_*` / `w/v` dependence on that Brannen bridge;
- the separate overall charged-lepton scale `v0`.

This is therefore a branch-local `Q` closeout candidate for review, not a full
charged-lepton Koide/Brannen package closeout and not a repo-wide status
promotion.
