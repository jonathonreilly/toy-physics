# Koide Q Controlled-C3-Breaking No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the controlled
charged-lepton-specific `C_3` breaking escape hatch but does not close
charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_controlled_c3_breaking_no_go.py`

---

## 1. Theorem Attempt

The full-lattice Schur-inheritance note leaves a genuine escape hatch:

```text
controlled charged-lepton-specific breaking of strict C_3[111] covariance.
```

The tempting closure upgrade is:

> controlled `C_3` breaking derives the missing normalized traceless source law
> `K_TL = 0`.

The executable result is negative.

Controlled breaking supplies a real `C_3` doublet direction and magnitude. The
charged-lepton Koide quotient depends only on the doublet radius. A direction
law, averaging law, or generic breaking action does not set that radius to the
A1 value without an additional value law.

---

## 2. Exact Carrier Decomposition

On the normalized real three-slot square-root amplitude carrier, write

```text
lambda = (1,1,1) + alpha (2,-1,-1) + beta (0,1,-1).
```

Then the runner verifies exactly:

```text
sum_i lambda_i = 3,
sum_i lambda_i^2 = 3 + (3/2)c^2,
c^2 = 4 alpha^2 + (4/3) beta^2.
```

Therefore

```text
Q = (sum_i lambda_i^2)/(sum_i lambda_i)^2
  = 1/3 + c^2/6.
```

The `C_3` generator rotates `(alpha,beta)` but preserves `c^2`. Thus the
doublet phase/direction is not the `Q` value.

---

## 3. Symmetry Restoration Is Not Koide

Averaging over the three `C_3` images gives:

```text
(lambda + C lambda + C^2 lambda)/3 = (1,1,1),
Q_average = 1/3.
```

So strict symmetry restoration kills the doublet. It does not derive the
Koide value. To get nontrivial hierarchy, the charged-lepton lane needs a
nonzero doublet radius; the question is what fixes that radius.

---

## 4. Explicit Breaking Source

For an exact controlled-breaking source

```text
S = (mu/2)c^2 - h1 alpha - h2 beta,
```

stationarity gives

```text
alpha* = h1/(4 mu),
beta*  = 3 h2/(4 mu),
c^2*   = (h1^2 + 3 h2^2)/(4 mu^2).
```

Hence

```text
Q* = 1/3 + (h1^2 + 3 h2^2)/(24 mu^2).
```

The Koide leaf would require:

```text
h1^2 + 3 h2^2 = 8 mu^2.
```

That is a new source-strength law, not a consequence of controlled breaking
itself.

Exact countervalues from the same source form are:

```text
h1 = 2 mu,        h2 = 0 -> c^2 = 1, Q = 1/2
h1 = 2 sqrt(2)mu, h2 = 0 -> c^2 = 2, Q = 2/3
h1 = 4 mu,        h2 = 0 -> c^2 = 4, Q = 1
```

Only the middle line is the Koide leaf, and it is selected by the source
strength.

---

## 5. Spontaneous-Breaking Coefficients

The same issue appears in the generic `C_3`-invariant Landau form on the
doublet radius:

```text
S(c^2) = A c^2 + B c^4.
```

The nonzero stationary radius is:

```text
c^2 = -A/(2B).
```

The Koide leaf would require:

```text
A + 4B = 0.
```

Again the missing object is a coefficient-ratio theorem. A spontaneous
breaking mechanism can produce a nonzero doublet, but it does not by itself
derive the charged-lepton radius.

---

## 6. Normalized Source Reading

On the normalized second-order carrier, the breaking radius is the block-power
ratio:

```text
E_perp/E_+ = c^2/2,
Y = diag(2/(1+c^2/2), 2(c^2/2)/(1+c^2/2)).
```

The exact dual-source difference satisfies:

```text
K_+ - K_perp = (c^2 - 2)(c^2 + 2)/(4 c^2).
```

Thus:

```text
K_TL = 0
<=> c^2 = 2
<=> E_+ = E_perp
<=> kappa = 2
<=> Q = 2/3.
```

Controlled `C_3` breaking has not removed the missing primitive; it has
localized it as the controlled-breaking radius law.

---

## 7. Review Consequence

The controlled-breaking route proves:

```text
a charged-lepton-specific C_3-breaking doublet can parameterize the observed
kind of hierarchy.
```

It does not prove:

```text
retained Cl(3)/Z^3 charged-lepton structure -> c^2 = 2.
```

The residual scalar is:

```text
controlled_breaking_radius_c^2=2
equiv K_TL = 0.
```

So this route cannot be promoted as a Koide closeout unless a retained theorem
fixes the breaking-source strength or Landau coefficient ratio.

---

## 8. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_controlled_c3_breaking_no_go.py
```

Result:

```text
PASSED: 16/16
KOIDE_Q_CONTROLLED_C3_BREAKING_NO_GO=TRUE
Q_CONTROLLED_C3_BREAKING_CLOSES_Q=FALSE
RESIDUAL_RADIUS_LAW=controlled_breaking_radius_c^2=2_equiv_K_TL=0
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used as an input.

---

## 9. Boundary

This note does not demote:

- the full-lattice Schur-inheritance theorem;
- the possibility that a future retained charged-lepton-specific breaking
  theorem could close the radius;
- the selected-line Brannen phase lane for `delta`.

It rejects only the stronger claim that controlled `C_3` breaking itself
derives the Koide radius.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0` or an
  equivalent retained radius/source/coefficient theorem;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
