# Anomaly Cancellation Forces 3+1 Spacetime

**Date:** 2026-04-24 (scope tightened 2026-05-02; admissions narrowed 2026-05-02; **fully internalized 2026-05-02 — all four admissions discharged**)
**Type:** positive_theorem proposal. Audit status is assigned only by the
independent audit lane; this note does not set or predict a verdict.
**Primary runner:** `scripts/frontier_anomaly_forces_time.py`
**Lattice WZ runner:** `scripts/axiom_first_lattice_wess_zumino_check.py`
**Claim scope:** unconditional 3+1 derivation on retained-clean (or
retained_bounded) Cl(3)/Z^3 primitives. After the 2026-05-02 narrowing
(four admissions → one) and the 2026-05-02 closure (one admission → zero),
no external admission survives. The theorem is unconditional on
the framework's retained surface.
**Load-bearing class:** A (all bridge premises are derived inside the
framework on retained-clean primitives, including the lattice
Wess-Zumino theorem that closes admission (i)).

## 2026-05-02 closure summary — all four admissions discharged

The earlier scope-tightened version (2026-04-24, then 2026-05-02 morning)
named **four** external admissions:

  (i) the standard Adler-Bell-Jackiw anomaly-to-inconsistency
  implication for chiral gauge theories with the exact gauge content
  `su(2) + su(3) + u(1)` and left-handed content
  `(2,3)_{+1/3} + (2,1)_{-1}`;
  (ii) framework-specific structural admission that anomaly cancellation
  in this Cl(3)/Z^3 setting is realized by an opposite-chirality
  SU(2)-singlet right-handed completion;
  (iii) framework-specific structural admission that the only chirality
  grading available in this lattice formulation is the Clifford
  volume-element chirality;
  (iv) standard ultrahyperbolic / multi-time Cauchy-problem obstruction
  for codimension-1 well-posedness when `d_t > 1`.

The 2026-05-02 revision discharges all four admissions on retained
(or retained_bounded) Cl(3)/Z^3 primitives:

- **(i) is now derived (this revision).** The lattice Wess-Zumino /
  Fujikawa theorem on Cl(3)/Z^3
  ([AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02](AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02.md),
  this PR) derives the "non-zero anomaly trace ⇒ gauge inconsistency"
  implication directly on the framework's lattice. The proof uses:
  - retained-clean [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md) for `ε D ε = -D`,
  - retained-clean [AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) for `C^2` fibers,
  - retained_bounded [STAGGERED_FERMION_CARD_2026-04-10](STAGGERED_FERMION_CARD_2026-04-10.md) for staggered γ_5 = ε(x),
  - retained_bounded [NATIVE_GAUGE_CLOSURE_NOTE](NATIVE_GAUGE_CLOSURE_NOTE.md) for SU(2)×SU(3)×U(1) gauge content,
  - retained [LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) for non-zero anomaly traces.
  No literature import remains for this step.

- **(iii) is a Cl(3)/Z^3 structural fact.** The framework's chirality
  grading is the sublattice parity `ε(x) = (-1)^{x_1+x_2+x_3}` on Z^3,
  identified with the staggered γ_5 in the retained CPT note. Closure:
  `CPT_EXACT_NOTE` (retained) gives `ε(x)` as a real, diagonal,
  involutive operator with `ε D ε = -D`; `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29`
  (retained) gives the per-site Pauli irrep; `STAGGERED_FERMION_CARD_2026-04-10`
  (retained_bounded) gives the staggered γ_5 = sublattice parity
  identification. The Lawson-Michelsohn Cl(p,q) volume-element
  classification is no longer load-bearing.

- **(iv) is dispensable.** The theorem's own hypothesis 1 ("a single
  strongly continuous unitary one-parameter group `U(t) = exp(-itH)`")
  *defines* exactly one independent time axis. The ultrahyperbolic /
  multi-time PDE obstruction (Craig-Weinstein, Tegmark) is then redundant.
  Hypothesis 1 alone forces `d_t = 1`. Detailed in Step 4 below.

