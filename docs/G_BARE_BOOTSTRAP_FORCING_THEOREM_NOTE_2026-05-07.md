# A4 Closure — g_bare = 1 Bootstrap Forcing from A_min + Retained Surface

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the canonical bootstrap proof
that `g_bare = 1` is forced from A1+A2 plus the retained-tier surface plus
the explicit (CKN) canonical Killing-form normalization admission. This
note threads the existing 2026-05-03 constraint-vs-convention +
rescaling-freedom-removal candidates plus the older Wilson small-a matching
into a single end-to-end derivation, analogous to the Block 06 closure of
substep 4 of the staggered-Dirac realization gate (PR #664). Does NOT
unilaterally promote the parent `G_BARE_DERIVATION_NOTE.md` row; that
parent's status is set by independent audit on the full chain.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_g_bare_bootstrap_forcing.py`

## Position in the project's open-gate map

The 2026-05-03 axiom restoration ([`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md))
recategorized the framework's two formerly-axiom items A3 and A4 as
**open derivation targets** (not framework axioms). The two open gates
are:

- **A3 — staggered-Dirac realization derivation target.** Bootstrap
  proof chain is now end-to-end at `bounded_theorem` tier across
  Blocks 02 (Grassmann), 03 (Kawamoto-Smit), 04 (BZ-corner), and 06
  (physical-species forcing — PR #664). Awaiting full-chain audit
  ratification.
- **A4 — g_bare = 1 derivation target.** Statement: *A1+A2 (+ closure
  of A3) forces `g_bare = 1` by canonical Cl(3) connection
  normalization; the Wilson plaquette coefficient `β = 2 N_c = 6`
  follows.*

This note is the **canonical bootstrap-packaging closure of A4** at
`bounded_theorem` tier with explicit (CKN) admission. Sister to
PR #664's Block 06 for A3.

## 0. Question

After the 2026-05-03 constraint-vs-convention disambiguation theorem
([`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md))
plus the rescaling-freedom-removal theorem
([`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md))
the parent `G_BARE_DERIVATION_NOTE.md` carries the structurally-forced
reading of `g_bare = 1` once the canonical Cl(3) connection normalization
(CN) is admitted. The remaining residual is:

```text
What is the canonical end-to-end bootstrap proof of g_bare = 1 from
A1+A2 plus the retained-tier surface plus the standard SU(N) Killing
form on the fundamental, with the convention layer (CN/CKN) surfaced
explicitly?
```

## Answer

**Below.** The bootstrap chain threads:

1. A1 → Cl(3) per-site uniqueness with Pauli realization (CL3 per-site
   uniqueness)
2. A1+A2 → graph-first SU(3) integration (gl(3) ⊕ gl(1) commutant on
   the taste cube)
3. SU(3) generators in the fundamental representation carry the
   canonical Killing-form normalization `Tr(T_a T_b) = δ_ab/2` (math
   convention input — same class as the SU(5) Killing form in PR
   #655 and the (LCL) labelling in PR #664)
4. Wilson plaquette small-a matching gives `β = 2 N_c / g_bare²`
   (G_BARE_TWO_WARD_*; old retained matching)
5. (CN) + (β = 2 N_c at canonical normalization) + rescaling-freedom-
   removal → `g_bare² = 1` via algebraic substitution
   (constraint-vs-convention theorem)
6. At N_c = 3, `g_bare = 1` and `β = 6` follow

The convention layer is exclusively at (CN) — the standard SU(N)
Killing form. There is no second `g_bare`-side convention.

## Setup

### Premises (A1+A2 + retained-tier inputs + math convention)

| ID | Statement | Class |
|---|---|---|
| A1 | Local algebra is Cl(3) | framework axiom |
| A2 | Spatial substrate is Z³ | framework axiom |
| CPS | Per-site Cl(3) uniqueness with Pauli realization, dim-2 chirality split | retained per [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) |
| GFSU3 | Graph-first SU(3) integration: gl(3) ⊕ gl(1) commutant on the taste cube, semisimple part = su(3) | retained per [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| WM | Wilson plaquette small-a matching: `β = 2 N_c / g_bare²` | retained per [`G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`](G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md) and [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md) |
| RFR | Rescaling-freedom-removal: under (CN), the rescaling A → c·A shifts β = c²·β with `g_bare` unchanged | per [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md) (decoration under cl3_color_automorphism_theorem) |
| CVC | Constraint-vs-convention: given (CN) + (WM) + (RFR), `g_bare = 1` is structurally forced; the convention layer is at (CN), not at `g_bare` | per [`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md) (positive_theorem, audited_conditional, td=430) |
| RIG | Rigidity reading: once the concrete su(3) operator algebra is fixed, no independent bare coupling parameter survives | per [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md) (positive_theorem) |
| NCV | Narrow-convention statement: `g_bare = 1` is the Wilson canonical-normalization convention | per [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md) (bounded_theorem, audited_conditional, td=296) |

### Forbidden imports

- NO PDG observed values (no measured α_s, no g coupling values)
- NO lattice MC empirical measurements as proof inputs
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms (A_min stays {A1, A2})
- NO appeal to dynamical fixed-point selection of g_bare (the dynamical-
  fixation route is closed by [`G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`](G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md))

### Admitted convention (explicit)

**(CKN) Canonical Killing-form Normalization.** SU(3) generators `T_a`
in the fundamental representation are normalized to the canonical
Killing form

```text
Tr(T_a T_b) = δ_ab / 2     (acting on the 3-dim fundamental).        (CKN)
```

This is the *standard* normalization for SU(N) generators in the
fundamental, equivalent to setting the Dynkin index `T(fund) = 1/2`. It
is **standard mathematical machinery** — the same convention class as:

- the SU(5) Killing-form admission used in PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)
  for the SU(5) embedding consistency theorem, surfaced there as
  `Tr[T_a T_b]_5 = (1/2)·δ_{ab}`;
- the (LCL) generation-labelling convention used in PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664)
  for the staggered-Dirac substep 4 closure;
