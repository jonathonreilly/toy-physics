# Anomaly Cancellation Forces 3+1 Spacetime

## Theorem (Anomaly-forced time, single-clock form)

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
| Witten SU(2) (doublets) | 4 (even)| OK        |

The Witten row is the nonperturbative global `SU(2)` anomaly count; its
standalone retained packaging is
[`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md).

Two anomaly coefficients are nonzero. By the Adler--Bell--Jackiw theorem
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

These are exactly the Standard Model hypercharge assignments. All five
anomaly traces vanish for the completed spectrum. The time theorem only
needs the existence of an SU(2)-singlet opposite-chirality completion; it
does not rely on uniqueness from anomaly arithmetic alone.

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

### Step 4. Single-clock codimension-1 evolution excludes `d_t > 1`

From Step 3, chirality allows odd `d_t in {1, 3, 5, ...}`. To finish the
derivation, one uses the framework's clock structure rather than more
anomaly arithmetic.

The graph framework already has one Hamiltonian clock. So any acceptable
continuum limit must preserve:

- one evolution parameter,
- one codimension-1 initial surface,
- arbitrary admissible initial states on that surface,
- unique deterministic evolution.

For `d_t = 1`, relativistic fields admit the standard hyperbolic Cauchy
problem on codimension-1 slices.

For `d_t > 1`, the continuum problem is ultrahyperbolic / multi-time.
Codimension-1 well-posedness is not available for arbitrary local data:
one must impose extra nonlocal Fourier-space support constraints on the
initial data. That is incompatible with the framework's graph semantics,
which allow arbitrary local basis states on a single time slice.

In that precise sense, `d_t > 1` is excluded by the single-clock /
codimension-1 Cauchy requirement.

Closed timelike curves, Wick-rotation pathologies, and multi-Hamiltonian
objections remain useful supporting remarks, but they are not the
load-bearing theorem step.

### Step 5. Conclusion

Combining Steps 1--4:

    Cl(3) on Z^3
      => SU(2) x SU(3) x U(1) with left-handed (2,3)_{+1/3} + (2,1)_{-1}
      => gauge anomaly (Tr[Y^3] != 0)
      => anomaly cancellation requires right-handed SU(2) singlets
      => chirality operator gamma_5 required
      => d_total = d_s + d_t must be even
      => d_t odd, with d_s = 3
      => single-clock codimension-1 evolution excludes d_t > 1
      => d_t = 1 uniquely
      => spacetime is 3+1 dimensional.  QED.

The temporal direction is not assumed; it is **derived** from the
combination of anomaly cancellation, chirality, and single-clock
codimension-1 evolution.

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
