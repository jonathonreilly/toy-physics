# DPLE Cannot Close A-BCC: Sign-Blindness No-Go

**Date:** 2026-04-19
**Status:** Formal no-go theorem. DPLE is a scalar-selector support
theorem on the open DM gate; it cannot derive the A-BCC axiom
(physical sheet = C_base).
**Companion to:**
`docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`

---

## 1. Precise statement

**Theorem (DPLE sign-blindness no-go).** The DPLE principle — that
W(t) = log|det H(t)| has at most floor(d/2) interior Morse-index-0
critical points on any open interval — cannot derive the A-BCC axiom
(identification of C_base = {det H > 0} as the physical PMNS sheet).

---

## 2. Background: what A-BCC and DPLE each say

**A-BCC (axiom, still open on DM flagship).** Among the connected
components of {det(H_base + J) ≠ 0}, the physically realized PMNS sheet
is the baseline-connected component C_base containing J = 0, i.e. the
component where det(H_base + J) > 0 (same sign as det H_base). This
is stated as an open item in `DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17`
(section "Still open", item 7).

**DPLE (theorem, this cycle).** On the retained linear Hermitian pencil
H(t) = H_0 + t H_1 with H_0 invertible, the observable

    W(t) = log|det H(t)|

has at most floor(d/2) interior Morse-index-0 critical points. The
vertical bars denote absolute value of det.

**F_3 (the retained F4 condition at d=3).** Four conditions:

  (1) Delta_ret = c_2^2 - 3 c_1 c_3 > 0       [real interior CP]
  (2) t_* = (-c_2 + sqrt(Delta_ret))/(3 c_3) in (0,1)  [in interval]
  (3) p''(t_*) > 0                              [Morse-index-0]
  (4) p(t_*) > 0  AND  sign(p(t_*)) = sign(c_0) [positive det, = C_base]

DPLE derives (1)-(3): at d = 3, the floor(3/2) = 1 bound makes the
interior minimum unique, so (1)-(3) are provably theorem-grade. Condition
(4) is a SIGN condition on det (not |det|).

---

## 3. Proof of the no-go

**Step 1: DPLE uses |det|, not det.**

W(t) = log|det H(t)|. Its critical points satisfy

    W'(t) = Tr[H(t)^{-1} H_1] = p'(t) / p(t)  =  0  iff  p'(t) = 0.

The Morse-index-0 condition is W''(t_*) > 0. None of these conditions
reference the SIGN of p(t_*); they reference only whether the derivative
vanishes and whether the second derivative is positive. The floor(d/2)
bound counts CPs of W = log|p|, which is the same for p > 0 and for p < 0
(since |p| is the same either way in terms of local geometry).

**Step 2: The DPLE bound holds for C_neg pencils (det H_0 < 0).**

Take any H_0 with det H_0 < 0 (i.e., H_0 in C_neg). The same Morse-index
argument applies: log|det(H_0 + t H_1)| has at most floor(d/2) interior
Morse-index-0 CPs. This is verified numerically in runner T8
(`frontier_dm_dple_theorem.py`): over 500 random C_neg pencils at d = 3,
the maximum interior Morse-index-0 CP count is <= 1.

**Step 3: The sign-match analog F_3^{neg} also produces a unique-basin selector on C_neg.**

For a C_neg pencil (det H_0 < 0), define F_3^{neg} by replacing condition
(4) with sign(p(t_*)) = sign(c_0) < 0. By DPLE, there is at most one
interior Morse-index-0 CP. Runner T8 finds explicit C_neg pencils
satisfying F_3^{neg} = True (interior minimum with p(t_*) < 0). The
sign-matched analog exists on C_neg just as on C_base.

**Step 4: DPLE cannot prefer C_base over C_neg.**

From steps 2-3: DPLE's generic structure is sign-symmetric. For any
(H_base, J_*) pair where F_3 = True on C_base, the analogous C_neg
setup supports F_3^{neg} = True on C_neg. DPLE has no mechanism to
distinguish the two.

Therefore: any argument of the form "DPLE => Basin 1 is the physical
basin" must smuggle in the sign condition (4), which is A-BCC. DPLE
cannot supply that sign condition from the log|det| observable alone.

**Step 5: The sign condition in F_3 IS A-BCC encoded.**

Condition (4) requires sign(p(t_*)) = sign(det H_base) > 0. This is
equivalent to: "the linear path from J = 0 to J_physical passes through
an interior minimum of det at which det > 0, i.e., the path stays on
C_base." This is A-BCC restricted to linear paths. P3 Sylvester confirms
that the physical Basin 1 path satisfies this as a theorem (det > 0 on
[0,1]); but that confirmation uses A-BCC as its premise (Basin 1 is the
physical basin), not as its conclusion.

**Conclusion.** DPLE derives conditions (1)-(3) of F_3. Condition (4)
encodes A-BCC. DPLE cannot derive A-BCC. QED.

---

## 4. What DPLE does buy (correct account)

DPLE is a genuine and non-trivial scalar-selector theorem:

- It demotes F4 from an imposed axiom to a theorem on the retained
  scalar-selector sub-gate (conditioned on A-BCC).
- It proves the d = 3 uniqueness of the clean binary selector structure:
  at d = 2 the condition is vacuous; at d >= 4 it fragments (multiple
  interior Morse-index-0 CPs possible).
- Combined with the other scalar-selector closures (MRU, Berry), it unifies
  the three Tier-1 scalar-selector routes as `d = 3`
  specializations of dim-parametric principles.

None of this implies source-side closure.

---

## 5. What remains open

A-BCC: deriving from the Cl(3)/Z^3 axiom why the physical PMNS sheet is
C_base. Candidate routes:

- **Observable-continuity / Grassmann-additivity** on W[J] = log|det|:
  derive that the physical sheet must be the connected component
  containing the zero-source baseline J = 0.
- **Structural sign theorem**: derive from retained source-package
  theorems that det(H_base) > 0 is an algebraic necessity, and that
  physical J-deformations preserve sign.

Neither route has been supplied. The A-BCC CP-phase no-go theorem
(main, `ABCC_CP_PHASE_NO_GO_THEOREM_NOTE_2026-04-19.md`) provides
observational grounding: all known C_neg chi^2=0 basins give
sin(delta_CP) > +0.247, which is T2K-excluded at >3sigma. This is strong
observational support for A-BCC but is not a derivation from retained
framework structure.

---

## 6. Relationship to the P3 Sylvester theorem

P3 Sylvester (`DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md`)
proves that the linear path from J = 0 to J_*(Basin 1) stays in C_base:
det(H_base + t J_*) > 0 for all t in [0, 1]. This is the pointwise
signature theorem AT the P3 pin.

P3 Sylvester proves Basin 1 is ON C_base (given that Basin 1 is the pin).
DPLE proves that on C_base, the unique interior minimum of det is at t_*
(F_3 structure). Neither P3 Sylvester nor DPLE derives WHY Basin 1 is the
physical pin, i.e., neither derives A-BCC. A-BCC is the input that
converts "Basin 1 is on C_base" into "Basin 1 is the physical basin."

---

## 7. Verdict

**DPLE is an honest support theorem on the open DM scalar-selector gate.**

It closes the F4 axiom on the conditioned sub-gate. It does not close
A-BCC. The source-side physical-sheet identification remains the single
open input on the DM flagship.

The this cycle synthesis description "DM A-BCC basin: axiom cost 1 -> 0"
refers to the F4 scalar-selector axiom only. The DM flagship lane remains
open pending A-BCC closure.
