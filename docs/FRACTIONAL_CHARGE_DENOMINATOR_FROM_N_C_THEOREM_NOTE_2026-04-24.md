# Fractional Charge Denominator From N_c Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-corollary theorem** on `main`. Extracts and packages as its own theorem the structural fact that the SM "third-integer" fractional charges `±1/3, ±2/3` arise specifically from `N_c = 3` via tracelessness on the C^{2 N_c + 2} taste space, combined with the parity of `N_c`. This corollary is implicit in [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) (the `6a + 2b = 0 ⇒ b = −3a` line) and in [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) (denominators in `{1, 3}`), but the **specific identification "denominator = N_c when N_c is odd"** is not currently named.
**Primary runner:** `scripts/frontier_fractional_charge_denominator_from_n_c.py`

---

## 0. Statement

**Theorem (fractional charge denominator from N_c).** On a hypothetical Cl(d)/Z^d framework with one SU(2)_L weak doublet of quarks (N_c colours) and one SU(2)_L weak doublet of leptons (no colour), the unique traceless U(1)_Y generator from the commutant has eigenvalue ratio

```text
Y(Q_L) : Y(L_L)  =  +1 : −N_c                                    (★)
```

(forced by tracelessness `2 N_c · Y(Q_L) + 2 · Y(L_L) = 0`). With the standard electric-charge convention `Q = T_3 + Y/2` and the fixing `Y(L_L) = −1`:

```text
Y(Q_L)  =  +1 / N_c
Q(u_L)  =  +1/2 + 1/(2 N_c)  =  (N_c + 1) / (2 N_c)
Q(d_L)  =  −1/2 + 1/(2 N_c)  =  (1 − N_c) / (2 N_c)
Q(ν_L)  =  +1/2 − 1/2        =  0
Q(e_L)  =  −1/2 − 1/2        =  −1
```

The fractional charge denominator depends on the parity of `N_c`:

```text
denominator  =  N_c           if N_c is odd                       (★★)
              =  2 N_c         if N_c is even
```

Specifically, for the **retained** `N_c = 3` (graph-first SU(3) closure):

```text
Y(Q_L)  =  +1/3                Q(u_L)  =  2/3        Q(d_L)  =  −1/3
```

with denominator exactly `3 = N_c`. This is the SM "third-integer" charge spectrum.

For hypothetical alternative N_c values:

| `N_c` | parity | `Y(Q_L)` | `Q(u_L)` | `Q(d_L)` | denominator | retained? |
|-------|--------|----------|----------|----------|-------------|-----------|
| 1 | odd | 1 | 1 | 0 | 1 | no (no colour) |
| 2 | even | 1/2 | 3/4 | −1/4 | 4 (= 2 N_c) | no |
| **3** | **odd** | **1/3** | **2/3** | **−1/3** | **3 (= N_c)** | **YES** |
| 4 | even | 1/4 | 5/8 | −3/8 | 8 (= 2 N_c) | no |
| 5 | odd | 1/5 | 3/5 | −2/5 | 5 (= N_c) | no |
| 7 | odd | 1/7 | 4/7 | −3/7 | 7 (= N_c) | no |

So the SM "third-integer" charges are not arbitrary — they are forced by the conjunction of `N_c = 3` *being a specific odd integer* with the retained tracelessness commutant structure.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Graph-first SU(3) gauge structure with `N_c = 3` | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Retained SU(2)_L gauge structure | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| Retained Q_L (colour-3 doublet) and L_L (colour-1 doublet) content | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| Retained U(1)_Y commutant tracelessness | [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) |
| Retained SM hypercharge values from anomaly closure | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| Standard electric-charge convention `Q = T_3 + Y/2` | textbook SM |

## 2. Derivation

### 2.1 Tracelessness on C^{2 N_c + 2}

The retained taste space carries the LH content:

- `Q_L`: SU(2) doublet × SU(3) fundamental → multiplicity `2 N_c` (= 2 weak × N_c colour)
- `L_L`: SU(2) doublet × SU(3) singlet → multiplicity `2` (= 2 weak × 1 colour)

