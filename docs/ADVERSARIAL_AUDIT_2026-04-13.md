# Adversarial Script Audit -- Hostile Referee Analysis

**Date:** 2026-04-13
**Auditor posture:** Hostile referee attempting to break each script
**Scripts audited:** 6 core frontier scripts
**Method:** Source code review, execution, input perturbation, tautology detection

---

## Executive Summary

The six scripts range from genuinely strong (SU(3) commutant) to
significantly overclaimed (Born rule). No outright bugs or circular
reasoning were found. The main systemic issues are:

1. **Inflated check counts** -- multiple scripts pad their scores with
   `check("statement", True)` calls that perform zero computation.
2. **Overclaimed scope** -- the Born rule script title says "derived"
   but it proves a weaker statement (I_3 = 0 given Born rule).
3. **Hidden lattice-size assumption** -- CPT requires even L, which is
   not documented as a constraint.
4. **The su(2)-on-factor-1 choice** remains the single largest conceptual
   assumption across the framework. The graph selector script addresses
   this partially but not completely.

No circular dependencies between scripts. No tautological passes that
would accept an incorrect algebra. The numerical checks are genuine.

---

## Script 1: frontier_su3_formal_theorem.py (106/106)

### Verdict: STRONG. The strongest script of the six.

**What it claims:** The commutant of {su(2) on factor 1, SWAP_23} in the
KS representation of Cl(3) is su(3) + u(1).

**Does it actually prove this?** YES, with genuine numerical verification.
The commutant computation uses SVD null-space analysis -- a real linear
algebra computation, not a tautology. The result dim=10 for the
commutant is a non-trivial output that would change for different inputs.

**Adversarial tests performed:**
- Cl(2) instead of Cl(3): commutant dimension drops to 1 (not 10). CORRECT.
- SWAP_12 instead of SWAP_23: does not commute with su(2). CORRECT.
- Random involution instead of SWAP_23: does not commute with su(2). CORRECT.
- Identity instead of SWAP_23: commutant stays at 16 (no reduction). CORRECT.

**Tautological checks found:** 3 checks on lines 107-109 verify that the
KS gammas equal their own definitions (G1 = sx x I x I). These pass by
construction and test nothing. Impact: negligible (3 of 106).

**The "T2 not in Cl(3)" check:** Genuine. The Cl(3) basis is entirely
real-valued; T2 = sy/2 x I x I has imaginary entries and cannot be
reconstructed. Reconstruction error = 1.414, well above the 0.1 threshold.

**Weakest check:** Lines 107-109 (tautological self-equality). These
could be removed without affecting the proof.

**Hidden assumptions:**
1. The choice of su(2) on factor 1 (not factor 2 or 3). This is the main
   input to the theorem, not derived within this script.
2. The choice of SWAP_23 (not SWAP_12 or SWAP_13). This IS derived: it is
   the unique swap commuting with the chosen su(2).

**Single point of failure:** If the su(2)-on-factor-1 identification is
physically wrong, the entire su(3) derivation fails. The graph selector
script partially addresses this.

---

## Script 2: frontier_anomaly_forces_time.py (86/86)

### Verdict: GOOD with significant padding. ~78 genuine checks, 8 are literal True.

**What it claims:** Anomaly cancellation of the LH content from Cl(3) forces
d_time = 1, deriving 3+1D spacetime.

**Does it actually prove this?** The anomaly computation (Steps 1-2) is
exact and uses Python's Fraction arithmetic -- no floating-point issues.
The Clifford algebra chirality argument (Step 3) is numerically verified
with explicit matrix constructions. Step 4 (uniqueness of d_t=1) is
entirely prose with `check("...", True)` calls.

**Eight tautological checks (literal True):**
- Line 268: `check("SU(3)^3 anomaly = 0", True, "2 - 1 - 1 = 0")`
- Lines 483, 485, 501, 514, 516, 526, 548: All physical arguments
  (CTCs, Ostrogradsky, etc.) passed as True without computation.

These are textbook physics arguments that are correct, but counting them
as PASS inflates the score. The honest count would be ~78/78 computed
checks plus 8 asserted-true physics arguments.

**Adversarial tests performed:**
- Independent anomaly recalculation: Tr[Y^3]_LH = -16/9, Tr[Y^3]_full = 0.
  Exactly matches. The Fraction arithmetic is bulletproof.
- The claim that RH charges are "uniquely" determined: This has a 2-fold
  degeneracy (Branch A/B) which is correctly documented as a relabeling
  (e_R <-> nu_R).

**Weakest check:** The 8 literal-True assertions in Step 4. These are
not computations but textbook knowledge assertions.

**Hidden assumptions:**
1. Takes the LH content (2,3)_{+1/3} + (2,1)_{-1} from the SU(3)
   commutant theorem as given. If Script 1 is wrong, this script fails.
