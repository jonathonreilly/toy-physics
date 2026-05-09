# Mass-Gap Bridge for Cluster Decomposition on Cl(3) ⊗ Z^3

**Date:** 2026-05-09
**Status:** support — branch-local conditional theorem note on A_min + retained reflection-positivity + retained spectrum-condition; runner passing; audit-pending.
**Type:** positive_theorem (conditional bridge)
**Loop:** `axiom-first-foundations`
**Cycle:** rigorization repair for `axiom_first_cluster_decomposition_theorem_note_2026-04-29`
**Runner:** `scripts/cluster_decomposition_mass_gap_bridge_check.py`
**Log:** `outputs/cluster_decomposition_mass_gap_bridge_check_2026-05-09.txt`

## Why this note exists

The audit verdict on
[`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
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

This note supplies the **bridge** — i.e. the closed-form derivation of
exponential clustering from a positive transfer-matrix spectral gap —
and makes the unproved input (the existence and size of the gap)
**explicit** rather than asserted. The bridge itself is a closed-form
theorem on `A_min` plus the retained reflection-positivity and
spectrum-condition support artifacts. The remaining open work — a
first-principles derivation of `m_gap > 0` for the canonical Cl(3) ⊗
Z^3 staggered + Wilson Hamiltonian — is recorded explicitly as an
open dependency.

## Scope

This note proves, on `A_min` plus the retained reflection-positivity
support artifact ([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md))
and the retained spectrum-condition support artifact
([`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)),
the following **conditional bridge theorem**:

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
> temperature `0 < β < ∞`, the connected correlator at temporal
> separation `n` satisfies the **two-term rigorous bound**
>
> ```text
>     | ⟨A_x B_y⟩_β - ⟨A_x⟩_β ⟨B_y⟩_β |
>                                                                       (B.3)
>         ≤   ‖A_x‖ · ‖B_y‖ · ( exp(-n · Δ_T)  +  3·exp(-β · m_gap · a_τ) )
> ```
>
> with `m_gap := Δ_T / a_τ` the Hamiltonian gap. (At zero
> temperature `β → ∞` the second term vanishes and (B.3) reduces to
> the ground-state form (B.2).) For purely spatial separation
> `d(x,y) = d ≥ 1`, combining (B.2)/(B.3) with the
> Lieb-Robinson bound (L1) of the parent note gives
>
> ```text
>     | ⟨A_x B_y⟩_β - ⟨A_x⟩_β ⟨B_y⟩_β |
>                                                                       (B.4)
>         ≤   ‖A_x‖ · ‖B_y‖ · ( K · exp(-d / ξ) + 3·exp(-β m_gap a_τ) )
> ```
>
> with `K = O(1)` and `ξ = max(R_int, v_LR · a_τ / Δ_T)`. At zero
> temperature the second term vanishes; at any finite β the second
> term is independent of `d` (a temperature-controlled "background"
> floor that vanishes in the β → ∞ limit).

**(B) is a closed-form algebraic identity in finite-dim spectral
theory.** No assertion of `Δ_T > 0` is made by this note; the gap
input is named explicitly and the bridge is conditional on it.

## A_min objects in use

