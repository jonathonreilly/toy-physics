# SO(3) Isotypic Orbit-Flat Narrow Theorem on `Sym^2(R^4)`

**Date:** 2026-05-10
**Claim type:** positive_theorem
**Primary runner:** [`scripts/frontier_universal_gr_so3_isotypic_orbit_flat_narrow.py`](./../scripts/frontier_universal_gr_so3_isotypic_orbit_flat_narrow.py)

## Claim scope (proposed)

> Let `h ∈ Sym^2(R^4)` be a symmetric `4×4` real matrix. Let
> `R ∈ SO(3)` act on `R^4` by `R = 1 ⊕ R_3`, i.e. block-diagonally with
> the temporal index fixed and `R_3` rotating the spatial indices
> `1, 2, 3`. Define `h' := R^T h R`. Define the rank-2 projector
>
> ```text
> Pi_A1(h) := diag( h_{00},  s/3,  s/3,  s/3 ),    s := h_{11} + h_{22} + h_{33},
> ```
>
> Here `Pi_A1` is a representation-label alias for the SO(3)-trivial
> lapse/spatial-trace projector, not a repo axiom label.
>
> and `Pi_perp(h) := h - Pi_A1(h)`. Define the diagonal-weighted
> Frobenius energy
>
> ```text
> ||h||^2_d  :=  sum_{i,j}  h_{ij}^2 / (d_i d_j),
> ```
>
> for any **isotropic spatial weight** `d = (d_0, d_s, d_s, d_s)` with
> `d_0, d_s > 0`.
>
> **Then for every `R ∈ SO(3)`:**
>
> 1. **(T1) SO(3)-trivial block is pointwise SO(3)-invariant:**
>    `Pi_A1(h') = Pi_A1(h)`.
> 2. **(T2) Complement L²-energy is orbit-flat:** `||Pi_perp(h')||^2_d = ||Pi_perp(h)||^2_d`.
> 3. **(T3) Complement coordinates do move:** for generic `(h, R)`,
>    `Pi_perp(h') ≠ Pi_perp(h)` as a tensor in `Sym^2(R^4)`, even though
>    its energy is conserved.
>
> **Corollary (orbit-flat selection no-go).** For any `α, β ∈ R`, the
> quadratic energy functional
>
> ```text
> E_{α,β}[h]  :=  α ||Pi_A1(h)||^2_d  +  β ||Pi_perp(h)||^2_d
> ```
>
> satisfies `E_{α,β}[h'] = E_{α,β}[h]` for all `R ∈ SO(3)`. Hence no
> stationarity / minimization of `E_{α,β}` selects a unique
> complement-frame section: any spatial frame in the SO(3) orbit
> realizes the same quadratic energy.

This is a pure linear-algebra / SO(3)-representation-theory result. It
**does not** claim:

- that the quadratic functional `E_{α,β}` is the physical
  Einstein-Hilbert action;
- that the spatial-isotropic background `d = (d_0, d_s, d_s, d_s)` is
  the physical background of any specific lattice gravity construction;
- a result about the universal GR route in its entirety — the
  corollary applies only to the **quadratic** SO(3)-equivariant energy
  class defined above and gives only an orbit-flat selection statement
  for that class;
- closure (or non-closure) of the universal `PL S^3 x R` GR program.

## Dependencies

None. This narrow note has zero load-bearing dependencies because it
states only elementary linear-algebra and SO(3)-representation-theory
facts on abstract `Sym^2(R^4)` with an abstract spatial-block SO(3)
action. The proof uses only `R_3^T R_3 = I` (orthogonal-group
invariance) and elementary tensor/Frobenius-norm identities — no
framework axiom, no physical input, no other note's result is
consumed.

The framework baseline memo `MINIMAL_AXIOMS_2026-05-03` is named in
plain text, not as a load-bearing markdown link. It records the physical
Cl(3) local algebra and Z^3 spatial substrate baseline; that connection
is informational, not load-bearing for the present theorem.

## Load-bearing step (class (A))

