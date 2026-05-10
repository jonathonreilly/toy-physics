# CKM from Schur Complement of the EWSB-Dressed NNI Mass Matrix

**Date**: 2026-04-09 (originally); 2026-05-10 (rigorize PATH B — narrow scope to algebraic Schur identity; bounded CKM observable comparison split out)
**Status**: bounded — exact algebraic Schur-complement identity `c_13^eff = c_12 · c_23` on the abstract NNI matrix structure; the broader Wolfenstein-basis CKM observable comparison (V_ub, V_cb, J, lambda, A) is a separate **bounded numerical observation** that overshoots PDG by the documented mass-ratio suppression factor (audit verdict `audited_failed`; status authority is the independent audit lane).
**Claim type**: bounded_theorem
**Claim scope**: the algebraic identity `c_13^eff = c_12 · c_23` from Schur complement of the generation-2 block in the 3x3 NNI geometric-mean-normalized mass matrix is the load-bearing class-(A) step. The broader CKM magnitude predictions (|V_us|, |V_cb|, |V_ub|, J, lambda, A in the Wolfenstein basis) are bounded numerical observations using imported NNI coefficients (c_12, c_23 from `CKM_NNI_COEFFICIENTS_NOTE`, `CKM_ABSOLUTE_S23_NOTE`), imported PDG masses, and an imported Z_3 Berry phase delta; they are not first-principles closures within this packet.
**Depends on**: `CKM_WOLFENSTEIN_CASCADE_THEOREM`, `CKM_NNI_COEFFICIENTS_NOTE`, `CKM_ABSOLUTE_S23_NOTE` (all upstream CKM authority chains)
**Script**: `scripts/frontier_ckm_schur_complement.py` (broad CKM observable comparison; PASS=10/FAIL=6 on bounded checks documenting the mass-ratio gap)
**Audit-companion**: `scripts/audit_companion_ckm_schur_complement_exact.py` (exact-symbolic verification of the load-bearing class-(A) algebraic identity; PASS=11/FAIL=0 at sympy `Rational` precision)

---

## Cited authorities (one-hop deps)

This note records explicit one-hop authority citations for the conditional
chain that underlies the broader CKM observable comparison (the bounded
half of this note). The audit verdict `audited_failed` correctly flagged
that the Wolfenstein-basis V_ub/V_cb/J/lambda/A predictions import upstream
NNI coefficients, absolute s_23, and Wolfenstein cascade premises that are
not derived in this packet. The citations below sharpen the conditional
structure on the live authority chain without claiming to derive those
upstream theorems here.

