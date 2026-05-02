# Anomaly Cancellation Forces 3+1 Spacetime

**Date:** 2026-04-24 (scope tightened 2026-05-02)
**Type:** bounded_theorem (proposed; audit-lane to ratify; current ledger
verdict is `audited_conditional` on `positive_theorem`, this edit narrows
source-note prose to a `bounded_theorem` claim conditional on four
explicitly-named external bridge admissions)
**Claim scope:** conditional 3+1 derivation under four explicitly-named
external admissions:
  (i) the standard Adler--Bell--Jackiw anomaly-to-inconsistency
  implication for chiral gauge theories with the exact gauge content
  `su(2) + su(3) + u(1)` and left-handed content
  `(2,3)_{+1/3} + (2,1)_{-1}`;
  (ii) the framework-specific structural admission that anomaly
  cancellation in this Cl(3)/Z^3 setting is realized by an opposite-
  chirality SU(2)-singlet right-handed completion (rather than a
  different anomaly-free extension);
  (iii) the framework-specific structural admission that the only
  chirality grading available in this lattice formulation is the
  Clifford volume-element chirality;
  (iv) the standard ultrahyperbolic / multi-time Cauchy-problem
  obstruction for codimension-1 well-posedness when `d_t > 1`
  (Craig--Weinstein 2009, Tegmark 1997).
Under these four admissions, spacetime signature `(3,1)` is forced.
**Load-bearing class:** B (conditional bridge — the four bridge
premises above are explicitly external, not derived from framework
primitives in this note).

## Out of scope: unconditional first-principles 3+1 derivation

The unconditional / first-principles version, in which every bridge
premise is derived from framework primitives without external
admissions, is *not* the claim of this row. The latest fresh-context
audit explicitly named the four external bridge premises above as
unclosed in the current ledger; this edit accepts that boundary and
narrows the load-bearing claim of this note to the conditional
derivation under those four named admissions.

## Theorem (Anomaly-forced time, single-clock form, conditional)

Let the Cl(3) Clifford algebra acting on Z^3 produce the gauge algebra
su(2) + su(3) + u(1) with left-handed fermion content

    (2, 3)_{+1/3}  +  (2, 1)_{-1}

(one generation of quarks and leptons). Assume additionally:

1. states evolve by a single strongly continuous unitary one-parameter
   group `U(t) = exp(-itH)`,
2. any acceptable continuum limit preserves arbitrary-state deterministic
   evolution from one codimension-1 initial surface,
3. the four external bridge premises listed in the Claim scope above
   (ABJ anomaly-to-inconsistency, opposite-chirality singlet completion,
   Clifford-volume-element chirality uniqueness, ultrahyperbolic
   codimension-1 obstruction).

Then consistency of the quantum gauge theory forces exactly one temporal
dimension, giving spacetime signature `(3,1)`.

## Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Conditional derivation that Cl(3) gauge content plus the four named
  external admissions (ABJ inconsistency, opposite-chirality singlet
  completion, Clifford-volume chirality uniqueness, ultrahyperbolic
  codimension-1 obstruction) force spacetime signature (3,1). NOT an
  unconditional first-principles 3+1 derivation.
proposed_load_bearing_step_class: B
status_authority: independent audit lane only
```

This source note does not set or predict an audit outcome. It submits
the conditional 3+1 derivation under the four named external
admissions. The unconditional first-principles version (where every
bridge premise is derived from framework primitives) remains out of
scope for this row.

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
standalone retained packaging is `SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`
(cross-reference, not a load-bearing upstream dep — the anomaly traces above
are computed inline in this note).
The pure color `SU(3)^3` row is the nontrivial cubic gauge anomaly; its
standalone retained packaging is `SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`
(cross-reference).
The four perturbative left-handed traces and the LH-only Witten count are
also packaged as the standalone retained subtheorem
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
this framework.

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

### Step 4. Single-clock codimension-1 evolution excludes `d_t > 1` (external bridge)

From Step 3, chirality allows odd `d_t in {1, 3, 5, ...}`. To finish the
derivation, one uses the framework's clock structure together with an
external classical PDE result.

The graph framework already has one Hamiltonian clock. So any acceptable
continuum limit must preserve:

- one evolution parameter,
- one codimension-1 initial surface,
- arbitrary admissible initial states on that surface,
- unique deterministic evolution.

For `d_t = 1`, relativistic fields admit the standard hyperbolic Cauchy
problem on codimension-1 slices.

For `d_t > 1`, the continuum problem is ultrahyperbolic / multi-time.
The standard classical-PDE result (Craig--Weinstein 2009 [4],
Tegmark 1997 [5]) is that codimension-1 well-posedness is not
available for arbitrary local data: one must impose extra nonlocal
Fourier-space support constraints on the initial data. That is
incompatible with the framework's graph semantics, which allow
arbitrary local basis states on a single time slice.

**Audit boundary (external bridge premise iv):** the ultrahyperbolic
codimension-1 obstruction is imported here from the classical-PDE
literature ([4], [5]) as an external bridge premise. This note does
not derive that obstruction from framework primitives. The narrowed
claim is conditional on this external result.

In that precise sense, and conditional on the literature obstruction,
`d_t > 1` is excluded by the single-clock / codimension-1 Cauchy
requirement.

Closed timelike curves, Wick-rotation pathologies, and multi-Hamiltonian
objections remain useful supporting remarks, but they are not the
load-bearing theorem step.

### Step 5. Conclusion

Combining Steps 1--4 *under the four external bridge admissions named in
the Claim scope above*:

    Cl(3) on Z^3
      => SU(2) x SU(3) x U(1) with left-handed (2,3)_{+1/3} + (2,1)_{-1}
      => gauge anomaly (Tr[Y^3] != 0)
      => [admission (i): ABJ inconsistency for chiral gauge theory]
      => anomaly cancellation required
      => [admission (ii): opposite-chirality SU(2)-singlet completion]
      => chirality operator gamma_5 required
      => [admission (iii): Clifford-volume-element chirality only]
      => d_total = d_s + d_t must be even
      => d_t odd, with d_s = 3
      => [admission (iv): ultrahyperbolic codimension-1 obstruction]
      => single-clock codimension-1 evolution excludes d_t > 1
      => d_t = 1 uniquely
      => spacetime is 3+1 dimensional.  QED (conditional).

The temporal direction is *conditionally* derived from the combination
of anomaly cancellation, chirality, single-clock codimension-1
evolution, and the four external bridge admissions named above. The
unconditional / first-principles version (with every bridge premise
re-derived from framework primitives) is *out of scope* for this
narrowed claim and remains an open lane.

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
