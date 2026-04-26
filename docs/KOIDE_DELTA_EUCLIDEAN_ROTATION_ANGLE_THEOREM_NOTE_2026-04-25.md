# Koide Brannen-as-Euclidean-Rotation-Angle Theorem

**Date:** 2026-04-25
**Lane:** Charged-lepton Koide Brannen phase `δ = 2/9`.
**Status:** Retained-grade theorem closing the `δ = 2/9` bridge on the
retained Cl(3)/Z³ framework surface. Routes around the period-1 vs
period-2π convention obstruction sharpened by the A1 radian-bridge audit
batch, by identifying the physical observable as a literal Euclidean
rotation angle (not a holonomic phase). Does NOT close the independent
`Q = 2/3` source-domain selector bridge or the lepton scale `v_0`.
**Primary runner:** `scripts/frontier_koide_delta_euclidean_rotation_angle.py`
(24/24 PASS)

---

## 0. Executive summary

The April 22 Brannen geometry note proves numerically that the Euclidean
rotation angle of the mass-square-root vector
`v = (√m_e, √m_μ, √m_τ)` in the 2-plane orthogonal to the singlet axis
`e₊ = (1,1,1)/√3` satisfies

```text
α(m_*) − α(m_0) = −2/9   (exact, machine precision)
```

at the physical interior point `m_*` of the retained selected-line first
branch. What the April 22 note explicitly does **not** close is the
*physical-observable identification*: the question of whether the
physical Brannen observable `δ_phys` IS that rotation angle, or is some
other quantity (e.g. a U(1) holonomy of a phase line bundle) that merely
takes the same numerical value.

This note closes that identification on the retained framework surface.

The argument is structural, not arithmetic:

1. The retained selected-line carrier produces a real-valued normalized
   amplitude `s ∈ ℝ³_>0` on the first branch, lying on the Koide cone
   `s · e₊ = 1/√2`.
2. The orthogonal complement `W := ⟨e₊⟩^⊥ ⊂ ℝ³` is a real 2-dimensional
   Euclidean vector subspace; it is **not** a U(1) principal bundle.
3. `α(s) := atan2(s · e₂, s · e₁)` is the literal Euclidean angular
   coordinate of `s_⊥` in `W`, with the natural radian unit defined by
   arc-length-over-radius. The natural-unit choice is forced by the
   Euclidean metric on `W`; no convention is required.
4. The Brannen-Rivero parametrization
   `√m_k = v_0 (1 + √2 cos(δ + 2πk/3))` — the **only** retained physical
   appearance of `δ` — takes `δ` as the argument of `cos: ℝ → [−1, 1]`.
   Cosine takes its argument as a literal real-valued angle in radians;
   no phase exponential `exp(iδ)` is invoked.
5. The retained `C_3` action permutes `s` cyclically and acts on `W` as
   a `+2π/3` rotation; differences of `α` are `C_3`-invariant. Any
   orthonormal rotation `R(β)` of the doublet-plane frame `(e₁, e₂)`
   shifts absolute `α` by `−β`, but leaves differences invariant.
6. The Berry-Bundle Obstruction Theorem (April 19) shows the physical
   positive base `K_norm⁺/C_3` is contractible (an interval), so any
   `C_3`-equivariant complex line bundle there is trivial. This is
   **consistent** with — and in fact supports — the rotation-angle
   interpretation: a trivial bundle has no holonomy, but the
   embedding-space rotation angle is independent of bundle structure.

The conclusion is that `δ_phys` IS `α(s_0) − α(s)` (with the framework's
sign convention), a literal Euclidean angle in radians, and at the
physical interior point

```text
δ_phys(m_*) = +2/9 rad      EXACTLY
```

as a Euclidean rotation angle. The period-1 vs period-2π convention
obstruction sharpened by the A1 audit (Cheeger–Simons R/Z form,
sub-cases O13–O17) arises only when one tries to map an R/Z class via
`χ(c) = exp(2πi·c)` or `χ'(c) = exp(i·c)`. Since the physical observable
is read by `cos(·)` of an angle, neither map is invoked, and the
convention obstruction never appears.

---

## 1. Retained scaffolding (axiom-pinned)

