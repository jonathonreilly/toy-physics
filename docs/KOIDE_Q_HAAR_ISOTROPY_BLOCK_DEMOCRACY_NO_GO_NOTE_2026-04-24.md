# Koide Q Haar/Isotropy Block-Democracy No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects Haar/isotropic
representation naturality as a derivation of the charged-lepton
`K_TL = 0` source law.
**Primary runner:** `scripts/frontier_koide_q_haar_isotropy_block_democracy_no_go.py`

---

## 1. Question

The source-free and block-democracy support routes close the charged-lepton
`Q` bridge conditionally:

```text
equal total real-isotype block weights
<=> K_TL = 0
<=> Q = 2/3.
```

The Nature-grade upgrade attempt is:

```text
retained C_3 carrier + natural Haar/isotropic measure
-> equal total singlet/doublet block weights.
```

The executable answer is:

```text
No.
```

Haar/O(3) isotropy equalizes energy per real dimension. It does not equalize
total energy per unequal-rank real isotype block.

---

## 2. Exact Carrier Geometry

Let `P_plus` be the `C_3` singlet projector and `P_perp = I - P_plus` the real
doublet projector on the three-slot carrier. Their ranks are:

```text
rank(P_plus) = 1,
rank(P_perp) = 2.
```

A general positive `C_3`-invariant Gaussian source covariance is:

```text
Sigma = sigma_plus^2 P_plus + sigma_perp^2 P_perp.
```

This leaves one positive variance ratio free. The expected block-total energy
ratio is:

```text
R = E_perp/E_plus = 2 sigma_perp^2 / sigma_plus^2.
```

The Koide/block-democracy leaf is:

```text
R = 1.
```

So it requires:

```text
sigma_plus^2 = 2 sigma_perp^2.
```

That is not Haar/O(3) isotropy. It is an anisotropic per-real-dimension
weighting that makes the one-dimensional singlet block carry the same total
energy as the two-dimensional doublet block.

---

## 3. Haar/Isotropic Result

Haar/O(3) isotropy sets:

```text
sigma_plus^2 = sigma_perp^2.
```

Therefore:

```text
R_iso = 2,
Q_iso = (1 + R_iso)/3 = 1,
K_TL_iso = 3/8.
```

Equivalently, the Haar push-forward for the singlet block-total fraction is:

```text
p_plus ~ Beta(1/2, 1),
E[p_plus] = 1/3,
E[p_perp] = 2/3.
```

This is rank weighting, not equal total block weighting.

---

## 4. Counterexample

The isotropic covariance

```text
Sigma = I
```

is retained and maximally natural under the larger `O(3)` symmetry. It is also
`C_3`-invariant. But it gives:

```text
E_perp/E_plus = 2,
Q = 1,
K_TL = 3/8.
```

Thus Haar/isotropic representation naturality does not force the normalized
traceless source to vanish.

---

## 5. Falsifiers

This no-go would be falsified by a retained measure theorem proving that the
physical source ensemble is not Haar/isotropic on the real carrier, but is
instead a block-total measure whose Radon-Nikodym weight is exactly inverse to
the real block ranks:

```text
sigma_plus^2 / sigma_perp^2 = 2.
```

It would also be falsified by a retained physical law that makes total
isotype-block energy, rather than per-real-dimension energy, the primitive
equipartition object and derives that law from `Cl(3)/Z^3` dynamics rather
than choosing it as a prior.

No such theorem is currently retained.

---

## 6. Reviewer Objections Answered

**Objection:** Haar naturality is the canonical representation-theoretic
measure, so it should close the block-democracy route.

**Answer:** It selects equal density per real dimension. Because the retained
blocks have ranks `1` and `2`, the induced block totals are `1:2`, not `1:1`.

**Objection:** Equal block totals are still natural if the blocks are treated
as two atoms.

**Answer:** Yes, but that is a different coarse graining. It is precisely the
extra equal-block prior already isolated by the entropy no-go.

**Objection:** The Koide covariance is still `C_3`-invariant.

**Answer:** Correct. `C_3` permits it, but does not select it. The missing
work is a retained theorem that picks the anisotropic variance ratio
`sigma_plus^2/sigma_perp^2 = 2`.

---

## 7. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_haar_isotropy_block_democracy_no_go.py
```

Result:

```text
PASSED: 14/14
KOIDE_Q_HAAR_ISOTROPY_BLOCK_DEMOCRACY_NO_GO=TRUE
Q_HAAR_ISOTROPY_CLOSES_Q=FALSE
RESIDUAL_PRIOR=equal_total_real_isotype_block_weights_equiv_K_TL=0
```

---

## 8. Boundary

This note does not demote the conditional source-free or equal-block support
theorems. It demotes only the stronger claim that Haar/isotropic
representation naturality derives the equal-total-block law.

The residual primitive remains:

```text
derive equal total real-isotype block weights
```

or equivalently derive the normalized no-traceless-source condition

```text
K_TL = 0.
```

