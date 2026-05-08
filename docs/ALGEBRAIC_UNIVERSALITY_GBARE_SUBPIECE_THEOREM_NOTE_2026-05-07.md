# Algebraic Universality on A_min — `g_bare = 1` Constraint Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the seventh sub-piece of the
algebraic-universality program (PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)).
This note proves that the constraint reading `g_bare = 1` derived in
PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667)
is invariant under realization choice **within a narrower class than the
sub-pieces 1–6**: namely, within the class of canonical-Killing-form-
normalized Wilson-style plaquette actions. Outside that class
(e.g. Symanzik-improved actions, non-Wilson lattice gauge formulations)
the bare-coupling-vs-β algebra changes form. The honest scope is
therefore narrower than the pure-algebraic predictions in the earlier
sub-pieces, and this note surfaces both the (CKN) and Wilson-action
choices as explicit admissions.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_gbare_subpiece.py`

## 0. Question

PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
distinguished two prediction classes within A_min's surface:

- **Algebraic class** — proofs use only A_min's representation-theoretic
  content (multiplicities, group structure, anomaly arithmetic). These
  are lattice-realization-invariant by direct proof structure, exact at
  every lattice scale, and listed as predictions 1–6 of the framing
  note (SM hypercharges, Tr[Y²] = 40/3, Y_GUT = √(3/5)·Y_min,
  sin²θ_W^GUT = 3/8, 5̄ ⊕ 10 ⊕ 1 SU(5) decomposition, 3+1 spacetime).
- **Continuum-limit class** — numerical values realization-dependent at
  finite `a`, Wilson-universality-class invariants in the asymptotic
  sense (`<P>`, `u_0`, α_LM, mass eigenvalues).

PR #670's §1 listed `g_bare = 1` (the constraint reading from PR #667)
as an item in the algebraic class, but flagged the (CKN) admission. The
question this note addresses is:

```text
Is `g_bare = 1` truly algebraically universal in the same sense as
SM hypercharges (provable using only A_min's representation-theoretic
content), or does the proof depend on a specific class of lattice
actions that narrows the universality scope?
```

## Answer

**`g_bare = 1` is universal across realization choice within a narrower
class than sub-pieces 1–6.** The proof of PR #667 relies on the Wilson
plaquette small-a matching `β = 2 N_c / g_bare²` as a load-bearing
input. That matching is intrinsic to the Wilson plaquette action class
and to the canonical Killing-form normalization (CKN). Within that
class the constraint `g_bare² = 1` follows by exact rational algebra
at N_c = 3. Outside the class (Symanzik-improved actions add higher-
order terms with different β–g_bare algebra; non-Wilson formulations
may not match β to g_bare² at all), the same algebra does not apply.

The honest scope is therefore:

> **Theorem (g_bare Algebraic Universality, narrower scope).**
> Within the class of canonical-Killing-form-normalized
> Wilson-style plaquette actions on Z³ realizing A_min's retained
> surface, the constraint `g_bare = 1` is invariant under realization
> choice. Realization choice within this class does not affect the
> algebra: any A_min-compatible realization that uses (i) (CKN)
> generator normalization and (ii) the Wilson plaquette action form
> produces `β = 2 N_c / g_bare²`, and at N_c = 3 algebra forces
> `g_bare² = 1`.

This is **strictly narrower** than the algebraic universality of
sub-pieces 1–6, which depends on no action-form choice. The (CKN) and
Wilson-action admissions are both surfaced explicitly.

## 1. Scope position

| Sub-piece | Scope of universality | Action-form dependent? |
|---|---|---|
| 1 — SM hypercharges | A_min retained surface (chiral content + anomaly arithmetic) | NO |
| 2 — Tr[Y²] = 40/3 | A_min retained surface | NO |
| 3 — Y_GUT = √(3/5)·Y_min | A_min retained surface + (SU(5) Killing form admission) | NO |
| 4 — sin²θ_W^GUT = 3/8 | A_min retained surface + (SU(5) Killing form) | NO |
| 5 — 5̄ ⊕ 10 ⊕ 1 SU(5) decomposition | A_min retained surface + (SU(5) Killing form) | NO |
| 6 — 3+1 spacetime / anomaly cancellation | A_min retained surface | NO |
| **7 — `g_bare = 1` (this note)** | **A_min retained surface + (CKN) + Wilson plaquette form** | **YES — Wilson plaquette action class only** |

Sub-pieces 1–6 are *pure-algebraic* universality: their proofs cite no
action-form. This sub-piece is *Wilson-action-class universality*: the
proof cites (CKN) plus the Wilson plaquette form, both as explicit
admissions. The narrower scope is honest and reflects the actual proof
structure of PR #667.

## 2. Definition: lattice-realization-invariance within the Wilson-action class

A framework prediction `P` is **lattice-realization-invariant within
the Wilson-action class** iff the proof of `P` cites:

- (a) only A_min's representation-theoretic content (multiplicities,
  group structure, anomaly arithmetic), AND
- (b) only the canonical Killing-form normalization (CKN) and the
  Wilson plaquette action form as action-form inputs.

It need not cite specific lattice-machinery quantities (specific β
values from MC, staggered-phase choices, BZ-corner labels, link
unitaries, lattice scale `a` as a load-bearing parameter, PDG values,
fitted matching coefficients).

Equivalently: any A_min-compatible realization that uses (CKN) and the
Wilson plaquette form produces the same `P` by direct proof
substitution.

This is **strictly narrower** than the §2 definition in PR #670 (pure
algebraic universality) because it admits (CKN) + the Wilson plaquette
form as load-bearing inputs.

## 3. Theorem (g_bare = 1 Wilson-class universality)

**Bounded theorem.** Under {A_min + retained-tier surface (per PR #667
premises CPS, GFSU3, WM, RFR, CVC, RIG, NCV) + the explicit (CKN)
admission + the Wilson plaquette action form admission}, the constraint

```text
g_bare² = 1     (so g_bare = +1 by positivity convention)
β       = 6     (at N_c = 3)
```

is invariant under realization choice within the canonical-Killing-
form-normalized Wilson-style plaquette action class. The proof of
[`G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md`](G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md)
(PR #667) walks chain (G1)–(G6) using only:

| Input class | Examples | Action-form dependent? |
|---|---|---|
| Group-theoretic constants | N_c = 3, T(fund) = 1/2 | NO |
| (CKN) admission | Tr(T_a T_b) = δ_ab/2 | NO (math convention) |
| Wilson plaquette small-a matching | β = 2 N_c / g_bare² | YES — Wilson plaquette only |
| Rescaling-freedom-removal at (CKN) | A → c·A shifts β = c²·β | NO (algebra given (CKN)) |
| Constraint-vs-convention algebra | g_bare² = 2 N_c / β at canonical β | NO (algebra) |
| Rational arithmetic | g_bare² = 6/6 = 1 | NO |

The Wilson plaquette small-a matching (WM) is the load-bearing
action-form choice: it is what ties β to g_bare² as `β = 2 N_c /
g_bare²`. At Symanzik-improved actions (e.g. one-loop tadpole-improved,
or with `c_1 P + c_2 R` rectangular corrections), the β–g_bare relation
acquires correction terms; the bare-coupling identity `β = 2 N_c` no
longer aligns with `g_bare² = 1` directly. Hence the universality
statement here is genuinely class-restricted.

## 4. Proof-walk verification

Walking [`G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md`](G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md)
chain (G1)–(G6) step by step:

| Step | Content | Inputs used | Lattice-machinery beyond (CKN) + Wilson form? |
|---|---|---|---|
| (G1) | A1 + CPS → Cl(3) per-site has dim-2 chirality summands; canonical Pauli generators σ_a satisfy `Tr(σ_a σ_b) = 2·δ_ab` | A1, CPS (Cl(3) per-site uniqueness) | NO — pure Pauli-algebra identity |
| (G2) | A1+A2 + GFSU3 → graph-first SU(3) is the semisimple part of the gl(3) ⊕ gl(1) commutant on the taste cube | A1, A2, GFSU3 | NO — graph-first commutant structure (action-form independent) |
| (G3) | (CKN): T_a in the fundamental satisfy `Tr(T_a T_b) = δ_ab/2` | (CKN) admission | (CKN) admission only — not lattice machinery |
| (G4) | WM: the Wilson plaquette small-a matching forces `β = 2 N_c / g_bare²` at the canonical generator basis | Wilson plaquette form, (CKN) | **YES — Wilson plaquette form is load-bearing** |
| (G5) | RFR + CVC: under (CKN) + (WM), `g_bare² = 1` algebraically follows from `β = 2 N_c = 6` | (CKN), (WM), RFR, CVC, rational arithmetic | NO beyond (G4) — algebraic |
| (G6) | At N_c = 3, β = 2·3 = 6 and g_bare² = 6/6 = 1 | rational arithmetic | NO — pure rational algebra |

**Conclusion.** Steps (G1), (G2), (G3), (G5), (G6) use only (CKN) +
algebraic content + retained surface. Step (G4) uses the Wilson
plaquette action form as an explicit, load-bearing input. The chain
produces the unique constraint `g_bare² = 1` at N_c = 3 within the
Wilson-plaquette + (CKN) class. ∎

## 5. Concrete realization-invariance test (within the Wilson-class)

Construct three hypothetical alternative A_min-compatible realizations
*within the Wilson-action class* (same Wilson plaquette form, same
(CKN) generator normalization, possibly different fermion realization
or graph orientation):

1. **Realization R_KS-Wilson** (canonical Kogut-Susskind staggered-Dirac
   + Wilson plaquette gauge action, A3-forced + (CKN)).
2. **Realization R_alt-A-Wilson** (hypothetical: same Wilson plaquette
   gauge action + (CKN), different fermion content packaging that still
   produces SU(3) color triplet at the canonical generator basis).
3. **Realization R_alt-B-Wilson** (hypothetical: any other
   A_min-compatible realization with same Wilson plaquette form +
   (CKN)).

For each, the Wilson small-a matching evaluates identically:

```text
β = 2 N_c / g_bare²
  = 2·3 / g_bare²  (at N_c = 3, canonical β = 6 from action input)
  ⇒ g_bare² = 1  (unique solution within the Wilson-class)
