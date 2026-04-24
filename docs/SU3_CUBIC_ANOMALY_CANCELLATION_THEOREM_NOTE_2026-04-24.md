# SU(3)³ Cubic Gauge Anomaly Cancellation Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-anomaly theorem** on `main`. Closes the SU(3)³ pure-gauge cubic anomaly that is *not* listed in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) Step 1 (which catalogues only the perturbative-Y conditions and the Witten Z₂; the cubic gauge-only conditions are absent from that table). A standalone closure is needed because SU(3)³ cancellation is non-trivial — it depends on the precise ratio of SU(3)-fundamental and anti-fundamental fermion content per generation, and a wrong content would break it.
**Primary runner:** `scripts/frontier_su3_cubic_anomaly_cancellation.py`

---

## 0. Statement

**Theorem (SU(3)³ cubic gauge anomaly cancellation).** For SU(3) gauge theory with chiral Weyl fermions, the cubic anomaly coefficient is

```text
A^{abc}(SU(3)³)  =  d^{abc}  ·  Σ_{R}  ε_R  ·  A(R)                    (*)
```

where `d^{abc}` is the symmetric structure constant of SU(3) (non-zero), `ε_R = +1` for left-handed, `ε_R = −1` for right-handed (or equivalently the chirality phase in the LH-conjugate frame), and `A(R)` is the cubic anomaly index of the SU(3) representation `R`:

```text
A(3)   =  +1     A(3̄)  =  −1     A(1)   =  0     A(8)   =  0     A(6)   =  +7   ...
```

Anomaly cancellation requires `Σ ε_R · A(R) = 0`.

On the retained one-generation SM content (Q_L + L_L + RH completion), the SU(3)-charged fields are:

| field | SU(3) rep (LH-conj. frame) | SU(2) mult | colour mult counted | A(R) | net contribution |
|-------|----------------------------|------------|----------------------|------|-------------------|
| `Q_L` | 3 | 2 | (already in 3) | +1 | `2 × 1 = +2` |
| `u_R^c` | 3̄ | 1 | (already in 3̄) | −1 | `1 × −1 = −1` |
| `d_R^c` | 3̄ | 1 | (already in 3̄) | −1 | `1 × −1 = −1` |

```text
Σ ε · A(R)  =  +2 − 1 − 1  =  0.                                         (*)
```

The SU(3)³ cubic gauge anomaly cancels identically on the retained content. Equivalently, the framework's chiral fermion content is "vector-like in net 3 vs 3̄ count" — there are exactly 2 fundamentals (from Q_L doublet) and 2 anti-fundamentals (from u_R^c, d_R^c), making `Σ A(R) = 0`.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| One-generation SM content with ν_R | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) |
| Graph-first SU(3) gauge structure with N_c = 3 | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| LH content `Q_L`, `L_L` and SU(3) representations | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| Anomaly index `A(R)` for SU(3) representations | textbook (Adler 1969, Bardeen 1969); standard SU(3) Lie algebra fact |

## 2. Background: cubic anomaly index `A(R)`

For a chiral Weyl fermion in SU(3) representation `R`, the cubic anomaly contribution is parametrized by the **anomaly index** `A(R)`, defined by

```text
Tr_R [ T^a {T^b, T^c} ]  =  A(R) · d^{abc} / 2.
```

`d^{abc}` is the totally symmetric SU(3) structure constant (non-zero for SU(3), unlike SU(2)).

Standard values:
- `A(1)` (singlet) = 0
- `A(3)` (fundamental) = +1
- `A(3̄)` (anti-fundamental) = −1
- `A(8)` (adjoint) = 0
- `A(6)` (symmetric tensor) = +7
- `A(6̄)` = −7
- General: `A(R̄) = −A(R)`

The cubic anomaly coefficient of a gauge theory with matter content `{R_i}` and chirality assignments is

```text
A^{abc}  =  d^{abc} ·  ½ ·  Σ_i ε_{R_i} A(R_i),
```

and gauge-invariance requires `Σ ε_R A(R) = 0`.

## 3. Derivation on retained SM content

