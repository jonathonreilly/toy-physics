# B−L Anomaly-Freedom Theorem with Retained ν_R

**Date:** 2026-04-24
**Status:** **retained standalone structural-identity theorem** on `main`. Extracts and packages as its own theorem the full four-condition B−L anomaly-freedom closure that appears only partially ("linear gravitational anomaly = 0") inside [`PROTON_LIFETIME_DERIVED_NOTE.md`](PROTON_LIFETIME_DERIVED_NOTE.md) and is not mentioned in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md). The retained one-generation closure including ν_R ([`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)) and the retained hypercharge uniqueness ([`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)) together imply that U(1)_{B−L} is fully gauge-able on the retained content with no additional fermions required.
**Primary runner:** `scripts/frontier_bminusl_anomaly_freedom.py`

---

## 0. Statement

**Theorem (B−L anomaly-freedom with retained ν_R).** Given the retained one-generation SM content on `main`:

```text
Q_L : (2, 3)_{+1/3}    (B = +1/3, L = 0)     — 6 fermions (2 weak × 3 color)
L_L : (2, 1)_{−1}      (B =  0,  L = +1)     — 2 fermions (2 weak × 1)
u_R : (1, 3)_{+4/3}    (B = +1/3, L = 0)     — 3 fermions (3 color)
d_R : (1, 3)_{−2/3}    (B = +1/3, L = 0)     — 3 fermions
e_R : (1, 1)_{−2}      (B =  0,  L = +1)     — 1 fermion
ν_R : (1, 1)_{0}       (B =  0,  L = +1)     — 1 fermion
```

with `B − L` as the right-handed difference of baryon and lepton numbers (`B − L = +1/3` for quarks, `−1` for leptons), all **four** B−L anomaly coefficients vanish identically:

```text
(G1)  Tr[B − L]              =  0    (gravitational × U(1)_{B−L})
(G2)  Tr[(B − L)³]           =  0    (U(1)_{B−L}³ cubic)
(G3)  Tr[SU(3)² × (B − L)]   =  0    (colour × U(1)_{B−L} mixed)
(G4)  Tr[SU(2)² × (B − L)]   =  0    (weak × U(1)_{B−L} mixed)
```

Consequence: `U(1)_{B − L}` can be gauged on the retained content **without introducing any additional fermions**. The retained ν_R is load-bearing for **both (G1) and (G2)** — without a right-handed neutrino, both `Tr[B − L]` and `Tr[(B − L)³]` would fail to close (each would equal `−1` instead of `0`). (G3) and (G4) are unaffected by ν_R, because ν_R is a gauge-singlet under both SU(3) and SU(2).

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| One-generation content including ν_R | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) |
| Retained SM hypercharge uniqueness | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| B − L quantum-number assignments (standard) | textbook; `B = 1/3` for quarks, `B = 0` for leptons; `L = 0` for quarks, `L = 1` for leptons |
| Retained anomaly-forces-time chirality completion | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| Adler–Bell–Jackiw anomaly trace formulae | Adler 1969; Bell & Jackiw 1969; standard SM anomaly-cancellation textbook material |

No observational input and no ν_R mass (or Majorana phase) appears in the derivation.

## 2. Explicit B − L assignments

In the left-handed-conjugate frame (all fermions written as left-handed, with right-handed species charge-conjugated; `B − L` values flip sign when taking `f_R → f_R^c`):

| Field | SU(3) | SU(2) | multiplicity (colour × weak) | `B − L` (LH frame) |
|-------|-------|-------|----------------------------|--------------------|
| `Q_L` | 3 | 2 | 6 | `+1/3` |
| `L_L` | 1 | 2 | 2 | `−1` |
| `u_R^c` | `3̄` | 1 | 3 | `−1/3` |
| `d_R^c` | `3̄` | 1 | 3 | `−1/3` |
| `e_R^c` | 1 | 1 | 1 | `+1` |
| `ν_R^c` | 1 | 1 | 1 | `+1` |

## 3. Derivation

### 3.1 (G1) Tr[B − L] (gravitational mixed anomaly)

Sum in LH-conjugate frame:

```text
Tr[B − L]  =  6 · (+1/3) + 2 · (−1)        (LH)
             + 3 · (−1/3) + 3 · (−1/3)     (u_R^c, d_R^c)
             + 1 · (+1) + 1 · (+1)         (e_R^c, ν_R^c)

           =  2 − 2 − 1 − 1 + 1 + 1  =  0.                     ✓ (G1)
```