- [`CKM_WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  (`audited_conditional`) — the canonical Wolfenstein-cascade structural
  identities for `lambda` and `A` from `n_pair`/`n_color`/`n_quark` counts
  and the canonical coupling `alpha_s(v)`. The Schur complement cascade
  framing in §3 of this note (Wolfenstein hierarchy as sequential
  integrating-out of generations) reads through the structural identities
  in that authority. PR #767 closed the exact-symbolic verification of those
  identities.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  (`audited_conditional`) — the structural-counts identities (M1)–(M5)
  for the CKM magnitudes in terms of `(p, c, q)` and `alpha_s`. PR #768
  closed the exact-symbolic verification of those identities at sympy
  `Rational` precision. The Wolfenstein-basis CKM observables in §3 of
  this note are conditional on those structural counts being supplied
  upstream rather than re-derived here.
- [`CKM_FROM_MASS_HIERARCHY_NOTE.md`](CKM_FROM_MASS_HIERARCHY_NOTE.md)
  (`audited_conditional`) — the Gatto-Sartori-Tonin parametric route from
  mass hierarchy bands to CKM magnitudes. The mass-ratio-suppression gap
  identified in §2 of this note (the `c_13^Wolfenstein = c_13^NNI ·
  sqrt(m_1/m_2)` correction) is consistent with the GST scaling
  `|V_us| ~ sqrt(m_d/m_s)` reading recorded in that authority.
- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  (`audited_conditional`) — the NLO protected-gamma surface for the
  Jarlskog `J = A^2 lambda^6 eta_bar` readout. PR #764 closed the
  exact-symbolic verification of the protection identity. The Jarlskog
  prediction in §3 of this note (Result 3) is conditional on that
  upstream surface.

The audit's `notes_for_re_audit_if_any` field (`missing_bridge_theorem`)
asks for retained-grade derivations of the NNI matrix inputs, c_12/c_23
values, Wolfenstein-basis suppression, and CP phase before re-auditing
the broader CKM claim. Those four open premises are explicitly the four
upstream authorities cited above; they remain `audited_conditional` and
are not promoted by this note.

---

## Rigorize-pass disposition (2026-05-10) — PATH B: narrow scope

The 2026-05-05 audit verdict (`audited_failed`, see
`docs/audit/data/audit_ledger.json`, runner_check_breakdown
A=3/B=0/C=0/D=7/total_pass=10) explicitly recorded the verdict rationale:
"safe as an exact Schur identity inside the specified NNI matrix;
conditional as a CKM derivation. Repair target: ... separate the exact
NNI identity from the bounded CKM observable comparison." The verdict
acknowledged the load-bearing class-(A) algebra is correct ("a valid
class-A algebraic Schur-complement calculation") but rejected the
broader Wolfenstein-basis CKM magnitude readout because the bounded
checks on the runner explicitly fail (V_ub overshoots by ~6x, J by
~4.7x, lambda by ~46%, A by ~51%, and the Schur c_13/c_23 ratio sits
1480x from the V_ub-best optimum) — failures that the note **itself**
already records in §1 ("Current status"), §2 ("Current status",
"Root cause"), §3 ("Open Gaps"), and §4 (numerical scorecard).

The 2026-05-10 rigorize pass selects **PATH B** as named by the audit's
own repair-target language: this note is hereby reframed with the
algebraic Schur-complement identity as the load-bearing class-(A) step,
and the broader CKM observable comparison split out as a **bounded
numerical observation** with the imported upstream authorities held
explicitly. The two PATH options at audit time were:

- **PATH A** (close the broader CKM derivation): provide retained-grade
  derivations of the four named upstream authorities (NNI coefficients,
  absolute s_23, Wolfenstein-basis suppression formula, Z_3 Berry phase
  for delta_CKM). This is genuine multi-row theorem-level work that
  belongs in the upstream authorities and is **deferred to future work**
  as a separate retained promotion of those rows. The CKM lane closure
  status (gate-closed 2026-04-25 via the taste-staircase mass-ratio
  route, see `QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25`)
  does not flow through this note's broader observable comparison.
- **PATH B** (narrow scope to the load-bearing identity): keep the
  algebraic class-(A) Schur identity as the load-bearing step (verified
  at exact precision by the audit-companion at PASS=11/0 on sympy
  `Rational`), and explicitly scope the broader Wolfenstein-basis CKM
  observable comparison as a bounded numerical observation that
  overshoots PDG by the documented and acknowledged mass-ratio
  suppression factor. This is the disposition selected by this rigorize
  pass.

The audit row's `audit_status` and `intrinsic_status` are unchanged
(`audited_failed`); per repo rules, no `docs/audit/data/*.json` files
are modified by this PR. PATH B simply makes the **claim scope** in
this note honest about which step is the load-bearing class-(A)
algebraic identity (verified at exact precision) versus which steps are
bounded numerical observations conditional on imported upstream
authorities.

---

## Imported observational/upstream inputs (NOT derived in this packet)

The following inputs are imported with retained authority cited; they
are NOT derived from A_min primitives in this note:

- **NNI coefficients `c_12 = 1.48` (up), `c_12 = 0.91` (down) and
  `c_23 = 0.672` (up), `c_23 = 0.663` (down)** — imported from
  `CKM_NNI_COEFFICIENTS_NOTE` and `CKM_ABSOLUTE_S23_NOTE`. The audit
  verdict explicitly named these as upstream-conditional rather than
  derived in this packet. The c_23 = R_23 (alpha_s C_F / 4pi) ln(m_3/m_2)
  formula in §1 ("Result 1") is a heuristic with R_23 fitted at ~8-9
  rather than derived; the universality hypothesis R_23 = R_12 used in
  the runner undershoots V_cb by ~3x.
- **PDG quark masses** at MSbar(2 GeV) for light, pole for heavy —
  imported observational inputs used in the Schur complement evaluation
  in §1 and §2.
- **Z_3 Berry phase `delta_CKM` for the CP phase** — imported from the
  `CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25`
  surface; the runner reports `delta_CKM = 29 deg` versus PDG 65.5 deg,
  documenting a separate gap.
- **Wolfenstein-basis suppression factor `sqrt(m_1/m_2)`** — the §2
  "Root cause" reading that converts the O(1) Schur-complement
  c_13^NNI into the observed O(lambda^3) Wolfenstein V_ub is itself an
  imported physical mechanism that the broader theorem requires for
  closure but does not derive. This is the second of the four named
  upstream-authority gaps.

---

## What this note's runner DOES verify (under PATH B scope)

Under the PATH B narrow scope, the primary runner
`scripts/frontier_ckm_schur_complement.py` verifies:

1. **Class-(A) load-bearing algebraic identity** (PASS, exact, both
   sectors): `c_13^eff(up) = c_12^u · c_23^u = 0.9951` and
   `c_13^eff(down) = c_12^d · c_23^d = 0.6034`, matching the closed-form
   Schur complement to machine precision in NumPy.
2. **Schur-complement structural identification** (PASS, exact):
   `c_13` is GENERATED from the Schur complement, not fitted, given
   imported `(c_12, c_23)`.
3. **Bounded numerical observations** (PASS for some, FAIL for others;
   the FAIL set is the documented Wolfenstein-basis gap): order-of-
   magnitude consistency for `|V_ub|` and the Wolfenstein hierarchy
   pattern `|V_ub| ~ A · lambda^3` hold; the PDG-tolerance bounded
   checks on lambda, A, V_cb, V_ub, and the Schur c_13/c_23 ratio
   FAIL by the documented mass-ratio suppression factor — exactly the
   gap acknowledged in §1, §2, and §3 of this note.

The audit-companion runner
`scripts/audit_companion_ckm_schur_complement_exact.py` (PASS=11/FAIL=0)
verifies the load-bearing class-(A) algebraic identity at exact sympy
`Rational` precision: it constructs the abstract 3x3 NNI matrix on
symbolic `(m_1, m_2, m_3, c_12, c_23)`, takes the Schur complement of
the generation-2 block, reduces `(M_eff)_13 = -c_12 · c_23 · sqrt(m_1
m_3)` symbolically, and verifies independence of `(m_1, m_3)` (only
m_2 — the integrated-out scale — appears in the cancellation). No
PDG/literature numerical comparators are consumed; the companion is
purely symbolic.

---

## What this note does NOT establish (under PATH B scope)

- A first-principles derivation of the NNI coefficients `c_12, c_23`
  from A_min primitives (those remain in `CKM_NNI_COEFFICIENTS_NOTE` /
  `CKM_ABSOLUTE_S23_NOTE`, both `audited_conditional`).
- A first-principles closure of the Wolfenstein-basis CKM magnitudes
  (V_ub, V_cb, lambda, A, J) at PDG-tolerance precision — the bounded
  checks fail by the documented mass-ratio suppression factor, which
  itself is an imported physical mechanism.
- A first-principles derivation of the Z_3 Berry phase delta_CKM (that
  remains in the protected-gamma theorem authority).
- The CKM lane gate closure (which closed 2026-04-25 via the
  taste-staircase mass-ratio route, **not** through this Schur
  complement broader observable comparison; see
  `QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25`).

---

## Future-work first-principles derivation target (deferred PATH A)

A retained promotion of the broader Wolfenstein-basis CKM observable
half of this note would require:

1. Retained-grade closure of `CKM_NNI_COEFFICIENTS_NOTE` and
   `CKM_ABSOLUTE_S23_NOTE` (currently `audited_conditional`) — this
   provides the upstream c_12, c_23 inputs as derived rather than
   imported.
2. A retained-grade Wolfenstein-basis suppression theorem
   `c_13^Wolfenstein = c_13^NNI · sqrt(m_1/m_2)` from A_min primitives
   plus EWSB cascade structure — this closes the §2 "Root cause" gap.
3. A retained-grade closure of the Z_3 Berry phase delta_CKM
   derivation (`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25`
   to retained, not currently `audited_conditional`).

These are theorem-level deferred work; the load-bearing class-(A)
algebraic Schur identity that survives PATH B is independent of all
three.

---

## Theorem (c_13 from Schur complement) — load-bearing class-(A) identity

Let M be the 3x3 NNI (nearest-neighbor interaction) mass matrix in the quark
flavor basis:

    M = [[m_1,  c_12*sqrt(m_1*m_2),  0              ],
         [c_12*sqrt(m_1*m_2),  m_2,  c_23*sqrt(m_2*m_3)],
         [0,  c_23*sqrt(m_2*m_3),  m_3              ]]

where the zero in the (1,3) position is the NNI texture constraint: generations
1 and 3 do not interact directly.

**Claim**: The effective 1-3 coupling is generated by the Schur complement when
integrating out the intermediate generation (generation 2):

    c_13^eff = c_12 * c_23

in the NNI geometric-mean normalization (M_ij = c_ij * sqrt(m_i * m_j)).

---

## Proof

The Schur complement of the (2,2) block in the 3x3 matrix M gives the
effective 2x2 matrix for generations 1 and 3:

    M_eff = [[m_1, 0], [0, m_3]] - (1/m_2) * [[a], [b]] * [a, b]

where a = c_12 * sqrt(m_1 * m_2) and b = c_23 * sqrt(m_2 * m_3).

The effective (1,3) element:

    (M_eff)_13 = -a*b / m_2
               = -c_12 * sqrt(m_1 * m_2) * c_23 * sqrt(m_2 * m_3) / m_2
               = -c_12 * c_23 * sqrt(m_1 * m_3)

In the NNI normalization where M_13 = c_13 * sqrt(m_1 * m_3):

    c_13^eff = |M_eff_13| / sqrt(m_1 * m_3) = c_12 * c_23

This is verified numerically to machine precision (fractional error < 0.01%)
in both up and down quark sectors.

---

## Three Key Results (bounded numerical observations under PATH B scope)

The three sections below are explicitly scoped under PATH B as **bounded
numerical observations** comparing the Schur-complement reading against
PDG. They are NOT load-bearing under the narrow-scope load-bearing
identity above; they are downstream comparisons that import upstream
authority chain inputs (NNI coefficients, absolute s_23, Z_3 Berry phase
delta) and document where the broader Wolfenstein-basis CKM observable
prediction overshoots PDG by the documented mass-ratio suppression
factor. The retained-grade promotion of these results requires the
upstream-authority closures listed in the "Future-work" section above.

### 1. Absolute c_23 from the EWSB-dressed mass matrix

The NNI coefficient c_23 is determined by the 1-loop EWSB self-energy at the
geometric mean scale mu = sqrt(m_2 * m_3):

    c_23 = (alpha_s(mu) * C_F / (4pi)) * ln(m_3/m_2) * R_23

where R_23 is the NNI overlap enhancement from the lattice BZ corner structure.

**Current status**: The absolute prediction using R_23 = R_12 (universality
hypothesis) gives |V_cb| = 0.015, which undershoots PDG by ~3x. The actual
R_23 needed is R_23 ~ 8-9, compared to R_12 ~ 2.75 for the 1-2 sector.

**Interpretation**: The 2-3 sector enhancement R_23 > R_12 is physically
expected because the 2-3 BZ corners are separated by a shorter momentum-space
distance on the taste lattice than the 1-2 corners (after EWSB axis selection
breaks S_3 -> Z_2). The ratio R_23/R_12 ~ 3 encodes the second symmetry
breaking step.

When c_23 is matched to V_cb via the EW charge ratio (c_23^u/c_23^d = W_up/W_down),
the matched values c_23^u = 0.672, c_23^d = 0.663 are consistent with the
previously fitted values (0.65).

### 2. Generated c_13 from the Schur complement

The NNI texture has c_13^bare = 0 by construction. The Schur complement
generates the effective 1-3 coupling:

    c_13^eff (up)   = c_12^u * c_23^u = 1.48 * 0.672 = 0.995
    c_13^eff (down) = c_12^d * c_23^d = 0.91 * 0.663 = 0.603

**Current status**: Using c_13 = c_12 * c_23 directly gives |V_ub| = 0.023,
which overshoots PDG (0.0038) by ~6x.

**Root cause**: The NNI c_12 coefficients are O(1) because they include the
geometric-mean normalization factor. In the Wolfenstein basis, the physical
c_13 involves an additional suppression by sqrt(m_1/m_2):

    c_13^wolf = c_13^NNI * sqrt(m_1/m_2)

For the up sector: c_13^wolf = 0.995 * sqrt(m_u/m_c) = 0.995 * 0.041 = 0.041
For the down sector: c_13^wolf = 0.603 * sqrt(m_d/m_s) = 0.603 * 0.224 = 0.135

This mass-ratio suppression is the physical mechanism that converts the
O(1) NNI Schur complement into the observed O(lambda^3) Wolfenstein hierarchy.

**Structural claim**: The Wolfenstein hierarchy

    |V_us| ~ lambda,  |V_cb| ~ A*lambda^2,  |V_ub| ~ A*lambda^3

is the Schur complement cascade applied to the NNI texture. Each power of
lambda arises from integrating out one generation.

### 3. Jarlskog invariant from EWSB-dressed invariants

With c_13 generated by the Schur complement and delta from the Z_3 Berry
phase, the Jarlskog invariant is fully determined:

    J = 1.45e-4  (PDG: 3.08e-5, ratio 4.7)

The overshoot tracks the c_13 overshoot: J is proportional to V_ub and
therefore to c_13. The mass-ratio correction factor would bring J into the
correct range.

---

## Open Gaps (Honest Assessment)

1. **Absolute c_23**: R_23 = R_12 universality undershoots by ~3x. Need to
   compute R_23 independently from the lattice BZ corner geometry.

2. **c_13 magnitude**: Schur complement gives the correct STRUCTURE
   (c_13 = c_12 * c_23) but overshoots by ~6x in magnitude. The mass-ratio
   suppression sqrt(m_1/m_2) must be incorporated into the effective
   Wolfenstein-basis formula.

3. **CKM phase**: delta_CKM = 29 deg vs PDG 65 deg. The Z_3 Berry phase
   source is correct but the projection through the mass hierarchy needs
   refinement.

---

## Relation to Prior Work

- The Schur complement identity c_13 = c_12 * c_23 is the NNI-texture version
  of the Branco-Lavoura-Silva (1999) result for texture zeros.
- The absolute c_23 program extends the five attacks of `CKM_ABSOLUTE_S23_NOTE`
  with the self-energy approach at geometric-mean scale.
- The cascade structure (lambda -> A*lambda^2 -> A*lambda^3 from sequential
  Schur complements) confirms the Wolfenstein = EWSB cascade theorem of
  `CKM_WOLFENSTEIN_CASCADE_THEOREM`.

---

## Numerical Verification (bounded numerical observation table)

The table below records the bounded numerical observation comparing the
PATH B downstream reading against PDG. Under the PATH B narrow scope,
this table is **not** load-bearing on the algebraic Schur identity
(which is independent of any PDG comparison); it documents the gap that
Wolfenstein-basis suppression and upstream NNI-coefficient closure
would need to close, and shows that the magnitude failures are concentrated
in the bounded comparison rather than in the algebraic Schur identity
itself.

| Observable | Schur complement | PDG | Ratio |
|-----------|-----------------|-----|-------|
| |V_us| | 0.328 | 0.224 | 1.46 |
| |V_cb| | 0.041 | 0.042 | 0.98 |
| |V_ub| | 0.023 | 0.0038 | 6.1 |
| J | 1.45e-4 | 3.08e-5 | 4.7 |
| delta | 29 deg | 65 deg | 0.45 |

All exact checks pass (c_13 = c_12*c_23 identity verified to machine precision).
Bounded checks on V_ub and J overshoot by the expected mass-ratio factor.
