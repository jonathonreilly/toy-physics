# Sparse Hermitian H + Hermitian-Exponentiation Readout + Locality Empirical Probe: Operational Reduction Note

**Date:** 2026-04-12 (originally); 2026-05-10 (audit-narrowing refresh:
explicit class-F definitional-substitution framing under named admitted
inputs).
**Status:** scope-narrowed bounded operational note. The runner numerically
verifies four consequences (Hamiltonian-support gives a graph, Hermitian
exponentiation is unitary, Schrodinger current is conserved, locality
versus dissipation versus unfactored topology comparisons) **after** the
named inputs `(sparse Hermitian H, Born-style readout convention,
Hamiltonian-support = edges extraction rule)` are supplied. The "single
axiom" framing — "conserved information flow on a network" — is a
definitional renaming of the original graph-plus-unitary package; this
note **does not** derive sparsity, Hermiticity, locality, or the specific
Hamiltonian structure from the verbal axiom alone.
**Claim type:** meta
**Claim boundary (in-note framing):** bounded operational note —
`(sparse Hermitian H, Hermitian-exponentiation readout, "support = edges"
extraction rule, locality probe choice)` ⇒ four runner-verified numerical
consequences.
The pre-refresh audit-ledger row recorded `claim_type: meta` with a
renaming verdict; this in-note framing records that renaming boundary
(class F, with the prior audit-recorded note that a second auditor may
re-classify as class E), without proposing any current audit-side
verdict or `claim_type` revision.
**Status authority:** independent audit lane only.
**Authority role:** records that the four numerical consequences follow
from `(sparse Hermitian H, Hermitian-exponentiation readout, support
= edges extraction rule)` as a class-F definitional renaming of the
graph-plus-unitary package. **Does not** propose retained, positive-
theorem, or framework-reduction promotion. The accepted-input ledger
for the current paper package remains the physical `Cl(3)` local
algebra on the `Z^3` spatial substrate per
[`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md).
**Runner:** `scripts/frontier_single_axiom_information.py`

**Scope note:** this is an operational support note for framework
compression and physical-lattice scoping. It is not the load-bearing
accepted-input ledger for the current paper package, whose framework
statement remains the physical `Cl(3)` local algebra on the `Z^3`
spatial substrate with the package boundary recorded in
[`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md).

## Audit boundary (2026-05-10 refresh of prior 2026-05-05 feedback)

The 2026-05-05 independent audit on the previous note revision recorded
a renaming verdict (load-bearing-step class F, criticality `critical`,
transitive descendants 266). The audit's `chain_closure_explanation`:

> *The runner and note assume the load-bearing sparse Hermitian H,
> then verify standard consequences: support gives a graph, Hermitian
> exponentiation is unitary, and the Schrodinger current is conserved.
> The missing step is a derivation that the verbal axiom uniquely or
> necessarily entails sparsity, Hermiticity, locality, and the specific
> Hamiltonian structure rather than defining them into H.*

The audit's `verdict_rationale`:

> *The numerical checks are mostly algebraic or model-demonstration
> checks after H has already been chosen as sparse and Hermitian. They
> do not derive the graph-unitary object from the single verbal axiom;
> they rename the original graph-plus-unitary package as conserved
> information flow and show familiar properties of that representation.
> Test 2 and Test 3 add self-consistency claims about locality and
> unitarity, but these rely on chosen graph models and imposed
> dissipative factors rather than closing a first-principles
> derivation.*

The audit's `notes_for_re_audit_if_any`:

> *A second auditor should re-check whether class F should instead be
> class E; either classification stays a renaming boundary rather than
> full closure.*

This note adopts the explicit class-F definitional-renaming framing.
The four named admitted inputs are listed in §"Admitted-context inputs"
below; each is a real upstream input, not a derivation. The
load-bearing step is `(admitted inputs) ⇒ four numerical consequences`,
evaluated mechanically by the runner.

**Admitted-context inputs (not derived in this note):**

1. **Sparse Hermitian H.** The mathematical realization is taken to be
   a sparse Hermitian operator `H` on a finite set. Sparsity is an
   admitted input (Test 2 below tests locality empirically on three
   chosen graph types; it does not derive sparsity from "conserved
   information flow"). Hermiticity is an admitted input (Test 3 below
   tests unitarity by **imposing** a non-zero dissipation rate `γ` and
   comparing against the `γ = 0` Hermitian baseline; it does not
   derive Hermiticity from "without being created or destroyed").
2. **Hermitian-exponentiation readout.** The unitary `U = exp(iHt)`
   and the probability current `J_ij = 2 Im(ψ_i* H_ij ψ_j)` are read
   off mechanically from `H`. The convention is admitted; it is not
   derived from the verbal axiom.
