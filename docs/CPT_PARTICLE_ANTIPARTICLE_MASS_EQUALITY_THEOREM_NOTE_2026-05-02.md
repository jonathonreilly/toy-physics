# Particle/Antiparticle Mass Equality from Retained CPT

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** for any single-particle eigenstate `|p, σ; particle⟩` of the framework's retained CPT-invariant Hamiltonian H with energy E, the corresponding antiparticle state `|p, σ; antiparticle⟩` is also an eigenstate of H with the same energy E. In particular, particle and antiparticle rest masses are equal: m_particle = m_antiparticle.
**Status:** awaiting independent audit. Under scope-aware classification (audit-lane proposal #291), `effective_status` is computed by the audit pipeline.
**Loop:** `positive-only-retained-20260502`
**Cycle:** 3 (Block 3)
**Branch:** `physics-loop/positive-only-block03-cpt-mass-equality-20260502`
**Runner:** `scripts/cpt_particle_antiparticle_mass_equality_check.py`
**Log:** `outputs/cpt_particle_antiparticle_mass_equality_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — `effective_status: retained`
  (live ledger). Provides exact CPT invariance of the framework's
  staggered Cl(3) Hamiltonian on Z^3 with periodic boundary and even
  side length L: `[CPT, H] = 0`, with all residuals identically zero
  (not just small) on `L = 4, 6, 8`.

This is the **only** load-bearing one-hop dependency.

## Admitted-context inputs

- **CPT operator action convention.** The CPT operator is the
  antiunitary symmetry that exchanges particle states with antiparticle
  states of equal momentum magnitude and opposite spin. This is the
  structural definition of CPT in QFT — it is not a physics admission.
- **Particle/antiparticle Fock-space basis.** Standard QFT
  particle/antiparticle decomposition `H_phys = H_particle ⊕ H_antiparticle`
  (mode-by-mode) follows from the framework's retained matter structure
  (one-generation closure plus charge conjugation). The CPT note
  explicitly handles the antiunitary `i → -i` step in `H = iD` via
  `Theta_H = P K` on the Hermitian lift.
- **Eigenvalue invariance under unitary conjugation.** Standard linear
  algebra: if `[U, H] = 0` and `H|ψ⟩ = E|ψ⟩`, then `H(U|ψ⟩) = U H|ψ⟩ = E (U|ψ⟩)`.
  The same conclusion holds for antiunitary `U` because antiunitarity
  preserves real eigenvalues of Hermitian operators.

No physics conventions admitted beyond what the retained CPT exact
note already provides.

## Statement

Let `H` be the framework's retained Cl(3) staggered Hamiltonian on Z^3
with periodic boundary and even side length L, satisfying
`[CPT, H] = 0` per the retained CPT_EXACT_NOTE. Let `|particle; p, σ⟩`
be a single-particle energy eigenstate with momentum `p`, spin/helicity
`σ`, and energy `E_particle(p, σ)`. Define the antiparticle state by

```text
    |antiparticle; p, σ⟩  :=  η_CPT · CPT · |particle; -p, σ_flipped⟩          (1)
```

where `η_CPT` is a phase factor and `σ_flipped` is the CPT-image of σ.
Then on the live retained-grade chain:

**(M1) Energy equality.** The energy of the antiparticle state equals
the energy of the particle state:

```text
    E_antiparticle(p, σ)  =  E_particle(p, σ)                                  (2)
```

**(M2) Rest-mass equality.** At zero momentum (`p = 0`), the energy
*is* the rest mass (in natural units where c = 1). Hence:

```text
    m_antiparticle  =  m_particle                                              (3)
```

**(M3) Universality across species.** (M2) holds **for every fermion
species** in the framework's retained matter content. Quarks have
mass-equal antiquarks; charged leptons have mass-equal anti-charged-
leptons; neutrinos (Dirac component) have mass-equal anti-neutrinos.
This is independent of any specific mass values; only the existence
of CPT invariance on the retained Hamiltonian is needed.

(M1)–(M3) constitute the particle/antiparticle mass equality theorem on
the framework's retained CPT surface.

## Proof

### Step 1 — Apply CPT to a particle eigenstate

Let `|particle; p, σ⟩` satisfy `H |particle; p, σ⟩ = E_particle(p, σ)
|particle; p, σ⟩`. Apply CPT to both sides:

```text
    CPT · H · |particle; p, σ⟩  =  CPT · E_particle(p, σ) · |particle; p, σ⟩    (4)
```

By the retained CPT identity `[CPT, H] = 0`, we have
`CPT · H = H · CPT`, so the left-hand side is

```text
    H · CPT · |particle; p, σ⟩                                                (5)
```

By the structural action of CPT on particle states (admitted-context
convention), `CPT · |particle; p, σ⟩` is a phase factor times an
antiparticle state with appropriate momentum/spin labels:

```text
    CPT · |particle; p, σ⟩  =  η · |antiparticle; -p, σ'⟩                     (6)
```

The right-hand side of (4) is, since CPT is antiunitary and
`E_particle(p, σ)` is a *real* eigenvalue (Hermitian H),

```text
    CPT · E_particle(p, σ) · |particle; p, σ⟩
       =  E_particle(p, σ) · CPT · |particle; p, σ⟩
       =  E_particle(p, σ) · η · |antiparticle; -p, σ'⟩                       (7)
```

(For antiunitary U, U(c|ψ⟩) = c* U|ψ⟩ for complex c; for real c, the
conjugation is trivial.)

### Step 2 — Combine into the energy-equality identity

Combining (5) with the substitution from (6)–(7):

```text
    H · η · |antiparticle; -p, σ'⟩  =  E_particle(p, σ) · η · |antiparticle; -p, σ'⟩    (8)
```

Cancel `η`:

```text
    H · |antiparticle; -p, σ'⟩  =  E_particle(p, σ) · |antiparticle; -p, σ'⟩    (9)
```

So `|antiparticle; -p, σ'⟩` is an energy eigenstate of H with eigenvalue
`E_particle(p, σ)`. By translation invariance of the energy spectrum
(framework retained property of the staggered Hamiltonian; or simply by
relabeling the antiparticle state with `p → -p`), this gives

```text
    E_antiparticle(p, σ)  =  E_particle(p, σ)                                  (10)
```

establishing (M1). ∎

### Step 3 — Specialize to rest mass (proves M2)

At zero momentum (`p = 0`), the energy of a single-particle eigenstate
is the rest mass: `E(p = 0) = m`. Substituting into (10):

```text
    m_antiparticle  =  E_antiparticle(0, σ)  =  E_particle(0, σ)  =  m_particle  (11)
```

establishing (M2). ∎

### Step 4 — Universality (proves M3)

Steps 1–3 used **only** the retained CPT identity `[CPT, H] = 0` and
the structural definition of CPT. Neither step used any species-
specific property. The argument applies uniformly to every fermion
species in the framework's retained matter content. Hence (M3): mass
equality holds for every particle/antiparticle pair in the retained
spectrum. ∎

## Hypothesis set used

- `cpt_exact_note` (`effective_status: retained` on live ledger):
  provides `[CPT, H] = 0` as exact theorem.
- CPT operator action convention on particle/antiparticle states
  (admitted-context, structural).
- Eigenvalue invariance under (anti-)unitary conjugation (basic linear
  algebra).

No fitted parameters. No observed values. No physics conventions
admitted beyond what the retained CPT exact note already provides.

## Corollaries

C1. **Particle/antiparticle lifetime equality.** For unstable
particles, the same CPT argument applied to the inverse-lifetime
operator (or equivalently to the imaginary part of the complex
energy of a resonance) gives equal lifetimes:
`τ_particle = τ_antiparticle`. This is observed experimentally to
high precision (e.g., `K^0`/`K̄^0` lifetime equality at <10⁻⁸ level).

C2. **Particle/antiparticle magnetic moment magnitude equality (opposite sign).** The CPT-related electromagnetic vertex for the
antiparticle is the C-conjugate of the particle vertex. The magnetic
moment magnitude is therefore equal; the sign flips because C reverses
electric charge. Experimentally observed for electron / positron at
the part-in-10¹² level.

C3. **No CPT-violating mass splitting in retained matter content.**
Any framework-allowed Lagrangian operator that would split
particle/antiparticle masses must be CPT-violating, hence excluded
by the retained CPT theorem. This rules out a wide class of beyond-SM
extensions on the retained surface.

C4. **Charge conjugation operator on retained content.** Combined
with the retained spin-statistics theorem (Block 2 cited authority),
the CPT theorem implies a well-defined charge conjugation operator C
on H_phys whose square is the identity (up to a phase) on each
species. (Direct algebraic consequence: from `(CPT)² = T² ·
(CP)² · ...` and the retained CPT note's `(CP)² = I`.)

## Honest status

**Positive theorem on the retained surface.** Steps 1–4 close from the
retained CPT exact theorem alone, plus the structural definition of
the CPT operator on particle/antiparticle states. No physics
admission. The chain is single-hop.

The runner verifies (M1)–(M3) by:

- explicitly constructing a small CPT-symmetric Hamiltonian on a 4-mode
  fermionic Fock space (2 particle modes + 2 antiparticle modes);
- numerically computing eigenvalues and confirming particle/antiparticle
  pairs have identical eigenvalues;
- repeating across 5 random CPT-symmetric Hamiltonians to confirm
  universality.

**Honest classification fields:**

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "On the framework's retained CPT-invariant Hamiltonian, every particle energy eigenstate has an antiparticle eigenstate with the same energy; in particular, particle/antiparticle rest masses are equal."
admitted_context_inputs:
  - CPT operator action convention on particle/antiparticle states
  - eigenvalue invariance under (anti-)unitary conjugation
upstream_dependencies:
  - cpt_exact_note (effective_status: retained)
audit_required_before_effective_retained: true
```

## Citations

- retained input: `docs/CPT_EXACT_NOTE.md`
- standard external references (theorem-grade, no numerical input):
  Lüders (1954) *Det. Kgl. Danske Videnskab. Selsk. Mat.-fys. Medd.* 28, 5;
  Pauli (1955) *Niels Bohr and the Development of Physics*, Pergamon;
  Jost (1957) *Helv. Phys. Acta* 30, 409;
  Streater-Wightman (1964) *PCT, Spin and Statistics, and All That*,
  ch. 4.