- the doubled-vs-minimal `Y` Convention A vs B admission in cycles 16/19;
- the SU(5) vs SO(10)/E6 GUT-group choice admission in cycle 19.

(CKN) is **not load-bearing for the framework's two axioms** — A1+A2
are unchanged. (CKN) is the math-convention layer at which the
convention status of `g_bare = 1` lives, per the 2026-05-03 constraint-
vs-convention theorem. With (CKN) admitted, `g_bare = 1` is structurally
forced (no separate `g_bare`-side convention layer).

## Theorem (g_bare = 1 forced under A1+A2 + retained + (CKN))

**Bounded theorem.** Under {A1, A2, CPS, GFSU3, WM, RFR, CVC, RIG, NCV}
+ the explicit (CKN) admission:

```text
The framework's bare gauge coupling is forced to
  g_bare = 1
on the canonical Cl(3) connection normalization, with the Wilson
plaquette coefficient
  β = 2 N_c = 6
following at N_c = 3. The convention layer is exclusively at (CKN);
there is no separate g_bare-side convention.
```

In particular:

- (G1) A1 + CPS → Cl(3) per-site has dim-2 chirality summands with
  canonical Pauli generators σ_a satisfying `Tr(σ_a σ_b) = 2·δ_ab` on
  the 2-dim spinor module (basic Pauli identity on the 2-dim
  representation).
- (G2) A1+A2 + GFSU3 → graph-first SU(3) is the semisimple part of
  the gl(3) ⊕ gl(1) commutant on the taste cube, carrying SU(3)
  generators T_a (a = 1..8) in the canonical fundamental representation
  on the canonical color-triplet block.
- (G3) (CKN): T_a in the fundamental satisfy `Tr(T_a T_b) = δ_ab / 2`
  by standard SU(N) Killing-form convention.
- (G4) WM: at the canonical generator basis (G3), the Wilson plaquette
  small-a matching forces `β = 2 N_c / g_bare²`.
- (G5) RFR + CVC: under (CKN) + (WM), the unique compatible
  `g_bare² = 1`. Any alternative requires either violating (CKN)
  (case a: generator dilation) or importing an external scale
  (case b: forbidden by A1+A2 minimality).
- (G6) Therefore: `g_bare = 1` and `β = 2 N_c = 6` at `N_c = 3`.

**Proof sketch.**

(G1) is the standard Pauli identity on Cl(3)'s per-site dim-2
representation, retained per CPS.

(G2) is the retained graph-first SU(3) integration theorem (GFSU3).

(G3) is (CKN), the explicit math-convention admission.

(G4) is the retained Wilson small-a matching (WM), which gives
β as the unique coefficient compatible with the canonical generator
basis.

