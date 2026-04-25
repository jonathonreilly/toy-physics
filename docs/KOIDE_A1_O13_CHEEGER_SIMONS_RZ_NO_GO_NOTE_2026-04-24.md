# Koide A1 — O13 Cheeger-Simons R/Z Period Inheritance No-Go

**Date:** 2026-04-24
**Lane:** Koide A1 / radian-bridge irreducibility — frontier mathematical-literature audit.
**Status:** **NO-GO.** The Cheeger-Simons differential-character functor does
not close the radian-bridge postulate P. The probe confirms a new obstruction
class **O13** which is a sharp subcase of O10 (Universal Lattice Closure /
Lindemann transcendence wall).
**Runner:** `scripts/frontier_koide_a1_cheeger_simons_rz_probe.py` (49/49 PASS,
PASS = obstruction-confirmed).

---

## 0. Summary

Cheeger-Simons differential characters `Ĥ^k(M; R/Z)` are the canonical
R/Z-valued (i.e. fractional, mod-1) cohomological refinement of integer
characteristic classes, generalizing the Chern-Simons invariant to
non-closed bases without requiring closed-loop topology. They are the
natural target of any "fractional cohomological 2/9" route that hopes to
escape the (rational)·π wall established by O10.

This probe asks: **does the CS framework provide a retained physical
structure on Cl(3)/Z³ that maps a fractional-mod-1 invariant to a literal
radian (not a rational multiple of π)?**

Result: **NO**. The CS framework provides a perfectly clean R/Z-valued
class with holonomy `2/9 mod 1` around the Z₃ generator (equivalently the
ABSS η-invariant of the lens space `L(3,1)`). However the canonical
isomorphism `R/Z → U(1)` is `χ(c) = exp(2πi·c)`, giving phase
`exp(4πi/9)` whose argument is `(4/9)π` — a rational multiple of π,
exactly on the Lindemann wall. To bridge from `c = 2/9 mod 1` to a literal
`2/9 rad` requires using the non-canonical convention `χ'(c) = exp(i·c)`
(period `1 rad` instead of `2π rad`); this is a renaming of postulate P,
not a derivation.

The CS framework therefore adds a **seventh independent dimensionless 2/9
source** (coinciding with the ABSS η at the level of holonomy), but it
does not bridge to a literal-radian 2/9. The new obstruction is named:

> **O13 — Cheeger-Simons R/Z period inheritance.** Differential characters
> `Ĥ^k(M; R/Z)` carry their R/Z period as a *defining* part of the
> functor, identified with U(1) via `exp(2πi·.)`. Phase angles extracted
> from CS classes are therefore `(rational)·π`. CS does not escape the
> (rational)·π wall; it sits downstream of O10.

---

## 1. Origin: why this probe was attempted

The mathematical-literature audit in this lane is methodically scanning
canonical quantization theorems for any that bridge a fractional invariant
to a literal radian. Standard Dirac/TKNN/Chern-Simons quantization all
require closed-loop topology + integer-valued invariants + 2π
normalization, producing `(rational)·2π` phases. They do not bridge to a
literal radian.

Cheeger-Simons differential characters are the canonical *secondary*
characteristic classes that:

1. Refine integer cohomology to `R/Z` (not just integer-valued).
2. Are well-defined on **non-closed** bases (no closed-loop requirement).
3. Are R/Z-valued by definition, providing fractional-mod-1 invariants
   without any prior 2π normalization in the codomain.

This makes CS the natural mathematical home for any retained
"fractional-mod-1 = 2/9" claim. Because the framework retains the ABSS
η-invariant `η(Z_3, weights (1,2)) = 2/9 mod ℤ`, and because the η-invariant
canonically lifts to a CS class in `Ĥ^1(L(3,1); R/Z)`, there is a clean
candidate construction to test.

The probe was designed to exhaustively answer: under what convention
does this CS class produce a literal-radian phase, and is that convention
retained?

