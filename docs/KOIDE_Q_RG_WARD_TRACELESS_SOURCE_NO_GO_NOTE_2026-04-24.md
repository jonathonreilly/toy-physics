# Koide Q RG/Ward Traceless-Source No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects retained Ward or
one-dimensional RG fixed-point grammar as a derivation of the normalized
charged-lepton traceless source law.
**Primary runner:** `scripts/frontier_koide_q_rg_ward_traceless_source_no_go.py`

---

## 1. Theorem Attempt

The strongest Ward/RG route is:

> the retained `C_3` Ward identity, or an associated local RG fixed-point
> principle on the normalized source quotient, might force the physical
> charged-lepton scalar `K_TL` to sit at zero.

The executable result is negative. Retained `C_3` leaves the quotient scalar
invariant, so its Ward operator is trivial on `K_TL`. A scalar RG grammar can
place a stable fixed point at any supplied value `c`.

---

## 2. Ward Identity

On the normalized quotient, the traceless source has the form:

```text
K = K_TL Z,
```

where `Z` is the retained singlet-minus-doublet block axis. The retained
cyclic action satisfies:

```text
C_3 K C_3^{-1} = K.
```

Therefore the Ward generator acts trivially on the quotient scalar:

```text
L_C3 K_TL = 0.
```

This proves invariance, not vanishing. A symmetry that leaves a scalar
coordinate fixed cannot derive that the coordinate is zero.

---

## 3. RG Fixed-Point Grammar

The most general local scalar beta-function germ begins:

```text
beta(K_TL) = b0 + b1 K_TL + b2 K_TL^2 + b3 K_TL^3 + ...
```

Then:

```text
beta(0) = b0.
```

Thus `K_TL = 0` is a fixed point only after imposing:

```text
b0 = 0.
```

That coefficient condition is source neutrality in RG language. It is not
derived by the retained Ward grammar.

---

## 4. Off-Koide Counterflow

The runner checks the stable scalar flow:

```text
dK_TL/dt = -(K_TL - c).
```

It has the stable fixed point:

```text
K_TL = c.
```

For example:

```text
c = 1/5
```

is mathematically admissible and gives an off-Koide normalized carrier. The
fixed-point principle alone therefore does not pick the Koide leaf.

---

## 5. Block-Exchange Parity

Imposing the quotient parity

```text
K_TL -> -K_TL
```

would remove even beta terms and force `b0 = 0`. But that parity is precisely
the extra block-exchange/source-neutrality law already identified as not
retained on the rank-1/rank-2 `C_3` carrier.

Using it here would rename the missing primitive.

---

## 6. Hostile Review

This route does not import mass-table data, observational pins, `Q = 2/3`,
`P_Q = 1/2`, `delta = 2/9`, or `K_TL = 0` as an assumption. Its failure is
the retained authority gap:

```text
retained C_3 Ward/RG grammar -> scalar quotient flow
```

but not:

```text
retained C_3 Ward/RG grammar -> c = 0.
```

---

## 7. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_rg_ward_traceless_source_no_go.py
```

Result:

```text
PASSED: 12/12
KOIDE_Q_RG_WARD_TRACELESS_SOURCE_NO_GO=TRUE
Q_RG_WARD_TRACELESS_SOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=c_fixed_point_equiv_K_TL
RESIDUAL_RG_PARAMETER=c_fixed_point_equiv_K_TL
```

---

## 8. Boundary

This note does not reject future microscopic flow mechanisms. It rejects only
the stronger claim that the currently retained Ward/RG grammar already derives:

```text
K_TL = 0.
```

The remaining primitive is an independently retained physical law setting the
quotient fixed-point parameter to:

```text
c = 0.
```
