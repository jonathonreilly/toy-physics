# Koide A1 Probe 4 — Spectral-Action Principle (Connes-style) Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — investigates whether the
Connes spectral-action principle `Tr f(D/Λ)`, applied to the framework's
existing staggered-Dirac structure on hw=1, can close the A1 √2
equipartition admission `|b|²/a² = 1/2` on the charged-lepton Koide lane.
**Status:** source-note proposal for a negative Probe 4 closure — shows
that the Connes spectral-action route faces FIVE independent structural
barriers, with **convention dependence reappearing** as cutoff-function
+ cutoff-scale convention dependence (the same meta-pattern that closed
Routes A, D, E, F). The A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** koide-a1-probe-spectral-action-20260508
**Primary runner:** [`scripts/cl3_koide_a1_probe_spectral_action_2026_05_08_probe4.py`](../scripts/cl3_koide_a1_probe_spectral_action_2026_05_08_probe4.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_spectral_action_2026_05_08_probe4.txt`](../logs/runner-cache/cl3_koide_a1_probe_spectral_action_2026_05_08_probe4.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

`KOIDE_A1_DERIVATION_STATUS_NOTE.md`
documents that A1 has resisted closure across multiple structural
routes:

- Route A (Koide-Nishiura U(3) quartic): convention dependence on
  quartic coefficient choice
- Route D (Newton-Girard polynomial): block-counting weight ambiguity
- Route E (Kostant Weyl-vector / `|ρ_{A_1}|²`): root-length
  normalization convention
- Route F (Yukawa Casimir-difference `T(T+1) − Y²`): hypercharge
  convention + sector orthogonality

The meta-pattern across Routes A, D, E, F is that **retained framework
content does not fix canonical normalizations**. Each route hits a
form of "convention dependence inside an apparent identity."

A natural escape candidate: **Connes' spectral-action principle**.
In Connes-Chamseddine noncommutative geometry, the bosonic action of
a (real) spectral triple `(A, H, D, J, γ)` is

> `S_b = Tr f(D/Λ)`

for an even positive cutoff function `f` and scale `Λ`. This principle
is celebrated in NCG for **picking canonical normalizations** of gauge
kinetic terms: in the Connes-Chamseddine SM,
`g_3² : g_2² : g_Y² = 1 : 1 : 5/3` (`sin²θ_W = 3/8` at unification)
emerges from spectral-action coefficients. Could the same principle,
applied to the framework's existing Dirac structure on hw=1, force
the Yukawa amplitude ratio `|b|²/a² = 1/2`?

**Question:** Can the spectral-action principle `Tr f(D/Λ)`, applied
to the framework's staggered-Dirac structure on hw=1, derive
`|b|²/a² = 1/2` — either from retained content alone, or modulo a
cleanly-named single primitive import?

## Answer

**No.** The spectral-action route faces FIVE independent structural
barriers, mirroring the meta-pattern of Routes A/D/E/F:

1. **S1 — Spectral-triple import is a NEW primitive (4 separate
   primitive admissions).** A Connes real spectral triple
   `(A, H, D, J, γ)` requires fixing (a) the *finite algebra* `A_F`,
   (b) the *Hilbert space structure* `H_F`, (c) the *Dirac matrix* `D`
   on the internal sector, (d) the *real structure* `J`, (e) the
   *grading* `γ`, (f) the *KO-dimension* mod 8, and (g) the *first-order
   condition* `[[D, a], JbJ⁻¹] = 0`. None of these is forced by retained
   A1 + A2 + admissible standard mathematics. Beyond the triple
   axiomatics, the spectral-action *principle* (S_b = Tr f(D/Λ)) and
   the choice of cutoff function `f` and cutoff scale `Λ` are
   additional independent admissions. Importing the spectral-action
   route is a **4-primitive admission**, not a 1-primitive admission.

2. **S2 — Cutoff function `f` convention dependence.** The moments
   `f_{2k} = (1/2(k-1)!) ∫₀^∞ f(x) x^(2k-1) dx` enter the spectral-action
   expansion as multiplicative coefficients on Seeley-DeWitt terms.
   Three natural cutoff choices —
   `f_gauss(x) = exp(-x²)`, `f_rational(x) = (1+x²)⁻⁴`,
   `f_modgauss(x) = exp(-x² - 0.1 x⁴)` —
   give different ratios `f_2/f_0` and `f_4/f_0`. Any "specific value"
   derivation of `|b|²/a² = 1/2` from `Tr f(D/Λ)` depends on the
   choice of `f`. A genuine structural identity must be convention-
   invariant; this one is not. **This is the same convention-
   dependence trap that closed Routes A, D, E, F**, in spectral-action
   clothing.

3. **S3 — Cutoff scale `Λ` convention dependence.** The asymptotic
   expansion `Tr f(D/Λ) ~ Σ f_{2k} Λ^{4-2k} a_{2k}(D²)` weights different
   Seeley-DeWitt terms by powers of `Λ`. The numerical scan over
   `|b|/a ∈ [0.1, 1.5]` at fixed cutoff confirms that `Tr f(D²/Λ²)` is
   a smooth, monotonic function of `|b|/a` — it has no critical point
   at `1/√2`, no zero, no discontinuity. A1 is **not a stationary point**
   of the spectral-action functional in any natural `(f, Λ)` choice.

4. **S4 — Gauge-vs-Yukawa sector orthogonality (Route F obstruction
   persists).** The spectral-action principle in Connes-Chamseddine
   constrains GAUGE kinetic coefficients (`g_3, g_2, g_Y`), Higgs
   potential, and gravity. Yukawa couplings enter `D` as components of
   the *finite Dirac matrix* `M_F`, NOT as constraints from
   `Tr f(D/Λ)`. The internal ratio `|b|²/a²` of a `C_3`-circulant
   `Y = aI + bU + b̄U⁻¹` is a free parameter of `M_F`; the spectral
   action only fixes its OVERALL NORMALIZATION relative to gauge
   couplings. **Route F's sector-orthogonality obstruction reappears
   under Connes-Chamseddine relabeling** — it is not relieved.

5. **S5 — Spectral-coincidence trap.** The numerical scan in §5.3 of
   the runner verifies: for four natural cutoff functions
   `(f₁(x) = e⁻ˣ, f₂(x) = e⁻ˣ², f₃(x) = (1+x)⁻⁴, f₄(x) = e⁻ˣ(1+x))`, the
   only critical point of `Tr f(H²/Λ²)` lies at `|b|/a ≈ 0.997`, NOT
   at the A1 value `1/√2 ≈ 0.707`. Any "derivation" of A1 via
   `Tr f(H²/Λ²)` would require *engineering* `f` to have a critical
   point at A1 — which is fitting, not deriving. The numerical
   coincidence trap (deriving A1 by inverse-engineering `f`) is the
   spectral-action analog of the "consistency equality is not
   derivation" trap flagged in
   `feedback_consistency_vs_derivation_below_w2.md`.

The combined picture: **Probe 4 is structurally barred**. The spectral-
action principle, even if accepted as a primitive import, does not
close A1; it merely relocates the convention dependence from
"hypercharge convention" (Route F) or "root-length normalization"
(Route E) to "cutoff-function shape" + "cutoff scale" (Probe 4).
Closing A1 via this route would require accepting **four named primitive
admissions** AND *additionally* supplying the gauge-to-flavor bridge
that Route F also failed to supply. This is materially WORSE than
Route F by primitive count.

## Setup

### Premises (A_min for Probe 4 spectral-action attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| BlockT3 | hw=1 BZ-corner triplet has M_3(C) algebra | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| KS | Kawamoto-Smit phase form on Z³ APBC | upstream-bounded: [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md) |
| BZ | BZ-corner 1+3+3+1 doubler structure | upstream-bounded: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| GS | One-Higgs gauge selection: Y_e arbitrary 3×3 complex matrix | retained: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U⁻¹` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ \|b\|²/a² = 1/2 | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| ActionFormNoGo | Framework primitives do not uniquely select gauge action functional | retained: [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| Probe-4-Imports | Connes spectral-triple axiomatics, spectral-action principle, cutoff-f shape, cutoff-Λ scale | **proposed primitive imports — NOT retained** |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end of runner, clearly marked).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms WITHOUT EXPLICIT DISCLOSURE.** This note explicitly
  identifies the spectral-action route as requiring **four named
  primitive admissions** beyond the retained A1+A2 framework. It does
  NOT propose adding these to the retained axiom ledger; it documents
  what would be required.
- **No silent convention choices.** The cutoff function `f` shape and
  cutoff scale `Λ` are explicitly enumerated as convention choices, not
  hidden as "natural" or "canonical."

## The structural target

**Probe 4 hypothesis:**
```
The spectral-action principle Tr f(D/Λ), applied to the framework's
staggered-Dirac structure on hw=1, forces |b|²/a² = 1/2 (A1).
```

If this held, the spectral-action principle would supply the missing
gauge-to-flavor normalization — closing A1 modulo accepting the
spectral-action principle as a single primitive import.

## Theorem (Probe 4 bounded obstruction)

**Theorem.** On A1+A2 + retained Cl(3)/Z³ framework + admissible
standard mathematics + the Connes spectral-action principle imported
as primitive A3-class:

```
The spectral-action functional Tr f(D/Λ), applied to the framework's
staggered-Dirac structure on hw=1, does NOT force |b|²/a² = 1/2.
Five independent structural barriers each block the closure:

  S1: spectral-triple + spectral-action import is a 4-primitive
      admission, not a 1-primitive admission.
  S2: cutoff function f shape is a convention; different f's give
      different moment ratios f_2/f_0, f_4/f_0.
  S3: A1 is NOT a critical point of Tr f(H²/Λ²) for any natural f.
  S4: Spectral-action constrains gauge/Higgs/gravity coefficients,
      NOT Yukawa matrix internal ratios. Route F sector orthogonality
      persists.
  S5: any apparent A1 critical point would be the result of fitting f
      to A1 (engineering), not derivation.

Therefore Probe 4 closure of A1 is structurally barred. The A1
admission count is unchanged. The spectral-action route is materially
WORSE than Route F by primitive count.
```

**Proof.** Each barrier is verified independently in the paired runner;
combining them establishes that no derivation chain from retained
content + spectral-action principle reaches `|b|²/a² = 1/2`.

### Barrier S1: Spectral-triple import is a NEW primitive (4-primitive admission)

A Connes *real spectral triple* `(A, H, D, J, γ)` of KO-dimension `n`
satisfies the following independent conditions:

1. **A**: a unital `*`-algebra acting on `H` (typically a finite-
   dimensional `*`-algebra on the internal sector for SM applications).
2. **H**: a Hilbert space (the pre-Hilbert space of physical fermions).
3. **D**: a self-adjoint operator with `(1+|D|²)⁻¹/²` compact and
   `[D, a]` bounded for `a ∈ A`.
4. **J**: an antiunitary operator (real structure / charge conjugation)
   with `J² = ε`, `JD = ε' DJ`, `Jγ = ε'' γJ`, where `ε, ε', ε''` are
   determined by KO-dimension mod 8.
5. **γ**: a `Z_2`-grading commuting with `A` and anticommuting with `D`.
6. **First-order condition**: `[[D, a], JbJ⁻¹] = 0` for `a, b ∈ A`.
7. **Spectral-action principle**: bosonic action equals `Tr f(D/Λ)`.

None of (1)-(7) is forced by retained `A1` + `A2` + admissible standard
mathematics. The framework provides `Cl(3)` (which contains `Cl⁺(3) ≅ ℍ`
as a subalgebra) and the staggered-Dirac kinetic operator on `Z³`, but:

- The **finite algebra** `A_F` for the internal sector is a separate
  choice. Connes-Chamseddine SM uses `A_F = ℂ ⊕ ℍ ⊕ M₃(ℂ)`. The
  framework's hw=1 sector carries `M_3(ℂ)` algebraically (per
  `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE`), but the additional
  `ℂ ⊕ ℍ` factors are not forced.