```

The N_c = 3 input is structural (graph-first SU(3) commutant on the
taste cube). The (CKN) admission is shared across all three. The
Wilson plaquette form is shared by construction. The matching identity
β = 2 N_c / g_bare² has no realization-dependent terms: it is the
small-a expansion of `β · Σ_p (1 − Re Tr U_p / N_c)` at canonical
(CKN) generators, and the small-a expansion gives the same
coefficient regardless of which specific Wilson realization is chosen.

Hence within the Wilson-action class the constraint is
realization-invariant. The narrower scope is honest because **outside
the class**, the matching identity itself changes form.

## 6. Out-of-class counterexamples (explicit, sanity check)

To make the narrower scope concrete, here are realizations that
**violate** the Wilson-action class assumption and where the algebra
changes form:

| Realization | What changes | Effect on g_bare = 1 algebra |
|---|---|---|
| Symanzik-improved Wilson (`c_1 P + c_2 R`) | Plaquette + rectangle terms with improvement coefficients | β–g_bare relation acquires `c_1`, `c_2`-dependent corrections; canonical β = 2 N_c does not directly force g_bare² = 1 |
| Tadpole-improved Wilson (`β/u_0⁴`) | Mean-field improvement multiplies β by `1/u_0⁴` | g_bare² = 2 N_c · u_0⁴ / β at canonical generator basis |
| Non-Wilson lattice gauge action (e.g. heat-kernel) | Different action functional entirely | β–g_bare matching identity may not exist in the same form |
| Generator-rescaled basis (T_a → c·T_a) | Violates (CKN) | β shifts to c²·β with g_bare unchanged (RFR theorem); realization is outside the class |

These counterexamples are not real obstructions to the framework —
they are out-of-class realizations that the framework does not commit
to. They are listed here only to make the narrower scope of the
universality claim explicit and honest. The framework's choice is the
canonical Wilson plaquette action + (CKN); within that choice the
constraint `g_bare = 1` is invariant under realization variation.

## 7. What this sub-piece does NOT close

- **Wilson plaquette action form uniqueness.** That `β · Σ_p (1 − Re
  Tr U_p / N_c)` is the canonical action form is itself an open
  derivation target, not closed by this note. The Wilson form is
  admitted as part of the class definition.
- **(CKN) derivation from raw A_min.** Whether `Tr(T_a T_b) = δ_ab/2`
  is uniquely forced by A1+A2 alone is a separate meta-question. (CKN)
  is admitted here as standard SU(N) representation theory, the same
  way PR #655 admits the SU(5) Killing form and PR #664 admits (LCL).
- **Pure algebraic universality.** This sub-piece is *narrower* than
  sub-pieces 1–6: those proofs cite no action-form input. The honest
  classification is: this sub-piece is in a "Wilson-class subset" of
  the algebraic-universality framing, not in the pure-algebraic
  subset.
- **Continuum-limit class predictions.** Numerical values of α_LM,
  m_H_tree/v at finite a, mass eigenvalues, etc., remain in the
  continuum-limit class with Wilson-universality scope. This sub-piece
  does not extend to those.
- **Audit ratification of PR #667.** The constraint-vs-convention
  theorem (CVC) and rescaling-freedom-removal (RFR) inputs to PR #667
  are at audited_conditional. Their retention drives the eventual
  retention of `G_BARE_DERIVATION_NOTE.md`. This note inherits PR
  #667's audit chain; it does not unilaterally promote any cited
  authority.

## 8. What this sub-piece DOES close

- **Conceptual scoping.** PR #670's framing-note §1 listed `g_bare = 1`
  in the algebraic class but flagged "(modulo CKN admission)." This
  note formalizes the scope: the universality is *within the Wilson-
  action class*, not pure algebraic. Both (CKN) and the Wilson
  plaquette form are surfaced as explicit admissions.
- **Proof-walk of PR #667's chain (G1)–(G6).** Each step is examined
  for action-form dependencies; only step (G4) is found to be
  load-bearing on the Wilson form; all other steps are algebraic given
  (CKN).
- **Realization-invariance within the class.** Three hypothetical
  in-class realizations all give the same constraint `g_bare² = 1`.
- **Out-of-class explicitness.** Counterexamples (Symanzik-improved
  Wilson, tadpole-improved Wilson, non-Wilson actions, generator
  rescaling) are listed with the algebra change they induce, making
  the narrower scope concrete.

## 9. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is a sub-piece of the algebraic-universality program (PR #670).
  It packages the seventh listed follow-on item: g_bare = 1 constraint
  reading. The honest scope is narrower than sub-pieces 1-6 (which are
  pure-algebraic): this sub-piece is universal within the
  canonical-Killing-form-normalized Wilson-style plaquette action
  class, with (CKN) and Wilson form both surfaced as explicit
  admissions. Eligible for retention upgrade once: (a) PR #667's
  CVC + RFR + WM chain is independently audited and retained, (b)
  this note is independently audited, (c) the (CKN) admission is
  ratified as legitimate math-convention layer (analogous to the
  SU(5) Killing form in cycle 16/19, the (LCL) labelling in PR #664).
audit_required_before_effective_retained: true
bare_retained_allowed: false
parent_update_allowed_only_after_retained: true
```

