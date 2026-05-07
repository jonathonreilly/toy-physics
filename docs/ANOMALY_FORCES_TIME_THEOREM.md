# Anomaly Cancellation Forces 3+1 Spacetime

**Date:** 2026-04-24 (scope tightened 2026-05-02; citation chain partially
internalized 2026-05-03; audit-prep stale-citation correction 2026-05-07)
**Type:** bounded_theorem proposal. The earlier "moving toward
positive_theorem" framing was withdrawn during 2026-05-07 audit-prep
because admission (i) (ABJ anomaly-to-inconsistency on the lattice) is
not currently routed to an internal companion note on `main`: the
proposed companion (PR 402) was closed without merge.
Audit status is assigned only by the independent audit lane; this note
does not set or predict a verdict, and the source author does not
propose a retained / positive_theorem promotion at this time.
**Primary runner:** `scripts/frontier_anomaly_forces_time.py`
**Claim scope:** conditional 3+1 derivation. Three of four previously
bare external admissions are now routed to named companion notes; the
fourth (admission (i), ABJ anomaly-to-inconsistency on the lattice)
remains a bare external admission on current `main`:
  (i) the Adler--Bell--Jackiw anomaly-to-inconsistency implication for
  chiral gauge theories with gauge content `su(2) + su(3) + u(1)` and
  left-handed content `(2,3)_{+1/3} + (2,1)_{-1}` is **NOT currently
  internalized**. A proposed lattice Wess-Zumino / Fujikawa `Z^4`
  companion note (filename `AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md`,
  proposed in PR 402) was **closed without merge**; the file does not
  exist on `main`. Until a successor companion note lands, admission (i)
  is treated as a bare external admission to the standard ABJ result
  [1,2] for chiral gauge theories. This is the single open admission
  that keeps this row's load-bearing class at B;
  (ii) the opposite-chirality SU(2)-singlet right-handed completion is
  internalized by the gauge-closure aggregator
  [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md), which
  carries the proposed_retained (audit-pending) graph-first
  SU(2)/SU(3)/U(1) closure to which the singlet completion is matched.
  Citation status on `main`: present (proposed_retained, audit-pending);
  (iii) the Clifford-volume-element chirality (the only chirality grading
  available in this lattice formulation) is internalized by the staggered
  sublattice parity `epsilon(x) = staggered gamma_5` carried by
  [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md). Citation status on `main`:
  present (proposed_retained, audit-pending);
  (iv) the ultrahyperbolic / multi-time Cauchy-problem obstruction is no
  longer load-bearing for this row: the single-clock codimension-1
  evolution theorem in
  [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
  derives the single-clock codimension-1 hypothesis from retained primitives
  (RP positivity, microcausality, Lieb-Robinson, cluster decomposition,
  Cl(3)/Z^3), which directly excludes `d_t > 1` without needing the
  classical-PDE ultrahyperbolic obstruction. The Craig--Weinstein /
  Tegmark literature is now a corroborating cross-reference, not an
  external load-bearing admission. PR 418 merged 2026-05-03; citation
  status on `main`: present (proposed_retained, audit-pending).
Under these citations plus the open ABJ admission (i), spacetime
signature `(3,1)` is forced. The load-bearing chain has one remaining
bare external admission (admission (i)).
**Load-bearing class:** B (conditional bridge) on current `main`. Any
promotion toward A (positive theorem) is conditional on a successor
companion note for admission (i) landing on `main` AND on independent
audit ratification — neither condition is currently met.

## Boundary update (2026-05-07 audit-prep pass)

The 2026-05-02 version listed four external admissions as bare imports.
The 2026-05-03 citation pass routed all four to companion notes.
Audit-prep on 2026-05-07 corrected stale citations:

- Admission (iv) (single-clock codimension-1 evolution): companion
  PR 418 merged on 2026-05-03; the cited note is now present on `main`
  as proposed_retained (audit-pending).
- Admission (i) (ABJ anomaly-to-inconsistency on the lattice): the
  proposed companion note (PR 402, filename
  `AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md`)
  was **closed without merge**; the cited file does not exist on `main`.
  Admission (i) is therefore reverted to a bare external admission to
  the standard ABJ result for chiral gauge theories.
- Admissions (ii) and (iii) remain routed to `NATIVE_GAUGE_CLOSURE_NOTE.md`
  and `CPT_EXACT_NOTE.md`, both present on `main` as proposed_retained
  (audit-pending).

This row remains a conditional bridge (bounded_theorem) on `main`. The
"positive_theorem" promotion previously conditioned on two pending PRs
landing is now conditioned on a successor companion note for admission
(i) PLUS independent audit ratification — neither condition is currently
met. Source-note authority does not assign or propose retained /
positive_theorem status; only the independent audit lane does.

## Theorem (Anomaly-forced time, single-clock form, conditional)

Let the Cl(3) Clifford algebra acting on Z^3 produce the gauge algebra
su(2) + su(3) + u(1) with left-handed fermion content

    (2, 3)_{+1/3}  +  (2, 1)_{-1}

(one generation of quarks and leptons), per
[`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md).
The single-clock codimension-1 evolution structure (one strongly
continuous unitary `U(t) = exp(-itH)`, one initial codimension-1 surface,
arbitrary admissible local data, deterministic evolution) is supplied by
[`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
(present on `main` as proposed_retained, audit-pending; PR 418 merged
2026-05-03), which derives that structure from RP positivity,
microcausality, Lieb-Robinson velocity, and cluster decomposition. The
ABJ anomaly-to-inconsistency implication is **assumed as a bare external
admission** to the standard ABJ result [1,2] for chiral gauge theories
(no internal companion note on `main`; PR 402 was closed without merge).
The Clifford volume-element chirality is the staggered sublattice parity
`epsilon(x)` of [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md).

Then consistency of the quantum gauge theory forces exactly one temporal
dimension, giving spacetime signature `(3,1)`.

## Audit-lane handoff

```yaml
proposed_claim_type: bounded_theorem
audit_required_before_effective_retained: true
audit_handoff_status: |
  Source author submits this row for audit as a bounded_theorem
  (conditional 3+1 derivation). Three of four previously bare external
  admissions are routed to internal companion notes that are present on
  main as proposed_retained, audit-pending. The fourth (admission (i),
  ABJ anomaly-to-inconsistency on the lattice) remains a bare external
  admission because PR 402 was closed without merge. The author does
  NOT propose positive_theorem / retained promotion at this time.
  Independent audit lane decides verdict.
admission_routing_status:
  - admission_id: i
    description: ABJ anomaly-to-inconsistency for chiral gauge theory
    routing_state: bare external admission (NOT internalized on main)
    proposed_companion_filename: docs/AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md
    proposed_companion_pr: 402
    proposed_companion_pr_state: CLOSED without merge
    cited_reference: ABJ result [1,2] for chiral gauge theories
    blocks_positive_theorem_promotion: true
  - admission_id: ii
    description: opposite-chirality SU(2)-singlet right-handed completion
    routed_to: docs/NATIVE_GAUGE_CLOSURE_NOTE.md
    landing_state: present on main (proposed_retained, audit-pending aggregator)
  - admission_id: iii
    description: Clifford-volume-element chirality is the only chirality grading
    routed_to: docs/CPT_EXACT_NOTE.md
    landing_state: present on main (proposed_retained, audit-pending; sublattice parity epsilon(x) = staggered gamma_5)
  - admission_id: iv
    description: ultrahyperbolic / multi-time codimension-1 obstruction
    routed_to: docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md
    landing_state: present on main (proposed_retained, audit-pending; PR 418 merged 2026-05-03)
    note: |
      Single-clock codimension-1 evolution is now derived from retained
      primitives (RP positivity, microcausality, Lieb-Robinson, cluster
      decomposition, Cl(3)/Z^3); this directly excludes d_t > 1 without
      invoking the classical-PDE ultrahyperbolic obstruction.
      Craig-Weinstein 2009 and Tegmark 1997 reduce to corroborating
      cross-references, not load-bearing imports.
proposed_claim_scope: |
  Cl(3)/Z^3 gauge content plus three internalized companion theorems
  (admissions (ii), (iii), (iv)) plus a bare external admission to ABJ
  for chiral gauge theories (admission (i)) force spacetime signature
  (3,1). On current main this is a bounded_theorem (B-class conditional
  bridge). A future positive_theorem (A-class) promotion path requires
  (a) a successor companion note for admission (i) landing on main, AND
  (b) independent audit ratification of admissions (ii), (iii), (iv).
proposed_load_bearing_step_class: B (bounded conditional bridge) on current main
status_authority: independent audit lane only
companion_pr_status:
  - PR 402 (lattice Wess-Zumino / Fujikawa Z^4 theorem): CLOSED without merge
  - PR 418 (single-clock codimension-1 evolution theorem): MERGED 2026-05-03
```

This source note does not set or predict an audit outcome. It submits
the partially citation-internalized 3+1 derivation as a bounded_theorem.
Three previously-bare admissions are routed to companion notes on `main`
(themselves audit-pending); admission (i) remains a bare external
admission because the proposed companion (PR 402) was closed without
merge. The author does not propose retained / positive_theorem
promotion at this time.

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

Three anomaly coefficients are nonzero. By the Adler--Bell--Jackiw theorem
[1,2] (admission (i), bare external admission on current `main`), the
gauge theory violates unitarity: Ward identities break and longitudinal
gauge boson modes fail to decouple. The theory is inconsistent as a
quantum field theory.

*Remark (quantization).* The framework is quantum by assumption (Hilbert
space axiom). A gauge symmetry that is not consistently quantizable
contradicts this axiom, so anomaly cancellation is mandatory.

### Step 2. Anomaly cancellation requires a right-handed singlet completion

Anomaly cancellation requires adding right-handed fermions. Since
chirality distinguishes SU(2) doublets (left) from singlets (right),
the new fermions must be SU(2) singlets. Parametrize them as:

    u_R = (1, 3)_{y_1},  d_R = (1, 3)_{y_2},  e_R = (1, 1)_{y_3},  nu_R = (1, 1)_{y_4}

The anomaly cancellation conditions Tr[Y] = 0, Tr[Y^3] = 0, and
Tr[SU(3)^2 Y] = 0 for the full (left + right) content yield three
equations in four unknowns. The cubic equation factors into two branches
related by relabeling `e_R <-> nu_R`. Imposing the neutral-singlet
identification `nu_R = 0` selects the Standard Model branch:

    y_1 = 4/3,   y_2 = -2/3,   y_3 = -2,   y_4 = 0

These are exactly the Standard Model hypercharge assignments. The
hypercharge anomaly traces, the `SU(3)^3` cubic anomaly, and the Witten
`SU(2)` count vanish for the completed spectrum. The time theorem only needs
the existence of an SU(2)-singlet opposite-chirality completion; it does not
rely on uniqueness from anomaly arithmetic alone.

*Remark (alternative chirality mechanisms).* In a local quantum field
theory on a lattice, the only algebraic source of a chirality grading
is the Clifford volume element. No alternative mechanism exists within
this framework. In the Cl(3)/Z^3 staggered formulation, this Clifford
volume-element chirality is realized concretely as the sublattice parity
`epsilon(x) = staggered gamma_5` of
[`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), so the chirality grading used
below is an internal framework primitive, not a bare admission.

### Step 3. Chirality requires even total spacetime dimension

The right-handed fermions are SU(2) singlets distinguished from
left-handed doublets by a chirality operator gamma_5. This operator must
satisfy:

  (a) gamma_5^2 = +I  (involution),
  (b) {gamma_5, gamma_mu} = 0 for all Dirac matrices gamma_mu.

By the classification of Clifford algebras [3]: in Cl(p,q) with
n = p + q generators, the volume element omega = gamma_1 ... gamma_n
satisfies

    omega gamma_mu = (-1)^{n-1} gamma_mu omega

Therefore:
- **n even:** omega anticommutes with all generators. With appropriate
  phase normalization, gamma_5 = (phase) * omega satisfies (a) and (b).
  The spinor representation splits S = S_+ + S_- (Weyl spinors exist).
- **n odd:** omega commutes with all generators (it is central in the
  algebra). No element of the Clifford algebra can simultaneously
  anticommute with all generators. Chirality does not exist.

For d_s = 3 spatial dimensions, chirality requires d_s + d_t even,
hence d_t must be **odd**: d_t in {1, 3, 5, ...}.

### Step 4. Single-clock codimension-1 evolution excludes `d_t > 1`

From Step 3, chirality allows odd `d_t in {1, 3, 5, ...}`. To finish the
derivation, one uses the framework's single-clock codimension-1 evolution
structure as derived in
[`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
(present on `main` as proposed_retained, audit-pending; PR 418 merged
2026-05-03), which itself follows from retained primitives (RP
positivity, microcausality, Lieb-Robinson velocity bound, cluster
decomposition, Cl(3)/Z^3). That theorem fixes:

- one evolution parameter,
- one codimension-1 initial surface,
- arbitrary admissible initial states on that surface,
- unique deterministic evolution.

For `d_t = 1`, relativistic fields admit the standard hyperbolic Cauchy
problem on codimension-1 slices, compatible with the single-clock
structure.

For `d_t > 1`, the existence of multiple inequivalent timelike directions
contradicts the *single* generator of the unitary one-parameter group
fixed by the single-clock theorem above: arbitrary local data on a
codimension-1 slice cannot be propagated by a unique `U(t)` if there is
more than one independent time direction. So `d_t > 1` is excluded
*directly* by the single-clock codimension-1 evolution theorem, without
needing the external classical-PDE ultrahyperbolic obstruction.

The classical-PDE ultrahyperbolic / multi-time results
(Craig--Weinstein 2009 [4], Tegmark 1997 [5]) corroborate the same
exclusion from a complementary continuum-PDE angle: codimension-1
well-posedness for `d_t > 1` requires extra nonlocal Fourier-space
support constraints incompatible with arbitrary local data. They are
retained here as cross-references, not as load-bearing external
admissions.

Closed timelike curves, Wick-rotation pathologies, and multi-Hamiltonian
objections remain useful supporting remarks, but they are not the
load-bearing theorem step.

### Step 5. Conclusion

Combining Steps 1--4, with three previously-bare admissions routed to
cited companion theorems and admission (i) retained as a bare external
ABJ admission:

    Cl(3) on Z^3
      => [NATIVE_GAUGE_CLOSURE_NOTE]
      => SU(2) x SU(3) x U(1) with left-handed (2,3)_{+1/3} + (2,1)_{-1}
      => gauge anomaly (Tr[Y^3] != 0)
      => [bare external admission to ABJ result [1,2]; PR 402 closed without merge]
      => anomaly cancellation required
      => [opposite-chirality SU(2)-singlet completion via NATIVE_GAUGE_CLOSURE_NOTE]
      => chirality operator gamma_5 required
      => [CPT_EXACT_NOTE: Clifford-volume / sublattice parity epsilon(x) = staggered gamma_5]
      => d_total = d_s + d_t must be even
      => d_t odd, with d_s = 3
      => [AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03 (on main; PR 418 merged 2026-05-03)]
      => single-clock codimension-1 evolution excludes d_t > 1
      => d_t = 1 uniquely
      => spacetime is 3+1 dimensional.  QED.

On current `main`, three of the four bridge premises above are citations
to companion notes (NATIVE_GAUGE_CLOSURE_NOTE [proposed_retained],
CPT_EXACT_NOTE [proposed_retained], single-clock codimension-1 evolution
[proposed_retained]); the fourth (ABJ anomaly-to-inconsistency on the
lattice) is a bare external admission to references [1,2]. The chain has
one remaining bare external admission, so the row submits as a
bounded_theorem (B-class conditional bridge), not as a positive theorem.

## Numerical verification

The script `scripts/frontier_anomaly_forces_time.py` verifies the algebraic
claims computationally: anomaly traces, Clifford algebra relations,
chirality operator properties in even/odd dimensions, the codimension-1
constraint witness, and the complete SM charge table. The theorem authority
is the proof above plus the exact anomaly arithmetic in the runner. The raw
runner score should not be cited by itself, because a small number of output
items are explicitly marked as assertions rather than numerical checks.

## References

[1] S. L. Adler, "Axial-vector vertex in spinor electrodynamics,"
    Phys. Rev. 177, 2426 (1969).

[2] J. S. Bell and R. Jackiw, "A PCAC puzzle: pi0 -> gamma gamma
    in the sigma model," Nuovo Cim. A 60, 47 (1969).

[3] H. B. Lawson and M.-L. Michelsohn, *Spin Geometry*,
    Princeton University Press (1989), Ch. I.

[4] W. Craig and S. Weinstein, "On determinism and well-posedness in
    multiple time dimensions," Proc. Roy. Soc. A 465, 3023 (2009).
    arXiv:0812.0210.

[5] M. Tegmark, "On the dimensionality of spacetime,"
    Class. Quant. Grav. 14, L69 (1997). arXiv:gr-qc/9702052.
