# Mass-Gap Bridge for Cluster Decomposition on Cl(3) ⊗ Z^3

**Date:** 2026-05-09
**Status:** bounded support theorem — finite-block transfer-matrix gap lemma on A_min support inputs; runner passing; audit-pending.
**Type:** bounded support note
**Loop:** `axiom-first-foundations`
**Cycle:** rigorization repair for `axiom_first_cluster_decomposition_theorem_note_2026-04-29`
**Runner:** `scripts/cluster_decomposition_mass_gap_bridge_check.py`
**Log:** `outputs/cluster_decomposition_mass_gap_bridge_check_2026-05-09.txt`

## Why this note exists

The audit verdict on
`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
records that the parent note's L2 (exponential clustering of thermal
connected correlators) was promoted from L1 (Lieb–Robinson commutator
bound) plus an asserted mass-gap / confinement bridge:

> "L2 exponential clustering is promoted from LR plus an asserted
> mass gap/confinement bridge. LR bounds alone control commutators
> outside a light cone; they do not prove static connected-correlator
> clustering for arbitrary canonical thermal states, and the packet
> gives no retained mass-gap or confinement authority that closes
> the bridge from microcausality to thermal connected-correlator
> decay."

This note salvages the closed finite-block transfer-matrix lemma that
the parent note needs: if a normalized transfer matrix has a unique top
eigenvector and gap `Δ_T > 0`, then temporal ground-state connected
correlators decay as `exp(-n Δ_T)`. It also records the finite-
temperature bound with the explicit excited-state thermal weight. The
gap itself is not derived here, and this note does not close the parent
spatial cluster-decomposition claim.

## Scope

This note proves, on each finite block after importing the
reflection-positivity support artifact
`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
and the spectrum-condition support artifact
`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`,
the following **bounded conditional lemma**:

> **(B)** Let `T` be the canonical reflection-positivity-reconstructed
> transfer matrix on `H_phys` (finite-dim on every finite block `Λ`),
> with `M_T := λ_max(T) > 0` and second eigenvalue `λ_1`. Define the
> **spectral gap of the transfer matrix** as
>
> ```text
>     Δ_T  :=  -log(λ_1 / M_T)  ≥  0.                                      (B.1)
> ```
>
> If `Δ_T > 0` (the **mass-gap input**), then for any two local
> Cl(3)-algebra operators `A_x, B_y` supported at lattice sites
> `x, y ∈ Λ` with `x ≠ y` along the temporal direction at separation
> `n := |t_x - t_y|`, the connected ground-state correlator satisfies
>
> ```text
>     | ⟨A_x B_y⟩_0 - ⟨A_x⟩_0 ⟨B_y⟩_0 |   ≤   ‖A_x‖ · ‖B_y‖ · exp(-n · Δ_T).   (B.2)
> ```
>
> For the canonical thermal state `ρ_β = Z⁻¹ exp(-β H̃)` at any inverse
> temperature `0 < β < ∞`, define the excited-state population
>
> ```text
>     q_β := Tr(P_\perp exp(-β H̃)) / Tr(exp(-β H̃)).
> ```
>
> The temporal connected correlator satisfies the finite-block bound
>
> ```text
>     | ⟨A_x B_y⟩_β - ⟨A_x⟩_β ⟨B_y⟩_β |
>                                                                       (B.3)
>         ≤   ‖A_x‖ · ‖B_y‖ · ( exp(-n · Δ_T)  +  6 q_β )
> ```
>
> with `m_gap := Δ_T / a_τ` the Hamiltonian gap. Since
> `q_β ≤ (D-1) exp(-β m_gap)/(1 + (D-1) exp(-β m_gap))` on a
> `D`-dimensional finite block, this is a controlled low-temperature
> correction with the finite-block degeneracy made explicit. At zero
> temperature `β → ∞`, `q_β → 0` and (B.3) reduces to the ground-state
> form (B.2).

**(B) is a closed-form finite-dimensional spectral lemma.** No
assertion of `Δ_T > 0` is made by this note; the gap input is named
explicitly and the bridge is conditional on it. A purely spatial
cluster-decomposition theorem still requires either a retained
Hastings-Koma-style gap-plus-LR theorem with constants, a spatial
transfer-matrix argument, or another retained derivation.

## A_min objects in use

Same as the parent
`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`:
A1 (Cl(3) site algebra), A2 (Z^3 substrate), A3 (finite-range Hamiltonian
from staggered + Wilson), A4 (canonical normalization fixing the operator
norm of each interaction term).

## Inputs and support artifacts

- **Reflection positivity / transfer matrix.** From
  `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`,
  `T : H_phys → H_phys` is a positive Hermitian operator on a finite-
  dimensional Hilbert space `H_phys`, with `M_T := λ_max(T) < ∞` and
  `T = T†`.