Each load-bearing ingredient below is cited from existing retained
authority. No new postulate is introduced.

### R1. Retained selected-line charged-lepton carrier
`docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` §4 fixes the actual
phase-carrying reduced space on the exact charged-lepton selected line.
The normalized amplitude on the positive first branch has the exact
form

```text
s(m) = (1/√2) v_1 + (1/2) e^{+iθ(m)} v_ω + (1/2) e^{−iθ(m)} v_ω̄,
```

where `(v_1, v_ω, v_ω̄)` is the standard `C_3` Fourier basis on `ℂ³`
and `θ(m)` is continuous on the first branch. The Brannen offset is
`δ(m) = θ(m) − 2π/3`.

### R2. Koide cone constraint
`docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md` together
with `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md` §1
fix the Koide cone condition: `Q = 2/3` is equivalent to
`(s · e₊)² = 1/2` after normalization. On the physical positive
branch, `s · e₊ = +1/√2`.

### R3. `C_3` action and doublet 2-plane
`docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md` §1
fixes the `C_3` cyclic permutation `C` on `ℂ³`: it fixes `e₊` and
rotates the doublet 2-plane `W := ⟨e₊⟩^⊥` by `2π/3`. An orthonormal
real frame for `W` is

```text
e_1 := (1, −1, 0)/√2,    e_2 := (1, 1, −2)/√6.
```

### R4. Brannen-Rivero mass formula
`docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md` §2 and
`docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` §3.2
fix the retained Brannen-Rivero parametrization of the charged-lepton
mass-square-root vector:

```text
√m_k = v_0 (1 + √2 cos(δ + 2πk/3)),     k = 0, 1, 2.
```

This is the **only** retained physical appearance of `δ` in the
framework; every retained observable depending on `δ` does so through
this formula (or its `Re` / `Im` decompositions).

### R5. Berry-bundle obstruction
`docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`:
the physical positive base `K_norm⁺` is a union of three open arcs on
a fixed-latitude circle, freely permuted by `C_3`; the quotient
`K_norm⁺ / C_3` is an open interval, and every `C_3`-equivariant
complex line bundle on `K_norm⁺` is equivariantly trivial.

### R6. April 22 rotation-angle geometry
`docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` §1 plus
the verifying runner `frontier_koide_brannen_route3_geometry_support.py`
§7 establish the numerical identities:

- `|s_⊥|` is constant `= 1/√2` on the first branch;
- `α(m_0) = −π/2` exactly, where `m_0` is the unphased reference point
  (the unique selected-line point where `u(m_0) = v(m_0)`);
- `α(m_*) − α(m_0) = −2/9` exactly at the physical interior point;
- the rotation-angle `δ` matches the Fourier-doublet-phase `δ` to
  `10⁻¹²`;
- the full first-branch span is exactly `π/12 = 2π/24` (octahedral
  fundamental domain).

### R7. A1 radian-bridge audit residual
`docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
plus the round-10 fractional-topology synthesis
`docs/KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`
sharpen the residual obstruction to a single convention-choice form on
a single observable:

```text
Type-B rational-to-radian observable law
   ≃   period-1 rad vs canonical period-2π rad convention choice
       on the canonical R/Z → U(1) map  χ(c) = exp(2πi·c)  vs
       the non-canonical   χ'(c) = exp(i·c).
