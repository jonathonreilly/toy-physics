# Kroschinsky-Marchetti-Salmhofer Fermionic Brydges Majorant — External Narrow Theorem

**Date:** 2026-05-11
**Claim type:** bounded_theorem
**Scope:** external fermionic-RG majorant theorem from Kroschinsky-Marchetti-Salmhofer arXiv:2404.06099 (2024), cited as rigorous-RG context for the fermionic Polchinski equation. No framework substitution, hierarchy formula, or physical scale closure is claimed.
**Status authority:** source-note proposal only; independent audit sets any audit result and pipeline-derived status.
**Runner:** [`scripts/frontier_kms_fermionic_brydges_majorant_external_narrow.py`](../scripts/frontier_kms_fermionic_brydges_majorant_external_narrow.py)
**Cache:** [`logs/runner-cache/frontier_kms_fermionic_brydges_majorant_external_narrow.txt`](../logs/runner-cache/frontier_kms_fermionic_brydges_majorant_external_narrow.txt)

## Claim

Let `V_l` denote the fermionic effective interaction at scale `l` along the Polchinski continuous Wilsonian flow with infrared cutoff parameter `l`. Let `||.||_h` denote a Brydges-Battle-Federbush polymer norm with auxiliary weight parameter `h > 0` (Gram-type fermion norm; see KMS §2 for the exact definition).

Then there exist scale-dependent majorant coefficients `M_l >= 0` and a Polchinski flow equation

```text
d/dl V_l = - <V_l, V_l>_C + Delta_C V_l
```

(where `<.,.>_C` is the Polchinski quadratic form and `Delta_C` is the cutoff-derivative Laplacian) for which the BBF polymer norm satisfies a per-scale majorant bound

```text
d/dl ||V_l||_h <= a(l) ||V_l||_h^2 + b(l) ||V_l||_h
```

with explicit, scale-integrable, non-negative `a(l), b(l)` derived from the Gram covariance decomposition (KMS Theorem 1; arXiv:2404.06099 v1, eq. (T1)).

As a corollary, if `||V_{l_0}||_h` is sufficiently small at the ultraviolet endpoint `l_0`, the flow is globally well-defined and contracts in the BBF norm, with the standard rigorous-RG global-existence consequences.

## Boundary

This note records an external fermionic-RG theorem and its standard published context. It does not claim:

- that any framework staggered-Dirac blocking/coarse-graining is the KMS continuous Polchinski flow;
- that the framework's canonical surface lies in the KMS small-data regime;
- that any project-specific coupling is the BBF norm coefficient at any scale;
- closure of any framework substitution, hierarchy formula, or physical scale;
- any numerical prediction or comparison with observation;
- any new framework axiom or repo-wide premise;
- specifically: the scaffold admissions of `HIERARCHY_BBS_STAGGERED_TASTE_BLOCKING_BRIDGE_SCAFFOLD_AVAILABILITY_BOUNDED_NOTE_2026-05-11.md` remain open; KMS provides published fermionic-RG technology, but the substrate-specific bridge to those admissions would still need to be separately constructed.

Any later framework use must separately construct the polymer norm, identify the framework substrate's effective action with `V_l`, verify the small-data hypothesis, and establish the physical bridge.

## External References

- A. Kroschinsky, D. Marchetti, M. Salmhofer, "A Brydges-Battle-Federbush representation for the fermionic Polchinski equation", arXiv:2404.06099 (2024).
- D. C. Brydges, "A short course on cluster expansions", in Phenomenes critiques, systemes aleatoires, theories de jauge (Les Houches 1984), North-Holland (1986), 129-183.
- M. Disertori, V. Rivasseau, "Continuous constructive fermionic renormalization", Annales Henri Poincare 1 (2000), 1-57.
- M. Salmhofer, Renormalization: An Introduction, Texts and Monographs in Physics, Springer (1999).
- J. Polchinski, "Renormalization and effective Lagrangians", Nuclear Physics B 231 (1984), 269-295.

## Verification

The paired runner checks:

1. exact Fraction arithmetic for the scalar majorant ODE `dy/dl = a y^2 + b y` solved on a finite-grid; small-data integrability of the closed-form solution;
2. monotonicity: if `y(l_0) <= y_0` and `a, b >= 0` integrable, then `y(l)` stays bounded on `[l_0, infinity)` iff `y_0` lies below the explicit small-data threshold;
3. composition: the per-scale norm bound chains across `N` scales `l_0 < l_1 < ... < l_N` with product structure on the exponential `b`-factor;
4. the small-data fixed-point structure of the Polchinski quadratic form, on scalar and finite-dimensional toy operators;
5. substrate-independence: the majorant ODE structure does not depend on the particular fermionic theory beyond the inputs `(a(l), b(l))`;
6. source-note boundary checks excluding framework bridge claims, framework-substrate-specific identification, and any scaffold-admission closure;
7. sharpness at the small-data threshold: above the threshold the scalar majorant blows up in finite scale-time;
8. positivity of the BBF norm by construction (sum of non-negative Gram norms over polymers).

Expected runner result: `PASS=N`, `FAIL=0`.