- **Spectrum condition.** From
  `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`,
  the vacuum-energy-subtracted Hamiltonian
  `H̃ := -(1/a_τ) log(T / M_T)` is self-adjoint and `H̃ ≥ 0` on `H_phys`.
- **Lieb-Robinson bound (L1) on `A_min`.** From the parent
  `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`,
  `‖[A_x(t), B_y]‖ ≤ 2‖A‖‖B‖ exp(-(d - v_LR|t|)/ξ)` for finite-range
  Hermitian Hamiltonian on Cl(3) ⊗ Z^3. This input is cited for the
  parent dependency context only; the lemma proved below is temporal
  and does not itself prove spatial cluster decomposition.

## Statement of the bridge (formal version)

Let `T` be a positive Hermitian operator on a finite-dim Hilbert
space `H_phys`. Let `M_T := λ_max(T)` and let `λ_1 := λ_2(T)` (second
largest eigenvalue, counted with multiplicity beneath the top). Define
the dimensionless **transfer-matrix spectral gap**

```text
    Δ_T  :=  -log(λ_1 / M_T)                                              (B.5)
```

so that `Δ_T > 0` if and only if the top eigenvalue of `T` is
non-degenerate (Perron–Frobenius regime, isolated top eigenvalue).
Let `|0⟩ ∈ H_phys` be the unique unit-norm top eigenvector of `T`,
i.e. the ground state of `H̃`.

**(B) Bridge theorem (gap → clustering).** *Conditional on
`Δ_T > 0`, for any bounded operators `A, B` on `H_phys`*:

**(B.1) Ground-state temporal clustering.** For any integer
`n ≥ 1`,

```text
    ⟨0|  A · T̃^n · B  |0⟩  -  ⟨0|A|0⟩ ⟨0|B|0⟩
                                                         (B.6)
        =     Σ_{k ≥ 1}  (λ_k / M_T)^n  · ⟨0|A|k⟩ ⟨k|B|0⟩
```

where `{|k⟩}_{k ≥ 0}` is an orthonormal eigenbasis of `T̃ := T/M_T`
with eigenvalues `1 = (λ_0/M_T) > (λ_1/M_T) ≥ (λ_2/M_T) ≥ … ≥ 0`.
Hence

```text
    | ⟨A · T̃^n · B⟩_0 - ⟨A⟩_0 ⟨B⟩_0 |   ≤   ‖A‖ · ‖B‖ · exp(-n · Δ_T).   (B.7)
```

**(B.2) Finite-temperature temporal bound.** For any `0 < β < ∞`,
the canonical thermal state `ρ_β := Z⁻¹ exp(-β H̃)` satisfies

```text
    | ⟨A · T̃^n · B⟩_β - ⟨A⟩_β ⟨B⟩_β |
                                                                        (B.8)
        ≤   ‖A‖ · ‖B‖ · ( exp(-n · Δ_T)  +  6 q_β )
```

where `q_β := Tr(P_\perp exp(-β H̃)) / Tr(exp(-β H̃))` is the actual
excited-state population on the finite block. Equivalently, if
`D = dim H_phys`,

```text
    q_β ≤ (D-1) exp(-β m_gap) / (1 + (D-1) exp(-β m_gap)).                 (B.9)
```

At zero temperature (`β → ∞`), `q_β → 0` and (B.8) reduces to (B.7).

**Not proved here.** The lemma does not prove spatial cluster
decomposition. Turning the temporal transfer-matrix gap into a
spatial connected-correlator bound requires an additional retained
gap-plus-Lieb-Robinson theorem, a spatial transfer-matrix gap, or an
equivalent retained argument.

## Proof of (B)

### Step 1 — Spectral decomposition of T̃

`T̃ := T/M_T` is positive Hermitian on finite-dim `H_phys`, with
spectrum `{(λ_k/M_T)}` satisfying `1 = (λ_0/M_T) > (λ_1/M_T) ≥ … ≥ 0`
(strict inequality at the top by the assumption `Δ_T > 0`). By the
finite-dim spectral theorem,

```text
    T̃   =   Σ_{k ≥ 0}  (λ_k/M_T) · |k⟩⟨k|                                    (B.11)
```

with `|k⟩` an orthonormal eigenbasis. Powers:

```text
    T̃^n   =   Σ_{k ≥ 0}  (λ_k/M_T)^n · |k⟩⟨k|                                 (B.12)
```

### Step 2 — Ground-state temporal clustering (proves B.1)

For any operators `A, B` on `H_phys`,

