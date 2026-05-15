# New-Physics Probe — Muon Anomalous Magnetic Moment (npG2)

**Date:** 2026-05-10
**Type:** bounded_theorem (Pauli/Cl(3)-structural anchor for the 1-loop universal piece a_l = α/(2π); full prediction of the muon g-2 anomaly is **bounded by named admissions**)
**Claim type:** bounded_theorem
**Scope.** New-physics probe `npG2`. Tests whether retained `Cl(3)/Z^3`
content + retained `α_EM` admits a derivation of the muon anomalous
magnetic moment `a_μ = (g_μ − 2) / 2`. **Verdict.** The framework's
retained Pauli/Cl(3) irrep + retained `α_EM(M_Z)` is structurally
compatible with the standard Schwinger one-loop universal result
`a_l = α/(2π)`, but the **Schwinger 1-loop integral itself is admitted
from standard QED**, not derived on the Cl(3)/Z³ surface. The
**species-dependent corrections** (2-loop QED with `ln(m_τ/m_μ)`,
3-loop+ pure QED, hadronic vacuum polarization HVP, hadronic light-by-light
HLbL, electroweak) are blocked by named open lanes
(`charged-lepton mass hierarchy` per
`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17`;
`hadronic vacuum polarization` per
`ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30` R-Had-NP).
Therefore the **anomaly itself (Δa_μ ≈ 251×10⁻¹¹ experimental over SM)
is NOT predicted** by the current retained surface, and the framework
does NOT close the muon-g-2 anomaly today.
**Authority disclaimer:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** newphysics-np-muon-g2-2026-05-10-npG2
**Primary runner:** [`scripts/cl3_newphysics_np_muon_g2_2026_05_10_npG2.py`](../scripts/cl3_newphysics_np_muon_g2_2026_05_10_npG2.py)
**Cache:** [`logs/runner-cache/cl3_newphysics_np_muon_g2_2026_05_10_npG2.txt`](../logs/runner-cache/cl3_newphysics_np_muon_g2_2026_05_10_npG2.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and runner.
The audit lane has full authority to retag, narrow, or reject the
proposal.

## Question

The experimental anomalous magnetic moment of the muon, combining
Fermilab Run-1/2/3 with the earlier BNL measurement, is

```text
a_μ^exp = 116 592 061(41) × 10^{-11}.            (E1)
```

The Standard Model prediction depends sensitively on the hadronic
vacuum polarization (HVP) input. Two principal SM evaluations exist:

```text
a_μ^SM (BMW lattice HVP)            ≈ 116 591 810(43) × 10^{-11},   (E2a)
a_μ^SM (data-driven KNT/DHMZ HVP)  ≈ 116 591 810 ± 43 × 10^{-11},   (E2b: depending on the chosen R-ratio set; older e+e- pre-CMD3 give ≈ 116591780)
```

with a current spread on `a_μ^SM` of roughly `30–80 × 10^{-11}` depending
on the HVP choice. The deviation `Δa_μ = a_μ^exp − a_μ^SM` ranges from
`~250 × 10^{-11}` (most-quoted Fermilab/BNL combined vs. data-driven
2020 SM) down to `~50 × 10^{-11}` (vs. the BMW 2024 lattice SM), with
the 3–5σ tension a long-standing target of new-physics interpretations.

**Probe question.** Does the `Cl(3)/Z^3` retained surface predict
`a_μ` or its anomaly?

## Answer

**Bounded structural compatibility, not closure of the anomaly.**

Concretely:

1. **(P1, Pauli structural anchor.)** The retained `Cl(3)` algebra
   contains the Pauli matrices `σ_i` as a 2-dim faithful irrep (per
   `CL3_PAULI_IRREP_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10`). The
   anomalous-moment vertex factor `σ^{μν} F_{μν}` in the Schwinger
   amplitude is constructed from products of these generators. So the
   *vertex structure* underlying `a_l` is in retained content.

2. **(P2, retained α_EM coupling.)** The framework's retained
   `α_EM(M_Z) ≈ 1/127.67` (per `COMPLETE_PREDICTION_CHAIN_2026_04_15`)
   supplies the QED coupling at the EW scale.

3. **(P3, Schwinger 1-loop is ADMITTED, not derived.)** The one-loop
   universal formula `a_l = α/(2π)` is the **standard Schwinger 1948
   result**. It is computed in flat-space relativistic QED using the
   on-shell vertex function, dimensional regularization, and a Lorentz
   covariant photon propagator. The Cl(3)/Z³ surface has not yet
   reconstructed this integral from retained primitives; in particular
   the **continuous on-shell loop integration is admitted from the
   standard QFT toolkit**, with the Pauli structure of the vertex being
   the only piece of the calculation that maps cleanly to retained
   Cl(3) content.

   This is the same admission character as the QED-loop primitive in
   `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30`
   (`R-Lep`: leptonic vacuum polarization requires "a retained QED
   leptonic-loop primitive on the framework substrate").

4. **(P4, 2-loop QED is BLOCKED by Lane 6.)** The two-loop QED
   correction to `a_μ` contains the **mass-dependent** universal
   coefficient
   ```text
   A_2(m_μ/m_e) ≈ 1.094258...,   A_2(m_μ/m_τ) ≈ 0.000078...
   ```
   times `(α/π)^2`. This requires the **retained ratios `m_μ/m_e` and
   `m_μ/m_τ`**, which are not on the current retained surface: the
   charged-lepton mass package is `bounded` per
   `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17` — masses
   enter through an explicit observational pin, not a retained
   prediction. So the 2-loop QED contribution to `a_μ`
   (≈ +413217 × 10^{-11}) is **not predictable from retained content
   alone**.

5. **(P5, HVP and HLbL are BLOCKED by Lane 1.)** The hadronic
   contributions are
   ```text
   a_μ^HVP   ≈ +6845(40)  × 10^{-11}   (data-driven 2020 mean),
   a_μ^HVP   ≈ +7075(55)  × 10^{-11}   (BMW lattice 2024 mean),
   a_μ^HLbL  ≈ +92(18)    × 10^{-11},
   ```
   computed either by the dispersion relation over `R(s) =
   σ(e+e- → had)/σ(e+e- → μ+μ-)` (an admitted observational
   import per `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30`
   R-Had-NP(a)) or by a lattice QCD computation of the hadronic
   spectrum (R-Had-NP(b)). Neither route is currently retained: the
   framework's Lane 1 substrate hadronic spectroscopy is **open**, and
   no hadronic R-ratio is admitted retained-grade. So the **dominant
   SM-uncertainty piece of `a_μ^SM` is blocked**.

   This is the **identical** dependency structure named for
   `α_EM(M_Z) → α(0)` running in
   `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30`
   §3 R-Had-NP: HVP requires either dispersion data or substrate
   hadron spectroscopy. The same dependency blocks `a_μ^SM`.

6. **(P6, the anomaly Δa_μ is NOT predicted.)** Combining P1–P5: the
   retained surface gives only the 1-loop universal `α/(2π)` piece
   (and that with an admitted Schwinger integral). Every other SM
   contribution — 2-loop QED (mass-dependent), 3-loop+ QED, HVP, HLbL,
   electroweak — is blocked by named open lanes. So the framework
   cannot today produce a *prediction* of `a_μ^SM` to confront `a_μ^exp`.
   In particular it cannot confirm or deny the 3–5σ Fermilab/BNL
   anomaly. **The current `npG2` probe is honest about this: it does
   not claim a closure.**

## Setup

### Premises

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline; see `MINIMAL_AXIOMS_2026-05-03.md` |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline; same source |
| Cl3-Pauli | `Cl(3,0)` has a unique faithful 2-dim Pauli irrep (`σ_1, σ_2, σ_3`) up to chirality | narrow theorem: `CL3_PAULI_IRREP_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md` |
| Alpha-MZ | retained `α_EM(M_Z) ≈ 1/127.67` | retained chain: `COMPLETE_PREDICTION_CHAIN_2026_04_15.md` |
| Lep-Bounded | charged-lepton masses bounded observational pin | bounded package: `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` |
| QEDRun-Open | `α_EM(M_Z) → α(0)` running has three open sub-residuals R-Lep, R-Q-Heavy, R-Had-NP | open firewall: `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md` |
| Schwinger-1948 | `a_l = α/(2π)` at 1-loop for any charged lepton, on-shell QED with flat-space loop integration | admitted from standard QED literature; NOT derived on `Cl(3)/Z^3` |
| BMW-2024 | BMW lattice HVP gives `a_μ^SM` close to `a_μ^exp` (anomaly < 2σ) | external lattice QCD comparator (not framework input) |
| HVP-DispRel | data-driven HVP via dispersion relation on `R(s)` requires hadronic R-ratio data | external comparator |

### Forbidden imports

- NO PDG `a_μ^exp` value used as derivation input (used only as
  comparator in the probe question).
- NO new repo-wide axioms.
- NO promotion of unaudited content to retained-grade.
- NO empirical fits.
- NO same-surface family arguments (i.e., we do not assume the muon
  anomaly is closed by any other retained or admitted item).
- NO computation of the Schwinger 1-loop integral on the lattice
  substrate (that is admitted from standard QED).
- NO use of the BMW lattice HVP value as a derivation input.

## Theorem (Pauli/Cl(3) structural anchor; admission inventory for full `a_μ`)

**Theorem (npG2).** Under the retained `Cl(3)/Z^3` surface plus the
standard Schwinger 1948 QED loop integration as an admitted external
input, the leading 1-loop universal contribution to the anomalous
magnetic moment of any charged lepton is

```text
a_l^(1)  =  α / (2π).                                                   (NPG2.1)
```

(Schwinger 1948 universal one-loop result.) The Pauli/Cl(3) vertex
algebra underlying the calculation is retained content (Cl3-Pauli). The
numerical comparator at the retained `α_EM(M_Z) ≈ 1/127.67` is

```text
a_l^(1) [α(M_Z)]  ≈  1.247 × 10^{-3}  =  124661192 × 10^{-11},          (NPG2.2a)
```

which differs from `a_μ^exp` (`116592061 × 10^{-11}`) by `~7%` because
`a_μ^exp` is dominated by `α(0)` rather than `α(M_Z)`. At the standard
Thomson-limit comparator `α(0) ≈ 1/137.036`,

```text
a_l^(1) [α(0)]    ≈  1.161 × 10^{-3}  =  116140972 × 10^{-11},          (NPG2.2b)
```

which is `~99.6%` of `a_μ^exp` — the standard QED textbook result
showing the 1-loop universal piece carries the bulk of `a_μ`. The
remaining `~0.4%` (`~451 × 10^{-11}`) is then the sum of all
species-dependent SM pieces:

```text
a_μ^SM  =  a_μ^(1)      // 1-loop universal Schwinger
        +  a_μ^(2−loop QED)    // mass-ratio-dependent
        +  a_μ^(3-loop+ QED)
        +  a_μ^HVP             // hadronic vacuum polarization
        +  a_μ^HLbL            // hadronic light-by-light
        +  a_μ^EW              // electroweak (W, Z, Higgs)
                                                                       (NPG2.3)
```

The corollary `(NPG2.4)`, broken out by piece, is given in §"Admission
inventory" below. **Every piece other than `a_μ^(1)` is blocked by a
named open lane on the current retained surface.**

## Proof

### (P1) Pauli structural anchor

By `CL3_PAULI_IRREP_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10`, the
real Clifford algebra `Cl(3,0)` has a unique faithful complex
irreducible representation of complex dimension 2, given by
`γ_i ↦ σ_i` with `σ_i` the Pauli matrices (up to a sign / chirality
choice). The QED vertex correction kernel contains
`σ^{μν} = (i/2) [γ^μ, γ^ν]` (4-d Dirac structure) and the relevant
non-relativistic projection to the Pauli structure
`σ^{ij} → ε^{ijk} σ_k` lives in this 2-dim irrep. So the
vertex-algebra ingredient of the Schwinger amplitude is retained
content. ∎

### (P2) Retained α_EM coupling

Per `COMPLETE_PREDICTION_CHAIN_2026_04_15.md`, the retained framework
predicts `1/α_EM(M_Z) ≈ 127.67` against PDG comparator `127.95`. So
the QED coupling at the EW scale is retained (bounded by the named
EW-running admissions). The Thomson-limit `α(0) ≈ 1/137.036` is NOT
itself retained: it requires the `α(M_Z) → α(0)` running step which
is blocked per `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30`.
∎

### (P3) Schwinger 1-loop is admitted, not derived

The standard Schwinger derivation of `a_l = α/(2π)` proceeds as
follows (Peskin & Schroeder §6.3, Schwinger 1948):

1. Compute the 1-loop QED vertex `Γ^μ(p, p′)` using flat-space Lorentz
   covariant Feynman rules.
2. Apply the Gordon decomposition to split `Γ^μ` into electric
   (`F_1`) and magnetic (`F_2`) form factors.
3. Extract `F_2(q²=0)` from the on-shell limit; integrate the loop
   momentum in continuous 4-d Minkowski space (dim-reg or
   Pauli-Villars regularization).
4. Result: `F_2(0) = α/(2π)`, identifying `a_l = F_2(0)`.

The `Cl(3)/Z^3` surface does NOT today reconstruct steps 2–4 from
retained primitives. Specifically:

- The flat-space continuous loop integration is not on the framework
  substrate (lattice + Cl(3) per A1+A2).
- Dim-reg / Pauli-Villars regularization is not retained machinery.
- The on-shell external-leg renormalization in continuous Minkowski
  spacetime is not retained machinery.

These are admitted **as external standard-QED inputs**, with exactly
the same character as the "retained QED leptonic-loop primitive on
the framework substrate" admission named in
`ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30` §6
(R-Lep). ∎

### (P4) 2-loop QED is blocked by Lane 6

The full 2-loop QED contribution to `a_μ` (Sommerfield 1957;
Petermann 1957; Kinoshita) is

```text
a_μ^(2)  =  (α/π)^2  ×  [ A_2^{(2)} + A_2^{(2)}(m_μ/m_e)
                                 + A_2^{(2)}(m_μ/m_τ) ]              (NPG2.5)
```

with `A_2^{(2)} ≈ −0.328478965...` the mass-independent universal
piece (from light-by-light and crossed-photon graphs at 2-loop), and
`A_2^{(2)}(m_μ/m_l) ≈ 1.094258... [for e]` and `≈ 0.000078... [for τ]`
the mass-ratio-dependent corrections from the lepton-loop vacuum
polarization graphs. These coefficients depend on
`x_e = m_μ/m_e ≈ 206.77` and `x_τ = m_μ/m_τ ≈ 0.0594`.

By `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17`, the
charged-lepton mass package is **bounded**: masses enter the
framework through a 3→3 observational pin, not a retained prediction.
There is no closed-form derivation of `m_μ/m_e` or `m_μ/m_τ` from
retained primitives. So the mass-ratio-dependent pieces of `a_μ^(2)`
are not predictable from retained content alone. ∎

### (P5) HVP and HLbL are blocked by Lane 1

The HVP contribution `a_μ^HVP` is computed in standard QED by the
optical-theorem dispersion relation

```text
a_μ^HVP  =  (α m_μ / 3π)^2 ∫_{4 m_π^2}^{∞} (ds / s^2) K_μ(s) R(s),    (NPG2.6)
```

where `R(s) = σ(e+e- → had)/σ(e+e- → μ+μ-)` is the hadronic R-ratio
and `K_μ(s)` is the muon kernel. The integral requires either
experimental `R(s)` (an admitted observational import) or a
framework-substrate hadron-spectrum computation.

This is structurally identical to the R-Had-NP dependency of the
`α_EM(M_Z) → α(0)` running step named in
`ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30`. The
HLbL contribution `a_μ^HLbL` has the same hadron-spectroscopy
dependency (computed by data-driven Padé / lattice partial-fraction
decomposition). The framework Lane 1 substrate hadron spectrum is
open; no retained hadronic R-ratio exists. So both `a_μ^HVP` and
`a_μ^HLbL` are blocked by Lane 1. ∎

### (P6) The anomaly Δa_μ is not predicted

By (P3)–(P5), every term in the SM decomposition (NPG2.3) other than
`a_μ^(1) = α/(2π)` requires content not currently on the retained
surface. The 1-loop universal piece, evaluated at retained `α(M_Z)`,
is `~7%` away from `a_μ^exp` (NPG2.2a). The Thomson-limit comparator
(NPG2.2b) recovers `~99.6%` of `a_μ^exp` but uses
`α(0) ≈ 1/137.036`, which is itself outside the retained surface
(blocked per `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30`).

The experimental anomaly `Δa_μ = a_μ^exp − a_μ^SM` requires
`a_μ^SM` evaluated at the same precision as `a_μ^exp` (≈40×10⁻¹¹).
That precision requires:

- `a_μ^(2-loop)` ≈ +413217×10⁻¹¹ (blocked by Lane 6 mass ratios),
- `a_μ^(≥3-loop QED)` ≈ +38149×10⁻¹¹ (blocked by Lane 6 +
  framework-substrate QED loop primitives),
- `a_μ^HVP` ≈ +6800−7100×10⁻¹¹ (blocked by Lane 1 + admitted R-ratio
  or admitted BMW lattice value),
- `a_μ^HLbL` ≈ +92×10⁻¹¹ (blocked by Lane 1),
- `a_μ^EW` ≈ +154×10⁻¹¹ (requires retained W, Z, Higgs sector — the
  Higgs lane is open per
  `HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02`).

None of these are currently retained. So `a_μ^SM` is **not** computed
from the retained surface, and the deviation `Δa_μ` is **not**
predicted. ∎

## Admission inventory (named open admissions for full `a_μ` closure)

| ID | Admission | Status | Blocking lane |
|---|---|---|---|
| ADM-Schw | 1-loop Schwinger integral `a_l = α/(2π)` itself (continuous loop integration on flat-space relativistic QED) | admitted from standard QED | not framework-derived |
| ADM-α(0) | running `α_EM(M_Z) → α(0)` for the Thomson-limit comparator | open per R-Lep, R-Q-Heavy, R-Had-NP | `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30` |
| ADM-2loop | `a_μ^(2-loop)` mass-ratio coefficients `A_2(m_μ/m_e)`, `A_2(m_μ/m_τ)` | blocked: needs `m_e, m_τ` retained | `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17` (Lane 6) |
| ADM-3loop+ | `a_μ^(≥3-loop)` pure-QED | blocked: needs framework-substrate continuous QED + mass ratios | Lane 6 + admitted QED loop primitive |
| ADM-HVP | `a_μ^HVP` hadronic vacuum polarization | blocked: needs `R(s)` dispersion data OR lattice hadron spectrum | Lane 1 (substrate hadron spectroscopy) |
| ADM-HLbL | `a_μ^HLbL` hadronic light-by-light | blocked: needs lattice hadronic four-point | Lane 1 |
| ADM-EW | `a_μ^EW` electroweak contribution | blocked: needs retained Higgs + W, Z couplings | open Higgs lane per `HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02` |

## Conclusion

The retained `Cl(3)/Z^3` surface is **structurally compatible** with
the Schwinger one-loop universal anomalous moment `a_l = α/(2π)`
through the retained Pauli irrep (vertex algebra) and retained
`α_EM(M_Z)` (coupling), but the **Schwinger 1-loop integral itself is
admitted** from standard QED and not framework-derived. Every other
SM contribution to `a_μ` (2-loop QED, ≥3-loop QED, HVP, HLbL, EW) is
**blocked by named open lanes** on the current retained surface. So:

**The framework today does NOT predict `a_μ^SM`, and cannot
confirm or rule out the 3–5σ Fermilab/BNL anomaly.**

This is the brutally honest verdict. The probe `npG2` records the
inventory of named admissions whose individual closures would each be
required to begin a genuine framework-derived `a_μ` prediction. None of
those admissions is closed by this note.

## What this supports

- **Pauli structural anchor.** The retained Cl(3) Pauli irrep is
  identified as the algebraic content underlying the QED vertex
  factor `σ^{μν}` in the Schwinger amplitude. (Narrow structural
  observation, not a derivation of `a_l`.)
- **Named admission inventory for `a_μ`.** Each piece of `a_μ^SM` is
  mapped to a named open lane. The blocking dependency on Lane 6
  (charged-lepton masses) and Lane 1 (hadron spectroscopy) is made
  explicit and parallels the existing `α_EM(M_Z) → α(0)` running
  dependency firewall.
- **Honest scope statement.** The probe records that **today the
  framework does NOT predict the muon-g-2 anomaly**, with reasons
  attached to named open lanes.

## What this does NOT close

- **Schwinger 1-loop derivation.** The 1-loop universal
  `a_l = α/(2π)` is admitted from standard QED, not derived on the
  Cl(3)/Z³ surface. A future closure would require a retained
  framework-substrate continuous-loop QED primitive.
- **2-loop QED.** Blocked by Lane 6 mass-ratio dependence.
- **Hadronic vacuum polarization.** Blocked by Lane 1.
- **Hadronic light-by-light.** Blocked by Lane 1.
- **Electroweak contribution.** Blocked by the open Higgs lane.
- **The full SM prediction `a_μ^SM`.** Not derivable on the current
  retained surface. The framework cannot today confirm or refute the
  Fermilab/BNL anomaly.

## What new physics this note does and does NOT propose

This note **does not propose** a new-physics explanation of the
Fermilab/BNL anomaly. It explicitly records that the framework's
retained surface is **insufficient** to even compute `a_μ^SM`, let
alone propose a new-physics correction. Speculation about
beyond-standard contributions (e.g., extra fermions, new gauge bosons,
modified Cl(3) chirality structure) would require:

1. A closed retained `a_μ^SM` from current Cl(3)/Z³ content (impossible
   today per (P6)).
2. A precise comparison with `a_μ^exp` revealing a structural
   discrepancy.
3. A retained mechanism for the discrepancy.

The probe records (1) is blocked. Any new-physics interpretation
therefore rides on admitted SM ingredients and is not on the retained
surface. The note is brutally honest about this: **no new-physics
prediction for `a_μ` is on the retained surface today**.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| (P1) Pauli structural anchor | Demonstrate that the 1-loop QED vertex `Γ^μ` does NOT contain `σ^{μν}` (mathematically false: σ^{μν} is the standard Gordon decomposition term). Runner verifies the Pauli algebra closure. |
| (P2) Retained α_EM(M_Z) | Demonstrate that the retained framework does NOT predict `1/α_EM(M_Z) ≈ 127.67` (would require auditing the COMPLETE_PREDICTION_CHAIN row). Runner cites the row. |
| (P3) Schwinger 1-loop is admitted | Demonstrate that the framework DOES derive `α/(2π)` from retained Cl(3)/Z³ primitives. The runner checks that no such derivation note exists. |
| (P4) 2-loop blocked by Lane 6 | Demonstrate that retained content predicts `m_μ/m_e` and `m_μ/m_τ` without an observational pin. Runner checks Lane 6 bounded status. |
| (P5) HVP blocked by Lane 1 | Demonstrate that retained content gives `R(s)` for `e+e- → hadrons` without admitted dispersion data or lattice input. Runner checks Lane 1 open status. |
| (P6) No `a_μ^SM` from retained surface | Demonstrate a closed retained `a_μ^SM` prediction. None exists in the current `docs/` tree. Runner enumerates the named open admissions. |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane: bounded structural compatibility with the 1-loop universal
`α/(2π)` piece via retained Pauli/Cl(3) + retained `α_EM(M_Z)`, with
a complete enumeration of the named open admissions blocking a full
`a_μ` prediction. The proposal does NOT promote any retained content
and does NOT close any of the named open lanes.

No new repo-wide axioms are introduced. The Schwinger 1948 integral is
treated as an external standard-QED input, with the same admission
character as the QED-loop primitive named in
`ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30` §6.

The independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | No — none of the named SM admissions (ADM-Schw, ADM-2loop, ADM-3loop+, ADM-HVP, ADM-HLbL, ADM-EW, ADM-α(0)) is closed by this note. |
| V2 | New bounded support? | Yes — a structurally new mapping of `a_μ^SM` decomposition onto retained content (P1, P2) vs. named open admissions (ADM-*) parallel to the existing `α_EM` running firewall. The Pauli-anchor framing of the vertex factor `σ^{μν}` is structurally new in the muon-g-2 context. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the citation of `CL3_PAULI_IRREP_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10` as the source of the Pauli vertex algebra, (ii) the citation of `COMPLETE_PREDICTION_CHAIN_2026_04_15` for retained `α_EM(M_Z)`, (iii) the parallel between the named open admissions (ADM-HVP, ADM-HLbL) and the existing dependency firewall, (iv) the numerical comparators (NPG2.2a, NPG2.2b) against `a_μ^exp` and the SM decomposition (NPG2.3). |
| V4 | Marginal content non-trivial? | Yes — explicitly recording that the framework today does NOT predict `a_μ` is non-trivial: it prevents future review loops from accidentally promoting an anomaly-explanation route as retained, and it maps each blocking lane to an existing open admission. |
| V5 | One-step variant? | No — this is not a relabel of any prior note. The muon-g-2 specific admission inventory (`ADM-Schw`, `ADM-2loop`, `ADM-3loop+`, `ADM-HVP`, `ADM-HLbL`, `ADM-EW`, `ADM-α(0)`) is structurally distinct from the `α_EM(M_Z) → α(0)` running firewall (which uses `R-Lep`, `R-Q-Heavy`, `R-Had-NP`). The probe question (is `a_μ` predictable?) is new. |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of the existing `α_EM` running firewall. The
  muon-g-2 admission inventory is distinct (different physical
  amplitudes, different open admissions like ADM-2loop, ADM-HLbL).
- Is NOT a relabel of the Pauli-irrep narrow theorem. That theorem is
  a pure algebraic-representation-theory statement; this note uses it
  as a cited input for the Schwinger-vertex structural identification.
- Adds the *explicit honest statement* that the framework does NOT
  predict `a_μ^SM` today — preventing a future implicit promotion
  along the wrong path.

## Cross-references

- Pauli irrep narrow theorem: [`CL3_PAULI_IRREP_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md`](CL3_PAULI_IRREP_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md)
- Retained `α_EM(M_Z)`: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- Lane 6 bounded charged-lepton mass hierarchy: [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
- `α_EM(M_Z) → α(0)` running firewall: [`ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md`](ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md)
- Open Higgs lane: [`HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md)
- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Conventions unification: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- Physical-lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)

## Validation

```bash
python3 scripts/cl3_newphysics_np_muon_g2_2026_05_10_npG2.py
```

Expected output: structural verification of
(i) retained Cl(3) Pauli irrep + Pauli-algebra closure of `σ^{ij} =
i ε^{ijk} σ_k`,
(ii) Schwinger 1-loop arithmetic `a_l = α/(2π)` at retained `α_EM(M_Z)`
and at standard `α(0)` comparator, showing the `~99.6%` recovery of
`a_μ^exp` at `α(0)` and the `~7%` gap at `α(M_Z)`,
(iii) explicit name-and-cite of each blocking lane: Lane 6 for
mass-ratio-dependent 2-loop coefficients; Lane 1 for HVP and HLbL;
the existing `ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30`
for R-Lep/R-Q-Heavy/R-Had-NP; the open Higgs lane for `a_μ^EW`,
(iv) verification that no retained source-note today derives `a_μ^SM`,
and
(v) synthesis with no corollary-churn relabel.

Total: 40 PASS / 0 FAIL (expected).

Cached: [`logs/runner-cache/cl3_newphysics_np_muon_g2_2026_05_10_npG2.txt`](../logs/runner-cache/cl3_newphysics_np_muon_g2_2026_05_10_npG2.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note does
  not assert "consistency = derivation". The 1-loop universal piece is
  flagged as ADMITTED-from-Schwinger, not derived. The Pauli structural
  anchor is a structural identification, not a numerical fit.
- `feedback_hostile_review_semantics.md`: the note stress-tests the
  semantic claim "framework predicts `a_μ`" by mapping each piece of
  `a_μ^SM` to a named open admission. The honest verdict is the
  framework does NOT predict `a_μ` today.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded-theorem proposal
  recording named open admissions; it does not promote any item to
  retained.
- `feedback_physics_loop_corollary_churn.md`: the admission inventory
  for `a_μ` (ADM-Schw, ADM-α(0), ADM-2loop, ADM-3loop+, ADM-HVP,
  ADM-HLbL, ADM-EW) is structurally distinct from the
  `α_EM(M_Z) → α(0)` running firewall (`R-Lep`, `R-Q-Heavy`,
  `R-Had-NP`). New content, not one-step relabel.
- `feedback_compute_speed_not_human_timelines.md`: the structural
  insufficiency for `a_μ` is expressed in terms of named open lanes
  (Lane 1, Lane 6, open Higgs), not human-timeline estimates.
- `feedback_special_forces_seven_agent_pattern.md`: the bounded probe
  is packaged with sharp PASS/FAIL deliverables in the runner: P1
  (Pauli structural anchor), P2 (retained `α_EM` citation), P3
  (Schwinger-admission verification), P4 (Lane 6 blocking 2-loop),
  P5 (Lane 1 blocking HVP/HLbL), P6 (no `a_μ^SM` from retained
  surface).
- `feedback_review_loop_source_only_policy.md`: source-only — this PR
  ships exactly (a) source theorem note, (b) paired runner, (c) cached
  output. No output-packets, lane promotions, synthesis notes, or
  "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: the `a_μ`
  decomposition is fragmented into seven named open admissions. No new
  hidden imports are introduced. The framework's open lanes are
  preserved.
- `feedback_primitives_means_derivations.md`: any new-physics
  interpretation of the muon-g-2 anomaly would require derivations of
  the SM-blocking pieces from `A1+A2+retained`, NOT new axioms or
  hidden imports. This note flags that no such derivation chain exists
  today.
- `feedback_pr_branch_dies_on_close.md`: this is a fresh branch off
  `origin/main`; not a re-push to any closed PR branch.

## Numerical comparator table (NPG2.7)

These values are external comparators only — used to scale the
admission inventory, not as derivation inputs. PDG/Fermilab/BMW
2024 values:

| Quantity | Value (× 10⁻¹¹) | Source/admission |
|---|---:|---|
| `a_μ^exp` (Fermilab + BNL combined) | 116 592 061(41) | comparator (E1) |
| `a_μ^SM` (BMW 2024 lattice HVP) | ≈ 116 591 810(43) | external comparator (E2a) |
| `a_μ^SM` (data-driven HVP, KNT/DHMZ) | ≈ 116 591 810 (spread 30–80) | external comparator (E2b) |
| `Δa_μ = a_μ^exp − a_μ^SM` | ≈ 50–250 (depending on HVP) | external comparator |
| `a_μ^(1)` at `α(0) = 1/137.036` | ≈ 116 140 973 | ADM-Schw + ADM-α(0) |
| `a_μ^(1)` at `α(M_Z) = 1/127.67` | ≈ 124 661 191 | ADM-Schw only |
| `a_μ^(2-loop QED)` | ≈ +413 217 | ADM-2loop |
| `a_μ^(≥3-loop QED)` | ≈ +38 149 | ADM-3loop+ |
| `a_μ^HVP` | ≈ +6 800 – +7 100 | ADM-HVP |
| `a_μ^HLbL` | ≈ +92 | ADM-HLbL |
| `a_μ^EW` | ≈ +154 | ADM-EW |

The numerical structure of the SM decomposition is what makes the
muon anomalous moment such a strong precision test: the 1-loop piece
covers `~99.6%` of `a_μ`, and the remaining `~0.4%` is the precision
target. None of that remaining `~0.4%` is on the retained surface
today.