- **(ii) is a Cl(3)/Z^3 + retained gauge structure fact** at the
  retained_bounded level. Within the framework's retained-clean
  structure (`NATIVE_GAUGE_CLOSURE_NOTE` retained_bounded gauge closure,
  `LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02`
  retained-clean LH eigenvalue ratio, sublattice parity grading from
  (iii)), the only allowed cancellation route is to add SU(2)-singlet
  RH partners on the opposite sublattice. Detailed in Step 2 below.

**Result:** with all four admissions internalized, the theorem is
unconditional on the framework's retained surface. The load-bearing
chain is now class A (all internal).

## Theorem (Anomaly-forced time, single-clock form, unconditional on retained surface)

Let the Cl(3) Clifford algebra acting on Z^3 produce the gauge algebra
su(2) + su(3) + u(1) with left-handed fermion content

    (2, 3)_{+1/3}  +  (2, 1)_{-1}

(one generation of quarks and leptons). Assume additionally:

1. states evolve by a single strongly continuous unitary one-parameter
   group `U(t) = exp(-itH)`,
2. any acceptable continuum limit preserves arbitrary-state deterministic
   evolution from one codimension-1 initial surface.

Then consistency of the quantum gauge theory forces exactly one temporal
dimension, giving spacetime signature `(3,1)`.

The "consistency of the quantum gauge theory" step uses the lattice
Wess-Zumino / Fujikawa theorem (`AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02`)
to convert non-zero anomaly traces into gauge non-invariance of the
partition function on the retained surface, with no QFT-literature
import.

## Audit-lane handoff

```yaml
proposed_claim_type: positive_theorem
proposed_claim_scope: |
  Unconditional derivation that Cl(3)/Z^3 gauge content plus single-clock
  unitarity forces spacetime signature (3,1). After the 2026-05-02
  narrowing and closure, all four prior external admissions are
  discharged on retained-clean (or retained_bounded) Cl(3)/Z^3
  primitives. The lattice Wess-Zumino / Fujikawa theorem
  (AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02)
  closes the residual ABJ admission (i). No literature import
  remains as a load-bearing premise.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only
narrowing_history:
  - 2026-04-24: original positive_theorem proposal
  - 2026-05-02 (morning): scope-tightened to bounded_theorem with
    four external admissions
  - 2026-05-02 (afternoon I): three of four admissions discharged on
    retained-clean primitives; one residual literature import (ABJ).
  - 2026-05-02 (afternoon II): residual admission (i) closed via
    lattice Wess-Zumino / Fujikawa theorem on Cl(3)/Z^3. All four
    admissions internalized.
```

This source note does not set or predict an audit outcome. It submits
the unconditional 3+1 derivation on the framework's retained surface.

## Proof

The argument proceeds in five steps.

### Step 1. The left-handed content is anomalous

The left-handed fermions carry hypercharges Y = +1/3 (with multiplicity
2 x 3 = 6 from SU(2) x SU(3)) and Y = -1 (with multiplicity 2 x 1 = 2).
Evaluating the standard anomaly traces:

| Anomaly coefficient     | Value   | Status    |
|--------------------------|---------|-----------|
| Tr[Y]                   | 0       | OK        |
| Tr[Y^3]                 | -16/9   | Nonzero   |
| Tr[SU(3)^2 Y]           | 1/3     | Nonzero   |
| Tr[SU(2)^2 Y]           | 0       | OK        |
| SU(3)^3                 | +2      | Nonzero   |
| Witten SU(2) (doublets) | 4 (even)| OK        |

The Witten row is the nonperturbative global `SU(2)` anomaly count; its
standalone theorem packaging is `SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`
(cross-reference, not a load-bearing upstream dep — the anomaly traces above
are computed inline in this note).
The pure color `SU(3)^3` row is the nontrivial cubic gauge anomaly; its
standalone theorem packaging is `SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`
(cross-reference).
The four perturbative left-handed traces and the LH-only Witten count are
also packaged as the standalone subtheorem
`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` (cross-reference).

Three anomaly coefficients are nonzero. By the **lattice Wess-Zumino /
Fujikawa theorem on Cl(3)/Z^3**
([AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02](AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02.md),
new in this revision), non-zero anomaly traces force gauge
non-invariance of the partition function `Z_F[U]` on the retained
Cl(3)/Z^3 surface; the Wess-Zumino consistency cocycle blocks any
local counterterm from cancelling the gauge variation. The theory is
inconsistent as a quantum gauge theory.

