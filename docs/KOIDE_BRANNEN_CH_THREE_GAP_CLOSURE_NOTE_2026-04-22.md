# Koide Brannen — Callan-Harvey Candidate: Sharpening & Alternate ABSS Route

**Date:** 2026-04-22
**Lane:** Charged-lepton Koide Brannen phase δ = 2/9.
**Status:** **Conditional support sharpening, NOT closure.** A first version of this note (commit b947506b) claimed to close the three open items in `docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md` §3. A hostile review correctly identified that the closure was not achieved (P0 critiques reproduced in §1 below). This revision is honest about the support-level status of the Callan-Harvey route and offers an alternate ABSS-equivariant-descent attempt in §10.
**Primary runner:** `scripts/frontier_koide_brannen_ch_three_gap_closure.py` (16/16 PASS — as a numerical consistency harness, not a closure theorem).

---

## 0. The three open items being targeted

From `docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md` §3, the bridge

```text
δ_Berry = (anomaly inflow rate) × (1D integration length)
        → δ = (2/9) × 1 = 2/9 rad
```

was flagged as missing three load-bearing steps:

1. a theorem that the charged-lepton **selected-line Berry phase** is the relevant Callan-Harvey descent quantity;
2. a **derivation of the descent factor 1**, rather than the assertion "unit lattice cell = unit clock-tick = one generation";
3. an actual constructed **anomaly-inflow current** or **operator map** from the ambient anomaly sector to the selected-line CP¹ carrier.

Two routes are explored below:

- **§3–§9 (CH route, support only).** The CH-descent attempt at these three items, preserved as the best-available support-level construction, with the reviewer's P0 critiques incorporated in-line as scope qualifiers. This does NOT constitute closure.
- **§10 (ABSS alternate route).** An attempt to close via direct Z_3-equivariant Atiyah-Bott-Segal-Singer descent on the selected-line CP¹, which does not rely on a bulk-to-defect inflow current. Honest about what it achieves and what it still leaves open (the dimensionless↔radian identification).

---

## 1. Reviewer P0 critiques (preserved verbatim for scope)

The following three P0 critiques from hostile review were correctly identified and are preserved here as explicit scope qualifiers of the CH route:

- **P0 on Gap 3.** *"The claimed anomaly-to-CP¹ map collapses to a trivial charge operator and then switches to the pre-existing Koide phase generator. The note claims Q_Σ acts as Y_q σ_3 on the doublet, but the construction immediately before it makes Q_Σ homogeneous Y_q multiplication on generation sites, which Fourier-transforms to Y_q I, not a nontrivial doublet generator. The runner confirms exactly that: Q_site = Y_q I_3 is trivial on the projective ray, then replaces it with the already-known conjugate-pair phase winding from the selected-line Koide state. That does not construct a Callan-Harvey operator map from the ambient anomaly current to the selected-line CP^1 carrier; it reuses the target Berry structure as the generator."*

- **P0 on Gap 2.** *"The Ω = 1 step is still a chosen anomaly-active normalization, not a derived retained theorem. The proof of Ω = 1 sets both transverse and tangent windings to the minimal nonzero value 1, then later justifies that choice by saying the bridge must live in the anomaly-active sector and the zero-flux sector would be inconsistent with the desired mechanism. That is the same missing normalization in new language: the derivation does not force the physical defect tube to carry exactly one unit of each winding, it selects that sector because it yields the target bridge. So the load-bearing descent factor remains assumed rather than derived from retained framework data."*

- **P0 on Gap 1.** *"Gap 1 is closed only by matching two preassigned numbers, not by proving Berry holonomy equals Callan-Harvey descent for the physical observable. The identification theorem says the Berry phase and CH phase are 'phases of the same wavefunction' and therefore equal, but that is exactly the missing bridge statement, not a derivation. The runner then implements this as δ_Berry from the existing Koide selected-line amplitude and δ_CH = c·Ω with the already-chosen Ω = 1, and calls the near-equality a closure. Nothing here derives a nontrivial map showing that the physical selected-line Berry observable is the Callan-Harvey descended phase; it only shows consistency after both sides have been normalized to 2/9."*

