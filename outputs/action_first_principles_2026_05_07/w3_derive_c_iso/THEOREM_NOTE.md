# Convention C-iso — Derivation Attempt: Bounded Result with Structural Obstruction

**Date:** 2026-05-07
**Workspace:** `outputs/action_first_principles_2026_05_07/w3_derive_c_iso/`
**Type:** source-note proposal — bounded derivation with named obstruction
**Outcome class:** **(c) Obstruction with one component partially derivable as O(g²) bounded**
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.
**Companion:** [`ATTACK_RESULTS.md`](ATTACK_RESULTS.md) (per-attack-vector log)
**Companion:** [`lieb_robinson_velocity_run.txt`](lieb_robinson_velocity_run.txt)
**Verification runner:** [`scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py`](../../../scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py)

---

## Executive summary

Convention C-iso reduces the **anisotropic** Trotter dictionary (Theorem T-AT
of [`DICTIONARY_DERIVED_THEOREM.md`](../DICTIONARY_DERIVED_THEOREM.md)) to the
**isotropic** Wilson 4D action at `β = 6` by admitting two sub-conventions:

> **(C-iso.i)** `a_τ = a_s` — time-discretization at the spatial scale
> (`ξ = 1`).
>
> **(C-iso.ii)** Wilson-replacement of the heat-kernel-form temporal
> plaquettes (an `O(g²)` finite-step correction).

This note attempts to derive C-iso from Cl(3)/Z³ primitives via six attack
vectors, and finds:

| Sub-component | Status | Margin |
|---|---|---|
| **C-iso.i** (`a_τ = a_s`) | **Genuinely admitted convention** | obstruction documented; cannot be derived from primitives |
| **C-iso.ii** (Wilson-replace) | **Bounded result** at `O(g²) ≈ 7-9%` (already known per Theorem T-AT.3); the Wilson-replace step is itself an admitted parsimony selection within the continuum-equivalence class | known O(g²); not eliminable without entering the parsimony equivalence class |
| **Joint C-iso bound** | **Bounded** at `O(g²) ≈ 5-15%` total (unchanged from existing) | unchanged |

**Therefore:** the bridge admissions reduce to **one admitted scalar
(`N_F = 1/2`) plus the existing `Convention C-iso` (now structurally
characterized as one genuinely admitted choice + one bounded parsimony
selection)** plus **continuum-equivalence-class parsimony**.

C-iso does NOT collapse to a derived theorem under the six attack vectors
investigated. The structural obstruction is that **Cl(3) and Z³ define no
emergent 4D substrate** — time is emergent in the framework's RP
reconstruction, and the temporal lattice spacing `a_τ` is a parameter of
the *discretization choice*, not a quantity forced by primitives.

This is a **clean, audit-defensible negative result** that strengthens the
existing bridge status: rather than an opaque "Convention C-iso", we now
have a four-layer stratification analogous to the `g_bare` chain
(parallel to [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)),
which **isolates the genuine admission to `(C-iso.i)` alone**.

---

## 1. The starting point: anisotropic-Trotter theorem

From [`DICTIONARY_DERIVED_THEOREM.md`](../DICTIONARY_DERIVED_THEOREM.md), the
Trotterization of `T = e^{-a_τ H_KS}` produces an **anisotropic 4D Euclidean
lattice action** with:

```
S_AT[U; ξ] = -Σ_{spatial p} β_σ · (1/N_c) Re Tr_F U_p^{(σ)}
            + Σ_{temporal p} [-ln K_{s_t}(U_p^{(τ)})]                 (S_AT)
```

with derived couplings

```
β_σ = 1/(g² ξ),       s_t = g²/(2ξ),       ξ = a_s/a_τ.            (T-AT couplings)
```

This is **theorem-grade** (positive theorem candidate; T-AT). It depends only
on retained primitives plus `A2.5` (which itself has a continuum-level
derivation per [`A2_5_DERIVED_THEOREM.md`](../A2_5_DERIVED_THEOREM.md)).

The remaining gap is to derive the **isotropic Wilson 4D action at `β = 6`**
from `(S_AT)`, which requires **Convention C-iso**:

> Set `ξ = 1` and replace `[-ln K_{s_t}(U_p^{(τ)})] ↦ -β_τ · (1/N_c) Re Tr_F U_p^{(τ)}` with `β_τ = β_σ`.

Each sub-step is examined below.

---

## 2. Stratification — analogous to the `g_bare` four-layer structure