---

## 2. Mathematical setup

### 2.1 Cheeger-Simons functor on retained Cl(3)/Z³

For a smooth manifold or finite CW/cubical complex `M`, the
**Cheeger-Simons differential characters** are an abelian group
`Ĥ^k(M; R/Z)` fitting into the short exact sequences

```
0 → H^{k-1}(M; R/Z) → Ĥ^k(M; R/Z) → Ω_ℤ^k(M) → 0
0 → Ω^{k-1}(M)/Ω_ℤ^{k-1}(M) → Ĥ^k(M; R/Z) → H^k(M; ℤ) → 0
```

where `Ω_ℤ^k` are closed integral k-forms (cf. Cheeger-Simons 1985).

**Specialization:** the retained spatial sector `M = T³/Z₃` is the
framework's `ℤ³` lattice (with `a⁻¹ = M_Pl`) modded by the body-diagonal
Z₃ family symmetry on the hw=1 charged-lepton sector. Its integer
cohomology is

| k | `H^k(T³/Z₃; ℤ)`               |
|---|-------------------------------|
| 0 | ℤ                             |
| 1 | Z₃ (torsion only)             |
| 2 | Z₃ (torsion only)             |
| 3 | ℤ (top class)                 |

The `Z₃`-torsion arises because the Z₃ action kills the free part of
`H^1(T³)` (free factors `H^1(T^3) = ℤ³` collapse under the diagonal
permutation action). All three `Ĥ^k` for k=1,2,3 are nontrivial.

### 2.2 Z₃-equivariant CS class with value 2/9

There is an explicit Z₃-equivariant cellular 1-cocycle representative
`c: g ↦ 2/9 mod 1` on the Z₃-generator's loop. This represents a class in
`H^1(T³/Z₃; R/Z)`, lifted to `Ĥ^1(T³/Z₃; R/Z)` via the SES with constant
flat connection 0. The class is *not* a Z₃-torsion class (since
`3·(2/9) = 2/3 ≠ 0 mod 1`); it is genuinely R/Z-fractional, which is the
extra refinement CS provides over plain integer cohomology.

This CS class is canonically identified with the ABSS η-invariant
`η(Z_3, weights (1,2)) = 2/9 mod ℤ` already retained in the framework
(see `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`). The CS lift is the
standard one: an η-invariant on a compact space lifts to a differential
character whose holonomy on the corresponding 1-cycle is `η mod 1`.

### 2.3 Phase normalization: the canonical isomorphism

The codomain `R/Z` is identified with `U(1)` by the **canonical** map

```
χ: R/Z → U(1),     χ(c) = exp(2πi·c).
```

This is the canonical Cheeger-Simons R/Z → U(1) isomorphism; it is
*defining* of the CS functor, not a free choice.

Under `χ`, the CS class with holonomy `c = 2/9 mod 1` produces the U(1)
phase

```
χ(2/9) = exp(2πi · 2/9) = exp(4πi/9),     arg = (4/9)π rad.
```

This is a `(rational)·π` radian — exactly on the Lindemann wall (O10).

---

## 3. Computation: any retained CS class with value 2/9 mod 1?

**Yes.** The probe constructs an explicit Z₃-equivariant Ĥ¹ representative
with holonomy `2/9 mod 1`. Cross-checks (probe section F):

- (1) ABSS η(Z₃, weights (1,2)) = `2/9 mod ℤ` ✓
- (2) Casimir ratio `C_2(fund)/C_2(Sym^3) = (4/3)/6 = 2/9` ✓
- (3) `R_conn`-derived `2(1 - R_conn) = 2/9` at `N_c = 3` ✓
- (4) Plancherel weight `(2 DOF of b)/(9 dim Herm_3) = 2/9` ✓
- (5) Ratio of two retained radians `(4π/9)/(2π) = 2/9` ✓
- (6) Scale-ratio identities (e.g. `R_conn · Y_L² = 8/9 · 1/4 = 2/9`) ✓
- (7) **NEW:** Cheeger-Simons holonomy `Ĥ¹(T³/Z₃; R/Z)` value `2/9 mod 1` ✓