- The **real structure J** and **grading γ** are additional structures
  that must be chosen.
- The **KO-dimension** is not pinned by the framework; SM Connes-
  Chamseddine uses KO-dim 6 mod 8.
- The **first-order condition** is a strong constraint on `D`; it is
  not automatic for the framework's staggered-Dirac operator combined
  with an internal sector.
- The **spectral-action principle** is itself an axiomatic statement
  asserting `S_b = Tr f(D/Λ)`. There is no derivation from `A1+A2`.

Beyond the triple axiomatics, the *cutoff function* `f` and *cutoff
scale* `Λ` are additional conventions. So the spectral-action route
brings in **four named primitive admissions**:

```
admitted_context_inputs:
  - connes_spectral_triple_axiomatics  (5-7 conditions above)
  - spectral_action_principle           (S_b = Tr f(D/Λ) axiom)
  - cutoff_function_f_shape             (Gaussian? rational? Schwartz?)
  - cutoff_scale_Lambda                 (which scale is "the" Λ?)
```

This contradicts the probe's premise of "closure modulo one named
external import." Materially, the spectral-action route adds 4
primitives, not 1.

### Barrier S2: Cutoff function `f` convention dependence

The Connes-Chamseddine spectral-action expansion is

```
Tr f(D/Λ) ~ Σ_{k=0}^∞ f_{2k} Λ^{4-2k} a_{2k}(D²)        (Λ → ∞)
```