The six contributions pair up in sign within `{LH}`, `{u_R^c, d_R^c}`, `{e_R^c, ν_R^c}`.

### 3.2 (G2) Tr[(B − L)³] (cubic U(1)_{B−L} anomaly)

Sum of cubed charges:

```text
Tr[(B − L)³]  =  6 · (1/3)³ + 2 · (−1)³
                 + 3 · (−1/3)³ + 3 · (−1/3)³
                 + 1 · (1)³ + 1 · (1)³

              =  6/27 − 2 − 3/27 − 3/27 + 1 + 1
              =  2/9 − 2/9 − 2 + 2  =  0.                      ✓ (G2)
```

**The ν_R contribution (+1) is load-bearing for (G2).** Without ν_R, the cubic sum would be `2/9 − 2/9 − 2 + 1 = −1 ≠ 0`. Note that ν_R is also load-bearing for (G1) above — removing it drops `Tr[B − L]` to `−1`. The `+1` contribution from ν_R^c closes both (G1) and (G2) simultaneously.

### 3.3 (G3) Tr[SU(3)² × (B − L)] (colour-B−L mixed anomaly)

Only SU(3) fundamentals contribute; the SU(3)² trace is proportional to the SU(2) multiplicity of each species:

```text
Tr[SU(3)² (B − L)]  =  2 · (1/3)        (Q_L: SU(2) doublet)
                       + 1 · (−1/3)     (u_R^c)
                       + 1 · (−1/3)     (d_R^c)

                    =  2/3 − 1/3 − 1/3  =  0.                 ✓ (G3)
```

### 3.4 (G4) Tr[SU(2)² × (B − L)] (weak-B−L mixed anomaly)

Only SU(2) doublets contribute; the SU(2)² trace is proportional to the colour multiplicity:

```text
Tr[SU(2)² (B − L)]  =  3 · (1/3)        (Q_L: colour 3)
                       + 1 · (−1)       (L_L: colour 1)

                    =  1 − 1  =  0.                            ✓ (G4)
```

## 4. Consequences

### 4.1 U(1)_{B−L} can be gauged on the retained content

Adler–Bell–Jackiw anomaly-cancellation conditions (G1)–(G4) are the complete set for gauging `U(1)_{B−L}` with chiral fermions. Their simultaneous vanishing means the retained SM content (with ν_R, at native-axiom level from the one-generation closure) is anomaly-free for `U(1)_{B−L}`.

No additional fermions are required. This is structurally unlike the SM without ν_R, for which (G2) has a non-zero residual `−1` that requires a right-handed neutrino (or a heavy Majorana completion) to close.

### 4.2 ν_R load-bearing for both (G1) and (G2)

Without ν_R (removing the 16th fermion per generation):

- **(G1) fails**: `Tr[B − L] = −1 ≠ 0` — the +1 contribution from ν_R^c is needed linearly.
- **(G2) fails**: `Tr[(B − L)³] = −1 ≠ 0` — the +1 contribution from ν_R^c is needed cubically.
- **(G3) closes** regardless of ν_R (ν_R is an SU(3) singlet; it contributes `0` to Tr[SU(3)² (B−L)]).
- **(G4) closes** regardless of ν_R (ν_R is an SU(2) singlet; it contributes `0` to Tr[SU(2)² (B−L)]).

So ν_R is exactly the gauge-singlet witness that simultaneously closes (G1) and (G2). The retained one-generation closure — which independently includes ν_R via anomaly-forces-time Step 2 + hypercharge uniqueness Y(ν_R) = 0 — is therefore structurally necessary for B−L anomaly-freedom.

Note that (G1) failing without ν_R is *not* the same as SM's hypercharge `Tr[Y] = 0` working without ν_R: those are different linear combinations of the U(1) quantum numbers, and ν_R's `Y = 0` vs `B−L = +1` is exactly what distinguishes the two.

### 4.3 Conservation of B − L at the perturbative level