The parent `G_BARE_DERIVATION_NOTE.md` is **not** to be updated from
this note alone. This sub-piece sits one level above PR #667's
bootstrap proof and uses it as a black box. Promotion of the parent
remains an audit-lane decision contingent on retention of CVC + RFR +
PR #667's chain.

## 10. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_gbare_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: g_bare = 1 constraint reading is lattice-realization-
invariant WITHIN the canonical-Killing-form-normalized Wilson-style
plaquette action class. Proof of PR #667's bootstrap chain
(G1)-(G6) uses (CKN) + Wilson plaquette form as explicit,
load-bearing admissions in step (G4); all other steps are algebraic
given (CKN). The narrower scope is honest: this sub-piece is
Wilson-action-class universality, NOT pure-algebraic universality.
At N_c = 3, exact rational algebra forces g_bare^2 = 1 and beta = 6.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (framing, narrower-scope
   theorem statement, proof-walk table, in-class realization test,
   out-of-class counterexamples, scope guards, sister-PR
   cross-references).
2. **Premise-class consistency.** All cited authorities exist on disk.
3. **β = 2 N_c / g_bare² → g_bare² = 1 at N_c = 3.** Exact `Fraction`
   arithmetic on the canonical Wilson small-a matching gives the
   unique solution `g_bare² = 1`.
