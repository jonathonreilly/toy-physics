# Convention C-iso — Four-Layer Stratification Theorem (Bounded)

**Date:** 2026-05-07
**Type:** bounded_theorem candidate (parallel to
[`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md))
**Status authority:** independent audit lane only. Source-note proposal —
audit verdict and downstream status are set only by the independent audit lane.
**Branch:** `claude/confident-robinson-5c47a5`
**Companion analytical note:** [`outputs/action_first_principles_2026_05_07/w3_derive_c_iso/THEOREM_NOTE.md`](../outputs/action_first_principles_2026_05_07/w3_derive_c_iso/THEOREM_NOTE.md)
**Companion attack log:** [`outputs/action_first_principles_2026_05_07/w3_derive_c_iso/ATTACK_RESULTS.md`](../outputs/action_first_principles_2026_05_07/w3_derive_c_iso/ATTACK_RESULTS.md)
**Verification runner:** [`scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py`](../scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py)
**Verification log:** [`outputs/action_first_principles_2026_05_07/w3_derive_c_iso/lieb_robinson_velocity_run.txt`](../outputs/action_first_principles_2026_05_07/w3_derive_c_iso/lieb_robinson_velocity_run.txt)

---

## 0. Audit context

This note characterizes Convention C-iso of
[`outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md)
into a four-layer stratification, parallel to the `g_bare` four-layer
stratification of
[`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md).

The note **strengthens** the existing C-iso characterization in three ways:

1. Decomposes C-iso into one **genuinely admitted scalar** (`a_τ = a_s`)
   plus one **bounded parsimony selection** (Wilson-temporal vs
   heat-kernel-temporal).
2. **Absorbs the parsimony selection** into the existing continuum-action-form
   parsimony framework
   ([`outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md)),
   so it is no longer a separately-named admission.
3. **Documents the structural obstruction** for the genuinely admitted scalar.

This note does **NOT** claim:
- That `a_τ = a_s` is uniquely forced by `A1` (Cl(3)) and `A2` (Z³)
  alone — the absolute convention status of `a_τ` is the remaining open
  foundational question.
- That standard 4D isotropic Wilson is uniquely forced. It is the comparator
  reached after admitting `a_τ = a_s` and using continuum-equivalence-class
  parsimony.

---

## 1. Claim scope

