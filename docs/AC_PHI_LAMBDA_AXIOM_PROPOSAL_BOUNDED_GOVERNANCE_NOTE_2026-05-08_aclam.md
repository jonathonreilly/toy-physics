# AC_φλ Identification Atom — Proposed Framework Axiom A3

**Date:** 2026-05-08
**Claim type:** axiom_proposal (governance, not derivation)
**Status:** unaudited candidate. This is an **AXIOM PROPOSAL** requiring
governance review, not a derivation. Audit verdict and downstream
status set only by the independent audit lane.
**Primary runner:** [`scripts/cl3_ac_phi_lambda_axiom_check_2026_05_08_aclam.py`](../scripts/cl3_ac_phi_lambda_axiom_check_2026_05_08_aclam.py)
**Cached output:** [`logs/runner-cache/cl3_ac_phi_lambda_axiom_check_2026_05_08_aclam.txt`](../logs/runner-cache/cl3_ac_phi_lambda_axiom_check_2026_05_08_aclam.txt)
**Source-note proposal:** audit verdict and downstream status set only
by the independent audit lane.

## 0. Audit context

The bridge gap closure status (after this session's work landed via
`d4df8d637` + `d444fb545` + subsequent salvages) reduces to **one
named admission** — the L3a trace-surface choice (V_3 vs V_full),
which per [`L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`](L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md)
is precisely localized to the staggered-Dirac realization gate's
substep 4.