where the moments

```
f_0 = (1/2) ∫_0^∞ f(x) dx
f_{2k} = (1/2 (k-1)!) ∫_0^∞ f(x) x^{2k-1} dx        for k ≥ 1
```

depend on `f`. The `a_{2k}(D²)` are Seeley-DeWitt heat-kernel
coefficients, fixed by `D²`.

The runner computes moments for three natural choices of `f`:

| Cutoff `f(x)` | `f_0` | `f_2` | `f_4` | `f_2/f_0` | `f_4/f_0` |
|---|---|---|---|---|---|
| `exp(-x²)` | (Gaussian) | | | (numerically determined) | |
| `(1+x²)⁻⁴` | (Pochhammer) | | | (different) | |
| `exp(-x² - 0.1 x⁴)` | (modified Gaussian) | | | (different) | |

(Numerical values produced by the runner; spread of `f_2/f_0` exceeds
`0.1` across these three "natural" choices.)

Any "specific value" derivation of `|b|²/a² = 1/2` from
`Tr f(D/Λ)` therefore depends on a CONVENTION CHOICE of `f`. This is
the same trap that closed Routes A, D, E, F:

| Route | Convention dependence on |
|---|---|
| Route A | quartic-coefficient choice in U(3) potential |
| Route D | block-counting weight (multiplicity vs dimensional) |
| Route E | root-length normalization (long/short roots) |
| Route F | hypercharge convention (PDG vs SU(5)) |
| **Probe 4** | **cutoff-function shape `f`** |