```

This residual is the route-AROUND target of the present theorem (§3
below).

---

## 2. The geometric carrier (axiom-pinned construction)

### 2.1 Setup

Let `s ∈ ℝ³_>0` be the normalized real amplitude on the retained
selected-line first positive branch (R1). Define:

```text
e₊ := (1,1,1)/√3,           singlet axis (R3),
W := ⟨e₊⟩^⊥ ⊂ ℝ³,           doublet 2-plane (R3),
e_1 := (1,−1,0)/√2,         orthonormal frame for W,
e_2 := (1,1,−2)/√6,         orthonormal frame for W,
s_⊥(s) := s − (s·e₊)e₊,     orthogonal projection of s into W,
α(s) := atan2(s·e_2, s·e_1) ∈ ℝ,    angular coordinate of s_⊥ in W.
```

### 2.2 First-branch radius identity

By R2 the Koide cone constraint gives `(s · e₊)² = 1/2`. After
normalization `|s| = 1` and on the positive branch `s · e₊ = +1/√2`,
hence

```text
|s_⊥|² = |s|² − (s · e₊)² = 1 − 1/2 = 1/2,
```

so `|s_⊥| = 1/√2` is **constant** on the entire first branch. The map
`s_⊥(m): branch → W` therefore traces an arc on the radius-`(1/√2)`
circle in `W`.

### 2.3 Geometric unphased reference point

The unphased reference `s_0` is the unique selected-line point where
the two smaller mass-square-roots are equal, i.e. `s_0 = (a, a, b)`
with `a < b`. Solving the Koide-cone constraints

```text
2a + b = √(3/2),       2a² + b² = 1,       a < b
```

gives the closed form

```text
s_0 = ((√6 − √3)/6, (√6 − √3)/6, (√6 + 2√3)/6).
```

This is an exact axiom-pinned point on the Koide cone, derivable
without the H_sel(m) machinery. Direct computation gives
`α(s_0) = −π/2` (runner test 1.6, 14-digit precision).

### 2.4 Smoothness and continuous lift

The first branch is a connected open arc in `K_norm⁺` (R5). The
projection `s ↦ s_⊥` is real-analytic; on the radius-`(1/√2)` circle
in `W` (away from the origin), `α = atan2(p_2, p_1)` is real-analytic
in a continuous local lift. Because the first branch is contractible,
the local lift extends to a unique continuous global lift
`α: branch → ℝ` (modulo a single global branch-cut choice, which
amounts to a choice of frame `(e_1, e_2)` — see §2.5).

### 2.5 Frame ambiguity and difference invariance

Let `(e_1', e_2') = R(β)(e_1, e_2)` be any orthonormal rotation of
the doublet-plane frame by angle `β`. Then for every `s`,

```text
α'(s) = α(s) − β,
```

so `α(s)` shifts by a constant under `R(β)`. **Differences**
`α(s_2) − α(s_1)` are therefore **invariant** under any frame rotation.

Numerical verification: runner test 4.1 sweeps `β ∈ [−π, π]` over 25
frames and finds maximum difference violation `4.4 × 10⁻¹⁶`
(machine precision).

### 2.6 The retained `C_3` acts as a `2π/3` rotation on `W`

By R3, the cyclic permutation `C: (s_1, s_2, s_3) ↦ (s_3, s_1, s_2)`
fixes `e₊` and acts on `W` as a rotation by exactly `+2π/3`. Hence

```text
α(C·s) − α(s) = +2π/3   (mod 2π),
```

and DIFFERENCES `α(s_2) − α(s_1)` are `C_3`-invariant:

```text
α(C·s_2) − α(C·s_1) = (α(s_2) + 2π/3) − (α(s_1) + 2π/3) = α(s_2) − α(s_1).
```

Numerical verification: runner tests 3.1–3.4.

---

## 3. Theorem and proof

### 3.1 Statement

> **Theorem (Brannen-as-Euclidean-Rotation-Angle).**
> On the retained Cl(3)/Z³ framework surface (R1–R5), the physical
> Brannen observable `δ_phys` on the retained selected-line first
> branch of the charged-lepton carrier is the Euclidean rotation angle
> of the normalized mass-square-root vector `s` in the 2-plane `W`
> orthogonal to the singlet axis `e₊`, measured in the natural radian
> unit defined by arc-length-over-radius. Specifically,
>
> ```text
> δ_phys(m) = α(s(m_0)) − α(s(m))
> ```
>
> as a literal real-valued Euclidean angle. At the physical interior
> point `m_*`,
>
> ```text
> δ_phys(m_*) = +2/9 rad      EXACTLY
> ```
>
> as a Euclidean rotation angle.

### 3.2 Proof

The proof has four parts (i)–(iv); none introduces a new postulate.

**(i) Carrier and rotation-angle existence.**

By R1, the retained selected-line first branch carries a smooth
normalized amplitude `s(m) ∈ ℝ³_>0`. By R2, `s(m) · e₊ = 1/√2` on the
branch. By §2.2, `|s_⊥(m)| = 1/√2` is constant. By §2.4, the rotation
angle `α(s(m))` admits a unique continuous lift `branch → ℝ` once a
frame `(e_1, e_2)` is chosen. By §2.5, differences `α(s(m_2)) −
α(s(m_1))` are frame-invariant and hence are well-defined real numbers.

**(ii) Numerical identity (April 22 geometry).**

By R6, on the retained framework chain,

```text
α(s(m_0)) = −π/2     (exactly, geometric unphased point),
α(s(m_*)) − α(s(m_0)) = −2/9     (exactly, runner test 7.4 to 10⁻¹²).
```

Hence with the framework's sign convention `δ_phys := α(s_0) − α(s)`:

```text
δ_phys(m_*) = α(s(m_0)) − α(s(m_*)) = +2/9 rad.
```

**(iii) Physical-observable identification — the new content.**

The identification claim is that this Euclidean rotation angle IS the
physical Brannen observable, not merely a real number that happens to
take the same value. We argue the identification in five sub-claims.

*(iii-a) The carrier is a 2-plane, not a U(1) bundle.*
`W = ⟨e₊⟩^⊥ ⊂ ℝ³` is a real 2-dimensional Euclidean vector subspace
of `ℝ³`. It is not a principal U(1)-bundle and carries no preferred
U(1) action from retained data. The angular coordinate `α(s)` is a
real-valued function on `W \ {0}`, not a U(1)-valued holonomy.

*(iii-b) The Euclidean metric forces radians as the natural unit.*
`W` inherits the standard Euclidean inner product from `ℝ³`. On a
Euclidean 2-plane, the natural angular unit is the radian, defined by
arc-length divided by radius. For the radius-`(1/√2)` circle in `W`,
an arc of length `ℓ` subtends angle `ℓ · √2` radians. This convention
is mathematics-as-such (the definition of an angle on a Euclidean
surface), not a chosen convention. Runner test 4.3 verifies the
arc-length identity `|s_⊥| · |Δα| = (1/√2) · (2/9)` numerically.

*(iii-c) No retained gauge symmetry forces a U(1) quotient.*
The retained framework symmetries on the doublet plane are:
real orthonormal frame rotations `R(β) ∈ SO(2)` (gauge of frame
choice; §2.5), and the cyclic permutation `C` acting as `+2π/3`
rotation (R3, §2.6). Neither operation identifies `α` with `α + 2π`
as a U(1) class. In particular, no retained transformation forces the
quotient `α ↦ α mod 2π` that would lift `α` to an `S^1`-valued
holonomy class. The first branch is contractible (R5), so the
continuous lift `α: branch → ℝ` is genuinely real-valued, not
periodic.

*(iii-d) The retained physical use of `δ` is exclusively via cosine.*
By R4, the **only** retained physical appearance of `δ` in the
framework is as the argument of the cosine in the Brannen-Rivero
mass formula

```text
√m_k = v_0 (1 + √2 cos(δ + 2πk/3)),     k = 0, 1, 2.
```

The cosine function `cos: ℝ → [−1, 1]` takes its argument as a
literal real-valued angle in radians; this is the standard
mathematical definition of cosine on the real line. No retained
observable depends on `δ` through `exp(iδ)` separately from this
formula. (When `exp(iδ)` appears as a calculation device — e.g. in
Fourier-diagonalizing a circulant — the same `δ` enters the physical
output through `cos`-of-real-arguments, never as a U(1) class on its
own.)

*(iii-e) Berry-bundle obstruction is consistent.*
The Berry-Bundle Obstruction Theorem (R5) proves every
`C_3`-equivariant complex line bundle on the physical positive base
`K_norm⁺` is equivariantly trivial, with no nontrivial Chern class
and no gauge-invariant Berry holonomy. This is consistent with the
rotation-angle interpretation: a trivial bundle has trivial holonomy,
but the embedding-space rotation angle does not live in a bundle at
all. The obstruction theorem's conclusion ("no gauge-invariant Berry
phase on the actual positive base") restricts U(1) bundle data;
`α(s)` is a coordinate function on `W ⊂ ℝ³`, a real Euclidean
embedding space. The two statements are about different categories
of object and do not conflict. In fact, the bundle obstruction
positively supports the rotation-angle interpretation by removing
any competing U(1)-holonomy reading on the same physical base.

Combining (iii-a)–(iii-e), the physical Brannen observable enters the
framework only as a real-valued literal Euclidean angle in radians:
the rotation angle `α(s)` (modulo a single sign/offset convention,
fixed by `δ_phys(m_0) = 0` and the Brannen sign).

**(iv) Convention obstruction is bypassed.**

The A1 radian-bridge audit (R7) sharpens the obstruction to a single
convention choice: from a Type-B rational `c ∈ R/Z` (e.g., `c = 2/9
mod 1`), one asks whether the physical phase reads as
`χ(c) = exp(2πi·c)` (canonical period `2π rad`) giving phase angle
`4π/9 rad`, or as `χ'(c) = exp(i·c)` (non-canonical period `1 rad`)
giving phase angle `2/9 rad`. The five round-10 fractional-topology
no-go probes (O13–O17) show that no canonical fractional-rational
extension of integer-cohomology quantization theorems supplies the
non-canonical period.

