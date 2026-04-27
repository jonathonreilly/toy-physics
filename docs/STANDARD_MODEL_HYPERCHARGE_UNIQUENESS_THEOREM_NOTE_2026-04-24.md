# Standard Model Hypercharge Uniqueness from Anomaly Cancellation

**Date:** 2026-04-24
**Status:** **proposed_retained standalone structural-uniqueness theorem** on `main`. Extracts and packages as its own theorem the uniqueness claim that is *used but not separately proposed_retained* in [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) Step 2 and implicitly carried by [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md). The proposed_retained anomaly-forces-time theorem explicitly states: *"The time theorem only needs the existence of an SU(2)-singlet opposite-chirality completion; it does not rely on uniqueness from anomaly arithmetic alone."* This note closes the conditional uniqueness statement as a standalone proposed_retained row; it does not rederive the proposed_retained left-handed surface, the singlet right-handed completion requirement, or the neutral-singlet input.
**Primary runner:** `scripts/frontier_sm_hypercharge_uniqueness.py`

---

## 0. Statement

**Theorem (SM hypercharge uniqueness from anomaly cancellation).** Given:

1. the retained left-handed content
   `Q_L : (2, 3)_{+1/3}` (quark doublet, 3 colors) and
   `L_L : (2, 1)_{-1}` (lepton doublet)
   ([`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md));
2. the retained requirement of an anomaly-cancelling right-handed
   SU(2)-singlet completion
   `u_R : (1, 3)_{y_1}, d_R : (1, 3)_{y_2}, e_R : (1, 1)_{y_3}, ν_R : (1, 1)_{y_4}`
   ([`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) Step 2);
3. vanishing of the three right-handed-sector-constraining anomaly traces
   `Tr[Y] = 0`, `Tr[Y³] = 0`, `Tr[SU(3)² Y] = 0`
   for the full (LH + RH) content (the mixed `SU(2)²Y` trace is already zero
   on the retained left-handed doublet surface and adds no singlet-RH
   constraint);
4. the neutral-singlet identification `y_4 ≡ Y(ν_R) = 0`
   ([`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md));
5. the physical electric-charge labelling
   `Q(u_R) > 0` (u_R is the up-type quark singlet)

then the right-handed hypercharges are **uniquely** determined:

```text
y_1 = +4/3,  y_2 = −2/3,  y_3 = −2,  y_4 = 0.                 (★)
```

These are the exact Standard Model hypercharges. Equivalently, the complete electric-charge spectrum of one generation is forced to the rational set `{0, ±1/3, ±2/3, ±1}`, with denominators exactly `{1, 3}`.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| left-handed Q_L, L_L content | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| SU(2)-singlet right-handed completion | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) Step 2 |
| anomaly-cancellation as a quantum-consistency requirement | same, Step 1 (Adler–Bell–Jackiw) |
| neutral-singlet identification `Y(ν_R) = 0` | [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) |
| electric-charge convention `Q = T_3 + Y/2` in the doubled-hypercharge convention used by the retained notes | standard SM bookkeeping |

No observed charge, mass, or cross-section is used.

Throughout this note, `Y` is the doubled Standard Model hypercharge used by
the retained anomaly notes: `Q = T_3 + Y/2`, and for `SU(2)` singlets
`Q = Y/2`.

## 2. Derivation

### 2.1 Anomaly traces for the full (LH + RH) content

Summing contributions with chirality sign (LH with `+`, RH with `−`, or equivalently sum all in the LH-conjugate frame):

**Tr[Y]**: Every chiral fermion contributes `Y` weighted by its SU(3) × SU(2) multiplicity.

```text
Tr[Y]  =  6 · (1/3) + 2 · (−1) − 3·y_1 − 3·y_2 − y_3 − y_4
       =  2 − 2 − 3(y_1 + y_2) − y_3 − y_4
       =  −3(y_1 + y_2) − y_3 − y_4                             (E1)
```

**Tr[SU(3)² Y]**: Only quark contributions (SU(3) fundamentals), weighted by the SU(3) Dynkin index `T(3) = 1/2` and SU(2) multiplicities:

```text
Tr[SU(3)² Y]  =  (1/2) · [ 2 · (1/3) − y_1 − y_2 ]              (E2)
```

where the factor 2 in the LH sum is the SU(2)-doublet multiplicity and quarks contribute with SU(3) Dynkin index 1/2 per colour factor.

**Tr[Y³]**: Cubic trace over all chirality-signed fermions:

```text
Tr[Y³]  =  6 · (1/3)³ + 2 · (−1)³ − 3·y_1³ − 3·y_2³ − y_3³ − y_4³
       =  2/9 − 2 − 3(y_1³ + y_2³) − y_3³ − y_4³
       =  −16/9 − 3(y_1³ + y_2³) − y_3³ − y_4³                 (E3)
```

(The `−16/9` is the LH-only cubic contribution, now explicitly packaged in
[`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md).)