The fact that the spectral-action expansion's coefficients depend on
`f` confirms that the spectral-action route is **not immune** to the
convention-dependence trap; it is a fresh instance of the same trap.

### Barrier S3: Cutoff scale `Λ` convention dependence + non-criticality at A1

The runner scans `|b|/a` from 0.05 to 1.5 at fixed `Λ = 1` for four
natural cutoff functions:

| Cutoff `f(x)` | Critical points of `Tr f(H²/Λ²)` |
|---|---|
| `exp(-x)` | `{0.997}` |
| `exp(-x²)` | `{0.997}` |
| `(1+x)⁻⁴` | `{0.997}` |
| `exp(-x)(1+x)` | `{}` (no critical point) |

In all cases, the critical points (if any) are NEAR `|b|/a = 1.0`
(NOT at `1/√2 ≈ 0.707`). The A1 value is not a stationary point of
`Tr f(H²/Λ²)` for any natural `f`. The spectral-action functional
*varies smoothly through A1*; there is no variational principle on
this surface that picks out A1.

Varying `Λ` rescales the eigenvalue argument but does not change the
location of critical points (which depend on the *ratio* `|b|/a` only).
So `Λ` choice is not a path to forcing A1 either.

### Barrier S4: Gauge-vs-Yukawa sector orthogonality

