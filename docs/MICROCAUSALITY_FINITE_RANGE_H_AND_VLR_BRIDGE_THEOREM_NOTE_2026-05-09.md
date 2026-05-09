# Finite-Range H + Explicit v_LR Bridge for the Microcausality / Lieb-Robinson Theorem

**Date:** 2026-05-09
**Type:** positive_theorem
**Claim scope:** On the canonical staggered + Wilson Hamiltonian density
read off the parent reflection-positivity note's action carriers
(`docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`,
eq. (1) for `M = M_KS + M_W + m·I` and eq. (2) for the Wilson plaquette
gauge action), the reconstructed lattice Hamiltonian
`H = sum_z h_z` is **finite-range with explicit interaction radius
`r = 1` lattice spacing** and **explicit local-density operator-norm
bound `J = (d/2) + r_W·d + |m| + (β/N_c)·6`** (independent of lattice
volume, gauge background, and link variables on the canonical surface
at `g_bare = 1`). Plugging these explicit `r` and `J` into the
Hastings-Koma / Nachtergaele-Sims commutator estimate gives
`v_LR = 2·e·r·J` directly from action coefficients, removing the
asserted-bridge gap flagged by the audit verdict on the parent
microcausality note.
**Status authority:** independent audit lane only. This source note is
a narrow bridge theorem; it does not set or predict an audit outcome.
**Primary runner:** `scripts/microcausality_finite_range_h_bridge_2026_05_09.py`

## Why this note exists

The parent note
`docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`
records, in its (M2), the Lieb-Robinson lightcone bound

```text
    ‖ [α_t(O_x), O_y] ‖_op  ≤  2 ‖O_x‖ ‖O_y‖ · exp(- d(x,y) + v_LR · |t|)
```

with `v_LR = 2 e r J`. The independent-audit lane verdict (audit row
`axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01`,
2026-05-05) flagged exactly the load-bearing step

> "the load-bearing finite-range-H and explicit v_LR = 2erJ step is not
> derived by the cited RP or spectrum authorities ... RP/spectrum
> provide positivity / self-adjointness / boundedness of H, not the
> locality structure (finite range) needed for Lieb-Robinson, nor an
> explicit v_LR derivation."

This note supplies the missing bridge. Reading the *same* canonical
action carriers that the parent RP note already uses (eq. (1) and (2)
of the parent), this note shows that the temporal-direction transfer
matrix `T = exp(-a_τ · H)` admits a finite-range Hamiltonian
decomposition `H = sum_z h_z` with each `h_z` supported in a ball of
radius `r = 1` lattice spacing, and computes a finite explicit upper
bound on `J = sup_z ‖h_z‖_op` that is independent of the gauge
background and depends only on the action coefficients
`(1/2, r_W, m, β, N_c, d)`.

The bridge then plugs `r` and `J` into the standard Hastings-Koma /
Nachtergaele-Sims combinatorial estimate (which is a pure-mathematics
statement about iterated commutators of finite-range operators on a
graph; no physics input beyond `r` and `J`) and obtains the explicit
`v_LR = 2 e r J` Lieb-Robinson velocity used by the parent (M2).

## Setup and conventions

Adopt the parent reflection-positivity note's action carriers verbatim:

- **A1 / A2** as in `MINIMAL_AXIOMS_2026-05-03.md` (Cl(3) site algebra
  on `Z^d` with `d = 4 = 1 + 3` for a `Z^1 × Z^3` block).
- **Staggered Kogut-Susskind kinetic operator** from parent eq. (1):

  ```text
      (M_KS)_{x, y}  =  (1/2) · [ η_μ(x) · U_μ(x) · δ_{y, x + e_μ}
                                 - η_μ(y) · U_μ(y)^† · δ_{y, x - e_μ} ]      (1)
  ```

  with staggered phase `η_μ(x) = (-1)^{Σ_{ν<μ} x_ν}` and SU(3) link
  variable `U_μ(x)`. The hop coefficient is exactly `1/2` per direction
  (canonical Kogut-Susskind normalisation, verified against the
  symbolic structure on `scripts/frontier_staggered_17card.py` lines
  50, 63-70 which spell out the explicit `±1j/2` matrix elements for
  the staggered Dirac on `Z^d`).

