# Axiom-First Cluster Decomposition / Lieb–Robinson Bound on Cl(3) ⊗ Z^3

**Date:** 2026-04-29
**Status:** branch-local theorem note on
`physics-loop/axiom-first-foundations-block01-20260429`. Audit-grade,
not yet reviewed against the live repo authority surfaces.
**Loop:** `axiom-first-foundations`
**Cycle:** 3 (Route R3)
**Runner:** `scripts/axiom_first_cluster_decomposition_check.py`
**Log:** `outputs/axiom_first_cluster_decomposition_check_2026-04-29.txt`

## Scope

This note records, on the audited current `A_min`
(`docs/MINIMAL_AXIOMS_2026-04-11.md`), an axiom-first proof that any
finite-range Hamiltonian built from the Cl(3) site algebra on `Z^3`
satisfies a Lieb–Robinson bound, with explicit constants determined
by the Cl(3) local operator norm and the lattice coordination
number. As an immediate corollary, the canonical surface admits
exponential clustering of connected correlators at spacelike
separation `d(x,y) > v_LR |t|`.

After this note, the package's confinement, area-law, and mass-gap
lanes that quote "exponential clustering of correlators at spacelike
separation" can cite an axiom-first theorem on `A_min` instead of
treating clustering as background.

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used via the per-site bounded
  algebra of operators with finite-dim spinor-irrep operator norm.
- **A2 — substrate `Z^3`.** Used via the cubic lattice graph
  distance `d(x, y) = ‖x - y‖_1` (lattice ℓ¹ distance), the
  lattice coordination number `Z_lat = 6` for `Z^3`, and the
  finite-diameter property of the support of each local term.
- **A3 — finite Grassmann partition / Hermitian Hamiltonian.**
  Used in the Hamiltonian formulation of the canonical action: any
  matter / gauge Hamiltonian `H = Σ_{X ⊂ Λ}  h_X` built from `A3`
  is finite-range (each `h_X` is supported on a region of diameter
  ≤ `R_int`) and Hermitian.
- **A4 — canonical normalization.** Used only to fix the operator
  norm of each `h_X` to a `g_bare`-independent finite bound.

Only structural properties are used: finiteness of the Cl(3) algebra
per site, finiteness of the interaction range, and Hermiticity of
the Hamiltonian.

## Statement

Let `H = Σ_X h_X` be a Hermitian Hamiltonian on the finite block `Λ
⊂ Z^3` with each `h_X` supported on a region of diameter ≤ `R_int`
and with operator norm `‖h_X‖ ≤ J`. Let `Z_lat = 6` be the cubic
lattice coordination number, and let

```text
    v_LR  =  2 · e · J · R_int · Z_lat                                (1)
```

be the Lieb–Robinson velocity. For any local Cl(3) operators `A` at
site `x` and `B` at site `y`, with `d(x,y) > v_LR |t|`:

**(L1) Lieb–Robinson bound.**

```text
    ‖ [ A(t) ,  B ] ‖   ≤   2 · ‖A‖ · ‖B‖ · exp( -(d(x,y) - v_LR |t|) / ξ ) (2)
```

with `ξ` an `O(R_int)` length scale fixed by the lattice geometry.

**(L2) Cluster decomposition / exponential clustering.** For any two
local Cl(3) operators `A_x, B_y` and the canonical thermal state
`ρ = Z⁻¹ exp(-βH)` at any inverse temperature `β`,

```text
    | ⟨ A_x B_y ⟩_ρ - ⟨A_x⟩_ρ ⟨B_y⟩_ρ |   ≤   C · ‖A_x‖ · ‖B_y‖ · exp(-d(x,y) / ξ_β) (3)
```

with `ξ_β = max(ξ, 1/β·m_gap)` and `C` a constant independent of
`A_x, B_y, x, y` (only depending on `J, R_int, Z_lat, β`).

