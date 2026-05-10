# Koide BAE 30-Probe Campaign Terminal Synthesis Meta Note

**Date:** 2026-05-09
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status set only after independent audit
review.
**Authority role:** records the terminal state of the 30-probe Brannen
Amplitude Equipartition (BAE) closure campaign. Documents the campaign's
two positive candidate results, multiple structural impossibility claims,
and the precisely-localized partial-falsification candidate (Probe 29:
the tested retained-content packet predicts κ=1 for charged-lepton
spectral relations, vs empirical κ=2 = BAE).
**Companion to:**
- [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
  (PR #751, prior 11-probe synthesis)
- [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
  (PR #790, BAE rename)
**Primary runner:** [`scripts/frontier_bae_30_probe_terminal_synthesis.py`](../scripts/frontier_bae_30_probe_terminal_synthesis.py)
**Cache:** [`logs/runner-cache/frontier_bae_30_probe_terminal_synthesis.txt`](../logs/runner-cache/frontier_bae_30_probe_terminal_synthesis.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim. This note
records what the 30-probe campaign converged to; it does not promote
theorems, modify retained content, or reclassify admissions.

## Naming

Throughout this note:
- **"framework axiom A1"** = retained `Cl(3)` algebra axiom per `MINIMAL_AXIOMS_2026-05-03.md`
- **"BAE"** = Brannen Amplitude Equipartition = the constraint `|b|²/a² = 1/2` for `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`
  (formerly "A1-condition"; renamed per PR #790 to resolve collision with framework axiom A1)
- **"P"** = radian-bridge primitive (= "magic angle" newly named in Probe 19, identified as same primitive in Probe 24)

## Campaign scope

The 30-probe campaign ran 2026-05-07 through 2026-05-09. Each probe
attacked closure of BAE from independent mathematical / physical /
methodological angles. All probes adhered to:
- `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE` substep-4 rule
  (no PDG values as derivation input)
- User constraint (2026-05-09): no new axioms, no external imports;
  attempted derivations from existing A1+A2+retained content only

## The 30 probes (PR-cited)

### Round 1 — Within retained content (algebra-level)

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 1 | Route F | Yukawa Casimir-difference `T(T+1) − Y² = 1/2` | #727 | barred (Y² convention dependence) |
| 2 | Route E | Kostant Weyl-vector `\|ρ_{A_1}\|² = 1/2` | #730 | barred (Cartan-Killing `\|α\|²` convention) |
| 3 | Route A | Koide-Nishiura U(3) quartic variational | #731 | barred (Wilson-coefficient circularity) |
| 4 | Route D | Newton-Girard polynomial structure | #732 | barred (weight-class (1,1) vs (1,2) ambiguity) |

### Round 2 — Natural extensions

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 5 | Probe 1 | RP/GNS canonical Frobenius | #735 | barred (vacuum-state freedom + log-functional choice) |
| 6 | Probe 2 | Anomaly extension to flavor sector | #733 | barred (R3 functoriality + category mismatch) |
| 7 | Probe 3 | Gravity-phase canonical scale | #736 | barred (sector orthogonality + character mismatch) |
| 8 | Probe 4 | Spectral-action (Connes) | #734 | barred (4 named primitives + cutoff convention) |

### Round 3 — Deep methodological

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 9 | Probe 5 | RG-flow fixed point (SM RGE) | #738 | barred (drives AWAY from BAE) |
| 10 | Probe 6 | Wrong operator class | #737 | barred (Y†Y collapses back to Hermitian) |
| 11 | Probe 7 | Z_2 × C_3 = Z_6 retained pairing | #740 | barred + identified 3:6 multiplicity locus |

### Synthesis (intermediate)

| Synth | 11-probe campaign synthesis | #751 |

### Round 4 — Plancherel/Peter-Weyl line

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 12 | Probe 12 | Plancherel/Peter-Weyl bimodule | #755 | sharpened to ℝ-isotype counting |
| 13 | Probe 13 | Real-structure / J-involution | #763 | sharpened to U(1)_b angular quotient |
| 14 | Probe 14 | Retained-U(1) hunt (9 candidates) | #784 | sharpened to "non-algebraic linear extension" |

### Round 5 — Parallel structural attacks

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 15 | Probe 15 | Continuum-limit derivation | #788 | barred (combinatorial vs Lie-group distinction) |
| 16 | Probe 16 | Q-readout functional pivot | #789 | sharpened: F2 ruled out, F1 vs F3 residue |
| 17 | Probe 17 | Lattice non-conjugation lift | #787 | barred (U(1)_b is spectrum-non-preserving) |

### Rename

| Rename | A1-condition → BAE rename meta | #790 |

### Round 6 — Discrete-choice closure

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 18 | Probe 18 | F1 canonical functional | #792 | sharpened: F2 structurally ruled out, F1 vs F3 binary |

### Round 7 — Constructive new physics

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 19 | **Probe 19** | **Wilson-chain mass derivation** | **#799** | **POSITIVE: m_τ derived to 0.017%** |
| 20 | Probe 20 | V(m) cubic extrema | #798 | barred (algebraic obstruction independent of c_1) |
| 21 | Probe 21 | Native lattice flow (bilinear) | #800 | barred (BAE neutral fixed point, not attractive) |
| 22 | Probe 22 | Spectrum-cone pivot | #801 | sharpened: spectrum=parameter via bridge identity |

### Round 8 — Refined first-principles attack

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 23 | Probe 23 | Lepton triplet C_3-cycle | #813 | barred (Wilson exponents non-integer for m_e, m_μ) |
| 24 | **Probe 24** | **φ from Z_3-character** | **#814** | **POSITIVE Step 1: φ_dimensionless = 2/9 = n_eff/d²** |
| 25 | Probe 25 | Physical-extremization / dynamics | #820 | sharpened: F1 reported structurally rejected by tested dynamics |
| 26 | Probe 26 | Wilson dimensional consistency | #818 | barred (chain factors are C_3-trivial scalar rescalings) |

### Round 9 — Falsification candidate

| # | Probe | Mechanism | PR | Outcome |
|---|---|---|---|---|
| 27 | Probe 27 | hw=N sector identification | #824 | barred (F3 sector-independent on Brannen ansatz) |
| 28 | Probe 28 | Full retained interactions | #827 | barred (F3 preserved by all C_3-covariant interactions) |
| 29 | **Probe 29** | **κ-prediction test** | **#825** | **PARTIAL FALSIFICATION: framework predicts κ=1, empirical κ=2** |
| 30 | Probe 30 | Radian from dimensions | #826 | barred (radian not in dimensional Buckingham-Pi inventory) |

## Two positive candidate results awaiting audit

### Probe 19 — m_τ Wilson chain

```
m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18} = 1.7771 GeV (matches PDG to 0.017%)
```

Exponent decomposition `18 = 16 (taste doublers, retained) + 2 (Yukawa-vertex factor)`. Five equivalent algebraic forms all give the same numerical value. Same numerical precision scale as `v_EW` (0.03%) and `m_t` (0.07%). This is a positive campaign result awaiting its own audit-lane status, not status promotion by this synthesis.

### Probe 24 Step 1 — φ_dimensionless = 2/9

```
φ_dimensionless = n_eff / d² = 2/9
```

Where `n_eff = 2` (C_3 conjugate-pair forcing: doublet winding number) and `d² = 9` (`dim_R(Herm_3)`). This is a positive character-algebra candidate result awaiting its own audit-lane status.

Step 2 obstruction: PDG-matching the Brannen circulant requires φ in literal radians, not native units. The radian-unit identification is the bounded primitive P (per `KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24` + Probes 24, 30).

## The structural finding — F3 is forced by C_3 representation theory

Probes 25 + 27 + 28 collectively report the following structural claim:

> **The (1,2) real-dim weighting on `Herm_circ(3)` is C_3 representation-theoretic (1 trivial real-dim + 2 doublet real-dims since `b ∈ ℂ`). In the tested packet it is robust under**:
> - **Free Gaussian dynamics** (Probe 25, 7 attack vectors converging mutual-deviation < 1e-9)
> - **Full retained interactions** (Probe 28, 8 routes including Yukawa, Higgs CW, gauge, plaquette, RP/transfer-matrix, spectral action, mode-counting, Ginzburg-Landau)
> - **Sector identification** (Probe 27, hw=1 vs hw=2 vs hw=3 all give same multiplicity)
> - **Spectrum vs parameter level** (Probe 22, bridge identity makes them equivalent)

F3 → κ=1 (degenerate eigenvalues). F1 → κ=2 (BAE).

The (1,1) multiplicity weighting that would give BAE is reported as **structurally absent** from the tested retained-dynamics packet. Closing BAE would require a multiplicity-counting principle distinct from C_3 rep theory on `Herm_circ(3)` — a principle not presently retained.

## The partial-falsification candidate (Probe 29)

The campaign reports that the tested retained-content packet gives a **unique canonical κ-predictor functional**:

```
Φ_canonical = (1/2) F3 = (1/2)[log E_+ + 2 log E_⊥]
```

Whose extremum is **κ = 1** (degenerate triplet), NOT κ = 2 (= BAE).

Empirical PDG charged-lepton κ ≈ 2.000037. Framework predicts κ = 1.

**Disagreement: factor of 2 in κ.**

Nine attack vectors (Probes 12, 19, 22, 24, 25, 26 + AV6/AV7/AV8/AV9 in Probe 29) converge inside the campaign packet: the tested framework content as a κ-predictor gives κ = 1.

This is a precisely-localized **partial-falsification candidate** for the framework's charged-lepton SPECTRAL-RELATION prediction. If the audit lane retains the candidate, it does NOT falsify:
- Mass scales (Probe 19 m_τ matches to 0.017%)
- EW-Planck hierarchy (retained, matches v_EW to 0.03%)
- Generation count (retained, matches LEP)
- Hierarchy pattern (qualitative match)
- Hypercharge ratios (retained, matches anomaly cancellation)

If retained by audit, it would falsify the framework's prediction of charged-lepton Koide ratio `Q = 2/3` from C_3-circulant matter-sector dynamics.

## Three structural impossibility claims (the campaign's deepest results)

1. **Probe 14**: no retained continuous U(1) projects to U(1)_b (algebra-automorphism failure mode)
2. **Probe 17**: U(1)_b is spectrum-non-preserving — cannot be ANY unitary similarity
3. **Probe 25 + 27 + 28**: F1 (multiplicity (1,1)) is reported structurally absent from the tested retained-dynamics packet across free + interacting + all hw=N sectors

## Admissions remaining

| Admission | Status |
|---|---|
| BAE (`\|b\|²/a² = 1/2`) | bounded; closure requires multiplicity-counting principle outside retained C_3 rep theory |
| P (radian bridge for `φ = 2/9`) | bounded; radian unit not in framework's dimensional inventory |
| Total | **2** (Probe 24 ruled out third) |

## Strategic options remaining

This note **does not select** any option:

1. **Accept partial falsification**: framework's charged-lepton κ-prediction is wrong (Probe 29). Document the falsification cleanly. Continue framework work on validated lanes.

2. **Build new retained physics outside C_3 rep-theory on `Herm_circ(3)`**: the missing primitive is structurally outside this class. Attempts would need radically different framing (different sector, different operator class, or new dynamical mechanism not in retained content).

3. **Pivot to other bridge work**: Convention C-iso engineering (in flight), substrate-to-carrier-forcing (Planck-from-structure, 3 missing theorems identified earlier), δ campaign, etc.

The audit lane has authority over whether the partial-falsification candidate stands, whether closure is required at the lepton-spectral-relation level, and which strategic path the framework pursues.

## What this note does NOT do

1. Promote BAE to retained or closed.
2. Claim partial falsification is the audit-lane verdict.
3. Modify any retained theorem.
4. Add a new axiom.
5. Reclassify admission count or `effective_status` of any specific row.
6. Select among the strategic options.

## Cross-references

- Foundational: `MINIMAL_AXIOMS_2026-05-03.md`, `PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`, `C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`, `CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`
- BAE rename: `BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md` (PR #790)
- Prior synthesis (11 probes): `KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md` (PR #751)
- Substep-4 rule: `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`
- All 30 probe source-notes referenced in the campaign table above

## Validation

```bash
python3 scripts/frontier_bae_30_probe_terminal_synthesis.py
```

Runner verifies:
1. This note is `meta` and does not declare pipeline status.
2. All 30 probes are cited with their PR numbers.
3. The 2 positive candidate results are recorded (m_τ Wilson chain, φ_dimensionless=2/9).
4. The structural impossibility claims are recorded (Probes 14, 17, 25+27+28).
5. The partial-falsification candidate (Probe 29 κ=1 vs empirical κ=2) is recorded.
6. The 2 remaining admissions (BAE + P) are correctly counted.
7. No new axiom, no theorem promotion, no admission reclassification.
8. Cross-references to retained foundational notes present.

## Review-loop rule

Going forward:

1. The 30-probe campaign on BAE is **terminal**. New BAE-closure attempts must explicitly identify why they're outside the C_3 rep-theory structural class (since the campaign has structurally established F3 forcing within that class).
2. Partial-falsification candidate (Probe 29 κ=1 vs κ=2) is recorded; not yet adjudicated by audit lane.
3. The 2 positive candidate results (Probe 19 m_τ scale, Probe 24 Step 1 φ_dimensionless) are independent candidate results awaiting their own audit-lane review.
4. The 2 remaining admissions (BAE, P) retain their bounded status until either closure or explicit admission.
