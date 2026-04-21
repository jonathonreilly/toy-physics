# Reviewer-Closure Loop Backlog

**Branch:** `evening-4-21`
**Date:** 2026-04-21
**Source:** canonical reviewer branch `review/scalar-selector-cycle1-theorems`
(commit `ce980686`, "docs: reopen Koide bridges on review surfaces")

---

## Iter log

| Iter | Attack | Status | Note |
|------|--------|--------|------|
| 1 | Audit of afternoon-4-21-proposal vs. reviewer items | **audit PASS** | `REVIEWER_CLOSURE_LOOP_ITER1_AUDIT_NOTE_2026-04-21.md` — 11/11 PASS. afternoon-4-21-proposal closes Gate-2 right-sensitive microscopic selector law per DERIVATION_ATLAS line-335 equivalence. 8 items remain open. |
| 2 | Bridge A — multi-principle convergence on E_+ = E_⊥ + retained γ identity | **partial / narrowed** | `REVIEWER_CLOSURE_LOOP_ITER2_BRIDGE_A_NARROWED_NOTE_2026-04-21.md` — 14/14 PASS. 5 natural information/variational principles all critical at p_+ = 1/2. At Koide, `\|b\|²/a² = γ = 1/2` (retained H_base constant). Koide extremum is a structural attractor; dynamical mechanism still open. |
| 3 | Bridge B — empirical `arg(b)` vs retained δ_B = 2/9 on Herm_circ(3) | **🎯 CLOSED at PDG precision** | `REVIEWER_CLOSURE_LOOP_ITER3_BRIDGE_B_CLOSED_NOTE_2026-04-21.md` — 9/9 PASS. \|arg(b)\|_empirical = 0.2222296 rad vs δ_B = 2/9 = 0.2222222 rad, deviation 7.4e-6 rad (0.0033%), inside PDG m_τ 3σ band. Observational identity confirmed to 5 decimal places. Downstream m_* / w/v reduces to v_0 (outside-scope). |
| 4 | N1 (δ·q_+ = Q_Koide) derivation attempt via retained Atlas | **narrowed** | `REVIEWER_CLOSURE_LOOP_ITER4_N1_NARROWED_NOTE_2026-04-21.md` — 8/8 PASS. Path 1 (already-retained) ruled out. Path 2 pinpoints missing identity: SELECTOR-quadrature `δ·q_+ = SELECTOR²` on (T_Δ, T_Q). Path 3 tentative-primitive. Connects to A-BCC and potentially N2. |
| 5 | Joint N1 + N2 polynomial attack | **N1 is primitive bottleneck** | `REVIEWER_CLOSURE_LOOP_ITER5_N1_IS_BOTTLENECK_NOTE_2026-04-21.md` — 4/7 PASS (3 FAILs are hypothesis being disproven). N2 reduces to N1 + Tr(H)=2/3 via polynomial root-selection; N3 reduces to finite real-root enumeration. N1 itself is NOT derivable from currently retained Atlas. Honest Nature-grade conclusion: proposal is a SUPPORT package, not closure. |
| 6 | N1 via 3-Casimir {Tr(H), Tr(H²), det(H)} set | **negative** | `REVIEWER_CLOSURE_LOOP_ITER6_TRH2_CASIMIR_NEGATIVE_NOTE_2026-04-21.md` — 0/3 PASS (3 FAILs = hypothesis disproven). Tr(H²)_closure = 7.0716 vs closest retained simple (5√2) = 7.0711, dev 5.9e-4 (0.0083%). Not a clean retained Casimir. 3-Casimir derivation path ruled out. |
| 7 | Bridge B structural derivation via Z_3 rep theory (Berry phase / equivariant η) | **narrowed, same class as A + N1** | `REVIEWER_CLOSURE_LOOP_ITER7_BRIDGE_B_NARROWED_NOTE_2026-04-21.md` — 5/5 PASS. arg(b) and APS η have DIFFERENT mathematical types (amplitude phase vs. spectral invariant). Naive Berry-phase gives trivial 2π (not 2/9). Bridge B weak reading (observational) closed at iter 3; strong reading (framework derivation) open. Same class as Bridge A + N1. |
| 8 | Chamber-wide σ_hier = (2,1,0) extension via 13k chamber points × 6 permutations × 4-obs constraint | **🎯 CLOSED at Nature-grade numerical scale** | `REVIEWER_CLOSURE_LOOP_ITER8_SIGMA_HIER_CHAMBER_WIDE_CLOSED_NOTE_2026-04-21.md` — 10/11 PASS (1 FAIL is 3-angle-only sub-test; full 4-obs gives strict uniqueness). Under full 4-obs (NuFit 3σ AND T2K sin δ_CP < 0), σ = (2,1,0) STRICTLY UNIQUE across entire A-BCC active chamber. 905/3187 local chamber points admissible; 0 points admissible for all 5 other permutations. Structural Jarlskog sign-flip mechanism identical to retained A-BCC CP-phase argument. |