**Step 1 — SO(3)-trivial block is pointwise invariant.** Write `h` in the canonical
`3+1` block form:

```text
       [ h_{00}    h_{0i} ]
h  =   [                  ],
       [ h_{i0}    h_{ij} ]
```

with `h_{0i}, h_{i0} ∈ R^3` (transposed columns/rows) and
`h_{ij} ∈ Sym^2(R^3)`. Under `R = 1 ⊕ R_3`,

```text
h'_{00}  =  h_{00},                                                       (1a)
h'_{0i}  =  (R_3)_{ji} h_{0j},                                            (1b)
h'_{ij}  =  (R_3)_{ki} (R_3)_{lj} h_{kl}.                                 (1c)
```

The SO(3)-trivial block is `(h_{00}, s/3 · I_3)` with
`s = tr(h_{ij}) = h_{kk}`.
Lapse invariance is `(1a)`. For the spatial trace,
`tr(h'_{ij}) = (R_3)_{ki} (R_3)_{li} h_{kl} = δ_{kl} h_{kl} = h_{kk} = s`,
using `R_3^T R_3 = I`. Thus `Pi_A1(h') = Pi_A1(h)` pointwise.

**Step 2 — Spatial Frobenius norm is SO(3)-invariant.** For any
`A ∈ Mat(3,R)` and `R_3 ∈ SO(3)`, the standard Frobenius norm is
orthogonally invariant:

```text
||R_3^T A R_3||_F^2  =  tr(R_3^T A^T R_3 R_3^T A R_3)  =  tr(A^T A)  =  ||A||_F^2.   (2)
```

Apply `(2)` to `A = h_{ij}`: `sum_{i,j} (h'_{ij})^2 = sum_{i,j} (h_{ij})^2`.
Similarly for the shift covector `h_{0i}`:
`sum_i (h'_{0i})^2 = sum_i (R_3)_{ji} (R_3)_{ki} h_{0j} h_{0k}
= sum_j (h_{0j})^2`, again by `R_3^T R_3 = I`.

**Step 3 — Total weighted energy is invariant under isotropic spatial
weight.** With `d = (d_0, d_s, d_s, d_s)` the diagonal weight matrix
`W := diag(1/d_0, 1/d_s, 1/d_s, 1/d_s)` satisfies `R^T W R = W`, since
`R = 1 ⊕ R_3` and `R_3^T (1/d_s · I_3) R_3 = (1/d_s) I_3`. Hence

```text
||h'||^2_d  =  tr(W h' W h')
             =  tr(W R^T h R W R^T h R)
             =  tr(W h W h)
             =  ||h||^2_d,
```

Concretely, expanding by sectors:

```text
||h'||^2_d  =  (h'_{00})^2 / d_0^2
              + 2 sum_i (h'_{0i})^2 / (d_0 d_s)
              + sum_{i,j} (h'_{ij})^2 / d_s^2
            =  (h_{00})^2 / d_0^2
              + 2 sum_i (h_{0i})^2 / (d_0 d_s)
              + sum_{i,j} (h_{ij})^2 / d_s^2
            =  ||h||^2_d.
```

The cross-sector and within-sector identifications use Steps 1–2.

**Step 4 — SO(3)-trivial block energy is invariant.** `Pi_A1(h')` and `Pi_A1(h)`
are equal by Step 1, so their `||·||^2_d` energies are trivially equal.

**Step 5 — Complement energy is invariant by subtraction.** Since the
SO(3)-trivial block is pointwise fixed (Step 1) and `||·||^2_d` is additive across
the orthogonal direct-sum `Pi_A1 ⊕ Pi_perp` (the `Pi_A1` block is supported
only on the diagonal `(00, 11, 22, 33)` slots while `Pi_perp` carries
the off-diagonal slots and the spatial-traceless diagonal piece — these
overlap only via the spatial trace, which `Pi_perp` annihilates by
construction), we have