The `g_bare` analysis identified four layers, of which exactly one (`L3 = N_F`)
is genuine convention. Following that template, the C-iso decomposition is:

| Layer | Statement | Status | Authority |
|---|---|---|---|
| **L1** | `Cl(3)` algebra at sites + `Z³` substrate | DERIVED (axiom A1 + A2) | [`MINIMAL_AXIOMS_2026-05-03.md`](../../../docs/MINIMAL_AXIOMS_2026-05-03.md) |
| **L2** | Time emerges from RP transfer-matrix reconstruction; `H` uniquely defined; `T(a_τ) = exp(-a_τ H)` for any `a_τ > 0` | DERIVED (Stone's theorem on retained `H`) | [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md), [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md) |
| **L3a** | Choice of temporal step `a_τ` (anisotropy `ξ = a_s/a_τ`) | **CONVENTION** (admitted) | this note's central finding; structural obstruction (§3) |
| **L3b** | Choice of lattice form for the temporal plaquette weight (heat-kernel = canonical Trotter; Wilson = parsimony alternative within continuum-equivalence class; both yield same `Tr(F²)` at leading order) | PARSIMONY-WITHIN-EQUIVALENCE-CLASS (bounded `O(g²)`) | [`A2_5_DERIVED_THEOREM.md`](../A2_5_DERIVED_THEOREM.md), [`DICTIONARY_DERIVED_THEOREM.md`](../DICTIONARY_DERIVED_THEOREM.md) Corollary T-AT.3 |
| **L4** | Standard 4D Wilson at `β = 6` (= comparator for Wilson 4D MC) | DERIVED-from-L3 (algebra) | trivially: at `ξ = 1`, `β_σ = 1/g²`, and `β_W = 2N_c/g_W² = 6` from `g_W² = g_KS² = 1` and `N_c = 3` |

**Reading:**
- L1 + L2 are derived.
- **L3a** is the *single genuinely admitted convention* in C-iso. Per the
  stratification, no axiom-chain in `{A1, A2, canonical Tr-form, RP, locality,
  single-clock, A2.5}` forces `a_τ = a_s`. This is the structural-obstruction
  analogue of `N_F = 1/2` in the `g_bare` chain.
- L3b is bounded by `O(g²)` per existing T-AT.3, and falls within the
  continuum-action-form parsimony equivalence class (already accounted for in
  the bridge bound).
- L4 is derived once L3a, L3b are admitted.

**Net:** C-iso reduces from "two admissions" to "one admitted scalar (`a_τ`)
plus one bounded parsimony selection (Wilson-temporal vs heat-kernel-temporal,
equivalence class enforced)".

This is the **strongest possible** characterization analogous to the `g_bare`
four-layer result.

---

## 3. The structural obstruction — why `a_τ = a_s` is genuinely admitted

The framework's axioms define **only spatial** structure: `Cl(3)` at sites
plus `Z³` substrate. Time is **emergent** via the RP transfer-matrix
reconstruction.

The mathematical content is:

```
Given: A1 + A2 + canonical Tr-form + RP + locality + single-clock,
       the framework derives a self-adjoint Hamiltonian H on H_phys.

For each a_τ > 0,
       T(a_τ) := exp(-a_τ H)  is a valid positive transfer matrix
       on H_phys (Stone's theorem, plus single-clock theorem (S1)).

The choice of a_τ is a parameter of the temporal discretization,
       not a quantity forced by the framework's axioms.
```

This is the precise content of the Single-Clock theorem (S1)–(S2) of
[`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md):
single-clock fixes the *form* (one-parameter unitary group `U(t) = exp(-itH)`),
not the *step* `a_τ`.

The framework's emergent-Lorentz program
([`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](../../../docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md))
gives a **continuum-limit speed of light** `c < ∞` as the asymptotic
light-cone slope, but the *lattice* anisotropy ratio `ξ` can take any value
without violating any framework primitive.

In particular:

- **Lieb-Robinson velocity** `v_LR = 2 e r J` is a *bound on signal
  propagation*, with dimensions of (lattice unit / time). It is a
  bounded operator-theoretic quantity that depends on `g²` and the
  operator-norm proxy `J`. Numerically, at canonical `g² = 1`, `v_LR ≈
  5.4` in units of `(a_s/time)` (per [the LR run log](lieb_robinson_velocity_run.txt)), giving a "natural"
  `a_τ = a_s/v_LR ≈ 0.18 a_s`, which is **not** equal to `a_s`. The LR
  velocity does **not** pin `ξ = 1`.

