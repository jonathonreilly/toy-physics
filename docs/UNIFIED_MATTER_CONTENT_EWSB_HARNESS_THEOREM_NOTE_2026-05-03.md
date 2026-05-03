# Unified End-to-End Matter-Content + EWSB Harness — Synthesis Closing Derivation

**Date:** 2026-05-03
**Type:** positive_theorem (synthesis)
**Claim scope:** the **synthesis-level closing derivation** that
cycles 01+02+04+06+07 of the retained-promotion campaign
2026-05-02 collectively close the matter-content + EWSB-direction
question on the framework's retained graph-first surface, and that
the chain is audit-verifiable as a UNIFIED CHAIN in a single
self-contained runner. The unified harness re-executes the FULL
CHAIN inline:

```text
retained graph-first SU(3) integration (Sym²(3) ⊕ Anti²(1) split)
+
retained narrow-ratio Y(L_L)/Y(Q_L) = -3
→
cycle 01 SU(3)^3 Diophantine forces 3̄ for u_R^c, d_R^c
→
cycle 02 SU(2) Witten Z_2 forces 4 doublets per generation
→
cycle 04 U(1)_Y mixed cubic forces (y_1, y_2, y_3) = (+4/3, -2/3, -2)
                                               on no-ν_R sector
→
all four anomaly conditions verified on the derived rep
   (Tr[Y] = Tr[Y^3] = Tr[SU(3)^2 Y] = Tr[SU(2)^2 Y] = 0)
→
cycle 06 Majorana null-space classification on derived rep
   (no-ν_R: empty; with-ν_R admission: {ν_R^T C P_R ν_R})
→
cycle 07 conditional EWSB Q = T_3 + Y/2 on derived rep
   (with admitted (2, +1)_Y Higgs candidate)
→
Q-spectrum {0, +2/3, -1/3, -1} on no-ν_R derived rep (matches SM)
+
Σ Q = 0 on derived rep (electric-charge anomaly-free)
```

The result is a **single integrated proof artifact** the audit lane
can verify in one hop, providing the chain-level closure of the
matter-content + EWSB-direction question.