4. **β = 6 at N_c = 3 (exact).** `β = 2 · N_c = 2 · 3 = 6`.
5. **Alternative-g_bare exclusion.** g_bare² ∈ {1/2, 2, 4} require
   β ≠ 6, hence are incompatible with the canonical normalization at
   the framework's β within the Wilson-action class.
6. **Realization-invariance within Wilson-class.** Three hypothetical
   in-class realizations (each at (CKN) + Wilson form) all give the
   same constraint.
7. **Out-of-class explicitness.** Symanzik-improved, tadpole-improved,
   non-Wilson, and generator-rescaled cases are listed with their
   algebra-change descriptions.
8. **Proof-walk audit.** Steps (G1), (G2), (G3), (G5), (G6) use only
   algebraic-class inputs; step (G4) is the Wilson-form admission.
   The runner confirms this classification.
9. **Forbidden-import audit.** Stdlib only, no PDG pins, no measured
   α_s, no fitted coefficients.
10. **Boundary check.** Wilson form, (CKN), pure algebraic
    universality, continuum-limit class, audit ratification all
    explicitly NOT closed.

## 11. Cross-references

- Parent framing: PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
  — algebraic-universality framing + first sub-piece (hypercharges).
- Parent gate (load-bearing source for chain (G1)–(G6)): PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667)
  — A4 closure / `g_bare = 1` bootstrap forcing
  ([`G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md`](G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md))
