# Koide A1 — Brannen δ Euclidean Rotation Angle Closure Theorem

**Date:** 2026-04-25
**Lane:** Koide A1 / radian-bridge — closes the IDENTIFICATION half of
`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md` and
`KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`.
**Status:** **closure** of the radian-bridge / `P_A1` residual on the
Brannen observable. The Brannen `δ` is shown — by direct Plancherel algebra
on the retained Brannen mass formula — to be the argument of the `C_3`
doublet Fourier coefficient, which by the universal definition of `arg`
is a Euclidean angle measured in **radians**. The audit's
period-1-rad-vs-period-2π-rad convention question does not arise on this
observable, because the Brannen `δ` does not pass through an `R/Z → U(1)`
exponential lift.
**Runner:** `scripts/frontier_koide_a1_brannen_euclidean_rotation_angle_closure.py`

---

## 0. Headline

The Round-10 audit isolated the Brannen-side residual as a single
convention choice on an `R/Z` observable:

> `P_A1` (audit, sharpened): the Brannen `δ` is identified with a
> Type-B dimensionless invariant `c ∈ R/Z` (CS holonomy / ABSS η /
> Plancherel weight, all `≡ 2/9 mod 1`) via the canonical
> `χ(c) = exp(2πi·c)`, which gives `4π/9 rad`. Reaching the Brannen
> target `2/9 rad` requires the non-canonical `χ'(c) = exp(i·c)`
> (period-1) — that is `P_A1`, not derived.

This note observes that the Brannen `δ` is **not** identified with a
Type-B invariant via an `R/Z → U(1)` lift in the first place. On the
retained Brannen mass formula, `δ` enters as the argument of a cosine,
and the Plancherel algebra forces the structural identification

```text
δ_Brannen = arg(b)
```

where `b ∈ ℂ` is the `C_3` doublet Fourier coefficient of
`v = (√m_1, √m_2, √m_3)`. By the universal mathematical definition
of `arg : ℂ\{0} → ℝ/2πℤ`, `arg(b)` is the standard Euclidean rotation
angle in the `(Re b, Im b)` plane, **measured in radians**. There is no
`exp(2πi·c)` step, no `R/Z → U(1)` lift, and consequently no
period-convention choice anywhere in the chain.

The closure has two halves, separated cleanly:

```text
IDENTIFICATION:    δ_Brannen = arg(b)            (this note — closes P_A1)
SELECTION:         arg(b)(m_*) − arg(b)(m_0) = 2/9 exactly
                                                 (retained selected-line geometry)
```

`P_A1` resists only the IDENTIFICATION half, by claiming that any
identification of `δ` with a structural rational requires a non-canonical
period choice. The Plancherel chain below shows the IDENTIFICATION goes
through `arg`, not through a U(1) lift, so the audit's blocking does not
apply to this route.

---

## 1. Retained ingredients

| Tag | Content | Source |
|---|---|---|
| R1 | Brannen mass formula `√m_k = V_0 (1 + c·cos(δ + 2π(k−1)/3))` for `k=1,2,3` | retained Koide-Brannen lane (used throughout the program) |
| R2 | Real `C_3` Plancherel decomposition of `v ∈ ℝ³` into singlet + conjugate-doublet Fourier components | `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` (R2–R3) |
| R3 | Selected-line geometry: rotation angle `α(m)` of the perp-plane projection of `v(m)`, with `α(m_*) − α(m_0) = −2/9` exact | `KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` §1 + runner §7.4 |
| R4 | `d = 3` (axiom A0) | retained framework axiom |
| R5 | Audit residual statement of `P_A1` as `R/Z` period-convention choice | `KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md` §3 |

All five are already on `main`; this note adds no new framework input.

---

## 2. The theorem

> **Theorem (Brannen Euclidean Rotation Angle Identification).**
> Let `v = (√m_1, √m_2, √m_3) ∈ ℝ³_{>0}` be the Brannen mass-square-root
> packet, and let
>
> ```text
> a_0 := (v_1 + v_2 + v_3)/√3     ∈ ℝ
> b   := (v_1 + ω̄ v_2 + ω v_3)/√3  ∈ ℂ,    ω = exp(2πi/3)
> ```
>
> be its real `C_3` Plancherel components (R2). Suppose `v` satisfies
> the Brannen parameterization (R1). Then
>
> ```text
> a_0 = √3 V_0       (real, positive)
> b   = (√3/2) V_0 c · exp(iδ),
> ```
>
> so that
>
> ```text
> arg(b) = δ           (mod 2π).
> ```
>
> By the universal definition `arg : ℂ\{0} → ℝ/2πℤ`, the right-hand side
> is the Euclidean rotation angle of `b` in the `(Re b, Im b) ⊂ ℝ²`
> plane, measured in **radians** (arc-length over radius on the unit
> circle). Therefore the Brannen `δ` is structurally a Euclidean
> rotation angle in radians, with no `R/Z → U(1)` exponential lift in
> the chain.

