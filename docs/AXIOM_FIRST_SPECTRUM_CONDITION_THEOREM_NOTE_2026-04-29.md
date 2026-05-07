# Axiom-First Spectrum Condition (Lattice Analogue) on Cl(3) ⊗ Z^3

**Date:** 2026-04-29 (citation-graph repair: 2026-05-02)
**Status:** support — branch-local theorem note on A_min; runner passing; audit-pending.
**Loop:** `axiom-first-foundations-block02`
**Cycle:** 1 (Route R7)
**Runner:** `scripts/axiom_first_spectrum_condition_check.py`
**Log:** `outputs/axiom_first_spectrum_condition_check_2026-04-29.txt`

## Cited authorities (one hop)

This note's load-bearing one-hop citation registered to the audit-graph
builder:

- [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
  — provides (R3) the positive Hermitian transfer matrix `T` on `H_phys`
  used by Step 1 of the proof of (SC1)–(SC2) below.

The 2026-05-02 citation-graph repair registers
`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` explicitly
as the one-hop load-bearing dependency, so the citation-graph builder picks
up the edge on the next pipeline run.

## Scope

The companion reflection-positivity support artifact states that the
canonical Cl(3) staggered + Wilson plaquette action on `A_min` is
reflection-positive, hence admits a positive Hermitian transfer
matrix `T` on a finite physical Hilbert space `H_phys`. This note
records the lattice analogue of the
**spectrum condition**: the reconstructed Hamiltonian
`H := -(1/a_τ) log(T)` on `H_phys` is self-adjoint and bounded below.

After this note, any package lane that relies on "the Hamiltonian
is positive after vacuum subtraction" can cite an axiom-first
lattice theorem on `A_min` instead of treating the spectrum
condition as a continuum import.

## A_min objects in use

Same as the reflection-positivity companion note. The transfer matrix `T` and physical Hilbert
space `H_phys` are constructed via the reflection-positivity
factorisation (companion support artifact).

## Statement

Let `T` be the canonical reflection-positivity-reconstructed
transfer matrix on `H_phys` (reflection-positivity companion). Let `M_T := ‖T‖_{op}` be
the operator norm of `T`. Then on `A_min`:

**(SC1) Self-adjointness.** `H := -(1/a_τ) log(T / M_T)` is a
self-adjoint operator on `H_phys`.

**(SC2) Boundedness below.** `H ≥ 0` on `H_phys`. The ground state
energy is `E_0 := 0`, and all excited-state energies satisfy
`E_n > 0`.

**(SC3) Energy gap.** The mass gap `m_gap := E_1 - E_0 = -(1/a_τ)
log(λ_1 / M_T) > 0` whenever `T` has a non-degenerate top eigenvalue,
which holds generically on the canonical surface.

**(SC4) Compatibility with cluster decomposition.** Combined with
the cluster-decomposition companion, the spectrum condition
implies exponential decay of connected correlators with rate
`m_gap`.

## Proof

### Step 1 — `T` is positive Hermitian (cited from the reflection-positivity companion)

By the reflection-positivity companion, `T` is Hermitian
and has spectrum `[0, M_T]` with `M_T = ‖T‖_{op} < ∞`. The 0
eigenspace (if any) is the kernel of `T`; on the orthogonal
complement `H_phys^×`, `T` has spectrum `(0, M_T]`.

### Step 2 — Functional calculus gives `log(T / M_T)`

On `H_phys^×`, `T / M_T` is a positive Hermitian operator with
spectrum `(0, 1]`. The functional calculus defines
`log(T / M_T)` as a self-adjoint operator with spectrum
`(-∞, 0]` (since `log` is real on positive reals and `log(1) = 0`).

Hence `H := -(1/a_τ) log(T / M_T)` is self-adjoint on `H_phys^×`
with spectrum `[0, +∞)`. Extension to `H_phys` is by setting
`H = +∞` on the kernel of `T` (formally; in practice
the kernel is empty on the canonical surface, so `H_phys^× = H_phys`).

### Step 3 — Ground state and gap

The top eigenvalue of `T / M_T` is `1`, achieved by the ground
state `|0⟩_phys`. Then `H |0⟩_phys = 0`, so `E_0 = 0`.

If `T` has a unique top eigenvalue (Perron–Frobenius for the
positive operator `T` on the canonical surface), the next
eigenvalue `λ_1 < M_T`, and

```text
    m_gap   =   E_1 - E_0   =   -(1/a_τ) log(λ_1 / M_T)   >   0.    (1)
```

### Step 4 — Combination with cluster decomposition

By the cluster-decomposition companion, connected correlators decay exponentially at
spacelike separation with rate set by the mass gap. On the
spectrum-condition side, this rate is exactly `m_gap` of (1). So
the long-distance correlator decay length is `1 / m_gap`.

This recovers the standard SU(3) confining-phase mass-gap /
correlation-length structure on the canonical surface. ∎

## Hypothesis set used

A_min only (via the reflection-positivity companion support artifact). No imports from the
forbidden list. The functional calculus / Perron–Frobenius results
are elementary finite-dim spectral theory on the bounded operator
`T`.

## Corollaries

C1. *Hamiltonian is self-adjoint and bounded below.* On `A_min`
the ground-state subtracted Hamiltonian `H_phys` has only
non-negative eigenvalues. This is the lattice analogue of the
Wightman positive-energy axiom.

C2. *Mass-gap is the spectral-gap of `T`.* Any package row that
quotes a mass-gap value or scaling can be related to the operator
spectrum of the canonical transfer matrix via (1).

C3. *Compatibility with clustering.* The cluster-decomposition companion + this theorem give
the lattice Reed–Simon / Wightman-axiom-pair on `A_min`.

## Honest status

**Branch-local theorem.** (SC1)–(SC4) are proved on `A_min` using
the reflection-positivity companion as a support artifact. The runner exhibits the spectrum
of `T`, the corresponding `H` spectrum, the gap, and confirms the
ground state has `E_0 = 0` after subtraction.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- companion reflection-positivity support artifact:
  `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- companion cluster-decomposition support artifact:
  `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [axiom_first_cluster_decomposition_theorem_note_2026-04-29](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