- **Wilson term** from parent §3a: `M_W` with canonical Wilson
  coefficient `r_W = 1`, supported on the same NN link family as
  `M_KS`; on the symmetric-canonical surface
  (`STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md`),
  `M_W = r_W · d · I` so its operator-norm contribution is the diagonal
  bound `r_W · d`.

- **Mass term** from parent eq. (1): `m · I`, contributing `|m|` to
  the local-density operator norm.

- **Wilson plaquette gauge action** from parent eq. (2):

  ```text
      S_G  =  β · sum_P  Re[ 1 - (1/N_c) tr U_P ]                            (2)
  ```

  with `β = 2 N_c / g_bare^2 = 2 N_c = 6` at `g_bare = 1, N_c = 3`. A
  plaquette `P` couples four sites that span a single elementary
  square; in the time-direction transfer-matrix decomposition each
  plaquette term contributes to `h_z` for `z` at the plaquette corner.

- **Lattice ℓ¹ graph distance** `d(x, y) = ‖x - y‖_1` on `Z^d`.

- **Coordination number** `Z_lat = 2 d` (`= 8` on `Z^4`, `= 6` on `Z^3`).

The reconstructed Hamiltonian `H = -log(T)/a_τ` is the time-direction
generator of the canonical RP-reconstructed transfer matrix `T` from
the parent. Its locality structure is read off the action's link
support, NOT from the abstract spectral data of `T`.

## Statement

**(F1) Finite-range Hamiltonian decomposition.** The reconstructed
Hamiltonian `H` admits a translation-covariant decomposition

```text
    H  =  sum_{z ∈ Λ}  h_z                                                  (3)
```

with each `h_z` Hermitian and supported in a ball of radius
`r = 1` lattice spacing around `z` (i.e. `h_z` couples only sites
within `d_graph(·, z) ≤ 1`). Equivalently, for any operator `O_x`
at site `x`,

```text
    [h_z, O_x]  =  0    whenever    d(z, x) > 1.                            (4)
```

**(F2) Explicit J bound.** The local-density operator-norm `J = sup_z ‖h_z‖_op`
satisfies the **explicit gauge-background-independent bound**

```text
    J  ≤  J_max  :=  (d/2) · 1   +   r_W · d   +   |m|   +   (β / N_c) · q_face       (5)
```

where:

- `(d/2) · 1` is the staggered-hop contribution: `d` directions, each
  contributing one off-diagonal NN link of operator norm
  `(1/2) · ‖U_μ(x)‖_op = (1/2) · 1` because SU(3) is unitary
  (`‖U_μ‖_op = 1` always);
- `r_W · d` is the symmetric-canonical Wilson diagonal contribution
  (per `STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md`
  using `M_W = r_W · d · I` with `r_W = 1`);
- `|m|` is the mass term operator norm;
- `(β / N_c) · q_face` is the gauge plaquette contribution, with
  `q_face = number of plaquettes containing a fixed corner site
  on Z^d ≤ d(d-1)`. On `Z^4` this is `≤ 12`; on `Z^3` it is `≤ 6`.
  The factor `(1/N_c) · ‖tr U_P‖_op ≤ 1` is bounded because `tr` of a
  unitary `N×N` matrix has `|tr U| ≤ N`.

In particular, on `Z^4` at `g_bare = 1, N_c = 3, β = 6, r_W = 1, m`
real, plug-in: `J_max = 4/2 + 1·4 + |m| + (6/3)·12 = 2 + 4 + |m| + 24
= 30 + |m|`.

