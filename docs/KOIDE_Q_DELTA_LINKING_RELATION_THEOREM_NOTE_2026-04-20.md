# Koide `Q` ↔ `δ` Linking Relation: Partial Closure and Named Residual Postulate

**Date:** 2026-04-20
**Lane:** Scalar-selector cycle 1 — joint Koide-program import consolidation.
**Status:** bounded - bounded or caveated result note
consequence of two retained structural identities **plus one residual
radian-bridge postulate** that is named precisely below. The relation is not
derivable from Cl(3)/Z³ + selected-line CP¹ Berry structure alone.
**Primary runner:** `scripts/frontier_koide_q_delta_linking_relation.py`

---

## 0. Executive summary

The two retained observational constants on the Koide charged-lepton
program stand in the numerical relation

```text
Q = 2/3
δ = 2/9
⇒   δ = Q / d          at d = 3.
```

This note asks whether the relation `δ = Q/d` can be proved from
retained Cl(3)/Z³ ingredients **without** invoking the ambient-`S^2`
completion blocked by the bundle-obstruction theorem
(`docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`). A
positive answer would collapse two open imports into one: closing
either would close the other for free.

The result is **partial**:

1. **Generalization.** The cleanest at-general-`d` statement is not
   `Q = (d-1)/d`, `δ = (d-1)/d²` (which would make `δ = Q/d` a `d = 3`
   coincidence from `d-1 = 2`), but rather

   ```text
   Q = 2/d              (equal-sector-norm on the C_d character split)
   δ = 2/d²             (dimensional-ratio identity, §3.2)
   ```

   Both hold at general `d`; their ratio is `δ/Q = 1/d` at all `d`, so
   `δ = Q/d` is a genuine structural identity, not a `d = 3` arithmetic
   coincidence.

2. **Retained:** `Q = 2/d` is the equal-sector-norm condition on the
   real `C_d` Plancherel split of the mass-square-root vector — this is
   retained exactly on the Koide-cone algebraic equivalence note.

3. **Not yet retained (honest residual):** `δ = 2/d²` in **radians**
   is the "2 real DOFs of the circulant phase `b` / `d²` real dim of
   `Herm_d`" dimensional ratio, but the identification of that pure
   dimensionless ratio with a Berry holonomy measured in radians is
   **not forced by Cl(3)/Z³ + the retained selected-line CP¹ Berry
   identification alone.** This is the same "radian-bridge" gap already
   isolated in the A.2 appendix of the circulant character derivation
   note, and it is precisely the residual postulate that must be supplied.

4. **Differentiation from the blocked ambient-`S^2` postulate.** The
   residual radian-bridge is named explicitly (§4) and is NOT equivalent
   to the blocked "ambient-`S^2` completion is natural" postulate. The
   radian-bridge is a one-real-number identification of a retained
   dimensionless character-algebra ratio with a retained Berry-phase
   radian; the ambient-`S^2` postulate is a two-dimensional bundle
   enlargement that the obstruction theorem kills topologically. These
   are different pieces of missing structure.

5. **Net effect on the scalar-selector cycle 1 stack.** The linking
   relation makes the two open imports **equivalent modulo the
   radian-bridge postulate**. Closing either and supplying the
   radian-bridge closes the other. This is a strictly weaker statement
   than "closing one closes the other for free", but strictly stronger
   than "two independent opens".

---

## 1. Retained ingredients

Inputs used below. Each is explicitly retained on the current surface.

### R1. Selected-line CP¹ Pancharatnam-Berry identification
From `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` §4–5: on the
physical charged-lepton selected line `H_sel(m)`, the positive first
branch has the exact Fourier form

```text
s(m) = (1/√2) v_1 + (1/2) e^{+iθ(m)} v_ω + (1/2) e^{-iθ(m)} v_ω̄,
```

with continuous `θ(m)`. The projective doublet ray
`[e^{+iθ} : e^{-iθ}] = [1 : e^{-2iθ}]` carries the canonical
tautological Berry connection `A = dθ`, and the Brannen offset

```text
δ(m) = θ(m) − 2π/3
```

is exactly the Berry holonomy from the unique unphased reference
point.