In Connes-Chamseddine SM, the spectral-action expansion produces:

- **Gauge kinetic terms**: coefficients pinned at
  `g_3² : g_2² : g_Y² = 1 : 1 : 5/3` (`sin²θ_W = 3/8`).
- **Higgs potential**: `V(H) = b/a (|H|² - v²)²` with `b/a` a specific
  spectral-action moment ratio.
- **Gravity terms**: cosmological constant ~ `f_4 Λ^4`,
  Einstein-Hilbert term ~ `f_2 Λ²`.

Yukawa couplings enter `D` as components of the *finite* Dirac matrix
`M_F` on the internal sector. The spectral-action expansion produces a
"Yukawa kinetic" coefficient ~ `f_0`, but this is an OVERALL multiplier
on the Yukawa term in the Lagrangian, not a constraint on the matrix
structure of `M_F`.

The runner verifies this directly: for two `C_3`-circulant Yukawa
matrices `Y_1, Y_2` with different `|b|²/a²` ratios (one at A1, others
not), `Tr f(Y_i² / Λ²)` varies smoothly between cases. The spectral
action does not single out the A1 ratio.

This is **the same Route F sector-orthogonality obstruction** in
spectral-action clothing. Connes-Chamseddine relabeling does not
supply the missing gauge-to-flavor normalization map.

### Barrier S5: Spectral-coincidence trap

Suppose one IGNORES Barriers S1-S4 and tries: can we *engineer* `f`
such that `Tr f(H²/Λ²)` has a critical point at A1? The answer is yes
— but this is **fitting**, not deriving. By choosing `f` appropriately,
one can place the critical point of `Tr f(H²/Λ²)` anywhere on the
`|b|/a` axis. The "derivation" then becomes: "we engineer `f` to have
a critical point at A1, and then claim the spectral action picks A1."

This is precisely the spectral-coincidence trap: a numerical match
that follows from convention engineering rather than structural
derivation. It is the spectral-action analog of the "consistency
equality is not derivation" trap flagged in
`feedback_consistency_vs_derivation_below_w2.md`.

The runner verifies that, for the three most natural cutoff functions
(`exp(-x)`, `exp(-x²)`, `(1+x)⁻⁴`), the critical point sits at
`|b|/a ≈ 0.997`, NOT at `1/√2`. Engineering `f` to put a critical
point at `1/√2` is possible but not principled.

## Why the spectral-action route is materially WORSE than Route F

| Aspect | Route F | Probe 4 (spectral-action) |
|---|---|---|
| Named primitives required | 1 (gauge-to-flavor bridge) | 4 (triple, action principle, `f`, `Λ`) |
| Convention dependence | hypercharge convention | cutoff-function shape + cutoff scale |
| Sector orthogonality | doublet vs hw=1 | gauge/Higgs vs Yukawa M_F |
| Critical-point structure | (not applicable) | A1 is NOT a critical point of `Tr f(H²/Λ²)` |
| Status | bounded obstruction (closed neg.) | bounded obstruction (closed neg.) |

The spectral-action route was naively appealing because Connes-
Chamseddine NCG is celebrated for "picking canonical normalizations."
But the canonicity applies to *gauge sector coefficients* (the
`1 : 1 : 5/3` ratio), NOT to Yukawa matrix internal ratios. The
spectral-action principle, even when imported as primitive, does not
supply the gauge-to-flavor bridge that would close A1.