- Convention-admission analogues:
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) — SU(5) embedding consistency (admits SU(5) Killing form)
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) — A3 substep 4 closure (admits (LCL) labelling)
- Constraint-vs-convention theorem (CVC, the load-bearing g_bare = 1
  forcing): [`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md)
- Rescaling-freedom-removal theorem (RFR):
  [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md)
- Wilson small-a matching theorem (WM):
  [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
- Narrow convention statement (NCV):
  [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
- Cl(3) per-site uniqueness (CPS):
  [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
- Graph-first SU(3) integration (GFSU3):
  [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- Cl(3) color automorphism (carries (CKN) one hop upstream):
  [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
- Minimal axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## 12. Honest scope

**Branch-local theorem.** This note is the seventh sub-piece of the
algebraic-universality program (PR #670). It walks PR #667's
bootstrap chain (G1)–(G6) and isolates which steps depend on (CKN)
and the Wilson plaquette action form as load-bearing inputs. The
universality scope is therefore **narrower** than sub-pieces 1–6.

**Crucial scope distinction.**

- **Sub-pieces 1–6** are pure-algebraic universality: their proofs
  cite no action-form or generator-normalization input as
  load-bearing. They hold across any lattice formulation that
  produces the same chiral content + retained gauge structure +
  retained anomaly traces.
- **Sub-piece 7** (this note) is Wilson-action-class universality:
  the proof cites (CKN) + Wilson plaquette form as load-bearing
  admissions. It holds across any A_min-compatible realization
  *within that class*. Outside the class (Symanzik-improved Wilson,
  tadpole-improved Wilson, non-Wilson formulations, generator-
  rescaled bases), the β–g_bare algebra changes form and the same
  constraint does not directly apply.

**Why this is still a useful sub-piece.**

The Wilson-action class is the framework's actual choice — A4 (the
former axiom, now a derivation target per PR #667) commits to the
Wilson plaquette action with (CKN). Within that choice, the
constraint `g_bare = 1` does not require any lattice-realization-
specific input (no MC measurements, no PDG pins, no fitted
coefficients, no specific staggered-phase choice, no specific
BZ-corner labels). It is class-A algebraic substitution in the
Wilson-class small-a matching. The sub-piece formalizes this honest
narrower scope.

**Not in scope.**

- Pure algebraic universality of `g_bare = 1` (would require closing
  the Wilson plaquette form uniqueness from A_min).
- (CKN) derivation from raw A_min (separate meta-question, parallel
  to (LCL) status in PR #664).
- Audit ratification of PR #667's chain. This sub-piece consumes that
  chain as a black box.
- Independent gauge couplings g' (U(1)_Y) and g_2 (SU(2)_L). Those
  have their own normalization conventions and chain through different
  parts of the framework; out of scope here. This sub-piece covers
  SU(3) color only.

## 13. Sister-PR pattern

This sub-piece's pattern mirrors PR #670 (hypercharge sub-piece) but
with an honest narrower scope flag:

| PR | Sub-piece | Scope of universality | Action-form admission | Closure tier |
|---|---|---|---|---|
| #670 | 1 — SM hypercharges | Pure algebraic (A_min retained surface) | None | bounded_theorem |
| (this PR) | 7 — `g_bare = 1` constraint | Wilson-action-class | (CKN) + Wilson plaquette | bounded_theorem |

The remaining 5 follow-on sub-pieces from PR #670's §6 (Tr[Y²] = 40/3,
Y_GUT, sin²θ_W^GUT, 5̄ ⊕ 10 ⊕ 1 decomposition, anomaly cancellation /
3+1 spacetime) are all expected to be pure algebraic, in the same
class as sub-piece 1. Sub-piece 7 (this note) is the unique
"Wilson-class subset" sub-piece because of its WM dependence.

All sister sub-pieces follow the legitimate "import → bounded retained
→ retire import" path per memory feedback, with no new axioms and
explicit convention admissions.
