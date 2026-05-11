# Hierarchy Matsubara Quartic Coefficient Ratio — Narrow Algebraic Theorem

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status:** bounded - exact algebraic coefficient computation; not a
Higgs quartic closure or lambda-UV anchor.
**Primary runner:** [`scripts/frontier_hierarchy_matsubara_quartic_coefficient_ratio_narrow.py`](../scripts/frontier_hierarchy_matsubara_quartic_coefficient_ratio_narrow.py)

## 0. Context

The framework's hierarchy free-energy density has a known small-m
expansion
[`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md):

```text
Δf(L_t, m)  =  A(L_t) · m²  +  B(L_t) · m⁴  +  O(m⁶).
```

The `m²` coefficient `A(L_t)` is recorded and used downstream:
`A_2 = 1/(8u_0²)`, `A_4 = 1/(7u_0²)`, `A_inf = 1/(4√3 u_0²)`. The `m⁴`
coefficient `B(L_t)` has not been computed in a source note.
This omission is load-bearing for at least two open questions:

1. **The `λ(M_Pl) = 0` claim** in
   [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
   asserts a vanishing high-scale Higgs quartic from a "framework-native
   composite-Higgs / no-elementary-scalar boundary structure." If the
   induced quartic from integrating out staggered fermions is finite and
   positive, the slogan "no bare quartic ⟹ λ(M_Pl) = 0" is false on
   the framework's own surface (NJL counterexample).

2. **The scale of the tree-level mean-field readout `m_H = v/(2u_0)`** in
   [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) is
   currently ambiguous: the curvature reading at the symmetric point
   plus a separate quartic identification would settle whether
   `1/(8u_0²)` lives at the lattice cutoff or at the EW scale.

This narrow theorem closes the algebraic computation of `B(L_t)` and
records the structural ratio `|B(L_t=4)|/|B(L_t=2)| = (8/7)^2` as a
clean algebraic identity. It does NOT itself establish any lambda-UV-anchor
claim.

## 1. Claim scope

> **Theorem (Matsubara quartic coefficient).** On the minimal spatial
> APBC block `L_s = 2` of the staggered Dirac operator on `Z⁴`, with the
> mean-field gauge factorization (admitted standard mean-field
> convention; same setup as
> [`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md)),
> the small-m expansion of the free-energy density
> `Δf(L_t, m) = (1/(2L_t)) Σ_ω log(1 + m²/(u_0²(3+sin²ω)))`
> has the **exact rational m⁴ coefficient**:
>
> ```text
> B(L_t)  =  -(1 / (4 L_t u_0⁴))  ·  Σ_ω  1 / (3 + sin²ω)².
> ```
>
> Specialized to `L_t ∈ {2, 4}`:
>
> ```text
> B(L_t = 2)  =  -1 / (64 u_0⁴)     (single APBC mode at sin²ω = 1)
> B(L_t = 4)  =  -1 / (49 u_0⁴)     (four uniformly-weighted modes at sin²ω = 1/2).
> ```
>
> The cross-endpoint quartic ratio is
>
> ```text
> |B(L_t = 4)|  /  |B(L_t = 2)|  =  64 / 49  =  (8/7)²  =  (A(L_t=4) / A(L_t=2))².
> ```

The narrow theorem **explicitly does NOT** claim:

- the Higgs scalar quartic `λ_H` — the m⁴ coefficient of `Δf` is the
  fermion-induced quartic in lattice units, not directly the SM Higgs
  EFT quartic without a separate matching theorem;
- a UV-anchor framework prediction for `λ(M_Pl)` — that would require a
  matching from the lattice fermion-bilinear theory onto the SM Higgs
  EFT, which is open;