> **Theorem (Convention C-iso four-layer stratification, candidate).**
> Under the framework's retained primitive stack
>
> - A1: Cl(3) at sites
>   ([`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)),
> - A2: Z³ substrate
>   ([`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)),
> - canonical Cl(3) Tr-form `Tr(T_a T_b) = δ_ab/2`
>   ([`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md)),
> - retained reflection positivity
>   ([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)),
> - retained microcausality / Lieb-Robinson
>   ([`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)),
> - retained single-clock codimension-1 evolution
>   ([`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)),
> - candidate Theorem A2.5
>   ([`outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md)),
> - candidate Theorem T-AT (Anisotropic Trotter Dictionary)
>   ([`outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md)),
>
> the dictionary from `S_AT[U; ξ]` (the Trotter-derived anisotropic action)
> to standard 4D isotropic Wilson at `β = 6` decomposes into exactly
> **four layers**, of which exactly **one** is a genuine convention:
>
> | Layer | Statement | Status | Evidence |
> |---|---|---|---|
> | L1 | A1 + A2 (Cl(3) at sites + Z³ substrate) | **DERIVED** (axiom) | minimal axioms note |
> | L2 | RP transfer matrix + Stone's theorem give unique self-adjoint `H` and `T(a_τ) = exp(-a_τ H)` for any `a_τ > 0` | **DERIVED** | RP theorem + single-clock theorem (S1) |
> | L3a | Choice of temporal step `a_τ` (i.e., anisotropy `ξ = a_s/a_τ`) | **CONVENTION** (admitted; choice = `1`) | structural obstruction; this note §3 |
> | L3b | Choice of lattice form for the temporal-plaquette weight | **PARSIMONY** within continuum-equivalence class (bounded `O(g²)`; absorbed into A2.5) | T-AT.3 numerical verification + A2.5 continuum-action parsimony |
> | L4 | Standard 4D Wilson at `β = 6` | **DERIVED** from L3 (algebra) | `β = 2N_c/g_KS² = 6` at `g_KS² = 1`, `N_c = 3`, ξ = 1 |
>
> Equivalently:
>
> **(C1) The anisotropic Trotter dictionary is forced** by L1 + L2 +
> Theorem T-AT. The *form* of the dictionary is uniquely determined.
>
> **(C2) The numerical value of `ξ = 1`** is the L3a admission. There is
> no axiom-derived value of `ξ`. The choice `ξ = 1` is the standard
> downstream choice "compare to 4D isotropic Wilson MC at `β = 6`", not a
> primitives-derivation.
>
> **(C3) The Wilson-temporal vs heat-kernel-temporal selection** is L3b
> parsimony, bounded by the continuum-equivalence-class width
> (Theorem A2.5). The numerical magnitude is `O(g²) ≈ 7-9%` at canonical
> `s_t = 0.5`, identical to the existing A2.5 parsimony band re-applied
> to the temporal sector.
>
> **(C4) The reduction `g_KS² = 1 ↔ β_W = 6` at leading order** is L4 — a
> derived constraint once L3a is admitted, with explicit one-loop
> anisotropy-radiative correction from Karsch 1982 / Klassen 1998.
>
> **(C5) Alternative bare anisotropies `ξ ≠ 1` give the same continuum
> physics** modulo `O(g²)` finite-lattice artifacts, by the
> continuum-action-form equivalence-class argument (Theorem A2.5).
>
> Therefore the framework has **exactly one genuine convention layer in
> the C-iso chain** — the choice `a_τ = a_s` of the temporal step at the
> spatial scale.

---

## 2. What this theorem uses

This note is downstream of the retained / candidate-retained surface:

1. **A1 + A2** (`Cl(3)` + `Z³` substrate): retained_axiom.
2. **Canonical Cl(3) Tr-form**: retained via
   [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md)
   and
   [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md).
3. **Retained reflection positivity**:
   [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md).
4. **Retained microcausality / Lieb-Robinson**:
   [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md).
5. **Retained single-clock codimension-1 evolution**:
   [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md).
6. **Candidate Theorem A2.5** (continuum-level Wilson-form):
   [`outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md).
7. **Candidate Theorem T-AT** (anisotropic Trotter dictionary):
   [`outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md).

The proof uses NO additional axiom. In particular, no extra primitive is
introduced beyond what is already in the framework's primitive stack.

---

## 3. The L3a structural obstruction

**Claim.** No theorem in the retained primitive stack
`{A1, A2, canonical Tr-form, RP, locality, single-clock, A2.5, T-AT}` forces
`a_τ = a_s`.

**Proof sketch (six attack vectors investigated; full details in
[`outputs/action_first_principles_2026_05_07/w3_derive_c_iso/ATTACK_RESULTS.md`](../outputs/action_first_principles_2026_05_07/w3_derive_c_iso/ATTACK_RESULTS.md)):**

1. **Lieb-Robinson velocity** `v_LR = 2 e r J` is `g²`-dependent. At
   canonical `g² = 1`, `v_LR ≈ 5.4` (numerically), giving "natural"
   `a_τ = a_s/v_LR ≈ 0.18 a_s` ≠ `a_s`. Sweep over `g²` confirms `v_LR`
   is not a `g²`-independent constant. (Numerical run:
   [`outputs/action_first_principles_2026_05_07/w3_derive_c_iso/lieb_robinson_velocity_run.txt`](../outputs/action_first_principles_2026_05_07/w3_derive_c_iso/lieb_robinson_velocity_run.txt).)

2. **Single-clock structure** pins the *form* (one-parameter unitary
   group `U(t) = exp(-itH)`, Stone's theorem on retained `H_phys`), not
   the *step* `a_τ`. The Single-Clock theorem (S1) explicitly defines
   `T(a_τ) = exp(-a_τ H)` for arbitrary `a_τ > 0`; no canonical value
   is selected.

3. **Continuum-limit emergent-Lorentz** is established at the level of
   *renormalized* propagator coefficients, not bare `ξ_bare`. The
   Karsch-Klassen one-loop calibration gives `ξ_bare(g²) ≠ 1` even when
   the renormalized speed of light = 1. Bare `ξ_bare = 1` is a parameterization
   choice, with infrared physics independent of this choice (modulo
   `O(g²)` finite-lattice artifacts).

4. **Heat-kernel temporal IS the framework's derived prediction**
   (Theorem T-AT). The "Wilson-replace" step is a reinterpretation for
   downstream comparison, not a derivation.

5. **Action-form continuum equivalence** (Theorem A2.5): Wilson-temporal
   and heat-kernel-temporal both produce the same continuum action
   `Tr(F²)`; difference is `O(s_t) = O(g²)` Symanzik-irrelevant
   correction. Absorbed into A2.5 parsimony.

6. **Reflection positivity** is satisfied by both Wilson-temporal and
   heat-kernel-temporal. RP does not select one over the other.

The structural obstruction is that **A1 + A2 fix only spatial structure**:
time is *emergent* via RP transfer-matrix reconstruction. The temporal
lattice spacing `a_τ` is a parameter of the *discretization choice*, not
a quantity forced by the framework's axioms.

Promoting `a_τ = a_s` to a derived theorem would require **either**:
- an additional substrate axiom `Z⁴` (rejected by A2 — would change the
  framework), **or**
- demanding emergent-Lorentz at the bare lattice level (impossible on any
  cubic lattice), **or**
- admitting a primitive that pins the renormalized speed of light at all
  `g²` (= Karsch-Klassen calibration; engineering, not primitives).

None of these is currently a retained derivation.

---

## 4. The L3b parsimony absorption

**Claim.** The Wilson-temporal vs heat-kernel-temporal choice is bounded
within the continuum-equivalence-class parsimony framework of Theorem
A2.5, and is therefore **not** a separately-named admission.

**Proof sketch.** By Theorem A2.5
([`outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md)),
the continuum-level magnetic operator on each spatial plaquette is uniquely
`α_eff · Tr(F²)`. Wilson-spatial, heat-kernel-spatial, and Manton-spatial are
different lattice representatives of the same continuum operator, with
difference `O(a²)` Symanzik-irrelevant.

