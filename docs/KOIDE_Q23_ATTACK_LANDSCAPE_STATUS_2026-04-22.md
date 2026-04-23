# Koide `Q = 2/3` Attack Landscape Status

**Date:** 2026-04-22
**Status:** navigation / landscape consolidation. Maps the full set of attack routes, no-gos, and support primitives on the `Q = 2/3` bridge as they stand after the April-22 retained landings plus autonomous-loop attacks.
**Purpose:** single reviewer entry point to the `Q = 2/3` landscape.

---

## 0. Where the bridge sits

The `Q = 2/3` extremal-principle bridge is **open**. Multiple support routes converge on one primitive, and multiple no-gos rule out candidate closures. The remaining open step is the **physical identification**: why does the charged-lepton packet realize the primitive?

Equivalently, the entire landscape has been reduced to:

```text
P_Q := |b|²/a² = 1/2       (from retained landing: KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE)
```

with multiple structural-arithmetic support routes landing on `1/2`. No mechanism yet forces the physical charged-lepton packet to realize `P_Q = 1/2`.

---

## 1. Support routes (all → `P_Q = 1/2` or equivalent)

### User-landed on main (commit `ffe965c7`)

| # | Identity | Source |
|---|----------|--------|
| S1 | `dim(spinor)/dim(Cl⁺(3)) = 2/4 = 1/2` | Cl(3) spinor / even-grade ratio |
| S2 | `T(T+1) − Y² = 3/4 − 1/4 = 1/2` | SU(2)_L × U(1)_Y Casimir at T = Y = 1/2 |
| S3 | `(T(T+1) − Y²) / (T(T+1) + Y²) = 1/2` | Normalized Casimir ratio |
| S4 | Frobenius-isotype / AM-GM support (retained) | Isolates Koide point as extremum |
| S5 | ABSS / topological fixed-point (retained) | Gives `η = 2/9 = Q/3` |

### Autonomous-loop attacks (loops 12, 13)

| # | Identity | Loop |
|---|----------|------|
| S6 | `E2² = (d²−1)/d² = |Tr[Y³]_LH|/2 = 8/9` at `d = 3` | Loop 12 (anomaly-identity conjecture) |
| S7 | `Q_Koide = (d−1)/d = 2s/(2s+1) = 2/3` at `d = 3, s = 1` | Loop 13 (spin-1 SO(3) route) |

**Convergence**: S1–S7 all land on the same structural target `P_Q = 1/2 ↔ Q_Koide = 2/3`. They represent **seven independent support paths** to the same primitive, from different retained structures.

---

## 2. No-gos (ruled out as closure mechanisms)

| # | No-go | Source |
|---|-------|--------|
| N1 | `Z_3`-invariance alone | `SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS` |
| N2 | Sectoral universality | same |
| N3 | Color-sector correction | same |
| N4 | Anomaly-forced cross-species | same |
| N5 | SU(2) gauge exchange mixing | same |
| N6 | Observable-principle character symmetry | same |
| **N7** | **O_h cubic covariance of H_base chart** | **Loop 14 (this session)** |

N7 is NEW: explicitly rules out that the retained affine chart `H(m, δ, q_+)` carries cubic-lattice O_h symmetry. The chart's covariance group in O_h is only `{+I, −I} = Z_2` (spatial parity).

---

## 3. Open structural question

After all 7 support routes + 7 no-gos, the physical identification question is:

> **Why does the physical charged-lepton packet realize `P_Q = 1/2`?**

Equivalent formulations:

- Why does the retained hw=1 charged-lepton triplet have singlet occupancy `σ_1 = 1/2` (balanced singlet:doublet)?
- Why does the second-order returned carrier satisfy `Y = I_2` (identity trace-2 positive cone)?
- Why `|b|²/a² = 1/2` on the physical cyclic image?

The support routes say this value has MANY structural coincidences; the no-gos say the obvious symmetry mechanisms fail. The remaining closure requires either:

**(A)** A retained physical principle selecting the primitive value (e.g., variational law, observable extremum, Ward-identity consequence).

