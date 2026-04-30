# ARTIFACT PLAN — axiom-first-foundations block01

Each cycle produces a paired theorem-note + runner. All paths are
branch-local on `physics-loop/axiom-first-foundations-block01-20260429`.

## Cycle 1 — R1: spin-statistics

- Theorem note: `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
- Runner: `scripts/axiom_first_spin_statistics_check.py`
- Output log: `outputs/axiom_first_spin_statistics_check_2026-04-29.txt`

Statement to prove: on `A_min`, the finite Grassmann generators that build
the local matter algebra at each `Z^3` site anticommute pairwise, and
the canonical bilinear form on the local Cl(3) module forces an
antisymmetric pairing between identical fermionic insertions in any
correlator. Hence the spin-statistics rule "fermions anticommute" is a
theorem, not an admitted import, on the canonical surface.

Runner exhibits: explicit construction of Grassmann generators on a
`L^3` lattice (small `L`, e.g. 2 or 4); test of pairwise anticommutation
of the lattice fermion field operators; symbolic check that swapping two
identical fermionic insertions in a representative two-point function
flips sign exactly.

## Cycle 2 — R2: reflection positivity

- Theorem note: `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- Runner: `scripts/axiom_first_reflection_positivity_check.py`
- Output log: `outputs/axiom_first_reflection_positivity_check_2026-04-29.txt`

Statement to prove: the canonical staggered-Dirac fermion action on
`Z^3` (with the temporal-direction reflection conventions used in the
package) plus the Wilson plaquette gauge action at `g_bare = 1` admits
a positive, Hermitian transfer matrix `T` on a finite physical Hilbert
space. Equivalently: site-reflection positivity holds for the canonical
action.

Runner exhibits: numerical construction of the transfer matrix on
small `L_t × L_s × L_s` slabs; spectrum check (all eigenvalues real,
non-negative); reflection-positivity inequality check on a basis of
local observables.

## Cycle 3 — R3: cluster decomposition / Lieb–Robinson

- Theorem note: `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- Runner: `scripts/axiom_first_cluster_decomposition_check.py`
- Output log: `outputs/axiom_first_cluster_decomposition_check_2026-04-29.txt`

Statement to prove: for a finite-range Hermitian Hamiltonian `H` built
from Cl(3) operators on `Z^3`, the connected two-point function
`<O_x(t) O_y(0)> - <O_x(t)><O_y(0)>` of bounded local operators decays
at most like `‖O‖^2 exp(-(d(x,y) - v|t|)/ξ)` for an explicit Lieb–Robinson
velocity `v` and length scale `ξ` determined by the local `Cl(3)`
operator norm and the lattice coordination number. Hence cluster
decomposition holds whenever `d(x,y) > v|t|`.

Runner exhibits: small-lattice exact diagonalisation; direct measurement
of the connected correlator vs separation; comparison to the predicted
Lieb–Robinson envelope.

## Stretch — R4: CPT theorem

- Theorem note (stretch): `docs/AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`
- Runner: `scripts/axiom_first_cpt_check.py` (only if a clean derivation
  closes; otherwise the note records the partial structure / sharper
  obstruction)
- Output log: `outputs/axiom_first_cpt_check_2026-04-29.txt`

Statement to attempt: there is an explicit involutive, antiunitary
operator `Θ` on the physical Hilbert space (constructed from Cl(3)
charge conjugation, lattice reflection, and complex conjugation) that
commutes with the canonical staggered-Dirac transfer matrix and reverses
the sign of all CP-odd local observables.

Honest fallback if the proof does not close in-block: output a partial
structure note that records the load-bearing wall (e.g. a specific
identity in Cl(3) charge conjugation that must be checked against
the staggered phases) and propose the next attack.