**Status:** audit pending. Audit-lane ratification of cycles 01-07
individually is also required (PRs #382, #383, #390, #405, #407);
cycle 11's chain status changes accordingly if any individual cycle
is demoted. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline; no author-side
tier is asserted in source.

**Runner:** [`scripts/frontier_unified_matter_content_ewsb_harness.py`](./../scripts/frontier_unified_matter_content_ewsb_harness.py)

**Authority role:** synthesis-level closing derivation for the
collective audit-verifiable chain of cycles 01+02+04+06+07. Provides
the integrated proof artifact for the matter-content + EWSB-direction
closure as a unified chain, without standing in for individual-cycle
verdicts.

## Synthesis-question obstruction

Cycles 01+02+04+06+07 are five independent PRs whose collective
claim is "the SM matter content + EWSB direction is derived from
retained primitives + admitted-context standard math." Without a
unified harness, an auditor must verify each cycle's runner separately
and then mentally synthesize the chain.

**This PR provides the single integrated runner that re-executes
every step inline**, making the chain audit-verifiable in one hop.

The closest precedent is **cycle 06** (PR #405), which synthesizes
cycles 01+02+04 + adds the Majorana null-space solve. **Cycle 11
extends cycle 06's synthesis principle through cycle 07's
conditional EWSB Q-formula**, providing the natural chain-level
closure of the matter-content + EWSB-direction question with
cross-cycle consistency checks and chain-level forbidden-imports
audit.

## Statement

Let:

- (P1, retained) Graph-first SU(3) integration giving Q_L : (2, 3)
  on the framework's selected-axis surface.
  [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) (td=312, retained).

- (P2, retained) The narrow-ratio theorem
  [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md)
  (td=265, retained) establishing Y(L_L)/Y(Q_L) = -3 structurally.

- (P3, retained) The framework's gauge structure
  SU(3)_c × SU(2)_L × U(1)_Y on the chiral surface, from
  [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md).

- (P4, sister-derivations) Cycles 01+02+04+06+07 of the
  retained-promotion campaign 2026-05-02:
  - cycle 01 ([PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382)):
    SU(3)^3 cubic Diophantine forces 3̄ for u_R^c, d_R^c.
  - cycle 02 ([PR #383](https://github.com/jonathonreilly/cl3-lattice-framework/pull/383)):
    SU(2) Witten Z_2 parity forces 4 doublets per generation.
  - cycle 04 ([PR #390](https://github.com/jonathonreilly/cl3-lattice-framework/pull/390)):
    U(1)_Y mixed cubic on no-ν_R forces (+4/3, -2/3, -2).
  - cycle 06 ([PR #405](https://github.com/jonathonreilly/cl3-lattice-framework/pull/405)):
    Majorana null-space synthesis on derived rep.
  - cycle 07 ([PR #407](https://github.com/jonathonreilly/cl3-lattice-framework/pull/407)):
    Conditional EWSB Q = T_3 + Y/2 on derived rep.

- (P5, admitted) A scalar field Φ in the (2, +1)_Y representation
  of SU(2)_L × U(1)_Y with non-zero VEV in its lower component.
  Identification with a specific framework primitive is the named
  obstruction documented in cycle 07's note.

- (P6, admitted) The optional ν_R extension admits Y(ν_R) = 0 and
  rep (1, 1)_0; without this admission, the framework's matter is
  the no-ν_R sector.

- (P7, admitted-context external) Standard ABJ anomaly cancellation
  requirement (Adler 1969; Bell-Jackiw 1969); SU(2) Witten Z_2
  requirement (Witten 1982); standard SM EWSB algebra
  (Peskin-Schroeder 1995 ch. 20). Mathematical machinery, not
  numerical comparator.

- (P8, convention) Doubled-Y convention with `Q = T_3 + Y/2` and
  Q(u_R) > 0 labelling.

**Conclusion (T1) (synthesis closing derivation).** Under
P1+P2+P3+P4+P7+P8 on the no-ν_R sector, the unified harness
verifies that the framework's derived SM one-generation matter
representation is

```text
Q_L : (2, 3)_{+1/3}
L_L : (2, 1)_{-1}
u_R : (1, 3)_{+4/3}
d_R : (1, 3)_{-2/3}
e_R : (1, 1)_{-2}
```

DERIVED inline from retained primitives + cycles 01+02+04 logic, with
all four anomaly conditions Tr[Y] = Tr[Y^3] = Tr[SU(3)^2 Y]
= Tr[SU(2)^2 Y] = 0 verified simultaneously.

**Conclusion (T2) (Majorana null-space on derived rep).** On the
DERIVED no-ν_R rep, the same-chirality P_R Majorana null space is
empty. Adding P6 (Y(ν_R) = 0 admission), the null space becomes
one-dimensional, spanned by `ν_R^T C P_R ν_R`. (Cycle 06 logic
re-executed inline.)

**Conclusion (T3) (conditional EWSB on derived rep).** Under
P3+P5+P7+P8 with the derived rep, the unbroken U(1) generator of
SU(2)_L × U(1)_Y → U(1)_em is uniquely Q = T_3 + Y/2; the
Q-spectrum on the derived rep is {0, +2/3, -1/3, -1} (no-ν_R) or
{0, +2/3, -1/3, -1, [0]} (with-ν_R extension). Denominators ⊆ {1, 3}.
(Cycle 07 logic re-executed inline.)

**Conclusion (T4) (electric-charge anomaly-free).** On the derived
rep with Q-formula Q = T_3 + Y/2, the chain-level identity
Σ Q = 0 holds. This is a corollary of T1 + T3 that no individual
cycle 01-07 verifies directly.

**Conclusion (T5) (cross-cycle consistency).** The Y values
(y_1, y_2, y_3) cycle 04 solves are byte-for-byte identical to the
Y values cycle 06's null-space solver consumes and the Y values
cycle 07's Q-spectrum check uses. The unified harness verifies
this consistency explicitly.

**Conclusion (T6) (chain-level forbidden-imports audit).** The
unified chain consumes:
- only retained primitives (P1, P2, P3) and admitted-context
  external math (P7) and conventions (P8);
- no PDG observed values, no literature numerical comparators, no
  fitted selectors, no admitted unit conventions beyond doubled-Y,
  no same-surface family arguments, and no load-bearing dependency
  on the demoted HYPERCHARGE_IDENTIFICATION_NOTE.

**Conclusion (T7) (counterfactual breakage modes).** Three explicit
counterfactuals demonstrate chain-level breakage:
- (K1) y_3 = -1 (instead of -2) breaks Tr[Y] = 0 and Tr[Y^3] = 0.
- (K2) Higgs in (2, -1)_Y instead of (2, +1)_Y with same lower-component
  VEV breaks Q = T_3 + Y/2 annihilation of ⟨Φ⟩.
- (K3) e_R as (1, 3) instead of (1, 1) breaks Tr[SU(3)^2 Y] = 0.

## Proof structure

The unified harness's runner executes 14 sections (Blocks A through N)
in order, each verifying one stage of the chain:

| Block | Content | Cycles encoded |
|-------|---------|----------------|
| A | SU(3)^3 cubic Diophantine → 3̄ | 01 inline |
| B | SU(2) Witten Z_2 → 4 doublets | 02 inline |
| C | U(1)_Y mixed cubic → SM Y values | 04 inline |
| D | Synthesis: derived SM rep | 01+02+04 |
| E | All four anomaly conditions on derived rep | (chain-level) |
| F | Majorana null-space on derived rep | 06 inline |
| G | SU(2) generators + EWSB on (2, +1)_Y doublet | 07 inline |
| H | Q-spectrum on derived rep | 07 inline |
| I | Σ Q = 0 (electric-charge anomaly-free) | (chain-level) |
| J | Cross-cycle consistency 04↔06↔07 | (chain-level) |
| K | Counterfactual breakage stack | (chain-level) |
| L | Universality: Q-formula independent of v | 07 inline |
| M | Forbidden-imports chain-level audit | (chain-level) |
| N | End-to-end chain consistency summary | (chain-level) |

Each block is a self-contained verification step that the audit lane
can inspect independently. Blocks marked "(chain-level)" are
synthesis-content that no individual cycle 01-07 verifies in
isolation.

## What this claims

- **(T1)** The synthesis-level closing derivation: cycles 01+02+04+
  06+07 collectively close the matter-content + EWSB-direction
  question on the framework's retained graph-first surface, and the
  chain is audit-verifiable in one hop via the unified harness.
- **(T2)** Majorana null-space classification on derived rep
  (re-execution of cycle 06): no-ν_R empty; with-ν_R one-dim.
- **(T3)** Conditional EWSB Q = T_3 + Y/2 on derived rep with
  Q-spectrum {0, ±1/3, ±2/3, ±1} matching SM.
- **(T4)** Σ Q = 0 chain-level corollary on derived rep.
- **(T5)** Cross-cycle 04↔06↔07 consistency on Y values + rep.
- **(T6)** Chain-level forbidden-imports audit clean.
- **(T7)** Three counterfactual breakage modes verified.

## What this does NOT claim

- Does NOT propose new theorem content beyond what cycles 01+02+04+
  06+07 individually claim. The synthesis-content (T4, T5, T6) are
  chain-level corollaries / audits of those cycles.
- Does NOT close cycle 07's named obstruction (Higgs identification
  from framework primitives). The unified harness uses cycle 07's
  CONDITIONAL form: GIVEN a (2, +1)_Y Higgs candidate, the unbroken
  generator is uniquely Q = T_3 + Y/2.
- Does NOT close PMNS / leptogenesis / Δm² / m_ββ / EWSB mechanism
  / Higgs mass / Yukawa couplings. Those are downstream phenomenology
  / mechanism notes.
- Does NOT promote any individual cycle 01-07's status. Each
  individual cycle's audit-lane disposition remains independent of
  cycle 11's verification.
- Does NOT replace the need for individual-cycle audit-lane
  ratification. Cycle 11's chain status changes accordingly if any
  individual cycle 01-07 is demoted.
- Does NOT promote any author-side tier; audit-lane ratification of
  cycle 11 itself is required.

## Cited dependencies

- (P1) [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) (retained, td=312).
- (P2) [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md) (retained, td=265).
- (P3) [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) (retained).
- (P4a) [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md) — cycle 01 sister ([PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382)).
- (P4b) `SU2_WITTEN_ANOMALY_DOUBLET_COUNT_DERIVED_THEOREM_NOTE_2026-05-02.md` — cycle 02 sister ([PR #383](https://github.com/jonathonreilly/cl3-lattice-framework/pull/383)).
- (P4c) [`SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md`](SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md) — cycle 04 sister ([PR #390](https://github.com/jonathonreilly/cl3-lattice-framework/pull/390)).
- (P4d) `SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md` — cycle 06 sister ([PR #405](https://github.com/jonathonreilly/cl3-lattice-framework/pull/405)).
- (P4e) `CONDITIONAL_EWSB_Q_FORMULA_ON_DERIVED_REP_THEOREM_NOTE_2026-05-02.md` — cycle 07 sister ([PR #407](https://github.com/jonathonreilly/cl3-lattice-framework/pull/407)).
- (P5) Admitted (2, +1)_Y Higgs candidate; not identified with framework primitive (named obstruction in cycle 07).
- (P6) Admitted Y(ν_R) = 0 input for ν_R extension; ν_R is optional (cycle 04 no-ν_R variant).
- (P7) Adler 1969, Bell-Jackiw 1969 (ABJ anomaly cancellation); Witten 1982 (SU(2) Z_2 anomaly); Peskin-Schroeder 1995 ch. 20 (SM EWSB algebra) — all admitted-context external mathematical machinery, role-labelled.

## Forbidden imports check (chain-level)

- No PDG observed values consumed.
- No literature numerical comparators consumed (Adler 1969,
  Bell-Jackiw 1969, Witten 1982, Peskin-Schroeder 1995 are
  admitted-context external mathematical machinery, role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention beyond the
  doubled-Y convention shared with cycles 04+06+07.
- No same-surface family arguments.
- No load-bearing dependency on the demoted
  `HYPERCHARGE_IDENTIFICATION_NOTE` (cycle 04's decoupling carries
  through to cycles 06, 07, 11).
- No pre-derived rep hand-coded as input — the rep is rederived
  inline from cycles 01+02+04 logic before being used as cycle 06+07's
  input.

## Validation

Primary runner: [`scripts/frontier_unified_matter_content_ewsb_harness.py`](./../scripts/frontier_unified_matter_content_ewsb_harness.py)
verifies (PASS=52/0, exact rational arithmetic + numerical SU(2)
generator algebra):

1. Cycle 01 inline: SU(3)^3 cubic anomaly forces minimal 2-field RH
   completion to be {3̄, 3̄}.
2. Cycle 02 inline: SU(2) doublet count = 4 per generation, Witten
   Z_2 index = 0.
3. Retained narrow-ratio: Y(L_L)/Y(Q_L) = -3.
4. Cycle 04 inline: y_1 + y_2 = 2/3 from Tr[SU(3)^2 Y] = 0.
5. Cycle 04 inline: y_3 = -2 from Tr[Y] = 0.
6. Cycle 04 inline: y_1·y_2 = -8/9 from cubic-symmetric identity.
7. Cycle 04 inline: rational discriminant 324 = 18^2.
8. Cycle 04 inline: y_1 = +4/3, y_2 = -2/3 (Q(u_R) > 0 labelling).
9. All four anomalies zero on derived rep simultaneously
   (Tr[Y], Tr[Y^3], Tr[SU(3)^2 Y], Tr[SU(2)^2 Y]).
10. SU(2) commutation relation [T_1, T_2] = i T_3.
11. Cycle 06 inline: no-ν_R Majorana null space empty.
12. Cycle 06 inline: with-ν_R Majorana null space is dim 1 (ν_R ν_R).
13. Cycle 07 inline: Q = T_3 + Y/2 annihilates ⟨Φ⟩ = (0, v/√2)^T.
14. Cycle 07 inline: Q' = T_3 - Y/2 does NOT annihilate ⟨Φ⟩.
15. Cycle 07 inline: only a = 1 over a-grid in [-2, 2].
16. Q-spectrum on no-ν_R derived rep is {0, +2/3, -1/3, -1};
    denominators ⊆ {1, 3}.
17. Σ Q over derived rep (LH-conjugate frame) = 0.
18. Cross-cycle 04↔06↔07 consistency on Y values for u_R, d_R, e_R.
19. Counterfactual K1: y_3 = -1 breaks Tr[Y] = 0 and Tr[Y^3] = 0.
20. Counterfactual K2: Y_phi = -1 with lower-component VEV breaks
    Q = T_3 + Y/2 annihilation.
21. Counterfactual K3: e_R as (1, 3) breaks Tr[SU(3)^2 Y] = 0.
22. Universality: Q = T_3 + Y/2 unbroken for v ∈ {1e-3, 1, 246, 1e6};
    Q' broken for all v.
23. Chain-level forbidden-imports clean (6 separate audit checks).
24. End-to-end consistency summary.

## Cross-references

- Cycle 01 sister: SU3_ANOMALY_FORCED_3BAR_COMPLETION ([PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382)).
- Cycle 02 sister: SU2_WITTEN_ANOMALY_DOUBLET_COUNT_DERIVED ([PR #383](https://github.com/jonathonreilly/cl3-lattice-framework/pull/383)).
- Cycle 04 sister: SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT ([PR #390](https://github.com/jonathonreilly/cl3-lattice-framework/pull/390)).
- Cycle 06 sister: SM_REP_DERIVED_MAJORANA_NULL_SPACE ([PR #405](https://github.com/jonathonreilly/cl3-lattice-framework/pull/405)).
- Cycle 07 sister: CONDITIONAL_EWSB_Q_FORMULA_ON_DERIVED_REP ([PR #407](https://github.com/jonathonreilly/cl3-lattice-framework/pull/407)).
- Retained: [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md).
- Retained: [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md).
- Retained: [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md).
- Parent (cycle 06): [`NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`](NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md).
- Parent (cycle 07): [`HIGGS_MECHANISM_NOTE.md`](HIGGS_MECHANISM_NOTE.md).
- Admitted external: Adler 1969, Bell-Jackiw 1969, Witten 1982,
  Peskin-Schroeder 1995 — role-labelled admitted-context mathematical
  machinery.

## Honesty disclosures

- Cycle 11 is a **synthesis** runner — its content is not new
  theorem material beyond cycles 01+02+04+06+07. Its derivation
  content is the integrated end-to-end verification + cross-cycle
  consistency + chain-level forbidden-imports audit.
- Cycle 11 does **not** stand in for individual-cycle audit-lane
  ratification. Cycles 01-07 each remain audit pending; cycle 11's
  unified-chain status is downstream of their individual verdicts.
- Cycle 11 uses cycle 07's CONDITIONAL form for EWSB; the named
  obstruction (Higgs identification from framework primitives)
  remains open. The unified harness does not address it.
- Cycle 11 does not promote any author-side tier; audit-lane
  ratification of cycle 11 itself is required.