```text
||Pi_perp(h')||^2_d
  =  ||h'||^2_d  -  ||Pi_A1(h')||^2_d
  =  ||h||^2_d  -  ||Pi_A1(h)||^2_d
  =  ||Pi_perp(h)||^2_d.
```

Step 5 gives `(T2)`.

**Step 6 — Complement coordinates move.** For a generic spatial
rotation by angle `θ ≠ 0` around any axis and a generic `h`, the shift
sector `(h_{01}, h_{02}, h_{03})` rotates as a 3-vector and the
spatial-traceless part rotates as a spin-2 tensor. Both sectors contain
non-trivial SO(3) representations; their pointwise values change under
non-identity `R_3`. Concrete witness: take `h_{01} = h_{10} = 1`, all
other components zero, and `R_3 = R_z(π/2)` (rotation by 90° around
the z-axis). Then under `h' = R^T h R`:

```text
h'_{0,j}  =  sum_k (R_z_{90})_{k,j} h_{0,k}
            =  (R_z_{90})_{1,j} · 1   (only h_{0,1} is nonzero)
            =  delta_{j,2} · (R_z_{90})_{1,2}
            =  delta_{j,2} · (-1).
```

So `h'_{0,1} = 0` and `h'_{0,2} = -1`. The shift index has rotated
from slot 1 to slot 2 (vector covariance), and `Pi_perp(h')` differs
from `Pi_perp(h)` in two off-diagonal slots while their `||·||^2_d`
energies are equal (both `= 2/(d_0 d_s)`).

**Step 7 — Corollary.** `E_{α,β}[h'] = α ||Pi_A1(h')||^2_d + β
||Pi_perp(h')||^2_d = α ||Pi_A1(h)||^2_d + β ||Pi_perp(h)||^2_d =
E_{α,β}[h]`, by Steps 4 and 5. ∎