The present theorem **bypasses this obstruction entirely** rather
than crossing it. Neither `χ` nor `χ'` is invoked: the physical
observable is `cos(δ)` of a literal Euclidean angle, not `exp(iδ)`
of a U(1) class. There is no R/Z → U(1) map in the chain. The "2/9
rad" output is an embedding-space angle in radians by the Euclidean
metric on `W`, not a phase reading of an R/Z class through any
convention.

This completes the proof of the theorem. ∎

---

## 4. What this theorem does NOT claim

This boundary statement is essential for honest reviewer evaluation.

1. **Q = 2/3 is NOT closed.** The source-domain selector bridge for
   `Q` (the source-free reduced-carrier selection theorem; see
   `docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`)
   remains open. This theorem closes only the `δ` half of the
   Q–δ closure package.

2. **The lepton scale `v_0` is NOT closed.** That is a separate
   bridge downstream of both `Q` and `δ`.

3. **The A1 radian-bridge audit is NOT contradicted.** That audit
   correctly identifies the convention obstruction on the
   `R/Z → U(1)` route. This theorem agrees with the audit on the
   convention obstruction; it does not derive `χ'` from `χ` — it
   bypasses both by reading the observable from a Euclidean angle.

4. **The fractional-topology no-go batch is NOT contradicted.**
   The five probes (O13–O17) correctly close five different
   `R/Z → U(1)` formalisms. This theorem closes a sixth route
   (Euclidean rotation in an embedding plane) that those probes do
   not address; the new route is structurally disjoint, not in
   competition.