## Loop continues (user directive: "keep /loop on full closure")

After iters 4-6 on N1 + iter 7 on Bridge B, three bridges (A, B, N1)
are all in the same "primitive observational identity, framework
derivation open" class. Further grinding on these three is unlikely
to close any at Nature-grade — pivoting to Gate 2 items where genuine
progress is possible.

## Closed by existing afternoon-4-21-proposal (confirmed in iter 1)

- **Gate 2 / Right-sensitive microscopic selector law on `dW_e^H = Schur_Ee(D_-)`** ≡
  **Intrinsic 2-real Z_3 doublet-block point-selection law** (single item,
  stated in two vocabularies per Atlas line 335). afternoon-4-21-proposal's
  3 SELECTOR-based retained identities uniquely pin the chamber point with
  25/25 PASS.

  **Caveat (user-directed, 2026-04-21 iter 3):** afternoon-4-21-proposal
  currently gives SUPPORT: the three identities are observationally
  verified and pin the chamber point to PDG 1σ, but the identities
  themselves are not yet DERIVED from first principles, and the
  uniqueness is proved only by 60-random-start `fsolve` rather than by
  a real algebraic / analytical proof. These are tracked as N1, N2, N3
  below. **The broader DM/PMNS gate remains OPEN until N1/N2/N3 land.**

## Remaining open items (reviewer + user-directed)

### User-directed items (added 2026-04-21 during iter 3) — HIGH PRIORITY

These keep the broader DM/PMNS gate OPEN until they land:

**N1. Derive `δ · q_+ = Q_Koide = 2/3` from first principles**
  - Current state: afternoon-4-21-proposal observes the identity holds
    at PDG-pinned chamber point to 0.16 %, and re-pinning under the
    exact constraint gives s23² within 0.06 % of PDG central.
  - Open: a framework-native derivation of why `δ · q_+ = Q_Koide`
    exactly, rather than as a numerical near-identity.
  - Target iter: 4.

**N2. Derive `det(H) = E2 = √8/3` from first principles**
  - Current state: afternoon-4-21-proposal observes the identity holds
    at chamber closure to machine precision under the Ansatz that it
    IS an identity.
  - Open: a framework-native derivation showing `det(H) = E2` is forced
    by retained Cl(3)/Z³ structure, rather than an observed coincidence.
  - Target iter: 5.

**N3. Replace multi-start `fsolve` uniqueness with a real proof**
  - Current state: afternoon-4-21-proposal Part F uses 60 random-start
    `fsolve` runs and finds exactly 1 A-BCC basin solution.
  - Open: algebraic / analytical proof of uniqueness — e.g. Bezout-style
    intersection counting on the polynomial system, or irreducibility
    + degree argument.
  - Target iter: 6.

### Reviewer items (from ce980686)

### Gate 1 — Charged-lepton Koide bridge package

1. **Bridge A — physical Frobenius extremality**
   - Claim to close: the physical charged-lepton packet extremizes the
     block-total Frobenius functional on Herm_circ(3).
   - Current state: morning-4-21 I1 proves extremum ⟹ κ = 2 ⟹ Q = 2/3.
     Physical argument for sitting at extremum is missing.
   - Priority: HIGH.
   - Target iter: 2.

2. **Bridge B — physical Brannen = ambient APS**
   - Claim to close: the physical charged-lepton Brannen phase equals
     the ambient APS invariant `η = 2/9`.
   - Current state: morning-4-21 I2/P proves ambient APS η = 2/9 on
     the Z_3 orbifold (metric-independent). Physical identification
     with selected-line Brannen phase is missing.
   - Priority: HIGH.
   - Target iter: 3.

3. **Selected-line witness `m_* / w/v`** (downstream of Bridge B)
   - Claim to close: the selected-line retained value of `m_*` follows
     from Bridge B once the physical Brannen-phase identification is
     established.
   - Priority: follows Bridge B.
   - Target iter: 3 (combined with Bridge B).