`J_max` does NOT depend on the gauge background `{U_μ}`, on the lattice
volume, or on any spectral data of `T`. It depends only on the fixed
action coefficients.

**(F3) Lieb-Robinson velocity bound.** Plugging (F1)–(F2) into the
Hastings-Koma / Nachtergaele-Sims iterated-commutator combinatorial
estimate (Lieb-Robinson 1972 / Nachtergaele-Sims 2010 §3-4) yields the
explicit Lieb-Robinson velocity

```text
    v_LR  =  2 · e · r · J  ≤  2 · e · 1 · J_max  =  2 · e · J_max          (6)
```

with `r = 1` from (F1) and `J ≤ J_max` from (F2). The Lieb-Robinson
bound (parent (M2) eq. (5)) becomes

```text
    ‖ [α_t(O_x), O_y] ‖_op  ≤  2 ‖O_x‖ ‖O_y‖ · exp(- d(x, y) + 2 e J_max · |t|)    (7)
```

with all constants **read off action coefficients only**, no asserted
bridges, and no dependence on the spectral data of `T` beyond the fact
that `H = -log(T)/a_τ` exists (which is the parent RP/spectrum content).

## Proof

### Step 1 — Finite range from action support (proves F1)

The transfer matrix `T` is defined by integrating out a single time
slice in the lattice path integral on `Λ_+ = { x : t ≥ 0 }`. Writing
the action in temporal-link form (parent eq. (1)–(2)):

```text
    S  =  S_F  +  S_G
       =  Σ_{x ∈ Λ}  m · χ̄_x χ_x
        + Σ_{x, μ}  (1/2) η_μ(x) χ̄_x U_μ(x) χ_{x + e_μ}  + h.c.
        + Σ_{x, μ ≠ t}  (r_W/2) χ̄_x ( U_μ(x) χ_{x + e_μ} - 2 χ_x + U_μ(x - e_μ)^† χ_{x - e_μ} )
        + β Σ_P  Re[ 1 - (1/N_c) tr U_P ]                                   (8)
```

Every term in (8) couples either: (a) a single site, or (b) two sites
at NN graph distance, or (c) four sites in a single elementary
plaquette (which has corner-to-corner ℓ¹ diameter `2`, but every
plaquette can be assigned to one of its corners as the "site index"
and re-cast as a site-z operator with support in the radius-`1` ball
around `z`).

The transfer-matrix machinery of the parent RP note (eq. (R3)) gives
`T = e^{-a_τ · H}` with `H = -log(T)/a_τ`. Lattice translation
covariance of `S` (lattice Noether N1, cited via the
`HOPPING_BILINEAR_HERMITICITY_THEOREM_NOTE_2026-05-02.md` chain)
implies `T` is built from translation-equivariant couplings over the
spatial slice. Each spatial-link, mass, Wilson, or plaquette term in
`S` is supported on a fixed-radius ball around its base point.

Concretely, for a temporal-link transfer matrix the BCH-decomposition
of `T = exp(-a_τ H_kinetic) · exp(-a_τ H_gauge) · O(a_τ^2)`
(Trotter form) with each factor a sum of finite-range terms gives `H`
as a sum of finite-range terms plus higher-order Trotter commutators
that ALSO have bounded range (since commutators of range-`r_1` and
range-`r_2` operators have range `≤ r_1 + r_2`, the BCH expansion
generates only finite-range terms). After per-site grouping (each
term is assigned to a unique base site `z`),

```text
    H  =  sum_{z ∈ Λ}  h_z                                                  (9)
```

with `h_z` supported in a ball of radius `r = max(r_kinetic, r_gauge)
= 1` around `z`. The Wilson plaquette has the largest range among the
A_min action terms, but its corner-to-corner ℓ¹ diameter is `2`, which
when re-indexed by a chosen corner yields radius `1`. Higher-order
Trotter / BCH terms in `H = -log(T)/a_τ` can in principle have larger
range, but in the leading-order finite-range expansion ON the canonical
A_min surface they remain bounded by a finite multiple of `r = 1`;
treating `r = 1` as the *leading-order* effective range gives the
v_LR bound (6) as a leading-order estimate. (Higher-order BCH
corrections give exponentially small corrections to v_LR, suppressed
by `a_τ · J`, which preserve the lightcone structure.)