2. The physical elimination of d_t >= 2 relies on standard GR/QFT
   arguments (no CTCs, no Ostrogradsky) that are asserted, not derived.

---

## Script 3: frontier_born_rule_derived.py (8/8)

### Verdict: OVERCLAIMED. Title says "derived" but proves something weaker.

**What it claims (title):** Born rule derived from lattice propagator structure.

**What it actually proves:** If you assume Hilbert space + P = |A|^2
(the Born rule), then the Sorkin parameter I_3 = 0. This is correct
but circular: the Born rule is an INPUT, not an output.

**The script acknowledges this** in its docstring and theorem statement,
noting that I_3 = 0 is an "algebraic identity" that holds "for ANY
complex numbers A, B, C" and that the lattice structure is "irrelevant."
The title is misleading but the content is honest.

**Two zero-computation checks:**
- Check 2 (symbolic expansion): Prints the algebraic proof as text.
  No computation. `pass_count += 1` awarded for printed prose.
- Check 8 (theorem statement): Prints the theorem. No computation.
  `pass_count += 1` awarded for printed prose.

**Genuinely tautological nature of the remaining checks:**
Checks 1, 3, 4 verify I_n = 0 for random complex numbers. This is
testing the identity |a+b+c|^2 - |a+b|^2 - ... = 0, which holds for
ALL complex numbers by high-school algebra. These checks would pass
for ANY Hilbert space, not just Cl(3).

**Check 5 (non-Born detection) is the best check:** It verifies that
P = |A|^p with p != 2 gives I_3 != 0. This genuinely tests
discriminating power and would fail if the formula were wrong.

**Checks 6-7 (lattice propagator):** Correct but redundant. They compute
lattice amplitudes and verify I_3 = 0, but the result follows from the
algebraic identity regardless of the amplitudes.

**Weakest checks:** 2 and 8 -- zero computation, pure prose awarded PASS.

**Critical assessment:** The script should be titled "Born rule implies
I_3 = 0" or "Sorkin test consistency." Calling it "Born rule derived"
suggests the Born rule follows from the lattice, which the script does
not demonstrate. The script's own text correctly states this, but the
title and filename are misleading.

---

## Script 4: frontier_cpt_exact.py (53/53)

### Verdict: SOLID with one hidden assumption and some redundancy.

**What it claims:** CPT is an exact symmetry of the staggered Cl(3)
Hamiltonian on Z^3 with periodic boundary conditions.

**Does it actually prove this?** YES. The algebraic proof is:
C H C = -H, P H P = -H, T H T^-1 = H (H is real), therefore
CPT H (CPT)^-1 = C P H P C = C(-H)C = -(-H) = H.
This is verified numerically for L = 4, 6, 8.

**Hidden assumption: EVEN L REQUIRED.**
The script only tests L = 4, 6, 8 (all even). I tested L = 5 (odd):
CPT FAILS with ||H - CPT*H*(CPT)^-1|| = 17.8. The reason: on odd-L
lattices with periodic boundary conditions, the sublattice structure
breaks at the wrap-around. Sites (L-1, 0, 0) and (0, 0, 0) are
both even-parity for odd L, so the hop between them does not flip
the sublattice parity. This breaks C H C = -H.

This is standard lattice QCD practice (staggered fermions require even L),
but the script does not document this constraint. An adversary could
claim the proof is incomplete for odd L.

**Severity:** LOW. Even L is a standard requirement for staggered
fermions. But it should be documented.

**Redundant checks:** The SME coefficient computation (all zero) is
logically equivalent to CPT invariance -- if CPT H (CPT)^-1 = H,
then the CPT-odd part is zero by definition. Similarly, "[CPT, H] = 0"
and "spectrum preserved under CPT" are reformulations of the same fact.
The 53 checks represent roughly 10-15 genuinely independent facts,
verified at 3 lattice sizes.

**Weakest check:** The spectrum preservation check -- it is an automatic
consequence of [CPT, H] = 0 and adds no independent information.

---

## Script 5: frontier_s3_shellability.py (32/32)

### Verdict: SOLID for finite R. General-R claim is prose, not computation.

**What it claims:** M_R = B_R union cone(dB_R) is PL homeomorphic to S^3
for all R >= 1, proved by constructive shelling.

**Does it actually prove this?** For R = 2, 3, 4, 5: YES. The shelling
orders are explicitly constructed and verified. For general R: the
argument is stated in prose (lines 903-933) and is plausible but not
machine-checked.

**R = 1 gap:** The docstring says "For every R >= 1" but R = 1 produces
zero cubes (all 8 corners of a unit cube at distance sqrt(3) > 1 from
origin). The code starts at R = 2. This is a cosmetic inconsistency.

**Shelling verification strength:** The check requires each new tet
to share at least one face with the previously built complex. For
3-simplices, this IS the correct shelling condition (any two faces
of a tet share an edge, so shared faces are automatically connected).
The implementation is correct.

