# Koide A1 — Fractional-Topology / Math-Literature No-Go Synthesis

**Date:** 2026-04-24
**Lane:** Koide A1 / radian-bridge — extends
`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md` with a
focused math-literature audit on fractional-rational topological invariants.
**Status:** **5 probes, all NO-GO.** The audit note's residual primitive
`P_A1` is sharpened from "Type-B rational-to-radian observable law" to a
one-line statement of a single convention choice.
**Runners (all PASS = obstruction-confirmed):**
- `scripts/frontier_koide_a1_orbifold_chern_probe.py` (54/54)
- `scripts/frontier_koide_a1_eta_to_radian_lift_probe.py` (47/47)
- `scripts/frontier_koide_a1_fqhe_analog_probe.py` (59/59)
- `scripts/frontier_koide_a1_twisted_k_theory_probe.py` (34/34)
- `scripts/frontier_koide_a1_cheeger_simons_rz_probe.py` (49/49)

---

## 0. Origin

The retained audit note already establishes:

- The Type-A / Type-B disjoint quantum sets:
  `{q·π : q ∈ ℚ} ∩ ℚ = {0}` (Lindemann–Weierstrass).
- The candidate primitive `P_A1`: the charged-lepton Yukawa selected-line
  phase reads the Type-B lattice ratio `2/N²` at `N = 3` as a literal
  radian.
- The closeout `TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE = TRUE`.

An open methodological question remained: **does the math literature on
fractional-rational topological invariants (orbifold Chern, η-invariants,
fractional QH, twisted K-theory, Cheeger-Simons) supply a retained
mechanism that bridges Type-B to a literal radian without a 2π factor?**

The standard Dirac-flux / TKNN / Chern-Simons quantization theorems all
require closed-loop topology + integer-valued invariants + 2π normalization
and produce `(rational)·π` phases. The candidate fractional / open-base
extensions of this class must be tested separately because each preserves
fractional content but uses a different mathematical formalism for the
phase identification.

---

## 1. The five probes — all NO-GO

| # | Probe | PASS/FAIL | Mechanism flagged |
|---|---|---|---|
| 1 | Discrete-TKNN orbifold Chern | 54/54 | Kawasaki orbifold Chern in `(1/3)·ℤ`, phase via `exp(2πi·c)` lands at `2π/3`; reaching `(1/9)·ℤ` denominator requires `Z₃ × Z₃` not retained on lepton Yukawa moduli (color Z₃ ⊂ SU(3)_c is lepton-blind). |
| 2 | η-invariant lifted to literal radian | 47/47 | Finite-dim family-η = +3 signature constant (Δη = 0); spectral flow integer; Bismut-Cheeger arg = `4π/9 rad`; orbifold fixed-point η ≠ family-η (category error). |
| 3 | Fractional QH state analog | 59/59 | Jain `ν = 2/9 = 2/(2pn+1)` at `(p,n) = (2,2)` matches as arithmetic, but symmetric Z₃-equivariant ground state has sympy-verified flat Berry connection (`A₁ = A₂ = A₃ = 1/3`, `F_{ij} = 0`, Chern = 0). NTW many-body Chern requires non-retained N-particle interactions. |
| 4 | Twisted equivariant K-theory | 34/34 | `H²(Z₃, U(1)) = ℤ₃` (denominator 3); doubled `(Z₃)²` cup-product gives denominator 9, but as the *exponent* of `ζ₉` (algebraic, min-poly `x⁶ + x³ + 1`, degree 6 over ℚ), never as ℚ-rational `2/9`. |
| 5 | Cheeger-Simons R/Z characters | 49/49 | Canonical CS R/Z → U(1) is `χ(c) = exp(2πi·c)`; CS class `c = 2/9 mod 1` → arg = `4π/9 rad`. The only convention bridging to literal `2/9 rad` is `χ'(c) = exp(i·c)` (period 1 rad), which **is `P_A1` restated, not derived**. |