These three critiques are accepted. The CH route as presented in §3–§9 below is **support-level consistency**, not closure.

---

## 2. Setup — defect, zero-mode bundle, ambient anomaly (unchanged from candidate note)

### 2.1 Bulk data

- Bulk manifold M = Z³ × R (physical lattice × single clock, by LP + AFT).
- U(1)_Y compact (HYP) with Dirac quantization of Y-flux (LQC):
  ```text
  (1/2π) ∫_{plaquette} F_Y ∈ Z    and    (1/2π) ∫_{edge × Δt} F_Y ∈ Z
  ```
- Per-generation 4D anomaly (retained arithmetic):
  ```text
  c := Tr[Y³]_{q_L} per gen = (2d)(1/d)³ = 2/d² = 2/9     (d = 3)
  ```

### 2.2 Codim-2 defect Σ and zero-mode bundle

Defect Σ = body-diagonal × time worldsheet (codim-2 in 4D). Zero-mode bundle at body-diagonal fixed sites: V = C³. Under retained Z_3 action (cyclic permutation):

```text
V = L₁ ⊕ L_ω ⊕ L_{ω̄}
```

Koide constraint σ_1 = 1/2 (from Q = 2/3 ≡ KFS) fixes the singlet occupancy; dynamical CP¹ carrier is **P(L_ω ⊕ L_{ω̄})**.

### 2.3 Retained ingredients (unchanged)

| Tag | Ingredient | Reference |
|-----|-----------|-----------|
| A0  | Cl(3) on Z³ | retained |
| LP  | Physical-lattice axiom | retained |
| AFT | ANOMALY_FORCES_TIME (3+1 single-clock + retained Y) | ANOMALY_FORCES_TIME_THEOREM |
| TGO | Body-diagonal ↔ generation | THREE_GENERATION_OBSERVABLE_THEOREM_NOTE |
| HYP | U(1)_Y compact from commutant | HYPERCHARGE_IDENTIFICATION_NOTE |
| LQC | Lattice U(1) compact + Dirac quantization | MONOPOLE_DERIVED_NOTE |
| KFS | Koide Fourier form, σ_1 = 1/2 | KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19 |
| NEF | Doublet conjugate-pair n_eff = 2 | KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20 |

---

## 3. CH Gap 3 attempt — anomaly-inflow current and operator map (**support only**)

### 3.1 The bulk CS_3 form (mathematically clean)

The bulk Y-current anomaly ∂_μ J^μ_Y = −(c/8π²) F_Y ∧ F_Y admits descent via the Chern-Simons 3-form

```text
CS_3 := (c/4π) A_Y ∧ dA_Y     with    dCS_3 = (c/4π) F_Y ∧ F_Y
```

This is standard and mathematically unambiguous.

### 3.2 Localized inflow current J^CH (mathematically clean)

The CH inflow current `J^CH = CS_3 |_{T_Σ}` is a well-defined 3-form on the tube T_Σ around the defect. Its restriction formula `dJ^CH = c · δ²_⊥(Σ) · ω_tan` is standard.

### 3.3 Where the CH identification fails on its own terms (**P0 Gap 3**)

*Hostile critique preserved:*

The retained U(1)_Y hypercharge Y_q = 1/d is **homogeneous across the three generations** — each body-diagonal fixed site carries the same Y_q. Therefore the bulk-to-defect restriction of J^μ_Y, integrated over the transverse plaquette, produces the site-diagonal operator

```text
Q_Σ = Y_q · I₃   on V = C³
```

in the generation basis. Fourier-transforming to the Z_3 basis: `Q_Σ = Y_q · I₃` is **still** the scalar operator — the Fourier matrix is unitary, so the scalar identity pulls back to a scalar. Therefore