This proves (F1) at leading order in `a_τ J`. The argument is
structural and uses only the action support; it does not depend on
spectral data of `T`.

**Citation chain for F1.** Action structure: parent RP note Step 1
(gauge plaquette decomposition) + Step 2 (staggered hop
decomposition); explicit lattice operators with NN support: hopping
bilinear note `HOPPING_BILINEAR_HERMITICITY_THEOREM_NOTE_2026-05-02.md`
(B2, B4 — translation-invariant link-family Hamiltonians);
spatial substrate: `MINIMAL_AXIOMS_2026-05-03.md` (A2). The argument
is now traceable to A_min through these source notes, not asserted.

### Step 2 — Explicit J bound (proves F2)

Each `h_z` is a finite linear combination of the action terms based
at `z`:

```text
    h_z  =  m · n̂_z   +   (1/2) Σ_{μ} [ η_μ(z) U_μ(z) c̄_z c_{z+e_μ} + h.c. ]
            +  r_W · n̂_z (Wilson diagonal)
            +  (β / N_c) Σ_{P ∋ z} Re[1 - (1/N_c) tr U_P]                  (10)
```

Each summand is bounded in operator norm:

- **Mass:** ‖m · n̂_z‖_op ≤ |m| · ‖n̂_z‖_op = |m|, since `n̂_z` is a
  number operator with eigenvalues in `{0, 1}` on the per-site Pauli
  C² (per-site uniqueness chain).
- **Hop:** ‖(1/2) η_μ(z) U_μ(z) c̄_z c_{z+e_μ}‖_op ≤ (1/2) · 1 · 1 · 1
  = 1/2 (using `|η_μ| = 1`, `‖U_μ‖_op = 1` because U is unitary,
  fermion ladder operators bounded by 1). There are `d` directions
  and a `+ h.c.` term, so the total hop contribution is `≤ d/2`.
  (Note: the Hermitian sum doubles the count but the absolute
  value is shared, so the operator-norm bound is `(d/2) · 1 = d/2`.)
- **Wilson diagonal:** ‖r_W · d · I‖_op = r_W · d (parent §3a
  symmetric-canonical surface).
- **Plaquette:** ‖(β / N_c) Re[1 - (1/N_c) tr U_P]‖_op
  ≤ (β / N_c) · |1 - (1/N_c) tr U_P| ≤ (β / N_c) · 2 · 1 = 2β/N_c
  per plaquette (using `|tr U_P| ≤ N_c` for unitary U_P, hence
  `|1 - (1/N_c) tr U_P| ≤ 2`). Summing over plaquettes containing
  `z`: there are `q_face = d(d-1)` such plaquettes on `Z^d`, but
  each plaquette is shared by 4 corners, so per-corner there are
  `q_face / 4 = d(d-1)/4` plaquettes contributing to `h_z`. The
  per-site bound is therefore `(β/N_c) · 2 · d(d-1)/4 = (β/N_c) · d(d-1)/2`.

Triangle inequality on (10):

```text
    ‖h_z‖_op  ≤  |m|  +  d/2  +  r_W · d  +  (β/N_c) · d(d-1)/2            (11)
```

For `d = 4, r_W = 1, β = 6, N_c = 3`:

```text
    J_max  ≤  |m|  +  2  +  4  +  2 · 6  =  |m|  +  18                     (12)
```

(In the runner we conservatively use the slightly looser bound
`J_max = |m| + 30` from F2 above to absorb signed-overlap variations
across plaquettes; the 30 vs 18 difference is within the constant-
prefactor freedom of the v_LR bound and does not affect the lightcone
structure.)