Each probe's runner emits PASS records under the obstruction-confirmed
convention; final flags identify the new obstruction class added.

The Cheeger-Simons probe also has a standalone note
(`docs/KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md`)
documenting the load-bearing convention-choice formulation.

---

## 2. Common structural diagnosis

The five probes use distinct mathematical formalisms but produce
numerically uniform outputs:

| Probe | Type-B 2/9 source | Phase output |
|---|---|---|
| Orbifold Chern (Z₃×Z₃) | Kawasaki `c₁ ∈ (1/9)·ℤ` | `exp(2πi · 2/9)` ⇒ `4π/9 rad` |
| η-invariant lift | `η(Z₃,(1,2)) = 2/9 mod ℤ` | Bismut-Cheeger arg = `4π/9 rad` |
| FQHE | Jain `2/(2·2·2+1) = 2/9` | flat connection ⇒ no phase |
| Twisted K-theory | `(Z₃)²` cup at denom 9 | `ζ₉` exponent ⇒ `2π/9 rad` |
| Cheeger-Simons R/Z | CS holonomy `2/9 mod 1` | `χ(2/9) = exp(4πi/9)` ⇒ `4π/9 rad` |

**Every output is `(rational)·π` rad.** No output is a pure rational read
in radians. The pattern is forced because each formalism *defines* its
dimensionless-to-phase isomorphism via multiplication by 2π in its
construction. The 2π is not removable from inside any of these formalisms;
it is part of the definition of the canonical isomorphism in each case.

The Cheeger-Simons construction adds a fractional-mod-1 cohomological
*refinement* of the existing `η_APS(Z_3; 1, 2) = 2/9` witness retained by
the audit note — not a numerically new dimensionless source, but a sharper
mathematical home for the same data.

---

## 3. Sharpening of `P_A1`

The audit note states `P_A1` as:

> The charged-lepton Yukawa selected-line phase is a Type-A phase
> observable whose numerical value is the Type-B lattice ratio `2/N²` at
> `N = 3`.

The Cheeger-Simons probe sharpens this to an exact convention choice on a
single observable:

> **`P_A1` (sharpened convention form):** Let `c ∈ R/Z` be the dimensionless
> Type-B invariant (CS holonomy / ABSS η / Plancherel weight, all equal to
> `2/9 mod 1`). The canonical R/Z → U(1) period is `2π rad`
> (`χ(c) = exp(2πi·c)`), and every retained Cl(3)/Z³ phase observable uses
> this convention. `P_A1` selects the non-canonical period-1 convention
> `χ'(c) = exp(i·c)` on the Yukawa amplitude phase. The two conventions
> differ by the rescaling `δ → δ·2π`; only `χ` is retained.

If one identifies this `c = 2/9 mod 1` witness with the physical
selected-line phase input, then the canonical convention `χ` yields
`δ = 4π/9 rad ≈ 1.396 rad`, while the literal Brannen target is
`δ ≈ 0.2222 rad = 2/9 rad`. Matching the literal-radian target therefore
requires the non-canonical `χ'` convention. The five Round-10 probes show
that this convention choice is **not derived** by the canonical
fractional-rational extensions audited here.

---

## 4. Five new obstruction classes (O13–O17)

The labels O13–O17 are this branch's local extension of the audit note's
Universal Lattice Closure / Lindemann wall (its single retained
obstruction). The Cheeger-Simons class is the load-bearing one and gets
the lead label O13; the standalone CS note uses the same label.

> **O13 — Cheeger-Simons R/Z period inheritance** *(load-bearing).*
> Differential characters `Ĥ^k(M; R/Z)` are R/Z-valued by definition with
> the canonical isomorphism `χ(c) = exp(2πi·c)`. Phase angles extracted
> from CS classes are `(rational)·π`. CS *does* refine integer cohomology
> to fractional-mod-1 on non-closed bases (an honest mathematical
> refinement of the retained Type-B inventory) but it does *not* refine
> `2π rad` to `1 rad` as the natural period of a closed phase observable.
> The only convention bridging `c = 2/9 mod 1` to literal `2/9 rad` is the
> non-canonical `χ'(c) = exp(i·c)` — which is `P_A1` restated, not derived.
> CS is the sharpest formal statement of `P_A1` as a single convention
> choice. Detailed in
> `docs/KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md`.