The total LH-fermion-state count per generation is `2 N_c + 2`.

A general traceless U(1)_Y generator on this 2-dimensional commutant (with eigenvalues `a` on quarks and `b` on leptons) satisfies

```text
Tr[Y]  =  (2 N_c) · a  +  2 · b  =  0
       ⟺  N_c · a + b  =  0
       ⟺  b  =  −N_c · a.                                          (T)
```

Hence the eigenvalue ratio is

```text
a : b  =  +1 : −N_c                                              (★)
```

up to overall normalisation.

### 2.2 Normalisation from electric-charge convention

With the convention `Q = T_3 + Y/2` and the lepton-doublet hypercharge fixed by the convention `Y(L_L) = −1` (giving `Q(e_L) = −1`):

```text
b  =  Y(L_L)  =  −1     ⟹     a  =  Y(Q_L)  =  +1/N_c
```

(using `b = −N_c a` rearranged to `a = −b/N_c = 1/N_c`).

### 2.3 Electric-charge formulas

The four LH-doublet electric charges follow:

```text
Q(u_L)  =  +1/2  +  Y(Q_L)/2  =  +1/2 + 1/(2 N_c)  =  (N_c + 1) / (2 N_c)
Q(d_L)  =  −1/2  +  Y(Q_L)/2  =  −1/2 + 1/(2 N_c)  =  (1 − N_c) / (2 N_c)
Q(ν_L)  =  +1/2  +  Y(L_L)/2  =  +1/2 − 1/2  =  0
Q(e_L)  =  −1/2  +  Y(L_L)/2  =  −1/2 − 1/2  =  −1
```

### 2.4 Denominator parity dependence

For `Q(u_L) = (N_c + 1) / (2 N_c)`:

- **`N_c` odd**: `N_c + 1` is even, so `gcd(N_c + 1, 2 N_c) = 2`, giving the reduced fraction `(N_c + 1)/2` over `N_c`. The denominator after reduction is `N_c`.
- **`N_c` even**: `N_c + 1` is odd, so `gcd(N_c + 1, 2 N_c) = 1` (since `2 N_c` shares no odd factor with `N_c + 1` when both are coprime parities). The denominator stays at `2 N_c`.

Hence

```text
denominator(Q_quark)  =  N_c           if N_c ∈ {1, 3, 5, 7, 9, …} (odd)
                      =  2 N_c         if N_c ∈ {2, 4, 6, 8, …}    (even)
```

### 2.5 Specialisation to retained N_c = 3

```text
N_c = 3        (retained)
Y(Q_L)        = +1/3
Q(u_L)         = 4/6 = 2/3        (denominator 3 = N_c)
Q(d_L)         = −2/6 = −1/3      (denominator 3 = N_c)
Q(ν_L), Q(e_L) = 0, −1            (integer denominators)

Spectrum:  {0, ±1/3, ±2/3, ±1}
Fractional denominators:  3 = N_c.
```

The famous "third-integer" SM fractional charges are exactly the imprint of `N_c = 3`. ∎

## 3. Joint constraint with Witten Z₂