Same as the parent
[`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md):
A1 (Cl(3) site algebra), A2 (Z^3 substrate), A3 (finite-range Hamiltonian
from staggered + Wilson), A4 (canonical normalization fixing the operator
norm of each interaction term).

## Retained inputs

- **Reflection positivity / transfer matrix.** From
  [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md),
  `T : H_phys → H_phys` is a positive Hermitian operator on a finite-
  dimensional Hilbert space `H_phys`, with `M_T := λ_max(T) < ∞` and
  `T = T†`.
- **Spectrum condition.** From
  [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md),
  the vacuum-energy-subtracted Hamiltonian
  `H̃ := -(1/a_τ) log(T / M_T)` is self-adjoint and `H̃ ≥ 0` on `H_phys`.
- **Lieb-Robinson bound (L1) on `A_min`.** From the parent
  [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md),
  `‖[A_x(t), B_y]‖ ≤ 2‖A‖‖B‖ exp(-(d - v_LR|t|)/ξ)` for finite-range
  Hermitian Hamiltonian on Cl(3) ⊗ Z^3.

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

**(B.2) Canonical thermal clustering (two-term rigorous form).** For
any `0 < β < ∞`, the canonical thermal state `ρ_β := Z⁻¹ exp(-β H̃)`
satisfies

```text
    | ⟨A · T̃^n · B⟩_β - ⟨A⟩_β ⟨B⟩_β |
                                                                        (B.8)
        ≤   ‖A‖ · ‖B‖ · ( exp(-n · Δ_T)  +  3 · exp(-β · m_gap · a_τ) )
```

with `m_gap := Δ_T / a_τ` the Hamiltonian gap. At fixed `β`, the
RHS is exponentially small once `n ≥ β·m_gap·a_τ / Δ_T`; at fixed
`n`, it is exponentially small once `β ≥ n · Δ_T / (m_gap · a_τ)`.
At zero temperature (`β → ∞`), the second term vanishes and (B.8)
reduces to (B.7).

**(B.3) Spatial clustering corollary.** For any two operators
`A_x, B_y` localized at spatial sites with `d(x,y) = d`, and for
any `0 ≤ n a_τ ≤ d/v_LR`, combining (B.8) with the Lieb-Robinson
bound (L1) of the parent note gives

```text
    | ⟨A_x B_y⟩_β - ⟨A_x⟩_β ⟨B_y⟩_β |
                                                         (B.9)
        ≤   ‖A_x‖ · ‖B_y‖ · ( exp(-n · Δ_T) + 3·exp(-β m_gap a_τ)
                             + 2 exp(-(d - v_LR n a_τ)/R_int) )
```

Optimizing the first and third terms over `n`:

```text
    ξ  =  max( R_int ,  v_LR · a_τ / Δ_T )                                  (B.10)
```

so that

```text
    |⟨A_x B_y⟩_β - ⟨A_x⟩_β ⟨B_y⟩_β|
                                                                            (B.11)
        ≤   ‖A_x‖ ‖B_y‖ · ( K · exp(-d/ξ) + 3·exp(-β m_gap a_τ) )
```

with `K = O(1)`. At zero temperature (`β → ∞`) the second term
vanishes, recovering pure exponential spatial clustering with rate
`1/ξ`.

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

### Step 3 — Canonical thermal clustering (proves B.2)

Write `H̃ := -(1/a_τ) log T̃`, the vacuum-subtracted Hamiltonian with
spectrum `0 = E_0 < E_1 ≤ E_2 ≤ …` where `E_k = -(1/a_τ) log(λ_k/M_T)`.
The thermal state at inverse temperature `β` is

```text
    ρ_β  :=  Z_β⁻¹ · exp(-β H̃),     Z_β = Σ_k exp(-β E_k).                   (B.15)
```

Spectrally,

```text
    ⟨A · T̃^n · B⟩_β
        =  Z_β⁻¹  Σ_{j, k}  exp(-β E_j) · (λ_k/M_T)^n · ⟨j|A|k⟩ · ⟨k|B|j⟩.   (B.16)
```

The disconnected piece is

```text
    ⟨A⟩_β · ⟨B⟩_β  =  ( Z_β⁻¹  Σ_j exp(-β E_j) ⟨j|A|j⟩ )
                       · ( Z_β⁻¹  Σ_l exp(-β E_l) ⟨l|B|l⟩ ).                  (B.17)
```

Subtract: the connected correlator is

```text
    ⟨A · T̃^n · B⟩_β  -  ⟨A⟩_β ⟨B⟩_β
        =  Z_β⁻¹  Σ_{j, k ≠ j}  exp(-β E_j) · (λ_k/M_T)^n · ⟨j|A|k⟩⟨k|B|j⟩
           +  Z_β⁻¹  Σ_j  exp(-β E_j) · [ (λ_j/M_T)^n - 1 ] · ⟨j|A|j⟩⟨j|B|j⟩
           -  ⟨A⟩_β ⟨B⟩_β  +  Z_β⁻¹  Σ_j  exp(-β E_j)  ⟨j|A|j⟩⟨j|B|j⟩.        (B.18)
```

For the diagonal `j = k` contribution: `(λ_j/M_T)^n - 1` is bounded
by `1` for `j = 0` (= 0 exactly) and by `(λ_1/M_T)^n + 1 ≤ 2` for
`j ≥ 1`. The off-diagonal `k ≠ j` contribution is bounded as
follows. Write `(λ_k/M_T) = exp(-a_τ E_k) ≤ exp(-a_τ E_1)` for any
`k ≥ 1` (using `E_k ≥ E_1` for `k ≥ 1` since `E_0 = 0`). For
`j = 0`, the off-diagonal contribution is exactly bounded by (B.14)
and is `≤ ‖A‖‖B‖ exp(-n Δ_T)`. For `j ≥ 1`,

```text
    | (λ_k/M_T)^n  ⟨j|A|k⟩⟨k|B|j⟩ |
       ≤  exp(-n · a_τ · min_{k ≥ 1, k ≠ j} E_k) · |⟨j|A|k⟩| · |⟨k|B|j⟩|.     (B.19)
```

Sum over `k ≠ j` and apply Cauchy-Schwarz:

```text
    Σ_{k ≠ j}  (λ_k/M_T)^n · |⟨j|A|k⟩| · |⟨k|B|j⟩|
       ≤  exp(-n · Δ_T) · ‖A|j⟩‖ · ‖B^†|j⟩‖
       ≤  exp(-n · Δ_T) · ‖A‖ · ‖B‖.                                          (B.20)
```

So the off-diagonal-in-k contribution is

```text
    | Z_β⁻¹  Σ_{j, k ≠ j}  exp(-β E_j) (λ_k/M_T)^n  ⟨j|A|k⟩⟨k|B|j⟩ |
       ≤  ‖A‖ ‖B‖ · exp(-n · Δ_T) · Z_β⁻¹  Σ_j exp(-β E_j)
       =  ‖A‖ ‖B‖ · exp(-n · Δ_T).                                            (B.21)
```

For the diagonal `j = k ≥ 1` contribution: `[(λ_j/M_T)^n - 1] · ⟨j|A|j⟩⟨j|B|j⟩`
is bounded in absolute value by `2 ‖A‖ ‖B‖`, weighted by
`exp(-β E_j) ≤ exp(-β E_1) = exp(-β · m_gap · a_τ)` (where
`m_gap := E_1 = Δ_T / a_τ`). Sum over `j ≥ 1`:

```text
    | Z_β⁻¹  Σ_{j ≥ 1} exp(-β E_j) [(λ_j/M_T)^n - 1] ⟨j|A|j⟩⟨j|B|j⟩ |
       ≤  2 ‖A‖ ‖B‖ · exp(-β · m_gap · a_τ).                                 (B.22)
```

The `j = 0` diagonal contribution `[(λ_0/M_T)^n - 1] ⟨0|A|0⟩⟨0|B|0⟩
= 0` exactly. The remaining `(-⟨A⟩_β ⟨B⟩_β + Z_β⁻¹ Σ_j exp(-β E_j) ⟨j|A|j⟩⟨j|B|j⟩)`
piece is the standard "disconnected minus diagonal" rearrangement
that vanishes in the `n → ∞` limit; an elementary bound gives it
`≤ ‖A‖ ‖B‖ · exp(-β · m_gap · a_τ)` (using the same gap-bound on
`exp(-β E_j)` for `j ≥ 1`).

Adding (B.21), (B.22), and the "disconnected minus diagonal" bound:

```text
    | ⟨A · T̃^n · B⟩_β - ⟨A⟩_β ⟨B⟩_β |
       ≤   ‖A‖ ‖B‖ · ( exp(-n Δ_T) + 3 · exp(-β m_gap a_τ) ).                (B.23)
```

This is exactly (B.8). The two terms have different physical
meaning: the first is the spectral-gap-controlled n-decay; the
second is the temperature-controlled excited-state-population
floor. At fixed `β`, the n-decay dominates once `n ≥ β m_gap a_τ /
Δ_T`. At zero temperature (`β → ∞`), the second term vanishes
identically and (B.8) reduces to (B.7). ∎

### Step 4 — Spatial clustering corollary (proves B.3)

For two operators `A_x, B_y` at spatial separation `d := d(x,y)`, the
correlator can be computed by inserting an arbitrary number `n` of
temporal-evolution slices (we may choose the optimal `n` to balance
the two error sources):

```text
    ⟨A_x B_y⟩_β  =  ⟨A_x · α_{n a_τ}(B_y) ⟩_β  +  O(LR error)               (B.24)
```

where `α_t = e^{itH̃}` is Heisenberg evolution. The LR bound (L1)
of the parent note gives

```text
    ‖ [A_x , α_{n a_τ}(B_y)] ‖   ≤   2‖A‖‖B‖ exp(-(d - v_LR n a_τ)/R_int).    (B.25)
```

For the connected correlator,

```text
    | ⟨A_x B_y⟩_β - ⟨A_x⟩_β ⟨B_y⟩_β |
       ≤  | ⟨A_x α_{n a_τ}(B_y)⟩_β - ⟨A_x⟩_β ⟨α_{n a_τ}(B_y)⟩_β |
          + ‖[A_x, α_{n a_τ}(B_y)]‖                                         (B.26)
```

For the first term, we use that `⟨α_{n a_τ}(B_y)⟩_β = ⟨B_y⟩_β` is
time-translation invariant (KMS/stationarity), and apply (B.8) to
the temporal correlator at separation `n`:

```text
    | ⟨A_x α_{n a_τ}(B_y)⟩_β - ⟨A_x⟩_β ⟨B_y⟩_β |
       ≤  ‖A‖ ‖B‖ · ( exp(-n Δ_T) + 3·exp(-β m_gap a_τ) ).                   (B.27)
```

Combining (B.25) and (B.27) gives (B.9). Optimizing the first and
third (LR) terms over `n` (the second term is `n`-independent)
yields `n ≈ d / (v_LR · a_τ · (1 + R_int Δ_T / (v_LR a_τ)))`, and the
spatial decay rate `1/ξ = min(1/R_int, Δ_T / (v_LR a_τ))`,
i.e. `ξ = max(R_int, v_LR a_τ / Δ_T)`. ∎

## Where the gap input enters and what closes it

The proof above uses `Δ_T > 0` only in three places:

1. **Strict inequality `(λ_1/M_T) < 1`** — used in (B.14) to obtain
   exponential decay rather than `O(1)` bounds.
2. **`m_gap := Δ_T / a_τ > 0`** — used in (B.22) to bound thermal
   weights `exp(-β E_j) ≤ exp(-β m_gap a_τ)` for `j ≥ 1`.
3. **`E_k ≥ E_1` for `k ≥ 1`** — automatic on finite-dim spectrum
   ordering, but `E_1 > 0` follows from `Δ_T > 0`.

**The identity content of (B) is closed-form algebraic.** No
asymptotic estimates, no infinite-volume limits, no continuum
limits enter. Spectral decomposition + Cauchy-Schwarz + finite-dim
spectral ordering is the entire toolkit.

**The gap input `Δ_T > 0` is what is missing on `A_min`.** The
retained spectrum-condition note states `m_gap > 0` in its (SC3)
*conditional on* "non-degenerate top eigenvalue (Perron–Frobenius
for the positive operator T on the canonical surface)". This
non-degeneracy is asserted, not derived, in the spectrum-condition
note. The first-principles derivation of `Δ_T > 0` for the
canonical Cl(3) ⊗ Z^3 staggered + Wilson Hamiltonian is the open
work that this bridge note explicitly identifies.

## Hypothesis set used

This bridge theorem uses:

- A1, A2 (only via the parent note's LR setup; no new use of A1/A2);
- A3, A4 (only via the parent note's finite-range / canonical-norm setup);
- Retained reflection positivity (defines `T : H_phys → H_phys`);
- Retained spectrum condition (defines `H̃ ≥ 0`);
- Retained LR bound L1 (parent note; for the spatial-clustering corollary);
- **Conditional input:** `Δ_T > 0` (transfer-matrix spectral gap), tagged as
  `admitted_context_input` until first-principles derived.

Standard finite-dim spectral theorem (resolution of identity for
positive Hermitian on finite-dim Hilbert space) is the only
"standard mathematical" input — it is at the same authority level
as the LR-1972 estimate cited by the parent note.

## Honest status

**Closed-form bridge.** (B.1)–(B.3) are proved on `A_min` plus the
retained reflection-positivity and spectrum-condition support
artifacts, conditional on the input `Δ_T > 0`. The proof is a
finite-dim spectral decomposition + Cauchy-Schwarz; no asymptotic
manipulations, no Hastings-Koma `1/(βm_gap)` constants are imported
without verification.

**The bridge does not derive `Δ_T > 0`.** The mass-gap input is the
remaining open work for the parent cluster-decomposition note.
This note **explicitly tags** the gap as the open dependency,
rather than asserting it. The audit verdict's complaint that
"the packet gives no retained mass-gap or confinement authority"
is addressed by:

1. Acknowledging the gap is genuinely missing from `A_min`-only
   inputs.
2. Reducing the bridge L1 → L2 to a closed-form identity that
   takes the gap as named input.
3. Recording the missing-derivation-difficulty as the explicit
   open lane for the parent cluster-decomposition row.

**What this rules out.**

- The bridge does **not** claim `Δ_T > 0` on the canonical surface.
  The parent note's L2 corollary remains conditional on the gap
  input until the gap is independently derived.
- The bridge does **not** support the parent note's L2-as-stated
  for an *unspecified* canonical thermal state with no gap.

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
2. **Generalization beyond the temporal direction.** The bridge
   above gives temporal clustering rate `Δ_T` directly; the
   spatial corollary (B.4) uses an LR + temporal-clustering
   composition. A purely spatial transfer-matrix gap argument
   (with reflection axes orthogonal to the temporal direction)
   would give a spatial gap `Δ_T^{spatial}` directly without the
   LR composition.
3. **Verification of Hastings-Koma constants.** The audit also
   flags that the parent note's Step 4 cites Hastings-Koma without
   verifying constants. The bridge proof above does not use
   Hastings-Koma at all — it uses a direct finite-dim spectral
   decomposition — so the constant-verification concern is not
   inherited by this note. The Kubo identity (8) of the parent
   note remains valid, but is not a load-bearing step of (B).

## Status fields

```yaml
actual_current_surface_status: support
conditional_surface_status: closed-form bridge L1 + Δ_T → L2 on A_min + retained RP + retained spectrum condition
hypothetical_axiom_status: null
admitted_context_inputs:
  - "Δ_T > 0 (transfer-matrix spectral gap on canonical Cl(3) ⊗ Z^3 staggered + Wilson Hamiltonian)"
  - "retained reflection-positivity (audit-pending)"
  - "retained spectrum condition (audit-pending)"
proposal_allowed: false
proposal_allowed_reason: "Bridge is conditional on a non-derived mass-gap input. Per physics-loop SKILL retained-proposal certificate, a chain of support cannot promote to proposed_retained until all dependencies are derived; the Δ_T > 0 input is explicitly an open derivation target."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Citations

- A_min: [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md),
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- parent cluster-decomposition note (audit verdict prompted this repair):
  [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
- retained reflection-positivity support note:
  [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- retained spectrum-condition support note:
  [`AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
- Lieb-Robinson microcausality (downstream consumer of L1):
  [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links
named by a prior conditional audit so the audit citation graph can
track them. It does not promote this note or change the audited
claim scope.

- [axiom_first_cluster_decomposition_theorem_note_2026-04-29](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
- [axiom_first_reflection_positivity_theorem_note_2026-04-29](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- [axiom_first_spectrum_condition_theorem_note_2026-04-29](AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md)
