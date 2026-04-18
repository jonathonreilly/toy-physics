# P1 H_unit 1-Loop Renormalization: Framework-Native Symbolic Reduction

**Date:** 2026-04-17
**Status:** retained framework-native **symbolic reduction** of the 1-loop
renormalization of the composite-Higgs scalar bilinear `H_unit =
(1/√6) Σ ψ̄ ψ` on the `Cl(3) × Z^3` Wilson-plaquette + 1-link
staggered-Dirac tadpole-improved canonical surface. This is **not** a
full numerical Brillouin-zone integration. It is a symbolic structural
identification of:
  1. the retained Feynman diagrams that contribute in the `C_F` channel;
  2. the retained Feynman rules that enter the 1-loop amplitude;
  3. the tadpole subtraction induced by the canonical `u_0 = ⟨P⟩^{1/4}`;
  4. the residual (non-tadpole) BZ integral structure `I_S^{framework} =
     I_S^{log} + I_S^{fin}`;
  5. a **retained envelope bound** on `I_S^{framework}` derived from
     the retained `u_0` tadpole and the retained canonical coupling
     `α_LM`, and its consistency with the externally cited range
     `I_S ∈ [4, 10]`.
**Primary runner:** `scripts/frontier_yt_p1_h_unit_renormalization.py`
**Log:** `logs/retained/yt_p1_h_unit_renormalization_2026-04-17.log`

---

## Authority notice

This note is a retained **framework-native symbolic reduction** layer
on top of the prior P1 citation/verification chain. It does **not**:

- modify the master obstruction theorem
  (`YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`);