### 3.1 Enumerate SU(3)-charged fields

In the LH-conjugate frame (all chiral Weyl fermions written as left-handed):

| field | SU(3) rep | colour-rep dimension | SU(2) multiplicity |
|-------|-----------|----------------------|---------------------|
| `Q_L` | 3 (fundamental) | 3 | 2 (doublet) |
| `u_R^c` | 3̄ (anti-fundamental) | 3 | 1 (singlet) |
| `d_R^c` | 3̄ (anti-fundamental) | 3 | 1 (singlet) |
| `L_L` | 1 (singlet) | 1 | 2 (doublet) |
| `e_R^c` | 1 (singlet) | 1 | 1 |
| `ν_R^c` | 1 (singlet) | 1 | 1 |

Only the SU(3)-charged fields (those with rep ≠ 1) contribute to the SU(3)³ trace. The leptonic fields are SU(3) singlets and contribute `A(1) = 0`.

### 3.2 Sum the anomaly indices

For each SU(3)-charged field, the contribution to the anomaly is `(SU(2) multiplicity) × A(R)`:

```text
Q_L      :  2 × A(3)  =  2 × (+1) =  +2
u_R^c    :  1 × A(3̄) =  1 × (−1) =  −1
d_R^c    :  1 × A(3̄) =  1 × (−1) =  −1
L_L      :  2 × A(1)  =  2 ×  0   =   0
e_R^c    :  1 × A(1)  =  1 ×  0   =   0
ν_R^c    :  1 × A(1)  =  1 ×  0   =   0
                                  ─────
                                  Σ = 0    ✓ (*)
```

### 3.3 Net 3-vs-3̄ count

Equivalently, the cancellation can be phrased as a **net SU(3)-fundamental count**:

- Total `3` representations (LH frame, each weighted by SU(2) mult): `Q_L` contributes `2 × (3) = 2 fundamentals`.
- Total `3̄` representations: `u_R^c + d_R^c = 1 + 1 = 2 anti-fundamentals`.
- Net: `2 − 2 = 0`.

This is a **vector-like** content from SU(3)'s perspective: there are exactly as many `3`s as `3̄`s in the chiral content, when SU(2) multiplicities are counted. This vector-like structure is what makes SU(3)³ cancel.

## 4. Falsification scenarios

Any modification that disturbs the net `3 − 3̄ = 0` count breaks SU(3)³ cancellation:

| Hypothetical content | net count `Σ ε A(R)` | Cancellation? |
|-----------------------|----------------------|---------------|
| Retained SM (Q_L + u_R + d_R per gen) | `+2 − 1 − 1 = 0` | ✓ |
| Add a 4th chiral 3-fundamental quark (no partner) | `+2 + 1 − 1 − 1 = +1` | ✗ |
| Add a sextet (6) of SU(3) | `+7 + 2 − 1 − 1 = +7` | ✗ |
| Add a chiral 3̄ partner for the 4th-gen quark | `+2 + 1 − 1 − 1 − 1 = 0` | ✓ (vector-like restored) |
| Remove `u_R^c` (no completion) | `+2 − 1 = +1` | ✗ |
| Standard 3+1 mirror world | `+2 − 1 − 1 + 2 − 1 − 1 = 0` | ✓ (mirror cancels) |

The retained SM content is precisely vector-like in SU(3) — the LH `Q_L` doublet provides 2 fundamentals, and the RH `u_R, d_R` singlets provide 2 anti-fundamentals, exactly cancelling.

## 5. Comparison with SU(2)³ anomaly (auxiliary)

For completeness: the SU(2)³ pure-gauge anomaly is structurally absent for SU(2) regardless of matter content, because

```text
d^{abc}(SU(2))  =  0
```

(the totally symmetric structure constant of SU(2) is zero — equivalently, all SU(2) representations are pseudo-real and their cubic anomaly index vanishes). So `A^{abc}(SU(2)³) ≡ 0` for any matter content; this requires no per-content verification.

The retained framework's SU(2)³ closure is therefore "automatic" while SU(3)³ is "non-trivial" and depends on the specific retained content.

## 6. Consequences