- **Continuum-limit isotropy** of the emergent-Lorentz dispersion is
  established at the level of *renormalized* propagator coefficients,
  not at the level of the bare lattice anisotropy `ξ`. The Karsch-Klassen
  one-loop calculation shows that for `ξ_renormalized = 1` (renormalized
  speed of light = 1), the bare `ξ_bare` is shifted by a known one-loop
  factor — but neither `ξ_bare = 1` nor `ξ_renormalized = 1` is forced by
  the framework. The choice of which `ξ` to call "isotropic" is itself a
  matter of which observable one demands isotropic.

This obstruction is **structural**: it is not a calculational gap to be
filled, but a feature of the framework's axiomatic minimality. Promoting
`a_τ = a_s` to a derived theorem would require **either**:

- (A) admitting an additional substrate axiom `Z⁴` instead of `Z³` (rejected
  by A2 — would change the framework), **or**
- (B) demanding emergent-Lorentz **at the bare lattice level** (rejected:
  emergent Lorentz is a *continuum-limit* statement; bare-lattice Lorentz
  invariance is impossible on any cubic lattice), **or**
- (C) admitting a primitive that pins the renormalized speed of light to 1
  at every value of `g²` (= one-loop tuning curve), which is itself the
  Karsch-Klassen calibration program — well-defined as engineering, but not
  primitives-derived.

None of these is currently a retained framework derivation, and none is a
plausible target without expanding the axiom set.

---

## 4. The bounded component — Wilson-replacement at finite `ξ`

C-iso.ii (Wilson-replace) is a **bounded selection** within the
continuum-equivalence class.

The framework's derived form is **heat-kernel temporal**: `[-ln K_{s_t}(W)]`.

The standard lattice-MC comparator uses **Wilson temporal**: `(N_c/s_t)·[1 - (1/N_c) Re Tr_F W]`.

The two differ at `O(s_t) = O(g²/(2ξ))`. At `ξ = 1, g² = 1` the difference
is `s_t = 0.5`, giving the verified ~7-9% systematic error in the
temporal-plaquette weight (Theorem T-AT.3 numerical verification).

**Crucial observation:** both Wilson-temporal and heat-kernel-temporal
produce the **same continuum action** `Tr(F²)` at leading order. By Theorem
A2.5 ([`A2_5_DERIVED_THEOREM.md`](../A2_5_DERIVED_THEOREM.md)), they are
*both* admissible representatives of the continuum-equivalence class. Their
difference at finite β is **Symanzik-irrelevant** (vanishes as
`a → 0`).

Therefore C-iso.ii is **not a separate admission** beyond the
already-existing **continuum-equivalence-class parsimony** ([`A2_5_DERIVED_THEOREM.md`](../A2_5_DERIVED_THEOREM.md)).
The 7-9% error at `s_t = 0.5` is just the magnitude of the parsimony band at
canonical operating point.

**Net for C-iso.ii:** absorbed into the existing continuum-equivalence-class
parsimony bound. Not a separately-named admission.

This is a **strict improvement** in the bridge characterization: previously
C-iso.ii was listed as a separate finite-`s_t` admission; here we show it is
*not* separate — it is part of the same parsimony freedom that A2.5 already
accounts for.

---

## 5. What this note achieves vs the prior "C-iso bounded `O(g²) ≈ 5-15%`"

### Before (per [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](../UNIFIED_BRIDGE_STATUS_2026_05_07.md))

```yaml
admitted_context_inputs:
  - N_F = 1/2 canonical Gell-Mann trace normalization
  - Convention C-iso (one opaque convention; bounded O(g²)~5-15%)
  - Continuum-equivalence-class parsimony (~5-10% across {Wilson, HK, Manton})
```

### After (this note)

```yaml
admitted_context_inputs:
  - N_F = 1/2 canonical Gell-Mann trace normalization        (L3 of g_bare chain)
  - Convention C-iso.i: time-discretization a_tau = a_s      (L3a of C-iso chain; this note)
  - Continuum-equivalence-class parsimony, which now subsumes
    BOTH the Wilson/HK/Manton continuum-action selection AND
    the C-iso.ii Wilson-replace temporal selection            (~5-15% bounded)
```

The headline change: C-iso is **not a new admission beyond what's already
named**. It decomposes as:

- **`C-iso.i` (genuine admission)**: parallel to `N_F = 1/2`. One scalar
  admission per chain. Both have audit-defensible structural-obstruction
  notes. Both could in principle be promoted by a higher principle, but
  neither is currently derivable.