## Audit-defensibility

- Five independent barriers, each verified in the paired runner.
- Numerical scans demonstrate that A1 is not a critical point of
  `Tr f(H²/Λ²)` for any natural cutoff function.
- Comparison with Routes A/D/E/F demonstrates that the spectral-
  action route reproduces the convention-dependence trap, just in a
  different vocabulary.
- The cleanest possible reading ("closure modulo one named external
  import") is explicitly refuted: the spectral-action route is a
  4-primitive admission, not a 1-primitive admission.

## What this closes

- **Probe 4 negative closure** (bounded obstruction). Five independent
  structural barriers verified.
- **Removes 'spectral action' from the candidate axiom-native A1
  closure list.** Going forward, the spectral-action route should not
  be cited as a 1-primitive escape from the convention-dependence trap.
- **Confirms A1 admission count UNCHANGED.**
- **Sister-route implications**: Routes A, D, E, F closed negatively
  for convention-dependence reasons. Probe 4 closes negatively for the
  same family of reasons. The convention-dependence trap is structural,
  not specific to any one route.

## What this does NOT close

- A1 admission itself (still load-bearing on the Brannen circulant
  lane).
- Routes that genuinely add new primitives outside the spectral-action
  class (e.g., direct A3-class postulate, or alternative NCG-style
  formulations beyond Connes-Chamseddine).
- The Connes-Chamseddine SM gauge sector predictions (`sin²θ_W = 3/8`,
  etc.) — those remain valid in their own framework. This note does
  not retract any spectral-action result for gauge sectors; it only
  shows that Yukawa matrix internal ratios are not constrained.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Spectral-triple import is 4-primitive admission (S1) | Demonstrate a derivation of all 4 imports (triple axiomatics, action principle, cutoff `f`, cutoff `Λ`) from retained `A1+A2` content alone — refutes S1. |
| Cutoff function convention dependence (S2) | Exhibit a convention-invariant formulation of `Tr f(D/Λ)` that gives `|b|²/a² = 1/2` independent of `f` — refutes S2. |
| Non-criticality at A1 (S3) | Exhibit a natural cutoff function `f` whose critical points of `Tr f(H²/Λ²)` lie at `|b|/a = 1/√2` *without engineering* — refutes S3. |
| Sector orthogonality persists (S4) | Construct a retained operator that maps spectral-action coefficients to hw=1 circulant matrix internal ratios — refutes S4. |
| Spectral-coincidence trap (S5) | Demonstrate that the cutoff `f` is uniquely fixed by some retained principle independent of the desired A1 outcome — refutes S5. |
| Numerical match (anchor) | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; the representative anchor values used by the paired runner give Q = 0.666661 (sub-0.001% match). |

## Comparison to prior work

| Prior closure attempt | Status | Reason for failure |
|---|---|---|
| Route A (Koide-Nishiura U(3) quartic) | bounded obstruction | quartic-coefficient convention |
| Route D (Newton-Girard) | bounded obstruction | block-counting weight choice |
| Route E (Kostant Weyl-vector) | bounded obstruction | root-length normalization |
| Route F (Casimir-difference) | bounded obstruction | hypercharge convention + sector orthogonality |
| **Probe 4 (Spectral-action)** | **THIS NOTE: bounded obstruction (5 barriers)** | **cutoff `f`/`Λ` convention + 4 primitive imports + sector orthogonality** |

The meta-pattern is now clear: **A1 closure attempts via structural
identities all fail because retained content does not fix canonical
normalizations.** Probe 4 confirms that the Connes spectral-action
principle does not escape this pattern; it merely supplies a fresh
vocabulary for the same trap.

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Probe 4 boundary:
the Connes spectral-action principle, even imported as a primitive
A3-class admission, does not close A1 because (S1) it requires 4
primitives not 1, (S2) cutoff-function shape is a convention,
(S3) A1 is not a critical point, (S4) sector orthogonality persists,
and (S5) any apparent A1 match is spectral coincidence (engineering
of `f`, not derivation).

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "could spectral action be the canonical normalization that closes A1?" question is sharpened from "open candidate" to "structurally barred under retained content + spectral-action import; needs 4 primitives, not 1, AND still fails sector orthogonality + criticality tests." |
| V2 | New derivation? | The five-barrier obstruction argument applied to the spectral-action route is new structural content. Prior status note enumerated Routes A/D/E/F but did not address the spectral-action escape candidate. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) Connes triple axiomatics enumeration, (ii) cutoff function convention numerics, (iii) cutoff scale + non-criticality verification, (iv) sector orthogonality persistence, (v) spectral-coincidence trap numerical scan. |
| V4 | Marginal content non-trivial? | Yes — the meta-pattern identification (cutoff-function `f`/`Λ` convention is the spectral-action analog of hypercharge / root-length / block-counting / quartic-coefficient conventions) is non-obvious from prior notes and directly closes the "NCG escape" hypothesis. |
| V5 | One-step variant? | No — the five-barrier argument is structural across multiple sectors (Connes axiomatics, cutoff conventions, sector orthogonality, criticality), not a relabel of any prior Koide route. The non-criticality numerical scan over four cutoff functions is original content. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior Koide routes. The five-barrier obstruction
  argument applied to the spectral-action route is new structural
  content with explicit numerical scans demonstrating non-criticality
  at A1 and convention dependence on cutoff function shape.