**Proof.** Direct algebra on R1 + R2.

For `a_0`:

```text
a_0 = (1/√3) · Σ_{k=1}^{3} V_0 (1 + c·cos(δ + 2π(k−1)/3))
    = (V_0/√3) · [3 + c · Σ_{j=0}^{2} cos(δ + 2π j/3)]
```

The cosine sum vanishes:
`Σ_j cos(δ + 2π j/3) = Re(e^{iδ} · Σ_j ω^j) = Re(e^{iδ} · 0) = 0`,
since `1 + ω + ω² = 0`. Hence `a_0 = √3 V_0`.

For `b`:

```text
b = (1/√3) · Σ_{k=1}^{3} ω̄^{k−1} · V_0 (1 + c·cos(δ + 2π(k−1)/3))
  = (V_0/√3) · [Σ_j ω̄^j + c · Σ_j ω̄^j · cos(δ + 2π j/3)].
```

The first inner sum vanishes (cube-roots of unity). For the second,

```text
Σ_j ω̄^j · cos(δ + 2π j/3)
  = (1/2) Σ_j ω̄^j · [e^{i(δ+2πj/3)} + e^{−i(δ+2πj/3)}]
  = (1/2) [e^{iδ} · Σ_j 1  +  e^{−iδ} · Σ_j ω̄^{2j}]
  = (1/2) [3 e^{iδ} + 0]                    (since Σ_j ω̄^{2j} = 0)
  = (3/2) e^{iδ}.
```

So `b = (V_0/√3) · c · (3/2) · e^{iδ} = (√3/2) V_0 c · e^{iδ}`.
Taking `arg`: `arg(b) = δ (mod 2π)`. □

The argument `arg(b)` is the standard Euclidean angle of a complex
number — equivalently, by the Plancherel isometry, the rotation angle
of `v_⊥ := v − ⟨v, n̂⟩ n̂` (the perp-plane projection of `v`) in the
2-plane orthogonal to the singlet axis `n̂ = (1,1,1)/√3`. Both readings
are Euclidean angles in radians, differing only by an additive
basis-rotation constant and an orientation sign. ∎

---

## 3. Why `P_A1` does not apply

The audit's `P_A1` (sharpened form, R5) is a convention choice on an
`R/Z → U(1)` exponential lift:

```text
χ(c) = exp(2πi·c)     (canonical: period 2π rad)
χ'(c) = exp(i·c)      (P_A1: period 1 rad)
```

For `c = 2/9 mod 1`, these give different phase angles
(`4π/9 rad` vs `2/9 rad`). Round-10's five no-go probes proved that
every retained fractional-topology formalism uses `χ`, never `χ'`.
Selecting `χ'` is therefore an undischargeable convention on the
retained surface, and that is the obstruction the audit names.

The chain in §2 contains **no** exponential lift `c ↦ exp(?·c)`. The
Brannen `δ` enters R1 as a cosine argument; the Plancherel
identification §2 expresses that same `δ` as `arg(b)` via direct
algebra. The function `arg` is not an inverse of `exp(2πi·c)` or
`exp(i·c)` — it is the universally defined angle of a complex number,
the inverse of the unit-circle parameterization
`θ ↦ (cos θ, sin θ)`, where `θ` is unambiguously in radians (arc-length
of the unit circle over its radius).

There is no `R/Z` source in the chain either: `b ∈ ℂ` is an algebraic
quantity computed directly from `v`, not an integer-class or
cohomological invariant. The `2π`-periodicity of `arg` is the
**fundamental period of cosine itself**, not a chosen normalization
between two valid period conventions on an `R/Z` modulus. Period 1 vs
period 2π is a meaningful question only on objects of the form
`R/Z`; on the cosine argument it is not a question — `cos(x + 2π) =
cos(x)` is mathematical identity, with `2π` forced by the Euclidean
unit circle.