- a Higgs mass extraction — that would require a specific readout
  convention (standard `v² = A/(2λ_eff)` from `B`, vs the
  framework's existing `m_H = v/(2u_0)` reading) which this note does
  not pick.

## 2. Admitted dependencies

| Authority | Role | Detail |
|---|---|---|
| Cl(3) Clifford identity `D_taste² = d · I` | admitted standard staggered fermion algebra | parent narrow theorem |
| Mean-field factorization `U_{ab} → u_0 δ_{ab}` | admitted standard mean-field convention | parent narrow theorem |
| `L_s = 2` minimal APBC block | admitted block-size choice; pins spatial momenta to BZ corners (sin²(k_i) = 1) | parent narrow theorem |
| Standard staggered Dirac dispersion `λ²(k, ω) = u_0² Σ_μ sin²(k_μ)` | admitted standard staggered fermion algebra | parent narrow theorem |

All dependencies are inherited from
[`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md).
The expansion of `log(1 + ε)` at `ε → 0` is standard analysis. No new
admissions.

## 3. Load-bearing step (class A)

```text
Starting from the parent decomposition:

  Δf(L_t, m)  =  (1 / (2 L_t))  ·  Σ_ω  log(1 + m² / (u_0² (3 + sin²ω))).      (1)

For each Matsubara mode ω, set ε_ω(m) := m² / (u_0² (3 + sin²ω)).

Standard Taylor expansion log(1 + ε) = ε - ε²/2 + ε³/3 - O(ε⁴):

  log(1 + ε_ω)  =  m² / (u_0² (3+s²))  -  m⁴ / (2 u_0⁴ (3+s²)²)  +  O(m⁶).    (2)

Summing over modes and dividing by 2 L_t:

  Δf  =  m² · A(L_t)  +  m⁴ · B(L_t)  +  O(m⁶)                                 (3)

with

  A(L_t)  =  (1 / (2 L_t u_0²))  ·  Σ_ω  1 / (3 + sin²ω)                       (4)

  B(L_t)  =  -(1 / (4 L_t u_0⁴))  ·  Σ_ω  1 / (3 + sin²ω)².                    (5)

Specialize to L_t = 2 and L_t = 4 using the Klein-four orbit closure
(sin²ω ∈ {1, 1} at L_t=2; sin²ω = 1/2 uniformly at L_t=4) inherited
from HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md:

  L_t = 2:  Σ_ω 1/(3+s²)²  =  2 · (1/16)        =  1/8
            B(2)            =  -(1/(8 u_0⁴)) · (1/8)
                            =  -1 / (64 u_0⁴).                                 (6)

  L_t = 4:  Σ_ω 1/(3+s²)²  =  4 · (1/(7/2)²) = 4 · 4/49  =  16/49
            B(4)            =  -(1/(16 u_0⁴)) · (16/49)
                            =  -1 / (49 u_0⁴).                                 (7)

Form the ratio:

  |B(L_t = 4)|     1 / (49 u_0⁴)         64
  ────────────  =  ─────────────────  =  ───  =  (8/7)².                        (8)
  |B(L_t = 2)|     1 / (64 u_0⁴)         49

The u_0 cancels. The ratio is the SQUARE of the inverse m² coefficient
ratio:

  A(L_t = 4)  /  A(L_t = 2)  =  (1/(7 u_0²)) / (1/(8 u_0²))  =  8/7,            (9)

so

  |B(L_t = 4)|  /  |B(L_t = 2)|  =  (A(L_t = 4) / A(L_t = 2))² .                (10)

This is class (A) — algebraic identity on the parent narrow theorem's
closed-form determinant plus standard log-Taylor expansion. ∎
```

## 4. Structural implications (named, not derived)

### 4.1 Composite-Higgs slogan retired (named obstruction)

The slogan "no fundamental scalar in the bare action ⟹ `λ(M_Pl) = 0`"
in
[`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
treats `λ(M_Pl) = 0` as a framework-native consequence of the lack of
an elementary scalar in the gauge-fermion lattice action. The honest
computation here gives a **finite, nonzero** induced quartic at the
lattice scale on `L_t ∈ {2, 4}`:

```text
B(L_t = 2)  =  -1 / (64 u_0⁴)  ≠  0
B(L_t = 4)  =  -1 / (49 u_0⁴)  ≠  0.
```

The induced quartic from integrating out staggered fermions is the
analogue of the NJL/top-condensation result that a composite scalar
generically has a finite quartic at its matching scale (Bardeen-Hill-
Lindner 1990). The slogan conflates "no bare quartic in the lattice
action" (true) with "induced quartic vanishes at the matching scale"
(false on this computation).

This is a **named obstruction** to the composite-Higgs route: a useful
negative finding that saves further effort from a structurally unsound
slogan.

### 4.2 The `(8/7)²` ratio as a structural identity

The cross-endpoint identity
`|B(L_t=4)|/|B(L_t=2)| = (A(L_t=4)/A(L_t=2))² = (8/7)²`
follows from the per-mode integrand structure: A is the Σ over
`1/(3+sin²ω)`, B is the Σ over `1/(3+sin²ω)²` (one extra factor per
mode), and the L_t=4 mode at `sin²ω = 1/2` differs from the L_t=2 mode
at `sin²ω = 1` by exactly the per-mode factor `(8/7)`, so B (which is
the sum of squares of the per-mode factor) inherits exactly the square
ratio.

### 4.3 Standard Higgs minimum readout — not the framework's chosen reading

If one applied the standard Higgs minimum extraction
`v² = A(L_t) / (2 |B(L_t)|)`:

```text
v²(L_t = 2)  =  (1/(8 u_0²))  /  (2 · 1/(64 u_0⁴))  =  4 u_0²
v²(L_t = 4)  =  (1/(7 u_0²))  /  (2 · 1/(49 u_0⁴))  =  7 u_0² / 2

v(L_t = 4) / v(L_t = 2)  =  √(7/8)  =  (7/8)^(1/2)  ≈  0.9354.
```

This compression is **(7/8)^(1/2), not (7/8)^(1/4)**. The framework's
existing `(7/8)^(1/4)` compression in
[`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
and
[`HIERARCHY_MATSUBARA_DETERMINANT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_MATSUBARA_DETERMINANT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md)
is therefore **NOT** the standard `v² = -μ²/(2λ)` Higgs minimum — it is
a different readout (per-mode geometric-mean of the determinant, see
the cited determinant-ratio note §4 corollary).

## 5. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_matsubara_quartic_coefficient_ratio_narrow.py
```

Verifies, at exact rational precision via Python `Fraction` AND symbolic
differentiation via SymPy:

1. The Taylor expansion of `log(1 + ε)` to `O(ε²)` reproduces (4) and
   (5) for the small-m coefficients.
2. Direct symbolic computation: `∂²Δf/∂m²|_{m=0} / 2 = A(L_t)` and
   `∂⁴Δf/∂m⁴|_{m=0} / 24 = B(L_t)` for `L_t ∈ {2, 4}`.
3. `A_2 = 1/(8 u_0²)`, `A_4 = 1/(7 u_0²)` (parent narrow theorem
   re-derivation as cross-check).
4. `B_2 = -1/(64 u_0⁴)`, `B_4 = -1/(49 u_0⁴)` exactly.
5. `|B_4|/|B_2| = 64/49 = (8/7)² = (A_4/A_2)²` exactly.
6. Sign assertion: `B(L_t) < 0` for both endpoints (the m⁴ coefficient
   of Δf is negative; this is opposite-sign from V_taste's m⁴ coefficient
   in HIGGS_MASS_FROM_AXIOM Step 4 because Δf and V_taste differ by an
   overall sign convention).
7. Standard Higgs minimum readout `v(L_t=4)/v(L_t=2) = (7/8)^(1/2)`
   computed and explicitly distinguished from the framework's
   `(7/8)^(1/4)` per-mode readout.

## 6. Audit scope

This is a bounded_theorem source row. The scope is the pure algebraic
`m^4` coefficient computation on the staggered Dirac free-energy density
at `L_s = 2` APBC mean field:

```text
B(L_t) = -(1/(4 L_t u_0^4)) * Sum_omega 1/(3+sin^2 omega)^2.
```

Specialized at `L_t in {2, 4}`:

```text
B_2 = -1/(64 u_0^4),  B_4 = -1/(49 u_0^4),
|B_4|/|B_2| = 64/49 = (8/7)^2.
```

The named obstruction corollary is that the slogan "composite Higgs
implies lambda(M_Pl) = 0" is retired by the finite, nonzero induced
quartic at the lattice scale. This note does not close a Higgs EFT
matching theorem or a lambda-UV anchor.

The narrow theorem is class (A) algebraic on admitted-standard staggered
fermion algebra (parent narrow theorem) plus standard analysis (Taylor
expansion of log). No new physical admissions.

## 7. What this theorem closes

- **B(L_t) explicitly computed** at endpoints L_t ∈ {2, 4}: clean
  rational values verifiable by symbolic differentiation.
- **Cross-endpoint ratio identity** `|B_4|/|B_2| = (A_4/A_2)² = (8/7)²`
  as a clean class (A) algebraic statement.
- **Composite-Higgs slogan named obstruction**: the induced quartic
  from integrating out staggered fermions is finite and nonzero, so
  the "composite ⟹ λ(M_Pl) = 0" slogan is structurally retired on
  the framework's own surface.
- **Sharpens the Higgs-mass readout question**: standard
  `v² = A/(2|B|)` gives `(7/8)^(1/2)` compression, NOT the framework's
  `(7/8)^(1/4)` reading. So the framework is using a non-standard
  readout (the per-mode geometric mean from the determinant identity
  note), and this is now explicitly distinguished.

## 8. What this theorem does NOT close

- The Higgs scalar quartic `λ_H` itself (requires UV→SM-EFT matching
  theorem; open).
- The `λ(M_Pl)` UV anchor (this note retires one heuristic route but
  does not provide a positive replacement).
- The scale at which `B(L_t)` is to be matched onto the SM Higgs EFT
  (lattice cutoff vs effective scale; standard Wilsonian-vs-1PI
  distinction; open).
- The framework's specific Higgs mass formula `m_H = v/(2u_0)`
  (depends on a separate readout choice, not standard Higgs minimum).

## 9. Cross-references

### Parent / specialization
- [`HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md`](HIERARCHY_MATSUBARA_DETERMINANT_NARROW_THEOREM_NOTE_2026-05-02.md)
  — parent narrow theorem; this note carves out the m⁴ coefficient.
- [`HIERARCHY_MATSUBARA_DETERMINANT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_MATSUBARA_DETERMINANT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md)
  — sister theorem on the determinant ratio identity; the (8/7)²
  pattern of B mirrors the (7/8)^16 pattern of det.
- [`HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md`](HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md)
  — has the A(L_t) endpoint formulas; this note adds B(L_t).

### Framework Higgs / vacuum claims being sharpened
- [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
  — claims `λ(M_Pl) = 0` from composite-Higgs heuristic; this note
  retires the heuristic.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — tree-level mean-field readout `m_H = v/(2u_0)`; this note shows the
  reading is non-standard (not `v² = A/(2|B|)`).
- [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md)
  — assumption-derivation ledger flags `λ(M_Pl) = 0` as "weakest leg of
  input chain"; this note quantitatively confirms the gap.

### Framework axioms / structural
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
  — Klein-four orbit selection of L_t = 4.

### Standard physics references (admitted-context literature, not load-bearing)
- Bardeen, Hill, Lindner (1990) — top-condensation NJL counterexample
  to "composite ⟹ λ = 0".
- Coleman & Weinberg (1973) — radiative corrections, induced quartic.