- Identifies a NEW STRUCTURAL OBSTRUCTION FAMILY (S1, S2, S3) not
  present in prior Koide route notes (Routes A/D/E/F focus on different
  primitive admissions; the spectral-action route requires its own
  analysis).
- Closes the "NCG escape" hypothesis specifically, addressing the
  question "can Connes-Chamseddine spectral action principle escape
  the convention-dependence trap of Routes A/D/E/F?" with a definitive
  negative answer.
- Provides explicit numerical scans (4 cutoff functions × 200 `|b|/a`
  values) demonstrating the non-criticality of `Tr f(H²/Λ²)` at A1.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Route F prior obstruction (sister): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Action-form uniqueness no-go (related): [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- CL3 SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Staggered Dirac BZ corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_spectral_action_2026_05_08_probe4.py
```

Expected output: structural verification of (i) probe target identification,
(ii) Barrier S1 spectral-triple primitive enumeration, (iii) Barrier S2
cutoff function convention numerics, (iv) Barrier S3 cutoff scale +
non-criticality at A1, (v) Barrier S4 gauge-vs-Yukawa sector orthogonality,
(vi) Barrier S5 spectral-coincidence trap numerical scan, (vii)
synthesis bounded-obstruction theorem, (viii) falsifiability anchor
(PDG values, anchor-only). Total: 15 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_probe_spectral_action_2026_05_08_probe4.txt`](../logs/runner-cache/cl3_koide_a1_probe_spectral_action_2026_05_08_probe4.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The numerical fact "engineering `f` to have a critical point
  at A1 reproduces the A1 value" is a consistency equality, not a
  structural derivation, and the proposed spectral-action route cannot
  load-bear A1 closure on this basis.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "Connes spectral action picks canonical
  normalizations" by showing that the action-level identification
  (Yukawa matrix internal ratio = spectral-action moment) is not a
  derivable identity — it requires the gauge-to-flavor bridge that
  retained content does not supply, plus three additional primitive
  imports.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the five-barrier
  argument with explicit numerical scans is substantive new structural
  content. The non-criticality scan (4 cutoff functions × 200 `|b|/a`
  values) is original numerical content not present in prior Koide
  route notes.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (still A and D, plus any future spectral-action variants outside
  Connes-Chamseddine) are characterized in terms of WHAT additional
  content would be needed (gauge-to-flavor bridge, normalization
  principle, cross-sector theorem, OR a fundamentally different
  spectral-action variant), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five independent barriers) on the spectral-
  action escape hypothesis, with sharp PASS/FAIL deliverables in
  the runner.
