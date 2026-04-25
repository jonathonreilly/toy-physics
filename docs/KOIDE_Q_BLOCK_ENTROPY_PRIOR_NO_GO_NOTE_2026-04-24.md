# Koide Q Block-Entropy Prior No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the block-democracy /
max-entropy route but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_block_entropy_prior_no_go.py`

---

## 1. Theorem Attempt

The block-democracy route can be written as a maximum-entropy statement on the
two retained block probabilities:

```text
p_+    = E_+/(E_+ + E_perp),
p_perp = E_perp/(E_+ + E_perp).
```

The tempting closure upgrade is:

> max entropy over the retained `C_3` block data forces `p_+ = p_perp = 1/2`,
> hence `E_+ = E_perp`, hence `Q = 2/3`.

The executable result is negative.

Max entropy needs a prior/coarse-graining. The A1 value follows only after
choosing the equal-real-isotype-block prior.

---

## 2. Radius Coordinates

For a Hermitian circulant amplitude operator

```text
Y = a I + b C + bbar C^2,
```

the retained Frobenius block energies are:

```text
E_+    = 3 a^2,
E_perp = 6 |b|^2.
```

With Brannen radius

```text
c = 2|b|/a,
```

the runner verifies:

```text
E_perp/E_+ = c^2/2,
kappa = a^2/|b|^2 = 2/(E_perp/E_+),
Q = (1 + E_perp/E_+)/3.
```

Thus the Koide radius law is equivalent to:

```text
E_perp/E_+ = 1
<=> c^2 = 2
<=> kappa = 2.
```

---

## 3. Entropy With A Prior

Let the entropy prior on the two coarse-grained blocks be:

```text
(pi_+, pi_perp).
```

Maximizing relative entropy

```text
S = -p log(p/pi_+) - (1-p) log((1-p)/pi_perp)
```

gives:

```text
p_+* = pi_+/(pi_+ + pi_perp),
p_perp* = pi_perp/(pi_+ + pi_perp).
```

Therefore the entropy-selected radius law is:

```text
E_perp/E_+ = pi_perp/pi_+,
c^2 = 2 pi_perp/pi_+,
kappa = 2 pi_+/pi_perp,
Q = (pi_+ + pi_perp)/(3 pi_+).
```

So entropy alone does not select the Koide radius. It returns the chosen prior.

---

## 4. Exact Counterexamples

The runner checks several retained-compatible coarse grainings:

```text
uniform real isotype blocks  (1,1) -> c^2=2, kappa=2, Q=2/3
uniform complex characters   (1,2) -> c^2=4, kappa=1, Q=1
singlet-heavy two-to-one      (2,1) -> c^2=1, kappa=4, Q=1/2
matrix real-dimension count   (3,6) -> c^2=4, kappa=1, Q=1
```

The A1 value is selected only by the equal-real-isotype-block prior:

```text
(pi_+, pi_perp) = (1,1).
```

That prior is exactly the block-democracy primitive in entropy language.

---

## 5. Review Consequence

The existing block-democracy max-entropy support runner is valid as a
conditional theorem:

```text
equal real-isotype-block prior -> c^2 = 2 -> Q = 2/3.
```

It does not prove:

```text
retained C_3/Herm_circ(3) data -> equal real-isotype-block prior.
```

Uniform over two real isotype blocks, uniform over three complex characters,
and uniform over real matrix dimensions are all natural enough to require an
extra physical rule choosing between them.

Thus the missing primitive has been renamed, not removed:

```text
equal_real_isotype_block_prior
equiv c^2 = 2
equiv kappa = 2
equiv K_TL = 0.
```

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_block_entropy_prior_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_BLOCK_ENTROPY_PRIOR_NO_GO=TRUE
Q_BLOCK_ENTROPY_MAXENT_CLOSES_Q=FALSE
RESIDUAL_PRIMITIVE=equal_real_isotype_block_prior_equiv_c^2=2_equiv_K_TL=0
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used.

---

## 7. Boundary

This note does not demote:

- the real-irrep-block democracy support theorem;
- the AM-GM block-total functional identity;
- the use of entropy as motivation for a possible retained primitive.

It rejects only the stronger claim that max entropy derives the Koide radius
from retained `C_3` data without an extra prior/coarse-graining law.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0` or an
  equivalent retained radius/source/prior theorem;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