The same argument applies to the *temporal*-plaquette weight: at the continuum
level, Wilson-temporal and heat-kernel-temporal both produce the same
`Tr(F_{0i}²)` operator, with difference `O(a²)`. Numerically (Theorem
T-AT.3), the difference is `O(s_t) = O(g²/(2ξ))`, giving `~7-9%` at canonical
`s_t = 0.5`.

This is the same magnitude and same structural origin as the existing A2.5
parsimony bound applied to the spatial sector. Therefore C-iso.ii is
absorbed into A2.5 — not a separate admission.

---

## 5. Why this matters — net effect on the bridge

### Before (per [`outputs/action_first_principles_2026_05_07/UNIFIED_BRIDGE_STATUS_2026_05_07.md`](../outputs/action_first_principles_2026_05_07/UNIFIED_BRIDGE_STATUS_2026_05_07.md))

```yaml
admitted_context_inputs:
  - N_F = 1/2 canonical Gell-Mann trace normalization
  - Convention C-iso (one opaque convention; bounded O(g²) ~ 5-15%)
  - Continuum-equivalence-class parsimony (~5-10% across {Wilson, HK, Manton})
```

**Three admissions**, with C-iso opaque.

### After (this note)

```yaml
admitted_context_inputs:
  - N_F = 1/2 canonical Gell-Mann trace normalization
    (L3 of g_bare four-layer stratification)
  - C-iso.i: a_tau = a_s (time-discretization at the spatial scale;
    L3a of C-iso four-layer stratification, this note)
  - Continuum-equivalence-class parsimony (now subsumes BOTH
    Wilson/HK/Manton continuum-action selection AND C-iso.ii
    Wilson-temporal/HK-temporal selection; ~5-15% bounded; A2.5)
```

**Two scalar admissions plus one bounded parsimony**, all transparently
named.

The headline change: C-iso decomposes cleanly, and Wilson-temporal vs
HK-temporal is no longer a separate admission. The bridge has exactly **two
genuine scalar admissions** (`N_F = 1/2`, `a_τ = a_s`) plus **one
continuum-equivalence-class parsimony bound**.

---

## 6. Why this is parallel to the `g_bare` four-layer stratification

The two stratifications are structurally identical:

| Aspect | `g_bare` chain | C-iso chain |
|---|---|---|
| L1 | A1 + A2 (axiom) | A1 + A2 (axiom) |
| L2 | Hilbert-Schmidt structure on `g_conc` (Killing rigidity) | RP transfer matrix + Stone's theorem (single-clock) |
| L3 (admission) | `N_F` overall scalar of HS form (= `1/2`) | `a_τ` temporal step (= `a_s`) |
| L3 (parsimony) | none separate | L3b: Wilson-temporal vs HK-temporal (absorbed into A2.5) |
| L4 (derived constraint) | `g_bare = 1` algebra | `β_W = 6` algebra |

