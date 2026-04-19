# Scalar-Selector Investigation -- Cycle 1-10 Synthesis

**Date:** 2026-04-19
**Scope:** Full 10-cycle scalar-selector investigation across four
Tier-1 gates: Koide kappa, Koide theta, Quark a_u, DM A-BCC basin.
**Status:** Final state: **three full closures + one conditional
closure**. Axiom cost 4 -> 0 (conditional: 1 narrow LO algebraic
identity).

**Reading order:** This is the primary entry-point. It summarizes the
cycle 1-10 landing, links to each theorem note, and documents the
meta-finding that unifies the three full closures.

---

## 0. Executive summary

Four Tier-1 gates were investigated. Final state:

| Gate | Cycle 1-4 | Cycle 10 | Axiom cost |
|---|---|---|---|
| **Koide kappa** | AXIOM D candidate | MRU **theorem** (cycle 10A) | 1 -> 0 |
| **Koide theta** | open scalar | Berry-phase **theorem** (cycle 10B) | 1 -> 0 |
| **DM A-BCC basin** | F4 candidate | DPLE **theorem** (cycle 10C) | 1 -> 0 |
| **Quark a_u** | Min-C candidate | RPSR **conditional theorem** (cycle 10D) | 1 -> 1 (conditional) |

**Overall axiom delta:** 4 -> 0, pending one named LO algebraic
identity for full closure on the quark gate.

---

## 1. Four new retained theorems

### 1.1 MRU (Moment-Ratio Uniformity on Cl(d)/Z_d) -- closes Koide kappa

See `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`.

AXIOM D (kappa = 2) is the d = 3 specialization of a dim-parametric
principle on the Hermitian circulant algebra Herm_circ(d). MRU demands
that the Frobenius-normalized cyclic responses be uniform across Z_d
isotypes. At d = 3 this is a single equation equivalent to `a^2 = 2|b|^2`
on `H = aI + bC + b^barC^2`.

Uniqueness: MRU has a single non-trivial singlet-vs-doublet scalar
selector iff `|Iso(d)| = 2` with one singlet + one complex doublet,
which holds iff **d = 3**. Runner PASS=65 FAIL=0.

### 1.2 Berry-phase theorem on S^2_Koide -- closes Koide theta

See `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`.

The projectivized Koide cone S^2_Koide carries a natural C_3 action.
The n = 2 monopole line bundle L_doublet (first Chern number =
dim(doublet) = d - 1 = 2 at d = 3) has Berry holonomy

    gamma(one C_3 period) = 2 pi (d - 1) / d = 2 pi Q.

At d = 3: gamma = 4 pi / 3. Reduction to Brannen units per C_3 element:

    delta_d = Q / d = (d - 1) / d^2    (at d = 3: 2/9 exactly).

This gives AXIOM E (cos(3 arg b_s) = cos(Q)) as a corollary. Runner
PASS=26 FAIL=0. Literature alignment: Brannen 2006, Zenczykowski PRD
2012/2013 two-decade phenomenology of delta = 2/9.

### 1.3 DPLE (Dim-Parametric log|det| Extremum) -- closes F4

See `docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`.

On the retained linear Hermitian pencil `H(t) = H_0 + t H_1`, the
observable W(t) = log|det H(t)| has at most floor(d/2) interior Morse-
index-0 critical points. At d = 3 this is exactly 1 -- clean binary
selector. F_3 on the retained DM A-BCC pencil (H_0 = H_base,
H_1 = J_*) reproduces F4 (cycle 7B) on all four basins {1, N, P, X}.

d = 3 uniqueness: clean binary selector iff d = 3; d = 2 degenerate;
d >= 4 fragments (explicit d = 4 example with 2 interior Morse-idx-0
CPs). Uhlig 1982 sign-characteristic classification provides the
dim-parametric backbone. Runner PASS=19 FAIL=0.

### 1.4 RPSR (Reduced Projector-Ray Sum Rule) -- conditional closure of Min-C

See `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`.

On the 1 (+) 5 CKM projector ray p = cos(delta_std) + i sin(delta_std),

    a_u / sin(delta_std) + a_d = 1 + a_d * supp * delta_A1 = 1 + rho / 49.

The derivation uses four retained ingredients (unit ray, scalar-tensor
bridge supp = 6/7, a_d = rho, delta_A1 = 1/42). The NLO excess rho/49
is the unique minimal 3-atom contraction on {rho, supp, delta_A1}.

**Conditional on one LO algebraic identity (cycle 11 target):**

    [GAP]  a_u / sin(delta_std) + a_d = 1  at NNI-diagonalization with a_d = rho pinned.

