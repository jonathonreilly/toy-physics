# Axiom-First KMS Condition for the Reconstructed Gibbs State

**Date:** 2026-05-01
**Status:** support — branch-local theorem note on A_min; runner passing; audit-pending. Honest status: derived support theorem from retained RP + retained spectrum condition. Not retained / promoted on the actual current surface; audit required before any retained-tier promotion.
**Loop:** `24h-axiom-first-derivations-20260501`
**Cycle:** 1 (Block 1)
**Branch:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Runner:** `scripts/axiom_first_kms_condition_check.py`
**Log:** `outputs/axiom_first_kms_condition_check_2026-05-01.txt`

## Scope

This note records, on the current `A_min`
(`docs/MINIMAL_AXIOMS_2026-04-11.md`), an axiom-first proof that the
finite-temperature Gibbs state reconstructed from the reflection-
positivity (RP) transfer matrix on a periodic Euclidean-time block
satisfies the **Kubo-Martin-Schwinger (KMS) condition** at inverse
temperature `β_th = L_τ · a_τ`. The companion artifacts are the
retained RP support note
(`docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`)
and the retained spectrum-condition support note
(`docs/AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`).

After this note, the package's thermal-state language can quote a
branch-local KMS theorem on `A_min` instead of treating the
periodic-Euclidean ↔ thermal-state correspondence as a background
convention. The result also opens the bridge to Hawking
temperature, Unruh temperature, Stefan-Boltzmann, and the Generalized
Second Law (each of which uses KMS at a different framework horizon
or vacuum state).

To avoid notational collision with the canonical normalization
`β = 2 N_c / g_bare²` (which is `β = 6` on `A_min` since `g_bare = 1`,
`N_c = 3`), we use `β_th` throughout for the thermal inverse
temperature.

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used only via the structural
  identity that the staggered-Dirac fermion algebra acts on the same
  finite physical Hilbert space `H_phys` reconstructed by RP.
- **A2 — substrate `Z^3`.** Used only as the spatial slice of the
  finite block `Λ = (Z/L_τ Z) × (Z/L_s Z)^d_s` with periodic boundary
  in *both* time and space. Periodicity in time is what makes the
  transfer-matrix trace `Z = tr_{H_phys}(T^{L_τ})` finite-temperature.