```text
    ⟨0| A · T̃^n · B |0⟩
       =  Σ_{k ≥ 0}  (λ_k/M_T)^n · ⟨0|A|k⟩ · ⟨k|B|0⟩
                                                         (B.13)
       =  ⟨0|A|0⟩⟨0|B|0⟩  +  Σ_{k ≥ 1}  (λ_k/M_T)^n · ⟨0|A|k⟩⟨k|B|0⟩
```

This is exactly (B.6). For the bound (B.7):

```text
    | ⟨A · T̃^n · B⟩_0 - ⟨A⟩_0 ⟨B⟩_0 |
        =  | Σ_{k ≥ 1}  (λ_k/M_T)^n · ⟨0|A|k⟩⟨k|B|0⟩ |
        ≤  Σ_{k ≥ 1}  (λ_1/M_T)^n · |⟨0|A|k⟩| · |⟨k|B|0⟩|       (since (λ_k/M_T)^n ≤ (λ_1/M_T)^n)
        ≤  (λ_1/M_T)^n · ( Σ_{k ≥ 1} |⟨0|A|k⟩|² )^{1/2}
                       · ( Σ_{k ≥ 1} |⟨k|B|0⟩|² )^{1/2}        (Cauchy-Schwarz)
        ≤  (λ_1/M_T)^n · ‖A|0⟩‖ · ‖B^†|0⟩‖
        ≤  (λ_1/M_T)^n · ‖A‖ · ‖B‖
        =  exp(-n · Δ_T) · ‖A‖ · ‖B‖.                                       (B.14)
```

The last line uses `(λ_1/M_T)^n = exp(-n · log(M_T/λ_1)) = exp(-n · Δ_T)`,
which is (B.7). ∎

### Step 3 — Finite-temperature temporal bound (proves B.2)

Write `H̃ := -(1/a_τ) log T̃`, the vacuum-subtracted Hamiltonian with
spectrum `0 = E_0 < E_1 ≤ E_2 ≤ …` where `E_k = -(1/a_τ) log(λ_k/M_T)`.
The thermal state at inverse temperature `β` is

```text
    ρ_β  :=  Z_β⁻¹ · exp(-β H̃),     Z_β = Σ_k exp(-β E_k).                   (B.15)
```

Let `P_0 = |0⟩⟨0|` and `P_\perp = I - P_0`. Define

```text
    q_β := Tr(P_\perp exp(-β H̃)) / Tr(exp(-β H̃)).                         (B.15)
```

Then `ρ_β = (1-q_β) P_0 + q_β σ_\perp` for a density matrix
`σ_\perp` supported on the excited subspace, so
`‖ρ_β - P_0‖_1 = 2 q_β`. For `X_n := A T̃^n B`,
`‖X_n‖ ≤ ‖A‖‖B‖`, hence

```text
    |Tr(ρ_β X_n) - ⟨0|X_n|0⟩| ≤ 2 q_β ‖A‖‖B‖.                              (B.16)
```

Similarly,

```text
    |Tr(ρ_β A)Tr(ρ_β B) - ⟨A⟩_0⟨B⟩_0| ≤ 4 q_β ‖A‖‖B‖.                     (B.17)
```

Combining (B.16), (B.17), and the ground-state bound (B.7):

```text
    | ⟨A · T̃^n · B⟩_β - ⟨A⟩_β ⟨B⟩_β |
       ≤   ‖A‖ ‖B‖ · ( exp(-n Δ_T) + 6 q_β ).                              (B.18)
```

This is exactly (B.8). The two terms have different meanings: the
first is the spectral-gap-controlled temporal decay in the ground
state, and the second is the finite-temperature excited-state
population. Since each excited energy obeys `E_k ≥ m_gap`, the crude
finite-block estimate

```text
    q_β ≤ (D-1) exp(-β m_gap) / (1 + (D-1) exp(-β m_gap))                  (B.19)
```

is available when an explicit dimension `D` is fixed. The runner tests
the sharper computed `q_β`; it does not replace `q_β` with a hidden
dimension-independent Boltzmann factor. ∎

## Where the gap input enters and what closes it

The proof above uses `Δ_T > 0` only in three places:

1. **Strict inequality `(λ_1/M_T) < 1`** — used in (B.14) to obtain
   exponential decay rather than `O(1)` bounds.
2. **`m_gap := Δ_T / a_τ > 0`** — used to make the finite-block
   excited-state population `q_β` vanish as `β → ∞`; the explicit
   finite-block dimension remains part of any crude Boltzmann bound.
3. **`E_k ≥ E_1` for `k ≥ 1`** — automatic on finite-dim spectrum
   ordering, but `E_1 > 0` follows from `Δ_T > 0`.

**The identity content of (B) is closed-form finite-block spectral
theory.** No infinite-volume limit or continuum limit enters.
Spectral decomposition, Cauchy-Schwarz, and trace-distance control
from `ρ_β` to the ground-state projector are the entire toolkit.