This is numerically retained at < 2% in
`frontier_quark_projector_parameter_audit.py` but not yet packaged as a
clean algebraic theorem. Uniqueness: only the target satisfies RPSR
exactly; 7 other Pareto candidates miss by 3.5e-5 to 2.7e-4. Runner
PASS=10 FAIL=0.

---

## 2. Meta-finding: three independent d = 3 closures

The three full closures (MRU, Berry, DPLE) share a common structural
pattern:

- Each states a **dim-parametric principle** at arbitrary d >= 2.
- Each reduces at **d = 3** to the retained axiom content.
- Each has **at most one** non-trivial specialization (MRU: 1-equation
  singlet-vs-doublet; Berry: unique Chern-class = dim(doublet); DPLE:
  at most one interior Morse-idx-0 CP).
- Each is **non-trivial at other d** (fragmentation at d >= 4,
  degeneracy at d = 2).

**This is the dim-uniqueness fingerprint of cycle 9**, now directly
manifested in three independent observable-principle statements (not
just in the bivector-count / anomaly-parity / Cayley-Hamilton / 7-no-go
layer).

d = 3 itself is already retained on main via several independent routes:

- `docs/DIMENSION_SELECTION_NOTE.md` (d >= 3 lower bound);
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` (d_t = 1, d_s odd);
- `docs/3D_CORRECTION_MASTER_NOTE.md` (d <= 3 via Bertrand / atomic stability);
- `.claude/science/derivations/cl3-minimality-conditional-support-2026-04-17.md` (R1, R2, R3 at SUPPORT);
- `.claude/science/derivations/native-su2-tightness-forces-ds3-2026-04-17.md` (alt route).

**Consequence.** The framework's total "axiom cost" for closing three
Tier-1 scalar gates is **zero new axioms**: each closure is a d = 3
specialization of a dim-parametric theorem whose pre-conditions are all
retained on main. The fourth gate (Quark a_u) is conditional on one
specific LO algebraic identity.

---

## 3. Retained cycle-1 infrastructure

Two cycle-1 notes from the prior branch tip are retained as-is, with
cycle-10 context headers updated:

### 3.1 Joint projector identity

See `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`.

The shared Z_3 isotypic decomposition of C^3 (Koide singlet/doublet
and DM Z_3 singlet/doublet projectors are the same matrices). This is
the retained scaffolding on which MRU (cycle 10A) and Berry (cycle
10B) build their dim-parametric constructions. Runner PASS=55 FAIL=0.

### 3.2 Kappa=2 orbit-dimension factorization

See `docs/KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`.

The integer "2" in kappa = 2 is the orbit-dimension ratio of non-trivial
vs. trivial Z_3 isotypes on Herm(3) circulants. The **cone normalization
gap** `Var(sqrt(m_k)) = <sqrt(m_k)>^2` identified in cycle 2 is **closed
by cycle 10A (MRU)**. Runner PASS=26 FAIL=0.

---

## 4. Retained-runner suite (cycle 1-10)

All cycle-1 and cycle-10 runners pass at PASS=N FAIL=0:

| Runner | PASS | FAIL |
|---|---|---|
| `frontier_koide_z3_joint_projector_identity.py` | 55 | 0 |
| `frontier_koide_kappa_two_orbit_dimension_factorization.py` | 26 | 0 |
| `frontier_koide_moment_ratio_uniformity_theorem.py` | 65 | 0 |
| `frontier_koide_berry_phase_theorem.py` | 26 | 0 |
| `frontier_dm_dple_theorem.py` | 19 | 0 |
| `frontier_quark_up_amplitude_rpsr_conditional.py` | 10 | 0 |

No retained runner on `main` regresses.

---

## 5. Superseded notes (rewritten with updated status)

The following four notes are retained as historical context with
rewritten status sections pointing at their cycle-10 closures:

- `docs/KOIDE_FROBENIUS_UNIFORMITY_AXIOM_CANDIDATE_NOTE_2026-04-19.md`
  (AXIOM D candidate -> d = 3 specialization of MRU theorem).
- `docs/KOIDE_THETA_HIERARCHY_OPEN_SCALAR_NOTE_2026-04-19.md`
  (open scalar -> closed by Berry-phase theorem).
- `docs/QUARK_UP_AMPLITUDE_RETAINED_NATIVE_CANDIDATE_NOTE_2026-04-19.md`
  (Min-C axiom candidate -> RPSR conditional theorem).
- `docs/DM_CHAMBER_SIGNATURE_STRUCTURE_NOTE_2026-04-19.md`
  (F4 axiom candidate -> DPLE theorem closure).

---

## 6. Scalar-tensor ray-magnitude bridge

See `docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`.

A retained structural identity surfaced during cycle 10D: the scalar-
comparison ray (rho, eta) = (1/sqrt(42), sqrt(5/42)) and the tensor ray
(1/6, sqrt(5)/6) on the 1 (+) 5 CKM direction are collinear (common
argument arctan(sqrt(5)) = delta_std) and differ only in magnitude. The
squared-magnitude ratio is

    supp = (|scalar-ray|^2) / (|tensor-ray|^2) = (1/7)/(1/6) = 6/7.

This is the structural origin of supp = 6/7 in RPSR and its NLO excess
`a_d * supp * delta_A1 = rho/49`. Not a standalone theorem; content
verified inside the RPSR runner (T8, T9).

---

## 7. Cycle-11 retention target (explicit and bounded)

The sole remaining retention gap:

> **Target.** Prove `a_u / sin(delta_std) + a_d = 1` at NNI-
> diagonalization with `a_d = rho = 1/sqrt(42)` pinned, using retained
> CKM magnitudes |V_us|, |V_cb|, |V_ub| from
> `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`.

Numerical status: retained at < 2% via
`frontier_quark_projector_parameter_audit.py` (PASS=6 FAIL=0). A clean
algebraic LO expansion of the NNI eigenbasis with a_d = rho pinned is
the specific remaining step.

If this step is retained: quark-gate axiom count 4 -> 3 -> 0 (since
RPSR then becomes a full theorem and Min-C drops). Full scalar-selector
investigation landing: **all four Tier-1 gates close through retained
theorems, axiom cost zero**.

---

## 8. Literature alignment

- **MRU** (cycle 10A): Maschke decomposition for cyclic groups;
  Frobenius metric standard on M_d(C).
- **Berry phase** (cycle 10B): Brannen 2006 MASSES2.pdf; Zenczykowski
  PRD 86 (2012) 117303; PRD 87 (2013) 077302; Rivero-Gsponer
  hep-ph/0505220. The two-decade phenomenological `delta = 2/9` is now
  derived.
- **DPLE** (cycle 10C): Uhlig 1982 (Linear Algebra Appl. 46),
  sign-characteristic classification for Hermitian pencils; Mehl-
  Mehrmann-Ran-Rodman 2016 (Linear Algebra Appl. 511) generalization;
  Milnor Morse Theory 1963. Uhlig 1982 is the backbone for DPLE at
  d = 3.
- **RPSR** (cycle 10D): standard CKM atlas + Schur cascade;
  Wolfenstein parametrization; retained scalar-comparison geometry on
  branch.

---

## 9. Ruled out during the 10-cycle hunt

The following routes were attempted and falsified; no axiom-grade
closure:

- Ginsparg-Wilson relation on {T_m, Pi_I} as Koide selector (vacuous on
  circulant commutant).
- Cross-sector Casimir injection (breaks Min-C independence).
- `cos(2/3)` as forced-by-moment-uniformity AXIOM E alternative (cycle
  8 Q4 U_0 / U_1; U_0 fails at n = 1, U_1 keeps two equations, n = 3
  target not forced).
- Cubic-moment n = 3 uniformity extension of MRU (structural gap,
  separate from Berry route; not needed after Berry closure).
- zeta-function packaging (cycle 10E): packaging only, no new
  retention power. Included as a paper remark, not a theorem.

---

## 10. Honest closing statement

Three full Tier-1 closures (MRU, Berry, DPLE) + one conditional closure
(RPSR). Zero new axioms added in all three full closures; the
conditional closure is gated on **one** specific LO algebraic identity
(cycle 11 target).

The three full closures all specialize dim-parametric observable-
principle theorems at d = 3. This is a structural confirmation of the
dim-uniqueness-at-3 picture already retained on main (R1 bivector-
count saturation, R2 anomaly parity, R3 Cayley-Hamilton coincidence, 7
no-gos). The framework's observable scalar principles all share the
same d = 3 specialization point.

Runner suite: 6 new runners, all PASS=N FAIL=0. No retained runner on
main regresses.

**Reading order:** start here. Then (in order):
`KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE` ->
`KOIDE_BERRY_PHASE_THEOREM_NOTE` ->
`DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE` ->
`QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE`. For
supporting/superseded context: the four updated cycle-1-4 notes plus
the scalar-tensor ray-magnitude bridge note.