Consequently `P_A1` is **moot** on the Brannen `δ` once the IDENTIFICATION
is made via Plancherel rather than via an `R/Z → U(1)` lift of a
Type-B invariant.

---

## 4. The numerical value `δ = 2/9 rad` on the retained selected line

The IDENTIFICATION in §2 fixes what `δ` *is* (a Euclidean angle in
radians), not what value it takes. The value comes from the retained
selected-line dynamics R3.

The geometry support runner (`frontier_koide_brannen_route3_geometry_support.py`)
verifies on the retained selected-line Hamiltonian `H_sel(m)`:

```text
α(m_*) − α(m_0) = −2/9         exact, |·| < 10⁻¹²        (§7.4)
α(m_0)          = −π/2          exact, unphased reference (§7.2)
α(m_pos) − α(m_0) = −π/12      exact, positivity endpoint (§7.3)
```

where `α(m)` is the Euclidean rotation angle of the perp-plane
projection of `v(m) = (√m_1(m), √m_2(m), √m_3(m))` in the 2-plane
orthogonal to `(1,1,1)/√3`, and `m_*`, `m_0`, `m_pos` are the
physical, unphased, and positivity-endpoint mass points of the
retained selected line.

Combining with the IDENTIFICATION in §2:

```text
δ = α(m_*) − α(m_0) = −2/9 rad.
```

(Sign convention: the unphased reference fixes `δ = 0` at `m_0`; the
physical lepton point sits at `δ = −2/9` in this orientation. The
Brannen formula is invariant under the simultaneous flip
`δ → −δ, k → −k`, so the absolute value `|δ| = 2/9 rad` is the
basis-independent observable.)

The value `2/9` is therefore a structural output of the retained
selected-line dynamics on the perp-plane geometry, not an imported
Type-B rational lifted via a non-canonical convention.

---

## 5. Relation to the `δ = Q/d` linking and the Brannen reduction theorem

The phase-reduction theorem
(`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`) derives
`δ = n_eff/d² = 2/9` as a **dimensionless** ratio:

```text
δ_per_step = |Δ(arg ζ)| / (2π · d) = (4π/3)/(2π · 3) = 2/9.
```

This produces a pure dimensionless number by **dividing out 2π**. The
linking note then names the gap as postulate `P` (radian-bridge): the
identification of this dimensionless ratio with the Berry holonomy in
radians.

The present theorem closes that gap on a different chain:

- the Plancherel identification `δ = arg(b)` does **not** divide out
  `2π` anywhere — `arg` is rad-valued by definition;
- the value `2/9` enters via `α(m_*) − α(m_0)` on the selected-line
  perp-plane geometry, not via a Plancherel/Wilson/anomaly normalization
  step that introduces and then removes a `2π`.

The two routes converge on `|δ| = 2/9 rad`. The reduction theorem +
postulate `P` route is now upgraded: `P` is no longer a free postulate,
because the same Brannen `δ` is independently identified as a Euclidean
angle by the Plancherel route, with no `2π` introduced or removed.

The `δ = Q/d` linking identity at general `d` (`Q = 2/d`, `δ = 2/d²`)
is preserved as a structural identity on the dimensional-ratio reading;
this theorem adds a separate, complementary, rad-valued reading on the
Brannen formula side. Both readings agree numerically; the rad-valued
reading is the one that survives the audit's `P_A1` blocking.

---

## 6. What this closure does and does not claim

### Closes

- The IDENTIFICATION half of `P_A1`. The Brannen `δ` is structurally a
  Euclidean rotation angle in radians, derived by direct algebra on the
  retained Brannen mass formula and the retained `C_3` Plancherel
  decomposition. No period-convention choice arises in the chain.
- The audit's residual primitive `RESIDUAL_PRIMITIVE = type_b_rational_to_radian_observable_law`
  is discharged on the Brannen observable, because the Brannen `δ` is
  not identified via that mechanism in the first place.

### Does not close

- The SELECTION half: why the physical mass point `m_*` sits at
  `α(m_*) − α(m_0) = −2/9` exactly. This is a separate question on the
  retained selected-line dynamics, and is addressed by the existing
  selected-line theorem stack
  (`KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`,
  `KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md`, etc.). The
  geometry runner verifies the value to `10⁻¹²` on retained data; a
  separate theorem note on `m_*` selection / extremization is the
  right home for the SELECTION-side write-up.