**The gap input `Δ_T > 0` is what is missing on `A_min`.** The
spectrum-condition support note states `m_gap > 0` in its (SC3)
*conditional on* "non-degenerate top eigenvalue (Perron–Frobenius
for the positive operator T on the canonical surface)". This
non-degeneracy is asserted, not derived, in the spectrum-condition
note. The first-principles derivation of `Δ_T > 0` for the
canonical Cl(3) ⊗ Z^3 staggered + Wilson Hamiltonian is the open
work that this bridge note explicitly identifies.

## Hypothesis set used

This bounded bridge theorem uses:

- A1, A2 (only via the parent note's LR setup; no new use of A1/A2);
- A3, A4 (only via the parent note's finite-range / canonical-norm setup);
- Reflection-positivity support (defines `T : H_phys → H_phys`);
- Spectrum-condition support (defines `H̃ ≥ 0`);
- The parent LR bound only as dependency context for the parent row;
- **Conditional input:** `Δ_T > 0` (transfer-matrix spectral gap), an
  explicit open input until first-principles derived.

Standard finite-dim spectral theorem (resolution of identity for
positive Hermitian on finite-dim Hilbert space) is the only
"standard mathematical" input — it is at the same authority level
as the LR-1972 estimate cited by the parent note.

## Honest status

**Closed-form finite-block bridge.** (B.1)–(B.2) are proved on the
finite-block transfer-matrix surface imported from the support notes,
conditional on the input `Δ_T > 0`. The proof is spectral
decomposition, Cauchy-Schwarz, and a trace-distance estimate; no
Hastings-Koma constants are imported.

**The bridge does not derive `Δ_T > 0`.** The mass-gap input is the
remaining open work for the parent cluster-decomposition note.
This note **explicitly tags** the gap as the open dependency,
rather than asserting it. The audit verdict's complaint that
"the packet gives no retained mass-gap or confinement authority"
is addressed by:

1. Acknowledging the gap is genuinely missing from `A_min`-only
   inputs.
2. Reducing the temporal transfer-matrix part of L2 to a closed-form
   identity that takes the gap as a named input.
3. Recording the missing-derivation-difficulty as the explicit
   open lane for the parent cluster-decomposition row.

**What this rules out.**

- The bridge does **not** claim `Δ_T > 0` on the canonical surface.
  The parent note's L2 corollary remains conditional on the gap
  input until the gap is independently derived.
- The bridge does **not** prove the parent note's spatial L2-as-stated.
  Spatial cluster decomposition still needs an additional retained
  gap-plus-LR theorem, a spatial transfer-matrix gap, or an equivalent
  retained argument.

**Repair targets for full closure (still open).**

1. **First-principles derivation of `Δ_T > 0` on the canonical
   Cl(3) ⊗ Z^3 staggered + Wilson Hamiltonian.** Standard candidates:
   (a) lattice strong-coupling expansion at `g_bare = 1` showing
   convergence with positive rate; (b) Perron-Frobenius on the
   positive transfer matrix proving non-degeneracy of the top
   eigenvalue under canonical-surface boundary conditions;
   (c) a structural confinement theorem on `A_min` giving
   `m_gap ≥ √σ` with `σ > 0` the string tension. None of these
   is currently retained on `A_min`.
2. **Generalization beyond the temporal direction.** The bridge above
   gives temporal transfer-matrix decay directly. A spatial cluster
   decomposition theorem still needs a retained gap-plus-LR result,
   a spatial transfer-matrix gap argument, or another retained
   spatial-decay proof.
3. **Verification of Hastings-Koma constants.** The audit also
   flags that the parent note's Step 4 cites Hastings-Koma without
   verifying constants. The bridge proof above does not use
   Hastings-Koma at all — it uses a direct finite-dim spectral
   decomposition — so the constant-verification concern is not
   inherited by this note. The Kubo identity (8) of the parent
   note remains valid, but is not a load-bearing step of (B).

## Citations

- A_min: `MINIMAL_AXIOMS_2026-04-11.md`,
  `MINIMAL_AXIOMS_2026-05-03.md`
- parent cluster-decomposition note (audit verdict prompted this repair):
  `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- reflection-positivity support note:
  `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- spectrum-condition support note:
  `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`
- Lieb-Robinson microcausality (downstream consumer of L1):
  `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`

## Audit dependency note

This note is a bounded finite-dimensional lemma with explicit
hypotheses. The parent cluster-decomposition note carries the graph
edge to this bridge. The upstream axiom-first notes above are recorded
as source context rather than additional graph edges, to avoid
reintroducing the known axiom-first cycle while the parent row awaits
re-audit.
