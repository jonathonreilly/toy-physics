# Quark Up-Amplitude Retained-Native Candidate -- SUPERSEDED by RPSR

**Date:** 2026-04-19
**Status:** SUPERSEDED (cycle 10D). Originally the cycle-3 "minimal-
contraction" (Min-C) candidate retained-atom construction for the quark
up-amplitude a_u. Cycle 10D replaced the abstract atom-economy rule
with the **Reduced Projector-Ray Sum Rule (RPSR)**, a physics identity
on the 1 (+) 5 projector ray. Min-C is now a **conditional theorem** --
conditional on one LO algebraic identity at NNI diagonalization.

**Primary reference:**
`docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`.

---

## 1. What changed between cycle 1-4 and cycle 10

### Cycle 1-4 state

The cycle 3 attack selected a_u via **minimal-contraction (Min-C)** on
retained atoms:

> Each retained atom appears to first degree only, no cross-sector
> Casimirs, no auxiliary rationals, minimal number of atoms consistent
> with the Pareto-joint-dominator criterion.

From the 8 Pareto-incomparable joint-dominator candidates
(17-quark-au-certification.md Table 2), Min-C under A1-corrected
scoring selected the target

    a_u = sqrt(5/6) * (1 - rho + rho * supp * delta_A1)
        = 0.7748865611  (10 decimals).

Cycle 4 cross-observable check: the full retained observable suite does
NOT discriminate among the 8 Pareto-incomparable candidates
(inter-candidate spreads 10 to 10^4 x below retained tolerance). Min-C
was retained as **axiom candidate** -- the structural rule "each atom
once, no cross-sector" was the axiom-atom.

### Cycle 10D state (this update)

The abstract Min-C rule is **replaced by a physics identity** on the
1 (+) 5 projector ray:

    RPSR:   a_u / sin(delta_std) + a_d  =  1 + a_d * supp * delta_A1
                                         =  1 + rho / 49.

RPSR is derived from retained infrastructure at LO + NLO:

- (1) |p|^2 = 1 (retained unit projector ray).
- (2) Scalar-tensor ray magnitude bridge supp = 6/7 (retained).
- (3) a_d = rho (retained QUARK_PROJECTOR_PARAMETER_AUDIT).
- (4) delta_A1 = 1/42 (retained democratic center-excess).
- (5) LO ray completeness `a_u/sin_d + a_d = 1` -- **numerical at < 2%,
      clean algebraic proof at NNI-diagonalization is the cycle 11
      retention target**.
- (6) NLO excess `rho/49` is the unique minimal 3-atom contraction on
      {rho, supp, delta_A1}.

Uniqueness: only the target satisfies RPSR exactly; the 7 other Pareto
candidates miss by specific non-zero margins in (3.5e-5, 2.7e-4) --
three orders of magnitude above numerical precision, one order of
magnitude below the NLO RPSR correction. RPSR is therefore a clean
**physics tie-breaker** that replaces the Min-C "atom-economy"
structural rule.

---

## 2. Current axiom status

Min-C is **conditional theorem**:

- The RPSR identity is derived from retained infrastructure modulo one
  LO algebraic gap.
- The gap is a specific, well-posed algebraic theorem target:
  `a_u / sin_d + a_d = 1` at NNI-diagonalization with a_d = rho pinned,
  using retained CKM magnitudes from CKM_ATLAS.

**If the gap closes (cycle 11):** Min-C drops from axioms; axiom count
on quark gate 4 -> 3.

**If the gap persists:** Min-C is still **sharpened**; the axiom is no
longer the abstract atom-economy rule but the specific LO identity.
Retention path is explicit and bounded.

---

## 3. Runner status

The old runner
`scripts/frontier_quark_up_amplitude_retained_native_candidate.py` is
NOT included in this branch (superseded). Functional content is
absorbed into the RPSR runner
`scripts/frontier_quark_up_amplitude_rpsr_conditional.py` (PASS=10
FAIL=0).

All 4 retained quark runners on main also pass unchanged:

- `frontier_quark_projector_parameter_audit.py`: PASS=6 FAIL=0
- `frontier_quark_projector_ray_phase_completion.py`: PASS=8 FAIL=0
- `frontier_quark_mass_ratio_full_solve.py`: PASS=15 FAIL=0
- `frontier_quark_up_amplitude_candidate_scan.py`: PASS=7 FAIL=0

---

## 4. Cross-references

- `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md` (cycle 10D, primary)
- `docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md` (supp = 6/7 derivation)
- `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` (retained unit ray + supp + delta_A1; on main)
- `docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` (retained a_d = rho; on main)
- `docs/CYCLE_1_TO_10_SYNTHESIS_NOTE_2026-04-19.md` (reading order)