### 2.2 Anomaly-cancellation system

Setting (E1), (E2), (E3) to zero:

```text
(A1)  3(y_1 + y_2) + y_3 + y_4  =  0
(A2)  y_1 + y_2                 =  2/3
(A3)  3(y_1³ + y_2³) + y_3³ + y_4³  =  −16/9
```

(E2) becomes (A2) after clearing the `1/2` factor.

### 2.3 Reduction under neutral-singlet identification

Imposing `y_4 = 0` (ν_R is the neutral singlet):

From (A1): `y_3 = −3(y_1 + y_2) − y_4 = −3·(2/3) − 0 = −2`.

So `y_3 = −2` uniquely under (A1, A2, y_4 = 0).

Substituting into (A3):

```text
3(y_1³ + y_2³) + (−2)³ + 0³  =  −16/9
3(y_1³ + y_2³) − 8           =  −16/9
3(y_1³ + y_2³)               =  8 − 16/9  =  72/9 − 16/9  =  56/9
y_1³ + y_2³                  =  56/27.                         (A3′)
```

### 2.4 Closed-form solve of the y_1, y_2 system

From (A2): `y_2 = 2/3 − y_1`. Substitute into (A3′):

```text
y_1³ + (2/3 − y_1)³  =  56/27.
```

Expand `(2/3 − y_1)³ = (2/3)³ − 3(2/3)² y_1 + 3(2/3) y_1² − y_1³ = 8/27 − (4/3) y_1 + 2 y_1² − y_1³`:

```text
y_1³ + 8/27 − (4/3) y_1 + 2 y_1² − y_1³  =  56/27
2 y_1² − (4/3) y_1 + 8/27                =  56/27
2 y_1² − (4/3) y_1                        =  48/27  =  16/9.
```

Multiply by 9:

```text
18 y_1² − 12 y_1 − 16  =  0
9 y_1² − 6 y_1 − 8     =  0
y_1  =  [6 ± √(36 + 288)] / 18  =  [6 ± 18] / 18.
```

Two solutions: `y_1 = 4/3` or `y_1 = −2/3`.

These two solutions are **related by the u_R ↔ d_R relabelling** (since swapping `y_1 ↔ y_2` preserves (A2), (A3′)): if `y_1 = 4/3` then `y_2 = −2/3`, and vice versa.

### 2.5 Imposing the electric-charge labelling

The electric-charge formula is `Q = Y/2` on `SU(2)` singlets in the doubled-hypercharge convention. Therefore the `up-type` label is the member of the quark-singlet pair with positive electric charge. Identifying `u_R` as up-type requires `Q(u_R) = y_1/2 > 0`, equivalently `y_1 > 0`, fixing `y_1 = +4/3` and `y_2 = −2/3`. ∎

### 2.6 Collected result

Under inputs (1–5), the unique solution is

```text
y_1 = +4/3 (u_R),  y_2 = −2/3 (d_R),  y_3 = −2 (e_R),  y_4 = 0 (ν_R).
```

The electric-charge spectrum in one generation is therefore

```text
Q ∈ { 0, ±1/3, ±2/3, ±1 }                                       (★★)
```

with denominators exactly `{1, 3}`, i.e. the retained inputs force quark fractional charge in units of `1/3` and the unit lepton charge `±1`. No continuous family, no additional branch survives.

## 3. Structural observations

- **Four unknowns, three anomaly equations, one neutrality input ⇒ uniqueness up to u_R ↔ d_R.** The electric-charge labelling breaks the residual two-fold degeneracy.
- **Rationality is forced.** The system `(A1, A2, A3′)` has rational coefficients `{−2/3, 2/3, 56/27}`. The discriminant of the reduced quadratic is `324 = 18²`, a perfect square. Uniqueness proceeds without any extension of `ℚ`.
- **Denominators `{1, 3}` are structural.** The `1/3` appears because the LH quark hypercharge `1/3` enters (A2) directly; it is not a fit.
- **The u_R ↔ d_R residual relabelling is the only discrete ambiguity.** Any proposed extension of this theorem (e.g. to fourth-generation species or to different left-handed content) must rebuild the entire anomaly system.

