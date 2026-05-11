# Bound State Selection: Stable Matter Only at d <= 3

**Status:** bounded - bounded or caveated result note

## Audit-conditional perimeter (2026-05-10)

Prior independent audit feedback on an earlier revision identified the
finite-lattice-to-continuum bridge as the load-bearing boundary:

> "The numerical part is not merely a printed constant: the source
> builds sparse lattice Laplacians and Coulomb potentials, diagonalizes
> them, and reports eigenvalue/localization diagnostics. However, the
> audited packet supplies no retained authority or bridge theorem
> connecting the finite, regularized, small-lattice results to
> continuum atomic stability or to the anthropic exclusion of d=2. The
> runner also labels d=4 and d=5 as fall-to-center in interpretive
> prose despite the implemented IPR threshold never flagging
> fall-to-center in the provided output."

The prior feedback repair target is `missing_bridge_theorem`: "provide a
retained analytic or independently audited bridge from the finite
regularized lattice diagnostics to continuum stable atomic chemistry,
including the exclusion of d=2 and the claimed d>=4 fall-to-center
behavior."

**Load-bearing scope (after this rigorization edit).** The retained
in-note content is the *finite-lattice diagnostic* listed in the
Results table (eigenvalue counts, ground-state energies, IPR values,
coupling-scan trends) at the modest lattice sizes specified; this is a
bounded, finite-N regularized numerical experiment. The interpretive
prose elsewhere in this note ("hydrogen-like Rydberg series",
"fall-to-center for d ≥ 4", "anthropic selection ⇒ d = 3", and the
Bounded-Claim "stable matter must exist ⇒ d = 3") is *not* covered by
the cited authority chain and is read as bridge-conditional. The
runner's "fall_to_center" column reports `False` for every row in the
cached output (see the Caveats section below); the Interpretation /
Bounded-Claim language extrapolates from the IPR *trend* under the
coupling scan, which is bounded-only and is not promoted to a
fall-to-center theorem.

This source edit only sharpens the conditional perimeter; no new
derivation is asserted and independent audit owns any current verdict
or effective status after the source change.

## Question

Does the d-dimensional Coulomb potential V(r) = -1/r^{d-2} support
bound states in a way that selects d=3 as the highest dimension with
stable atoms?

## Method

For d = 2, 3, 4, 5, build the lattice Hamiltonian H = -Laplacian + V on
a d-dimensional grid with Dirichlet boundary conditions, where V is the
d-dimensional Coulomb potential:

| d | Potential | Lattice |
|---|-----------|---------|
| 2 | V = -log(r) | 30x30 |
| 3 | V = -1/r | 16^3 |
| 4 | V = -1/r^2 | 10^4 |
| 5 | V = -1/r^3 | 5^5 |

Diagonalize H with scipy.sparse.linalg.eigsh. Count negative eigenvalues
(bound states). Analyze ground state localization via IPR (inverse
participation ratio) and radial decay profile. Run Crank-Nicolson
propagation to check dynamical localization.

Key diagnostic for fall-to-center: IPR approaching 1 means all weight on
one lattice site (the nucleus), which is the d >= 4 instability.

## Results

| d | N_bound | E_ground | IPR | Physical | Classification |
|---|---------|----------|-----|----------|---------------|
| 2 | 40+ | -2.56 | 0.0054 | YES | Confining (infinite bound states) |
| 3 | 8 | -0.74 | 0.0152 | YES | Hydrogen-like Rydberg series |
| 4 | 1 | -0.52 | 0.0147 | Marginal | Critical coupling, fall-to-center trend |
| 5 | 0 | +0.28 | 0.0153 | NO | No bound states |

### Coupling scan (d=4, marginal case)

| Coupling g | E_ground | N_bound | IPR |
|-----------|----------|---------|-----|
| 0.5 | +0.26 | 0 | 0.0005 |
| 1.0 | +0.19 | 0 | 0.0007 |
| 2.0 | -0.05 | 1 | 0.0037 |
| 3.0 | -0.52 | 1 | 0.0147 |
| 5.0 | -1.99 | 5 | 0.0363 |
| 8.0 | -4.65 | 10 | 0.0499 |
| 12.0 | -8.45 | 10 | 0.0563 |

IPR increases monotonically with coupling: the wavefunction concentrates
at the origin as coupling grows. This is the fall-to-center instability.

### Coupling scan (d=5)

No bound states for g <= 4. At g=8, one bound state appears with
IPR = 0.093 (high, approaching fall-to-center). d=5 requires
unrealistically strong coupling for any bound state, and even then
it is unstable.

## Interpretation

d=3 is the highest dimension with a Rydberg series -- multiple bound
states with distinct energy levels and exponentially localized
wavefunctions. This is what atoms require for chemistry.

- d=2: Confining potential, infinite bound states (but 2D)
- d=3: Finite Rydberg series (8 bound states at g=2), genuine localization
- d=4: Marginal. One bound state at critical coupling, but falls to center
  as coupling increases. No stable atomic structure.
- d=5: No bound states at physical couplings.

## Bounded Claim

The lattice Hamiltonian on the listed grid sizes (d = 2: 30×30; d = 3:
16³; d = 4: 10⁴; d = 5: 5⁵) reproduces a dimension-dependent
bound-state diagnostic in the printed bands of the Results table. On
the cited authority chain, the retained bounded statement is the
finite-lattice numerical reproduction itself; promotion of the
diagnostic to "d = 3 is selected as the unique dimension supporting
stable atoms" depends on a retained continuum-bridge theorem that the
prior audit feedback identified as missing. The "anthropic selection ⇒ d = 3"
prose is therefore a bridge-conditional reading, not a bounded theorem
of the cited dependency chain.

## Caveats

- Lattice sizes are modest (especially d=5 at 5^5 = 3125 sites)
- Dirichlet boundary conditions introduce finite-size effects
- The regularization r_min = 1 (lattice spacing) affects the
  d >= 4 singularity
- The "fall-to-center" descriptor for d ≥ 4 is an *interpretive
  reading of the IPR coupling-scan trend*, not an output of an
  implemented IPR threshold. The cached runner output reports
  `fall_to_center = False` for every row (see
  `logs/runner-cache/frontier_bound_state_selection.txt`); in
  particular, the runner does not flag d = 4 or d = 5 as
  fall-to-center under its current IPR threshold. The
  "fall-to-center trend" language is therefore not a runner-validated
  claim and is bridge-conditional under the prior feedback boundary.
- Angular momentum analysis not performed (would strengthen the argument)
- No retained continuum-bridge theorem connects the finite-lattice
  diagnostic to continuum atomic stability or to the d = 2 exclusion;
  the prior feedback repair target is to supply such a retained bridge
  theorem (or independently audited derivation) before any "stable
  matter must exist ⇒ d = 3" reading can be promoted past
  bridge-conditional.

## Script

`scripts/frontier_bound_state_selection.py`