Each step uses only elementary linear-algebra identities
(`R_3^T R_3 = I`, Frobenius-norm orthogonal invariance, additivity of
`||·||^2_d` across the `Pi_A1 ⊕ Pi_perp` split). Class **(A)** load-bearing
step throughout.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_universal_gr_so3_isotypic_orbit_flat_narrow.py
```

Verifies, at exact symbolic precision via `sympy.trigsimp` /
`sympy.simplify` and at machine precision via `numpy` random sampling:

1. **Symbolic (T1):** `Pi_A1(R^T h R) - Pi_A1(h) ≡ 0` as a symbolic
   matrix identity in `(h_{00}, ..., h_{33}, φ, θ, ψ)`.
2. **Symbolic (T2):** `||Pi_perp(R^T h R)||^2_d - ||Pi_perp(h)||^2_d ≡ 0`
   as a symbolic identity for isotropic spatial weight `(d_0, d_s, d_s, d_s)`.
3. **Symbolic anisotropic-control:** with anisotropic spatial weight
   `(d_0, d_1, d_2, d_3)` having `d_1 ≠ d_2`, the complement energy is
   **not** invariant — confirms the isotropic premise is load-bearing.
4. **Symbolic shift-covariance:** `h_{0i}` rotates as a 3-vector under
   `R_3` (sample identity check on `h_{01}^2 + h_{02}^2 + h_{03}^2`).
5. **Symbolic spatial-traceless covariance:** the spin-2 component of
   `h_{ij}` mixes non-trivially under `R_3` (concrete witness on a
   chosen `(h, R_3)`).
6. **Numerical (T1+T2) on random samples:** for 200 random
   `(h, R_3) ∈ Sym^2(R^4) × SO(3)`, `|Pi_A1(h') - Pi_A1(h)| < 1e-13`
   and `|||Pi_perp(h')||^2_d - ||Pi_perp(h)||^2_d| < 1e-13`.
7. **Numerical (T3) on random samples:** for 200 random
   `(h, R_3 ≠ I)`, `|Pi_perp(h') - Pi_perp(h)|_max > 1e-3` on a
   non-trivial fraction of samples — coordinates move.
8. **Corollary on random `(α, β)`:** `|E_{α,β}[h'] - E_{α,β}[h]| <
   1e-13` for 200 random `(α, β, h, R_3)`.
9. **Concrete witness:** `h_{01} = 1, R_3 = R_z(π/2)` gives
   `h'_{01} = 0, h'_{02} = 1` (shift rotates as vector),
   `||Pi_perp(h')||^2_d = ||Pi_perp(h)||^2_d` exactly.
10. **Context references exist.** `MINIMAL_AXIOMS_2026-05-03`
    is the framework baseline memo (context only, no upstream dependency).

## Audit-Lane Disposition

Claim type is `positive_theorem`. The proposed claim scope is the pure
SO(3)-representation-theory / linear-algebra orbit-flat invariance:
under spatial-block SO(3) action on `Sym^2(R^4)` and isotropic spatial
diagonal weight, the rank-2 SO(3)-trivial block (lapse + spatial trace)
is pointwise invariant and the orthogonal-complement weighted energy is
orbit-flat, so no quadratic-energy minimization in this class can
canonically select a unique complement-frame section. This is not a
physical Einstein-Hilbert or lattice-gravity-action claim.

Audit status is set only by the independent audit lane. This source note
does not write or predict an audit verdict.

## What this theorem provides

A clean, reusable structural lemma that downstream universal-GR notes
can cite without scope-creep concerns. Specifically, the orbit-flat
behavior of a quadratic SO(3)-equivariant energy on `Sym^2(R^4)` with
isotropic spatial weight is now a standalone audit candidate,
independent of the universal-GR route's other
premises. Downstream notes that previously needed to re-derive or
reassert this orbit-flatness can cite the present theorem as a
class-(A) algebraic identity.

## What this theorem does NOT close

- The full universal-GR route on `PL S^3 × R` — the present theorem
  isolates only the SO(3)-orbit-flat selection structure for a
  quadratic energy class with isotropic spatial weight; it does not
  address curvature localization, the polarization-frame bundle
  problem, or the Lorentzian-signature extension.
- Whether higher-order (cubic, quartic, ...) SO(3)-equivariant
  functionals on `Sym^2(R^4)` could distinguish complement-frame
  sections — out of scope; the corollary is restricted to the
  quadratic class.
- Whether anisotropic spatial weights yield a different selection
  picture — the symbolic anisotropic control test confirms the
  isotropic premise is load-bearing; non-isotropic backgrounds are
  outside the present scope.

## Relation to parent universal-GR notes (informational, not load-bearing)

`MINIMAL_AXIOMS_2026-05-03` is the framework baseline memo for the
physical Cl(3) local algebra and Z^3 spatial substrate. The present
narrow theorem isolates a pure linear-algebra orbit-flatness fact and
does not consume that baseline as a load-bearing premise.

`UNIVERSAL_GR_CONSTRAINT_ACTION_STATIONARITY_NOTE` is the parent note
where this orbit-flat structure was first observed in the universal-GR
context. The parent note's broader claim about the full universal-GR
route remains in its current audit state; the present narrow theorem
isolates only the underlying linear-algebra fact and is independent of
any broader universal-GR claim.

`UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE` is a sister note recording the
A1 invariant section. The present narrow theorem extends the
A1-invariance fact (`(T1)`) to a complement-energy orbit-flatness fact
(`(T2)`) under the isotropic-spatial-weight premise.

These references are plain-text pointers for readers, not
load-bearing dependencies. The citation graph builder follows
markdown-link arrows; this section deliberately uses bare paths to
avoid wiring non-retained-grade rows into the retention chain of a
self-contained linear-algebra theorem.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.
- No new axioms introduced — the theorem is on abstract `Sym^2(R^4)`
  with a generic SO(3) action; framework axioms appear only as a
  cross-reference anchor.
- No new repo vocabulary — the note uses canonical narrow-theorem
  template structure (mirroring `KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02`
  and `SCHUR_COVARIANCE_INHERITANCE_NARROW_THEOREM_NOTE_2026-05-02`,
  cited here as plain-text pattern references only) and standard
  linear-algebra terminology only.
