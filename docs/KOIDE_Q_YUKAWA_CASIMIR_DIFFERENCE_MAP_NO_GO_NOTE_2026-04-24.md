# Koide Q Yukawa Casimir-Difference Map No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This audits the strongest A1/Yukawa
candidate and rejects promoting the Casimir-difference arithmetic to Koide
closure without an amplitude-map theorem.
**Primary runner:** `scripts/frontier_koide_q_yukawa_casimir_difference_map_no_go.py`

---

## 1. Question

The strongest A1/Yukawa route observes:

```text
T(T+1) - Y^2 = 1/2
```

for the lepton `SU(2)_L` doublet and the Higgs, uniquely among the checked
Yukawa-relevant Standard Model representations.

The tempting closure theorem is:

```text
|b|^2/a^2 = T(T+1) - Y^2.
```

Since the Koide radius is equivalent to:

```text
|b|^2/a^2 = 1/2,
```

this would close `Q`.

The executable answer is:

```text
The arithmetic is exact support, but the amplitude map is not derived.
```

---

## 2. Exact Support Arithmetic

For the lepton/Higgs doublet:

```text
T = 1/2,
|Y| = 1/2.
```

Therefore:

```text
T(T+1) = 3/4,
Y^2 = 1/4,
T(T+1) + Y^2 = 1,
T(T+1) - Y^2 = 1/2.
```

The sum is the `C_tau = 1` support used in the radiative tau lane. The
difference is exactly the A1/Koide amplitude ratio if the amplitude map is
supplied.

---

## 3. Why This Does Not Close Q

Let

```text
rho = |b|^2/a^2.
```

Then:

```text
Q(rho) = (1 + 2 rho)/3,
K_TL(rho) = rho/2 - 1/(8 rho).
```

So:

```text
rho = 1/2
<=> Q = 2/3
<=> K_TL = 0.
```

The missing theorem is not the Casimir arithmetic. It is the physical map:

```text
rho = T(T+1) - Y^2.
```

Standard same-sign gauge/radiative weights naturally produce:

```text
g2^2 T(T+1) + g1^2 Y^2.
```

The difference requires a relative sign or asymmetric measure:

```text
g2^2 T(T+1) - g1^2 Y^2.
```

That sign/asymmetry is not currently retained.

---

## 4. Countermaps

Several retained scalar maps are algebraically available:

```text
rho = T(T+1) - Y^2 = 1/2 -> Q = 2/3
rho = T(T+1) + Y^2 = 1   -> Q = 1
rho = Y^2 = 1/4          -> Q = 1/2
```

Only the first is Koide. Choosing it is exactly the amplitude-map lemma.

A general linear map

```text
rho = alpha T(T+1) + beta Y^2
```

lands on Koide only after imposing one coefficient equation:

```text
alpha = (2 - beta)/3.
```

---

## 5. Falsifiers

This no-go would be falsified by a retained electroweak or Clifford theorem
deriving:

```text
|b|^2/a^2 = T(T+1) - Y^2
```

for the charged-lepton cyclic amplitude, with exact normalization and without
using `Q = 2/3` or `K_TL = 0` as input.

It would also be falsified by a retained asymmetric measure, Wess-Zumino, or
topological sector that explains why the `SU(2)_L` and `U(1)_Y` contributions
enter the amplitude ratio with opposite signs.

No such theorem is currently retained.

---

## 6. Reviewer Objections Answered

**Objection:** The exact `1/2` is too specific to ignore.

**Answer:** It is strong support and should be kept. The no-go rejects only
the closure promotion without the amplitude-map theorem.

**Objection:** The tau radiative lane already derives a charged-lepton
Yukawa scalar.

**Answer:** That lane uses the same-sign sum `C_tau = 1` and supports scale.
The Koide radius needs the difference and a map to the cyclic amplitude ratio.

---

## 7. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_yukawa_casimir_difference_map_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_YUKAWA_CASIMIR_DIFFERENCE_MAP_NO_GO=TRUE
Q_YUKAWA_CASIMIR_DIFFERENCE_MAP_CLOSES_Q=FALSE
RESIDUAL_SCALAR=rho_amp_minus_TTplus1_minus_Y2_equiv_K_TL
RESIDUAL_MAP=rho_amp_minus_TTplus1_minus_Y2_equiv_K_TL
```

---

## 8. Boundary

This note does not demote the Yukawa Casimir-difference observation. It marks
it as one of the strongest support clues for a future positive closure.

The residual primitive remains:

```text
derive the amplitude map rho = T(T+1) - Y^2
```

equivalently:

```text
derive K_TL = 0.
```
