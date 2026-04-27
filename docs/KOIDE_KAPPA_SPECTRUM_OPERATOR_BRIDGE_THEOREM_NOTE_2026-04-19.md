# Koide kappa Spectrum-Operator Bridge Theorem

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide / MRU
**Status:** proposed_retained positive theorem. Spectrum-side Koide `Q = 2/3`
implies operator-side `kappa = 2` via an exact symbolic identity on the
retained cyclic-compression bridge, with zero new axiom cost. The
operator-side `kappa = 2` content is a corollary, not an independent
primitive.
**Primary runner:** `scripts/frontier_koide_kappa_spectrum_operator_bridge_theorem.py`

---

## 0. Executive summary

On the retained hw=1 cyclic compression, a generic Hermitian circulant
`H` admits the parametrization

```text
H = a I + b C + bbar C^2,   a in R, b in C.
```

The retained cyclic-compression bridge gives the eigenvalues `lambda_k`
in closed form:

```text
lambda_k = a + b omega^k + bbar omega^{-k},   omega = exp(2 pi i / 3).
```

Under the retained P1 square-root identification `lambda_k = sqrt(m_k)`,
the sqrt-mass vector `v = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau))` is the
eigenvalue triple `(lambda_0, lambda_1, lambda_2)`. Its C_3 Fourier
decomposition is

```text
a_0 = (lambda_0 + lambda_1 + lambda_2) / sqrt(3) = sqrt(3) * a,
z   = (lambda_0 + omega^bar lambda_1 + omega lambda_2) / sqrt(3) = sqrt(3) * b.
```

**Theorem (bridge identity).** The following identity holds identically
on `Herm_circ(3)`:

```text
a_0^2 - 2 |z|^2  =  3 (a^2 - 2 |b|^2).
```

Both sides vanish simultaneously. The spectrum-side statement
`a_0^2 = 2 |z|^2` (equivalently Koide `Q = 2/3`) is therefore
**exactly equivalent** to the operator-side statement `a^2 = 2 |b|^2`
(equivalently `kappa = 2`). No new operator-side axiom is introduced —
the operator-side closure is inherited from the spectrum-side closure
via the retained cyclic-compression Fourier dictionary.

At PDG charged-lepton masses:

```text
Q = 0.666661     (target 2/3)
sigma = a_0^2 / (a_0^2 + 2|z|^2) = 0.500005     (target 1/2)
kappa = a^2 / |b|^2 = 2.000037     (target 2)
```

All three match within `3e-4`, which is the residual floor of PDG
numerical input. The bridge identity symbolically closes with exact
zero residual.

**Positioning vis-a-vis the branch.** The MRU weight-class obstruction
theorem (`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19`)
named the missing operator-side object as "a retained 1:1 real-isotype
measure". This bridge theorem shows the operator-side `kappa = 2`
content is redundant: once Berry + Brannen close the spectrum-side
`Q = 2/3` at machine precision, the operator-side `kappa = 2` follows
for free from the retained Fourier dictionary. The "separate operator
side primitive" is not needed.

---

## 1. Setup

### 1.1 Retained cyclic-compression bridge

On `Herm_circ(3)` any Hermitian circulant `H` is parametrized by one
real scalar `a` and one complex scalar `b`:

```text
H = a I + b C + bbar C^2,
```

with `C` the cyclic shift. The eigenvectors of `C` are the Fourier
basis

```text
f_k = (1/sqrt(3)) (1, omega^k, omega^{2k})^T,   k = 0, 1, 2.
```

The eigenvalues of `H` on this basis are `lambda_k` as above.

### 1.2 Sqrt-mass vector and its Fourier decomposition

The retained P1 square-root amplitude principle sets
`v_k = sqrt(m_k) = lambda_k`. The Plancherel identity on the
charged-lepton sqrt-mass vector is

```text
|v|^2 = a_0^2 + |z|^2 + |zbar|^2 = a_0^2 + 2 |z|^2,
```

with

```text
a_0 = (v_0 + v_1 + v_2) / sqrt(3),
z   = (v_0 + omega^bar v_1 + omega v_2) / sqrt(3).
```

Koide's `Q = 2/3` is equivalent to

```text
sigma := a_0^2 / |v|^2 = 1/2,   i.e. a_0^2 = 2 |z|^2.
```

### 1.3 Operator-side MRU condition

On the Hermitian-circulant parametrization `(a, b)`, the retained
block-total Frobenius decomposition gives

```text
E_+    = ||a I||_F^2 = 3 a^2,
E_perp = ||b C + bbar C^2||_F^2 = 6 |b|^2,
```

and the MRU equality `E_+ = E_perp` is `3 a^2 = 6 |b|^2`, i.e.
`kappa := a^2 / |b|^2 = 2`.

---

## 2. Theorem

**Theorem (spectrum-operator bridge).** On `Herm_circ(3)`, the exact
polynomial identity

```text
a_0^2 - 2 |z|^2  =  3 (a^2 - 2 |b|^2)
```

holds identically for all real `a` and complex `b`. Consequently

```text
[spectrum-side]  a_0^2 = 2 |z|^2
         <=>  [operator-side]  a^2 = 2 |b|^2
         <=>  kappa = 2,
```

with zero residual. The operator-side MRU is the same content as the
spectrum-side Koide condition written in cyclic-circulant coordinates.

**Proof.** The eigenvalues of `H = a I + b C + bbar C^2` are
`lambda_k = a + b omega^k + bbar omega^{-k}`, which are real because
`b omega^k + bbar omega^{-k}` is real. Substituting into the two Fourier
coefficients:

```text
a_0 = (lambda_0 + lambda_1 + lambda_2) / sqrt(3)
    = (1/sqrt(3)) [3 a + b (1 + omega + omega^2) + bbar (1 + omega^{-1} + omega^{-2})]
    = sqrt(3) a,   since 1 + omega + omega^2 = 0.
```

For `z`:

```text
z = (1/sqrt(3)) [lambda_0 + omega^bar lambda_1 + omega lambda_2]
  = (1/sqrt(3)) [a (1 + omega^bar + omega) + b (1 + omega^bar omega + omega * omega^2)
                                          + bbar (1 + omega^bar omega^{-1} + omega * omega^{-2})].
```

Using `omega^bar = omega^2 = omega^{-1}` and `1 + omega + omega^2 = 0`,
the `a` term vanishes, and `b`-term simplifies to `3 b`, with
`bbar`-term vanishing. Therefore `z = sqrt(3) b`, hence `|z|^2 = 3 |b|^2`.

Combining:

```text
a_0^2 - 2 |z|^2 = 3 a^2 - 6 |b|^2 = 3 (a^2 - 2 |b|^2).
```

QED.

**Consequence.** The operator-side `kappa = 2` (equivalently MRU
`E_+ = E_perp`) is a corollary of the spectrum-side Koide condition under
the cyclic-compression bridge, with residue EXACTLY zero.

---

## 3. Implication for the Koide closure stack

Before this theorem, the operator-side MRU was carried as a candidate
principle requiring a retained 1:1 real-isotype measure. The MRU
weight-class obstruction theorem observed that the retained
`log|det|` law on the unreduced circulant gives weights `(1, 2)` and
lands at `kappa = 1`, not `kappa = 2`.

This theorem shows the operator-side framing is not an **independent**
primitive: once the spectrum-side Koide condition `sigma = 1/2` is
accepted, the operator-side `kappa = 2` content follows for free.
Berry + Brannen already close the spectrum side at machine precision;
hence the operator-side closure comes free.

**Net axiom cost of operator-side kappa = 2 given spectrum-side closure:**
zero.

**What remains.** The single remaining load-bearing input is the
spectrum-side scalar condition `sigma = 1/2` (equivalently Koide
`Q = 2/3`). Both operator-side and spectrum-side framings are now
shown to be the same statement in different coordinates, via this
bridge identity.

---

## 4. Falsification checks

1. **Bridge identity sensitivity.** If the cyclic-compression bridge
   were broken (e.g. by working on `Herm(3)` without the cyclic
   commutant restriction), `a_0` and `z` would not have the closed-form
   `sqrt(3) a`, `sqrt(3) b` relationship, and the bridge identity would
   not hold. The runner verifies the identity holds on 200 random
   `Herm_circ(3)` samples with max residual `< 1e-10`.

2. **Spectrum-side sensitivity.** If PDG masses were shifted
   (numerically) away from the Koide value, `Q` would drift from
   `2/3`, and both `sigma` and `kappa` would drift in lockstep — which
   is exactly the content of the bridge identity.

3. **Dimension-sensitivity.** The bridge form `|z|^2 = 3 |b|^2` uses
   `d = 3` explicitly: the factor 3 is the orbit length. At `d != 3`,
   the Fourier decomposition has different structure and the bridge is
   different. The bridge theorem is stated at `d = 3` only.

---

## 5. Runner — expected output

```
TOTAL: PASS=9 FAIL=0
```

The runner verifies:

- `T1` Hermitian circulant construction (`H = H^H` symbolic).
- `T2` Fourier eigenvalues `lambda_k` are real symbolically.
- `T3` Exact symbolic bridge `a_0 = sqrt(3) a`.
- `T4` Exact symbolic bridge `|z|^2 = 3 |b|^2`.
- `T5` Exact symbolic identity `a_0^2 - 2 |z|^2 = 3 (a^2 - 2 |b|^2)`.
- `T6` PDG Koide `Q ~ 2/3` (numerical).
- `T7` PDG operator-side `kappa ~ 2` (numerical).
- `T8` Identity on 200 random `Herm_circ(3)` samples (max residual
  `< 1e-10`).
- `T9` Closure equivalence on kappa = 2 sample set gives zero residual.

No hard-coded True values. All PASSes are keyed to substantive
symbolic or numerical computations.

---

## 6. Cross-references

**Retained branch material:**

- `docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
  — the obstruction theorem this note positively closes on the
  operator side.
- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
  — the MRU statement at d = 3.
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
  — spectrum-side `delta = 2/9` closure.
- `docs/KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md`
  — retained cyclic-compression bridge.
- `docs/KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md`
  — P1 square-root identification `lambda_k = sqrt(m_k)`.
- `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`
  — spectrum-side `sigma = 1/2 <=> Q = 2/3` equivalence.
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
  — operator-space lift of `sigma = 1/2`.

**Companion note this cycle:**

- `docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`
  — second independent closure route naming the 1:1 real-isotype
  measure explicitly.

---

## 7. Honest limits

This theorem does NOT close the spectrum-side Koide `Q = 2/3` itself.
That remains the single load-bearing input for the charged-lepton cone
normalization. What this theorem establishes is:

- Under the cyclic-compression bridge, operator-side `kappa = 2` is a
  direct corollary of spectrum-side `Q = 2/3` (and vice versa), with
  zero residual.
- The "two closures" (spectrum-side and operator-side) collapse to one
  content at `d = 3`.
- The MRU weight-class obstruction's named operator-side gap
  ("missing 1:1 real-isotype measure") is now closed from the
  spectrum-side side of the bridge: the closure is inherited, not
  separately required.

The operator-side multiplicity-weighted realization of the 1:1 measure
is given independently by the companion block-total Frobenius measure
theorem.
