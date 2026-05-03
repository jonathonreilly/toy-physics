# Anomaly Cancellation Forces 3+1 Spacetime

**Date:** 2026-04-24 (scope tightened 2026-05-02; citation chain internalized 2026-05-03)
**Type:** bounded_theorem proposal moving toward positive_theorem proposal.
Audit status is assigned only by the independent audit lane; this note does
not set or predict a verdict.
**Primary runner:** `scripts/frontier_anomaly_forces_time.py`
**Claim scope:** conditional 3+1 derivation. The four bridge premises that
were previously listed as bare external admissions are now each routed to a
named companion note rather than left as unaudited imports:
  (i) the Adler--Bell--Jackiw anomaly-to-inconsistency implication for
  chiral gauge theories with gauge content `su(2) + su(3) + u(1)` and
  left-handed content `(2,3)_{+1/3} + (2,1)_{-1}` is internalized by the
  lattice Wess-Zumino / Fujikawa `Z^4` theorem in
  [`AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md`](AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md)
  (companion PR pending merge; this row's positive-theorem promotion is
  conditional on that landing);
  (ii) the opposite-chirality SU(2)-singlet right-handed completion is
  internalized by the gauge-closure aggregator
  [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md), which
  carries the retained graph-first SU(2)/SU(3)/U(1) closure to which the
  singlet completion is matched;
  (iii) the Clifford-volume-element chirality (the only chirality grading
  available in this lattice formulation) is internalized by the staggered
  sublattice parity `epsilon(x) = staggered gamma_5` carried by
  [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md);
  (iv) the ultrahyperbolic / multi-time Cauchy-problem obstruction is no
  longer load-bearing for this row: the single-clock codimension-1
  evolution theorem in
  [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
  derives the single-clock codimension-1 hypothesis from retained primitives
  (RP positivity, microcausality, Lieb-Robinson, cluster decomposition,
  Cl(3)/Z^3), which directly excludes `d_t > 1` without needing the
  classical-PDE ultrahyperbolic obstruction. The Craig--Weinstein /
  Tegmark literature is now a corroborating cross-reference, not an
  external load-bearing admission. (Companion PR pending merge.)
Under these citations, spacetime signature `(3,1)` is forced. The load-bearing
chain has no bare external admissions once the two companion PRs land.
**Load-bearing class:** B (conditional bridge) on current main; promotes to
A (positive theorem) once the two companion notes land and are picked up
on `main`.

## Boundary update (2026-05-03 citation pass)

The 2026-05-02 version listed four external admissions as bare imports.
This edit replaces each bare admission with a citation to a retained or
about-to-be-retained companion note (see Claim scope, items (i)--(iv)).
The unconditional / first-principles 3+1 derivation, with every bridge
premise derived from framework primitives, is now *the* targeted claim
of this row: it becomes a positive theorem on current main once the two
companion PRs (lattice WZ on `Z^4`, single-clock codimension-1 evolution)
land. Until they land on `main`, this note remains a conditional bridge
referencing those companion notes by filename; the prose chain below has
no bare admissions but is conditional on the companion notes' presence.

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
(companion PR pending merge), which derives that structure from RP
positivity, microcausality, Lieb-Robinson velocity, and cluster
decomposition. The ABJ anomaly-to-inconsistency implication is internalized
by
[`AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md`](AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md)
(companion PR pending merge). The Clifford volume-element chirality is the
staggered sublattice parity `epsilon(x)` of
[`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md).

Then consistency of the quantum gauge theory forces exactly one temporal
dimension, giving spacetime signature `(3,1)`.

## Audit-lane handoff

```yaml
proposed_claim_type: positive_theorem
audit_required_before_effective_retained: true
audit_handoff_status: |
  Author proposes positive_theorem promotion on the basis that all four
  previously bare external admissions are now routed to internal companion
  notes. Audit lane decides ratification.
previously_bounded_admissions_now_internal:
  - admission_id: i
    description: ABJ anomaly-to-inconsistency for chiral gauge theory
    routed_to: docs/AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md
    landing_state: companion PR pending merge to main
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
    landing_state: companion PR pending merge to main
    note: |
      Single-clock codimension-1 evolution is now derived from retained
      primitives (RP positivity, microcausality, Lieb-Robinson, cluster
      decomposition, Cl(3)/Z^3); this directly excludes d_t > 1 without
      invoking the classical-PDE ultrahyperbolic obstruction.
      Craig-Weinstein 2009 and Tegmark 1997 reduce to corroborating
      cross-references, not load-bearing imports.
proposed_claim_scope: |
  Cl(3)/Z^3 gauge content plus the four cited internal companion theorems
  force spacetime signature (3,1). When all four cited companion notes are
  present on main, this row has no bare external admissions and submits as
  a positive_theorem. Until the two pending companion PRs merge, the row
  effectively reads as bounded_theorem on current main, with the citation
  chain pre-positioned.
proposed_load_bearing_step_class: A (positive theorem) once both pending companion PRs land; B (bounded conditional) on current main pending those merges
status_authority: independent audit lane only
companion_prs_pending:
  - PR-402-equivalent (lattice Wess-Zumino / Fujikawa Z^4 theorem)
  - PR-418 (single-clock codimension-1 evolution theorem)
```

This source note does not set or predict an audit outcome. It submits
the citation-internalized 3+1 derivation. The previously-bare external
admissions are now routed to companion notes; the row's positive-theorem
promotion is conditional only on those companion notes being present on
`main`.

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
[1,2], the gauge theory violates unitarity: Ward identities break and
longitudinal gauge boson modes fail to decouple. The theory is
inconsistent as a quantum field theory.

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
(companion PR pending merge), which itself follows from retained
primitives (RP positivity, microcausality, Lieb-Robinson velocity bound,
cluster decomposition, Cl(3)/Z^3). That theorem fixes:

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

Combining Steps 1--4, with each previously-bare admission now routed to a
cited companion theorem:

    Cl(3) on Z^3
      => [NATIVE_GAUGE_CLOSURE_NOTE]
      => SU(2) x SU(3) x U(1) with left-handed (2,3)_{+1/3} + (2,1)_{-1}
      => gauge anomaly (Tr[Y^3] != 0)
      => [AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02 (PR pending)]
      => anomaly cancellation required
      => [opposite-chirality SU(2)-singlet completion via NATIVE_GAUGE_CLOSURE_NOTE]
      => chirality operator gamma_5 required
      => [CPT_EXACT_NOTE: Clifford-volume / sublattice parity epsilon(x) = staggered gamma_5]
      => d_total = d_s + d_t must be even
      => d_t odd, with d_s = 3
      => [AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03 (PR pending)]
      => single-clock codimension-1 evolution excludes d_t > 1
      => d_t = 1 uniquely
      => spacetime is 3+1 dimensional.  QED.

Once the two pending companion PRs land on `main`, every bridge premise
above is a citation to a retained or audit-pending companion note
(retained: NATIVE_GAUGE_CLOSURE_NOTE [proposed_retained], CPT_EXACT_NOTE
[proposed_retained]; about-to-be-retained: the two pending companion
notes). The chain has no bare external admission, and the row submits as
a positive theorem rather than as a conditional bridge.

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