## 4. Relationship to adjacent retained rows

| Row | Status before | Status after |
|-----|---------------|--------------|
| LH content `Q_L + L_L` | retained ([`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)) | unchanged |
| anomaly-forced `3+1` | retained ([`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)) | unchanged |
| existence of anomaly-cancelling RH completion | retained (ditto, Step 2) | unchanged |
| one-generation closure at SM hypercharges | retained ([`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)) | unchanged |
| **RH hypercharges uniqueness at SM values** | *(not separately packaged; used but not retained as standalone)* | **retained structural uniqueness theorem (this note)** |
| electric-charge quantization `Q ∈ {0, ±1/3, ±2/3, ±1}` | implicit | **retained structural corollary** |

The uniqueness claim was previously a load-bearing but unlabelled step inside the time theorem and the one-generation closure note. This note packages it as a named retained row so that:

1. The electric-charge quantization statement has an explicit retained authority.
2. Future extensions (e.g. fourth-generation searches, dark-sector hypercharge proposals, any extension to the LH content) can cite this note as the base uniqueness statement they must modify.
3. Reviewer-facing claim structure now separates *existence* (time theorem) from *uniqueness* (this note).

## 5. What this theorem does and does not claim

**Claims:**

- Under inputs (1–5), the RH hypercharges are exactly `(4/3, −2/3, −2, 0)`, no freedom.
- Electric charges in one generation are rational with denominators `{1, 3}`; this is **structural**, not a fit.
- The residual discrete relabelling `u_R ↔ d_R` is the only ambiguity removed by the electric-charge convention.

**Does NOT claim:**

- Uniqueness across generations (each generation independently satisfies the same anomaly system; inter-generational labelling ambiguities — e.g. the PMNS mixing — are separate).
- A native-axiom derivation of `Y(ν_R) = 0`; the neutral-singlet identification is treated here as an input (see [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)).
- Uniqueness of the gauge group itself; assumed to be `SU(2) × SU(3) × U(1)_Y` from the retained Cl(3) chain ([`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md), [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)).
- Extension to beyond-SM hypercharge assignments (fourth generation, mirror fermions, etc.); this theorem explicitly uses the retained three-generation structure's one-generation template.

## 6. Falsifiability

Indirect, via the retained structural inputs:

- Any detection of a fermion with electric charge **outside** `{0, ±1/3, ±2/3, ±1}` (e.g. `±2/3 + ε` with `ε ≠ 0`) falsifies `(★★)`, hence the theorem.
- Any detection of a fundamental non-SU(2)-singlet right-handed fermion violates input (2), hence breaks the derivation.
- A validated chiral matter sector with the same retained left-handed surface and neutral singlet but different singlet-RH hypercharges would falsify the uniqueness theorem. A sector with different left-handed content, different gauge group, or additional mirror/vectorlike matter would instead be outside this theorem's hypotheses.

The theorem passes current data: all SM fermions have the hypercharges listed in `(★)`, to within experimental precision, and no `ΔQ` deviation is observed.

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_sm_hypercharge_uniqueness.py
```

Expected: `PASS=30, FAIL=0`.

The runner:

1. Sets up the anomaly system (E1, E2, E3) in exact rational arithmetic.
2. Imposes `y_4 = 0` and the full system on `(y_1, y_2, y_3)`.
3. Enumerates all rational solutions (expected: exactly two, related by `y_1 ↔ y_2`).
4. Verifies the `Q(u_R) > 0` labelling picks `y_1 = +4/3` uniquely.
5. Reports electric-charge denominators to confirm `{1, 3}`.

## 8. Cross-references

- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) — existence of the RH completion, anomaly traces `−16/9`, `1/3` cited
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — LH content
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) — `Y(ν_R) = 0` pin
- [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) — named `Tr[Y^2]` / GUT-normalization arithmetic on the same one-generation content
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) — wider closure whose hypercharge step is now retained standalone
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) — why the same template applies per generation
- Adler 1969, Bell–Jackiw 1969 — original ABJ anomaly