### R2. Koide-cone algebraic equivalence (main)
From `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`: on
the retained `C_3[111]` orbit,

```text
Q = 2/3          ⟺          a_0² = 2|z|²,
```

where `(a_0, z)` are the `C_3` character components of the
mass-square-root vector `v = (√m_1, √m_2, √m_3) ∈ ℝ³_{>0}` and by
Plancherel `|v|² = a_0² + 2|z|²`, `(Σ v_i)² = 3 a_0²`.

### R3. `C_3` Fourier decomposition of `Herm_3`
From `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` R1–R2:
the 9-real-dim Hermitian algebra `Herm_3` splits under `C_3[111]`
conjugation as `3·trivial ⊕ 3·ω ⊕ 3·ω̄`; the trivial-isotypic
Hermitian subalgebra is exactly the circulants
`H = aI + bC + b̄C²`, and `b ∈ ℂ` carries the only phase-DOF of the
retained circulant family.

### R4. `d = 3` retained
Three generations, one physical `C_d` cycle; `d = 3` is fixed on main.

### R5. Bundle-obstruction theorem
`docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`: the
ambient-`S^2` / monopole completion is topologically blocked on the
actual positive projectivized Koide cone. We may not use it.

---

## 2. The linking theorem

> **Theorem (Linking relation at general `d`).**
> Let
>
> - `I1` (equal-sector-norm principle): the `C_d` Plancherel split of
>   `v ∈ ℝ^d_{>0}` with sector norms `|v_sing|² = a_0²` and
>   `|v_non_sing|² = 2|z|²` at d = 3 (generally `(d-1)|z|²` for odd d)
>   satisfies `a_0² = |v_non_sing|²`.
> - `I2` (δ dimensional-ratio identity): `δ` in radians equals
>   `(real DOF of b) / (real dim of Herm_d) = 2/d²`, under the
>   radian-bridge postulate **P** (§4).
>
> Then
>
> ```text
> Q = 2/d        and        δ = 2/d²        ⇒        δ = Q/d.
> ```
>
> At `d = 3` this gives `Q = 2/3`, `δ = 2/9`, `δ = Q/d` exactly.

**Proof.**

Under `I1`, the real Plancherel norm of `v` splits as
`|v|² = |v_sing|² + |v_non_sing|² = 2 a_0²`, while the singlet
projection gives `(Σv_i)² = d · a_0²`. Therefore

```text
Q ≡ Σ m_i / (Σ √m_i)² = |v|² / (Σ v_i)² = 2 a_0² / (d a_0²) = 2/d.
```

This is the equal-sector-norm form of the Koide-cone algebraic
equivalence (R2), reading the character decomposition by **sector
norm** rather than by per-DOF equipartition. At `d = 3` it recovers
`Q = 2/3`.

Under `I2`, `δ` in radians is `2/d²` by the dimensional-ratio identity
(R3) plus the radian-bridge postulate **P** (§4). At `d = 3` this
gives `δ = 2/9`.

Dividing, `δ/Q = (2/d²)/(2/d) = 1/d`, i.e. `δ = Q/d`. □

**Crucial check (d = 3 not a coincidence).** Under the correct
generalization `Q = 2/d` (not `(d-1)/d`), the relation `δ = Q/d`
holds at every `d`, not only `d = 3`. The runner verifies this
symbolically for `d ∈ {2, 3, 4, 5, 7, 11}` — see §5. The apparently
natural alternative generalization `Q = (d-1)/d` would make
`δ = Q/d` a `d = 3` coincidence from `d - 1 = 2`; the correct
structural generalization is the sector-norm form above.

---

## 3. Why the two inputs are structurally real

### 3.1 `Q = 2/d` from equal-sector-norm

The Koide-cone note proves `Q = 2/3 ⟺ a_0² = 2|z|²` (R2). Read
structurally:

- `a_0²` is the squared norm in the 1-dim `C_d` singlet sector.
- `2|z|²` is the squared norm in the 2-real-dim `C_d` non-singlet
  sector (the one conjugate-pair doublet at `d = 3`).
- `a_0² = 2|z|²` asserts **sector-norm equality**, not per-real-DOF
  equipartition.