3. **"Hamiltonian-support = graph edges" extraction rule.** Test 1's
   "graph emerges from H" claim uses the admitted convention that the
   nonzero pattern of `H` **defines** the edges. This is a graph-
   extraction convention, not a derived consequence of conserved
   information flow.
4. **Locality probe choice.** Test 2 probes three graph types (3D
   cubic lattice, complete graph, random Erdős-Rényi). The conclusion
   "locality is forced" is a comparative empirical observation across
   these chosen models, not a first-principles derivation that `H`
   must be sparse from the verbal axiom.

**Cited authorities (cited as related, not as authority closure):**

- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) — the
  load-bearing accepted-input ledger for the current paper package
  (physical `Cl(3)` local algebra on the `Z^3` spatial substrate).
  Cited as the non-superseded framework surface.
- [`SINGLE_AXIOM_HILBERT_NOTE.md`](SINGLE_AXIOM_HILBERT_NOTE.md) — the
  sibling `audited_renaming` operational note that records the same
  class of definitional-compression boundary on the local-tensor-
  product Hilbert space framing. Cited as a sibling renaming surface,
  not as authority closure.

## The claim (scope-narrowed)

The two axioms of the model (graph substrate + unitary dynamics) are
**operationally unified** — i.e. **renamed** — into a single verbal
axiom:

> "There exist distinguishable things, and information flows between them
> without being created or destroyed."

- "Distinguishable things" provides the **labels** `i ∈ S` for the
  admitted finite state set.
- "Flows between them" provides the **interpretation** of the admitted
  sparse Hermitian `H`'s nonzero pattern as edges.
- "Without being created or destroyed" provides the **interpretation**
  of the admitted Hermiticity as norm preservation.

The mathematical realization (admitted, not derived): a sparse
Hermitian operator `H` on a finite set, with the Hermitian-
exponentiation readout convention `U = exp(iHt)` and the Schrödinger
current `J_ij = 2 Im(ψ_i* H_ij ψ_j)`. **This is not** a derivation
that the verbal axiom uniquely or necessarily entails sparsity,
Hermiticity, locality, or the specific Hamiltonian structure. It is a
class-F definitional renaming of the graph-plus-unitary package, with
the four admitted inputs listed above bearing the load.

## What was tested

### Test 1: Numerical consequences of the admitted sparse Hermitian H

Start with the **admitted** sparse real symmetric matrix `H` on `N`
states (admitted-context inputs 1, 2, 3 above). The runner verifies
mechanically that the admitted "support = edges" extraction rule
recovers a graph, that Hermitian exponentiation produces a unitary
to machine precision, and that the Schrödinger current is locally
conserved.

| N  | Unitarity err  | Conservation err | Locality ratio |
|----|---------------|-----------------|----------------|
| 8  | 2.2e-16       | 5.6e-17         | 10.7x          |
| 16 | 2.2e-16       | 1.4e-17         | 20.9x          |
| 32 | 5.6e-16       | 6.9e-18         | 54.4x          |
| 64 | 4.4e-16       | 1.7e-18         | 154.4x         |

- exp(iHt) is unitary to machine precision (admitted Hermitian H plus
  admitted Hermitian-exponentiation readout ⇒ unitary, mechanically).
- The probability current `J_ij = 2 Im(ψ_i* H_ij ψ_j)` satisfies
  local conservation to machine precision **under the admitted readout
  convention**.
- The unitary `U` is concentrated on graph edges (under the admitted
  "support = edges" extraction rule): the locality ratio (mean `|U_ij|`
  on-graph vs off-graph) grows with `N`, reaching 154x at `N = 64`.

The admitted sparse Hermitian `H`, together with the admitted readout
and extraction conventions, mechanically produces graph + current +
unitary representations. This is a definitional renaming, **not** a
first-principles derivation of `H`'s sparsity or Hermiticity from the
verbal axiom.

### Test 2: Locality comparator

Poisson field on three graph types:

| Graph type          | phi(r) exponent | Clean power law? |
|--------------------|----------------|-----------------|
| 3D cubic lattice    | -1.80          | Yes (finite-size steepened) |
| Complete graph      | flat (0.0)     | No: only 2 distinct values |
| Random Erdos-Renyi  | -1.32          | No: residual 0.83 |

The fully-connected graph has no notion of distance: the Poisson equation
gives a flat potential (all non-source nodes equivalent). Only the
geometrically-local lattice produces a 1/r-like field with attraction.

### Test 3: Dissipation comparator

Dissipative per-hop loss (gamma) applied to the Poisson field:

| gamma | M_eff CV | Effective alpha | Norm at 10 hops |
|-------|----------|----------------|-----------------|
| 0.00  | 0.34     | -1.82          | 1.000           |
| 0.02  | 0.37     | -1.90          | 0.668           |
| 0.05  | 0.41     | -2.02          | 0.358           |
| 0.10  | 0.49     | -2.21          | 0.122           |
| 0.30  | 0.77     | -3.01          | 0.001           |

Dissipation steepens the effective power law from -1.8 toward -3.0 and
doubles the variation of M_eff(r) = phi(r) * r. The "mass seen at distance r"
becomes distance-dependent, breaking beta = 1. Unitarity is required for the
mass law to hold.

### Test 4: (G, U) is irreducible

Three topologies with 64 nodes each:

| Topology    | Bandwidth | Min gap  | P(0->0) | Participation |
|-------------|-----------|----------|---------|---------------|
| 1D chain    | 4.00      | 0.0070   | 0.333   | 2.6 sites     |
| 2D lattice  | 7.52      | 0.0419   | 0.111   | 6.9 sites     |
| 3D lattice  | 9.71      | 0.2361   | 0.037   | 18.0 sites    |

- Pairwise spectral distances: 0.31 to 0.57 (all > 0).
- Adding one weak edge to the 3D lattice shifts the spectrum by 0.009
  and changes the propagator by up to 0.11.
- Fidelity of 1D evolution vs 3D evolution: 0.11 (far from 1.0).
  U from one graph produces wrong physics on another.

The pair (G, U) cannot be factored: changing G changes U, and vice versa.

## The renamed object

Under the four admitted-context inputs, the "graph-unitary" (`G`, `U`)
package is **operationally renamed** as a single mathematical object:
a sparse Hermitian operator `H` on a finite set `S`. From the admitted
`H` together with the admitted readout and extraction conventions:

1. **Graph**: the nonzero pattern of `H` defines edges (under the
   admitted "support = edges" extraction rule).
2. **Unitary**: `exp(iHt)` is unitary (admitted Hermitian-exponentiation
   readout).
3. **Current**: `J_ij = 2 Im(ψ_i* H_ij ψ_j)` is locally conserved
   (admitted readout).
4. **Locality**: for small `t`, `U` inherits the admitted sparsity.
5. **Physics**: the spectrum of `H` determines the observables read out
   under the admitted convention.

This is a definitional renaming of the original two-axiom package
(graph + unitary) into a single verbal axiom plus four admitted
auxiliary inputs. The renaming is class-F (audit-recorded), with the
admitted inputs bearing the load. The verbal axiom alone does **not**
force sparsity, Hermiticity, locality, or the specific Hamiltonian
structure.

## What this is

A numerical demonstration that, given the four admitted inputs above,
the phrase "conserved information flow on a network" can be used as a
single verbal renaming of the graph-plus-unitary package. Under the
admitted inputs, the runner verifies four numerical consequences:

- A graph (from the admitted "Hamiltonian-support = edges" extraction
  rule applied to the admitted sparse `H`)
- Unitary dynamics (from the admitted Hermiticity of `H` plus the
  admitted Hermitian-exponentiation readout convention)
- Locality (from the admitted sparsity, probed empirically across
  three chosen graph models)

The four tests confirm that, **inside the admitted-input scope**,
removing any component (the graph, the unitarity, or the coupling
between them) breaks the operational consequences.

## What this is not (audit-boundary recording)

- This is not a proof that `H` must be sparse from the verbal axiom
  alone (sparsity is an admitted input; Test 2 probes locality
  empirically across three chosen graph types, it does not derive
  sparsity from "conserved information flow").
- This is not a proof that `H` must be Hermitian from the verbal axiom
  alone (Hermiticity is an admitted input; Test 3 imposes a non-zero
  dissipation rate to compare against the Hermitian baseline, it does
  not derive Hermiticity from "without being created or destroyed").
- This is not a proof that the "Hamiltonian-support = edges" extraction
  rule is the unique graph-extraction convention forced by the verbal
  axiom (this is an admitted convention used by Test 1).
- This is not a proof that the Hermitian-exponentiation readout
  convention is forced by the verbal axiom (this is an admitted
  readout convention).
- The finite-size steepening of `α` (`-1.8` at `N = 24` vs `-1.0` at
  `N → ∞`) is a known lattice artifact, not a failure of the argument.
- The construction assumes finite-dimensional Hilbert space. Extension
  to infinite dimensions requires additional care.
- This note does **not** modify the parent audit-ledger row, **does
  not** promote any current or prior audit verdict,
  **does not** derive sparsity, Hermiticity, locality, or the specific
  Hamiltonian structure from the verbal axiom alone, and **does not**
  extend the audited scope beyond the class-F definitional-renaming
  framing.
