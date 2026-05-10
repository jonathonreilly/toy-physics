# Connes-Kreimer Birkhoff Factorization — External Narrow Theorem

**Date:** 2026-05-10
**Claim type:** positive_theorem
**Scope:** external mathematical theorem for characters of the
Connes-Kreimer Hopf algebra of rooted trees over a commutative
Rota-Baxter target algebra.
**Status authority:** source-note proposal only; independent audit
sets any audit result and pipeline-derived status.
**Runner:** [`scripts/frontier_connes_kreimer_birkhoff_factorization_external_narrow.py`](../scripts/frontier_connes_kreimer_birkhoff_factorization_external_narrow.py)
**Cache:** [`logs/runner-cache/frontier_connes_kreimer_birkhoff_factorization_external_narrow.txt`](../logs/runner-cache/frontier_connes_kreimer_birkhoff_factorization_external_narrow.txt)

## Claim

Let `H_R` be the Connes-Kreimer Hopf algebra of rooted trees and let
`A = A_- direct_sum A_+` be a commutative unital algebra with a
Rota-Baxter projection `T: A -> A_-`. For every character
`phi: H_R -> A`, there are unique characters `phi_-` and `phi_+`
such that

```text
phi = phi_-^{*-1} * phi_+
```

under convolution, with `phi_-(1) = phi_+(1) = 1`,
`phi_-(ker epsilon) subset A_-`, and
`phi_+(ker epsilon) subset A_+`.

For every non-empty tree `t`, the factors are constructed recursively:

```text
prepared_phi(t) = phi(t) + sum_c phi_-(P^c(t)) phi(R^c(t))
phi_-(t)        = -T(prepared_phi(t))
phi_+(t)        = (id - T)(prepared_phi(t))
```

where the sum runs over admissible cuts of `t`, `P^c(t)` is the
pruned forest, and `R^c(t)` is the rooted remainder.

This is Connes-Kreimer's algebraic Birkhoff factorization theorem for
renormalization Hopf algebras.

## Boundary

This note records the external theorem only. It does not claim:

- that any framework operator is a character on `H_R`;
- that any project-specific perturbation expansion has been organized
  as a rooted-tree Hopf algebra;
- closure of any hierarchy formula, `alpha_LM` substitution, blocking
  map, taste-decoupling map, or 16-fold composition;
- any numerical physics prediction or comparison to observation;
- any new framework axiom or repo-wide premise.

Any later use of this theorem in a framework lane must separately
construct the character, target algebra, Rota-Baxter projection, and
bridge to that lane's physical quantity.

## External References

- A. Connes and D. Kreimer, "Renormalization in Quantum Field Theory
  and the Riemann-Hilbert Problem I: the Hopf Algebra Structure of
  Graphs and the Main Theorem", Communications in Mathematical Physics
  210 (2000), 249-273; arXiv:hep-th/9912092.
- A. Connes and D. Kreimer, "Renormalization in Quantum Field Theory
  and the Riemann-Hilbert Problem II: the beta-function,
  Diffeomorphisms and the Renormalization Group", Communications in
  Mathematical Physics 216 (2001), 215-241; arXiv:hep-th/0003188.

## Verification

The paired runner does not attempt to reprove the published theorem.
It verifies the source note's structural transcription on low-depth
examples:

1. the rooted-tree coproduct for `t1` and `t2`;
2. the convolution formula on `t1` and `t2`;
3. the Laurent pole projection Rota-Baxter identity on representative
   Laurent series;
4. the recursive Birkhoff factors for `phi(t1) = 1/e + a`;
5. the recursive Birkhoff factors for
   `phi(t2) = 1/e^2 + b/e + c`;
6. the convolution-unit identities on `t1` and `t2`;
7. the note's no-framework-bridge boundary.

Expected runner result: `PASS=8`, `FAIL=0`.