```text
Q_Σ |_{L_ω ⊕ L_{ω̄}} = Y_q · I₂,    not   Y_q · σ_3
```

and its projective quotient on CP¹ = P(L_ω ⊕ L_{ω̄}) is the **identity**, which generates **zero** CP¹ rotation.

The earlier §3.3 claim that `Q_Σ = Y_q · σ_3` on the doublet was incorrect. The runner test 3.2 actually verifies the opposite: `"Homogeneous Y_q on generation sites gives trivial Q_Σ (Y-multiplication)"` is confirmed PASS. The subsequent invocation of the conjugate-pair phase winding as the "generator" is a **reuse of the target Koide structure**, not an output of the CH operator map.

**Conclusion (§3):** The CH route, taken on its own retained-data terms, produces a TRIVIAL operator map. A nontrivial CH operator map would require the bulk Y-background to be **Z_3-inhomogeneous across generations** — either Z_3-breaking or Z_3-equivariant with different per-site Y-flux. The retained framework does not force either. **Gap 3 remains open on the CH route.**

---

## 4. CH Gap 1 attempt — the identification theorem (**consistency only**)

### 4.1 What the CH identification would need

For δ_Berry(m₀ → m_*) to genuinely equal δ_CH(Σ_gen) as a derivation (not a coincidence), we would need an explicit construction of the CH descent connection 1-form `A^CH` on CP¹ that:

- does not use the Koide amplitude's phase structure as input;
- has integrated value `c · Ω = 2/9 · 1 = 2/9` on the selected-line arc;
- is gauge-equivalent to the Pancharatnam-Berry `A_CP¹ = dθ`.

### 4.2 Where the CH identification fails (**P0 Gap 1**)

*Hostile critique preserved:*

The previous §4 "proof" was:

> *"A single wavefunction can have only one well-defined Berry holonomy; therefore δ_Berry = δ_CH."*

This is exactly the identification statement that needs to be proved, recast as its own proof. The runner's `|δ_Berry − δ_CH| ≈ 10⁻¹³` is consistency after both sides have been normalized to 2/9 (δ_Berry from the Koide amplitude, δ_CH via `c · Ω = 2/9 · 1`), not derivation.

**Conclusion (§4):** The CH route provides **numerical consistency** between δ_Berry and the nominal δ_CH = c · Ω, but the identification of the physical Berry observable WITH the CH descent phase is not derived. **Gap 1 remains open on the CH route.**

---

## 5. CH Gap 2 attempt — the descent factor Ω = 1 (**sector choice, not derivation**)

### 5.1 The Fubini/Dirac computation (mathematically clean)

On any minimum-nonzero U(1)_Y configuration with integer transverse and tangent windings `(n_⊥, n_∥) = (1, 1)`:

```text
Ω = ∫_{T_Σ} F_Y ∧ F_Y / (8π²) = 2·(2π·n_⊥)·(2π·n_∥)/(8π²) = n_⊥ · n_∥ = 1
```

This is a correct Fubini + Dirac-quantization computation on the tube T_Σ.

### 5.2 Where the Ω = 1 derivation fails (**P0 Gap 2**)

*Hostile critique preserved:*

The selection of `(n_⊥, n_∥) = (1, 1)` — rather than `(0, 0)`, `(1, 2)`, `(2, 0)`, etc. — is not forced by retained axioms. The previous §5.2.1 "justification" invoked:

- the bridge must live in the anomaly-active sector (zero-flux inconsistent with the target mechanism);
- the retained Z_3 structure would be U(1)_Y-indistinguishable in the Y = 0 sector.

Both are post-hoc appeals to the target, not derivations from retained data. No retained axiom specifies that the physical defect tube carries exactly `(n_⊥, n_∥) = (1, 1)`. Any nontrivial integer pair would satisfy compactness + Dirac quantization.

**Conclusion (§5):** Ω = n_⊥ · n_∥ is correctly computed as an integer. The specific value **1** is a sector choice of the retained U(1)_Y topology, not a retained theorem. **Gap 2 remains open on the CH route.**