These seven sources are all *dimensionless rationals*; (7) coincides with
(1) at the level of the underlying eta data. The CS construction does not
provide a new dimensionful source; it is the same dimensionless 2/9 with
a fractional-mod-1 refinement.

---

## 4. Phase normalization analysis: 2π vs 1 rad period

This is the load-bearing test of the probe. We exhaustively enumerate
retained Cl(3)/Z₃ structure that could pick `1 rad` (rather than `2π rad`)
as the natural period of a closed phase observable:

| Structure | Phase observable | Natural period |
|---|---|---|
| Z₃ generator `U_g`, eigvalues `e^{2πik/3}` | `arg(λ_k)` | 2π |
| Cl(3) bivector rotation `exp(θ J_{ij})` | spinor angle | 4π (vector 2π) |
| Wilson plaquette `exp(iΦ)` | plaquette holonomy | 2π |
| APBC boundary factor `exp(iπ)` | half-period anti-periodic | 2π (or π) |
| Cyclic Wilson loop `tr(U_a U_b U_c)` | trace eigenvalues | 2π |
| Cheeger-Simons `Ĥ^k → U(1)` | `χ(c) = exp(2πi·c)` | **2π by definition** |

**Every retained period is a rational multiple of π.** No retained
structure picks `1 rad` as a natural period.

The non-canonical alternative is

```
χ': R/Z → U(1),     χ'(c) = exp(i·c)     (period 1 rad).
```

Under `χ'`, the CS class with `c = 2/9 mod 1` produces phase
`exp(i · 2/9)`, with argument `2/9 rad` literally — bridging to delta.
But this convention is *not* the canonical Cheeger-Simons R/Z → U(1) map,
and *no retained Cl(3)/Z₃ lattice structure justifies it*. Selecting
`χ'` over `χ` *is* the radian-bridge primitive, restated in the language
of differential characters.

---

## 5. Three convention options enumerated

| Convention | Map | `c = 2/9` → arg | On Lindemann wall? | Status |
|---|---|---|---|---|
| `χ(c) = exp(2πi·c)` | canonical CS R/Z → U(1) | `(4/9)π` | yes | retained |
| `χ̃(c) = exp(πi·c)` | half-period (spin lifts) | `(2/9)π` | yes | retained but does not bridge |
| `χ'(c) = exp(i·c)` | 1-rad period | `2/9` rad literally | **no** | NOT retained; equivalent to postulate P |

The only convention that bridges to literal `2/9 rad` is `χ'`, which is
exactly the radian-bridge primitive being investigated. Every retained
phase normalization on Cl(3)/Z³ uses `2π`, `π`, or `4π` (rational
multiples of π).

---

## 6. Verdict

**NO-GO.** Cheeger-Simons R/Z differential characters do not close the
radian-bridge postulate P. The CS framework is a clean canonical home for
fractional-mod-1 invariants and produces an explicit `2/9 mod 1` class on
the retained Z₃-equivariant Cl(3)/Z³ structure, but the canonical R/Z →
U(1) period is `2π`. The phase angle extracted from the CS class is
`(4/9)π` — a rational multiple of π, exactly on the Lindemann wall (O10).

To bridge to literal `2/9 rad`, one must select the non-canonical
1-rad-period convention `exp(i·c)`, which is itself the radian-bridge
primitive being investigated. This is a renaming of postulate P, not a
derivation.

The CS construction therefore:

1. Adds a **seventh independent dimensionless 2/9 source** (CS holonomy),
   coinciding with ABSS η at the level of underlying data.
2. Inherits the (rational)·π wall on phase extraction.
3. Confirms a new obstruction class.

---

## 7. New obstruction class: O13

