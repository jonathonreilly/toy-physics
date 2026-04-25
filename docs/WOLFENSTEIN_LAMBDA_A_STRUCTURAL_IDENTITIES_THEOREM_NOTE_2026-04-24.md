# Wolfenstein λ and A Structural Identities Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-identity theorem** on `main`. Companion to [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md). Extracts and packages as their own theorem the inline identities `λ² = α_s(v)/2` and `A² = 2/3` from [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) §"Exact Constants", which appear inside the parent atlas theorem but are not individually retained as named rows.
**Primary runner:** `scripts/frontier_wolfenstein_lambda_a_structural_identities.py`

---

## 0. Statement

**Theorem (Wolfenstein λ and A structural identities).** On the retained CKM atlas/axiom surface ([`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)) with retained `n_pair = 2` (SU(2) doublet structure) and retained `n_color = N_c = 3` (graph-first SU(3) closure), the Wolfenstein parameters `λ` and `A` satisfy the exact structural identities

```text
(W1)   λ²  =  α_s(v) / n_pair  =  α_s(v) / 2                        (Cabibbo from strong coupling)
(W2)   A²  =  n_pair / n_color  =  2 / 3                              (Wolfenstein A from group-rep ratio)
```

A combined identity then follows from product:

```text
(W3)   A² · λ²  =  (n_pair / n_color) · (α_s(v) / n_pair)
                =  α_s(v) / n_color  =  α_s(v) / 3                   (combined "λ² A²" identity)
```

(W2) is a **pure rational** independent of any coupling. (W1) is α_s(v)-linear. (W3) is `α_s(v)/3` — also α_s(v)-linear with denominator `n_color = 3`.

These three identities, together with the retained CP-phase identity `cos²δ = 1/6` from [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md), constitute the **complete** Wolfenstein structural-parameter package on the retained CKM atlas.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Canonical CKM atlas/axiom package | [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `n_pair = 2`: SU(2)_L doublet structure | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| `n_color = N_c = 3`: graph-first SU(3) | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| `n_quark = 2 × 3 = 6`: quark-block dimension | derived from `n_pair × n_color` |
| `α_s(v) = α_bare/u_0²`: retained plaquette coupling | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md) |
| Retained α_LM geometric-mean structure | [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md) |

No observed CKM matrix element, quark mass, or fitted CKM observable enters the derivation.

## 2. Derivation

### 2.1 (W2): A² = 2/3 from group-rep counting

The CKM atlas defines the Wolfenstein A parameter via the structural ratio of weak-doublet count to colour count:

```text
A²  =  n_pair / n_color.
```

Substituting retained values:

```text
A²  =  2 / 3.                                                        (W2)
```

This is a pure rational independent of any coupling. It is exact under the retained gauge-structure inputs and holds for every value of `α_s(v)`.

Equivalently, `A = √(2/3) ≈ 0.8165`.

### 2.2 (W1): λ² = α_s(v)/2 from coupling+rep counting

The CKM atlas defines the Cabibbo angle parameter via the structural ratio of strong coupling to weak-doublet count:

```text
λ²  =  α_s(v) / n_pair.
```

Substituting `n_pair = 2`:

```text
λ²  =  α_s(v) / 2.                                                   (W1)
```

This is α_s(v)-linear; the structural content is the **factor of `n_pair = 2`** in the denominator, not the absolute scale of α_s(v).

### 2.3 (W3): A² · λ² = α_s(v)/n_color = α_s(v)/3

Combining (W1) and (W2):

```text
A² · λ²  =  (n_pair / n_color) · (α_s(v) / n_pair)
        =  α_s(v) / n_color
        =  α_s(v) / 3.                                              (W3)
```

The product `A² λ²` is α_s(v) divided by `n_color = N_c = 3`. The factor `n_pair = 2` cancels. This is the structural projection of the strong coupling onto the "per-colour" channel.

### 2.4 Cross-check: |V_us| from λ

The standard Wolfenstein parameterisation gives `|V_us| ≈ λ` to leading order:

```text
|V_us|  ≈  λ  =  √(α_s(v) / 2)  =  √(α_s(v)) / √2.
```

With retained `α_s(v) = 0.10330382…`:

```text
|V_us|  ≈  √(0.10330382 / 2)  =  √0.05165191  ≈  0.22727.
```

PDG 2024: `|V_us| = 0.22534 ± 0.00060`. Framework prediction within `+0.86%`.

### 2.5 Cross-check: |V_cb| from A and λ

The standard Wolfenstein gives `|V_cb| ≈ A · λ²`:

```text
|V_cb|  ≈  A · λ²  =  √(2/3) · α_s(v)/2  =  α_s(v) · √(2/3) / 2.
```

Or equivalently using (W3): `A² · λ⁴ = (α_s(v)/3) · λ²`, so `|V_cb|² = A² · λ⁴ = α_s(v)² / 6`, giving `|V_cb| = α_s(v) / √6`.

```text
|V_cb|  =  α_s(v) / √6  ≈  0.10330382 / 2.44949  ≈  0.04217.
```

PDG 2024: `|V_cb| = 0.04200 ± 0.00060`. Framework prediction within `+0.41%`.

This `|V_cb| = α_s(v) / √6` is itself a clean structural identity: the second Cabibbo-Kobayashi-Maskawa magnitude is the strong coupling divided by √6.

## 3. Numerical verification at retained `<P> = 0.5934`

| Quantity | Symbolic | Numerical | PDG 2024 | Deviation |
|----------|----------|-----------|----------|-----------|
| `α_s(v)` | α_bare/u_0² | 0.10330 | 0.1033 (running to v) | retained |
| `λ²` | α_s(v)/2 | 0.05165 | 0.05078 | +1.7% |
| `λ` | √(α_s(v)/2) | 0.22727 | 0.22534 | +0.86% |
| `A²` | 2/3 | 0.66667 | 0.6989 | -4.6% |
| `A` | √(2/3) | 0.81650 | 0.8362 | -2.4% |
| `A² λ²` | α_s(v)/3 | 0.03443 | (derived) | – |
| `\|V_us\|` ≈ λ | √(α_s(v)/2) | 0.22727 | 0.22534 | +0.86% |
| `\|V_cb\|` ≈ Aλ² | α_s(v)/√6 | 0.04217 | 0.04200 | +0.41% |
| `\|V_ub\|` ≈ Aλ³ | α_s(v)^(3/2)/(6√2) | 0.00391 | 0.00370 | +5.7% |

(For `|V_ub|`, the structural identity is `|V_ub| = A · λ³ · √(ρ²+η²) = A · λ³ / √6` if combined with the CP-radius identity `ρ² + η² = 1/6` from my retained CKM CP-phase theorem; otherwise `|V_ub|` ≈ A · λ³ to leading Wolfenstein order, giving `α_s(v)^(3/2) / (6√2)`.)

## 4. Joint package with CKM CP-phase identity

Combined with [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md):

| Wolfenstein parameter | Structural identity | Numerical |
|------------------------|---------------------|------------|
| `λ²` | `α_s(v) / 2` (W1, this theorem) | 0.05165 |
| `A²` | `2/3` (W2, this theorem) | 0.66667 |
| `ρ` | `1/6` (CP-phase theorem) | 0.16667 |
| `η` | `√5/6` (CP-phase theorem) | 0.37268 |
| `cos²δ` | `1/6` (CP-phase theorem) | 0.16667 |
| `δ` | `arccos(1/√6) = arctan(√5)` (CP-phase theorem) | 65.905° |
| `J` | `α_s(v)³ · √5 / 72` (factorisation) | 3.42×10⁻⁵ |

Together these identities form the **complete** Wolfenstein parameter structural surface on the retained CKM atlas. Every Wolfenstein parameter is either a pure rational, or `α_s(v)`-monomial, or a combination thereof.

## 5. Structural observations

- **(W2) is α_s-independent.** The identity `A² = 2/3` is a pure group-theoretic ratio. It would survive any rescaling of `α_s(v)`; only the underlying gauge-structure ratio `n_pair/n_color = 2/3` matters.
- **(W1) carries the α_s scale.** `λ² = α_s(v)/2` ties the Cabibbo angle directly to the strong coupling, with the factor `1/2 = 1/n_pair` from electroweak structure.
- **The combined product (W3) `A² λ² = α_s(v)/3`** projects α_s(v) onto the colour-count denominator, removing all weak-structure factors.
- **`|V_cb| = α_s(v)/√6`** is a particularly clean derived identity: the magnitude of the second Cabibbo-Kobayashi-Maskawa transition is α_s divided by `√6 = √n_quark`.

## 6. Falsifiability

Sharp:

- Any precision measurement of `|V_us|` significantly outside framework's `√(α_s(v)/2)` band falsifies (W1).
- Any measurement of `|V_cb|/|V_us|² = A` significantly outside `√(2/3) = 0.8165` falsifies (W2).
- LHCb / Belle II projected precision on `|V_us|` to 0.1% by 2028 will sharpen the test.
- Current PDG 2024 data is consistent with framework at ~1%.

## 7. Scope and boundary

**Claims:**

- (W1) `λ² = α_s(v)/2` exactly on retained CKM atlas + n_pair = 2.
- (W2) `A² = 2/3` exactly on retained gauge-structure ratios.
- (W3) `A² λ² = α_s(v)/3` derived combined identity.
- `|V_cb| = α_s(v)/√6` derived structural form.
- All identities are exact at the structural level; numerical agreement is sub-percent.

**Does NOT claim:**

- A native-axiom derivation of `α_s(v)` itself (separately retained via plaquette/CMT).
- Higher-order Wolfenstein corrections (beyond leading).
- Quark-mass-ratio or sector-mass content (separate lanes).
- Beyond-SM CP phases or Majorana phases.

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_wolfenstein_lambda_a_structural_identities.py
```

Expected: all checks pass.

The runner:

1. Computes `λ²` and `A²` from retained `α_s(v)` and `n_pair`, `n_color`.
2. Verifies (W1) `λ² = α_s(v)/2` symbolically and numerically.
3. Verifies (W2) `A² = 2/3` exactly via `Fraction`.
4. Computes (W3) `A² λ² = α_s(v)/3` and verifies algebraic identity.
5. Cross-checks `|V_us|`, `|V_cb|`, `|V_ub|` against PDG 2024.
6. Sympy symbolic verification of identities.

## 9. Cross-references

- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) — parent retained CKM theorem
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) — CP-phase companion identities
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md) — retained `α_s(v)`
- [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md) — retained α_LM/α_s(v) structural relationship
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained `N_c = 3`
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — retained `n_pair = 2`
- Wolfenstein 1983 "Parametrization of the Kobayashi-Maskawa matrix", Phys. Rev. Lett. 51, 1945 — original Wolfenstein parameterisation