---

## 6. CH route summary (support-level)

The CH route's best-available state:

| Step | Status |
|------|--------|
| Bulk CS_3 and J^CH formulae (§3.1–3.2) | Mathematically clean; standard |
| Operator map CH → CP¹ (§3.3) | **Fails**: uniform Y_q is trivial on CP¹ |
| Descent factor Ω = 1 (§5) | **Sector choice**; not derived |
| Identification Berry = CH descent (§4) | **Consistency** at 10⁻¹³, not derivation |
| Combined δ = c · Ω = 2/9 rad (forward prediction) | Numerically correct; derivation pending |
| Runner 16/16 PASS | Consistency harness, not closure proof |

This is useful as **support**: it makes the open questions much more precise than the original candidate note, and provides a numerical consistency harness. It is **not closure**.

---

## 7. Cross-references (unchanged, all on main)

- `docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md` — the candidate-route note this sharpening targets.
- `docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md` — n_eff = 2 derivation (NEF).
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — selected-line Berry holonomy (KFS).
- `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` — Wilson-Dirac zero-mode realization.
- `docs/MONOPOLE_DERIVED_NOTE.md` — lattice compactness & Dirac quantization (LQC).
- `docs/HYPERCHARGE_IDENTIFICATION_NOTE.md` — U(1)_Y from commutant (HYP).
- `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — body-diagonal ↔ generation (TGO).
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` — 3+1 single-clock & retained hypercharges (AFT).
- Callan & Harvey, *Anomalies and Fermion Zero Modes on Strings and Domain Walls*, Nucl. Phys. B250 (1985) 427.
- Atiyah, Bott, Singer, *The index of elliptic operators: III*, Ann. Math. 87 (1968) 546.

---

## 8. Scope qualifiers (support-level claim, explicit)

This note's CH route:

- **Does NOT close** the three open items from `KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md` §3.
- **Does** sharpen them: for (Gap 3) it exposes that uniform Y_q on homogeneous generations is structurally trivial on CP¹, making the open question more precise; for (Gap 2) it identifies Ω = n_⊥ · n_∥ as the relevant integer with open sector-choice question; for (Gap 1) it establishes numerical consistency at 10⁻¹³.
- **Does not claim** regulator-independent continuum derivation, m_* from a variational principle, or Q = 2/3 axiom-natively (all remain separate open lanes).

See §10 below for the alternate ABSS equivariant-descent attempt.

---

## 9. CH route artifacts

- This note.
- `scripts/frontier_koide_brannen_ch_three_gap_closure.py` (support-level consistency runner, 16/16 PASS; renaming is not required since tests pass as consistency, not closure).

---

## 10. Alternate route — ambient 4D equivariant-signature descent (partial discharge, with precise residual)

The CH route fails the closure bar. This section attempts an alternate partial-closure path: use the **ambient 4D** equivariant G-signature at body-diagonal fixed points (the genuine source of the rigorous 2/9 value), and make the bridge to the selected-line CP¹ carrier through the *structural* identification of the transverse 2-complex-dim tangent with the doublet Hilbert space L_ω ⊕ L_{ω̄}. Companion runner: `scripts/frontier_koide_brannen_absss_equivariant_descent.py`.

### 10.1 What this route does and does not attempt

**Partial discharge attempt**:
- Derive the dimensionless 2/9 as an ambient-4D equivariant-signature invariant with NO sector choice, NO flux winding, NO inflow-current reuse of Koide structure.
- Make the ambient-to-CP¹ structural identification precise: the transverse 2-complex-dim tangent at each body-diagonal fixed point is naturally L_ω ⊕ L_{ω̄}, the same doublet Hilbert space that hosts the selected-line CP¹.