### 6.1 Pure-gauge cubic-anomaly closure complete

Combined with the trivial SU(2)³ = 0:

```text
SU(2)³   ≡  0  identically (group-theoretic)
SU(3)³   =  0  on retained SM content (matter-content)            (this theorem)
```

so all pure-gauge cubic anomalies vanish on the retained framework.

### 6.2 Distinct from perturbative-Y conditions

This closure is structurally separate from the conditions catalogued in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md):
- `Tr[Y]` (gravitational mixed) — covered there
- `Tr[Y³]` (cubic U(1)) — covered there
- `Tr[SU(3)² Y]` (mixed colour-Y) — covered there
- `Tr[SU(2)² Y]` (mixed weak-Y) — covered there
- Witten Z₂ (SU(2) topological) — covered in [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)

The SU(3)³ cubic-gauge condition is the missing seventh anomaly condition for full SM gauge consistency, now closed here.

### 6.3 Structural force on RH content

The cancellation requires both `u_R^c` and `d_R^c` to be present as SU(3) anti-fundamentals — neither can be omitted without restoring the anomaly. Combined with the retained one-generation closure (which fixes `u_R, d_R` from anomaly-forces-time + hypercharge uniqueness), SU(3)³ provides an **independent** structural witness for the same RH-completion content.

### 6.4 Restriction on extensions

Adding any chiral SU(3)-charged matter must preserve the `Σ ε A(R) = 0` condition. This rules out:
- Adding a chiral fundamental without its anti-fundamental partner
- Adding an SU(3) sextet (`A(6) = +7`) without a sextet-bar
- Adding asymmetric tensor representations chirally

Any retained-framework extension to dark-quark sectors (e.g., chiral confining mirror) must explicitly close SU(3)³ on the extended content.

## 7. Scope and boundary

**Claims:**

- (*) `Σ ε A(R) = 0` for SU(3)³ on retained SM content with ν_R.
- The retained SM is "vector-like in net SU(3) fundamental count" (2 `3`s and 2 `3̄`s when SU(2) multiplicities are counted).
- SU(2)³ ≡ 0 group-theoretically (auxiliary).

**Does NOT claim:**

- The perturbative ABJ anomaly conditions (covered in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) and [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)).
- The Witten Z₂ global anomaly (covered in [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)).
- Native-axiom uniqueness of the RH SU(3) representations (assumed from one-generation closure).
- A native-axiom derivation of `N_c = 3` (separate from [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)).
- That the only SU(3)³-anomaly-free completion is the SM (other vector-like extensions exist; this theorem only says retained SM works).

## 8. Falsifiability

Sharp:

- Discovery of any chiral SU(3)-charged matter content giving `Σ ε A(R) ≠ 0` would falsify the framework's gauge consistency.
- LHC searches for chiral exotic colour content (e.g., 4th-generation quarks without partners, SU(3) sextets) constrain the framework.
- Current data: no exotic chiral SU(3) content beyond SM. Framework consistent.

## 9. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_su3_cubic_anomaly_cancellation.py
```

Expected: all checks pass.

The runner:

1. Enumerates SU(3)-charged fermions on retained content with anomaly indices `A(R)`.
2. Sums `Σ ε A(R)` weighted by SU(2) multiplicity → verifies = 0.
3. Tests falsification scenarios (4th-gen quark only, sextet, removed RH partner) → confirms each gives non-zero anomaly.
4. Confirms the "net 3 − 3̄ = 0" structural form.
5. Verifies SU(2)³ ≡ 0 trivially (d^{abc} = 0 for SU(2)).

## 10. Cross-references

- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) — perturbative-Y anomaly conditions (does not include SU(3)³)
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — uniqueness from perturbative-Y anomaly system
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md) — global SU(2) topological anomaly
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md) — global B-L anomaly closure
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) — retained content
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained N_c = 3
- Adler 1969 "Axial vector vertex in spinor electrodynamics", Phys. Rev. 177, 2426 — original ABJ
- Bardeen 1969 "Anomalous Ward identities", Phys. Rev. 184, 1848 — non-abelian ABJ