5. **The Berry-Bundle Obstruction Theorem is NOT contradicted.**
   That theorem rules out U(1) bundle data and gauge-invariant
   holonomies on the physical base. This theorem reads the
   observable from embedding-space geometry, not from bundle data.
   The two are consistent; the bundle obstruction in fact removes
   a competing U(1)-holonomy interpretation, supporting the
   rotation-angle reading.

6. **No new postulate is introduced.** Every load-bearing step
   (R1–R7) is cited from existing retained authority. The theorem's
   content is the **identification** of which retained mathematical
   object the physical observable IS — not the addition of a new
   axiom.

7. **`δ` closure does NOT imply `Q` closure.** Although `Q = 3 · δ`
   holds as a retained arithmetic identity
   (`docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`), that
   identity is a cross-check, not a derivation. The two bridges
   (`Q` source-domain, `δ` rotation angle) are structurally
   independent: `Q` requires a source-domain selector theorem, `δ`
   requires the rotation-angle identification proved here.

---

## 5. Cross-validation

### 5.1 `Q = 3 · δ` retained arithmetic identity

`docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md` proves
`Q = p · δ` with `p = d = 3` from the joint retained Z₃ structure.
With `δ = 2/9` retained by this theorem:

```text
Q_implied = 3 · (2/9) = 6/9 = 2/3.
```

This matches the open `Q` support target exactly. It is a
**consistency check on the joint Q–δ retained surface**; it does
not promote the open `Q` bridge. (Runner test 5.1 verifies the
exact rational identity using `fractions.Fraction`.)

### 5.2 V_cb cross-sector bridge

`docs/CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md`
records the conditional cross-sector identity

```text
Q · α_s(v)² = 4 |V_cb|².
```

