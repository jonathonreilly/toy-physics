# Koide Q Real-Structure Neutrality No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This rejects retained real /
antiunitary character conjugation as a derivation of the charged-lepton
`K_TL = 0` source law.
**Primary runner:** `scripts/frontier_koide_q_real_structure_neutrality_no_go.py`

---

## 1. Question

Plain `C_3` symmetry does not force the normalized traceless source to vanish.
A stronger route is to include the retained real structure:

```text
complex conjugation: omega <-> omega^2.
```

The attempted closure is:

```text
C_3 + real/antiunitary neutrality
-> singlet/doublet neutrality
-> K_TL = 0.
```

The executable answer is:

```text
No.
```

The real structure neutralizes the two complex conjugate characters inside
the real doublet. It does not exchange the rank-1 singlet with the rank-2
real doublet, and it does not set their total source weights equal.

---

## 2. Exact Character Structure

The complex `C_3` character projectors split the carrier as:

```text
P0, P_omega, P_omega^2.
```

Complex conjugation fixes `P0` and exchanges the two nontrivial characters:

```text
conj(P0) = P0,
conj(P_omega) = P_omega^2.
```

The retained real doublet is:

```text
P_perp = P_omega + P_omega^2.
```

Thus antiunitary neutrality can remove the `omega` versus `omega^2` splitting.
It cannot remove the `P0` versus `P_perp` ratio.

---

## 3. General Real-Neutral Source

The most general positive source neutral under this real structure is:

```text
S = a P0 + b(P_omega + P_omega^2),
a > 0, b > 0.
```

It is `C_3`-equivariant and real. It still contains one free
singlet-vs-doublet ratio.

In the normalized block-energy coordinate

```text
R = E_perp/E_plus,
```

the retained formulas are:

```text
Q(R) = (1 + R)/3,
K_TL(R) = (R^2 - 1)/(4R).
```

The Koide leaf is the special value:

```text
R = 1.
```

Real-structure neutrality does not derive that value.

---

## 4. Counterexample

The runner checks the explicit retained real-neutral source:

```text
a = 1,
b = 2.
```

It gives:

```text
R = 2,
Q = 1,
K_TL = 3/8.
```

This source is `C_3`-equivariant, invariant under character conjugation, and
off the Koide leaf.

---

## 5. Falsifiers

This no-go would be falsified by a retained antiunitary or real-structure
operation that acts on the quotient as an actual sign flip

```text
K_TL -> -K_TL
```

while preserving the physical carrier.

It would also be falsified by a retained real-structure theorem proving that
total singlet and total real-doublet source weights must be equal, not merely
that the two conjugate complex doublet characters have equal weights.

The present retained real structure proves only the second statement inside
the doublet.

---

## 6. Reviewer Objections Answered

**Objection:** Character conjugation is a real symmetry beyond plain `C_3`.

**Answer:** Correct. It is included. It enforces equality between the
`omega` and `omega^2` character weights, but the singlet weight remains
independent.

**Objection:** A quotient-level swap of two reduced coordinates would fix
`R = 1`.

**Answer:** That swap is not this real structure. The real structure exchanges
two rank-one complex characters inside the rank-two real doublet; it does not
exchange the rank-one singlet with the rank-two doublet.

---

## 7. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_real_structure_neutrality_no_go.py
```

Result:

```text
PASSED: 11/11
KOIDE_Q_REAL_STRUCTURE_NEUTRALITY_NO_GO=TRUE
Q_REAL_STRUCTURE_NEUTRALITY_CLOSES_Q=FALSE
RESIDUAL_RATIO=real_neutral_singlet_doublet_ratio_equiv_K_TL
```

---

## 8. Boundary

This note does not reject the retained real structure. It rejects only the
stronger claim that real/antiunitary neutrality derives the missing
singlet-vs-doublet source ratio.

The residual primitive remains:

```text
derive K_TL = 0
```

from a physical law acting on the singlet-vs-doublet quotient.