> **O13 — Cheeger-Simons R/Z period inheritance.** Differential characters
> `Ĥ^k(M; R/Z)` are R/Z-valued by definition, with the canonical
> isomorphism to U(1) given by `exp(2πi·.)`. Therefore phase angles
> extracted from CS classes are of the form `2π·c` for `c` a retained
> rational, which is `(rational)·π`. The CS construction does not escape
> the (rational)·π wall established by O10; it sits downstream of it.
>
> Equivalently: CS classes provide retained refinements of integer
> cohomology to fractional-mod-1, but they do not provide a retained
> refinement of `2π rad` to `1 rad` as the natural period of a closed
> phase observable. Selecting the non-canonical `exp(i·.)` convention
> *is* postulate P.

**Parent class:** the audit note's Universal Lattice Closure / Lindemann
transcendence wall (locally relabeled O10 in this synthesis line).
**Domain killed:** all "fractional-mod-1 = 2/9" routes that hope the CS
or differential-character formalism circumvents the 2π normalization.

This is the load-bearing obstruction class added by the Round-10
fractional-topology synthesis (companion classes O14–O17 in
`KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`).

---

## 8. Cross-references

- `KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
  (parent note on main; Type-A/Type-B framing, retained periodic
  phase-source audit, Universal Lattice Closure / Lindemann wall = O10
  in this note's labelling).
- `KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`
  (Round-10 synthesis; this CS note is its load-bearing convention-choice
  entry).
- `KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md` (the original
  postulate P named here; the four prior closure candidates A–D).
- `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` (selected-line CP¹ Berry
  structure; ABSS η provenance).
- `KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md` (bundle
  topology obstruction R2; physical base is an interval).
- `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` (Plancherel
  weight `2/9` source, A.2).
- `KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO_NOTE_2026-04-24.md`
  (companion no-go on lattice Wilson selected-line route).
- `KOIDE_DELTA_MARKED_RELATIVE_COBORDISM_NO_GO_NOTE_2026-04-24.md`
  (companion no-go on relative cobordism route).
- Cheeger, J. and Simons, J. (1985), *Differential characters and
  geometric invariants*, Lecture Notes in Math. 1167, Springer.

---

## 9. Runner PASS list (49/49)

- **A.1–A.4** Hat{H}^k functor well-defined; R/Z natural codomain;
  H^*(T³/Z₃; ℤ) computed; CS classes nontrivial for k=1,2,3.
- **B.1–B.5** Explicit Z₃-equivariant Ĥ¹ representative: ABSS η =
  2/9 mod ℤ, cellular 1-cocycle c(g) = 2/9, lift to Ĥ¹.
- **C.1–C.6** Phase convention: canonical χ gives `(4/9)π`; alternate
  `exp(i·.)` gives literal 2/9 but is postulate P itself.
- **D.1–D.7** Lattice period search: every retained period is
  `(rational)·π`; no 1-rad-period retained.
- **E.1–E.4** Obstruction analysis: O13 = R/Z period inheritance,
  inherits from O10.
- **F.1–F.7** CS is the seventh dimensionless 2/9 source; coincides
  with ABSS η.
- **G.1–G.4** Numerical sanity: standard arg = `4π/9 ≈ 1.396` rad,
  literal target = `2/9 ≈ 0.222` rad, |diff| > 1.
- **H.1–H.7** Verdict: CS does not close postulate P; new class O13
  confirmed.

---

## 10. Closeout fingerprints

```
KOIDE_A1_CHEEGER_SIMONS_RZ_NO_GO=TRUE
CHEEGER_SIMONS_RZ_CLOSES_A1=FALSE
OBSTRUCTION_CLASS=O13
OBSTRUCTION_NAME=Cheeger-Simons R/Z period inheritance
OBSTRUCTION_PARENT=O10 (Universal Lattice Closure / Lindemann wall)
RESIDUAL=postulate P (literal 1-rad period of R/Z is a non-canonical structural input)
```