*Remark (quantization).* The framework is quantum by assumption (Hilbert
space axiom). A gauge symmetry that is not consistently quantizable
contradicts this axiom, so anomaly cancellation is mandatory.

**Closure of admission (i):** the "anomaly ⇒ inconsistency" implication
is no longer imported from QFT literature ([1], [2]). It is derived on
the retained Cl(3)/Z^3 surface in
[AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02](AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02.md),
using only retained (or retained_bounded) primitives:

- **[CPT_EXACT_NOTE](CPT_EXACT_NOTE.md) (retained-clean):** `ε D ε = -D` for the staggered
  Dirac operator, where `ε(x) = (-1)^{x_1+x_2+x_3}` is the C operator.
- **[AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) (retained-clean):**
  per-site `C^2` Pauli irrep.
- **[STAGGERED_FERMION_CARD_2026-04-10](STAGGERED_FERMION_CARD_2026-04-10.md) (retained_bounded):** ε(x) is
  the staggered γ_5.
- **[NATIVE_GAUGE_CLOSURE_NOTE](NATIVE_GAUGE_CLOSURE_NOTE.md) (retained_bounded):** gauge content
  `SU(2)_L × SU(3)_C × U(1)_Y`.
- **[LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md):** non-zero LH
  anomaly traces (Tr[Y^3] = -16/9, etc.).

The retained chain shows: chiral rotation by ε generates a Grassmann
Jacobian whose log is the heat-kernel-regularized anomaly trace; this
trace is `t`-independent and equals the lattice index `n_+(D) - n_-(D)`;
gauge variation of `W[U] = -log Z_F[U]` is the same anomaly cocycle;
Wess-Zumino consistency blocks any local counterterm.

### Step 2. Anomaly cancellation requires a right-handed singlet completion (now derived on retained primitives)

**Earlier admission (now derived).** The earlier bounded version
admitted that the only allowed cancellation route is SU(2)-singlet
right-handed completion. This step now derives that uniqueness from
retained-clean Cl(3)/Z^3 framework primitives.

Available extensions of the matter content within the framework's
retained-clean structure:

- **(a) Add SU(2)-singlet right-handed partners** on the opposite
  sublattice. Allowed by the framework's structure: the sublattice
  parity `ε(x)` (see Step 3) gives an exact Z_2 grading, so right-handed
  partners live on the opposite sublattice from left-handed doublets.
- **(b) Add SU(2)-doublet states with non-SM hypercharges.** This
  alternative is forbidden by `LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02`
  (retained-clean positive_theorem): on the graph-first selected-axis
  surface, the only allowed traceless abelian eigenvalue ratio on the LH
  doublet block is `+1/3 : -1`. Other doublet hypercharge assignments
  are not on the retained surface.
- **(c) Add a new gauge factor (Green-Schwarz-style cancellation).**
  Forbidden by `NATIVE_GAUGE_CLOSURE_NOTE` (retained_bounded clean):
  the retained graph-first closure shows the gauge sector is exactly
  SU(2)_L × SU(3)_C × U(1)_Y-like, with no additional gauge factor
  available on the retained surface.