All perturbative processes on the retained surface conserve `B − L` exactly, even in the presence of electroweak sphalerons (which violate `B + L` but preserve `B − L`). This is consistent with the retained strong-CP theorem ([`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md), θ-surface closure) preserving `B − L` via `det(M_u M_d)` being a weak-sector phase only.

### 4.4 Relation to the proton-lifetime bounded prediction

The retained 36 leptoquark operators in the Cl(3) algebra (see [`PROTON_LIFETIME_DERIVED_NOTE.md`](PROTON_LIFETIME_DERIVED_NOTE.md)) are dimension-6 `B`-violating operators. They *do not* violate `B − L`: each leptoquark operator pairs `ΔB = 1` with `ΔL = 1`, preserving `B − L = 0`. The proton-decay channels like `p → e⁺ π⁰` have `ΔB = −1, ΔL = −1`, hence `Δ(B − L) = 0`.

## 5. Structural observations

- **All four anomaly traces are rational.** Each trace is a sum of rational multiples of small rationals `{1/3, −1, +1, −1/3}`, closed by Pythagorean integer arithmetic without any extension of ℚ.
- **ν_R is structurally load-bearing for both (G1) and (G2).** (G3) and (G4) close without ν_R (since ν_R is SU(3) × SU(2) singlet). Both linear *and* cubic B−L anomaly conditions require the ν_R contribution, establishing ν_R as the structural witness forced by B−L anomaly-freedom in addition to the anomaly-forces-time hypercharge closure.
- **The closure is independent of hypercharge.** `B − L` is orthogonal to the retained `Y` direction in the two-dimensional U(1) sector of the commutant; the anomaly-freedom of `B − L` is a distinct structural fact from the SM hypercharge anomaly-freedom already packaged in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).
- **Gauged B−L implies a Z′ boson.** Any extension of the retained gauge group to `SU(2) × SU(3) × U(1)_Y × U(1)_{B−L}` adds a new gauge boson `Z′`; the retained anomaly-freedom says no additional fermions are needed to close the quantum theory, only the bookkeeping of which gauge bosons appear.

## 6. Scope and boundary

**Claims:**

- (G1)–(G4) vanish identically on the retained one-generation SM content with ν_R.
- `U(1)_{B−L}` is gauge-able on the retained content without adding matter.
- ν_R is load-bearing for BOTH the linear (G1) and cubic (G2) conditions.

**Does NOT claim:**

- That `U(1)_{B−L}` *is* gauged in the framework (the retained gauge group is `SU(2) × SU(3) × U(1)_Y`; this theorem says only that the *option* of gauging `B − L` is anomaly-consistent).
- A numerical prediction for any `Z′` mass or coupling if `B − L` were gauged.
- Cross-generation content: the theorem applies per-generation and extends trivially to all three generations (each generation satisfies (G1)–(G4) independently).
- A derivation of `B`, `L`, or `B − L` charges themselves from the retained gauge structure — these are standard SM bookkeeping.
- Majorana-mass structure for ν_R (the theorem is purely about B−L quantum-number anomaly coefficients; Majorana mass violates `L` but not `B − L` by 2 units and is a separate dynamical question).

## 7. Falsifiability

Indirect:

- A confirmed detection of a light `B − L` gauge boson `Z′` would confirm the gauging is physically realised (with framework consistent from anomaly-freedom).
- A confirmed detection of proton decay with `Δ(B − L) ≠ 0` (e.g. `p → e⁻` rather than `p → e⁺`) would violate the retained anomaly-freedom picture.
- Any observed process with `Δ(B − L) = ±2` at high confidence (e.g. neutrino-less double-beta decay) would constrain the Majorana structure of ν_R and is a separate test.

Current status: No experimental data violates `U(1)_{B − L}` anomaly-freedom. Proton decay at `τ < 10⁴⁰` yr would rule out the retained framework but not the anomaly-freedom per se (the bound concerns the B-violating leptoquark operator scale, not the anomaly).

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_bminusl_anomaly_freedom.py
```

Expected: all checks pass.

The runner:

1. Enumerates the retained LH-conjugate-frame fermion content.
2. Evaluates (G1)–(G4) as rational-number arithmetic via `fractions.Fraction`.
3. Verifies each trace equals `0` exactly (not within floating-point tolerance).
4. Verifies the ν_R load-bearing claim by recomputing (G2) without ν_R and showing it equals `−1` instead of `0`.
5. Reports rational intermediate values for transparency.

## 9. Cross-references

- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) — retained ν_R inclusion
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — retained SM hypercharges include `Y(ν_R) = 0`
- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) — retained anomaly-forces-time theorem (does not package B−L separately)
- [`PROTON_LIFETIME_DERIVED_NOTE.md`](PROTON_LIFETIME_DERIVED_NOTE.md) — contains a partial (linear-only) B−L anomaly-freedom remark superseded by this theorem
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — retained LH content
- Adler 1969 "Axial vector vertex in spinor electrodynamics", Phys. Rev. 177, 2426
- Bell & Jackiw 1969 "A PCAC puzzle: π⁰ → γγ in the σ-model", Nuovo Cim. A 60, 47