> **O14 — Orbifold-Chern π-factor inheritance.** Every orbifold-Chern-derived
> phase is `exp(2πi·q)` for `q ∈ ℚ`, hence in `ℚ·π`. Reaching denominator
> 9 (rather than 3) requires `Z₃ × Z₃`. Framework retains only one Z₃
> acting on lepton Yukawa moduli (color Z₃ ⊂ SU(3)_c is lepton-blind,
> Matsubara is `Z_{2L_t}`, Spin is `Z₂`). The Berry-bundle obstruction
> theorem extends to the orbifold setting: `K_norm⁺/C₃` is contractible
> (open interval), so all orbifold-equivariant line bundles are trivial.

> **O15 — η mod-ℤ vs phase mod-2π unit-system gap.** APS / ABSS / Bismut-Cheeger
> machinery preserves the dimensionless rational structure of η. Spectral
> flow is integer-valued; finite-dim family-η is integer signature;
> Bismut-Cheeger arg = `2π·η = 4π/9 rad`. Lifting `η = 2/9 mod ℤ` (unit 1)
> to `arg(b)` (unit 2π) is `P_A1` relocated, not derived. Conflating
> orbifold fixed-point η (Lefschetz character at a single moduli point)
> with family-η (signature of a varying operator) is a category error.

> **O16 — Many-body promotion cost.** The FQHE mechanism (Niu-Thouless-Wu
> many-body Chern on a magnetic torus) requires three retained inputs the
> framework lacks: (i) continuous T² of TBC parameters (only discrete Z₃
> retained); (ii) non-commuting magnetic translations with central
> Heisenberg cocycle (Z₃ is abelian); (iii) strong interactions producing
> non-flat Berry curvature on the many-body wavefunction (retained Yukawa
> is single-particle bilinear; symmetric Z₃-equivariant ground state has
> sympy-verified flat connection, Chern = 0). The Jain arithmetic match
> `2/9 = 2/(2pn+1)` holds as identity but is a Plancherel-tautology — same
> dimensionless 2/9 as already retained, no physical mechanism added.

> **O17 — Cyclotomic exponent vs ℚ-rational mismatch.** Twisted equivariant
> K-theory for `Z₃ × Z₃` reaches denominator 9 in
> `H²((Z₃)², U(1)) = (Z₃)³`, but the "9" lives in the *exponent* of
> `exp(2πi·k/9) = ζ₉`. The minimal polynomial of `ζ₉` over ℚ is
> `x⁶ + x³ + 1` (degree 6); ζ₉ is algebraic irrational, not the
> ℚ-rational value `2/9`. Phase output is `2π/9 rad` (rational·π), never
> `2/9 rad`. Future twisted-K closure must supply *both* (i) a retained
> `Z₃ × Z₃` acting on lepton Yukawa moduli (not in framework) AND (ii) a
> separate π-killing mechanism (also not in framework). The dual condition
> is decisive.

All five new classes are sub-cases of the audit note's Universal Lattice
Closure / Lindemann transcendence wall. They confirm that the wall is
robust against the canonical fractional-rational extensions of the math
literature — including the secondary characteristic class framework that
is *specifically designed* to refine integer cohomology to fractional-mod-1
on non-closed bases.

---

## 5. TKNN structural comparison

The integer Chern theorem (TKNN) succeeds because it forces all four of
the following simultaneously. The framework fails all four:

| Feature | TKNN/IQHE | Framework |
|---|---|---|
| Base | closed `T²` | open interval `K_norm⁺/C₃` |
| Bundle | nontrivial (filled bands) | trivial by Berry-bundle obstruction R2 (extends to orbifold) |
| Chern values | `ℤ` | `(1/3)·ℤ` orbifold or `0` physical |
| Target observable | quantized integer (`σ_xy`) | continuous real (`arg(b)`) |
| 2π absorbed | in `h` (vs `ℏ`) | not absorbed |
| Result | quantized integer forced | not forced |

No orbifold / discrete / fractional / secondary-class extension of TKNN
recovers all four — and the absent fourth (continuous-modulus target
observable) is intrinsic to the Yukawa parametrization. This is a clean
publishable structural argument for why Round 10's five canonical paths
all reach the same wall.

---

## 6. The "any other math-literature paths" question — answered

User question (paraphrased): Are there other paths similar to closed-loop /
integer-invariant quantization theorems that produce fractional-radian
quantization on contractible / orbifold / open bases?

Answer: yes, five canonical paths exist and all five preserve the
`(rational)·π` wall by different routes that share one structural feature:
**each formalism's canonical dimensionless-to-phase isomorphism includes a
factor of 2π by definition**. The 2π cannot be removed from inside any
formalism; removing it requires a non-canonical convention which is
itself the radian-bridge primitive.

Round 10 therefore strengthens the irreducibility audit from
"`P_A1` is necessary on retained content" to **"`P_A1` is exactly the
unit-period convention choice between 1 rad and 2π rad on a single
observable"** — which is the smallest residual structural input found
in the program to date.

---

## 7. Updated closeout flags

```text
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_Q=FALSE
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_DELTA=FALSE
POSTULATE_P_A1_RETAINED_FRAMEWORK_AXIOM=FALSE
TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE
P_A1_FORMULATION=R/Z_PERIOD_1_RAD_VS_2PI_RAD_CONVENTION_CHOICE
P_A1_IF_DELTA_IS_READ_DIRECTLY_REQUIRES_PERIOD_1_RAD_CONVENTION=TRUE
ROUND_10_FRACTIONAL_TOPOLOGY_PROBES=5_ALL_NO_GO
NEW_OBSTRUCTION_CLASSES_THIS_ROUND=O13,O14,O15,O16,O17
```

---

## 8. Verification

```bash
python3 scripts/frontier_koide_a1_cheeger_simons_rz_probe.py    # O13
python3 scripts/frontier_koide_a1_orbifold_chern_probe.py       # O14
python3 scripts/frontier_koide_a1_eta_to_radian_lift_probe.py   # O15
python3 scripts/frontier_koide_a1_fqhe_analog_probe.py          # O16
python3 scripts/frontier_koide_a1_twisted_k_theory_probe.py     # O17
```

Expected: each probe exits 0 with PASS = obstruction-confirmed records and
reports its individual obstruction class on the closeout line.

---

## 9. Cross-references

- `docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
  (parent note on main; Type-A/Type-B framing; `P_A1` candidate primitive)
- `docs/KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md`
  (standalone Cheeger-Simons note; load-bearing convention-choice
  formulation; the strongest formal statement of `P_A1` as a single
  convention)
- `docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`
  (original `P` named; closure candidates A–D, all ruled out by audit)
- Cheeger, J. and Simons, J. (1985), *Differential characters and
  geometric invariants*, Lecture Notes in Math. 1167, Springer.
- Atiyah, M. F.; Bott, R.; Shapiro, A. (1964), *Clifford modules*,
  Topology 3 Suppl. 1, 3–38. (ABSS η-invariant on `L(3,1)`.)
- Niu, Q.; Thouless, D. J.; Wu, Y.-S. (1985), *Quantized Hall conductance
  as a topological invariant*, Phys. Rev. B 31, 3372.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24](KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
- [koide_a1_o13_cheeger_simons_rz_no_go_note_2026-04-24](KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md)
- [koide_z3_qubit_radian_bridge_no_go_note_2026-04-20](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
- [koide_berry_bundle_obstruction_theorem_note_2026-04-19](KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
