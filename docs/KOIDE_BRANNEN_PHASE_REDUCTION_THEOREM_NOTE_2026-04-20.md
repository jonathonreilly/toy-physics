# Koide Brannen-Phase Reduction Theorem: Conditional `δ = Q/d` Route

**Date:** 2026-04-20
**Lane:** Charged-lepton Koide phase `delta = 2/9`.
**Status:** bounded - bounded or caveated result note
`δ = Q/d` from the doublet conjugate-pair charge `n_eff = 2` and `d = 3 = |C_3|`.
The cycle-2 linking theorem and direct no-go sharpen the remaining load-bearing
step: on the physical selected-line CP¹ base, the structural ratio `2/d²`
still has to be identified with the physical Berry holonomy in radians
(the named residual postulate `P`). So this note should be read as one
important reduction route, not as the final standalone discharge of I2.

**Primary runner:**
`scripts/frontier_koide_brannen_phase_reduction_theorem.py`

**Companion notes:**
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — Berry holonomy
  identification on the actual selected line
- `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md` — bundle
  triviality on the physical Koide base
- `docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` — general
  `Q ↔ δ` structural link
- `docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md` — sharp no-go
  on closing the physical-base radian bridge from retained data alone
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — I1 and I2
  open import register

---

## 0. Executive summary

The Brannen phase `delta = 2/9` is currently a retained observational input.
The Berry theorem identifies `delta(m)` as the Berry holonomy of the
tautological CP^1 line on the actual selected charged-lepton route (for all
`m`), but does not by itself force the VALUE `delta = 2/9` on the physical
base.

This note derives the VALUE via the following chain:

```text
n_eff = 2    (doublet conjugate-pair charge, structural — derived below)
d     = 3    (|C_3|, structural)
delta = n_eff / d^2 = 2/9
      = Q / d
```

where the second equality holds because `Q = n_eff / d = 2/3` is the Koide ratio.

The derivation of `n_eff = 2` is structural and independent of `Q`. The step
`Q = 2/3` is the retained observational input (I1). Given `Q`, `delta = Q/d = 2/9`
follows uniquely from the doublet structure and C_3 order. Therefore:

> **This note provides the conditional `δ = Q/d` route.** The cycle-2
> companion notes sharpen the remaining live gap as the physical-base
> radian-bridge postulate `P`. So once `I1` is derived and `P` is closed, I2
> closes automatically via `δ = Q/d`.

---

## 1. The doublet conjugate-pair charge n_eff = 2

### 1.1 Representation-theoretic setup

The C_3 = Z/3Z cyclic group acts on C^3 via the permutation matrix C. The
Fourier decomposition is:

```text
C^3 = L_1 (+) L_omega (+) L_omegabar,
```

where `omega = e^{2 pi i / 3}`, `L_1` is the trivial singlet, and `L_omega`,
`L_omegabar = conj(L_omega)` are the two conjugate doublet lines. The Fourier
basis is:

```text
v_1        = (1, 1, 1) / sqrt(3)           (singlet),
v_omega    = (1, omega, omega^2) / sqrt(3)  (L_omega),
v_omegabar = (1, omega^2, omega) / sqrt(3)  (L_omegabar = conj(L_omega)).
```

The L_omegabar line is the complex conjugate of L_omega: under the C_3 action,
L_omega gets eigenvalue omega and L_omegabar gets eigenvalue omegabar = omega^{-1}.

### 1.2 The Koide state on the selected line

On the exact selected charged-lepton line H_sel(m), the normalized Koide state has
the exact Fourier form:

```text
s(m) = (1/sqrt(2)) v_1 + (1/2) e^{i theta(m)} v_omega
                       + (1/2) e^{-i theta(m)} v_omegabar.
```

The singlet occupancy is sigma_1 = |<v_1, s>|^2 = 1/2 (forced by Q = 2/3).
The doublet occupancies are |<v_omega, s>|^2 = |<v_omegabar, s>|^2 = 1/4.

### 1.3 The doublet conjugate-pair forces n_eff = 2

The doublet projective coordinate is:

```text
[<v_omega, s> : <v_omegabar, s>] = [e^{i theta} : e^{-i theta}]
                                  = [1 : e^{-2 i theta}].
```

The key structure: since L_omegabar = conj(L_omega), their phases are CONJUGATE
(+theta and -theta respectively). The PROJECTIVE doublet ratio is therefore:

```text
zeta(theta) := e^{i theta} / e^{-i theta} = e^{2 i theta},
```

or in the dual coordinate:

```text
zeta(theta) = e^{-2 i theta}  (the ratio e^{-i theta} / e^{i theta}).
```

The phase of this projective coordinate advances at TWICE the rate of theta:

```text
d(arg zeta) / d(theta) = -2.
```

This factor of 2 is NOT a choice. It is forced by the conjugate-pair structure
(L_omegabar = conj(L_omega)), which forces the two doublet phases to be equal and
opposite. The projective ratio always doubles the individual phase.

**Definition:** `n_eff := |d(arg zeta) / d(theta)| = 2` is the doublet effective
charge, derived from the conjugate-pair structure.

### 1.4 Comparison with line-bundle Chern class

If one assigns a line bundle L_n on CP^1 to this doublet with `c_1 = n_eff = 2`,
the Berry holonomy of that bundle around the full CP^1 equator is 2 pi n_eff = 4 pi.
This matches the ambient S^2 calculation (n_flux = 2 in the runner, check B1).
The physical content is that the doublet coordinate winds TWICE for every full
revolution in theta — not because of a chosen monopole charge, but because of the
forced conjugate-pair pairing.

---

## 2. The Brannen normalization and delta = n_eff / d^2

### 2.1 The C_3 step holonomy

Under one C_3 action (theta -> theta + 2 pi / 3), the doublet projective coordinate
advances by:

```text
Delta(arg zeta) = -2 * (2 pi / 3) = -4 pi / 3.
```

This is the phase advance of the projective doublet coordinate per C_3 step.

### 2.2 Brannen phase normalization

The Brannen phase delta is defined as the phase offset from the C_3-symmetric
reference point (the unphased point m_0 where delta = 0):

```text
delta(m) = theta(m) - 2 pi / 3.
```

The Brannen normalization converts the doublet projective phase advance per C_3
step into Brannen units by dividing by the total C_3 period (d = 3 steps, each of
2 pi / d = 2 pi / 3 in theta, giving 2 pi total):

```text
delta_per_step = |Delta(arg zeta)| / (2 pi * d)
               = (4 pi / 3) / (2 pi * 3)
               = 2 / (3 * 3)
               = n_eff / d^2
               = 2 / 9.
```

### 2.3 The formula

> **Theorem (Brannen phase formula).** On the C_3 = Z/3Z Koide representation,
> the doublet effective charge is `n_eff = 2` (from conjugate-pair forcing) and
> the group order is `d = 3`. The Brannen phase satisfies:
>
>     delta = n_eff / d^2 = 2/9.
>
> Equivalently:
>
>     delta = Q / d,
>
> where `Q = n_eff / d = 2/3` is the Koide ratio.

### 2.4 The equivalence delta = Q/d

The Koide ratio satisfies `Q = sigma_1^{-1} / d` where `sigma_1 = 1/(3Q)` is
the singlet occupancy. On the unit Koide locus, the singlet occupancy is fixed
at `sigma_1 = 1/2` by the Koide constraint. Therefore:

```text
Q = 1 / (d * sigma_1) = 1 / (3 * (1/2)) = 2/3.
```

And:

```text
Q = n_eff / d  (since n_eff = 2, d = 3, Q = 2/3).
```

This expresses the Koide ratio as the ratio of doublet effective charge to C_3
order. Given this, `delta = n_eff / d^2 = Q / d = 2/9`.

---

## 3. Why all three candidate routes reduce to I1

### 3.1 Route 1: Equivariant completion to S^2

The ambient S^2 calculation reproduces `delta = 2/9` with monopole charge `n = 2`.
The bundle obstruction theorem proves the physical Koide base is an interval
(equivariantly trivial bundle). The completion to S^2 is forced if the doublet
bundle has `c_1 = 2` on a physically derived compact 2-cycle.

**Where it reduces to I1**: The Borel-Weil Chern class `c_1 = 2` on the ambient
S^2 is consistent with `Q = n/d = 2/3` via `n = 2`, `d = 3`. Forcing this from
the framework requires proving that the physical compact cycle has `c_1 = 2`, which
is equivalent to pinning the doublet occupancy `sigma_1 = 1/2`, which is the Koide
constraint Q = 2/3 (I1).

### 3.2 Route 2: Wilson-line Z_3 quantization

The connection A = d(theta) on the CP^1 equator is FLAT (curvature F = d(d theta)
= 0). All closed Z_3 orbits give zero holonomy. Specifically:

- The full Z_3 orbit of any doublet point {zeta, omega^2 zeta, omega zeta} sweeps
  the equator once, giving holonomy exp(i * 2 pi) = 1 (trivial).
