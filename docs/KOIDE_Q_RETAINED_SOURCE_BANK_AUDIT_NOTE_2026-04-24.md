# Koide Q Retained Source-Bank Audit

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the charged-lepton
`Q = 2/3` bridge but does not close it.
**Primary runner:** `scripts/frontier_koide_q_retained_source_bank_audit.py`

---

## 1. Question

After the trace/Lagrange-multiplier reduction and the block-exchange
obstruction, the `Q` bridge is the single scalar condition

```text
K_TL = 0
```

on the normalized first-live second-order carrier.

This audit asks whether the source classes already retained in the
charged-lepton package force that condition.

Answer:

```text
No.
```

---

## 2. Audit Buckets

### 2.1 Normalized `C_3`-Equivariant Block Sources

The exact normalized source relation gives

```text
Y = diag(y, 2-y),
K_TL(y) = (1-y)/(y(2-y)).
```

The condition `K_TL = 0` has the unique solution `y = 1`, but the source
class itself admits all `0 < y < 2`. So `C_3`-equivariant block sources
leave the same one scalar free.

### 2.2 Weighted Character Sources

The retained weighted character-source class has the exact form

```text
S_(mu,nu) = diag(mu_0 nu_0, mu_1 nu_2, mu_2 nu_1).
```

If the largest diagonal entry is unique, the selected ray is a basis axis and
has

```text
Q = 1,
```

not `2/3`. If the top is degenerate, the class does not select a unique ray.
Thus this class cannot force the Koide point.

### 2.3 Full Taste-Cube Descent

The full-cube source descent is valuable but does not close the value law. It
proves the physical `C^8` carrier descends exactly to the same cyclic channels

```text
B0, B1, B2.
```

Those channels are independent, and the normalized `Q` coordinate remains a
function of the same response ratio:

```text
Y_+ = 2(r0^2/3) / (r0^2/3 + (r1^2+r2^2)/6).
```

The Koide point is the special relation

```text
r1^2 + r2^2 = 2 r0^2.
```

The descent supplies the carrier. It does not supply that value law.

### 2.4 Democracy / Source-Free Law

Real-irrep block democracy and the source-free law are exact conditional
closures:

```text
E_+ = E_perp
<=> K_TL = 0
<=> Q = 2/3.
```

But adopting democracy or source-freeness is exactly adopting the missing
primitive. It is not a derivation from earlier retained source grammar.

---

## 3. Review Consequence

The source-bank audit does not promote Koide `Q` closure.

It shows that the current retained source classes fall into four buckets:

- leave `K_TL` free;
- select axes or degenerate families rather than the Koide ray;
- provide the exact cyclic carrier but no value law;
- close only by assuming the same democracy/source-free primitive.

Therefore the next irreducible `Q` target remains:

```text
derive K_TL = 0
```

from a new retained charged-lepton source grammar or an anomaly/gauge theorem
that acts directly on the normalized traceless source.

---

## 4. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_retained_source_bank_audit.py
```

Result:

```text
PASSED: 12/12
KOIDE_Q_RETAINED_SOURCE_BANK_AUDIT_NO_GO=TRUE
Q_SOURCE_BANK_EXHAUSTION_CLOSES_Q=FALSE
```

---

## 5. Boundary

This note is not a closure theorem. It is a source-bank no-go/triage theorem.
The charged-lepton package remains open:

- `Q = 2/3` still needs a physical no-traceless-source law;
- `delta = 2/9` still needs the physical Brannen Berry/APS bridge;
- the charged-lepton scale `v0` remains a separate support lane.