**(B)** Promoting one of the support identities (S1–S7) to a retained physical law. For example:
- S2 `T(T+1) − Y² = 1/2` would need a retained variational principle extremizing `T(T+1) − Y²` on the charged-lepton packet.
- S6 would need Route A (source-surface trace σ sin(2v) = 8/9 → LH anomaly with 1/2 factor) or Route B (direct Cl(3) derivation of E2).
- S7 would need sub-route (b) body-diagonal isotropy or (c) SU(2)_L × generation — loop 14 ruled out sub-route (a).

---

## 4. Attack bandwidth summary

| Direction | Progress | Blocker |
|-----------|----------|---------|
| Support identities | Many converging; S1–S7 all land on 1/2 | None (all retained) |
| Physical-identification principle | None retained | This is the remaining bridge |
| Obvious symmetry mechanisms | 7 no-gos | Ruled out as simple closures |
| Structural reformulations | Multiple (loops 12, 13, user's single-primitive) | Different fundamental questions |

The bridge is **over-determined in support** (many paths land on the same value) but **under-determined in physical-identification** (no retained principle forces any of them).

---

## 5. What a reviewer should note

The `Q = 2/3` bridge is a classic case of "simple algebraic identity with many confirming coincidences and no retained derivation". This pattern is recognized:

- `P_Q = 1/2` is the smallest nontrivial retained value that the charged-lepton packet COULD realize, and 7 independent support routes agree on it.
- None of the 7 no-gos can close it via standard symmetry mechanisms (already audited).
- The closure requires either a NEW variational principle on the retained surface OR a retained promotion of one support identity to physical law.

The framework's status on this lane is: **"bounded with maximum support, open at the level of physical principle"**.

---

## 6. How this differs from the six earlier no-gos

N1-N6 target SYMMETRY-BASED closures (group actions). N7 (loop 14) targets a LATTICE-GEOMETRIC closure (cubic O_h invariance of the chart). All seven no-gos now audit the symmetry-based mechanisms for the Q = 2/3 closure.

The remaining closure paths are either (a) variational (extremize a specific functional) or (b) derivation of one of the support identities from deeper retained structure. These are not covered by the seven no-gos.

---

## 7. Attack branches (autonomous-loop session)

Three branches in this session target Q = 2/3:

1. [`koide-q23-anomaly-structural-attack`](https://github.com/jonathonreilly/cl3-lattice-framework/tree/koide-q23-anomaly-structural-attack) (loop 12): conjecture E2² = (d²−1)/d² = |Tr[Y³]_LH|/2.
2. [`koide-q23-spin1-structural-route`](https://github.com/jonathonreilly/cl3-lattice-framework/tree/koide-q23-spin1-structural-route) (loop 13): `Q = (d−1)/d = 2s/(2s+1)` at spin s = 1, d = 3.
3. [`koide-q23-lattice-oh-stabilizer`](https://github.com/jonathonreilly/cl3-lattice-framework/tree/koide-q23-lattice-oh-stabilizer) (loop 14): **NO-GO** on O_h covariance of H_base chart (sub-route (a) of spin-1).

Each opens a different attack axis. Progress on any would close `Q = 2/3`.

---

## 8. Cross-references

- `docs/KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md` — user's single-primitive narrowing.
- `docs/KOIDE_Q_NORMALIZED_SECOND_ORDER_EFFECTIVE_ACTION_THEOREM_2026-04-22.md` — user's normalized action theorem.
- `docs/KOIDE_Q_MINIMAL_SCALE_FREE_SELECTOR_NOTE_2026-04-22.md` — user's minimal scale-free selector.
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — six original no-gos.
- `docs/KOIDE_Q23_ANOMALY_STRUCTURAL_ATTACK_NOTE_2026-04-22.md` — loop 12.
- `docs/KOIDE_Q23_SPIN1_STRUCTURAL_ROUTE_NOTE_2026-04-22.md` — loop 13.
- `docs/KOIDE_Q23_OH_COVARIANCE_NOGO_NOTE_2026-04-22.md` — loop 14.
- `docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md` — Q = 3·δ structural link.
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — Berry holonomy identification.