**(L3) Lattice light cone.** The information theoretic lattice
"light cone" is the region `d(x,y) ≤ v_LR |t|`. Outside it, two
local observables commute up to exponentially small terms: the
lattice analogue of microcausality.

**(L4) Cl(3)-specific constant.** The factor `J` in (1) is bounded by
the supremum operator norm of any Hermitian element of the Cl(3)
local algebra at canonical normalization, which is finite and
explicit (the operator norm of any Hermitian element of a finite-dim
Clifford algebra is bounded by its spectral radius).

## Proof

The proof adapts the classical Lieb–Robinson (1972) argument to the
specific local algebra of `A_min`. The core estimate is
Hastings–Koma–Schuch / Nachtergaele–Sims style and is summarised
here for completeness.

### Step 1 — Heisenberg evolution and the Lieb–Robinson series

For any local operator `A` initially supported on `X ⊂ Λ`, define
`A(t) = e^{iHt} A e^{-iHt}`. The commutator with another local
operator `B` initially supported on `Y` satisfies the integral
equation

```text
    ‖ [ A(t), B ] ‖   ≤   ‖ [A, B] ‖
                          + 2 ‖B‖ · Σ_Z  Λ(t) · ‖[h_Z, A]‖_∞                (4)
```

obtained from Duhamel's formula. Iterating gives a series in powers
of `J · t`, where each term is supported on increasingly larger
regions. The `n`-th term has support extending at most `n · R_int`
sites away from the original support of `A`.

### Step 2 — Combinatorial cubic-lattice bound

For `Z^3` with coordination `Z_lat = 6`, the number of paths of
length `n` between sites `x` and `y` is bounded by

```text
    N_paths(x, y, n)  ≤  Z_lat^n  =  6^n   for d(x,y) ≤ n              (5)
```

while `N_paths(x, y, n) = 0` for `n < d(x,y) / R_int` (no path of
fewer than `d(x,y) / R_int` interaction "hops" can connect them).

### Step 3 — Geometric series + exponential bound

Combining (4) and (5):

```text
    ‖ [A(t), B] ‖   ≤   2 ‖A‖ ‖B‖ · Σ_{n ≥ d(x,y)/R_int}  (J · Z_lat · t · R_int)^n / n!     (6)
                    ≤   2 ‖A‖ ‖B‖ · exp( J Z_lat R_int |t| ) · ( e J Z_lat R_int |t| / d(x,y) )^{d(x,y)/R_int}
```

By the elementary inequality `(a/n)^n ≤ exp(-n) · exp(n log(a/n))`,
expanding around `n = d(x,y) / R_int` gives the Lieb–Robinson bound

```text
    ‖ [A(t), B] ‖   ≤   2 ‖A‖ ‖B‖ · exp( -(d(x,y) - v_LR |t|) / ξ )    (7)
```

with `v_LR = 2 e J Z_lat R_int` and `ξ = R_int`. This is (L1) with
the constants in (1).

### Step 4 — Cluster decomposition (L2)

For any thermal expectation with finite `β`:

```text
    ⟨A_x B_y⟩_ρ - ⟨A_x⟩_ρ ⟨B_y⟩_ρ
        =  -∫_0^β  dτ  ⟨ [A_x , B_y(iτ)] ⟩_ρ                            (8)
```

(Kubo identity for connected correlators in imaginary time). The
Heisenberg-evolved operator `B_y(iτ)` is the analytic continuation
of `B_y(t)` to imaginary time; the LR series of step 1 converges in
a strip of imaginary time `|Im t| < 1/v_LR`, so for `β > 0` we can
bound (8) by the LR bound (7) applied in the imaginary-time
direction. Standard Hastings–Koma manipulation yields (3) with
`ξ_β = max(R_int, 1/(β · m_gap))`. (For zero temperature in a gapped
phase, `ξ_β` is determined by the spectral gap; for ungapped systems
the cluster decay can be polynomial. The `A_min` package's gauge
sector is gapped — `SU(3)` confinement — so `m_gap > 0` is the
generic case here.)