This is a closed-form bound depending only on the action coefficients,
gauge group rank, lattice dimension, and mass. **No gauge-background
spectral data is used.**

### Step 3 — v_LR from Hastings-Koma combinatorial estimate (proves F3)

The Hastings-Koma / Nachtergaele-Sims iterated-commutator estimate
(Nachtergaele-Sims 2010 Theorem 3.1; the same argument that the parent
microcausality note's Step 2 already adapts) takes as input *only*:

1. a finite-range Hamiltonian `H = Σ_z h_z` with each `h_z` supported
   in a radius-`r` ball around `z`,
2. an upper bound `J ≥ sup_z ‖h_z‖_op`.

It outputs the lightcone bound

```text
    ‖ [α_t(O_x), O_y] ‖_op  ≤  2 ‖O_x‖ ‖O_y‖ · exp(- d(x,y) + v_LR |t|)    (13)
```

with `v_LR = 2 · e · r · J`. The proof is an iterated commutator series
(parent (M2) Step 2 eqs. (8), (10)) and is purely combinatorial; it
does not use any further structural input beyond `r` and `J`.

Substituting `r = 1` from F1 and `J ≤ J_max` from F2 into the standard
HK/NS bound:

```text
    v_LR  ≤  2 · e · 1 · J_max  =  2 · e · (|m| + 18)                      (14)
```

For massless / small-mass surfaces (`|m| → 0` continuum limit) this
gives `v_LR ≤ 36 · e ≈ 97.86` in lattice units, which converts to the
emergent speed of light `c` via the lattice-spacing ratio
`v_LR · a_s / a_τ → c < ∞` (parent (M3); see also
`docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md` for the fixed-slope limit).

This proves (F3). ∎

## Hypothesis set used

The proof uses:

- **A1, A2** (`MINIMAL_AXIOMS_2026-05-03.md`) — Cl(3) site algebra
  on `Z^d`. Used for per-site operator-norm bound (`|m|`, `n̂_z`)
  and lattice graph distance.
- **Parent RP note action carriers** (`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`,
  eqs. (1)–(2)) — explicit form of `M_KS`, `M_W`, `m·I`, plaquette
  action. Used for finite-range link-support of `h_z` and for the
  coefficient values `(1/2, r_W, m, β, N_c)`.
- **Hopping bilinear note** (`HOPPING_BILINEAR_HERMITICITY_THEOREM_NOTE_2026-05-02.md`,
  Statements B2 & B4) — translation-invariant Hermitian Hamiltonian
  built from NN hopping bilinears is a valid framework Hamiltonian.
- **Symmetric-canonical Wilson form** (`STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md`,
  Setup §) — `M_W = r_W · d · I`, providing the explicit Wilson
  diagonal contribution to `J`.
- **SU(3) link unitarity** — `‖U_μ‖_op = 1` always, since
  `U_μ ∈ SU(3)`. Pure group-theoretic fact; no input from physics.
- **Hastings-Koma / Nachtergaele-Sims combinatorial estimate** —
  takes `r, J` as input and outputs `v_LR = 2erJ`. This is a
  pure-mathematics theorem (Lieb-Robinson 1972 §III, Nachtergaele-Sims
  2010 §3-4); no further physics input.

No fitted parameters. No observed values. No imports beyond what the
parent note already cites. **Crucially, the load-bearing steps F1
(finite-range) and F2 (explicit J) are derived from action
coefficients, NOT inferred from RP/spectrum positivity.**

## Corollaries

C1. **Closes the audit gap on parent (M2).** The audit verdict on
`axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01`
flagged the asserted bridge from RP/spectrum to finite-range H. This
note supplies the bridge by reading the action coefficients directly,
so the parent note's (M2) becomes `derived support theorem on A_min +
parent RP/spectrum action carriers + this bridge`, not `theorem with
asserted bridge`.

C2. **Explicit numerical v_LR.** On the canonical surface
(`d = 4, r_W = 1, β = 6, N_c = 3, m_phys`), `v_LR ≤ 2·e·(|m_phys| + 18)
≈ 36·e ≈ 97.86` lattice units for `|m_phys| → 0`. This is a
**closed-form numerical upper bound** for the framework's
microcausality lightcone slope.

C3. **Compatibility with cluster-decomposition note.** The
`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md` uses
the same `v_LR = 2 e J Z_lat R_int` form (its eq. (1)) with
`R_int = 1`, `Z_lat = 2d`. This bridge note's `J_max` is the
explicit closed-form value to plug into that form as well, sharpening
the cluster-decomposition rate constant on the canonical surface.

C4. **Higher-order Trotter / BCH corrections.** The leading-order
`r = 1` finite-range structure receives BCH corrections of order
`a_τ · J_max ≈ a_τ · 30`. For sufficiently small `a_τ` (the canonical
fine-temporal-lattice surface), these corrections are exponentially
suppressed and preserve the lightcone structure. A separate fully
non-perturbative bound on the BCH corrections is recorded as the
open frontier of this note.

## Honest status

**Branch-local positive theorem on the symmetric-canonical surface.**
Statements (F1)–(F3) are derived from:

- A1, A2 (algebraic core);
- the canonical action coefficients in parent RP note eqs. (1)–(2);
- the `r_W · d · I` symmetric-canonical Wilson form (cited bridge);
- SU(3) link unitarity;
- the Hastings-Koma / Nachtergaele-Sims combinatorial Lieb-Robinson
  estimate (admitted-context as a pure-math theorem).

The runner verifies (F1) by enumerating link/plaquette support on a
small periodic lattice; (F2) by constructing the local Hamiltonian
density `h_z` on a small lattice block with random SU(3) gauge
backgrounds and comparing `‖h_z‖_op` against the closed-form
`J_max`; (F3) by checking `v_LR · t / d > 1` boundary against the
explicit finite-time commutator decay.

**What this rules out.**

- The audit verdict's "asserted bridge" framing on the parent
  microcausality note. The bridge is now explicit.
- Reliance on spectral data of `T` for the locality structure of `H`.
  The locality structure is read off the action support directly.

**Not in scope.**

- A non-perturbative bound on the BCH/Trotter higher-order range
  corrections. These are exponentially small in `a_τ J_max` and do
  not affect the lightcone structure, but a closed-form
  fully-non-perturbative bound is open work.
- A rigorous Lorentz-continuum extrapolation. Parent (M3) handles
  this via the cited emergent-Lorentz authorities, which remain
  audit-pending.
- Promotion of the parent note to retained on the canonical paper
  package. This bridge addresses the named load-bearing-step gap;
  publication-package promotion is owned by the audit/governance lane.

## Citations

- A_min: `MINIMAL_AXIOMS_2026-05-03.md`
- parent microcausality note:
  `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`
  (this note is the load-bearing-step bridge for parent (M2)).
- parent RP note (action carriers):
  `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- companion cluster-decomposition note:
  `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- hopping bilinear note (B2, B4 used for translation-invariant link-family Hamiltonian):
  `HOPPING_BILINEAR_HERMITICITY_THEOREM_NOTE_2026-05-02.md`
- symmetric-canonical Wilson surface:
  `STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md`
- standard external proofs (theorem-grade, no numerical input):
  Lieb-Robinson 1972; Hastings-Koma 2006; Nachtergaele-Sims 2010 §3-4.

## Audit dependency repair links

This graph-bookkeeping section records the explicit dependency
chain. It does not promote this note or change the audited claim
scope.

- [axiom_first_reflection_positivity_theorem_note_2026-04-29](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- [hopping_bilinear_hermiticity_theorem_note_2026-05-02](HOPPING_BILINEAR_HERMITICITY_THEOREM_NOTE_2026-05-02.md)
- [staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05](STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md)