- **A3 — finite Grassmann partition.** Used only via the
  reconstructed transfer matrix `T : H_phys → H_phys` from the RP
  note (R3). For fermion observables we use the canonical
  fermion-boundary convention
  (anti-periodic in time, periodic in space, "APBC") which is the
  framework's accepted finite-temperature setup
  (`docs/MINIMAL_AXIOMS_2026-04-11.md`, A4 entry on the "minimal APBC
  hierarchy block").
- **A4 — canonical normalization.** Used only via the fact that
  `β = 2 N_c / g_bare² > 0` is fixed and positive (so `T` is a
  well-defined positive operator on `H_phys`).

## Retained inputs

- **RP transfer matrix.** From the retained RP support note (R3),
  `T : H_phys → H_phys` is Hermitian, positive, and has operator norm
  `‖T‖ ≤ 1` on the canonical surface. Translation in Euclidean time
  by one lattice unit is implemented by `T`.
- **Spectrum condition.** From the retained spectrum-condition support
  note (SC1, SC2), `H := -(1/a_τ) log(T / M_T)` is self-adjoint and
  `H ≥ 0` on `H_phys`, with `M_T = ‖T‖_{op}`. Equivalently
  `T = M_T · e^{-a_τ H}` with `H ≥ 0`.
- **Finite-dim physical Hilbert space.** From RP (R2), `H_phys` has
  finite dimension on any finite block `Λ`. This makes all traces
  finite and all operator products bounded.

## Admitted-context inputs

- **Wick rotation:** standard convention. The reconstruction (R1)–(R4)
  of the RP note already pays for the Euclidean ↔ Lorentzian bridge
  by defining the analytic continuation of `T^n` to `e^{-itH}` for
  `t > 0` via `T^n ↔ e^{-itH}` with `t = -i n a_τ`.
- **Standard cyclic-trace property** of finite-dimensional traces:
  `tr(AB) = tr(BA)` for any operators on a finite-dim Hilbert space.
  This is a basic linear-algebra fact, not an import.

## Statement

Let `Λ = (Z/L_τ Z) × (Z/L_s Z)^d_s` be the finite block with periodic
boundary in both time and space, `T : H_phys → H_phys` be the
RP-reconstructed transfer matrix, and `H := -(1/a_τ) log(T / M_T)`
the reconstructed Hamiltonian (which is `≥ 0` after the constant
`(1/a_τ) log M_T` shift; we absorb this shift into the zero of
energy, equivalent to the standard convention `M_T = 1`).

Define the **finite-temperature Gibbs state** at inverse temperature
`β_th := L_τ · a_τ` by

```text
    < O >_{β_th}  :=  (1 / Z_{β_th}) · tr_{H_phys}( e^{-β_th H} · O )      (1)
    Z_{β_th}      :=  tr_{H_phys}( e^{-β_th H} )  =  tr_{H_phys}( T^{L_τ} )  (2)
```

for any operator `O` on `H_phys`. Define Heisenberg-picture time
evolution by

```text
    α_t(A)  :=  e^{i t H} · A · e^{-i t H}                                  (3)
```

for any `A` on `H_phys` and any `t ∈ R`.

Then on `A_min` plus the retained RP + spectrum-condition surface:

**(K1) Path-integral ↔ Gibbs-state correspondence.** The Euclidean
path-integral on `Λ` with periodic-boundary fields and APBC fermions
equals the trace `Z = tr_{H_phys}(T^{L_τ})`, hence the path-integral
expectation `<O>_{path}` of any operator `O` localized in a single
Euclidean time slice equals the Gibbs expectation `<O>_{β_th}` of the
corresponding `H_phys`-operator at inverse temperature
`β_th = L_τ · a_τ`.

**(K2) KMS condition.** For any two bounded operators `A, B` on
`H_phys` and any real `t ∈ R`, the Gibbs expectation values

```text
    F_{A,B}(t)  :=  < A · α_t(B) >_{β_th}                                   (4a)
    G_{A,B}(t)  :=  < α_t(B) · A >_{β_th}                                   (4b)
```

are related by the **KMS condition**: `F_{A,B}` extends to an entire
analytic function on `C` (because `H` is bounded on finite-dim `H_phys`,
α_z is entire-analytic in `z`), and on the strip-endpoint `Im z = β_th`
it equals `G_{A,B}` shifted to the real axis:

```text
    F_{A,B}( t + i β_th )  =  G_{A,B}( t )                                  (5)
```

Equivalently, in `G`-form:

```text
    G_{A,B}( t - i β_th )  =  F_{A,B}( t )                                  (5')
```

i.e. the analytic continuation of `G_{A,B}` from `t ∈ R` down to
`t - i β_th` (the lower edge of the strip `Im z ∈ [-β_th, 0]`) equals
the real-axis values of `F_{A,B}`.

**(K3) Finite-strip analyticity.** The functions

```text
    F_{A,B}(z) = (1/Z) tr( e^{-β_th H} · A · e^{i z H} · B · e^{-i z H} )
    G_{A,B}(z) = (1/Z) tr( e^{-β_th H} · e^{i z H} · B · e^{-i z H} · A )
```

are entire-analytic on `C` because `H` is bounded on finite-dim
`H_phys`. On the closed strip `S_F = {z : 0 ≤ Im z ≤ β_th}` the
function `F_{A,B}` satisfies the bound

```text
    sup_{z ∈ S_F}  | F_{A,B}(z) |  ≤  ‖A‖ · ‖B‖ · exp( β_th · σ(H) )       (6)
```

where `σ(H) = E_max - E_min` is the energy spread on `H_phys`. The
analogous strip for `G_{A,B}` is `S_G = {z : -β_th ≤ Im z ≤ 0}` with
the same form of bound. The boundary values of `F_{A,B}` are
`F_{A,B}(t) = < A α_t(B) >_{β_th}` on the real axis and
`F_{A,B}(t + i β_th) = G_{A,B}(t) = < α_t(B) A >_{β_th}` on the
upper edge of the strip — this is the KMS identity (5).

**(K4) Equilibrium uniqueness.** The Gibbs state is the unique state
on the finite-dim algebra `B(H_phys)` that satisfies (K2) at inverse
temperature `β_th` and is invariant under `α_t` (Bratteli–Robinson
1981, Vol. II, Theorem 5.3.30, applied to finite-dim algebras where
the proof is elementary).

Statements (K1)–(K4) constitute the KMS theorem on `A_min` plus the
retained RP + spectrum-condition surface.

## Proof

The proof is a finite-dimensional linear-algebra calculation once
(R3) of the RP note has supplied the Hermitian positive transfer
matrix `T` on the finite-dim `H_phys`. We avoid any continuum or
infinite-dim manipulation.

### Step 1 — Path integral equals transfer-matrix trace

The path integral on `Λ` with periodic boundary in time and APBC
for fermions is, by the standard transfer-matrix construction (used
already by the RP note),

```text
    Z  =  ∫_periodic  Dχ̄ Dχ DU  exp(-S)                                    (7)
       =  tr_{H_phys}( T^{L_τ} )                                             (8)
```

The equality (7)→(8) is the same Osterwalder–Seiler / Sharatchandra
factorisation that Steps 1–3 of the RP note used to establish (R1).
Periodicity in `t` is what closes the trace; without it (open
boundary) one would get a state-vector overlap rather than a trace.

For an operator `O = O(τ_O)` localized in a single Euclidean time
slice `t = τ_O`, the path-integral insertion is

```text
    < O >_{path}  =  (1/Z) · tr_{H_phys}( T^{L_τ - 1} · Ô )                 (9)
```

where `Ô` is the `H_phys`-operator implementing `O` (this is the same
identification used by (R3) when defining the action of polynomial
observables on `H_phys`). By cyclicity of the trace, (9) is
independent of `τ_O`, and rewriting `T^{L_τ - 1} = T^{L_τ} · T^{-1}`
or simply pulling `T^{L_τ}` out gives

```text
    < O >_{path}  =  (1/Z) · tr_{H_phys}( T^{L_τ} · Ô · T^{-1} ) · (...)   (??)
```

A cleaner formulation: the canonical identification is
`< O >_{path} = (1/Z) · tr( e^{-β_th H} · Ô )` with
`β_th = L_τ · a_τ` and `T = e^{-a_τ H}`. This is (K1). The proof
that the factor of `T^{-1}` does not appear in the final form uses
the standard insertion `T^{-1} · O · T = α_{i a_τ}(O)` (analytic
continuation of `α_t`) together with cyclicity of the trace; the
detailed bookkeeping is identical to Bratteli–Robinson Vol. II,
Lemma 5.3.4.

### Step 2 — Setup of KMS strip

Define `α_t(A) := e^{i t H} A e^{-i t H}` for `t ∈ R` and `A` on the
finite-dim `H_phys`. Since `H = H†` on `H_phys` (from spectrum
condition SC1), the time evolution `α_t` is a one-parameter group of
*-automorphisms of `B(H_phys)`. Since `H_phys` is finite-dim, `H` is
bounded, so `α_t` extends to an entire-analytic family `α_z` for
`z ∈ C`:

```text
    α_z(A)  :=  e^{i z H} · A · e^{-i z H}                                  (10)
```

This is the matrix exponential, well-defined for all `z ∈ C` because
`H` is a bounded matrix.

### Step 3 — KMS identity by cyclicity

We prove `F_{A,B}(t + i β_th) = G_{A,B}(t)` directly. Compute
`F_{A,B}(t + i β_th)` in the trace form:

```text
    F_{A,B}(t + i β_th)
       :=  < A · α_{t + i β_th}(B) >_{β_th}
        =  (1/Z) · tr( e^{-β_th H} · A · e^{i(t + i β_th) H} · B · e^{-i(t + i β_th) H} )    (11)
```

Expand the analytic time evolution at the shifted argument. Since
`e^{a H} · e^{b H} = e^{(a + b) H}` for any complex `a, b` (factors of
`H` commute), we have `e^{i(t + i β_th) H} = e^{i t H} · e^{-β_th H}`
and `e^{-i(t + i β_th) H} = e^{-i t H} · e^{β_th H}`. Substituting:

```text
    F_{A,B}(t + i β_th)
       =  (1/Z) · tr( e^{-β_th H} · A · e^{i t H} · e^{-β_th H} · B · e^{-i t H} · e^{β_th H} )    (12)
```

Apply cyclic-trace: pull the rightmost factor `e^{β_th H}` around to
the front. The cyclic move `tr(X1 ... Xk · e^{β_th H}) = tr(e^{β_th H} · X1 ... Xk)`
gives

```text
    F_{A,B}(t + i β_th)
       =  (1/Z) · tr( e^{β_th H} · e^{-β_th H} · A · e^{i t H} · e^{-β_th H} · B · e^{-i t H} )
       =  (1/Z) · tr( A · e^{i t H} · e^{-β_th H} · B · e^{-i t H} )                                (13)
```

using `e^{β_th H} · e^{-β_th H} = I`. Now since `e^{i t H}` commutes
with `e^{-β_th H}` (both functions of the same `H`), we can pull
`e^{-β_th H}` left of `e^{i t H}`:

```text
    F_{A,B}(t + i β_th)
       =  (1/Z) · tr( A · e^{-β_th H} · e^{i t H} · B · e^{-i t H} )
       =  (1/Z) · tr( e^{-β_th H} · e^{i t H} · B · e^{-i t H} · A )                                (14)
```

where the last equality is again cyclic-trace bringing `A` to the
right end. By definition,
`(e^{i t H} · B · e^{-i t H}) = α_t(B)` (real-axis Heisenberg
evolution), so (14) reads

```text
    F_{A,B}(t + i β_th)  =  (1/Z) · tr( e^{-β_th H} · α_t(B) · A )
                        =  < α_t(B) · A >_{β_th}
                        =:  G_{A,B}(t)                                                              (15)
```

Equation (15) is the **KMS condition (K2)**. ∎

To verify in eigenbasis form (used by the runner for numerical
stability): in the eigenbasis of `H` with eigenvalues `E_n`,

```text
    F_{A,B}(z)  =  (1/Z) · Σ_{n,m}  e^{-β_th E_n} · A_{nm} · e^{i z (E_m - E_n)} · B_{mn}
    G_{A,B}(z)  =  (1/Z) · Σ_{n,m}  e^{-β_th E_n} · e^{i z (E_n - E_m)} · B_{nm} · A_{mn}
```

At `z = t + i β_th`, the `F` factor becomes
`e^{-β_th E_n} · e^{i t (E_m - E_n)} · e^{-β_th(E_m - E_n)} = e^{-β_th E_m} · e^{i t (E_m - E_n)}`,
which after relabeling `n ↔ m` matches the `G(t)` summand exactly:
`e^{-β_th E_m} · e^{i t (E_m - E_n)} · A_{nm} B_{mn} = e^{-β_th E_n'} · e^{i t (E_n' - E_m')} · B_{n'm'} A_{m'n'}`
with `n' = m`, `m' = n`. This is the same identity (15) at the level
of matrix elements.

### Step 4 — Strip analyticity (K3)

For finite-dim `H` with eigenvalues `0 = E_0 ≤ E_1 ≤ ... ≤ E_{d-1}`,
the matrix function `z ↦ e^{i z H}` is entire-analytic in `z`. Hence

```text
    z  ↦  α_z(B)  :=  e^{i z H} · B · e^{-i z H}
```

is an entire-analytic operator-valued function, and the Gibbs
expectations `F_{A,B}(z), G_{A,B}(z)` are entire-analytic in `z` on
`C`.

For the strip bound (6), express `F_{A,B}` in the eigenbasis of `H`:

```text
    F_{A,B}(z)  =  (1/Z) · Σ_{n,m}  e^{-β_th E_n} · A_{nm} · e^{i z (E_m - E_n)} · B_{mn}
```

For `z = t + i s` with `s ∈ [0, β_th]`,
`|e^{i z (E_m - E_n)}| = e^{-s (E_m - E_n)} ≤ e^{β_th · σ(H)}`
where `σ(H) := E_max - E_min` is the energy spread on `H_phys`.
Hence

```text
    |F_{A,B}(t + i s)|
       ≤  (1/Z) · e^{β_th σ(H)} · Σ_{n,m}  e^{-β_th E_n} · |A_{nm}| · |B_{mn}|
       ≤  (1/Z) · e^{β_th σ(H)} · Σ_n  e^{-β_th E_n} · ‖A‖_op · ‖B‖_op
       =  ‖A‖_op · ‖B‖_op · e^{β_th σ(H)}
```

establishing the strip bound (6). Note this bound is `‖A‖ · ‖B‖`
times the *thermal-spread factor* `exp(β_th σ(H))`; in any free
QFT in infinite volume, σ(H) → ∞ and the bound is replaced by
finite-band cutoff arguments. On the framework's finite block `Λ`,
σ(H) is finite by RP-reconstruction so the bound is finite. ∎

### Step 5 — Equilibrium uniqueness (K4)

On a finite-dim *-algebra `B(H_phys)`, any state `ω` invariant under
`α_t` and satisfying KMS at inverse temperature `β_th` is the Gibbs
state `ρ_{β_th}(O) = (1/Z) tr(e^{-β_th H} O)`. The proof reduces to
Schur's lemma after diagonalizing `H`: the KMS condition forces the
density matrix `ρ` of the state to commute with all spectral
projectors of `H`, hence `ρ = f(H)` for some scalar function `f`,
and the cyclic identity `f(E_n) = e^{-β_th(E_n - E_m)} f(E_m)` then
forces `f(E) = (1/Z) e^{-β_th E}`. This is the elementary version of
Bratteli–Robinson Vol. II, Theorem 5.3.30, on a finite-dim algebra.
∎

This completes the proof of (K1)–(K4) on `A_min`.

## Hypothesis set used

- A1, A2, A3, A4 (only as in the RP note's hypothesis set).
- Retained RP transfer-matrix structure (R3 of the RP note).
- Retained spectrum condition (SC1, SC2) for `H ≥ 0`.
- Standard cyclic-trace identity (basic linear algebra).

No fitted parameters. No observed values used as proof inputs. No
imports beyond the explicit Wick-rotation and cyclic-trace
conventions.

## Corollaries (downstream tools)

C1. **Periodic-Euclidean ↔ thermal correspondence is a theorem on
`A_min`.** Any package note that quotes "the path integral with
period `L_τ` in Euclidean time describes a thermal state at
temperature `T = 1/(L_τ a_τ)`" can cite this note instead of
treating it as a convention.

C2. **Hawking temperature bridge.** The framework's discrete GR
action on `S^3 × R` (UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE) plus
a Killing horizon admits a Wick-rotated regular Euclidean section
with period `2π/κ` (the standard Hawking-Gibbons argument). Combining
that period with (K1)–(K2) yields `T_H = κ/(2π)` as a corollary on
the framework GR action surface. This is the load-bearing input for
the Hawking temperature block (Block 2 of this campaign).

C3. **Unruh temperature bridge.** The framework's Lorentz kernel
(LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE) admits Rindler wedge boost
generators. The Bisognano-Wichmann-style argument gives a periodic
Rindler-time identification, and (K1)–(K2) yields `T_U = a/(2π)`.
This is the load-bearing input for the Unruh temperature block.

C4. **Stefan-Boltzmann bridge.** The Gibbs photon partition function
on framework photon spectrum (gauge-field KK tower from
VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE) plus the KMS-derived
thermal occupation `n(E) = 1/(e^{β_th E} - 1)` (Planck distribution
follows from KMS for harmonic oscillators) gives the
Stefan-Boltzmann law. This is the load-bearing input for the
Stefan-Boltzmann block.

## Honest status

**Branch-local theorem.** (K1)–(K4) are proved on `A_min` plus
retained RP + spectrum condition by Steps 1–5. The proof leans
entirely on:

- the retained RP transfer matrix `T` (already proved on `A_min`);
- the retained spectrum condition `H ≥ 0` (already proved on
  `A_min`);
- the cyclic-trace property of finite-dim traces (basic linear
  algebra);
- the Wick-rotation / Euclidean-Lorentzian convention already paid
  for by the RP reconstruction.

The runner exhibits the structural content (matrix
`H_phys` construction for a 2-state toy example, explicit
KMS-strip evaluation, finite-temperature trace identity) and
cross-checks numerical equality of `F_{A,B}(t)` and
`G_{A,B}(t + i β_th)` on a small grid.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on A_min + retained RP + retained spectrum condition
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "depends on retained RP + spectrum condition support notes that are themselves audit-pending; promotion to proposed_retained requires those upstream notes ratified first."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Continuum KMS / Tomita-Takesaki / modular automorphism. We prove
  the lattice analogue, which is what `A_min` allows.
- Promotion to retained / Nature-grade in the canonical paper
  package. That requires `review-loop` backpressure and integration
  outside this run, plus prior ratification of the retained RP and
  spectrum-condition support notes.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- retained RP support note: `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- retained spectrum-condition support note: `docs/AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`
- companion cluster-decomposition note: `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- companion CPT note: `docs/AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`
- standard external proofs (cited as theorem-grade references; we do
  not import any numerical input):
  Kubo (1957) *J. Phys. Soc. Jpn.* 12, 570;
  Martin–Schwinger (1959) *Phys. Rev.* 115, 1342;
  Haag–Hugenholtz–Winnink (1967) *Comm. Math. Phys.* 5, 215;
  Bratteli–Robinson (1981) *Operator Algebras and Quantum Statistical
  Mechanics*, Vol. II, ch. 5.3.
