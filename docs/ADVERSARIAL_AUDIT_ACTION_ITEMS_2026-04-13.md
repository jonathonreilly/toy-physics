# Adversarial Audit — Action Items for Codex Review

**Date:** 2026-04-13
**Source:** `ADVERSARIAL_AUDIT_2026-04-13.md` (hostile referee analysis of 6 core scripts)
**Status:** Proposed fixes — awaiting codex review before implementation

---

## Summary

No bugs, no circular reasoning, no fatal flaws found across all 6 core scripts.
Four presentation/documentation issues identified that a real referee could attack.
Proposed fixes below — none changes the underlying mathematics.

---

## Item 1: Born rule script overclaims its scope

**Script:** `frontier_born_rule_derived.py` (8/8 PASS)

**Problem:** Title says "Born rule derived" but the script proves: IF amplitudes
compose linearly and probabilities are |ψ|², THEN I₃ = 0. The I₃ = 0 identity
is true for ANY complex amplitudes — it's not specific to Cl(3) or even to
quantum mechanics. Two of the 8 checks are printed prose counted as PASS.

**Referee attack:** "This doesn't derive the Born rule. It proves a trivial
algebraic identity. The title is misleading."

**Proposed fix:**
- Rename script to `frontier_i3_zero_exact.py` or `frontier_pairwise_interference.py`
- Rename note to `I3_ZERO_EXACT_NOTE.md` (codex already uses this language)
- Change all "Born rule derived" language to "exact pairwise interference theorem"
- Remove the 2 prose-only checks or relabel them as ASSERTION

**Impact on paper:** None — codex already frames this correctly as "exact I₃ = 0
on the Hilbert surface, not a freestanding derivation of the Born rule."

---

## Item 2: CPT script breaks for odd lattice size

**Script:** `frontier_cpt_exact.py` (53/53 PASS)

**Problem:** The CPT theorem requires the lattice to have even side length L.
At odd L (tested: L=5), the transformation fails: ||H - CPT·H·CPT⁻¹|| = 17.8.
This is because the bipartite structure of Z³ requires even L for consistent
periodic boundary conditions. Standard in lattice QCD but not documented in
the script.

**Referee attack:** "Your CPT theorem only works for even lattice sizes. Is
that a physical restriction or a bug?"

**Proposed fix:**
- Add `assert L % 2 == 0, "CPT requires even L (bipartite lattice)"` at the top
- Add a comment explaining: on Z³ with PBC, even L ensures the bipartite
  sublattice structure is consistent. This is standard (cite Sharpe 2006).
- Optionally: add an explicit test at odd L that EXPECTS failure, documenting
  the restriction as a known feature

**Impact on paper:** None — the physical lattice has L ~ 10⁶⁰ (even). The
restriction is a finite-size technicality, not a physics limitation.

---

## Item 3: Anomaly script has 8 non-computational checks

**Script:** `frontier_anomaly_forces_time.py` (86/86 PASS)

**Problem:** 8 of 86 checks use `check("textbook statement", True)` — they
assert known physics results without computing anything. Examples: "anomalous
gauge theory is inconsistent" and "multiple time dimensions produce ghosts."
These inflate the check count from ~78 genuine to 86.

**Referee attack:** "8 of your 86 checks are just assertions, not computations.
Your real pass rate is 78/78."

**Proposed fix:**
- Either: replace each literal-True check with a minimal computation that
  verifies the claim (e.g., compute the ghost norm for d_t=2 and show it's
  negative; compute the Ward identity violation for an anomalous theory)
- Or: relabel these 8 as "ASSERTION (textbook)" in the output, separate from
  computational PASS/FAIL. Report score as "78 computed + 8 asserted = 86 total"

**Impact on paper:** None — the core anomaly calculation (exact Fraction
arithmetic on Tr[Y³], Tr[SU(3)²Y]) is bulletproof. The textbook assertions
are correct but not computationally verified by this script.

---

## Item 4: S³ shellability general-R argument is not constructive

**Script:** `frontier_s3_shellability.py` (32/32 PASS)

**Problem:** The shellability construction is verified computationally for
R = 2, 3, 4, 5 (32/32 genuine checks). The general-R argument ("structural
induction on the shelling construction") is prose in the docstring, not a
verified computation. R=1 gives zero cubes (vacuous pass).

**Referee attack:** "You've verified S³ for 4 values of R. That's not a proof
for all R. How do I know R = 100 works?"

**Proposed fix:**
- Extend computation to R = 6, 7, 8, 9, 10 (should be feasible — the R=5
  complex has 2448 tets, R=10 might have ~20000). If all pass, the inductive
  pattern is much more convincing.
- Alternatively: prove that the Phase 1 + Phase 2 shelling strategy works for
  general R by showing the attachment property is maintained at each step
  (this may be a short combinatorial argument)
- Document honestly: "constructively verified for R ≤ N, argued for general R
  by structural induction"

**Impact on paper:** Moderate — S³ is a newly closed gate. The proof should be
as tight as possible. Running R up to 10 is cheap insurance.

---

## Non-issues (confirmed robust)

These were tested and found solid — no action needed:

- **SU(3) commutant (106/106):** Strongest script. Correctly fails for Cl(2),
  random involutions, wrong SWAP operators. 3 tautological self-equality
  checks (negligible).
- **Graph-first selector (63/63):** Most honest script. All 63 checks are
  genuine computations. Modest claims correctly scoped.
- **Cross-script dependencies:** Linear chain (commutant → anomaly → Born),
  no circularity. CPT, S³, selector are independent.
- **Single point of failure (su(2) factor identification):** Tested with 1000
  random conjugations and all 3 axis choices — basis-independent.

---

## Recommendation

Fix items 1-4 before submission. None changes the math. All reduce the
referee attack surface. Items 1-3 are 30-minute fixes. Item 4 (extending S³
to R=10) may take longer depending on compute time.

The core scripts are solid. The adversarial audit found presentation issues,
not mathematical errors.