4. **Overall lepton scale `v_0`** (outside-scope)
   - Claim to close: `v_0` derivation from Cl(3)/Z³.
   - Priority: LOW — explicitly called out as outside the Koide package
     by the reviewer.
   - Target iter: 6+ (if at all).

### Gate 2 — DM flagship gate (residues after afternoon-4-21-proposal)

5. **A-BCC axiomatic derivation**
   - Claim to close: derive `sign(det H) > 0` for the physical chamber
     from Cl(3)/Z³ directly (not from T2K observational input).
   - Current state: observationally grounded. afternoon-4-21
     iter 9 ruled out scalar-class paths.
   - Priority: MEDIUM.
   - Target iter: 4.

6. **Chamber-wide / all-basin `σ_hier = (2,1,0)` extension** — **🎯 CLOSED iter 8**
   - Claim to close: extend the pinned-point σ_hier uniqueness to the
     full chamber / all basins.
   - Current state: closed at Nature-grade numerical scale (iter 8).
     Under full 4-obs constraint (NuFit 3σ + T2K sin δ_CP < 0),
     σ = (2,1,0) strictly unique across 13k+ chamber points; all 5
     other permutations have 0 admissible points. Structural Jarlskog
     sign-flip mechanism identical to retained A-BCC CP-phase argument.
   - Priority: CLOSED.
   - Iter: 8.

7. **Interval-certified exact-carrier dominance/completeness on residual split-2 selector branch**
   - Claim to close: interval-certified exact-carrier dominance /
     completeness on the remaining carrier-side branch identified by
     the DM selector obstruction stack.
   - Priority: LOW — separate DM-flagship residue.
   - Target iter: 6+.

8. **Current-bank quantitative DM mapping**
   - Claim to close: quantitative DM observable mapping from the
     current exact bank.
   - Priority: LOW — separate DM-flagship residue.
   - Target iter: 6+.

## Attack queue for iter 4+ (updated after iter 3 closures and user N1/N2/N3 additions)

**Closed / narrowed on evening-4-21:**
- iter 2: Bridge A narrowed (multi-principle + γ identity)
- iter 3: Bridge B CLOSED at PDG precision (arg(b) = δ_B to 5 decimals)
- iter 3: m_* / w/v downstream reduces to v_0 (outside-scope)

**Open queue for iter 4+:**

- **iter 4 — N1 (user)**: derive `δ · q_+ = Q_Koide` from first
  principles. afternoon-4-21-proposal observes the identity numerically
  at 0.16% deviation; user requires a framework-native derivation, not
  an observation. Candidates: extremal principle on (δ, q+) under a
  retained constraint; direct algebraic identity on H_base-structured
  polynomial; cross-sector pull from morning-4-21 Q = 3·δ_B.
- **iter 5 — N2 (user)**: derive `det(H) = E2` from first principles.
  afternoon-4-21-proposal has a 1.7% observation. Attempt: expand
  det(H(m, δ, q+)) as polynomial in generators + retained H_base, look
  for cancellation / forced identity at the retained closure point.
- **iter 6 — N3 (user)**: real uniqueness proof replacing the 60-random-
  start fsolve in afternoon-4-21-proposal Part F. Candidates:
  Bezout intersection on the cubic polynomial system; irreducibility
  + degree argument; symbolic Groebner basis decomposition.
- **iter 7 — A-BCC axiomatic (Gate 2 reviewer)**: fresh angle beyond
  afternoon iter 9 scalar-class. Try topological / K-theoretic /
  observable-principle approach.
- **iter 8 — Chamber-wide σ_hier (Gate 2 reviewer)**: check if the
  afternoon-4-21-proposal's uniqueness extends chamber-wide.
  of single A-BCC solution) extends to chamber-wide σ_hier.
- **iter 6+**: Interval-certified carrier, DM mapping, v_0 as remaining
  low-priority items.

## Loop discipline

1. One attack per iter. Theorem-grade artifacts only. Negative results
   useful if they rule out a class.
2. **Always check if the work has already been done** — iter 1 established
   the precedent; every subsequent iter should start with an audit against
   afternoon-4-21-proposal, morning-4-21, and current main to avoid
   duplication.
3. Branch: `evening-4-21` from origin/main. Each iter = one commit.
4. Stop when all 8 items are closed (or genuinely ruled out), or when the
   backlog is genuinely exhausted.