**Residual that remains**:
- The equivariant-signature invariant is dimensionless; the Brannen phase δ is radian. Identifying dimensionless 2/9 with radian 2/9 is the load-bearing **dimensionless↔radian residual** (same I2-lane I8 residual flagged in `.claude/plans/brannen-p-assumption-enumeration.md`).
- This alternate route does NOT close the radian identification. It sharpens the CH route's three gaps to one genuine residual.

### 10.2 Correction of an earlier mis-statement

A prior draft of this section attempted to compute the ABSS/equivariant-signature contribution directly on the 1-complex-dimensional CP¹ = P(L_ω ⊕ L_{ω̄}). **That calculation gives 0 per fixed point, not 2/9** — because the G-signature contribution `(1+ω^w)/(1-ω^w)` at a 1-complex-dim fixed point with weight w on Z_3, summed over k = 1, 2, has opposite imaginary parts that cancel (verified symbolically).

The correct source of the 2/9 value is the **2-complex-dimensional** tangent at an ambient-4D body-diagonal fixed point, where the contribution is `(1+ω^{w_1 k})(1+ω^{w_2 k}) / [(1-ω^{w_1 k})(1-ω^{w_2 k})]` — the product, not the sum, of two 1-dim factors.

### 10.3 Ambient 4D setup (retained)

The retained manifold is `M = Z^3 × R` with Z_3 acting by cyclic permutation of the three spatial axes. At a body-diagonal fixed point `p = (x_0, x_0, x_0, t_0)`:

- Time tangent: invariant (Z_3 acts trivially).
- Spatial tangent: C³ in the complexified decomposition, with retained Z_3-Fourier:
  ```text
  C³_{spatial} = L_1 ⊕ L_ω ⊕ L_{ω̄}
  ```
- L_1 direction = body-diagonal itself (invariant). The **transverse 2-complex-dim** tangent is
  ```text
  T_⊥ p  =  L_ω ⊕ L_{ω̄}                                                    (10.1)
  ```
  with Z_3 acting as `diag(ω, ω²)`, i.e. **tangent weights (1, 2)**.

**This identification (10.1) is structural, retained, and not a choice**: it comes from Cl(3) representation theory + body-diagonal identification + Z_3 cyclic permutation.

### 10.4 Single-fixed-point equivariant G-signature contribution = 2/9

At a 4-real-dim fixed point with Z_d tangent weights (w_1, w_2) in a 2-complex-dim transverse tangent, the G-signature Lefschetz contribution per fixed point is:

```text
sign(ω^k, p)  =  Π_{j=1,2} (1 + ω^{w_j k}) / (1 - ω^{w_j k})                    (10.2)
```

Summed over nontrivial Z_d elements and divided by |Z_d| gives the fixed-point contribution to the equivariant-η invariant:

```text
η_p  =  (1/d) · Σ_{k=1}^{d-1} sign(ω^k, p)                                    (10.3)
```

For d = 3, weights (1, 2):

```text
sign(ω, p)    =  (1+ω)(1+ω²) / [(1-ω)(1-ω²)]  =  1 / 3         (since (1+ω)(1+ω²) = 1, (1-ω)(1-ω²) = 3)
sign(ω², p)   =  (1+ω²)(1+ω)  / [(1-ω²)(1-ω)]  =  1 / 3

η_p  =  (1/3) · (1/3 + 1/3)  =  2/9                                          (10.4)
```

This is sympy-exact and forced by retained Z_3 structure on the 2-complex-dim transverse tangent. **No sector choice, no flux winding, no background assumption.**

### 10.5 The structural identification T_⊥ p = L_ω ⊕ L_{ω̄} = doublet Hilbert of the selected-line CP¹ carrier

The 2-complex-dim transverse tangent at each body-diagonal 4D fixed point (§10.3) is L_ω ⊕ L_{ω̄}. This is **the same** doublet Hilbert space that hosts the selected-line CP¹ carrier (§2.2). This is a structural identification forced by:

- body-diagonal = L_1 direction (TGO + Z_3 Fourier);
- transverse 2-plane = L_ω ⊕ L_{ω̄} (orthocomplement to L_1 in C³);
- selected-line CP¹ carrier = P(L_ω ⊕ L_{ω̄}) (retained KFS construction).