Both stratifications:
- Identify exactly one **genuinely admitted scalar** (the L3 admission).
- Use existing retained framework structure for L1 and L2.
- Derive L4 trivially as algebra once L3 is admitted.
- Could in principle promote the L3 admission via a higher principle, but
  none is currently retained.

This parallelism is a strong consistency check on the framework's
admission-stratification methodology.

---

## 7. Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  Convention C-iso decomposes into a four-layer stratification:
  - L1: A1 + A2 (axiom)
  - L2: RP + Stone (derived; transfer matrix T(a_tau) = exp(-a_tau H) exists for any a_tau > 0)
  - L3a: a_tau = a_s (genuine convention; structural obstruction documented)
  - L3b: Wilson-temporal vs HK-temporal (parsimony within A2.5 continuum-equivalence class; absorbed into A2.5 bound)
  - L4: standard 4D Wilson at beta_W = 6 (derived algebra once L3a is admitted)
  Net: exactly one admitted scalar (a_tau = a_s) plus one parsimony band (subsumed by A2.5).
proposed_load_bearing_step_class: A (algebra; obstruction is structural, not technical)
audit_required_before_effective_retained: true
admitted_context_inputs:
  - A_min retained
  - candidate Theorem A2.5
  - candidate Theorem T-AT
proof_load_bearing_steps:
  1. Stone's theorem on retained H_phys: T(a_tau) = exp(-a_tau H) for any a_tau > 0 (class A).
  2. v_LR = 2 e r J is g^2-dependent; verified numerically (class A).
  3. Single-clock theorem (S1) pins form, not step (class A; direct from Stone).
  4. Both Wilson-temporal and heat-kernel-temporal satisfy RP; not selected by RP (class A).
  5. Wilson-vs-HK temporal absorbed into A2.5 continuum-equivalence-class parsimony (class A).
companion_obstruction_note: outputs/action_first_principles_2026_05_07/w3_derive_c_iso/THEOREM_NOTE.md
companion_attack_log: outputs/action_first_principles_2026_05_07/w3_derive_c_iso/ATTACK_RESULTS.md
```

---

## 8. What this theorem does NOT claim

- That `a_τ = a_s` itself is uniquely forced by `A1` (Cl(3)) and `A2`
  (Z³) alone — the absolute convention status of `a_τ` is the remaining
  open foundational question (parallel to `N_F = 1/2`).
- That standard 4D isotropic Wilson MC at `β = 6` is uniquely forced.
- That the framework's prediction `⟨P⟩_KS(g²=1)` equals
  `⟨P⟩_W(β=6) = 0.5934` exactly. The bound is `O(g²) ≈ 5-15%` per existing
  C-iso characterization.

---

## 9. Citations

- **A_min**: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **Parallel stratification (`g_bare`)**:
  - [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  - [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- **Retained primitives used**:
  - [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
  - [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
  - [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
  - [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md)
- **Candidate inputs**:
  - [`outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/A2_5_DERIVED_THEOREM.md)
  - [`outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md`](../outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVED_THEOREM.md)
  - [`outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVATION_RESULTS.md`](../outputs/action_first_principles_2026_05_07/DICTIONARY_DERIVATION_RESULTS.md)
- **Standard physics references** (cited as inputs, not framework axioms):
  - Karsch F. (1982), *Nucl. Phys.* B205, 285 — anisotropic Wilson; one-loop coupling matching.
  - Klassen T. (1998), *Nucl. Phys.* B533, 557 — SU(N) one-loop anisotropy coefficients.
  - Hasenfratz A., Hasenfratz P. (1981), *Nucl. Phys.* B193, 210.
  - Engels J., Karsch F., Satz H. (1982), *Phys. Lett.* B113, 398.
  - Suzuki M. (1976), *Comm. Math. Phys.* 51, 183.
  - Kogut J., Susskind L. (1975), *Phys. Rev.* D11, 395.
  - Smit J. (2002), *Introduction to Lattice Gauge Theory*, Cambridge §4.4.
  - Hall B. (2003), *Lie Groups, Lie Algebras, and Representations*, §11.3.
  - Helgason S. (1978), *Differential Geometry, Lie Groups, and Symmetric Spaces*, ch. III §6.
  - Polyakov A. M. (1980), *Phys. Lett.* B72, 477 — heat-kernel asymptotic.
