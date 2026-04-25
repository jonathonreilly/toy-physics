# Koide Q Block-Exchange Rank Obstruction

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This sharpens the `Q = 2/3`
source-law bridge but does not close it.
**Primary runner:** `scripts/frontier_koide_q_block_exchange_rank_obstruction.py`

---

## 1. Question

After the traceless-source reduction, the live `Q` bridge is the one scalar
condition

```text
K_TL = 0.
```

One possible closure route would be a retained symmetry exchanging the singlet
and real-doublet blocks. Such a symmetry would send

```text
K_TL -> -K_TL,
```

and invariance would force `K_TL = 0`.

This note asks whether that block-exchange symmetry exists on the actual
retained three-generation `C_3` carrier.

Answer:

```text
No.
```

---

## 2. Projector Structure

Let

```text
P_+    = J / 3,
P_perp = I - J / 3,
```

where `J` is the all-ones matrix on the three-generation cyclic carrier.
These are exact complementary `C_3`-central projectors:

```text
rank(P_+)    = 1,
rank(P_perp) = 2.
```

The rank mismatch is load-bearing.

No invertible similarity can map `P_+` to `P_perp`, because rank is invariant
under `S P S^(-1)`. No unitary conjugation can exchange them either, because
unitary conjugation preserves rank and trace.

---

## 3. Commutant and Character Algebra

Every matrix commuting with the retained cyclic generator is circulant and
preserves `P_+` and `P_perp` separately. So the `C_3` commutant contains no
internal operation that swaps the two real isotypes.

Equivalently, over the complex character algebra the primitive central
idempotents are

```text
P_0, P_omega, P_omega^2,
```

each rank one, while the real doublet is

```text
P_perp = P_omega + P_omega^2.
```

Automorphisms may permute primitive complex characters, but they cannot map a
single primitive idempotent to a sum of two primitive idempotents. Therefore
the real-isotype exchange

```text
P_+ <-> P_perp
```

is not a `*`-automorphism of the retained `C_3` commutant.

---

## 4. Consequence for the Source Law

The lifted trace/traceless source is

```text
K = K_trace I + K_TL (P_+ - P_perp).
```

A genuine block-exchange symmetry would be exactly the missing sign flip

```text
K_TL -> -K_TL.
```

But the retained carrier has no such exchange symmetry. Thus `K_TL = 0` is
not forced by block exchange on the physical `C_3` carrier.

The formal swap of two coordinates on the reduced two-slot quotient is a
different object. It can be adopted as a quotient-level measure/democracy law,
but it is not inherited from the retained three-generation carrier.

---

## 5. Review Consequence

This closes one of the tempting Nature-grade escape routes negatively:

```text
derive K_TL = 0 from singlet/doublet block exchange
```

does not work on the actual retained carrier.

The remaining `Q` bridge is therefore still:

```text
derive K_TL = 0
```

from some source other than plain `C_3` symmetry or lifted block exchange, for
example:

- a retained charged-lepton source grammar;
- an independently justified real-irrep block-democracy/measure law;
- an anomaly or gauge theorem that acts directly on the normalized
  traceless source;
- a full retained source-bank exhaustion proving every physical charged-lepton
  source is pure trace at this order.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_block_exchange_rank_obstruction.py
```

Result:

```text
PASSED: 9/9
KOIDE_Q_BLOCK_EXCHANGE_RANK_OBSTRUCTION=TRUE
```

---

## 7. Boundary

This note does **not** prove `Q = 2/3`. It proves only that a block-exchange
derivation of the traceless-source law is unavailable on the current retained
carrier. The full charged-lepton Koide lane remains open:

- `Q = 2/3` still needs a physical law forcing `K_TL = 0`;
- `delta = 2/9` still needs the physical Brannen Berry/APS bridge;
- the charged-lepton scale `v0` remains separate.