**So the ambient 4D equivariant-signature fixed-point contribution 2/9 is computed on exactly the same C² space on which the selected-line Berry phase lives.**

### 10.6 What this closes and what it doesn't

**Closes (retained-structural, no sector choice)**:
- ABSS/equivariant-signature gives dimensionless 2/9 as a rigorous invariant of the retained Z_3 action on the ambient C² = L_ω ⊕ L_{ω̄}.
- The ambient C² at the 4D fixed point IS the CP¹'s doublet Hilbert space (identical, not analogous).
- This discharges the **value-source** issue in both Gap 2 (no sector selection needed) and Gap 3 (the operator is the retained Z_3 action itself, not a reused target structure).

**Does NOT close (single remaining residual)**:
- The identification of **dimensionless rational 2/9** (G-signature invariant) with **radian Berry phase 2/9 rad** (observable). The G-signature is a regularized spectral sum, naturally a dimensionless rational; the Brannen phase is a radian-valued physical observable. Equating them requires a natural-radian convention.
- This is the I8/I2 residual flagged in `.claude/plans/brannen-p-assumption-enumeration.md` — same residual every prior route encountered.

### 10.7 Status after the alternate route

The alternate ambient-4D ABSS/G-signature route:

- **Rigorously derives** the dimensionless 2/9 from the retained Z_3 representation on ambient C². **No sector choice. No flux winding. No reuse of Koide target.**
- **Structurally identifies** the ambient tangent space with the selected-line doublet Hilbert space (identical, retained).
- **Does not close** the dimensionless↔radian identification. This residual is sharp: empirically forced by PDG (<0.03%), but not derived from the retained axiom set.

Honest bottom line: the three open items of the candidate note are reduced to **one** precise residual — the natural-radian convention on the retained framework that identifies dimensionless G-signature rationals with radian Berry observables. This is strictly less open than the three gaps in the candidate note, but is **not** closure.

### 10.8 Companion runner

`scripts/frontier_koide_brannen_absss_equivariant_descent.py` verifies:

1. Z_3 Fourier decomposition C³ = L_1 ⊕ L_ω ⊕ L_{ω̄} (standard).
2. Body-diagonal = L_1 direction; transverse 2-plane at body-diagonal fixed points = L_ω ⊕ L_{ω̄} (linear algebra check).
3. Z_3 tangent weights on L_ω ⊕ L_{ω̄} are (1, 2) (sympy).
4. Verify CP¹-only single-fixed-point G-signature = **0**, per the correction in §10.2 (sympy, flagged as explicitly NOT the 2/9 source).
5. Ambient-4D single-fixed-point G-signature contribution = **2/9** from the 2-complex-dim tangent (sympy exact).
6. Structural identification: the ambient 2-complex-dim transverse tangent IS the selected-line CP¹'s doublet Hilbert space (linear algebra + retained structure).
7. Selected-line Koide Berry holonomy δ(m_0 → m_*) = 2/9 to 10⁻¹³ (numerical; matches the dimensionless ambient G-signature value).
8. Honest residual: dimensionless 2/9 identified with radian 2/9 is NOT derived (flagged).

---

## 11. Consolidated scope

| Route | Dimensionless 2/9 | Radian bridge | Closure? |
|-------|------------------|----------------|----------|
| CH descent (§3–9) | Sector choice (Ω = 1 chosen) | Not addressed | **No** — support only |
| ABSS equivariant descent (§10) | **Forced** from Z_3 rep theory | Not addressed | **No** — partial closure; one residual remains |
| Combined | Dimensionless value derived (via ABSS) | Radian convention still load-bearing | **No**, but single residual is now precise |

This is the current state. The residual step is the I2-lane I8 issue ("Fourier phase = radian Berry holonomy at natural units") flagged in `.claude/plans/brannen-p-assumption-enumeration.md` §I8, still open.