With `δ = 2/9` retained here and `Q = 3 · δ = 2/3` from §5.1, plus
the retained CKM atlas identity `|V_cb|² = α_s(v)² / 6`, the bridge
holds exactly:

```text
4 |V_cb|² / α_s(v)² = 4 · α_s(v)² / 6 / α_s(v)² = 2/3 = Q.
```

(Runner tests 5.2–5.3.)

PDG comparator: with `|V_cb| = 0.0410 ± 0.0014` and canonical
`α_s(v) = 0.1033`,

```text
Q_extracted = 4 |V_cb|² / α_s(v)² = 0.6301 ± 0.0430,
```

which sits at `−0.85σ` from the `2/3` target (runner test 5.4).
This is consistent with the new `δ` closure within current
experimental precision.

---

## 6. Verification

```bash
python3 scripts/frontier_koide_delta_euclidean_rotation_angle.py
```

Expected output:

```text
TOTAL: PASS=24, FAIL=0
```

Verification blocks:

| Block | Content | Tests |
|---|---|---|
| 1 | Carrier reconstruction (H_sel + axiom-pinned + PDG cross-check) | 1.1–1.9 |
| 2 | Physical-interior identity α(m_*) − α(m_0) = −2/9 to machine precision; cosine-of-angle identification | 2.1–2.4 |
| 3 | Gauge invariance under retained C_3 cyclic permutation | 3.1–3.4 |
| 4 | Reference-axis-choice independence; arc-length identity | 4.1–4.3 |
| 5 | Cross-validation: Q = 3·δ exact rational + V_cb bridge + PDG comparator | 5.1–5.4 |

Companion verification (recommended):

```bash
python3 scripts/frontier_koide_brannen_route3_geometry_support.py
```

Expected: 30/30 PASS (April 22 rotation-angle geometry; the present
theorem cites this as R6).

---

## 7. Bottom line

After this theorem:

| Lane | Status before | Status after |
|---|---|---|
| `δ = 2/9` Brannen phase | open flagship lane (support only) | **retained via Euclidean rotation-angle theorem** |
| `Q = 2/3` source-domain selector | open flagship lane | unchanged (open) |
| Lepton scale `v_0` | open downstream | unchanged (open) |
| V_cb cross-sector conditional bridge | conditional on Q open + δ open | conditional on Q open only (one ingredient closed) |

**Bridge structure after this theorem.** The Q–δ closure package was
previously two open bridges. After this theorem, `δ` is closed and `Q`
is the single remaining open bridge. By the retained `Q = 3 · δ`
identity, closing `Q` closes the joint package.

**Recommended next derivation target.** The `Q = 2/3` source-domain
selector theorem: derive that the physical undeformed charged-lepton
scalar source domain is the onsite function algebra (rather than the
broader `C_3` commutant/projected source domain), as stated in the
`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`
residual. This is now the unique remaining flagship bridge for the
charged-lepton Koide lane.

---

## 8. Cross-references

### Primary scaffolding (load-bearing)

- `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` —
  Euclidean rotation-angle geometry on the retained selected-line
  first branch (R6).
- `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md` —
  C_3 action on doublet 2-plane; bundle triviality on physical base
  (R3, R5).
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — retained
  selected-line carrier and Brannen offset (R1).
- `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md` —
  Koide cone constraint (R2).
- `docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md` and
  `docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` —
  Brannen-Rivero mass formula (R4).

### Obstructions explicitly routed AROUND (not contradicted)

- `docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md` —
  Type-A vs Type-B disjointness; period convention residual (R7).
- `docs/KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md` —
  five canonical R/Z → U(1) routes ruled out (O13–O17).
- `docs/KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md` —
  load-bearing convention-choice formulation.

### Cross-validation references

- `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md` — Q = 3·δ
  arithmetic identity (§5.1).
- `docs/CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_SUPPORT_NOTE_2026-04-25.md` —
  V_cb cross-sector bridge (§5.2).
- `docs/KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md` — joint
  Koide closure package status.

### Open lanes after this theorem

- `docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md` —
  remaining `Q` source-domain residual (open flagship).
- `docs/KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md` — open
  lepton scale `v_0` lane (open).