- **`C-iso.ii` (now absorbed into parsimony)**: not separate.

**Total admission count for the bridge:**

```
2 admitted scalars (N_F = 1/2 in g_bare; a_tau = a_s in C-iso)
+ continuum-equivalence-class parsimony (one bounded equivalence-class choice)
```

**No hidden admissions remain.**

---

## 6. The audit-defensible four-layer stratification (formal statement)

> **Theorem (C-iso four-layer stratification, candidate).** Under the
> framework's retained primitive stack (A1 + A2 + canonical Tr-form + RP +
> locality + single-clock + Theorem A2.5 + Theorem T-AT), the dictionary
> from `(S_AT)` to standard 4D isotropic Wilson at `β = 6` decomposes into
> exactly four layers:
>
> | Layer | Statement | Status |
> |---|---|---|
> | L1 | A1 + A2 (Cl(3) + Z³) | DERIVED (axiom) |
> | L2 | RP transfer matrix + Stone's theorem give unique `H` and `T(a_τ) = exp(-a_τ H)` for any `a_τ > 0` | DERIVED |
> | L3a | The temporal step `a_τ` (= anisotropy `ξ = a_s/a_τ`) | **CONVENTION** (admitted; choice = `1`) |
> | L3b | Lattice-form selection of the temporal plaquette weight | PARSIMONY-WITHIN-EQUIVALENCE-CLASS (bounded `O(g²)`; absorbed into continuum-action parsimony of A2.5) |
> | L4 | Standard 4D Wilson at `β = 2N_c/g_KS² = 6` | DERIVED-from-L3 |
>
> Equivalently:
>
> **(D1) Anisotropic Trotter is forced** by L1+L2 (Theorem T-AT). The
> *form* of the dictionary is uniquely determined.
>
> **(D2) The numerical value of `ξ = 1`** is the L3a admission. There is
> no axiom-derived value of `ξ`. The choice `ξ = 1` is a downstream choice
> of "compare to standard 4D isotropic Wilson MC at `β = 6`", not a
> derivation.
>
> **(D3) The Wilson-temporal vs heat-kernel-temporal selection** is L3b
> parsimony, bounded by the continuum-equivalence-class width
> (Theorem A2.5).
>
> **(D4) The reduction `g_KS² = 1 ↔ β_W = 6` at leading order** is L4 — a
> derived constraint once L3a is admitted, with explicit one-loop
> anisotropy-radiative correction (Karsch 1982; Klassen 1998).
>
> Therefore the framework has **exactly one genuinely admitted convention
> in the C-iso chain** — the choice `a_τ = a_s` of the temporal step at
> the spatial scale.

**Hostile-review check.** The stratification pinpoints "what is admitted"
to a single scalar. The remaining derivations (L1, L2, L4) are theorem-grade
or trivial-algebra. The L3b component is rigorously bounded by an existing
continuum-action-form parsimony note (A2.5).

This is the *cleanest* audit-defensible characterization of C-iso the
framework can produce without expanding A1/A2.

---

## 7. Six attack vectors — summary

Per-attack-vector details are in [`ATTACK_RESULTS.md`](ATTACK_RESULTS.md).
Summary table:

| Attack | Hypothesis | Result | Net delta |
|---|---|---|---|
| **A1. LR velocity sets `a_τ = a_s`** | `v_LR = 1` in canonical units forces `a_τ = a_s/v_LR = a_s` | **NEGATIVE**: `v_LR = 2 e r J` is `g²`-dependent; numerically `v_LR ≈ 5.4` at canonical, not 1 | rules out attack 1; obstruction confirmed |
| **A2. Single-clock causality forces `a_τ = a_s`** | The single-clock structure pins both form and step | **NEGATIVE**: single-clock pins form (one-parameter unitary group), not step | rules out attack 2; obstruction confirmed |
| **A3. Continuum-limit consistency forces `ξ = 1`** | The unique continuum-limit Lorentz/rotation structure forces the lattice anisotropy `ξ_bare = 1` | **PARTIALLY POSITIVE**: it forces the *renormalized* `ξ → 1` at fixed point of the Karsch-Klassen RG, but bare `ξ` may differ at one-loop. Continuum content is in continuum-action-form parsimony (A2.5), not separate primitive | reframes; not a new derivation |
| **A4. Heat-kernel temporal is the framework's prediction** | The right comparator is *anisotropic* lattice MC (heat-kernel temporal). Wilson-temporal is a reinterpretation | **POSITIVE for honest scope**: this is the correct framing of T-AT. The "Wilson-replace" step is an L3b parsimony, not a derivation. Already documented in T-AT.3 | reframes C-iso.ii to L3b parsimony |
| **A5. Action-form continuum equivalence sharpening** | Symanzik-irrelevance of HK-vs-Wilson temporal at leading order in `a²` | **POSITIVE**: subsumes C-iso.ii into A2.5 parsimony bound; explicit `O(g²)` quantitative bound retained | C-iso.ii absorbed into existing parsimony |
| **A6. Reflection positivity in mixed-action lattice** | RP forces a unique temporal-action choice | **NEGATIVE**: both Wilson-temporal and heat-kernel-temporal satisfy RP (heat-kernel inherits RP from `H_KS` via Trotter; Wilson-temporal is OS-RP separately verified). Both choices are RP-compatible | rules out attack 6 as a uniqueness mechanism |

