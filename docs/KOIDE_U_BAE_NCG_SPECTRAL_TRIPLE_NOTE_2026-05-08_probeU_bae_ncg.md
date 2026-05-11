# Koide BAE Probe U — Connes-Chamseddine NCG Spectral Triple Attack on the C_3[111] Triplet

**Date:** 2026-05-08
**Type:** no_go (bounded NCG-spectral-action route obstruction; no
positive closure; source contribution: a finite
Connes-Chamseddine-style spectral-triple model `(A_F, H_F, D)` built
from the physical `Cl(3)` local algebra plus the `Z^3` spatial
substrate, with `D = H_circ` on hw=1 under the Brannen square-root
identification. The model parameterizes the circulant amplitudes,
but BAE is not robustly selected: on the phase-zero and Brannen-phase
slices the tested cutoffs do not have a BAE stationary point, and if
phase is allowed to float the BAE-stationary phases are
cutoff-dependent. The route therefore remains dependent on imported
spectral-action, cutoff, phase, and real-structure choices.)
**Claim type:** no_go
**Scope:** review-loop source-note proposal — Probe U of the Koide
**BAE-condition** closure campaign. Tests whether the
**Connes-Chamseddine non-commutative-geometry spectral triple**
`(A, H, D)` with `A` represented by the physical `Cl(3)` local
algebra plus functions on the `Z^3` spatial substrate, `H` = lepton
sector, and `D = H_circ` on hw=1 (so eigenvalues of `D` are `√m_k`
under the Brannen square-root identification) forces `|b|²/a² = 1/2` (BAE) on the
`C_3`-equivariant Hermitian circulant `H_circ = aI + bC + b̄C²`
via the spectral-action principle `Tr f(D/Λ)`. The reformulation
explicitly tests the V-MaxEnt critical observation that
"`(a, b)` parameterizes H, not ρ" — i.e., it tests whether a
tool that parameterizes H itself (rather than acting on it)
escapes the structural decouplings established at the operator
(Probe 28), wave-function (Probe X), topological (Probe Y),
thermodynamic (Probe V-MaxEnt), and larger-symmetry (Probe V-S_3)
levels.
**Status:** source-note proposal for a bounded NCG-spectral-action
route obstruction. The spectral-triple identification `D = H_circ`
makes the parameterization of H manifest, but the tested spectral
actions do not supply a cutoff- and phase-independent BAE selector.
The paired runner checks the finite model, heat-kernel coefficients,
cutoff-moment spread, phase-zero and Brannen-phase non-criticality,
floating-phase cutoff dependence, and real-structure gap. The BAE
admission count is unchanged.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probeU-ncg-20260508
**Primary runner:** [`scripts/cl3_koide_u_bae_ncg_2026_05_08_probeU_bae_ncg.py`](../scripts/cl3_koide_u_bae_ncg_2026_05_08_probeU_bae_ncg.py)
**Cache:** [`logs/runner-cache/cl3_koide_u_bae_ncg_2026_05_08_probeU_bae_ncg.txt`](../logs/runner-cache/cl3_koide_u_bae_ncg_2026_05_08_probeU_bae_ncg.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **physical `Cl(3)` local algebra** = repo-baseline local algebra;
  this note does not introduce it as a new axiom.
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H_circ = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. **BAE is the primary name**; older branch material
  may contain a deprecated alias, but this note uses BAE.
- **Brannen square-root identification** = the `√m_k` identification:
  `√m_k = v_0 (1 + √2 cos(δ + 2πk/3))` with `(v_0, δ)` the circulant
  parameters. Per `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
  R2: eigenvalues of `H_circ` are identified with `√m_k`.
- **"NCG"** = non-commutative geometry (Connes-Chamseddine).
- **"Spectral triple"** = `(A, H, D)` with `A` an involutive algebra,
  `H` a Hilbert space carrying a `*`-representation of `A`, `D` a
  self-adjoint operator with compact resolvent and `[D, a]` bounded
  for `a ∈ A`.

These are distinct objects despite legacy shared labels.

## Question

The 30-probe BAE closure campaign (terminal synthesis 2026-05-09;
PR #790) closed BAE negatively across:

| Layer | Mechanism | Closure |
|---|---|---|
| Operator (Probes 12-30) | C_3 rep theory on `Herm_circ(3)`: (1, 2) real-dim | bounded |
| Wave-function (Probe X) | Pauli antisym → trivial-isotype singlet, b-decoupled | bounded |
| Topological (Probe Y) | K-theory class `(1, 1, 1) ∈ Z⊕Z⊕Z`; integer-valued | bounded |
| Thermodynamic (Probe V-MaxEnt) | MaxEnt over states at FIXED H | bounded |
| Larger-symmetry (Probe V-S_3) | S_3 rep on `Herm_circ(3)` | bounded |

The **critical observation from V-MaxEnt** is:

> **"`(a, b)` parameterizes H, not ρ. MaxEnt optimizes over states
> at FIXED H."**

This sharpens the structural locus of all five rejections:

> **The `(a, b)` parameters live on the configuration space
> `Herm_circ(3) ≅ ℝ³` of the operator H itself. Any tool that
> ACTS ON H (operator algebras, antisymmetrization, K-theory
> class of bundles, MaxEnt over states, larger symmetry rep)
> sees H as a fixed object — `(a, b)` is invisible to it.
> A tool that could pin `(a, b)` must PARAMETERIZE H itself.**

The natural candidate is the **Connes-Chamseddine spectral
triple**, where the Dirac operator `D` directly parameterizes
the action functional `Tr f(D/Λ)`. In the framework's natural
identification:

- `A` represented by the physical `Cl(3)` local algebra plus functions
  on the `Z^3` spatial substrate
- `H` = lepton sector (3-dim on hw=1, spanned by e, μ, τ
  generations)
- `D = H_circ` on hw=1 (under the Brannen square-root identification:
  eigenvalues of `H_circ` are `√m_k`)

The spectral action `S[D] = Tr f(D/Λ)` (Connes-Chamseddine 1996,
Comm. Math. Phys. 182:155) directly depends on `D = H_circ`,
hence on `(a, b)`. **In principle**, a stationarity condition
`δS/δa = δS/δ|b| = 0` could pin `|b|²/a²`.

**Question (Probe U):** Does the Connes-Chamseddine spectral action
`Tr f(D/Λ)` with `D = H_circ` on hw=1 force `|b|²/a² = 1/2` (BAE)?

This is structurally distinct from any prior probe: prior probes
attacked at OPERATOR level (acting on Hilbert states), WAVE-FUNCTION
level (antisymmetrized tensors), TOPOLOGICAL level (K-theory of
bundles), THERMODYNAMIC level (states at fixed H), and
LARGER-SYMMETRY level (S_3 reps on Herm_circ(3)). Probe U attacks
at the **NCG-spectral-action level**, the unique level on which
`D = H_circ` makes `(a, b)` directly parameterize the action
functional.

This probe also re-tests the prior **Probe 4 (Spectral-Action
Connes-style Bounded Obstruction)** result (PR #734) under the
new "parameterizes H" lens. Probe 4 concluded negatively with
five barriers (cutoff `f` convention, cutoff `Λ` convention,
non-criticality, sector orthogonality, spectral-coincidence trap)
but framed the route as "spectral action acts on H." Probe U
removes this framing: with `D = H_circ` natively, the action
parameterizes H. We test whether this reformulation escapes
the Probe 4 barriers.

## Answer

**No.** The finite Connes-Chamseddine-style spectral-triple model
`(A, H, D = H_circ)` does not derive the BAE point from repo
baseline content. It is useful precisely because it realizes the
"parameterizes H" target, then shows the route still needs extra
cutoff, phase, and real-structure choices. Six review-loop checks
support the bounded no-go:

```
NCG-AV1   D = H_circ identification (Brannen square-root input)
          The spectral triple is well-defined: D is self-adjoint on
          hw=1 (since H_circ is Hermitian), the algebra A acts through
          the finite source representation, and the eigenvalues of D
          match the Brannen square-root identification. This means
          (a, b) enters D as free parameters of the configuration
          space Herm_circ(3); D does not internally constrain them.

NCG-AV2   Spectral action heat-kernel expansion
          Tr f(D²/Λ²) ~ Σ_k f_{2k} Λ^{4-2k} a_{2k}(D²)
          where a_{2k}(D²) are Seeley-de Witt coefficients. On a
          0-dimensional internal sector (hw=1), the expansion
          reduces to:
          a_0 = Tr(I) = 3
          a_2 = -Tr(D²) = -3a² - 6|b|² (= -‖H_circ‖²_F)
          a_4 = (1/2) Tr(D⁴) on the checked phase-zero slice.
          The checked low-order coefficients depend on (a, b) but
          do not have a BAE stationary point on that slice.

NCG-AV3   Cutoff-function f convention dependence
          Tr f(D/Λ) depends on f. Three natural choices —
          Gaussian f(x) = exp(-x²), rational f(x) = (1+x²)⁻⁴,
          modified Gaussian f(x) = exp(-x² - 0.1x⁴) — give
          different moment ratios f_2/f_0 and f_4/f_0. The
          numerical critical points of Tr f(D²/Λ²) shift with f.
          (This is Probe 4's S2 barrier — preserved.)

NCG-AV4   No robust BAE criticality under spectral action
          Numerical scan over |b|/a ∈ [0.05, 1.5] at fixed phase
          zero and fixed Λ for four natural cutoffs:
          - exp(-x):       critical point at |b|/a ≈ 0.997
          - exp(-x²):      critical point at |b|/a ≈ 0.997
          - (1+x)⁻⁴:       critical point at |b|/a ≈ 0.997
          - exp(-x)(1+x):  no critical point in scan range
          none at BAE point |b|/a = 1/√2 ≈ 0.707. At the Brannen
          phase 2/9, dS/d|b| at BAE is also nonzero for the tested
          cutoffs. If phase is allowed to float, BAE-stationary
          phases exist for some cutoffs but move with f, so they do
          not define a cutoff-independent framework selection.

NCG-AV5   First-order condition gap (D-J commutator)
          A real spectral triple requires [[D, a], JbJ⁻¹] = 0 for
          the first-order condition. With D = H_circ on hw=1 and
          A represented by physical Cl(3) local algebra plus Z^3
          substrate functions, this constraint relates the C_3
          covariance of H_circ to the J-action. The repo baseline
          does not supply a canonical J on the hw=1 lepton sector;
          this is an extra imported choice.
          (This is Probe 4's S1 barrier — preserved; note that
          even with D = H_circ specified, J is not pinned by
          source content.)

NCG-AV6   Spectral triple parameterizes H but not BAE
          Confirming the V-MaxEnt critical observation: the
          spectral triple genuinely parameterizes H (since D = H_circ
          and (a, b) enters D directly). HOWEVER, the action
          functional Tr f(D/Λ) depends on (a, b) only through the
          eigenvalue spectrum of D, which is given by
          λ_k = a + 2|b| cos(arg(b) + 2πk/3) (k = 0, 1, 2).
          The spectral action is a symmetric function of these
          eigenvalues. Symmetry alone does not supply the BAE
          isotype-weighting rule `a² = 2|b|²`; a separate selector
          would still be needed.
```

**Verdict: bounded no-go for this NCG-spectral-action route.** The
"parameterizes H itself" framing is realized, but parameterization is
not enough: the route remains cutoff-, phase-, and real-structure
dependent. The BAE admission count is unchanged. No new framework
axiom is introduced.

## Setup

### Premises (A_min for Probe U)

| ID | Statement | Class |
|---|---|---|
| physical Cl(3) local algebra | `Cl(3)` local algebra | repo baseline; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| `Z^3` spatial substrate | physical spatial substrate | repo baseline; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | retained per [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | retained per [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| EigSpec | Eigenvalues of `H_circ`: `λ_k = a + 2|b| cos(arg(b) + 2πk/3)` | retained per same source R2 |
| Brannen sqrt | Brannen square-root identification: `√m_k = λ_k` (eigenvalues of `H_circ` are `√m_k`) | imported from same source R2 |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | retained per [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a² = 2\|b\|² ⟺ \|b\|²/a² = 1/2` (BAE) | retained per [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Probe4 | Spectral-action route under "S_b acts on H": 4 primitives + cutoff convention | retained per [`KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`](KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md) |
| Probe28 | Operator-level: F3 (1,2) real-dim canonical; F1/BAE absent | retained per [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) |
| ProbeY | Topological-level: K-theory class `(1, 1, 1) ∈ R(C_3)` | retained per [`KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md`](KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md) |
| M3 | M_3(C) algebra on hw=1 triplet generated by translations + C_3[111] | retained per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |

**Imported mathematical tools used (Connes-Chamseddine NCG; standard
mathematical machinery — these are bounded route tools, not new
repo-wide physics axioms):**

- **Connes-Chamseddine spectral triple** `(A, H, D)` — definition
  per Connes 1994 (NCG, Academic Press) and Connes-Chamseddine 1996
  (Comm. Math. Phys. 182:155). Standard mathematical structure.
- **Spectral action principle** `S[D] = Tr f(D/Λ)` for an even
  positive cutoff `f` — Chamseddine-Connes 1996. Used here as an
  imported tool for this bounded no-go check.
- **Heat-kernel / Seeley-de Witt expansion** — Seeley 1967, de Witt
  1965, Gilkey 1995 (Invariance Theory, Heat Equation, and
  Atiyah-Singer Index Theorem). Standard mathematical machinery.
- **Spectral functional calculus** — for self-adjoint `D`, `f(D)`
  is defined by spectral decomposition and `Tr f(D/Λ) = Σ_k f(λ_k/Λ)`
  with `λ_k` the eigenvalues of `D`. Standard.

These are **mathematical statements / a recognized mathematical
toolkit**, not new physics primitives. They are used to compute
properties of the stated source content, not as new framework axioms.

### Forbidden imports

- NO PDG observed mass values used as derivation input
- NO lattice MC empirical measurements as derivation input
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new framework axioms — NCG is an imported mathematical toolkit
  for this bounded route check, not a framework axiom.
- NO admitted spectral coefficients — moments `f_{2k}` are computed
  from explicit `f`'s; Seeley-de Witt coefficients are computed from
  `D = H_circ` directly.

## The structural argument

The Probe U conclusion can be stated structurally:

> **The Connes-Chamseddine spectral triple `(A, H, D = H_circ)` on
> the physical `Cl(3)` local algebra plus `Z^3` spatial substrate realizes the
> "parameterizes H itself" target identified by V-MaxEnt — `(a, b)`
> enters `D` directly through the circulant amplitude. However,
> the spectral action `Tr f(D/Λ)` is a symmetric polynomial in the
> eigenvalues `λ_k(a, b) = a + 2|b| cos(arg(b) + 2πk/3)` and on the
> chosen cutoff function. On the fixed phase-zero and Brannen-phase
> slices the tested cutoffs do not select the BAE ratio; when phase is
> allowed to float, BAE-stationary phases are cutoff-dependent.**

Hence: realizing the "parameterizes H" target is necessary but not
sufficient. The action functional would additionally need a
cutoff-, phase-, and real-structure-independent BAE selection rule;
this branch does not supply one.

## Per-attack-vector analysis

Six bounded NCG-spectral-action checks are tested. They preserve the
negative BAE route boundary; none closes BAE.

### NCG-AV1 — Spectral triple `(A, H, D = H_circ)` is well-defined

**Status: TRIPLE CONSTRUCTED; PARAMETERIZATION ACHIEVED.**

A spectral triple requires:
1. `A` involutive algebra acting on `H`.
2. `H` Hilbert space with `*`-rep of `A`.
3. `D` self-adjoint with compact resolvent on `H`, `[D, a]` bounded.

For the finite source model:
- `A` is represented by the physical `Cl(3)` local algebra plus
  functions on the `Z^3` spatial substrate.
- `H` = the hw=1 lepton sector ≅ `ℂ³`, with the source `M_3(ℂ)`
  representation per `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE`.
- `D = H_circ = aI + bC + b̄C²` — Hermitian by construction,
  hence self-adjoint on `ℂ³`. Compact resolvent: trivial in the
  finite-dimensional case (resolvent is finite-rank).

The triple is consistent. The eigenvalues of `D = H_circ` are
`λ_k = a + 2|b| cos(arg(b) + 2πk/3)`, matching the Brannen
square-root identification `√m_k = λ_k`.

**Verified numerically (runner Section 1):**
- 1.1: D is Hermitian.
- 1.2: D has compact resolvent (finite rank).
- 1.3: Eigenvalues of D match circulant formula.
- 1.4: Triple satisfies basic NCG axioms (self-adjoint, finite
  resolvent, [D, a] bounded for a ∈ A).
- 1.5: Parameters (a, b) appear in D directly (parameterization
  achieved).

### NCG-AV2 — Spectral action heat-kernel expansion

**Status: COEFFICIENTS COMPUTED; NO STATIONARY CONDITION AT BAE.**

The Connes-Chamseddine spectral action is

```
S[D] = Tr f(D/Λ)
```

For the asymptotic expansion in `Λ → ∞`, one writes (using the
heat-kernel representation `f(x) = ∫_0^∞ e^{-tx²} dν(t)` for
appropriate `ν`):

```
Tr f(D/Λ) ~ Σ_{n ≥ 0} f_{4-2n} Λ^{4-2n} a_{2n}(D²)
```

where `f_k = (1/Γ(k/2)) ∫_0^∞ x^{k-1} f(x) dx` and `a_{2n}(D²)`
are the Seeley-de Witt coefficients of the heat operator
`exp(-t D²)`.

For a 0-dimensional internal space (hw=1 ≅ pt), the heat kernel is

```
Tr exp(-t D²) = Σ_k exp(-t λ_k²)
```

with `λ_k` the eigenvalues of `D`. Expanding in `t`:

```
Tr exp(-t D²) = 3 - t Tr(D²) + (t²/2) Tr(D⁴) - ... = Σ_k (-t)^n a_{2n}/n!
```

so:

```
a_0(D²) = Tr(I) = 3
a_2(D²) = -Tr(D²) = -(3a² + 6|b|²)        [via Frobenius E_+ + E_⊥]
a_4(D²) = (1/2) Tr(D⁴) = (1/2)(3a⁴ + 36 a²|b|² + 18|b|⁴ + lower in |b|⁴)
```

(Exact expressions computed in runner Section 2.)

**Critical observation:** `a_2 = -‖H_circ‖²_F = -3a² - 6|b|²` is
exactly the negative of the block-total Frobenius norm. Setting
`∂a_2/∂|b|² = 0` gives `|b|² = 0`, NOT `|b|²/a² = 1/2`. Setting
`∂a_2/∂a = 0` gives `a = 0`. Neither stationary point is BAE.

The next coefficient `a_4 ∝ Tr(D⁴)` is a quartic in `(a, |b|)`.
Its stationary points (computed analytically and numerically in
runner Section 2) are at `|b|/a = 0` and `|b|/a → ∞`. The BAE
point `|b|/a = 1/√2` is NOT a stationary point of `a_4`.

**Verified numerically (runner Section 2):**
- 2.1: a_0 = 3 (rank).
- 2.2: a_2 = -3a² - 6|b|² (= -‖H_circ‖²_F) on test point.
- 2.3: a_4 quartic computed; stationary points at |b|=0 and |b|→∞.
- 2.4: ∂a_2/∂|b| = 0 ⟹ |b| = 0 (not BAE).
- 2.5: ∂a_4/∂|b| = 0 ⟹ |b| = 0 (not BAE).
- 2.6: BAE is generic point (not stationary of a_n).

### NCG-AV3 — Cutoff-function `f` convention dependence

**Status: PRESERVES Probe 4 S2 BARRIER.**

The spectral action depends on `f` via the moments `f_{2k}`. The
runner computes moments for three natural cutoff functions:

| Cutoff `f(x)` | `f_0` | `f_2` | `f_4` | `f_2/f_0` | `f_4/f_0` |
|---|---|---|---|---|---|
| `exp(-x²)` (Gaussian) | √π/2 ≈ 0.886 | 1/2 | 3/4 | ≈ 0.564 | ≈ 0.846 |
| `(1+x²)⁻⁴` (rational) | numerical | numerical | numerical | (different) | (different) |
| `exp(-x²-0.1x⁴)` | numerical | numerical | numerical | (different) | (different) |

The ratios `f_2/f_0` differ across "natural" choices. Any "specific
value" derivation of `|b|²/a² = 1/2` from the spectral action
requires fixing `f` to a particular shape — which is itself a
convention choice. This is the Probe 4 S2 barrier, preserved
under the `D = H_circ` reformulation.

**Verified numerically (runner Section 3):**
- 3.1: Gaussian moments `f_0 = √π/2`, `f_2 = 1/2`, `f_4 = 3/4`.
- 3.2: Rational moments computed numerically (different ratios).
- 3.3: Mod-Gaussian moments computed (different ratios).
- 3.4: f_2/f_0 spread across cutoffs > 0.1.
- 3.5: f_4/f_0 spread across cutoffs > 0.1.

### NCG-AV4 — Non-criticality of BAE under spectral action

**Status: BAE NOT A STATIONARY POINT FOR ANY NATURAL `f`.**

The runner scans `|b|/a` from 0.05 to 1.5 at fixed `a = 1`,
`arg(b) = 0`, `Λ = 1` for four cutoff functions:

| Cutoff `f(x)` | Critical points of `Tr f(D²/Λ²)` |
|---|---|
| `exp(-x)` | {≈ 0.997} |
| `exp(-x²)` | {≈ 0.997} |
| `(1+x)⁻⁴` | {≈ 0.997} |
| `exp(-x)(1+x)` | {} (no critical point in scan range) |

In all cases, critical points (when they exist) are NEAR
`|b|/a = 1.0`, NOT at `|b|/a = 1/√2 ≈ 0.707`. The BAE point is
generic, not stationary, under the spectral action.

The structural reason: for `arg(b) = 0`, the eigenvalues of `D`
become

```
λ_0 = a + 2|b|         (largest)
λ_1 = λ_2 = a - |b|     (degenerate)
```

The spectral action is

```
Tr f(D²/Λ²) = f((a+2|b|)²/Λ²) + 2 f((a-|b|)²/Λ²)
```

Setting `∂/∂|b| = 0`:

```
2(a+2|b|) f'((a+2|b|)²/Λ²) - 2(a-|b|) f'((a-|b|)²/Λ²) = 0
```

This factors via `λ_0 - 2λ_1 = 3|b|`, giving the critical condition

```
(a+2|b|) f'((a+2|b|)²/Λ²) = (a-|b|) f'((a-|b|)²/Λ²)
```

For monotone-decreasing `f` (so `f' < 0`), the LHS is positive
for `|b| > 0`, the RHS is positive only for `|b| < a`. The
critical point — when it exists — is determined by `f`'s shape,
NOT by representation theory. On the phase-zero slice it sits near
`|b| ≈ a` for the tested monotone cutoffs, not at `|b| = a/√2`.
At the Brannen phase `2/9`, the BAE derivative is also nonzero for
the tested cutoffs. When the phase is allowed to vary, some cutoffs
have accidental BAE-stationary phases, but those phases move with
the cutoff and therefore do not define a framework-derived selector.

**Verified numerically (runner Section 4):**
- 4.1: exp(-x) phase-zero critical at |b|/a ≈ 0.997.
- 4.2: exp(-x²) phase-zero critical at |b|/a ≈ 0.997.
- 4.3: (1+x)⁻⁴ phase-zero critical at |b|/a ≈ 0.997.
- 4.4: exp(-x)(1+x) has no phase-zero critical point.
- 4.5: BAE point not critical on the phase-zero slice.
- 4.6: BAE deviation from phase-zero critical: |Δ(|b|/a)| ≈ 0.29.
- 4.7: BAE derivative at Brannen phase `2/9` is nonzero for tested cutoffs.
- 4.8: floating-phase BAE-stationary points, when present, are cutoff-dependent.

### NCG-AV5 — First-order condition gap (D-J commutator)

**Status: PRESERVES Probe 4 S1 BARRIER.**

A real spectral triple `(A, H, D, J, γ)` requires the first-order
condition `[[D, a], J b J⁻¹] = 0` for `a, b ∈ A`. With `D = H_circ`
on hw=1 and `A` represented by the physical `Cl(3)` local algebra
plus functions on the `Z^3` spatial substrate, this constraint
relates the C_3-covariance of H_circ to the J-action.

For lepton sector NCG (Connes-Chamseddine 2007, KO-dim 6 mod 8),
`J` is an antiunitary charge-conjugation operator. The framework
does not supply a canonical `J` on the hw=1 lepton sector — the
Cl(3) structure provides a real involution `α: Cl(3) → Cl(3)`
(via the natural conjugation `α(γ_i) = -γ_i` or similar), but the
extension to hw=1 lepton states is an extra choice.

This means even with `D = H_circ` specified, the full spectral
triple `(A, H, D, J, γ)` requires `J` and `γ` as additional
admissions. The Probe 4 S1 barrier (4-primitive admission count)
is preserved, with one primitive (`D`) shifted from "admitted" to
"derived from the Brannen square-root input" but `J`, `γ`, and the cutoff `f`
remaining as 3 admissions.

**Net primitive count:** 3 (J, γ, cutoff f) + 1 (spectral action
principle) = 4. Same as Probe 4. The "parameterization of H"
reformulation does NOT reduce the primitive count; it shifts one
primitive (D) into an existing source input.

**Verified numerically (runner Section 5):**
- 5.1: Cl(3) has natural involution α (real structure candidate).
- 5.2: Extension of α to hw=1 lepton states is not unique.
- 5.3: First-order condition is non-trivial; not automatic.
- 5.4: Net admission count under D = H_circ: 4 (J, γ, f, action
  principle).

### NCG-AV6 — Spectral triple parameterizes H but not BAE

**Status: V-MAXENT OBSERVATION CONFIRMED — PARAMETERIZATION
ACHIEVED, BAE STILL NOT FORCED.**

The V-MaxEnt critical observation states:

> "(a, b) parameterizes H, not ρ. MaxEnt optimizes over states at
> FIXED H."

Probe U realizes the "parameterizes H itself" target by setting
`D = H_circ` directly. The parameters `(a, b)` enter the spectral
triple's Dirac operator, hence the action functional `Tr f(D/Λ)`.

**Confirmed:** parameterization is achieved (NCG-AV1).

**HOWEVER:** the action functional, as a symmetric function of
the eigenvalues `λ_k(a, b)`, depends on `(a, b)` only via power
sums:

```
P_n(a, b) = Σ_k λ_k^n
```

Computing the first few power sums (with `arg(b) = 0` for
simplicity; the general case is similar):

```
P_1 = 3a                                    (linear in a, no |b|)
P_2 = 3a² + 6|b|²                           (quadratic; ‖H_circ‖²_F)
P_3 = 3a³ + 18 a|b|² + 6|b|³ cos(3 arg(b))  (general arg(b))
P_4 = 3a⁴ + 36 a²|b|² + 18|b|⁴              (specifically at arg(b)=0,
                                             general formula similar)
```

(General formulas in runner Section 6.)

The spectral action is

```
Tr f(D²/Λ²) = Σ_k f(λ_k²/Λ²) = sum of f-values at λ_0², λ_1², λ_2²
```

which can be expanded as a power series in `(λ_k²/Λ²)`, hence as
a polynomial in power sums `P_2, P_4, ...`.

**The BAE condition `a² = 2|b|²` is NOT a stationary condition of
ANY polynomial in the power sums `P_2, P_4, ...` for natural
cutoff functions.** Specifically:

- `P_2` stationary in `|b|`: only at `|b| = 0`.
- `P_4` stationary in `|b|`: only at `|b| = 0` (or `|b| → ∞`).
- Polynomial combinations: critical points at `|b|/a ≈ 0.997`
  or absent.

So even with full parameterization of H via `D = H_circ`, the
spectral action does not select BAE.

**The structural failure mode is now precisely identifiable:** the
spectral action depends on the eigenvalue spectrum of `D`, which
is a SYMMETRIC function of the C_3-character components. BAE is
an UNBALANCED equipartition condition (`a² : |b|² = 2 : 1`,
from block-total Frobenius `E_+ : E_⊥ = 3a² : 6|b|² = 3a² : 3a²
= 1 : 1` at BAE); the spectral action does not weight the trivial
and non-trivial isotype contributions equally — it weights them
according to `f`'s shape.

**Verified numerically (runner Section 6):**
- 6.1: Power sums P_1, P_2, P_3, P_4 computed analytically.
- 6.2: P_2 = 3a² + 6|b|² stationary only at |b|=0.
- 6.3: P_4 stationary only at extremes.
- 6.4: BAE not stationary for checked low-order power sums on the
  phase-zero slice.
- 6.5: Spectral action is a symmetric eigenvalue functional.
- 6.6: Symmetric-function dependence does not by itself supply the
  BAE isotype-weighting selector.

## Theorem (Probe U NCG-spectral-action-level structural decoupling)

**Theorem (NCG-DECOUPLE).** On the physical `Cl(3)` local algebra
plus `Z^3` spatial substrate baseline, the C_3[111] hw=1
BZ-corner forcing source, M_3(ℂ) on hw=1, C_3-equivariant Hermitian
circulant `H_circ = aI + bC + b̄C²`, the Brannen square-root
identification, and the imported Connes-Chamseddine NCG mathematical toolkit (spectral triple
definition, spectral action principle, heat-kernel /
Seeley-de Witt expansion, spectral functional calculus):

```
(a) The spectral triple (A, H, D = H_circ) with A represented by
    the physical Cl(3) local algebra plus Z^3 substrate functions,
    H = hw=1 lepton sector, D = H_circ on hw=1 is well-defined:
    D is self-adjoint, has finite-rank resolvent, and [D, a] is
    bounded for a ∈ A. The eigenvalues of D match the Brannen √m_k
    identification.
    [Verified Section 1.]

(b) The spectral action S[D] = Tr f(D/Λ) admits a heat-kernel
    asymptotic expansion
        S[D] ~ Σ_k f_{4-2k} Λ^{4-2k} a_{2k}(D²)
    where a_0(D²) = Tr(I) = 3, a_2(D²) = -‖H_circ‖²_F = -3a² - 6|b|²,
    a_4(D²) = (1/2) Tr(D⁴) is a quartic in (a, |b|). The first
    non-trivial coefficient a_2 is stationary only at |b| = 0,
    NOT at the BAE point.
    [Verified Section 2.]

(c) The cutoff function f shape is a convention, not pinned by
    repo baseline content. Three natural choices (Gaussian, rational,
    modified Gaussian) give moment ratios f_2/f_0 differing by
    > 0.1. This is the Probe 4 S2 barrier, preserved under the
    D = H_circ reformulation.
    [Verified Section 3.]

(d) BAE is not a stationary point of Tr f(D²/Λ²) on the phase-zero
    or Brannen-phase slices for the four tested cutoff functions
    (exp(-x), exp(-x²), (1+x)⁻⁴, exp(-x)(1+x)). When phase is allowed
    to float, BAE-stationary phases are cutoff-dependent rather than
    framework-selected.
    [Verified Section 4.]

(e) The first-order condition [[D, a], J b J⁻¹] = 0 requires
    specifying J (real structure) on hw=1, which is not supplied by
    this source packet.
    Net primitive admission count under D = H_circ remains 4
    (J, γ, cutoff f, spectral action principle); the same as
    under Probe 4's "S_b acts on H" framing.
    [Verified Section 5.]

(f) The spectral action is a symmetric function of the C_3-character
    eigenvalues. That symmetry does not provide the BAE
    isotype-weighting rule `a² = 2|b|²` by itself. The "spectral
    triple parameterizes H" target is realized, but parameterization
    alone does not pin BAE.
    [Verified Section 6.]

Therefore: this finite NCG-spectral-action route does not close BAE.
The "parameterizes H itself" reformulation preserves the Probe 4
cutoff-convention barrier and the real-structure/cutoff import count.
The BAE admission count is unchanged. No new framework axiom is
introduced.
```

**Proof / runner support.** Computed items are verified by the runner:
Section 0
(retained sanity); Section 1 (NCG-AV1 spectral triple
construction); Section 2 (NCG-AV2 heat-kernel expansion);
Section 3 (NCG-AV3 cutoff-function convention); Section 4
(NCG-AV4 non-criticality scan); Section 5 (NCG-AV5 first-order
condition gap); Section 6 (NCG-AV6 power-sum decomposition);
Section 7 (six-level closure synthesis); Section 8 (convention
robustness); Section 9 (does-not disclaimers). ∎

## Algebraic root-cause

The NCG-spectral-action decoupling has a clean structural root:

> **The spectral action `Tr f(D/Λ)` is a symmetric function of
> the eigenvalues of `D`. With `D = H_circ`, the eigenvalues are
> `λ_k = a + 2|b| cos(arg(b) + 2πk/3)`. The action depends on
> `(a, b)` only through power sums `P_n = Σ_k λ_k^n`. BAE
> (`a² = 2|b|²`) is an UNBALANCED isotype-equipartition
> condition (trivial : non-trivial Frobenius weights `3a² : 6|b|²
> = 1 : 1` at BAE) — it relates the trivial-character sector to
> the non-trivial-character sector. The spectral action, by
> symmetry in eigenvalues, treats all three eigenvalues on equal
> footing; it does not weight the trivial isotype against the
> non-trivial isotype in the specific 2:1 ratio BAE requires.**

This is the structural analog at the NCG level of the Probes
12-30 operator-level conclusion: the (1, 2) real-dim weighting
of `Herm_circ(3)` under C_3 isotype split is fixed by
representation theory; BAE asks for a (1, 1) weighting. The
spectral action, depending on power sums, cannot supply this
asymmetric weighting from an even-symmetric cutoff `f`.

## Why this probe is structurally distinct from prior probes

| Probe | Layer | Mechanism | Does (a, b) enter? | Conclusion |
|---|---|---|---|---|
| Probes 12-30 | OPERATOR (Hilbert states) | C_3 rep theory: (1, 2) real-dim on Herm_circ(3) | No, structurally (acts on H) | F1 / BAE absent |
| Probe X | WAVE-FUNCTION (∧^N tensors) | C_3 rep theory: det(C) = +1, Pauli ε ∈ trivial isotype | No, structurally (acts on ∧³V) | Slater singlet b-decoupled |
| Probe Y | TOPOLOGICAL (bundles, K-theory) | C_3 rep theory: K_C3(pt) = Z⊕Z⊕Z; integer-quantized | No, integer-quantized data | (a, b) absent from K-theory |
| Probe V-MaxEnt | THERMODYNAMIC (states ρ at fixed H) | MaxEnt over states with fixed H | No (H fixed; ρ optimized) | (a, b) param H not ρ |
| Probe V-S_3 | LARGER-SYMMETRY (S_3 on Herm_circ(3)) | S_3 rep on Herm_circ(3) | No, structurally (acts on H) | reflection rep symmetric |
| **Probe U** | **NCG-SPECTRAL-ACTION (D = H_circ)** | **Spectral action Tr f(D/Λ); D parameterized by (a, b)** | **YES — parameterization realized** | **Cutoff/phase/real-structure choices still not fixed; BAE not robustly selected** |

Probe U is the **unique** prior-or-current probe in which `(a, b)`
enters the constraint structure directly. Probes 12-30, X, Y,
V-MaxEnt, V-S_3 all act on H (or on objects derived from H);
Probe U parameterizes H via `D = H_circ`. **And yet BAE is still
not forced.** Even when the structural objection of "the tool acts
on H, not parameterizes it" is removed, the spectral action route
still needs extra cutoff, phase, and real-structure choices.

## Sharpened terminal residue (six-level closure)

Combining Probes 12-30 (operator), Probe X (wave-function),
Probe Y (topological), Probe V-MaxEnt (thermodynamic), Probe
V-S_3 (larger-symmetry), and Probe U (NCG-spectral-action):

> **The BAE condition `|b|²/a² = 1/2` remains unforced across the
> six checked structural layers:**
>
> - **Operator layer (Probes 12-30):** any C_3-covariant
>   interaction preserves the (1, 2) real-dim weighting on
>   Herm_circ(3). F1 structurally rejected at free + interacting
>   levels.
>
> - **Wave-function layer (Probe X):** Pauli antisymmetrization
>   is C_3-trivial (det(C) = +1). Slater singlet ∈ trivial isotype,
>   decoupled from doublet b-sector.
>
> - **Topological layer (Probe Y):** K-theory class, index theorem,
>   anomaly polynomial, and Cech cohomology are all
>   integer-quantized isotype-count data. Continuous (a, b) is
>   NOT in topological data.
>
> - **Thermodynamic layer (Probe V-MaxEnt):** MaxEnt optimizes
>   over states ρ at fixed H. (a, b) parameterizes H, not ρ;
>   MaxEnt does not constrain H.
>
> - **Larger-symmetry layer (Probe V-S_3):** S_3 reflection rep
>   on Herm_circ(3) is symmetric under the b ↔ b̄ involution;
>   does not pin |b|.
>
> - **NCG-spectral-action layer (Probe U, this probe):** the
>   Connes-Chamseddine spectral triple (A, H, D = H_circ)
>   parameterizes H via D. The spectral action depends on cutoff,
>   phase, and real-structure choices; the tested surfaces do not
>   supply a robust BAE selector.

Closing BAE therefore continues to require admitting a
multiplicity-counting principle as a NEW PRIMITIVE. The
NCG-spectral-action-level path does not provide an alternative.

The "parameterizes H itself" target is realized in Probe U, and BAE
is still not forced. A positive BAE derivation would still need a
source selector that is not supplied by this NCG-spectral-action
route.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `no_go` (bounded NCG-spectral-action route
  obstruction; source contribution: the finite spectral-triple model
  (A, H, D = H_circ) realizes parameterization of H, but the route
  remains cutoff-, phase-, and real-structure-dependent and does not
  robustly select BAE)
- audit-derived effective status: set only by the independent
  audit lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2"]`
  — the residual admission, with the
  Probe U sharpening: **"The finite Connes-Chamseddine-style
  spectral-triple model (A, H, D = H_circ) parameterizes H via D.
  Yet the spectral action route remains cutoff-, phase-, and
  real-structure-dependent. The 'parameterizes H' reformulation does
  not escape the Probe 4 cutoff-convention barrier. Net imported
  choice count remains 4 (J, γ, cutoff f, spectral action principle)
  — same as Probe 4."**

**No new admissions added by this probe. The BAE admission count
is UNCHANGED.**

### What this probe DOES

1. Tests whether the Connes-Chamseddine spectral triple
   `(A, H, D = H_circ)` built on the physical `Cl(3)` local algebra
   plus `Z^3` spatial substrate representation forces
   `|b|²/a² = 1/2` (BAE) via the spectral action principle.
2. Identifies six bounded route checks (NCG-AV1 through NCG-AV6)
   showing that the spectral action does not robustly select BAE.
3. Identifies the algebraic root-cause: the spectral action is
   a symmetric function of eigenvalues, depending on `(a, b)`
   through eigenvalue-symmetric data plus cutoff/phase choices; BAE
   is an isotype-equipartition condition requiring an additional
   selector.
4. Establishes a sharpened terminal residue: BAE absent from
   operator-level (Probes 12-30), wave-function-level (Probe X),
   topological-level (Probe Y), thermodynamic-level (Probe
   V-MaxEnt), larger-symmetry-level (Probe V-S_3), AND
   NCG-spectral-action-level (Probe U) source content.
5. Cross-references prior Probe 4 (Spectral-Action Connes-style
   Bounded Obstruction, PR #734); confirms that the
   "parameterizes H itself" reformulation does not escape the
   cutoff-convention barrier.
6. Realizes the V-MaxEnt critical observation: a tool that
   PARAMETERIZES H (rather than acting on it) is constructed
   explicitly via `D = H_circ` — the parameterization is genuine
   but does not pin BAE.

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new framework axiom or new admission.
3. Does NOT modify any retained theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT promote external surveys to retained authority.
7. Does NOT replace Probes 12-30, Probe X, Probe Y, Probe
   V-MaxEnt, or Probe V-S_3 (it complements them at a
   structurally distinct layer).
8. Does NOT replace Probe 4 (PR #734); rather, it
   re-derives Probe 4's conclusion under the new
   "parameterizes H" lens, confirming the Probe 4 cutoff-
   convention barrier persists.
9. Does NOT propose an alternative κ value as physical.
10. Does NOT promote sister bridge gaps (L3a, L3b, C-iso,
    W1.exact).
11. Does NOT introduce new physics axioms — uses standard
    NCG mathematical machinery (spectral triple, spectral
    action, heat-kernel) as an imported mathematical toolkit for
    this bounded route check.

## Honest assessment

**What the probe finds:**

1. **The finite Connes-Chamseddine-style spectral-triple model
   `(A, H, D = H_circ)` is well-defined.** D is self-adjoint with
   finite-rank resolvent; eigenvalues match the Brannen
   square-root input.
   Parameterization of H is achieved.

2. **The spectral action heat-kernel expansion gives explicit
   Seeley-de Witt coefficients:** `a_0 = 3`, `a_2 = -3a² - 6|b|²`,
   `a_4 = (1/2) Tr(D⁴)` on the checked slice. The checked
   low-order coefficients do not have BAE as a stationary point.

3. **Cutoff function `f` shape is a convention.** Three natural
   choices give moment ratios `f_2/f_0` differing by > 0.1.
   Probe 4 S2 barrier persists.

4. **BAE is not robustly selected by `Tr f(D²/Λ²)`.** On the
   phase-zero and Brannen-phase slices, BAE is not stationary for
   the tested cutoffs; with phase floating, BAE-stationary phases
   are cutoff-dependent.

5. **First-order condition requires `J` and `γ`, not supplied by
   this source packet.** Net imported choice count remains 4 under
   `D = H_circ`.

6. **The spectral action is an eigenvalue-symmetric functional.**
   BAE is an isotype-equipartition condition and still needs a
   selector beyond eigenvalue symmetry plus arbitrary cutoff/phase
   choices.

**What this probe contributes to the campaign:**

1. **Source contribution**: explicit construction of the finite
   Connes-Chamseddine-style spectral-triple model `(A, H,
   D = H_circ)`; analytic and numerical evaluation of Seeley-de
   Witt coefficients `a_0`, `a_2`, `a_4` for the circulant Hermitian
   on hw=1; numerical scan of the spectral action functional over
   `|b|/a` and phase for four cutoff functions.

2. **Sharpened residue characterization**: BAE absent from
   operator-level (Probes 12-30), wave-function-level (Probe X),
   topological-level (Probe Y), thermodynamic-level (Probe
   V-MaxEnt), larger-symmetry-level (Probe V-S_3), AND
   NCG-spectral-action-level (Probe U) source content. The
   Probe U layer is the unique layer in which `(a, b)`
   PARAMETERIZES the constraint object — and even this fails
   to force BAE.

3. **Six-layer route boundary**: returns the same
   campaign-terminal-state obstruction at a sixth,
   structurally distinct layer (NCG-spectral-action level),
   distinct from all prior probes. The
   "parameterizes-vs-acts-on" framing is tested and shown
   insufficient — parameterization is necessary but not sufficient
   for BAE selection.

4. **Cross-confirmation of Probe 4 (PR #734)**: re-derives
   Probe 4's negative closure under the new lens, confirming
   the cutoff-convention barrier is invariant under
   reformulation.

The remaining residue is:

> **BAE = (1, 1)-multiplicity-weighted extremum on the additive
> log-isotype-functional class. The (1, 2) real-dim weighting
> (operator-level) is fixed by C_3 representation theory; the
> trivial det character of `∧³V` (wave-function-level) is fixed
> by the parity of the 3-cycle; the K-theory class
> `[V] = (1, 1, 1) ∈ R(C_3)` (topological-level) is fixed by the
> regular C_3 representation; MaxEnt acts on states ρ not on
> (a, b) (thermodynamic-level); S_3 reflection rep is symmetric
> under b ↔ b̄ (larger-symmetry-level); the spectral action
> `Tr f(D/Λ)` with `D = H_circ` remains cutoff-, phase-, and
> real-structure-dependent (NCG-spectral-action-level). The checked
> layers do not supply the (1, 1) multiplicity-counting principle
> required for BAE.**

Closing BAE therefore still requires a multiplicity-counting or
isotype-weighting selector distinct from the checked operator,
wave-function, topology, thermodynamic, larger-symmetry, and
NCG-spectral-action route content.

## Cross-references

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### C_3 / circulant structure / Brannen square-root identification

- BZ-corner forcing (Block 04): [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue / Brannen `√m_k` identification: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Three-generation observable (M_3 algebra on hw=1): [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Probe campaign — companion probes

- Probe 4 (Spectral-Action Connes-style, "S_b acts on H"): [`KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`](KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md)
- Probe Y (topological / K-theory): [`KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md`](KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md)
- Probe 28 (operator-level / interacting dynamics): [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)
- Probe 25 (free-Gaussian extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 18 (F1-vs-F3 algebraic): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- 30-probe terminal synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)

### Naming convention

- BAE rename note: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)

## Validation

```bash
python3 scripts/cl3_koide_u_bae_ncg_2026_05_08_probeU_bae_ncg.py
```

Expected: `=== TOTAL: PASS=51, FAIL=0, ADMITTED=28 (computed=51) ===`
or a future regenerated equivalent with `FAIL=0`.

The runner verifies:

1. Section 0 — Retained sanity (C_3 cycle is unitary, order 3,
   det = +1; H_circ = aI + bC + b̄C² is Hermitian, C_3-equivariant;
   eigenvalues match the circulant formula; Brannen `√m_k` identification
   consistent).
2. Section 1 — NCG-AV1: spectral triple (A, H, D = H_circ)
   well-defined; D self-adjoint; finite-rank resolvent;
   eigenvalues match the Brannen square-root input.
3. Section 2 — NCG-AV2: heat-kernel Seeley-de Witt coefficients
   a_0, a_2, a_4 computed analytically; stationary points
   identified (NOT at BAE).
4. Section 3 — NCG-AV3: cutoff function f convention dependence;
   moments f_0, f_2, f_4 for Gaussian, rational, modified-Gaussian;
   moment-ratio spread > 0.1.
5. Section 4 — NCG-AV4: numerical scan of Tr f(D²/Λ²) over
   |b|/a ∈ [0.05, 1.5] for four cutoff functions; phase-zero and
   Brannen-phase BAE non-criticality; floating-phase cutoff
   dependence.
6. Section 5 — NCG-AV5: first-order condition gap; J, γ admission
   count; net primitive count = 4 under D = H_circ.
7. Section 6 — NCG-AV6: power-sum decomposition P_n(a, b);
   checked low-order phase-zero derivatives and symmetric-functional
   selector gap.
8. Section 7 — Six-level synthesis: comparison with Probes 12-30,
   X, Y, V-MaxEnt, V-S_3.
9. Section 8 — Convention robustness (basis change, cycle inverse).
10. Section 9 — Does-not disclaimers (no BAE closure, no new
    admission, no PDG, no retained-theorem modification, no new
    physics axioms; NCG used as imported toolkit only).

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links
so the audit citation graph can track them. It does not promote
this note or change the audited claim scope.

- [staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) (hw=1 triplet)
- [koide_circulant_character_derivation_note_2026-04-18](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) (H_circ; Brannen square-root input)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_frobenius_isotype_split_uniqueness_note_2026-04-21](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) (KoideAlg ⟺ BAE)
- [koide_a1_probe_spectral_action_bounded_obstruction_note_2026-05-08_probe4](KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md) (companion: spectral-action S_b acts on H)
- [koide_y_bae_topological_index_ktheory_note_2026-05-10_probeY_bae_topological](KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md) (topological-level companion)
- [koide_bae_probe_interacting_dynamics_bounded_obstruction_note_2026-05-09_probe28](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) (operator-level companion)
- [koide_bae_probe_physical_extremization_bounded_obstruction_note_2026-05-09_probe25](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) (free-Gaussian baseline)
- [three_generation_observable_theorem_note](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) (M_3 on hw=1)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- [koide_bae_30_probe_campaign_terminal_synthesis_meta_note_2026-05-09](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