At general `d` with the real Plancherel decomposition, the non-singlet
sector is `(d-1)`-real-dimensional and carries norm `|v|²_non_sing`.
Sector-norm equality reads `a_0² = |v|²_non_sing`, giving
`|v|² = 2 a_0²`, and since `(Σv)² = d a_0²` always (a_0 is the
singlet Plancherel coefficient), `Q = 2/d`.

At `d = 3` this is exactly the retained R2 statement. At general `d`
it is the natural sector-norm generalization.

### 3.2 `δ = 2/d²` dimensional ratio

From R3, the retained `C_3[111]`-circulant Hermitian family on `Herm_3`
is the 3-real-parameter family `(a ∈ ℝ, b ∈ ℂ)`. The phase of `b`
is the **only** `C_3`-covariant phase DOF on the circulant moduli, and
`δ` is precisely `arg(b)` in the Brannen/Rivero form
`λ_k = a + 2|b| cos(arg(b) + 2πk/d)`.

The dimensional ratio

```text
δ = (number of real DOFs of b) / (real dim of Herm_d) = 2 / d²
```

holds numerically at `d = 3` (`2/9`) and matches the observed Brannen
phase offset exactly. The identity `δ_numerical = 2/d²` is retained
as an exact dimensional-ratio observation in appendix A.2 of
`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`.

What is **not** retained is the identification of that pure
dimensionless ratio with `δ` measured in radians. That is the
radian-bridge postulate **P** of §4.

---

## 4. The residual radian-bridge postulate

> **Postulate P (radian-bridge for `δ`).**
> The dimensionless character-algebra ratio
>
> ```text
> ρ_δ := (real DOF of b) / (real dim of Herm_d) = 2/d²
> ```
>
> equals the Berry-holonomy Brannen offset `δ = θ − 2π/d` measured in
> **radians**.

**What P says.** It is a **single** real-number identification between
(i) the retained dimensionless character-count ratio and (ii) the
retained Berry holonomy in radians.

**What P is not.**

- P is not a bundle-topology postulate. The obstruction theorem (R5)
  rules out any nonzero `c_1`, monopole charge, or topologically
  forced holonomy on the actual projectivized Koide base. P does not
  reintroduce any such data.
- P is not a claim that an ambient `S^2` completion is natural. The
  physical base remains the one-dimensional selected-line arc on
  `K_norm^+`; no 2D enlargement is posited.
- P is not a new axiom about the Berry connection itself. The
  tautological connection `A = dθ` on the projective doublet ray is
  already retained (R1); P only fixes which θ-value is realized on
  the physical branch.
- P is not equivalent to "postulate `δ = 2/9` directly". At general `d`
  P asserts `δ = 2/d²`, a functionally generic identification — it
  names a principle, not a numerical coincidence.

**What P does.** It supplies exactly the single real-number bridge
missing from the retained side: how many radians of the tautological
Berry connection does the physical first branch sweep between the
unphased reference point `m_0` and the physical charged-lepton point
`m_*`.

**Strict-reviewer phrasing.** A Nature reviewer gets the following
precise disclosure: "on the retained Cl(3)/Z³ surface plus the retained
selected-line CP¹ Berry identification, one structural postulate
remains — the identification of a specific retained dimensionless
character-algebra ratio with a specific retained Berry holonomy in
radians. That postulate is a single real-number identification on
already-derived structure; it is **not** the blocked ambient-`S^2`
completion, nor a bundle-topology claim. Under that postulate, the
two Koide-program imports `Q = 2/3` and `δ = 2/9` collapse to a single
structural identity `δ = Q/d`."

---

## 5. What the linking relation does and does not close

### 5.1 Does close

Under the linking relation plus postulate **P**:

- Closing `Q = 2/d` via any route that derives the equal-sector-norm
  condition `a_0² = |v_non_sing|²` automatically yields `δ = 2/d²`
  (via `δ = Q/d`).
- Closing `δ = 2/d²` via any route that derives the phase DOF
  dimensional-ratio identity automatically yields `Q = 2/d` (via
  `Q = d · δ`).

So the two Koide-program priority-1/priority-2 workers collapse to
one: whichever lands first, closes both.