The substep 4 AC has been further decomposed in
[`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
into three atoms with explicit fates:

| Atom | Fate |
|---|---|
| AC_φ (physical-observable) | **forced to FAIL** under retained C_3[111] symmetry |
| AC_λ (species-label) | **provable** from retained substep 2 (Kawamoto-Smit) |
| AC_φλ (identification) | **residual**; no standard-QFT axiom equivalent |

This note proposes admitting AC_φλ as **framework axiom A3** to close
the bridge gap admission count to **zero**.

## 1. Proposed axiom

```
A3 (Physical-Species Identification Axiom).

The framework's 3-fold structure on the hw=1 BZ-corner triplet —
characterized by:
  (i)   the M_3(C) endomorphism algebra on H_{hw=1} ≅ C^3,
  (ii)  the C_3[111] cyclic generator acting on the corners, and
  (iii) the no-proper-quotient theorem on H_{hw=1}
— IS the Standard Model flavor-generation structure carrying three
quantum-mechanically distinct physical species (generations).
```

Rationale: the three structural components (i–iii) are all retained
positive theorems; A3 provides the **physical interpretation** of the
combined structure as the SM flavor-generation carrier.

A3 is an empirically falsifiable assertion (see §5) and is structurally
analogous to a DHR superselection rule (Doplicher-Haag-Roberts 1971)
declaring that the C_3-orbit decomposes into three superselection
sectors corresponding to three SM generations.

## 2. Four required properties

This axiom proposal must satisfy four governance criteria; companion
notes document each:

| Property | Companion note | Verdict |
|---|---|---|
| **Independence** from A1+A2 | [`outputs/.../INDEPENDENCE_PROOF.md`](../outputs/action_first_principles_2026_05_08/ac_phi_lambda_axiom_proposal/INDEPENDENCE_PROOF.md) | A3 is **not derivable** from A1+A2 (proven via AC_φ forced-failure + 7-attack W2 obstruction + 10-attack L3a obstruction) |
| **Consistency** with retained framework | [`outputs/.../CONSISTENCY_PROOF.md`](../outputs/action_first_principles_2026_05_08/ac_phi_lambda_axiom_proposal/CONSISTENCY_PROOF.md) | A3 is **consistent** with all retained results; no internal contradictions; no audit-ledger conflicts |
| **Minimality** (smallest sufficient axiom) | [`outputs/.../THEOREM_NOTE.md`](../outputs/action_first_principles_2026_05_08/ac_phi_lambda_axiom_proposal/THEOREM_NOTE.md) §3 | A3 is **minimal**: removing any of (i)–(iii) breaks downstream closure |
| **Empirical falsifiability** | [`outputs/.../EMPIRICAL_FALSIFIABILITY.md`](../outputs/action_first_principles_2026_05_08/ac_phi_lambda_axiom_proposal/EMPIRICAL_FALSIFIABILITY.md) | A3 is **falsifiable** via lattice MC measurement of C_3-breaking observables in the hw=1 sector |

Numerical verification of these four properties (where machine-checkable):
**21/0 EXACT PASS** in the runner.

## 3. Downstream consequences (if A3 admitted)

The companion note [`outputs/.../DOWNSTREAM_CONSEQUENCES.md`](../outputs/action_first_principles_2026_05_08/ac_phi_lambda_axiom_proposal/DOWNSTREAM_CONSEQUENCES.md)
enumerates exactly which bounded artifacts lift to retained under A3.
Summary:

| Artifact | Pre-A3 | Post-A3 |
|---|---|---|
| L3a admission | bounded_obstruction | **closed** (corollary of A3) |
| L3b admission | bounded (≡ L3a) | **closed** (W2.bridge) |
| Substep 4 of staggered-Dirac realization gate | bounded_theorem (with AC) | **positive_theorem** (corollary of A3) |
| `N_F = 1/2` on V_3 | bounded_theorem (W2.norm conditional) | **positive_theorem** (W2.norm closure chain unblocked) |
| Staggered-Dirac realization synthesis | bounded_theorem (Block 06) | **positive_theorem** (substep 4 lifted) |
| Bridge-gap admission count | 1 (L3a) | **0** |
| Bridge-gap admission types | trace-surface choice | none |

**Net effect**: the bridge gap closes at admission level. The remaining
bounded element is the C-iso numerical systematic (W1 ε_witness),
which is engineering, not admission.

## 4. Independence (sketch — full proof in companion note)

A3 is independent of A1+A2 because:

(a) **AC_φ is forced to FAIL under retained primitives** — proven in
    [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md).
    Any C_3[111]-symmetric self-adjoint operator on H_{hw=1} ≅ C^3
    has equal expectation values on all three corner states.
    Therefore the species-distinguishing physical-observable content
    of A3 cannot be recovered from observable algebras invariant under
    retained primitives.

(b) **The L3a admission's 10-vector enumeration is exhaustive** — proven
    in [`L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`](L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md).
    Zero unconditional positive arrows; all four partials reduce to
    the matter-rep / staggered-Dirac realization identification
    (= AC_φλ).

(c) **The W2.binary 7-vector enumeration is exhaustive** — proven in
    [`N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md`](N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md).
    All seven attack routes give clean obstructions or partials
    conditional on framework-level identifications (= AC_φλ).

The combined evidence demonstrates A3 cannot be derived from A1+A2 +
canonical Tr-form + RP + locality + single-clock + Lieb-Robinson +
the retained Casimir / Cl(3)-color-automorphism / N_F-binary / etc.
chain.

## 5. Empirical falsifiability (sketch — full in companion note)

A3 makes the **specific empirical prediction**: physical observables
on the hw=1 sector exhibit the C_3-breaking structure characteristic
of three SM generations. Specifically:

> **Falsifiability test.** A lattice Monte Carlo measurement of the
> three C_3-broken expectation values `⟨Ô⟩_corner_a` (a = 1, 2, 3) for
> any species-distinguishing observable Ô must agree with the SM
> flavor-generation pattern (e.g., distinct quark-lepton mass scales)
> within experimental precision. If the framework's predicted pattern
> disagrees with experiment at the precision of generation-mixing
> observations (CKM matrix, neutrino oscillations), A3 is falsified.

Specifically: if lattice MC on the Cl(3) framework's substrate gives
identical mass scales for all three generations (i.e., the C_3
symmetry is unbroken at the physical level), A3 is falsified.
Conversely, the empirically observed mass hierarchy (m_t ≫ m_c ≫ m_u)
is consistent with A3.

## 6. Comparison to standard QFT axioms

A3 is structurally analogous to DHR superselection rules
(Doplicher-Haag-Roberts 1971; Streater-Wightman §2.4-§4.5):

| Standard QFT axiom | Cl(3) framework analogue |
|---|---|
| Spectrum condition (Wightman W2) | Forced to fail under retained C_3 (= AC_φ) |
| Spin-statistics | Provable from retained substep 2 (= AC_λ) |
| **DHR superselection (3 sectors)** | **A3 (proposed): 3-fold C_3-orbit ↔ 3 SM generations** |
| Lorentz invariance | (separate; not at issue) |
| Vacuum uniqueness | (separate; not at issue) |

The pattern is: structural claims that bridge mathematical formalism to
physical interpretation are admitted as axioms in standard QFT
(Wightman-style or operator-algebraic). A3 is the framework's
analogous bridge — empirically falsifiable, structurally minimal, and
not derivable from the kinematic axioms.

## 7. What this proposal closes vs does not close

### Closes (under governance acceptance)

- The L3a admission (V_3 vs V_full trace surface) becomes a
  **derived corollary** of A3.
- Substep 4 of the staggered-Dirac realization gate lifts from
  `bounded_theorem` to `positive_theorem`.
- All bounded_theorem labels in the bridge-dependent chain that were
  conditional on L3a become retained (specifically the W2.norm
  V_3 closure chain, the N_F binary reduction, and the per-site
  ↔ V_3 bridge identification per W2.bridge).
- **Bridge-gap admission count drops from 1 to 0.**

### Does not close

- The **C-iso numerical systematic** in the W1 multi-plaquette
  numerics (currently bounded at ~1.3% absolute, target ε_witness
  ~ 3×10⁻⁴). This is a separate engineering/compute problem,
  unaffected by A3 — addressed independently in the SU(3) NLO
  closure follow-up work.
- Any framework predictions in lanes that have their own admissions
  beyond the bridge gap.

## 8. Authority and governance

This is an **axiom proposal**, not a derivation. The decision to
admit A3 is a **governance act** by the independent audit lane.

**Recommendation to the audit lane**: review A3 against the four
governance criteria (independence, consistency, minimality,
empirical falsifiability) per the companion notes. If all four are
audited clean, A3 may be admitted as a framework axiom alongside
A1+A2.

**If admitted**, update the canonical axiom set
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) (or
its successor) to include A3 with the proposed formulation.

**If rejected**, the L3a admission persists as an open gate and the
bridge gap remains at one admission until either (a) a new derivation
route is discovered (none currently visible per the exhaustive
attack-vector analyses cited above), or (b) a different axiom is
admitted that closes L3a as a corollary.

## 9. References

- [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) — the 3-atom decomposition justifying A3 as the residual atom
- [`L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`](L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md) — L3a localization to substep 4
- [`N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md`](N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md) — W2.binary 7-attack obstruction
- [`PER_SITE_SU2_BRIDGE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2bridge.md`](PER_SITE_SU2_BRIDGE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2bridge.md) — W2.bridge L3b ≡ L3a
- [`N_F_V3_NORMALIZATION_BOUNDED_NOTE_2026-05-07_w2norm.md`](N_F_V3_NORMALIZATION_BOUNDED_NOTE_2026-05-07_w2norm.md) — W2.norm closure chain
- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) — HS rigidity
- [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md) — four-layer stratification
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) — current axiom set (A1, A2)
- Wightman, A.S. (1956). Quantum field theory in terms of vacuum expectation values. *Phys. Rev.* 101, 860.
- Streater, R.F. & Wightman, A.S. (1964). *PCT, Spin and Statistics, and All That.*
- Doplicher, S., Haag, R., Roberts, J.E. (1971). Local observables and particle statistics. *Comm. Math. Phys.* 23, 199.