**Net:** four of six attack vectors confirm the obstruction (A1, A2, A6 negative; A3 reframes), and two improve the characterization (A4, A5 absorb C-iso.ii into existing A2.5 parsimony bound).

---

## 8. Conclusion — outcome class

**This is outcome class (c)** per the deliverable specification:

> Documents why C-iso is genuinely admitted, with each attack vector explained.

with the additional **bounded result** that:

> The C-iso admission decomposes into:
> - one **genuinely admitted scalar** (`a_τ = a_s`, parallel to `N_F = 1/2`)
> - one **parsimony-within-equivalence-class** selection (Wilson-temporal vs
>   heat-kernel-temporal, absorbed into A2.5 continuum-action-form parsimony).

After this note, the bridge admission count is:

```
2 admitted scalars (N_F = 1/2; a_tau = a_s)
+ 1 continuum-equivalence-class parsimony (subsuming both action-form and Wilson-temporal/HK-temporal)
```

This is **strictly cleaner** than the prior "Convention C-iso O(g²)~5-15%"
opaque admission: the genuinely admitted part is now one scalar with an
explicit structural-obstruction note (this document), and the remainder is
covered by the existing A2.5 parsimony framework.

The four bridge-dependent lanes
([α_s direct Wilson loop](../LANE_PROMOTION_ALPHA_S_DIRECT_WILSON_LOOP.md);
[Higgs mass from axiom](../LANE_PROMOTION_HIGGS_MASS_FROM_AXIOM.md);
[Gauge-scalar bridge](../LANE_PROMOTION_GAUGE_SCALAR_BRIDGE.md);
[Koide-Brannen phase](../LANE_PROMOTION_KOIDE_BRANNEN_PHASE.md)) can promote
to `bounded_theorem` / `retained_bounded` immediately, with the cleaner
admission set above.

---

## 9. Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem (with clean obstruction note for genuine admission)
claim_scope: |
  Convention C-iso (a_tau = a_s + Wilson-replace) decomposes into:
  - L3a admission: a_tau = a_s (genuine convention; structural obstruction from
    Z^3 axiom-only spatial substrate, time emergent via RP).
  - L3b parsimony: Wilson-temporal vs heat-kernel-temporal (absorbed into the
    continuum-action-form parsimony band of A2.5; bounded O(g^2) ~ 7-9% at
    canonical s_t = 0.5).
  Net: one scalar admission a_tau = a_s, parallel to N_F = 1/2 in the g_bare
  chain, with all-other components derived or absorbed into existing parsimony.
proposed_load_bearing_step_class: A (algebra; obstruction is structural, not technical)
audit_required_before_effective_retained: true
admitted_context_inputs: |
  - A_min (A1 + A2 + retained Tr-form + RP + locality + single-clock).
  - Theorem A2.5 (continuum-level Wilson-form) for L3b parsimony absorption.
  - Theorem T-AT (anisotropic Trotter dictionary) as the starting point.
proof_load_bearing_steps: |
  1. Stone's theorem on retained H_phys gives T(a_tau) = exp(-a_tau H) for any a_tau > 0
     (class A).
  2. v_LR = 2 e r J is g^2-dependent; no canonical v_LR = 1 emerges; thus
     a_tau = a_s/v_LR != a_s in primitives-only units (class A).
  3. Single-clock theorem (S1) pins form (one-parameter unitary group), not step.
     Direct consequence of Stone's theorem on finite-dim H_phys (class A).
  4. Wilson-temporal vs heat-kernel-temporal: both RP-compatible, both lie in
     A2.5 continuum-equivalence class; difference is O(g^2) at canonical s_t.
     Subsumes C-iso.ii into existing A2.5 parsimony (class A).
