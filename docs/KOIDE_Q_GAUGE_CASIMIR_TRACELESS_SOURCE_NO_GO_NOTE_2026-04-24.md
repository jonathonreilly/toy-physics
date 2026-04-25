# Koide Q Gauge-Casimir Traceless-Source No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the gauge/anomaly route
to charged-lepton `Q = 2/3` but does not close it.
**Primary runner:** `scripts/frontier_koide_q_gauge_casimir_traceless_source_no_go.py`

---

## 1. Question

The strongest axiom-native-looking `Q` route in the current package is the
Casimir-difference coincidence:

```text
T(T+1) - Y^2 = 1/2
```

for the charged-lepton Yukawa doublet participants. This equals the
Koide/A1 primitive

```text
|b|^2/a^2 = 1/2.
```

After the traceless-source reduction, the Nature-grade question is sharper:

> does retained gauge/Casimir data force the normalized second-order
> traceless source `K_TL` to vanish?

Answer:

```text
No.
```

---

## 2. What Survives

The retained arithmetic is exact and useful:

- the lepton doublet `L` and Higgs `H` are the only listed SM participants
  with `T(T+1)-Y^2 = 1/2`;
- the charged-lepton Casimir sum is
  ```text
  C_tau = T(T+1)+Y^2 = 1;
  ```
- the Casimir difference is
  ```text
  T(T+1)-Y^2 = 1/2.
  ```

This remains strong support for the A1/Koide route.

---

## 3. Why It Does Not Close `Q`

Gauge Casimir data are internal electroweak representation scalars. A
gauge-blind scalar contribution to the normalized two-block source has the
form

```text
K = c I.
```

Its decomposition is

```text
K_trace = c,
K_TL    = 0.
```

But on the normalized carrier `Tr(Y)=2`, `K_trace` is exactly the
Lagrange-multiplier gauge of the trace constraint. It is absorbed by

```text
lambda' = lambda + K_trace.
```

Therefore a scalar Casimir contribution does not select the shape
`Y_+/Y_perp`. It supplies support constants, not a physical value law.

To close `Q`, one must prove the missing map:

```text
|b|^2/a^2 = T(T+1)-Y^2.
```

Equivalently, on the normalized second-order carrier:

```text
gauge/Casimir data force K_TL = 0.
```

That map is exactly the open amplitude-ratio/source-law lemma. It is not
derived by the retained gauge arithmetic alone.

---

## 4. Relation to Existing Gauge No-Go

The result is consistent with the existing `SU(2)_L` gauge-exchange no-go.
Gauge exchange on the retained `hw=1` triplet is species-diagonal and does not
generate the cyclic off-axis data needed to force the Koide cone.

Thus the gauge route currently has the following status:

- exact Casimir support scalars: **yes**;
- exact charged-lepton specificity: **yes**;
- direct theorem forcing `K_TL = 0`: **no**.

---

## 5. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_gauge_casimir_traceless_source_no_go.py
```

Result:

```text
PASSED: 12/12
KOIDE_Q_GAUGE_CASIMIR_TR_SOURCE_NO_GO=TRUE
Q_GAUGE_CASIMIR_CLOSES_Q=FALSE
RESIDUAL_SCALAR=missing_Casimir_to_amplitude_K_TL_map
```

---

## 6. Boundary

This note does not demote the Casimir-difference route as support. It demotes
only the stronger claim that retained gauge/Casimir arithmetic by itself
forces the normalized traceless-source law.

The next irreducible `Q` target remains:

```text
derive K_TL = 0
```

without assuming `K_TL = 0`, `|b|^2/a^2 = 1/2`, `Q = 2/3`, or an unexplained
Casimir-to-amplitude map.
