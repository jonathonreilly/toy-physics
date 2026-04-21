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

## Closed by existing afternoon-4-21-proposal (confirmed in iter 1)

- **Gate 2 / Right-sensitive microscopic selector law on `dW_e^H = Schur_Ee(D_-)`** ≡
  **Intrinsic 2-real Z_3 doublet-block point-selection law** (single item,
  stated in two vocabularies per Atlas line 335). afternoon-4-21-proposal's
  3 SELECTOR-based retained identities uniquely pin the chamber point with
  25/25 PASS.

## Remaining open reviewer items (8)

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

6. **Chamber-wide / all-basin `σ_hier = (2,1,0)` extension**
   - Claim to close: extend the pinned-point σ_hier uniqueness to the
     full chamber / all basins.
   - Current state: observational at pinned point. Chamber-wide open.
   - Priority: MEDIUM.
   - Target iter: 5.

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

## Attack queue for iter 2+

- **iter 2**: Bridge A (Gate 1). Try cross-sector pull: afternoon-4-21-proposal
  has Tr(H) = Q_Koide and δ·q+ = Q_Koide. If the morning-4-21 Frobenius
  functional's maximum on Herm_circ(3) equals Tr(H_physical) or another
  afternoon-closure identity, Bridge A's extremal-principle is forced by
  the afternoon closure — a genuine cross-sector reduction.
- **iter 3**: Bridge B + m_* witness (Gate 1). Try: morning-4-21 APS
  η = 2/9 on Z_3 orbifold; afternoon-4-21-proposal has δ·q+ = 2/3 = 3·(2/9)
  from the retained identity Q = 3·δ_B. Does the afternoon chart-δ
  coordinate literally equal the retained Brannen phase times some
  retained factor? If so, Bridge B reduces to a chart-coordinate identity.
- **iter 4**: A-BCC (Gate 2). Try fresh angle beyond the scalar-class
  ruled out in afternoon iter 9 — e.g., topological / K-theoretic /
  observable-principle argument.
- **iter 5**: Chamber-wide σ_hier (Gate 2). Check whether the
  afternoon-4-21-proposal's uniqueness result (60-random-start proof
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