companion_obstruction_note: this note (THEOREM_NOTE.md)
companion_attack_log: ATTACK_RESULTS.md
```

---

## 10. Cross-references

- **Parent dictionary derivations**:
  - [`DICTIONARY_DERIVATION_RESULTS.md`](../DICTIONARY_DERIVATION_RESULTS.md) — main analytical note
  - [`DICTIONARY_DERIVED_THEOREM.md`](../DICTIONARY_DERIVED_THEOREM.md) — Theorem T-AT
- **Parallel `g_bare` stratification**:
  - [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md) — four-layer stratification template
  - [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](../../../docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) — joint trace-AND-Casimir rigidity (analogue of "what's derived in C-iso")
- **Continuum-action parsimony (Wilson/HK/Manton equivalence class)**:
  - [`A2_5_DERIVED_THEOREM.md`](../A2_5_DERIVED_THEOREM.md) — continuum-level uniqueness of the dim-4 magnetic operator
  - [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md) — finite-β no-go on action-form uniqueness
- **Time-emergence chain**:
  - [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
  - [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
  - [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
- **Emergent-Lorentz**:
  - [`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](../../../docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md) — bounded-conditional theorem
  - [`LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md`](../../../docs/LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md)
- **Standard physics references** (cited as inputs to bounded result, not framework axioms):
  - Karsch F. (1982), *Nucl. Phys.* B205, 285 — anisotropic Wilson action; one-loop coupling matching.
  - Klassen T. (1998), *Nucl. Phys.* B533, 557 — SU(N) one-loop anisotropy coefficients.
  - Hasenfratz A., Hasenfratz P. (1981), *Nucl. Phys.* B193, 210 — anisotropic lattice expansion.
  - Engels J., Karsch F., Satz H. (1982), *Phys. Lett.* B113, 398 — KS Hamilton limit.
  - Suzuki M. (1976), *Comm. Math. Phys.* 51, 183 — Trotter expansion.
  - Kogut J., Susskind L. (1975), *Phys. Rev.* D11, 395 — Hamiltonian formulation.
  - Smit J. (2002), *Introduction to Lattice Gauge Theory*, Cambridge §4.4.

---

## 11. What this note does NOT close

- **`a_τ = a_s` derivation from a higher principle.** Open foundational
  question. Possible future paths: (i) emergent-Lorentz at the lattice level
  (rejected: impossible on cubic lattice); (ii) higher-principle
  Z⁴-substrate (rejected: violates A2); (iii) Karsch-Klassen one-loop
  calibration giving renormalized `ξ = 1` at all `g²` (engineering, not
  primitives); (iv) holographic / categorical principle (no such retained
  framework derivation currently).
- **One-loop anisotropy radiative correction values for SU(3) at canonical
  `g² = 1`.** Engineering calculation (Karsch coefficients), not yet
  performed for the framework's specific heat-kernel-temporal action.
- **The lattice-action form selection in the absence of A2.5.** A2.5 is
  itself a candidate theorem (continuum-level derived; finite-β residual).
  If A2.5 is not retained, the L3b parsimony argument relies on its own
  audit-pending status.

---

## 12. Bottom line

C-iso does **not** collapse to a fully-derived theorem under the six attack
vectors investigated. The structural obstruction is the framework's
**emergent-time** structure: with A1+A2 fixing only spatial structure, the
temporal lattice spacing `a_τ` is a parameter of the discretization, not a
quantity forced by primitives.

However, the analysis **strengthens** the bridge characterization in three
ways:

1. **Decomposes C-iso into one scalar admission (`a_τ = a_s`) plus one
   parsimony selection (Wilson-temporal vs HK-temporal).**
2. **Absorbs the parsimony selection into the existing A2.5
   continuum-equivalence-class parsimony framework**, removing it as a
   separately-named admission.
3. **Promotes the `a_τ = a_s` admission to L3a status with an explicit
   structural-obstruction note** (this document), parallel to the
   `N_F = 1/2` admission at L3 in the `g_bare` chain.

After this note, the bridge has **exactly two genuinely admitted scalars**
(`N_F = 1/2`, `a_τ = a_s`) plus **one continuum-equivalence-class
parsimony bound** (which is itself a derived theorem at the continuum
level, A2.5). The four bridge-dependent lanes can promote to
`bounded_theorem` / `retained_bounded` with this cleaner admission set.

This is a **substantial advance over the prior "opaque Convention
C-iso"** characterization, even though the negative result on C-iso.i is
genuine.