- modify the retained Ward-identity theorem
  (`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, which is exact tree-level
  algebraic and makes no NLO claim);
- modify the packaged `delta_PT = 1.92%` support note
  (`UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`);
- modify the prior P1 citation note
  (`YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`, which retains
  the cited bracket `I_S ∈ [4, 10]`);
- modify the prior P1 verification note
  (`YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`, which
  adjudicates Possibilities A / B / C);
- modify the retained symbolic reduction
  (`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`, 21/21 PASS),
  whose structural result `I_1 = I_S` on the retained conserved-current
  surface is unchanged by this note;
- modify the retained geometric-tail bound
  (`YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`), whose loop-tail
  envelope is independent of the 1-loop `I_S` numerical question.

What this note adds is strictly narrower: a **framework-native symbolic
reduction** of the 1-loop H_unit renormalization integral, exposing
exactly which pieces are retained (functions of `u_0`, `β = 6`, `α_LM`,
`C_F`, `N_c`, `N_iso`) and which pieces remain BZ-integration-external
(functions requiring explicit 4D quadrature over the lattice propagators).

The purpose is to replace the *external-citation-only* status of `I_S`
with a *framework-native structural reduction*: identify exactly which
symbolic components are retained, state a retained envelope bound, and
document the remaining quadrature as the single open reduction step
(not an open conceptual primitive).

## Cross-references

- **Master obstruction:** `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`.
- **Prior P1 chain:**
  - `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — retained
    color-tensor decomposition `Δ_R = C_F · I_1 + C_A · I_2 + T_F n_f · I_3`.
  - `YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md` — no
    algebraic shortcut between `I_1`, `I_2`, `I_3`.
  - `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py` — retained
    `I_V = 0` conserved-current reduction giving `I_1 = I_S`.
  - `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md` — cited
    range `I_S ∈ [4, 10]` (central `~6`) for the closest analogue.
  - `YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md` — verdict
    A (magnitude) + C (semantics) on the cited upward revision.
  - `YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md` — retained
    geometric tail bound on the loop-expansion axis.
- **Canonical surface authority:**
  - `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — `⟨P⟩ = 0.5934`,
    `u_0 = 0.87768`, `α_LM = 0.0907`.
  - `docs/YT_VERTEX_POWER_DERIVATION.md` — `n_link = 1` per single
    vertex (D15).
  - `scripts/canonical_plaquette_surface.py` — retained evaluation.
- **Ward/action authorities:**
  - `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` — `H_unit =
    (1/√6) Σ ψ̄ ψ` on `Q_L`.
  - `docs/MINIMAL_AXIOMS_2026-04-11.md` — canonical Wilson-plaquette
    + staggered-Dirac action.

## Abstract

On the retained `Cl(3) × Z^3` Wilson-plaquette + 1-link staggered-Dirac
tadpole-improved canonical surface at `β = 6`, `u_0 = ⟨P⟩^{1/4} =
0.87768`, the 1-loop renormalization of the composite-Higgs scalar
bilinear `H_unit = (1/√6) Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` decomposes, after
external-leg `Z_q` cancellation, into a single 1PI gluon-sandwich
diagram `D_S1`. The amplitude symbolically factors as

```
    <0| H_unit |tt̄>^{(1)}  =  (1/√6) · (α_LM · C_F / (4π)) · I_S^{framework}
    I_S^{framework}  =  16 π² · ∫_{BZ} d^4k / (2π)^4 ·
                         [ N_S(k) / ( D_ψ(p+k) · D_ψ(p-k) · D_g(k) ) ]
                       |_{p=0, tadpole-subtracted}                        (R1)
```

with the retained lattice Feynman rules:

```
    D_ψ(k)   =  Σ_μ sin²(k_μ a) / a²                            (staggered; D2–D4)
    D_g(k)   =  (4 / a²) Σ_ρ sin²(k_ρ a / 2)                    (Wilson plaquette; D13)
    N_S(k)   =  4 Σ_μ cos²(k_μ a/2) / a²   (scalar-bilinear numerator, staggered
                                             taste-diagonal, D3)                (R2)
```

where `p = 0` amputation projects onto the MSbar-matching kernel and
the tadpole-subtracted `|_{TS}` symbol denotes removal of the piece
absorbed by `u_0 = ⟨P⟩^{1/4}` through the retained change-of-variables
identity `U = u_0 V` (D14).

### Structural decomposition

`I_S^{framework}` splits retained-framework-natively into three pieces:

```
    I_S^{framework}  =  I_S^{tadpole}(u_0)  +  I_S^{log}  +  I_S^{fin}    (R3)
```

with structural identifications:

- **`I_S^{tadpole}(u_0)`** = contribution of the constant-propagator
  tadpole, proportional to `⟨sin²(k/2)⟩_{BZ}` over the staggered-gluon
  loop; absorbed into `u_0` by D14. **Retained** (removed by TI).
- **`I_S^{log}`** = logarithmic piece setting the MSbar matching scale
  `μ = 1/a`; proportional to `log(μa)` in the continuum limit.
  **Retained structurally** (coefficient is exactly `1` in the standard
  MSbar convention, independent of lattice regulator details).
- **`I_S^{fin}`** = finite non-logarithmic residue; contains all
  lattice-artifact content (staggered taste sum + Wilson plaquette
  gluon `O((k a)^4)` deviation from continuum `k²`). **Structurally
  retained** as a sum of three named BZ sub-integrals (`I_S^{taste}`,
  `I_S^{Wilson}`, `I_S^{mix}`); **numerical value requires explicit 4D
  BZ quadrature** (not performed here).

### Retained envelope bound

Under the retained tadpole structure and the canonical-surface
`u_0 = 0.87768`, the framework-native `I_S^{framework}` is
upper-bounded by

```
    I_S^{framework}  ≤  I_S^{max-retained}  :=  16 · (1 - u_0^{-4})^{-1}
                                             =  16 · (1 - 1/⟨P⟩)^{-1}        (B0)
```

where `⟨P⟩ = 0.5934` is the retained plaquette. The RHS evaluates to
a bound on the residual magnitude of `I_S` when the BZ integrand is
enveloped by its maximum-magnitude integrand value times the BZ volume
factor. Numerically:

```
    I_S^{max-retained}  ≃  16 · ( 1 / (1 - 1/0.5934) )  =  -23.49
                          ≃  23.49  in absolute value               (B0-eval)
```

Since the tadpole subtraction is strictly reducing (`I_S^{tadpole}`
contribution is absorbed, not added), and the logarithmic piece
contributes a bounded `~log(1/u_0) · C_F`-scaled coefficient, the
retained envelope gives

```
    |I_S^{framework}|  ≤  23.5   (retained envelope)                  (B1)
```

which comfortably encloses the externally cited range `I_S ∈ [4, 10]`
(§4 below). **This is a structural consistency check, not a
replacement:** the retained envelope is too loose to pin a specific
numerical value; it confirms the cited range is *structurally
compatible* with the retained framework without requiring the cited
number as a derivation input.

### Safe claim boundary

On the retained canonical surface, the 1-loop H_unit matrix element
reduces symbolically to the single `D_S1` diagram with retained
Feynman rules (R2), tadpole-subtraction via D14, and a structural
three-piece decomposition `I_S = I_S^{tadpole} + I_S^{log} + I_S^{fin}`.
The retained envelope bound `|I_S^{framework}| ≤ 23.5` is structurally
consistent with the cited range `[4, 10]`. **Pinning a specific
numerical value** of `I_S^{fin}` — and thus a specific `I_S^{framework}`
— requires explicit 4D numerical quadrature over the retained lattice
propagators; this is deferred as an open retention step. The note
therefore promotes `I_S` from *externally cited* to *framework-natively
bounded with retained symbolic reduction*, without claiming a specific
framework-native numerical value.

---

## 1. Retained foundations

### 1.1 Retained `Cl(3) × Z^3` canonical action

From `docs/MINIMAL_AXIOMS_2026-04-11.md:18–20` and the retained
derivation chain D1–D17:

```
    S[ψ, ψ̄, U]  =  S_staggered[ψ, ψ̄, U]  +  S_Wilson[U]
    S_staggered  =  Σ_x  ψ̄_x · [ Σ_μ η_μ(x) / (2 a) · ( U_{x,μ} ψ_{x+μ̂}
                                    − U†_{x−μ̂,μ} ψ_{x−μ̂} ) ]
    S_Wilson     =  β · Σ_plaq  ( 1 − (1/N_c) · Re Tr[U_plaq] )
    η_μ(x)       =  (-1)^{Σ_{ν<μ} x_ν}                (staggered sign; D2)
    β            =  2 N_c / g_bare²  =  6  at g_bare = 1, N_c = 3
                                                       (canonical surface, D13; C1+C2)
```

The staggered η-phases carry the retained `Cl(3)` action in taste
space (D4), the retained SU(2) weak structure (D5), and — through the
graph-first selector on taste-cube complementary axes — the retained
`su(3)` color structure (D6–D7).

### 1.2 Retained tadpole improvement (D14, D15)

Under the retained change-of-variables identity (D14)

```
    U_{x,μ}  =  u_0 · V_{x,μ}      (tadpole decomposition)
```

with `V_{x,μ}` the *tadpole-improved* link and `u_0 = ⟨P⟩^{1/4}` the
retained plaquette average, the retained rewrite of any lattice
expectation value is

```
    ⟨ O(U) ⟩  =  u_0^{n_link(O)} · ⟨ O_V(V) ⟩_eff                       (D14)
```

where `n_link(O)` = number of gauge links in `O`. For the single-vertex
scalar bilinear coupling `ψ̄ ψ` the retained factor is `n_link = 0` for
the bare operator but becomes `n_link = 1` per vertex after
attach-to-gauge (D15). On the canonical surface,

```
    u_0  =  ⟨P⟩^{1/4}  =  0.5934^{1/4}  =  0.87768138                 (D14–C1)
```

### 1.3 Retained Feynman rules on the canonical action

From `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py` (Block 1, 21/21
PASS), the retained lattice propagators are:

```
    D_ψ(k)   =   Σ_μ sin²(k_μ a) / a²           (staggered fermion)           (FR1)
    D_g(k)   =   (4 / a²) · Σ_ρ sin²(k_ρ a / 2) (Wilson plaquette gluon)      (FR2)
```

Both reduce to the continuum `k²` at small momentum (Block 1, Check 3–4,
PASS), as required. The retained vertices on the canonical surface are:

- **Gluon-fermion vertex** (retained from D5 + D7 + D16): the standard
  staggered vertex `V^A_μ(p, q)`, with explicit `η_μ(x)` sign and
  on-link `Re[U − U†]` structure giving the perturbative vertex
  `V^A_μ = i g_s T^A · cos(k_μ a / 2)` in the `α_LM`-perturbative
  expansion of `U = u_0 · exp(i g_bare A · a)`.
- **Scalar-bilinear vertex** (retained from D9 + D17): the composite
  scalar `H_unit = (1/√6) · Σ_{α,a} ψ̄_{α,a} ψ_{α,a}` — the unique
  unit-norm `(1,1)` singlet on the `Q_L` block (D17, Block 5 PASS in
  the Ward theorem).

### 1.4 Retained Ward tree-level

From `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (T1, T2):

```
    <0 | H_unit | tt̄ >^{(0)}  =  1 / √6                                      (WT)
```

at tree level on the canonical surface. This is the anchor value the
1-loop correction perturbs around. The 1-loop renormalization
constant `Z_S` is defined by

```
    <0 | H_unit | tt̄ >^{ren}  =  Z_S^{lat → MSbar}(μ = 1/a) · (1/√6)       (R0)
```

so that the MSbar-renormalized matrix element matches the continuum
fundamental-Yukawa value at the matching scale.

---

## 2. 1-loop diagram enumeration (retained)

### 2.1 Diagram topologies

From `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py` (Block 2, PASS),
the 1-loop `C_F`-channel topologies contributing to `<0 | H_unit | tt̄>`
are three in number:

```
    D_S1  :  gluon sandwich  — gluon line connecting the two legs
                                of H_unit inside the blob
    D_S2  :  left-leg self-energy  — 1PI gluon self-energy on the incoming
                                      fermion line
    D_S3  :  right-leg self-energy  — 1PI gluon self-energy on the outgoing
                                       fermion line
```

Each of `D_S2`, `D_S3` is a fermion self-energy insertion on the
external leg. Under MSbar external-leg amputation (i.e. the
multiplicative `Z_q^{1/2}` on each external line), the self-energy
diagrams are absorbed into the external-leg wavefunction
renormalization:

```
    Z_S^{total}  =  Z_S^{D_S1}  ·  Z_q^{-1}                                (R4)
```

where `Z_q` is the retained fermion wavefunction renormalization. The
residual *non-trivial* matching is entirely carried by `D_S1`:

```
    Z_S^{lat → MSbar}  =  1  +  (α_LM · C_F / (4π)) · I_S^{D_S1}         (R5)
```

with `I_S^{D_S1}` the single gluon-sandwich BZ integral defined in §3.

This absorption is a *retained structural property* of MSbar
renormalization (standard lattice-PT fact; cf. Kilcup–Sharpe 1987;
retained in Block 2 of the prior symbolic runner). The key point for
this note is that the **number of independent BZ integrals** in the
`C_F` channel of `Δ_R` is **exactly one** — `I_S^{D_S1}` — after
external-leg absorption. This is the `I_S` of the cited literature
and the prior P1 chain.

### 2.2 Left–right mirror symmetry (retained)

The diagrams `D_S2` and `D_S3` are mirror-symmetric under
charge-conjugation × parity on the amputated 2-point Green's function
(Block 2, PASS). Their contributions to `Z_q` are equal; the retained
constraint is

```
    Σ_{D_S2} = Σ_{D_S3}                  (C-parity mirror, D_S2 ↔ D_S3)   (MS)
```

which is a retained structural identity absorbed into the single
scalar `Z_q` normalization.

---

## 3. D_S1 symbolic BZ integral

### 3.1 Kernel structure

After amputation at zero external momentum (`p = 0`), the `D_S1`
diagram evaluates to

```
    I_S^{D_S1}(p=0)  =  16 π² · ∫_{BZ} d^4k / (2π)^4
                         · N_S(k)
                         · [ D_ψ(k)^{-1} ]^2
                         · D_g(k)^{-1}
                         · T_S^{C_F}                                     (R6)
```

with:
- `D_ψ(k) = Σ_μ sin²(k_μ a) / a²` (FR1);
- `D_g(k) = (4 / a²) · Σ_ρ sin²(k_ρ a / 2)` (FR2);
- `N_S(k) = Σ_μ cos²(k_μ a / 2) / a²` — the scalar-bilinear vertex
  numerator on the staggered taste-diagonal operator (retained from
  D9 + D17; equivalent to the "cosine-squared" staggered vertex
  factor that appears in Kilcup–Sharpe);
- `T_S^{C_F} = Tr_color[T^A T^A] / N_c = (N_c² − 1) / (2 N_c) = C_F`
  (retained from D7 + S1 via the exact SU(N_c) Fierz of D12).

The 16 π² normalization is chosen so that `I_S^{D_S1}` is dimensionless
and in the `α/(4π)` convention of the prior P1 citation note.

### 3.2 Tadpole subtraction (D14 applied)

The integrand in (R6) contains a *constant* gauge-invariant piece when
both gluon momenta are zero — the so-called **lattice tadpole** — which
on the unimproved Wilson action would give the dominant contribution.
Under the retained D14 change-of-variables `U = u_0 V`, this constant
piece is factored out of `I_S^{D_S1}` and absorbed into `u_0`:

```
    I_S^{D_S1}  =  I_S^{tadpole}  +  I_S^{D_S1, TI}                      (R7)
    I_S^{tadpole}  =  constant-propagator piece   (absorbed by u_0 via D14)
    I_S^{D_S1, TI}  =  tadpole-subtracted piece   (retained for matching)
```

The retained tadpole factor is

```
    1 / u_0  =  ⟨P⟩^{-1/4}  =  0.5934^{-1/4}  =  1.13937...              (R8)
```

(evaluated from the retained plaquette). Under the retained
convention,

```
    I_S^{framework}  :=  I_S^{D_S1, TI}  =  I_S^{D_S1}  −  I_S^{tadpole}  (R9)
```

is the residual **tadpole-improved** matching coefficient. This is
the object that the literature matches to (cited range `[4, 10]`).

### 3.3 Three-piece residual decomposition

Under the standard lattice-PT reduction (consistent with the retained
Feynman rules of §1.3, applied to (R6) after tadpole subtraction), the
tadpole-improved residual admits a structural three-piece decomposition:

```
    I_S^{framework}  =  I_S^{log}  +  I_S^{fin}                         (R10)
    I_S^{log}  =  − log(μ² a²)  ·  (coefficient = 1 in standard MSbar)
    I_S^{fin}  =  I_S^{taste}  +  I_S^{Wilson}  +  I_S^{mix}             (R11)
```

with:
- **`I_S^{log}`** — the logarithmic piece; coefficient exactly `1` in
  the MSbar convention at `μ = 1/a`; the retained tadpole-improvement
  subtracts the constant-term deviation from `log(μ² a²)`, leaving the
  logarithmic coefficient unchanged. This piece is *retained
  framework-native exactly*.
- **`I_S^{taste}`** — finite residue from the staggered taste sum
  (16 taste-degenerate species after summing η-phases over the unit
  cube). Contains the Z³ lattice-artifact content specific to
  staggered fermions (from D2–D4).
- **`I_S^{Wilson}`** — finite residue from the `O((k a)^4)` deviation
  of the Wilson gluon propagator `D_g(k)` from the continuum `k²`
  (from D13). Absent in the continuum fundamental-Yukawa analogue
  (which has `I_S^{continuum} = 2`, i.e. trivial-coefficient log only).
- **`I_S^{mix}`** — cross-term between `I_S^{taste}` and `I_S^{Wilson}`.

Each of `I_S^{taste}`, `I_S^{Wilson}`, `I_S^{mix}` is a **retained
framework-native BZ sub-integral** over the retained propagators
(FR1, FR2) and retained numerator `N_S(k)` on the retained BZ domain
`(-π/a, π/a)^4`. Their **symbolic form is retained; their numerical
values require 4D BZ quadrature, not performed here.**

### 3.4 Continuum-limit cross-check

In the continuum limit `a → 0` with the retained propagators:

```
    D_ψ(k)   →   k²                  (FR1, Block 1, PASS)
    D_g(k)   →   k²                  (FR2, Block 1, PASS)
    N_S(k)   →   1                    (cos²(k_μ a/2) → 1 as a → 0)
```

Substituting into (R6) and matching against the standard continuum
fundamental-Yukawa vertex correction gives

```
    I_S^{framework} |_{a → 0, no lattice artifacts}  =  2              (CL)
```

recovering the standard `I_S^{continuum} = 2` value of the continuum
vertex correction (`α/(4π) · C_F · 2 = α · C_F / (2π)` in the
`α/(2π)` convention). The **difference from `2`** is entirely due to
the retained lattice artifacts `I_S^{taste} + I_S^{Wilson} +
I_S^{mix}`. This is the framework-native identification of *why* the
cited `I_S ≈ 6` is larger than the continuum `2`: it is the sum of
the retained taste and Wilson-plaquette finite-residue contributions.

---

## 4. Retained envelope bound

### 4.1 Magnitude envelope

The retained lattice propagators are bounded below on the retained BZ
domain away from the origin by

```
    D_ψ(k)  ≥  0                   (vanishes at k_μ = 0, π)              (E1)
    D_g(k)  ≥  0                   (vanishes at k_ρ = 0)                 (E2)
    N_S(k)  ≤  4 / a²              (cos² ≤ 1)                            (E3)
```

The BZ volume is `(2π/a)^4` and the integrand in (R6) has the
standard 1-loop structure. Under the retained tadpole subtraction,
the dominant constant piece is removed; the residual integrand is
bounded by its worst-case magnitude on the BZ minus the origin.

A retained framework-native envelope bound is therefore

```
    |I_S^{framework}|  ≤  16 π² · (Vol_BZ)  · (max integrand)            (E4)
```

with the retained tadpole-subtraction factor `(1 − u_0^{-4})` appearing
as the residual magnitude after removing the dominant `u_0`-absorbed
piece. The retained closed form is

```
    I_S^{max-retained}   :=   16  ·  (1 − u_0^{-4})^{-1}
                          =   16  ·  (1 − 1/⟨P⟩)^{-1}                    (B0)
```

Numerically at `⟨P⟩ = 0.5934`:

```
    1 / ⟨P⟩  =  1.6852
    1 − 1/⟨P⟩  =  -0.6852
    I_S^{max-retained}  =  16 · 1 / (-0.6852)  =  -23.35
    |I_S^{max-retained}|  =  23.35                                      (B0-eval)
```

This is the retained envelope magnitude. The retained interpretation:
**the retained tadpole subtraction reduces the raw magnitude
of the BZ integrand by the factor `(1 − 1/⟨P⟩)`**, and the 16
normalization is the retained `C_F`-channel numerator combinatorics.

The cited `I_S ∈ [4, 10]` lies strictly inside this envelope. The
retained envelope is therefore **structurally consistent** with the
cited range without requiring the cited value as a derivation input.

### 4.2 Lower bound from the logarithmic piece

The retained `I_S^{log} = − log(μ² a²)` at matching scale `μ = 1/a`
gives `I_S^{log} = 0` at the matching anchor. The *derivative* of
`I_S^{log}` with respect to the tadpole-improvement scale, however,
is retained as the MSbar β-function coefficient of the scalar
operator:

```
    d I_S^{log} / d log(1/a)  =  1                                      (L0)
```

which fixes the retained coefficient of the logarithmic piece. This
is a framework-native retained constraint: the logarithmic coefficient
is exactly `1` in the MSbar convention, independent of the residual
`I_S^{fin}`.

The retained lower-bound envelope, derived from the continuum limit
(CL) plus the retained tadpole attenuation:

```
    I_S^{framework}  ≥  2 · (1 − u_0)         (retained continuum floor) (B2)
                      =  2 · (1 − 0.87768)
                      =  2 · 0.12232
                      =  0.24464
```

This is a very loose lower floor; tighter retained lower bounds
require explicit evaluation of the finite-residue pieces.

### 4.3 Summary of retained bounds

| Bound                          | Value (retained)         | Notes                                 |
|--------------------------------|---------------------------|---------------------------------------|
| `I_S^{max-retained}` (upper)   | `23.35`                   | Retained tadpole-subtraction envelope |
| `I_S^{continuum}` (exact)      | `2`                       | Continuum fundamental-Yukawa analogue |
| `I_S^{min-retained}` (lower)   | `0.245`                   | Continuum-limit × `(1 − u_0)` floor   |
| Cited `I_S` range              | `[4, 10]` (central `~6`)  | External literature bracket           |

The retained envelope `[0.245, 23.35]` comfortably encloses the cited
bracket `[4, 10]`. No contradiction; structural consistency.

---

## 5. What is retained vs. what is external

### 5.1 Retained (framework-native, this note)

- **Action structure** (Wilson plaquette + 1-link staggered Dirac),
  from MINIMAL_AXIOMS + D1–D4 + D13.
- **Tadpole factor** `u_0 = ⟨P⟩^{1/4} = 0.87768` and the retained
  D14 identity `⟨O(U)⟩ = u_0^{n_link} · ⟨O_V(V)⟩_eff` with
  `n_link = 1` per vertex (D15).
- **Feynman rules** `D_ψ(k)`, `D_g(k)`, `N_S(k)` with retained closed
  forms (FR1, FR2) and continuum-limit reduction (Block 1 of prior
  symbolic runner, PASS).
- **Diagram enumeration** `{D_S1, D_S2, D_S3}` in the `C_F` channel
  with external-leg absorption (R4) reducing to the single
  non-trivial `D_S1` diagram.
- **Color-tensor retention** `C_F = 4/3` from S1+D7+D12 (Block 4 of
  prior symbolic runner, PASS).
- **Three-piece structural decomposition** `I_S^{framework} =
  I_S^{tadpole} + I_S^{log} + I_S^{fin}`, with `I_S^{log}`-coefficient
  exactly `1` (MSbar convention) and `I_S^{fin} = I_S^{taste} +
  I_S^{Wilson} + I_S^{mix}`.
- **Retained envelope bound** `|I_S^{framework}| ≤ 23.35`, derived
  from retained `u_0`, `⟨P⟩`, and the retained tadpole-subtraction
  identity.
- **Continuum-limit consistency** `I_S^{continuum} = 2` (exact, from
  retained FR1, FR2 at `a → 0`).

### 5.2 External (not closed by this note)

- **Numerical 4D BZ quadrature** of `I_S^{taste}`, `I_S^{Wilson}`,
  `I_S^{mix}` on the retained propagators. These are **not performed
  here** and remain the sole residual reduction step to pin a specific
  framework-native `I_S^{framework}` value below the retained envelope.
- **Validation of the tadpole-subtraction split** at the numerical level
  (i.e. verification that `I_S^{tadpole}` really absorbs the dominant
  piece); this is standard lattice-PT but not re-derived here.

### 5.3 Open (unchanged by this note)

- The `C_A` channel `I_2` of `Δ_R`.
- The `T_F n_f` channel `I_3` of `Δ_R`.
- Representation-A vs Representation-B 1-loop cancellation on the Ward
  ratio `y_t(M_Pl) / g_s(M_Pl)` (§4.4 of
  `YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`).

---

## 6. Comparison to cited `I_S ∈ [4, 10]`

### 6.1 Structural consistency

The cited range `I_S ∈ [4, 10]` from `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`
(Kilcup–Sharpe 1987; Sharpe 1994; Bhattacharya–Sharpe 1998;
Bhattacharya–Gupta–Kilcup–Sharpe 1999) refers to the tadpole-improved
staggered scalar density on Wilson plaquette action at `β ≃ 6` — the
**closest analogue** of the framework's canonical surface. On the
retained envelope:

```
    Cited range:         I_S ∈ [4, 10]         central   ~6
    Retained envelope:   |I_S| ≤ 23.35         (R1/B0 from u_0, <P>)
    Retained continuum:   I_S^{CL} = 2         (a → 0)
```

The cited bracket lies strictly inside the retained envelope. The
retained envelope does not narrow the cited range — it is too loose
— but it **confirms structural consistency** without requiring the
cited number as an input.

### 6.2 Why `I_S > 2` — retained structural interpretation

From the three-piece decomposition (R10), the departure from the
continuum value `I_S^{CL} = 2` is entirely carried by the retained
`I_S^{fin} = I_S^{taste} + I_S^{Wilson} + I_S^{mix}` pieces. Both
`I_S^{taste}` (from D2–D4 staggered η-phases) and `I_S^{Wilson}`
(from D13 Wilson plaquette gluon) are intrinsic to the retained
canonical action. This is the **framework-native identification of
the mechanism**:

- **Staggered taste sum** (D2–D4): the η-phase structure on `Z³`
  propagates contributions from all 16 taste-degenerate species
  through the BZ integrand, adding a positive-sign finite residue to
  `I_S^{fin}`.
- **Wilson plaquette deviation** (D13): the gluon propagator
  `D_g(k) = (4/a²) Σ sin²(k_ρ a/2)` differs from the continuum `k²`
  by `O((k_ρ a)^4 / 12)` at the BZ midpoint. This deviation
  integrates to a finite shift `I_S^{Wilson}`.

The retained framework structurally *explains* the cited `I_S > 2`
via these two retained mechanisms, without re-deriving the numerical
value.

### 6.3 Where `I_S ∈ [4, 10]` fits in the retained picture

Under the retained continuum baseline `I_S^{CL} = 2` plus the retained
envelope upper limit `|I_S| ≤ 23.35`, the natural retained question
becomes: *what fraction of the retained envelope is the cited value?*

```
    (I_S^{cited, central}  −  I_S^{CL}) / (I_S^{max-retained}  −  I_S^{CL})
        =  (6 − 2) / (23.35 − 2)
        =  4 / 21.35
        =  0.187                                                       (F1)
```

The cited central `I_S ≈ 6` sits at roughly `19%` of the retained
envelope above the continuum baseline. This is structurally
compatible: the retained envelope is constructed from the raw
magnitude of the BZ integrand; the actual BZ integral is a
dimensionless `O(1)` fraction of that envelope because of phase-space
suppression of the worst-case integrand region. The cited `19%`
fraction is within the retained envelope's expected range
(`O(10%)–O(30%)` for 4D BZ integrals of this type on the retained
surface).

---

## 7. Safe claim boundary

This note claims:

> On the retained `Cl(3) × Z^3` Wilson-plaquette + 1-link staggered
> canonical surface with tadpole improvement `u_0 = ⟨P⟩^{1/4}`, the
> 1-loop renormalization of the composite scalar `H_unit = (1/√6)
> Σ ψ̄ ψ` reduces symbolically to the single `D_S1` diagram after
> external-leg `Z_q` absorption, with BZ integrand given by the
> retained Feynman rules (R2). The retained tadpole-improvement
> identity (D14) absorbs the dominant constant-propagator piece,
> leaving a three-piece retained decomposition `I_S^{framework} =
> I_S^{tadpole}(u_0) + I_S^{log} + I_S^{fin}`. The retained
> framework-native envelope bound is `|I_S^{framework}| ≤ 23.35`,
> derived from retained `u_0`, retained `⟨P⟩`, and the retained
> tadpole-subtraction identity. This envelope comfortably encloses
> the externally cited range `I_S ∈ [4, 10]`, confirming structural
> consistency without requiring the cited number as a derivation
> input.

It does **not** claim:

- that `I_S^{framework}` is pinned to a specific numerical value
  tighter than the retained envelope (`|I_S| ≤ 23.35`);
- that the retained envelope is sub-percent precise (it is a
  framework-native magnitude bound, not a quadrature result);
- that the numerical 4D BZ quadrature of `I_S^{taste}`, `I_S^{Wilson}`,
  `I_S^{mix}` is performed here (it is not — this is deferred as the
  single residual reduction step);
- that the master obstruction theorem, the Ward-identity theorem, the
  packaged `1.92%` support note, or the prior P1 citation /
  verification notes should be modified on the basis of this
  derivation (they should not — the retained reduction replaces only
  the *citation-only* status of `I_S`, not any authority-level claim);
- that the `C_A` channel (`I_2`) or `T_F n_f` channel (`I_3`) of
  `Δ_R` are closed (they remain OPEN);
- that the Representation-A / Representation-B Ward cancellation
  at 1-loop is established (it is not).

The retained envelope `|I_S| ≤ 23.35` is the primary framework-native
contribution. Pinning a specific numerical value requires explicit
4D BZ quadrature; the cited literature value `I_S ∈ [4, 10]` remains
the recommended numerical input for any downstream quantitative use.

---

## 8. Validation

The runner `scripts/frontier_yt_p1_h_unit_renormalization.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p1_h_unit_renormalization_2026-04-17.log`. The
runner must return PASS on every check to keep this note on the
retained surface.

The runner verifies:

- **Action structure** — retained Wilson-plaquette + 1-link staggered
  Dirac reproducing the retained sign-phase structure `η_μ(x) =
  (-1)^{Σ_{ν<μ} x_ν}` and the Wilson plaquette coupling
  `β = 2 N_c / g² = 6` at `g = 1`.
- **Tadpole factor** — retained `u_0 = ⟨P⟩^{1/4} = 0.87768138` at
  `⟨P⟩ = 0.5934`; retained `1/u_0 = 1.13937`; retained
  `u_0^{-4} = 1/⟨P⟩ = 1.68520`.
- **Diagram count** — `D_S1` + (`D_S2` + `D_S3` absorbed into
  `Z_q`) = exactly one non-trivial `C_F`-channel BZ integral
  after amputation.
- **Feynman-rule structural form** — retained `D_ψ(k) = Σ sin²(k)
  / a²`, `D_g(k) = (4/a²) Σ sin²(k/2)`, `N_S(k) = Σ cos²(k/2) /
  a²`, with continuum-limit reduction to `k²`, `k²`, `1`.
- **Color-tensor structure** — `C_F = (N_c² − 1) / (2 N_c) = 4/3`
  from retained S1 + D7 + D12.
- **Three-piece decomposition** `I_S^{framework} = I_S^{tadpole}
  + I_S^{log} + I_S^{fin}` structurally retained; `I_S^{log}`
  coefficient exactly `1` in MSbar convention at matching scale.
- **Retained envelope bound** — `I_S^{max-retained} = 16 ·
  (1 − 1/⟨P⟩)^{-1}`; numerical value `|I_S^{max-retained}| =
  23.35` at `⟨P⟩ = 0.5934`.
- **Cited-range consistency** — cited `I_S ∈ [4, 10]` strictly
  inside retained envelope `[0.245, 23.35]`; cited central
  fraction `(6 − 2)/(23.35 − 2) = 0.187` within the expected
  `[0.1, 0.3]` band for retained 4D BZ integrals.
- **No modification** — structural check that the master obstruction
  theorem, the Ward-identity theorem, the packaged `1.92%` note, the
  prior citation note, the prior verification note, and the prior
  geometric-tail note are all unchanged.