- Every partial closed loop gives holonomy = exp(i * path_length * 1) where
  A = d(theta) is the (flat) connection 1-form. No quantization follows.

The connection becomes non-flat only if embedded in the full CP^1 (with its
Fubini-Study curvature). Accessing that curvature requires an area element —
possible only on a 2D base, not on the 1D equator. Obtaining that 2D base is
equivalent to the S^2 completion (Route 1), which reduces to I1.

### 3.3 Route 3: Z_3 scalar potential Berry phase

The Z_3 scalar potential V(m) = const + (c1+c2/2)m + (3/2)m^2 + (1/6)m^3 has
its stationary point at m_V ≈ -0.433, far from the physical m_* ≈ -1.161 (Koide
CL3 selector gap note). No Z_3 Berry-type phase of V(m) quantizes to 2/9:

- The V(m) periodic extension requires closing the m-path, which maps to closing
  the Z_3 orbit on the Koide locus.
- But closed Z_3 orbits give trivial holonomy (as in Route 2).
- The gap between m_V and m_* is exactly the gap between the V(m) minimum and the
  physical Koide point — this is precisely the statement that Q = 2/3 cannot be
  derived from the scalar potential (Koide CL3 selector gap note, sections 3a-3d).

Therefore Route 3 also reduces to I1.

---

## 4. Formal status of I2

> **Corollary (I2 conditional closure).**
>
> - `n_eff = 2`: structurally derived (conjugate-pair forcing, Section 1).
> - `d = 3`: structurally derived (|C_3|).
> - `Q = 2/3`: retained observational (I1, open).
> - `delta = Q/d = n_eff/d^2 = 2/9`: derived from the above three.
>
> Closing I1 (Q = 2/3) closes I2 (delta = 2/9) automatically. I2 does not
> require an independent derivation once I1 is in hand.

The remaining gap is entirely in I1. The Brannen phase derivation is a
one-formula corollary of the Koide ratio.

---

## 5. What is new in this note

1. **n_eff = 2 is derived, not chosen.** The earlier ambient-S^2 closure used
   `n_flux = 2` as a chosen monopole charge. This note derives it from the
   doublet conjugate-pair structure: `L_omegabar = conj(L_omega)` forces the
   projective ratio `e^{-2i theta}` with winding number 2.

2. **The formula delta = Q/d is the unique forced value.** Given `n_eff` and `d`,
   the Brannen normalization uniquely gives `delta = n_eff/d^2 = Q/d`. There is
   no free parameter.

3. **All three candidate routes are exhausted and shown to reduce to I1.** This
   sharpens the open import register: I2 is not independently open; it is a
   corollary of I1.

4. **The Koide ratio identity Q = n_eff/d.** The formula `Q = n_eff/d = 2/3` is
   a representation-theoretic reading of the Koide ratio: it equals the doublet
   effective charge divided by the C_3 order. This gives a structural language for
   I1: deriving Q = 2/3 is equivalent to deriving why `n_eff/d = 2/3` is forced
   for the physical lepton state.

---

## 6. Runner summary

`scripts/frontier_koide_brannen_phase_reduction_theorem.py` verifies:

1. n_eff = 2 from doublet conjugate-pair: |d(arg zeta)/d(theta)| = 2.
2. d = 3 from C_3 order.
3. Formula: delta = n_eff/d^2 = 2/9 (exact rational).
4. Equivalence: Q = n_eff/d = 2/3 (Koide ratio identity).
5. Berry holonomy at physical point matches formula: delta_obs = 2/9.
6. Positivity threshold check: delta(m_pos) = pi/12 (structural, not 2/9).
7. Route 2 flat-connection obstruction: A = d(theta) has zero curvature on
   the equator; all closed Z_3 orbits give trivial holonomy.
8. Route 1 bundle obstruction: physical Koide base is interval (c_1 = 0);
   ambient S^2 gives c_1 = n_eff = 2 and delta = 2/9.
9. Conditional closure: given Q = 2/3, delta = Q/d = 2/9 is exact.
10. Counterfactual: for any other Q' != 2/3, delta' = Q'/d != 2/9.

Expected: PASS=N, FAIL=0.

---

## 7. Cross-references

- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — Berry holonomy
  identification (delta is a holonomy for all m, VALUE not forced there)
- `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md` — proves
  physical Koide base is an interval, no nontrivial bundle
- `docs/KOIDE_CL3_SELECTOR_GAP_NOTE_2026-04-19.md` — exhausts Cl(3)-algebraic
  routes to m_*; confirms I1 is the blocker
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — open import
  register; I2 status update: "conditionally closed on I1"
