# Cycle 02 (Retained-Promotion) Claim Status Certificate — SU(2) Witten Anomaly Doublet-Count Derivation (closing derivation)

**Block:** physics-loop/su2-witten-doublet-count-derivation-2026-05-02
**Note:** docs/SU2_WITTEN_ANOMALY_DOUBLET_COUNT_DERIVED_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_su2_witten_anomaly_doublet_count_derivation.py (PASS=14/0)
**Target row:** su2_witten_z2_anomaly_theorem_note_2026-04-24 (claim_type=positive_theorem, audit_status=audited_conditional, td=134, lbs=B)

## Block type

**Closing derivation** (output type (a) per the new retained-promotion
campaign prompt). New theorem note + runner that **derives the
verdict-identified obstruction** (SU(2) doublet count + RH-singlet
completion) from retained framework primitives.

## Promotion Value Gate (V1–V5)

### V1: SPECIFIC verdict-identified obstruction this PR closes

Quoted from parent row's `verdict_rationale`:

> the runner hard-codes that premise [Q_L, L_L SU(2) doublet
> multiplicities and RH-singlet completion] and then checks parity.
> Repair target: add or cite a retained-grade one-generation matter
> theorem deriving the Q_L/L_L SU(2) Weyl-doublet content and singlet
> completion from the retained graph/gauge surface.

**This PR's closing-derivation theorem derives the SU(2) doublet count
(3 + 1 = 4) and the RH-singlet completion from retained `Q_L : (2, 3)`
and `L_L : (2, 1)` rep literals + structural chirality of SU(2)_L,
replacing the parent's hand-coded multiplicities table.**

### V2: NEW derivation contained

The parent's runner takes a hand-entered table of fields with their
multiplicities (Q_L: 3, L_L: 1, RH: 0) and verifies that 3+1+0 = 4 mod 2
= 0. This is hand-coded counting, not a derivation.

This PR's derivation:
1. Reads the SU(2) doublet count from the retained `(2, 3)` literal of
   `Q_L`: dim_SU(3)(Q_L) = 3 doublets per generation (one per color).
2. Reads the SU(2) doublet count from `L_L : (2, 1)`: 1 doublet
   (color singlet).
3. Derives the RH-singlet status from the chirality of SU(2)_L
   (structural argument from `NATIVE_GAUGE_CLOSURE_NOTE`).
4. Sums to 4 per generation.
5. Applies the Witten Z_2 anomaly index formula (admitted from external
   QFT, Witten 1982) and verifies cancellation.
6. Extends to multi-generation: 4 N_gen always even.
7. Verifies counterfactual: dropping L_L doublet gives 3 (odd),
   anomalous — the cancellation is non-trivial.

### V3: Audit lane couldn't already do this from existing retained primitives + standard math machinery

The audit lane in restricted one-hop context cannot synthesize
matter-content rep literals + chirality of SU(2)_L + Witten Z_2
topology in one hop. Each piece is a separate authority:
- `LEFT_HANDED_CHARGE_MATCHING.md` (Q_L rep);
- `ONE_GENERATION_MATTER_CLOSURE.md` (L_L rep);
- `NATIVE_GAUGE_CLOSURE.md` (chirality of SU(2)_L);
- Witten 1982 (admitted-context external).

The closing derivation puts them all together with the explicit
counterfactual demonstration of non-triviality.

### V4: Marginal content non-trivial

Yes:
- π_4(SU(2)) = Z_2 admitted-context external authority (cited, not
  re-derived).
- Doublet count derivation from rep literal (not just hand-coding).
- Multi-generation parity argument.
- Counterfactual demonstration that the lepton doublet IS required for
  one-generation cancellation (dropping it gives index 1, anomalous).
- Connection to the framework's `NATIVE_GAUGE_CLOSURE` for chirality.

This is genuine derivation content the parent row didn't have.

### V5: Not a one-step variant of an already-landed cycle

Cycle 01 (PR #382) derived SU(3)^3 cubic anomaly cancellation forcing
2 LH 3̄ singlets. This is SU(3) cubic anomaly with Diophantine
enumeration. Cycle 02 is SU(2) Witten Z_2 anomaly with parity (mod 2)
counting + topological cancellation. Different anomaly types
(perturbative cubic vs topological global), different math
(Diophantine vs parity), different parent rows. Not a one-step
variant.

## Outcome classification (per new prompt)

**(a) Closing derivation.** This PR provides a new theorem note +
runner that **derives the verdict-identified obstruction** (SU(2)
doublet count + RH-singlet completion) from retained framework
primitives. The outcome IS retained-positive movement on the parent
row's load-bearing step, conditional on audit-lane ratification of:
- the framework's lattice-fermion convention (color components as
  independent Weyl fields);
- the chirality of SU(2)_L as the weak gauge factor;
- the standard Witten Z_2 anomaly index formula.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Witten 1982 is
  standard external mathematical reference, role-labelled
  admitted-context external authority).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this derivation:
- Parent row `su2_witten_z2_anomaly_theorem_note_2026-04-24`
  load-bearing class-B step closes (matter-content multiplicities
  derived, not hand-coded).
- The SU(2) Witten Z_2 anomaly cancellation becomes a derived theorem
  on the framework's retained matter content.
- Combined with cycle 01 (SU(3) cubic) and downstream PRs on
  hypercharge / mixed anomalies, the framework's complete one-generation
  anomaly-freedom claim moves toward retained status.

## Honesty disclosures

- The framework-side conventions (lattice-fermion content, chirality of
  weak gauge group, multi-generation extension) are admitted-context
  framework conventions, not pure mathematics.
- The Witten Z_2 anomaly itself is admitted from external QFT.
- The runner does not modify any audit-ledger file.
- This PR + cycle 01's PR together close the SU(3) and SU(2) anomaly
  cancellation derivations. Mixed anomalies (SU(3)^2 U(1)_Y, U(1)_Y^3,
  gravitational^2 U(1)_Y) and hypercharge uniqueness remain separate
  authority rows for future work.
