# Koide Q = 2/3 via Spin-1 SO(3) Structural Route

**Date:** 2026-04-22
**Status:** partial closure proposal. Reformulates the open `Q = 2/3` bridge as a specific structural question: does the retained 3-generation charged-lepton triplet carry a spin-1 SO(3) representation?
**Primary runner:** `scripts/frontier_koide_q23_spin1_structural_route.py` (8/8 PASS)

---

## 0. Candidate structural chain

```
d_spatial = 3                    [retained from Cl(3) + ANOMALY_FORCES_TIME]
spin-s rep with d = 2s+1         [SO(3) representation theory]
Q_Koide = 2s/(2s+1) = (d−1)/d    [proposed structural identity]
→  Q_Koide = 2/3 at s = 1        [d = 3 ⇒ s = 1]
```

**If the retained charged-lepton 3-generation triplet carries spin-1 SO(3) representation, then `Q_Koide = 2/3` is forced axiom-natively by `d_spatial = 3`.**

## 1. The algebraic identity

The proposed structural form:

```text
Q_Koide  =  (d − 1) / d  =  2s / (2s + 1)                                   (★)
```

These two forms are **sympy-identically equal** under the SO(3) representation-theoretic parametrization `d = 2s + 1`. At `s = 1` (spin-1, the vector / adjoint representation): `d = 3` and `Q_Koide = 2/3`.

## 2. Why this route is novel vs. the six existing no-gos

`SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` flags six structural no-gos on `Q = 2/3`:

| No-go | Target mechanism |
|-------|------------------|
| 1 | Z_3-invariance alone |
| 2 | Sectoral universality |
| 3 | Color-sector correction |
| 4 | Anomaly-forced cross-species |
| 5 | SU(2) gauge exchange mixing |
| 6 | Observable-principle character symmetry |

This route targets a DIFFERENT mechanism: **SO(3) spatial isotropy → spin-1 representation → Q = 2s/(2s+1) algebraic identity at s = 1**. None of the six no-gos address SO(3) / spatial-isotropy / spin-1 rep identification on the 3-generation triplet, so the six no-gos do NOT preclude this route.

## 3. The outstanding structural step

The chain (★) reduces `Q = 2/3` to the single structural claim:

> **Does the retained 3-generation charged-lepton triplet carry a spin-1 representation of SO(3)?**

Dimension-counting is clean: any 3-dim SO(3) representation is uniquely spin-1 (`2s+1 = 3 ⇒ s = 1`). So if the retained hw=1 triplet carries an SO(3) rep at all, it must be spin-1.

But the retained framework explicitly retains only the `Z_3 ⊂ O_h ⊂ SO(3)` body-diagonal subgroup on the 3-generation structure. Whether this extends to full SO(3) (spatial isotropy) on the generation-label space is the outstanding question.

### Three candidate derivations for the SO(3) extension

**(a) Lattice O_h rotation invariance of H_base.** The retained Hermitian chart `H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q` has specific matrix entries. If `H_base` is invariant under the full `O_h` cubic point group acting on Z³ (48 elements), and O_h ⊂ SO(3), then the hw=1 triplet carries the restriction of an SO(3) rep.

**(b) Body-diagonal Z_3 fixed-point structure.** The retained Z_3 body-diagonal fixed sites on Z³ carry a natural action of the isotropy subgroup (rotations around the body-diagonal). This isotropy is SO(2) × Z_2, but embedding into full SO(3) via the body-diagonal axis direction could upgrade the 3-fold to spin-1.

**(c) SU(2)_L doublet × generation.** In the SM, charged leptons sit in SU(2)_L × generation = 2 × 3 = 6-dim space per chirality. The 3-generation sector alone is the "singlet of SU(2)_L" inside this product. If the retained framework forces the generation factor to carry a retained angular-momentum representation, dimension-3 forces spin-1.

Any of (a), (b), (c) being retained-structural would close `Q = 2/3`.

## 4. What this note closes and does not close

**Closes (algebraically)**:
- The identity `(d−1)/d = 2s/(2s+1)` at `d = 2s+1` is exact (sympy).
- At retained `d = 3`, `Q_Koide = 2/3` follows from the spin-1 interpretation.
- Counterfactual at other `d` gives different `Q` values (`d = 4 → Q = 3/4`, `d = 5 → Q = 4/5`, etc.), so `d = 3` is essential.

**Does NOT close (outstanding structural step)**:
- The retained derivation that hw=1 triplet = spin-1 SO(3) rep (vs generic 3-dim Z_3-equivariant space).
- Any of the three candidate sub-routes (a), (b), (c).

## 5. Comparison with the doublet-magnitude conjecture (loop 12)

Loop 12's conjecture was `E2² = |Tr[Y³]_LH|/2 = (d²−1)/d²`, giving `Q_Koide = 3(d²−1)/(4d²)`. This gives `2/3` at `d = 3` but differs at other `d` (e.g., `d = 4 ⇒ Q = 45/64`).

The spin-1 route gives `Q_Koide = (d−1)/d`, which gives `2/3` at `d = 3` and `3/4` at `d = 4`. So the two conjectures AGREE at `d = 3` but DIVERGE at other `d`.

Both are compatible with the retained `d = 3` fact. Both reduce to different fundamental structural questions:

| Route | Fundamental question |
|-------|----------------------|
| Loop 12 (anomaly-identity) | Is `E2² = |Tr[Y³]_LH|/2` structural? |
| Loop 13 (spin-1 SO(3)) | Does hw=1 triplet carry spin-1 SO(3) rep? |

Both routes attack the Koide `Q = 2/3` bridge; progress on either would close it.

## 6. Cross-references

- `docs/KOIDE_Q23_ANOMALY_STRUCTURAL_ATTACK_NOTE_2026-04-22.md` — loop 12 anomaly-identity route.
- `docs/KOIDE_Q_EQ_3DELTA_DOUBLET_MAGNITUDE_THEOREM_NOTE_2026-04-22.md` — loop 2 doublet-magnitude identity.
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` — retained d = 3.
- `docs/MINIMAL_AXIOMS_2026-04-11.md` — framework axioms including Cl(3)/Z³.
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — six existing no-gos.
- Standard SO(3) representation theory (Wigner, Weinberg Vol 1 Ch 2.5).