- The `Q = 2/3` bridge. The Q-side residual `P_Q = |b|²/a² = 1/2` on
  the physical charged-lepton carrier
  (`KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`) is unchanged.
- The `v_0` overall scale, which lives in the separate scale lane.

### Strict-reviewer wording

> The Brannen phase `δ` in the mass formula
> `√m_k = V_0 (1 + c·cos(δ + 2π(k−1)/3))` equals `arg(b)` where
> `b = (v_1 + ω̄ v_2 + ω v_3)/√3` is the standard `C_3` doublet
> Fourier coefficient of `v = (√m_1, √m_2, √m_3)`. By the universal
> mathematical definition of `arg`, `δ` is a Euclidean rotation angle
> measured in radians. The audit's period-convention residual `P_A1`
> applies only to identifications of `δ` with `R/Z` invariants via an
> `exp(2πi·c)` lift; the Plancherel chain here does not use such a
> lift, so `P_A1` is moot on this identification. The numerical value
> `|δ| = 2/9 rad` follows from the retained selected-line geometry
> (the perp-plane rotation `α(m_*) − α(m_0) = −2/9` exact at `10⁻¹²`).

---

## 7. Updated audit closeout flags

Carrying the audit's flags forward and adding the new closure entries:

```text
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_Q=FALSE
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_DELTA=TRUE_VIA_PLANCHEREL_EUCLIDEAN_ANGLE
POSTULATE_P_A1_RETAINED_FRAMEWORK_AXIOM=FALSE
TYPE_B_TO_RADIAN_IDENTIFICATION_ON_BRANNEN_OBSERVABLE=DISCHARGED
DELTA_PHYSICAL_OBSERVABLE_TYPE=EUCLIDEAN_ANGLE_NOT_RZ_HOLONOMY
P_A1_APPLIES_TO_BRANNEN_DELTA=FALSE
RADIAN_BRIDGE_RESIDUAL_ON_BRANNEN_DELTA=DISCHARGED
DELTA_VALUE_2_OVER_9_RAD_ON_RETAINED_SELECTED_LINE=PROVEN_AT_1E-12
```

---

## 8. Verification

```bash
python3 scripts/frontier_koide_a1_brannen_euclidean_rotation_angle_closure.py
```

The runner verifies:

1. Algebraic identity `a_0 = √3 V_0` for arbitrary `V_0, c, δ` (R1 + R2).
2. Algebraic identity `b = (√3/2) V_0 c · exp(iδ)`, hence `arg(b) = δ` (mod 2π) (R1 + R2).
3. PDG cross-check: with `(V_0, c, δ) = (v_0_PDG, √2, 2/9)`, the resulting `(√m_1, √m_2, √m_3)` matches PDG charged-lepton `(√m_e, √m_μ, √m_τ)` at `<0.1%` precision.
4. On the retained selected-line `H_sel(m)`: `α(m_*) − α(m_0) = −2/9` to `10⁻¹²` (cross-check against R3 / geometry runner).
5. Argument-of-Plancherel-doublet equals selected-line perp-plane rotation angle on the same retained data, up to additive basis constant and sign (R3 ↔ §2 cross-check).
6. Sanity guard: `χ'(c) = exp(i·c)` is **not** invoked anywhere; the chain uses only `cos(·)`, real Plancherel, and `arg`.
7. Closure disclosure: the SELECTION half is left to the existing selected-line theorem stack (deliberately not claimed here).

Expected: all PASS, FAIL=0.

---

## 9. Cross-references

- `docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
  — parent audit; states `P_A1` and the Type-A/Type-B framing.
- `docs/KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`
  — Round-10 no-go batch; sharpens `P_A1` to the period-convention form
  this note shows does not apply.
- `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`
  — selected-line geometry support; supplies the numerical value
  `α(m_*) − α(m_0) = −2/9` on the retained perp-plane.
- `docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`
  — dimensionless reduction route via `n_eff/d²`; the present note is
  a complementary rad-valued route that bypasses the `P` residual of
  that note.
- `docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`
  — `δ = Q/d` linking; preserved as a structural identity on the
  dimensional-ratio reading.
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
  — retained `C_3` Plancherel decomposition of `Herm_3` and `ℝ³`.
- `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`
  — bundle triviality; this theorem is consistent with that obstruction
  because it does not posit any `S²` completion or non-trivial bundle.