(G5) chains RFR + CVC: RFR removes the `T_a → c·T_a` rescaling
freedom by showing it shifts β = c²·β; CVC then uses (G3) + (G4) +
RFR to algebraically force `g_bare² = 1` at the canonical
normalization. The chain works *given* (CKN); without (CKN) the
convention layer migrates to `g_bare`, but that case is the older
narrow-convention reading (NCV) which is not the load-bearing path
here.

(G6) is direct algebra: at N_c = 3, `β = 2·3 = 6`, and from
`β = 2 N_c / g_bare²` we get `g_bare² = 2 N_c / β = 6/6 = 1`. ∎

## What this closes

- The A4 open gate is now **bootstrap-closed at bounded_theorem tier**
  with explicit (CKN) admission, analogous to A3's closure via Blocks
  02-04 + 06.
- The constraint-vs-convention disambiguation is packaged with the
  rescaling-freedom-removal + Wilson small-a matching into a single
  end-to-end chain from A1+A2 to `g_bare = 1`.
- The convention layer is surfaced explicitly as (CKN) — the SU(N)
  Killing form on the fundamental — and is identified as the *only*
  convention layer for A4 (no separate `g_bare`-side admission).
- The "g_bare = 1" / "β = 2 N_c = 6" pair becomes available as a
  bootstrap-derived constraint pair (modulo (CKN)), not as separate
  conventions.

## What this does NOT close

- **The (CKN) admission itself.** The convention status of the SU(N)
  Killing-form normalization is intrinsic to SU(N) representation theory
  as standard math. Whether (CKN) is *uniquely forced* by A1+A2 alone
  (i.e., without invoking standard math machinery) is a separate
  meta-question and is OUT OF SCOPE here. This note treats (CKN) the
  same way PR #655 treated the SU(5) Killing form and PR #664 treated
  the (LCL) labelling convention: a clean math-convention admission
  surfaced explicitly.
- **The Wilson plaquette action form.** That `β · Σ_p (1 - Re Tr U_p / N_c)`
  is the canonical action form is a separate question — the Wilson form
  is the simplest gauge-invariant lattice action with minimal locality,
  but proving its uniqueness from A1+A2 is a different open derivation
  target. This note assumes the Wilson form via WM.
- **The fermion realization.** The staggered-Dirac realization gate
  (A3) is closed elsewhere (substeps 1-4 via Blocks 02-04 + 06,
  PR #664). This note depends on A3's closure only weakly (via the
  graph-first SU(3) commutant which uses Z³ structure but not full
  fermion content).
- **Independent audit ratification.** The constraint-vs-convention
  theorem (CVC) is at audited_conditional. Its retention drives the
  parent `G_BARE_DERIVATION_NOTE.md`'s eventual retention. Until
  independent audit retains CVC + RFR + this note, A4 stays
  bounded-closed but not retained.

## Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on retained-tier {A1, A2, CPS, GFSU3, WM} and audited_conditional
  {CVC, RFR}, plus the explicit (CKN) math-convention admission. Eligible
  for retention upgrade once: (a) CVC + RFR reach retained tier via
  independent audit, (b) WM's audit-conditional companions
  (G_BARE_TWO_WARD_*) are similarly cleared, (c) this note is independently
  audited, and (d) (CKN) admission is ratified as legitimate math-
  convention layer (analogous to the SU(5) Killing form in cycle 16/19,
  the (LCL) labelling in PR #664).
audit_required_before_effective_retained: true
bare_retained_allowed: false
parent_update_allowed_only_after_retained: true
```

The parent `G_BARE_DERIVATION_NOTE.md` is **not** to be updated from
this note alone. Per its own dependency-chain gate, it requires
retained-tier closure of CVC + RFR before its `open_gate` status can
be retired. This note is the canonical bootstrap-packaging that the
audit lane can use to evaluate the full chain; promotion of the parent
remains an audit-lane decision.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_g_bare_bootstrap_forcing.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: A4 (g_bare = 1) is bootstrap-closed at bounded_theorem tier
modulo the explicit (CKN) Canonical Killing-form Normalization
admission. The chain A1+A2 + retained → g_bare = 1 holds via the
constraint-vs-convention + rescaling-freedom-removal + Wilson small-a
matching theorems at audited_conditional / retained tier.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings present (theorem, premises (A1, A2, CPS, GFSU3, WM, RFR, CVC, RIG, NCV) all labeled, (CKN) convention surfaced, (G1)-(G6) chain steps named).
2. **Premise-class consistency.** Each cited premise's note exists. The note's claim about audit class matches the audit-ledger's effective_status as of 2026-05-07.
3. **Pauli identity verification.** `Tr(σ_a σ_b) = 2·δ_ab` for the 2-dim Pauli generators.
4. **(CKN) consistency.** With T_a = σ_a/2 (the canonical SU(2) embedding into fundamental), Tr(T_a T_b) = δ_ab/2 holds.
5. **(WM) algebra.** Given β = 2·N_c / g_bare² and N_c = 3, β = 6 forces g_bare² = 1 as an exact `Fraction` substitution.
6. **(RFR) rescaling identity.** A → c·A shifts β as β' = c²·β with g_bare unchanged on the canonical generator basis.
7. **Alternative-g_bare exclusion.** g_bare² ∈ {1/2, 2, 4} all force β ≠ 6 at N_c = 3, hence are incompatible with the canonical normalization at the framework's β.
8. **(CKN) admission audit.** Convention layer surfaced explicitly + flagged not-load-bearing for A1+A2 (analogous to (LCL) admission audit in PR #664).
9. **Forbidden-import audit.** Stdlib only, no PDG pins, no measured α_s.
10. **Boundary check.** Wilson form, fermion realization, (CKN) derivation from raw A_min, and audit ratification all explicitly NOT closed.

## Cross-references

- Parent gate: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md)
- Sister A3 closure (analogous packaging pattern): [`STAGGERED_DIRAC_PHYSICAL_SPECIES_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_FORCING_THEOREM_NOTE_2026-05-07.md) (PR #664)
- Constraint-vs-convention theorem (CVC, the load-bearing g_bare=1 forcing): [`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md)
- Rescaling-freedom-removal theorem (RFR): [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md)
- Wilson small-a matching theorems (WM): [`G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`](G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md), [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
- Rigidity reading (RIG): [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md)
- Narrow convention statement (NCV): [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
- Cl(3) per-site uniqueness (CPS): [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
- Graph-first SU(3) integration (GFSU3): [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- Dynamical-fixation obstruction (closed; this route is NOT used here): [`G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`](G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md)
- Status correction audit packet (the 2026-05-02 disposition that drove the 2026-05-03 repair candidates): [`G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md)
- Convention-admission analogues: [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md) (Convention A vs B), [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md) (SU(5) vs SO(10)/E6 GUT group choice), [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (PR #655, SU(5) Killing form admission)
- Minimal axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Honest scope

**Branch-local theorem.** This note packages the existing 2026-05-03
g_bare repair candidates plus retained Wilson small-a matching plus
retained graph-first SU(3) into a single end-to-end bootstrap proof of
A4, with the explicit (CKN) Canonical Killing-form Normalization
admission surfaced. Same closure pattern as PR #655 (SU(5) embedding)
and PR #664 (A3 substep 4): convert "admitted" to "derived modulo
explicit convention admission" using A_min + retained surface as the
load-bearing base.

**Not in scope.**

- Closed-form derivation of (CKN) itself from raw A_min. The SU(N)
  Killing form on the fundamental is standard math machinery; whether
  it descends from "raw A1+A2 alone" is a separate meta-question
  parallel to the (LCL) status in PR #664.
- Wilson plaquette action form uniqueness from A_min. Treated here
  via the WM premise; deeper uniqueness is downstream.
- Promotion of the parent `G_BARE_DERIVATION_NOTE.md` row. That is an
  audit-lane decision contingent on retention of CVC + RFR + this
  note.
- Independent gauge couplings g' (U(1)_Y) and g_2 (SU(2)_L). Those
  have their own normalization conventions and chain through different
  parts of the framework; out of scope here. This note covers SU(3)
  color only.

## Sister-PR pattern

This PR's closure pattern mirrors:

| PR | Gate / target | Convention admission | Closure tier |
|---|---|---|---|
| #655 | SU(5) embedding consistency from cycle 16/19 | SU(5) Killing form `Tr[T_a T_b]_5 = δ_ab/2` | bounded_theorem |
| #664 | A3 substep 4 (physical-species reading) | (LCL) generation labelling by mass-ordering | bounded_theorem |
| **(this PR)** | **A4 (g_bare = 1) bootstrap closure** | **(CKN) SU(3) Killing form `Tr(T_a T_b) = δ_ab/2`** | **bounded_theorem** |

All three follow the legitimate "import → bounded retained → retire
import" path per memory feedback, with no new axioms and explicit
convention admissions.
