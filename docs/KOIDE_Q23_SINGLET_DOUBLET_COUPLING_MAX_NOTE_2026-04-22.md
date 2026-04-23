# Koide Q = 2/3 via Singlet-Doublet Coupling Maximization

**Date:** 2026-04-22
**Status:** **candidate variational attack** on the Q = 2/3 open bridge. Mathematical content (unique max at σ_1 = 1/2) is exact; retained physical motivation for the functional is the outstanding step.
**Primary runner:** `scripts/frontier_koide_q23_singlet_doublet_coupling_max.py` (9/9 PASS)

---

## 0. Proposal

Define the "singlet-doublet coupling" functional on the Z_3 Fourier occupancy:

```
C(σ_1)  :=  σ_1 · (1 − σ_1)  =  σ_1 · σ_doublet
```

where `σ_1` is the total singlet occupancy and `σ_doublet = 1 − σ_1` is the total doublet occupancy on the retained Z_3 decomposition of the hw=1 charged-lepton triplet.

**Mathematical fact (sympy exact)**: `C(σ_1)` has a **unique maximum** on `[0, 1]` at `σ_1 = 1/2`, with `C(1/2) = 1/4`.

**Physical consequence**: if the retained physical charged-lepton packet extremizes `C` (maximum coupling between singlet and doublet Z_3 sectors), then

```
σ_1 = 1/2  ⇒  Q_Koide = 1/(d·σ_1) = 2/3    (at d = 3)
```

closes the Q = 2/3 bridge.

## 1. Why this is attack #8

This is the **8th candidate route** on the Q = 2/3 landscape after:

- 7 support routes (converging on `P_Q = 1/2` or `σ_1 = 1/2`).
- 7 no-gos (ruling out simple symmetry mechanisms).

The variational approach is NOVEL: no existing no-go targets variational principles on Z_3 Fourier occupancy. Closure requires only **ONE retained physical principle** (motivation for the functional), not a cascade of structural derivations.

## 2. The math (sympy-exact)

`C(σ_1) = σ_1 · (1 − σ_1)`:
- Unique critical point: `dC/dσ_1 = 1 − 2σ_1 = 0 ⇒ σ_1 = 1/2`.
- Second derivative: `d²C/dσ_1² = −2 < 0` → maximum.
- Maximum value: `C(1/2) = 1/4`.

Numerical sweep over [0.01, 0.99] confirms global max.

## 3. Koide connection

From the Koide state Fourier form `s(m) = (1/√2) v_1 + (1/2)e^{iθ} v_ω + (1/2)e^{−iθ} v_{ω̄}` with σ_1 = 1/2:

```
Q_Koide  =  1/(d · σ_1)  =  1/(3 · (1/2))  =  2/3                          (exact)
```

So: `σ_1 = 1/2 ↔ Q_Koide = 2/3`.

## 4. Convergence with other natural functionals

Multiple natural information-theoretic and coupling functionals share the extremum at σ_1 = 1/2:

| Functional | Extremum at σ_1 = 1/2 | Value |
|------------|----------------------|-------|
| `C = σ_1 · (1 − σ_1)` | MAX | `1/4` |
| `H = −σ_1 ln σ_1 − (1−σ_1) ln(1−σ_1)` (Shannon) | MAX | `ln 2` |
| `S_Tsallis = 1 − σ_1² − (1−σ_1)²` | MAX | `1/2` |

All three of these 1D functionals peak at σ_1 = 1/2. This is a strong sign that the Koide point is the **natural "balance" point** of Z_3 occupancy.

## 5. What would close the bridge

A retained physical principle that forces the charged-lepton packet to extremize one of these functionals. Candidates:

- **(i) Maximum mutual information** between singlet and doublet Z_3 sectors (Shannon-based).
- **(ii) Maximum coupling strength** σ_1 · σ_doublet (product-based).
- **(iii) Minimum purity** σ_1² + σ_doublet² (Tsallis-based).

None are currently retained as physical laws. The framework has RETAINED the algebraic identity that σ_1 = 1/2 follows from Q = 2/3, and 7 independent support routes all land on σ_1 = 1/2. A variational principle that FORCES this value would close the bridge.

## 6. Scope qualifiers

- **Mathematical fact**: unique max at σ_1 = 1/2 is exact.
- **Physical content**: the variational principle that selects `C` (or `H` or `S_Tsallis`) as the functional to extremize is NOT YET retained. Three candidate motivations are documented in §5 but none is currently a retained theorem.
- **This is CANDIDATE closure, not actual closure**: Q = 2/3 remains open on the retained derivation footing.

## 7. Cross-references

- `docs/KOIDE_Q23_ATTACK_LANDSCAPE_STATUS_2026-04-22.md` — full landscape status.
- `docs/KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md` — user-landed single-primitive narrowing.
- `docs/KOIDE_Q23_ANOMALY_STRUCTURAL_ATTACK_NOTE_2026-04-22.md` — loop 12 anomaly-identity route.
- `docs/KOIDE_Q23_SPIN1_STRUCTURAL_ROUTE_NOTE_2026-04-22.md` — loop 13 spin-1 route.
- `docs/KOIDE_Q23_OH_COVARIANCE_NOGO_NOTE_2026-04-22.md` — loop 14 no-go.
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — six original no-gos.
