# Koide Q Cl(3) Grade-Involution Even-Source No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects retained `Cl(3)`
grade/chiral parity as a derivation of the normalized charged-lepton
traceless source law.
**Primary runner:** `scripts/frontier_koide_q_cl3_grade_involution_even_source_no_go.py`

---

## 1. Theorem Attempt

The strongest `Cl(3)` parity route is:

> the retained grade involution, or chiral parity, might send the normalized
> traceless source `K_TL` to `-K_TL`, forcing `K_TL = 0`.

The executable result is negative. The admitted Koide carrier is the
first-live second-order carrier. Grade involution flips first-order Clifford
generators but fixes second-order even bilinears. The surviving
singlet/doublet source ratio is therefore grade-even.

---

## 2. Exact Evenness

For first-order Clifford variables:

```text
Gamma_i -> -Gamma_i.
```

The first-live Koide carrier is second order:

```text
Gamma_i^2 -> Gamma_i^2.
```

So both retained second-order blocks are grade invariant:

```text
P_plus Gamma^2  -> P_plus Gamma^2
P_perp Gamma^2  -> P_perp Gamma^2.
```

---

## 3. Source Algebra

A general retained `C_3`-invariant source on the even carrier is:

```text
K = a P_plus + b P_perp.
```

Its trace/traceless decomposition is:

```text
K_trace = (a+b)/2
K_TL    = (a-b)/2.
```

Grade parity acts on Clifford degree. It does not exchange:

```text
P_plus <-> P_perp.
```

Therefore it imposes no equation:

```text
a = b.
```

---

## 4. Counterexample

The runner checks:

```text
a = 1, b = 2.
```

The corresponding source response is grade invariant, but:

```text
K_TL = -1/2 != 0.
```

This is a retained even-source counterexample to the attempted grade-parity
closure.

---

## 5. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or `K_TL = 0` as an assumption. Its failure is
structural:

```text
Cl(3) grade parity -> odd/even Clifford-degree selection
```

but not:

```text
Cl(3) grade parity -> singlet/doublet source neutrality.
```

Using grade parity to force the source law would require an additional
singlet/doublet exchange principle, which is the already named missing
primitive.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_cl3_grade_involution_even_source_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_CL3_GRADE_INVOLUTION_EVEN_SOURCE_NO_GO=TRUE
Q_CL3_GRADE_INVOLUTION_EVEN_SOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=cl3_even_source_ratio_a_minus_b_equiv_K_TL
```

---

## 7. Boundary

This note does not reject the retained `Cl(3)` grade structure. It rejects
only the stronger claim that grade/chiral parity derives:

```text
K_TL = 0
```

on the even second-order Koide carrier.