The Witten Z₂ anomaly cancellation theorem ([`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)) requires the SU(2)-doublet count per generation `N_D = N_c + 1` to be **even**, i.e. `N_c` must be **odd**.

Combined with the present theorem:

| `N_c` | Witten consistent? | Frac. denominator |
|-------|---------------------|---------------------|
| 1 | ✓ (no colour, trivial) | 1 (integer) |
| 2 | ✗ (Witten broken) | n/a |
| **3** | **✓** | **3 = N_c** |
| 4 | ✗ (Witten broken) | n/a |
| 5 | ✓ | 5 = N_c |
| 7 | ✓ | 7 = N_c |

So **only odd N_c is gauge-consistent**, and on the consistent set the fractional denominator equals N_c. The "denominator = 2 N_c" case (even N_c) is disallowed by Witten.

The retained `N_c = 3` is therefore doubly distinguished:
1. Witten Z₂ consistent (3 + 1 = 4 even).
2. Fractional denominator = N_c = 3 (clean third-integer charges).

These are independent structural witnesses for the retained N_c = 3 (beyond the underlying graph-first SU(3) closure that derives N_c = 3 directly).

## 4. Falsification

Sharp:

- A discovery of any fundamental fermion with non-third-integer fractional electric charge (e.g. `Q = 1/4`, `1/5`, `2/7`, etc.) would falsify the retained `N_c = 3`. Current data: no such particle observed.
- A discovery of a fundamental quark with charge outside `{±1/3, ±2/3}` would falsify the retained one-generation closure.
- The observed quark charges (`u: +2/3`, `d: −1/3`, etc.) confirm `N_c = 3` and the third-integer denominator pattern.

Pattern testing: every quark observed (u, d, c, s, t, b) has charge in `{±1/3, ±2/3}`. Six independent confirmations of the structural prediction.

## 5. Structural observations

- **Tracelessness is the load-bearing condition.** Without it, the U(1)_Y generator would have no canonical normalisation, and the eigenvalue ratio would be free.
- **The ratio is `1 : −N_c`, not `1 : −1`.** The asymmetry comes from the fact that quarks have N_c colour copies while leptons do not. If the framework had `0` quarks (no colour), the ratio would be undefined (no commutant U(1)).
- **The factor of 2 in `Q = T_3 + Y/2`** is the ONLY place where parity of N_c enters denominator reduction. With a different convention (e.g. `Q = T_3 + Y` and Y rescaled), the denominator pattern could shift but the *ratio* `Y(Q_L) : Y(L_L) = 1 : −N_c` is convention-independent.
- **For N_c = 1 (no colour):** Q(u_L) = (1+1)/2 = 1 (integer), Q(d_L) = 0 (integer). All charges integer — no "fractional structure" exists. The fractional denominator of N_c = 3 is the **first non-trivial value** in the natural sequence.

## 6. Scope and boundary

**Claims:**

- Eigenvalue ratio `Y(Q_L) : Y(L_L) = 1 : −N_c` from tracelessness on C^{2 N_c + 2}.
- Electric-charge denominator pattern: `N_c` for odd N_c, `2 N_c` for even.
- Retained `N_c = 3` gives third-integer SM charges exactly.
- Joint with Witten Z₂ → only odd N_c is gauge-consistent.

**Does NOT claim:**

- Native-axiom uniqueness of `N_c = 3` (separately retained via [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)).
- Free hypercharge values of right-handed completions (that is the scope of [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)).
- Beyond-SM scenarios with multiple Higgs doublets, additional U(1)s, or chiral RH content (those would change the trace-condition analysis).
- A full derivation of the convention `Q = T_3 + Y/2` (textbook).

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_fractional_charge_denominator_from_n_c.py
```

Expected: all checks pass.

The runner:

1. Solves the tracelessness equation `2 N_c · Y_q + 2 · Y_ℓ = 0` symbolically and numerically.
2. Verifies eigenvalue ratio `(★)` for retained `N_c = 3`.
3. Computes electric-charge spectrum for `N_c ∈ {1, 2, 3, 4, 5, 6, 7}` via exact `Fraction` arithmetic.
4. Verifies denominator parity rule `(★★)`.
5. Cross-checks with Witten Z₂ (only odd N_c is anomaly-consistent).
6. Confirms retained N_c = 3 gives `Q ∈ {0, ±1/3, ±2/3, ±1}`.

## 8. Cross-references

- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) — `6a + 2b = 0 ⇒ b = −3a` derivation
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — `{1, 3}` denominator set established
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained `N_c = 3`
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md) — odd-N_c Witten consistency joint constraint
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — retained Q_L, L_L content
- Gell-Mann & Nishijima 1953 "Charge independence for V particles", Phys. Rev. 91, 512 — original Q = T_3 + Y convention