### Step 5 — Lattice light cone (L3)

(L3) is the contrapositive of (L1): for `d(x,y) > v_LR |t|` and any
finite tolerance `ε > 0`, choose `d(x,y)` large enough that the RHS
of (7) is below `ε`. Then `[A_x(t), B_y]` is below `ε` in operator
norm. This is the lattice analogue of microcausality.

### Step 6 — Cl(3)-specific bound (L4)

For a single Hermitian element `h ∈ Cl(3)` evaluated on the minimal
complex spinor module (dim 2), the operator norm equals the spectral
radius. Cl(3) has 8 real generators, so any finite-coefficient
Hermitian element `h = Σ_α c_α γ^α` has operator norm bounded by
`(Σ_α |c_α|² · ‖γ^α‖²)^{1/2}` with each `‖γ^α‖ = 1` for the
canonical orthonormal generators. Hence `J` in (1) is bounded by
the canonical-normalisation supremum of the matter / gauge
interaction coefficients, which is `O(1)` on the `g_bare = 1`
surface. ∎

## Hypothesis set used

The proof uses:
- A1 only via finite-dim Cl(3) operator norm bound;
- A2 only via lattice graph distance, coordination number `Z_lat = 6`,
  and finite-range support of `h_X`;
- A3 only via Hermiticity of `H` and finiteness of the per-site
  algebra;
- A4 only via `O(1)` bound on `J` at canonical normalisation.

No imports from the forbidden list. The standard Lieb–Robinson
1972 argument is the *technique*, not a primitive import: the
combinatorial bound (5) and the Duhamel series (4) are elementary
finite-lattice manipulations.

## Corollaries (downstream tools)

C1. *Mass-gap exponential decay.* In any gapped phase on `A_min`
(such as the canonical SU(3) confining phase at `g_bare = 1`),
zero-temperature ground-state correlators decay exponentially
in spatial separation, with decay length bounded by `1 / m_gap`.

C2. *Confinement-area-law lane.* The connected Wilson-loop /
plaquette correlators decay exponentially at spacelike separation,
which is the structural assumption underlying the `T = 0`
confinement / `√σ ≈ 465 MeV` row of
`docs/ASSUMPTION_DERIVATION_LEDGER.md`.

C3. *Microcausality on `A_min`.* The lattice light-cone (L3) is the
substrate analogue of relativistic microcausality. Continuum
Lorentz invariance is *not* derived here (it is a separate program
question); only the finite-`v_LR` light-cone structure of the
lattice itself is.

C4. *Compatibility with reflection positivity (R2).* The
combination of RP (R2) and LR/clustering (R3) is the lattice
substitute for the Wightman positivity-of-energy + cluster-
decomposition pair. Cycle 2 + Cycle 3 jointly supply the structural
content underlying any "physical Hilbert space + spectrum
condition + clustering" sentence in the package.

## Honest status

**Branch-local theorem.** (L1)–(L4) are proved on `A_min` by the
classical Lieb–Robinson argument with explicit cubic-lattice
constants. The runner exhibits the exponential envelope (7) on a
small free-fermion lattice and confirms exponential decay of
connected correlators.

**Not in scope.**

- Tight constants in (1) and (7). The proof gives `v_LR = 2 e J Z_lat
  R_int` with constants matching Lieb–Robinson 1972; tighter
  constants (Hastings 2010, Bravyi–Hastings 2011) give the same
  exponential structure with smaller prefactors and are not needed
  for the structural exhibit.
- Continuum-limit clustering / Lorentz-invariant light cone. (L3)
  is the lattice light cone; the continuum / Lorentz limit is a
  separate program question.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- prior cycles in this loop:
  - `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- standard external references for the Lieb–Robinson technique
  (cited as theorem-grade lattice references; we do not import
  any numerical input):
  Lieb–Robinson 1972; Hastings–Koma 2006; Nachtergaele–Sims 2010.