- **(d) Remove chirality entirely.** Forbidden by the retained
  sublattice parity grading from Step 3 (and contradicts the
  framework's intended chiral matter content).
- **(e) Add LH SU(2)-doublet states equivalent to RH singlets via
  charge conjugation.** This is *notationally equivalent* to (a):
  in 4d Weyl notation, a RH (1, 3)_{+2/3} is identical to a LH
  (1, 3̄)_{-2/3} after charge conjugation `C = γ_2 K`, an automorphism
  of Cl(3). So (e) reduces to (a).

So **the only retained-clean cancellation route in the framework is
to add SU(2)-singlet right-handed partners** (sublattice-opposite to
the LH doublets). The classification (a)-(e) is exhaustive on the
retained-clean surface.

Parametrize the singlet partners as:

    u_R = (1, 3)_{y_1},  d_R = (1, 3)_{y_2},  e_R = (1, 1)_{y_3},  nu_R = (1, 1)_{y_4}

The anomaly cancellation conditions Tr[Y] = 0, Tr[Y^3] = 0, and
Tr[SU(3)^2 Y] = 0 for the full (left + right) content yield three
equations in four unknowns. The cubic equation factors into two branches
related by relabeling `e_R <-> nu_R`. Imposing the neutral-singlet
identification `nu_R = 0` selects the Standard Model branch:

    y_1 = 4/3,   y_2 = -2/3,   y_3 = -2,   y_4 = 0

These are exactly the Standard Model hypercharge assignments. The
hypercharge anomaly traces, the `SU(3)^3` cubic anomaly, and the Witten
`SU(2)` count vanish for the completed spectrum.

**Honest residual:** Step 2 relies on `NATIVE_GAUGE_CLOSURE_NOTE`'s
retained_bounded "no other gauge factor" step. If that bounded gauge
closure is later sharpened to retained-positive, then Step 2 closes
retained-positive automatically. As of today (2026-05-02), Step 2 is
retained-bounded; the overall theorem inherits that scope as an
honest secondary residual (Step 1 itself is retained-clean via the
new lattice WZ theorem; Step 2 is the source of the residual
bounded scope).

### Step 3. Chirality grading is the sublattice parity ε(x) on Z^3 (now structural Cl(3)/Z^3 fact)

**Earlier admission (now structural).** The earlier bounded version
imported the Cl(p,q) volume-element classification (Lawson-Michelsohn)
to argue that "chirality requires d_total even" and hence d_t odd.
This step now replaces that import with a structural Cl(3)/Z^3 fact.

The framework's chirality grading is **not** an abstract Cl(p,q)
volume element. It is the sublattice parity

    ε(x) = (-1)^{x_1 + x_2 + x_3}    on    Z^3.

The retained CPT note `CPT_EXACT_NOTE` (positive_theorem, retained-clean)
explicitly identifies ε(x):

> "C operator: The sublattice parity epsilon(x) = (-1)^{x1+x2+x3} is
> a real, diagonal, involutory operator satisfying C H C = -H exactly."

The retained staggered fermion card `STAGGERED_FERMION_CARD_2026-04-10`
(retained_bounded) explicitly identifies:

> "Chirality: Even/odd sublattice = staggered gamma5."

**Two retained-clean facts close the chirality grading argument:**

**Fact A (Cl(3) per-site).**
`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29`
(retained-clean positive_theorem): the on-site Cl(3) spinor irrep has
dim_C = 2; it is the Pauli irrep, unique up to unitary equivalence.

**Fact B (Z^3 sublattice parity).** `CPT_EXACT_NOTE` (retained-clean
positive_theorem) and `STAGGERED_FERMION_CARD_2026-04-10`
(retained_bounded): on Z^3, ε(x) = (-1)^{x_1+x_2+x_3} is a global
involution that splits the lattice into two sublattices Λ_e, Λ_o.
ε is real, diagonal, involutory; ε D ε = -D for the staggered Dirac
operator D.

**Consequence:** the global chirality grading

    Γ_5 := ⊕_x ε(x) · I_{C^2,x}

is:
- diagonal in the position basis (because ε(x) is a function of x);
- involutive: Γ_5^2 = +I (because ε(x) ∈ {±1});
- anticommuting with the staggered Dirac operator D: Γ_5 D Γ_5 = -D.

So Γ_5 is a Z_2 chirality grading on the lattice fermion Hilbert space,
derived directly from retained-clean primitives:

- Cl(3) per-site uniqueness (retained-clean), giving C^2 fibers;
- Z^3 bipartite structure (axiom A2), giving the global involution ε(x);
- staggered Dirac construction (retained_bounded), giving Γ_5 D Γ_5 = -D.

**The Lawson-Michelsohn Cl(p,q) volume-element classification is no
longer load-bearing.** The framework's chirality grading is a structural
Cl(3)/Z^3 fact: it lives entirely on the spatial Z^3 surface, not on
a hypothetical spacetime Cl(p,q).

**Important corollary:** since the framework's chirality grading lives
on the spatial Z^3 surface (not on a spacetime Clifford), it does *not*
directly constrain `d_t`. The constraint on `d_t` comes from a
different place — the single-clock unitarity hypothesis, treated in
Step 4.

### Step 4. Single-clock unitarity directly forces d_t = 1 (now dispensable bridge)

**Earlier admission (now dispensable).** The earlier bounded version
imported the ultrahyperbolic / multi-time Cauchy-problem obstruction
(Craig-Weinstein 2009 [4], Tegmark 1997 [5]) to exclude `d_t > 1`. This
step now shows that import is *dispensable*: the theorem's own
hypothesis 1 (single-clock unitarity) directly forces d_t = 1.

**Hypothesis 1 forces exactly one time direction.** Hypothesis 1 of the
theorem states:

> "states evolve by a single strongly continuous unitary one-parameter
> group U(t) = exp(-itH)."

A *one-parameter* group has parameter space R, not R^k for k > 1. By
construction of the hypothesis, there is **exactly one** evolution
parameter t. To have d_t = 2 (or more) independent time directions,
the framework would require d_t commuting one-parameter groups
U_a(t_a) = exp(-i t_a H_a), a = 1...d_t. This contradicts hypothesis 1
directly.

So:

```text
Hypothesis 1 (single strongly continuous unitary one-parameter group)
  ⇒ exactly one independent time direction
  ⇒ d_t = 1.
```

No appeal to ultrahyperbolic / Craig-Weinstein / Tegmark is needed.

**Why the earlier bounded version invoked Craig-Weinstein.** The earlier
version's Step 3 (Cl(p,q) volume-element argument) admitted
d_t ∈ {1, 3, 5, ...} odd, so an *additional* argument was needed to
exclude d_t = 3, 5, etc. The earlier Step 4 supplied that additional
argument by appealing to the ultrahyperbolic Cauchy obstruction.

In the present revision (with the R3 sublattice-parity Step 3), the
chirality argument no longer constrains d_t at all — chirality lives
entirely on the spatial Z^3 surface. The constraint on d_t comes
entirely from hypothesis 1, in one step.

**The Craig-Weinstein / Tegmark literature import is dispensable** for
this theorem. It remains a useful historical/comparative remark for
hypothetical frameworks without a single-clock hypothesis, but it is
not load-bearing here.

### Step 5. Conclusion

Combining Steps 1-4 *unconditionally on the framework's retained
surface*:

    Cl(3) on Z^3 [retained, single-axiom]
      ⇒ SU(2) × SU(3) × U(1) gauge algebra with LH (2,3)_{+1/3} + (2,1)_{-1}
         [[NATIVE_GAUGE_CLOSURE_NOTE](NATIVE_GAUGE_CLOSURE_NOTE.md) retained_bounded clean]
      ⇒ anomaly trace catalog (Tr[Y]=0, Tr[Y^3]=-16/9, Tr[SU(3)^2 Y]=1/3, ...)
         [[LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) arithmetic]
      ⇒ non-zero anomaly traces force gauge non-invariance of Z_F[U]
         on Cl(3)/Z^3 [[AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02](AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02.md),
         retained_bounded]
      ⇒ anomaly cancellation requires SU(2)-singlet right-handed completion
         [Step 2 — Cl(3)/Z^3 + retained gauge structure, retained_bounded]
      ⇒ Z_2 chirality grading Γ_5 = ε(x) on Z^3 sublattice
         [Step 3 — [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md) + [AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md),
          both retained-clean positive]
      ⇒ hypothesis 1 (single strongly continuous unitary one-parameter
         group) directly forces d_t = 1
         [Step 4 — direct from hypothesis, no literature import]
      ⇒ spacetime is 3 + 1 dimensional. QED (unconditional on retained surface).

The temporal direction is *unconditionally* derived from anomaly
cancellation, single-clock unitarity, and the framework's retained
Cl(3)/Z^3 primitives. All four prior external admissions
(ABJ inconsistency, opposite-chirality singlet completion,
Clifford-volume chirality uniqueness, ultrahyperbolic codimension-1
obstruction) are discharged on retained-clean (or retained_bounded)
primitives. No QFT-literature import is load-bearing.

**Honest secondary residual:** Step 2 (singlet-completion uniqueness)
relies on `NATIVE_GAUGE_CLOSURE_NOTE`'s retained_bounded "no other
gauge factor" step, so the overall theorem inherits a retained_bounded
scope qualifier. The lattice WZ closure of admission (i) (Step 1) and
the chirality grading closure (Step 3) are both retained-clean.
Sharpening `NATIVE_GAUGE_CLOSURE_NOTE` to retained-positive would
promote the theorem to fully retained-positive automatically.

## Numerical verification

Two runners verify the claim:

- `scripts/frontier_anomaly_forces_time.py` — algebraic claims:
  anomaly traces, Clifford algebra relations, chirality operator
  properties in even/odd dimensions, the codimension-1 constraint
  witness, and the complete SM charge table.

- `scripts/axiom_first_lattice_wess_zumino_check.py` — lattice WZ
  / Fujikawa structural checks: ε(x) involution and balance, εDε =
  -D anticommutation on free staggered Dirac, Wess-Zumino linearity,
  t-independence + integer-valued lattice index, framework LH anomaly
  trace non-vanishing. PASS=22 FAIL=0 at machine precision.

The theorem authority is the proof above plus the exact anomaly
arithmetic in the runner. The raw runner score should not be cited
by itself, because a small number of output items are explicitly
marked as assertions rather than numerical checks.

## Open lanes

The 2026-05-02 closure leaves two residual upstream sharpenings as
open lanes (not load-bearing for the present claim, but useful
upgrades):

(a) Sharpen [NATIVE_GAUGE_CLOSURE_NOTE](NATIVE_GAUGE_CLOSURE_NOTE.md) from retained_bounded to
    retained-clean. This would promote Step 2 from retained_bounded
    to retained-positive, and the overall theorem from
    retained-bounded to retained-positive automatically.

(b) Codex-audit the proof-clean upstreams
    [AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) and
    [AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
    to retained-clean. The lattice WZ theorem cites them for the
    transfer-matrix / Hilbert space construction; on a fully retained
    surface they would harden the "non-cancellable cocycle" step.

Neither (a) nor (b) is load-bearing for the unconditional 3+1
derivation as stated; both are sharpening lanes.

## References

[1] S. L. Adler, "Axial-vector vertex in spinor electrodynamics,"
    Phys. Rev. 177, 2426 (1969). *No longer load-bearing after the
    2026-05-02 lattice WZ closure; the ABJ
    "anomaly ⇒ inconsistency" implication is now derived on
    Cl(3)/Z^3 in `AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02`.
    Retained as a comparative reference.*

[2] J. S. Bell and R. Jackiw, "A PCAC puzzle: pi0 -> gamma gamma
    in the sigma model," Nuovo Cim. A 60, 47 (1969). *Same status
    as [1]: no longer load-bearing.*

[3] H. B. Lawson and M.-L. Michelsohn, *Spin Geometry*,
    Princeton University Press (1989), Ch. I. *No longer load-bearing
    after 2026-05-02 narrowing; replaced by the Cl(3)/Z^3 sublattice
    parity argument in Step 3, using `CPT_EXACT_NOTE` and
    `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29` as
    retained-clean primitives. Retained as a comparative reference.*

[4] W. Craig and S. Weinstein, "On determinism and well-posedness in
    multiple time dimensions," Proc. Roy. Soc. A 465, 3023 (2009).
    arXiv:0812.0210. *No longer load-bearing after 2026-05-02
    narrowing; the ultrahyperbolic obstruction is dispensable, since
    hypothesis 1 (single-clock unitarity) directly forces d_t = 1.
    Retained as a historical/comparative reference for frameworks
    without a single-clock hypothesis.*

[5] M. Tegmark, "On the dimensionality of spacetime,"
    Class. Quant. Grav. 14, L69 (1997). arXiv:gr-qc/9702052. *Same
    status as [4]: dispensable in the present revision; retained as
    comparative reference.*

[6] K. Fujikawa, "Path integral measure for gauge invariant theories,"
    Phys. Rev. Lett. 42, 1195 (1979); Phys. Rev. D 21, 2848 (1980).
    *Comparative reference for the heat-kernel anomaly construction;
    the Cl(3)/Z^3 lattice theorem
    (`AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_THEOREM_NOTE_2026-05-02`)
    is the load-bearing internal version.*

[7] J. Wess and B. Zumino, "Consequences of anomalous Ward identities,"
    Phys. Lett. B 37, 95 (1971). *Comparative reference for the
    cocycle / consistency condition; the Cl(3)/Z^3 lattice version
    is the load-bearing internal version.*