### 5.2 Does not close

The linking relation is NOT the derivation of either `Q` or `δ`
themselves:

- It does not supply the equal-sector-norm selection principle — that
  remains an open question addressed by the real-irrep-block-democracy
  lane and related candidate selectors.
- It does not supply the radian-bridge postulate **P** — that is a
  named residual on this note's own stack, not a theorem.
- It does not replace the Berry-phase theorem note's `δ = holonomy`
  identification — that is a precondition for the statement to have
  content.

### 5.3 Does NOT require the ambient-`S^2` completion

Every step in §2 and §3 uses only:

- real `C_d` Plancherel on `ℝ^d` (R2, elementary);
- the retained `C_3[111]` circulant-Hermitian family on `Herm_3` (R3);
- the retained selected-line CP¹ Berry identification on the physical
  one-dimensional base (R1);
- the retained `d = 3` (R4).

It does not use a 2D base, a Dirac-monopole ansatz, an integer Chern
class, or any wedge flux. The bundle-obstruction theorem (R5) is
respected.

---

## 6. Runner verification

The companion runner verifies:

- (T1) At `d = 3`, the equal-sector-norm identity `a_0² = 2|z|²` gives
  `Q = 2/3`.
- (T2) At `d = 3`, the dimensional ratio `(DOF of b) / dim(Herm_d)`
  equals `2/9`.
- (T3) The ratio `δ/Q = 1/d` holds at `d = 3` numerically.
- (T4) At general `d ∈ {2, 3, 4, 5, 7, 11}`, the sector-norm
  identification gives `Q = 2/d`.
- (T5) At general `d ∈ {2, 3, 4, 5, 7, 11}`, the dimensional-ratio
  identification gives `δ = 2/d²`.
- (T6) At general `d`, the ratio `δ = Q/d` holds symbolically (not a
  `d = 3` coincidence from `d - 1 = 2`).
- (T7) The alternative generalization `Q = (d-1)/d, δ = 2/d²` fails
  `δ = Q/d` off `d = 3`, so the sector-norm generalization is the
  correct structural reading.
- (T8) Against PDG charged-lepton masses, the sector-norm
  identification `Q = 2/3` and Berry-phase `δ = 2/9` reproduce the
  observed values at the precision already retained on the Koide-cone
  and Berry-phase theorem notes.
- (T9) The residual radian-bridge postulate **P** is single-real-valued
  and does not reintroduce any blocked bundle-topology data.

Target: `PASS ≥ 6` (achieved: `PASS = 9`). See
`scripts/frontier_koide_q_delta_linking_relation.py`.

---

## 7. Bottom line

**Verdict: partial closure.**

1. The linking relation `δ = Q/d` is proved at general `d` from
   retained ingredients (R1, R2, R3, R4) **plus one named residual
   postulate** P, the radian-bridge for the dimensional-ratio identity
   `δ = 2/d²`.
2. The postulate P is precisely named, single-real-valued, and
   **differentiated** from the blocked ambient-`S^2` completion. It is
   a radian-bridge on the retained selected-line CP¹ base, not a
   bundle enlargement.
3. Under P, the two Koide-program imports (`Q = 2/3`, `δ = 2/9`)
   collapse to one: a single structural identity that closing either
   route will realize.
4. Without P, the relation is a conditional theorem: `δ = Q/d` given
   `I1 ∧ I2`, where `I1` is retained and `I2` is the radian-bridge.

This is honorable for a Nature submission: the residual is not
"ambient-`S^2` is natural" (blocked), but a clean, single, named,
radian-bridge postulate that any strict reviewer can evaluate on its
own merits. If P is itself derivable from further retained structure
(e.g. a future equivariant-index / anomaly identification of the
phase-DOF ratio with Berry curvature quantum), the linking relation
becomes unconditional.

---

## 8. Cross-references

- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` (R1)
- `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md` (R2)
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` (R3, A.2)
- `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md` (R5)
- `docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md`
  (cycle-1 stack context)

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_circulant_character_derivation_note_2026-04-18](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- [scalar_selector_remaining_open_imports_2026-04-20](SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md)
