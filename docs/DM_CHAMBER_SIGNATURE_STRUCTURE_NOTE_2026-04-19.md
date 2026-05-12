# DM Chamber Signature Structure -- F4 Closed by DPLE Theorem

**Date:** 2026-04-19
**Status:** support - structural or confirmatory support note
**Primary runner:** scripts/frontier_dm_dple_theorem.py
signature-structure analysis of the DM A-BCC chart, introducing F4
(interior-minimum linear-path Sylvester discriminant) as the basin-
selector axiom candidate. this cycle reduces F4 to a **theorem**: the
d = 3 specialization of the dim-parametric **log|det| extremum
principle (DPLE)** on the retained linear Hermitian pencil. F4 is no
longer an independent axiom.

**Primary reference:**
`docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`.

---

## 1. What changed between this cycle-4 and this cycle

### this cycle-4 state

Cycles 7B and 8 identified F4 as the discriminating axiom candidate on
the DM A-BCC chart:

> F4: on the linear pencil `p(t) = det(H_base + t * J_src)`, require an
> interior critical point t* in (0, 1) with p(t*) > 0. Equivalently
> A_2^2 - 3 A_1 A_3 > 0 on cubic coefficients.

Basin-discrimination values:

- Basin 1: Delta_ret = +7.80 (INTERIOR CP in (0,1)) -> F4 TRUE.
- Basin N: Delta_ret = -10.14 -> F4 FALSE (no real critical point).
- Basin P: Delta_ret > 0 but roots OUTSIDE (0,1) -> F4 FALSE.
- Basin X: Delta_ret < 0 -> F4 FALSE.

Composite selector `F1 AND F2 AND F3 AND F4` uniquely picks Basin 1 in
560-seed chamber scans.

F4 is retained-adjacent (algebraic, reinforcing the retained P3
Sylvester linear-path theorem on main), but its physical justification
-- variational / Wilson / slot-freeze derivation -- was the **1-axiom
gap**.

### this cycle state (this update)

F4 reduces to a **theorem** via the dim-parametric **DPLE principle**.
The principle, stated at arbitrary d >= 2:

> Let H(t) = H_0 + t H_1 be a linear Hermitian pencil on Herm(d; C)
> with H_0 invertible.  The observable W(t) = log|det H(t)| has at most
> floor(d/2) interior Morse-index-0 critical points on any open
> interval.

At d = 3 this upper bound is **exactly 1**, giving a clean binary
selector F_3 equivalent to F4 (cycle 7B). Algebraically:

    F_3  :=  Delta_ret = c_2^2 - 3 c_1 c_3 > 0
             AND smaller real root of p'(t) in (0, 1)
             AND p(t*) > 0
             AND sign(p(t*)) = sign(c_0).

Verification on DM A-BCC basins (probe T3): F_3 agrees with retained F4
on all four basins. Basin 1 is uniquely selected.

DPLE's requirements:

- Jacobi's formula (standard).
- Sylvester signature and its algebraic structure (standard).
- Morse-idx-0 characterization of local minima (standard).
- Retained H_base and J_* (retained on main).
- Retained linear-path parameter t in (0, 1) via the retained P3
  Sylvester linear-path signature theorem (on main).

**None of these are new axioms.** DPLE is a mechanically verifiable
algebraic theorem; F4 is its d = 3 specialization on the retained
pencil.

**Scope.** DPLE closes conditions (1)-(3) of F_3 (structure of the
unique interior minimum at d=3). Condition (4) -- sign(p(t_*)) =
sign(det H_base) > 0 -- encodes A-BCC (physical sheet = C_base) and is
not derived from DPLE. A-BCC remains an open source-side input; see
`DM_DPLE_ABCC_NO_GO_NOTE_2026-04-19.md`.

### Dim-uniqueness

- d = 2: F_2 is vacuous (no cubic discriminant branch).
- **d = 3**: F_3 is a clean binary selector (at most 1 interior
  Morse-idx-0 CP).
- d >= 4: F_d fragments (probe T4 constructs an explicit d = 4
  Hermitian pair with 2 interior Morse-idx-0 CPs in (0, 1) by random
  search).

Combined with retained R1 / R2 / R3 on main, d = 3 is the unique dim at
which the DM A-BCC lane has a physical carrier with a clean binary F_d
selector -- the same dim-uniqueness fingerprint as MRU (this cycle) and
Berry (this cycle).

---

## 2. Current axiom status

F4 is **not an axiom anymore**. The content (interior-min-in-(0,1) with
positive signature) is now a corollary of DPLE + retained d = 3 +
retained linear-path theorem.

The chamber signature structure analysis (cycle 7B / 8) survives as the
concrete numerical verification that DPLE_{d=3} reproduces F4 exactly on
the four DM A-BCC basins.

---

## 3. Runner status

The old runners `scripts/frontier_dm_chamber_signature_structure.py`
and `scripts/frontier_dm_f4_discriminator_axiom_candidate.py` are NOT
included in this branch (superseded). Their functional content is
absorbed into the DPLE theorem runner
`scripts/frontier_dm_dple_theorem.py` (PASS=19 FAIL=0).

The DPLE runner (`frontier_dm_dple_theorem.py`) is now PASS=22 FAIL=0
(T1-T7 original checks plus T8 sign-blindness / A-BCC gap check).

Retained DM runners on main pass unchanged:

- `frontier_sigma_hier_uniqueness_theorem.py`: PASS=24 FAIL=0
- `frontier_dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_2026_04_18.py`: PASS=11 FAIL=0
- `frontier_abcc_cp_phase_no_go_theorem.py`: PASS=20 FAIL=0
- `frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py`: PASS=26 FAIL=0

---

## 4. Cross-references

- `docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md` (this cycle, primary)
- `docs/DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md` (retained path theorem, on main)
- `docs/CYCLE_1_TO_10_SYNTHESIS_NOTE_2026-04-19.md` (reading order)
- Uhlig 1982 (Linear Algebra Appl. 46); Mehl-Mehrmann-Ran-Rodman 2016; Milnor Morse Theory 1963.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_dple_dimension_parametric_extremum_theorem_note_2026-04-19](DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md)
- [dm_neutrino_source_surface_p3_sylvester_linear_path_signature_theorem_note_2026-04-18](DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md)
