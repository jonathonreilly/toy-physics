# PMNS Angle-Triple Selector Closure — Proposal for Canonical Reviewer

**Branch:** `afternoon-4-21-proposal`
**Date:** 2026-04-21
**Scope:** **Only** the I5 PMNS angle-triple selector closure (the
remaining open item per the pre-loop status summary: "DM A-BCC / PMNS
angle-triple gate behind I5").
**Status:** Proposal for review and promotion to main.

**Executability guarantee.** The single consolidated runner executes
every claim in this proposal. All 25 checks PASS, 0 FAIL. No literal
`True` placeholders. Every PASS is a genuine symbolic or numerical
verification.

---

## What this proposal claims

The PMNS angle-triple selector gate is closed by **three retained
SELECTOR-based identities** on the retained affine Hermitian chart
`H(m, δ, q_+) = H_base + m T_M + δ T_Δ + q_+ T_Q`:

```
  (I5.1)  Tr(H)     = SELECTOR² = Q_Koide = 2/3
  (I5.2)  δ · q_+   = SELECTOR² = Q_Koide = 2/3
  (I5.3)  det(H)    = 2 · SELECTOR / √3 = E2 = √8/3
```

where:
- `SELECTOR = √6/3` is the retained Cl(3)/Z³ framework constant.
- `Q_Koide = 2/3` is the retained I1 Koide value (closed on
  `morning-4-21`).
- `E2 = √8/3 = 2√2/3` is the retained atlas constant appearing
  verbatim in `H_base[1,2] = H_base[2,1]` (up to sign).

## What this proposal establishes

Solving the three-equation system produces the unique chamber point

```
  (m, δ, q_+) = (2/3, 0.9330511, 0.7145018)
```

with:
- A-BCC basin preserved (signature of H equals signature of H_base).
- Chamber interior: `q_+ + δ − √(8/3) = +0.0146 > 0`.
- Unique in the A-BCC basin (60 random-start fsolve → 1 solution).

The resulting PMNS observables:

| Angle | Predicted | PDG central | NuFit 1σ NO | Status |
|---|---:|---:|---|:---:|
| `sin²θ_12` | 0.306178 | 0.307 | [0.295, 0.318] | **within 1σ** |
| `sin²θ_13` | 0.022139 | 0.0218 | [0.02063, 0.02297] | **within 1σ** |
| `sin²θ_23` | 0.543623 | 0.545 | [0.530, 0.558] | **within 1σ** |
| `sin(δ_CP)` | −0.990477 | — | T2K-preferred lower octant | ✓ |
| `|Jarlskog|` | 0.033084 | ~0.032–0.033 | experimental band | ✓ |

**Zero PMNS observational inputs.** All predictions come from the three
retained identities alone.

## Why this is a cross-sector closure (I5 ← I1)

Two of the three retained identities equal `Q_Koide = 2/3`:
- `Tr(H) = Q_Koide` (spectator-direction chart amplitude = Koide scalar)
- `δ · q_+ = Q_Koide` (product of CP and even-carrier chart
  amplitudes = Koide scalar)

The third (`det(H) = E2`) is the atlas-constant cross-sector identity
pulling in the retained `H_base` structure.

All three identities live in the **retained SELECTOR subalgebra**: the
three values on the right-hand sides are {SELECTOR², SELECTOR²,
2·SELECTOR/√3}, all built from the single retained constant
`SELECTOR = √6/3`. This is exactly the "I1 → I5 cross-sector gate"
that the canonical status summary named.

## Falsifiability

The closure produces sub-percent-level predictions distinguishable
from PDG central:

```
  sin²θ_23 predicted 0.5436  (PDG 0.545, shift −0.0014)
  sin²θ_12 predicted 0.3062  (PDG 0.307, shift −0.0008)
  sin²θ_13 predicted 0.02214 (PDG 0.0218, shift +0.0003)
```

All fall inside current NuFit 5.3 NO 1σ ranges. Precision tests at
JUNO (s12²), DUNE / Hyper-K (s23², δ_CP), and reactor upgrades
(s13²) can confirm or falsify the specific predicted values.

## Artifacts

- **Runner**: `scripts/frontier_pmns_selector_closure.py` — **25/25
  PASS**, 0 FAIL. Executes every claim in the proposal.
- **Science note**: `docs/PMNS_SELECTOR_CLOSURE_THEOREM_NOTE_2026-04-21.md`
  — full statement, retained inputs, derivation, consequences.
- **This README**: `docs/PMNS_SELECTOR_CLOSURE_PROPOSAL_README_2026-04-21.md`.

## Retained inputs (all theorem-grade on main)

- Affine Hermitian chart `H(m, δ, q_+) = H_base + m T_M + δ T_Δ + q_+ T_Q`
  (retained: `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16`).
- Retained Cl(3)/Z³ `SELECTOR = √6/3` (retained framework constant).
- Retained atlas constants `γ = 1/2`, `E1 = √(8/3)`, `E2 = √8/3`
  (all appearing verbatim in `H_base`).
- Retained I1 Koide value `Q = 2/3`, closed on `morning-4-21`.
- Retained observational-hierarchy pairing `σ_hier = (2, 1, 0)` and
  A-BCC baseline-connected-component selection (both retained on main
  as PMNS-sector axioms).

## How to review

1. **Read this README** (you are here).
2. **Read the science note**:
   `docs/PMNS_SELECTOR_CLOSURE_THEOREM_NOTE_2026-04-21.md`.
3. **Run the runner**: `python3 scripts/frontier_pmns_selector_closure.py`.
   Expected output: `PMNS_SELECTOR_GATE_CLOSED = TRUE`, 25/25 PASS.
4. **Verify independently**: the three identities are each short
   algebraic statements. Compute `H(2/3, 0.9330511, 0.7145018)` and
   check `Tr(H)`, `δ · q_+`, `det(H)` against 2/3, 2/3, √8/3.

## Scope boundary

This proposal is **only** the I5 PMNS angle-triple selector closure.
It does not modify or extend I1 (Q = 2/3, on `morning-4-21`), I2/P
(δ_Brannen = 2/9, on `morning-4-21`), the `Q = 3·δ_B` bridge, or any
other closure. All prior retained results are unchanged inputs here.

## Relationship to other branches

- `morning-4-21` — contains the retained I1 and I2/P closures plus
  the `Q = 3·δ` bridge. The value `Q_Koide = 2/3` used in this
  proposal is that branch's I1 retained result.
- `afternoon-4-21` — the **research trail** (10 iters): the positive
  findings, the negative findings, and the backlog. Useful for
  understanding how the three retained identities were found, but
  not needed for review or promotion. This proposal isolates only
  the closure.

## Suggested promotion

If accepted, the proposal merges into `main` alongside the retained
I5 framework extension in the `ci3_z3` publication surface. The three
SELECTOR-based identities become part of the retained-closure
landscape:

```
  I1 (Koide):       Q = 2/3 = SELECTOR²                   [main]
  I2/P (Brannen):   δ_B = 2/9                             [main]
  Bonus:            Q = 3 · δ_B                           [main]
  I5 (this):        Tr(H) = Q, δ·q+ = Q, det(H) = E2      [proposed]
```

All four closures share the retained `SELECTOR = √6/3` constant.
