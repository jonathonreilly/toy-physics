# Koide Q Dihedral-Normalizer Exchange No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects the retained
`D_3`/`S_3` normalizer of the `C_3` body-axis as a source of the missing
singlet/doublet exchange needed to derive `K_TL = 0`.
**Primary runner:** `scripts/frontier_koide_q_dihedral_normalizer_exchange_no_go.py`

---

## 1. Theorem Attempt

The strongest normalizer route is:

> plain `C_3` does not exchange the singlet and real-doublet blocks, but the
> retained cubic/S3 geometry contains a dihedral normalizer of the body-axis
> cyclic group. Perhaps the extra reflection supplies the missing
> `K_TL -> -K_TL` sign flip.

The executable result is negative. The reflection sends
`omega <-> omega^2` inside the real doublet and fixes the singlet. It does not
exchange the rank-1 singlet with the rank-2 real doublet.

---

## 2. Exact Normalizer Action

Let `C` be the retained cyclic generator and `F` a reflection satisfying:

```text
F C F = C^{-1}.
```

Thus `F` is the retained dihedral normalizer reflection. On the central
projectors:

```text
F P_plus F^{-1} = P_plus
F P_perp F^{-1} = P_perp.
```

Over the complex character projectors:

```text
F P0 F^{-1} = P0
F P_omega F^{-1} = P_omega^2
F P_omega^2 F^{-1} = P_omega.
```

So the new reflection enforces conjugate-character neutrality only inside:

```text
P_perp = P_omega + P_omega^2.
```

---

## 3. Invariant Source Algebra

The full `D_3` commutant is:

```text
[[x8, x7, x7],
 [x7, x8, x7],
 [x7, x7, x8]].
```

Equivalently, every retained-normalizer-invariant source is:

```text
K = a P_plus + b P_perp.
```

Its trace/traceless decomposition is:

```text
K_trace = (a+b)/2
K_TL    = (a-b)/2.
```

The full normalizer imposes no equation:

```text
a = b.
```

---

## 4. Counterexample

The runner checks:

```text
a = 1, b = 2.
```

This source is invariant under both `C` and the retained reflection `F`, but:

```text
K_TL = -1/2 != 0.
```

Thus retained `D_3`/`S_3` normalizer symmetry does not close the Koide source
law.

---

## 5. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or `K_TL = 0` as an assumption. Its failure is:

```text
retained normalizer -> omega/omega^2 neutrality
```

but not:

```text
retained normalizer -> singlet/doublet total neutrality.
```

Adding a sign flip of `K_TL` would be the missing block-exchange/source-law
primitive, not a theorem from the retained normalizer.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_dihedral_normalizer_exchange_no_go.py
```

Result:

```text
PASSED: 11/11
KOIDE_Q_DIHEDRAL_NORMALIZER_EXCHANGE_NO_GO=TRUE
Q_DIHEDRAL_NORMALIZER_EXCHANGE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=dihedral_invariant_singlet_doublet_ratio_equiv_K_TL
```

---

## 7. Boundary

This note strengthens the earlier block-exchange and real-structure no-gos by
including the full retained normalizer reflection explicitly. It does not
reject the normalizer as retained structure. It rejects only the stronger
claim that this normalizer derives:

```text
K_TL = 0.
```