**All checks are genuinely computed:** No literal-True passes. The
vertex link checks (S^2), Euler characteristic (chi = 0), boundary
sphere verification, and shelling validity are all real computations.

**Weakest check:** The vertex-decomposability check for R = 2, 3 uses
a greedy algorithm that may not find an order even when one exists.
The script correctly notes this limitation and does not count incomplete
vertex decomposability as a failure.

---

## Script 6: frontier_graph_first_selector_derivation.py (63/63)

### Verdict: HONEST. Claims are modest and well-supported.

**What it claims:** The quartic invariant of cube-shift operators selects
coordinate axes as minima, providing a graph-native axis selector.

**Does it actually prove this?** YES. The selector F(p) = sum_{i<j} p_i p_j
is explicitly computed from Tr(H^4) and shown to have axis minima. The
simplex scan verifies minima are exactly at the three vertices.

**Dimension specificity:** The formula Tr(H^4) - Tr(H^2)^2/8 uses
the hardcoded 8 = 2^3 (dimension of the d=3 cube space). For d=2
the divisor would be 4, for d=4 it would be 16. This is not a bug
-- the script explicitly works in d=3 -- but the selector mechanism
works identically for any d, not just d=3.

**Adversarial test (other dimensions):** The axis-selection property
holds for d=2 and d=4 as well. The selector is a generic property of
commuting involutions, not specific to Cl(3). The script is honest
about this: it claims "graph-first" axis selection, not Cl(3)-specific.

**All 63 checks are genuine computations.** The permutation covariance
checks (18 checks for all S_3 permutations of axes), the exact trace
formulas, and the simplex analysis are all real.

**Weakest check:** The Z_2 stabilizer check (lines 205-213) verifies
that swapping the other two axes preserves the selected axis. This is
trivially true for any coordinate axis and does not test anything
about the dynamics.

**What remains unproven:** The script derives the axis selector but
does NOT connect it to the SU(3) commutant theorem. The concluding
text correctly states: "The remaining step is to integrate this
selected axis into the bounded commutant theorem."

---

## Cross-Script Dependency Analysis

**Dependency graph:**
```
F (graph selector) --[provides axis choice]--> A (SU(3)) --[provides LH content]--> B (anomaly/3+1D)
C (Born rule): INDEPENDENT
D (CPT): INDEPENDENT  
E (S3 shellability): INDEPENDENT
```

**Circular dependencies:** NONE found. F -> A -> B is a linear chain.
F does not use SU(3) (only cube shifts). A does not use anomaly results.

**Single point of failure:** The su(2)-on-factor-1 identification.
If this choice is physically wrong, Scripts A and B both fail.
Script F partially addresses this by deriving axis selection from
graph-native data, but the bridge from "selected axis" to
"su(2) on that factor" remains an assumption.

---

## Summary Table

| Script | Claimed | Genuine | Literal True | Tautological | Overclaimed? |
|--------|---------|---------|-------------|-------------|-------------|
| SU(3) commutant | 106 | ~103 | 0 | 3 (self-equality) | No |
| Anomaly/3+1D | 86 | ~78 | 8 | 0 | Slightly (Step 4) |
| Born rule | 8 | 5 | 0 | 2 (prose passes) | YES (title) |
| CPT exact | 53 | ~15 independent | 0 | 0 | No (redundancy, not overclaim) |
| S3 shellability | 32 | 32 | 0 | 0 | Slightly (R>=1 vs R>=2) |
| Graph selector | 63 | 63 | 0 | 0 | No |

## Ranked by Strength (strongest first)

1. **SU(3) commutant** -- genuine numerical proof of a non-trivial algebraic fact
2. **S3 shellability** -- constructive proof with no shortcuts (for finite R)
3. **CPT exact** -- correct theorem, well-verified (hidden even-L assumption)
4. **Graph selector** -- honest scope, all checks genuine, but modest claim
5. **Anomaly/3+1D** -- strong core padded with asserted physics
6. **Born rule** -- misleading title, proves weaker statement than claimed

## Recommendations

1. **Born rule script:** Rename to `frontier_sorkin_test.py` or
   `frontier_born_implies_i3_zero.py`. The current title overclaims.
2. **Anomaly script:** Replace the 8 literal-True checks with actual
   computations (e.g., verify propagator convergence numerically for
   d_t = 1 vs d_t = 2, compute CTC length for d_t = 2).
3. **CPT script:** Add an explicit assertion that L must be even, with
   a brief note about why (bipartite lattice structure requires it).
4. **S3 script:** Change "R >= 1" to "R >= 2" in the docstring, or
   add a degenerate-case note for R = 1.
5. **All scripts:** Consider reporting independent-check counts alongside
   total-check counts to give a more honest picture of proof strength.
