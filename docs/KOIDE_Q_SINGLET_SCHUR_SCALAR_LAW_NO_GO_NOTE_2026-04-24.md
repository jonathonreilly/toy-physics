# Koide Q Singlet-Schur Scalar-Law No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects a retained
`C_3` singlet/baryon Schur extension as a derivation of the normalized
charged-lepton `K_TL = 0` source law.
**Primary runner:** `scripts/frontier_koide_q_singlet_schur_scalar_law_no_go.py`

---

## 1. Question

After the normalized trace reduction, the live `Q` primitive is one scalar:

```text
K_TL = 0.
```

A possible new route is to enlarge the charged triplet by a retained
`C_3`-singlet or baryon-like auxiliary mode, then integrate it out. The
closure hope is:

```text
C_3 singlet extension + Schur reduction
-> equal effective singlet/doublet sources
-> K_TL = 0.
```

The executable answer is:

```text
No.
```

The Schur correction shifts only the trivial Fourier block. It introduces a
new scalar `lambda`, and `K_TL = 0` becomes one equation fixing `lambda`.
That is a reparameterization of the missing law, not a derivation.

---

## 2. Exact Schur Form

Let

```text
P_plus = J/3,
P_perp = I - J/3,
```

where `J = 11^T` is the retained `C_3` trivial-mode matrix. A general
two-block source is

```text
S = s_plus P_plus + s_perp P_perp.
```

A retained `C_3` singlet Schur correction has the form

```text
S_eff = S - lambda J.
```

Since `J = 3P_plus`, the effective coefficients are exactly:

```text
s_plus_eff = s_plus - 3 lambda,
s_perp_eff = s_perp.
```

Therefore the normalized traceless-source residual is:

```text
rho_singlet = s_plus - 3 lambda - s_perp.
```

---

## 3. Why This Does Not Close Q

The condition `K_TL = 0` is equivalent here to:

```text
rho_singlet = 0
<=> lambda = (s_plus - s_perp)/3.
```

But the retained singlet extension does not derive that value of `lambda`.
Exact retained choices can sit below, on, or beyond the neutral point:

```text
s_plus = 2, s_perp = 1, lambda = 0   -> rho_singlet = 1
s_plus = 2, s_perp = 1, lambda = 1/3 -> rho_singlet = 0
s_plus = 2, s_perp = 1, lambda = 1   -> rho_singlet = -2
```

Only the middle line lands on the Koide/source-neutral leaf, and it does so by
choosing the required Schur scalar.

---

## 4. Positivity Is Not Enough

If the auxiliary singlet is positive, a typical Schur coefficient has the
form:

```text
lambda = |beta|^2 / epsilon >= 0.
```

This supplies a sign restriction. It does not supply:

```text
lambda = (s_plus - s_perp)/3.
```

Indeed, if `s_plus < s_perp`, the required neutralizing `lambda` is negative
and cannot be produced by a positive singlet energy. Positivity restricts the
route; it does not select the Koide value.

---

## 5. Falsifiers

This no-go would be falsified by a retained microscopic theorem for the
singlet extension that derives

```text
lambda = (s_plus - s_perp)/3
```

from charged-lepton dynamics without using the target `K_TL = 0`.

It would also be falsified by a physical law fixing the auxiliary coupling
`beta` and singlet energy `epsilon` so that their Schur quotient equals the
pre-Schur source mismatch for all retained charged-lepton sources.

No such theorem is present in the current retained package.

---

## 6. Reviewer Objections Answered

**Objection:** A singlet Schur complement is a new physical carrier, not a
repeat of plain `C_3`.

**Answer:** Correct, and the runner includes it. The new carrier shifts the
trivial block only; the required shift magnitude remains free.

**Objection:** Integrating out a positive singlet might naturally cancel the
traceless source.

**Answer:** Positivity gives `lambda >= 0`, not the exact scalar
`(s_plus - s_perp)/3`. In some source regions the required cancellation even
has the wrong sign.

---

## 7. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_singlet_schur_scalar_law_no_go.py
```

Result:

```text
PASS=12 FAIL=0
SINGLET_SCHUR_FORCES_K_TL=FALSE
KOIDE_Q_SINGLET_SCHUR_SCALAR_LAW_CLOSES_Q=FALSE
RESIDUAL_SCALAR=rho_singlet=s_plus-3*lambda-s_perp
```

---

## 8. Boundary

This note does not reject singlet/baryon extensions as future source
mechanisms. It rejects only the stronger claim that the currently retained
`C_3` Schur form already derives the no-traceless-source law.

The residual primitive remains:

```text
derive K_TL = 0
```

or, in this extension,

```text
derive rho_singlet = 0.
```

