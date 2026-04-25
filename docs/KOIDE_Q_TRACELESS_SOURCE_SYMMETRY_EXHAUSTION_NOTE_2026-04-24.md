# Koide Q Traceless-Source Symmetry Exhaustion

**Date:** 2026-04-24
**Status:** Branch-local negative theorem. This does not close `Q`; it shows
that the remaining `K_TL = 0` primitive is not forced by current
`C_3` symmetry plus trace normalization alone.
**Primary runner:** `scripts/frontier_koide_q_traceless_source_symmetry_exhaustion.py`

---

## 1. Question

After the trace/Lagrange-multiplier reduction, the `Q = 2/3` bridge is the
single scalar condition

```text
K_TL = 0.
```

This note asks whether current symmetry and normalization data already force
that scalar to vanish.

Answer:

```text
No.
```

---

## 2. Source Space

Let `P_plus` be the `C_3` singlet projector and `P_perp = I - P_plus` the
real-doublet projector on the three-generation cyclic carrier. A lifted
trace/traceless block source has the form

```text
K = k_trace I + k_tl (P_plus - P_perp).
```

The runner verifies exactly that this source commutes with the cyclic
generator. Therefore the `Q`-relevant traceless source is not excluded by
`C_3` equivariance.

Modulo pure trace, the source quotient is one-dimensional:

```text
span{I, P_plus-P_perp} / span{I}.
```

---

## 3. No Internal Block Exchange

Every matrix commuting with the cyclic generator has circulant form:

```text
[[x8, x6, x7],
 [x7, x8, x6],
 [x6, x7, x8]].
```

Every such matrix preserves `P_plus`. Hence the current `C_3` symmetry has no
internal operation exchanging the singlet and real-doublet sectors. The two
sectors are inequivalent isotypes, so `C_3` alone cannot impose

```text
K_TL -> -K_TL
```

as a symmetry that would force `K_TL = 0`.

---

## 4. Explicit Counterexample

The runner gives an admissible nonzero source:

```text
K_TL = 1/5.
```

The constrained positive trace-2 solution is

```text
Y = diag(0.807417596433, 1.19258240357),
```

which is inside the normalized cone but off the Koide point:

```text
Q = 0.825677653809 != 2/3.
```

Thus a nonzero `K_TL` is compatible with current `C_3` symmetry and trace
normalization.

---

## 5. Consequence

The current symmetry-only data do not close the `Q` bridge.

The remaining closure target is sharper:

```text
derive K_TL = 0
```

from one of:

- a retained charged-lepton source grammar;
- a real-irrep block-democracy principle;
- a block-exchange principle not contained in plain `C_3`;
- an anomaly or gauge theorem;
- a full retained source-bank exhaustion showing all physical charged-lepton
  sources have zero traceless component at this order.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_traceless_source_symmetry_exhaustion.py
```

Result:

```text
PASSED: 9/9
KOIDE_Q_TRACELESS_SOURCE_SYMMETRY_EXHAUSTION_NO_GO=TRUE
```

---

## 7. Boundary

This is a no-go against closing `Q` from `C_3` symmetry and trace
normalization alone. It leaves the full Koide lane open:

- `Q = 2/3` still needs a physical no-traceless-source law;
- `delta = 2/9` still needs the physical Brannen Berry/APS bridge;
- the charged-lepton overall scale `v0` remains separate.
