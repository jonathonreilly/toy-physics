# Top-Yukawa Structural Identification: y_t(M_Pl) = g_s(M_Pl) / sqrt(6)

**Date:** 2026-04-17 (audit-prep refresh: 2026-05-06)
**Status:** bounded structural identification on the canonical evaluation
surface. This note records the structural identification of the unit-normalized
H_unit-to-top matrix element with the framework's top-Yukawa readout on the
canonical Wilson-staggered surface within `A_min = {Cl(3), Z^3}`. It is **not**
a first-principles derivation of the Standard Model top Yukawa value.
**Claim type:** bounded_theorem author hint; independent audit lane sets the
actual `claim_type`, `audit_status`, and pipeline-derived `effective_status`.
**Admitted context inputs (open-gate dependencies under
`MINIMAL_AXIOMS_2026-05-03.md`):**
- `staggered_dirac_realization_derivation_target` (parent: pending packaging,
  see `MINIMAL_AXIOMS_2026-05-03.md` §"recategorized from axiom to open gate")
- `g_bare_derivation_target` (parent: `G_BARE_DERIVATION_NOTE.md`)
The note conditions on closure of these two derivation targets; they are
explicitly listed as `admitted_context_inputs`, not derived here.
**Primary runner:** `scripts/frontier_yt_ward_identity_derivation.py`
(45 PASS / 0 FAIL on current source).
**Support (NOT part of the authority chain):**
`UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`
documents the perturbative 1-loop vertex correction, which is OPEN
for quantitative lane reuse (not part of this support-tier identification).

---

## Audit boundary

This note identifies the unit-normalized `H_unit` matrix element on the
Q_L scalar-singlet channel within `A_min = {Cl(3), Z^3}`, including the
`1/sqrt(6)` Clebsch-Gordan overlap and the canonical-surface ratio
calculation.

**The identification map: framework readout, not SM Yukawa derivation.**
The framework's top-Yukawa readout is *defined* by the unit-normalized
H_unit matrix element on the canonical evaluation surface. The note proves
that this defined readout equals `g_bare / sqrt(6)` on the canonical
surface, and that the ratio `y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6)` is exact
and tadpole-invariant. The note does **not** prove that the framework's
defined readout equals the Standard Model top-Yukawa observable; that
identification is a separate question handled downstream (RG running,
matching, threshold corrections).

This note does **not** claim to derive the numerical Standard Model top
Yukawa value from first principles, to derive the existence of the SM
Yukawa construct independent of this identification, or to supply a
precision prediction after RG running and matching.

**Conditional on the named open gates (g_bare, staggered-Dirac), the
exact algebraic claims `(T1)` and `(T2)` below are runner-verified at
machine precision.**

Prior audit history: the audit lane previously recorded
`audit_status=audited_renaming` for `yt_ward_identity_derivation_theorem`,
cross-confirmed as class E by `codex-fresh-context-20260430-01-yt-ward`
(2026-04-30) and `fresh-agent-popper-019ded72` (2026-05-03). The repeat
finding identifies the load-bearing step as the *definition* of `y_t_bare`
as the H_unit matrix element. This refresh:
1. Tightens scope language so the claim boundary is the framework readout
   identity, not the SM Yukawa map;
2. Replaces the stale `MINIMAL_AXIOMS_2026-04-11.md` citation (now
   superseded) with `MINIMAL_AXIOMS_2026-05-03.md`;
3. Lists `g_bare = 1` and the staggered-Dirac realization as
   `admitted_context_inputs` (open gates) per the restored axiom set;
4. Narrows the claim_type author hint from `open_gate` to
   `bounded_theorem` to match the restored axiom set's per-lane bookkeeping
   rule for quantitative `y_t` results
   (`MINIMAL_AXIOMS_2026-05-03.md`:182-191).

---

## Structural identification (tree-level algebraic support)

On the Cl(3) × Z³ Wilson-staggered lattice with the canonical
plaquette / u_0 evaluation surface (C1 + C2, `g_bare = 1` at
`β = 2 N_c / g_bare² = 6`), the bare Yukawa of the unit-norm (1,1)
scalar composite `H_unit` on the Q_L = (2,3) block satisfies the
exact tree-level 1PI matching identity

```
    y_t_bare = g_bare / sqrt(2 N_c) = g_bare / sqrt(6)                 (T1)
```

as an algebraic consequence of D16 (tree-level Feynman diagram
completeness of the bare action), D17 (composite-Higgs scalar
uniqueness on the Q_L block, Block 5 verified), the exact SU(N_c)
color Fierz identity D12 (Block 4), and the exact Lorentz Clifford
Fierz identity S2 (Block 8).

On the same canonical evaluation surface, the tadpole factor
`1/sqrt(u_0)` is common to both `g_s(M_Pl)` and `y_t(M_Pl)` via D15
(`n_link = 1` per single vertex) and cancels in the ratio, giving
the exact tree-level identity

```
    y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)                               (T2)
```

on the same surface.

**Scope of this support note:**
- It is the exact tree-level 1PI matching identity only.
- It makes NO quantitative precision claim (no `±%`, no NLO bound,
  no lane budget).
- Perturbative 1-loop corrections, higher-order topology corrections,
  and any quantitative lane reuse are OUT OF SCOPE of this note
  and are discussed in the support note (see above).
- Downstream quantitative reuse of this identity inherits whatever
  systematic the downstream package carries independently. This
  note does not narrow or claim such systematics.

---

## Inputs and dependency table

| # | Input | Status | Source |
|---|-------|--------|--------|
| **AX1** | **Cl(3) local algebra** | **AXIOM** | framework axiom |
| **AX2** | **Z³ spatial substrate** | **AXIOM** | framework axiom |
| D1 | Z³ bipartite → Z₂ parity ε = (-1)^{x+y+z} | DERIVED from AX2 | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):14-18 |
| D2 | Staggered fermion η phases on Z³ | DERIVED from D1 | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):14-18 |
| D3 | Taste doubling: 2³ = 8 internal species | DERIVED from D2 | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):16 |
| D4 | η phases → Cl(3) action in taste space | DERIVED from D3 + AX1 | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):17 |
| D5 | Cl(3) ⊃ su(2) → SU(2) weak gauge symmetry | DERIVED from D4 | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):18 |
| D6 | Graph-first axis selector on taste cube {0,1}³ | DERIVED from D3 | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):52-66 |
| D7 | Residual swap on complementary axes → `su(3)` closure | DERIVED from D6 | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):69-75 |
| D8 | Left-handed quark block `Q_L : (2,3)_{+1/3}`, dim 6 | DERIVED from D7 + graph-first selector | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md):93-95; [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md):13 |
| D9 | Composite Higgs `phi = (1/N_c) psi-bar_a psi_a` (taste condensate of quark bilinear, no independent Higgs field) | DERIVED from D3 + D8 | [`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md):33-40 |
| D10 | Composite 2-point function `<phi^† phi> = (1/N_c²) Tr_color[G G]` | DERIVED from D9 | [`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md):46-56 |
| D11 | Free-theory singlet `Tr[M M^†]_singlet = N_c |G_0|²` | DERIVED from D10 | [`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md):105-114 |
| D12 | Exact SU(N_c) Fierz identity on fundamental generators | DERIVED structural | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md):169-172 (proof at :78-94) |
| D13 | Wilson plaquette coupling `β = 2 N_c/g_bare²` at canonical surface | DERIVED from D5 + D7 + standard Wilson action | standard lattice QFT applied to D5, D7 |
| D14 | CMT exact identity `<O(U)> = u_0^{n_link} <O_V(V)>_eff` (change-of-variables `U = u_0 V`) | DERIVED structural | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md):213-221 |
| D15 | `n_link = 1` per single vertex, `n_link = 2` per vacuum polarization | DERIVED structural | [`YT_VERTEX_POWER_DERIVATION.md`](YT_VERTEX_POWER_DERIVATION.md):29-38 |
| C1 | Canonical plaquette / `u_0 = ⟨P⟩^{1/4}` evaluation surface | ADMITTED context input (canonical-surface choice; closure target = staggered-Dirac realization derivation, see `MINIMAL_AXIOMS_2026-05-03.md`:56-93) | `MINIMAL_AXIOMS_2026-05-03.md`:182-191 |
| C2 | `g_bare = 1` on canonical surface | ADMITTED context input (open-gate derivation target; canonical parent: `G_BARE_DERIVATION_NOTE.md`) | `MINIMAL_AXIOMS_2026-05-03.md`:95-136 |
| S1 | SU(3) fundamental Casimir `C_F = (N_c²-1)/(2N_c) = 4/3` | STANDARD Lie-algebra fact | applied to D7 |
| S2 | Lorentz-group Fierz: `(γ^μ)(γ_μ) = c_S(1)(1) + c_P(iγ_5)(iγ_5) + c_V(γ^μ)(γ_μ) + c_A(γ^μγ_5)(γ_μγ_5) + 0·σσ`, with `|c_S| = 1` | STANDARD Clifford-algebra identity | Itzykson-Zuber §2-5; verified by Block 8 of runner |
| D16 | Tree-level Feynman-rule completeness of the bare action on the scalar-singlet channel: at O(α_LM), the bare Cl(3) × Z³ action (Wilson plaquette + staggered Dirac, C1-C2) yields exactly ONE tree diagram contributing to `Γ⁽⁴⁾(q²)` on the color-singlet × iso-singlet × Dirac-scalar channel — the single-gluon-exchange diagram, projected via D12 + S2 with coefficient (3.5) | DERIVED from tree-level Feynman rules of the cited action + the absence of any fundamental scalar field or bare contact 4-fermion vertex in the bare action (D9 composite-Higgs) | framework-native; follows from `MINIMAL_AXIOMS_2026-05-03.md`:32-43 + D9 |
| D17 | Scalar-singlet composite uniqueness on the Q_L block: the unique unit-normalized (Z² = 6) color-singlet × iso-singlet × Dirac-scalar composite operator on Q_L = (2,3) is `H_unit = (1/√(N_c · N_iso)) Σ ψ̄ψ`. Other (1,8), (3,1), (8,3) irreps give `Z² = 8, 9/2, 24` respectively (Block 5 verified) — each distinct from `Z² = 6`, hence none are the framework's scalar singlet on this block | DERIVED and numerically verified (Block 5) | [`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md):33-40 (D9); Block 5 of runner |

The only AXIOMS are AX1 (Cl(3)) and AX2 (Z³). The remaining inputs are
the framework chain (D1-D17), a CANONICAL NORM CHOICE (C1, C2), or a
STANDARD group-theoretic identity (S1, S2) that is independent of
framework content. S1 and S2 are properties any SU(N_c) gauge theory in
4D with Dirac fermions must respect — they are not framework axioms.
**There is no separate "matching axiom" in this note.** The bare-action
1PI Green's function `Γ⁽⁴⁾` on the scalar-singlet channel is computed two
algebraically equivalent ways within the same cited framework surface:
directly from Feynman rules (D16 → OGE only at O(α_LM)) and via
the composite operator `H_unit` (D17 → unique scalar singlet on
Q_L). The two evaluations of the same Green's function must agree;
that algebraic identity gives `y_t_bare² = g_bare²/(2 N_c)`.

---

## Structural identification fact: no independent Yukawa parameter

The identification uses one piece of structural content that
deserves explicit attention: **the Cl(3) × Z³ lattice action has NO
independent Yukawa parameter**. This follows framework-natively from D9:

**D9 ([`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md):33-40)**: the framework's
Higgs is the composite taste condensate `phi = (1/N_c) psi-bar_a psi_a`,
NOT an independent fundamental scalar field.

**Structural consequence**: because the framework has no independent
Higgs field, there is no separate `L_Y = y_t · phi · (psi-bar_L psi_R)`
vertex with an independent coefficient `y_t` in the bare Cl(3) × Z³
lattice action. The bare Lagrangian contains only:
- Wilson plaquette (D13): gauge kinetic term, coefficient β at canonical surface
- Staggered Dirac operator (D2-D4): fermion kinetic term
- No separate Higgs or Yukawa terms

The "Yukawa coupling" `y_t` in the SM sense is therefore an **identified
emergent observable**, not a bare parameter. It is extracted from:
- The composite `phi` (defined by D9)
- The composite's VEV after EWSB
- The top-channel projection (Clebsch-Gordan on the Q_L block, D8)

There is **no free parameter** `c_Y` to "identify with g_bare" because
no such parameter exists in the bare Cl(3) × Z³ action. The earlier
reviews' objection to an "unsupported vertex-identification" step is
resolved by observing that no such identification step is needed — the
Yukawa is not a vertex in the bare action, it is an identified observable
of the composite structure.

---

## Structural calculation

### Step 1: Canonical kinetic normalization of phi on the Q_L block

Extend D9's color-only form to the full Q_L block (D8) by including the
isospin index α:

```
    phi(x) = (1/Z) * sum_{α,a} psi-bar_{α,a}(x) psi_{α,a}(x)           (1.1)
```

Compute `<phi(x) phi(y)>_{conn,free}` using D10's formula + the free
propagator δ_{αβ} δ_{ab} G_0(x,y):

```
    <phi(x) phi(y)>_{conn,free} = -(N_c · N_iso / Z²) · G_0(x,y)²      (1.2)
```

Canonical unit-residue (absorbing the fermion-loop sign):

```
    Z² = N_c · N_iso = 6  →  Z = sqrt(6)                              (1.3)
```

### Step 2: Clebsch-Gordan overlap of the unit-norm singlet

The (1,1) singlet state in the Q_L ⊗ Q_L* bilinear Hilbert space
(dim = 36), unit-normalized, is

```
    |S> = (1/sqrt(6)) * sum_{α,a} |α,a> ⊗ |α,a>*                      (2.1)
```

The top-channel basis bilinear `|top-pair> = |up, top-color> ⊗ |up, top-color>*`
has overlap

```
    <top-pair | S> = 1/sqrt(6)                                        (2.2)
```

(same for each of the 6 basis components, by singlet uniformity).

### Step 3: Same-1PI-function residue check (scalar-singlet channel)

This step records the load-bearing identity entirely within the
cited Cl(3) × Z³ framework surface, as a single 1PI Green's function
computed two ways. There is no UV-vs-EFT matching, no second
"effective theory" to be defined; only one theory, one Green's
function, two algebraically equivalent representations of it.

**Object of the check.** Define the amputated, 1PI, color-singlet
× iso-singlet × Dirac-scalar-scalar projection of the four-fermion
Green's function on the Q_L block:

```
    Γ⁽⁴⁾(q²) := P_{S,(1,1)} · ⟨ψ̄ψ(q) ψ̄ψ(-q)⟩_{1PI,amp}            (3.1)
```

where `P_{S,(1,1)}` projects onto the single channel
`O_S = (ψ̄ψ)_{(1,1)} (ψ̄ψ)_{(1,1)}` — color-singlet, iso-singlet,
Dirac-scalar on both bilinears. **Only this one channel is the
subject of the note; no other Dirac or representation channel is
claimed.**

**Representation A — direct OGE computation in the bare action.**

The cited bare action contains only the Wilson plaquette and the
staggered Dirac operator (D16, `MINIMAL_AXIOMS_2026-05-03.md`:32-43; conditional on staggered-Dirac realization gate, see :56-93) — no
fundamental scalar field, no contact 4-fermion operator. At tree
order in α_LM, the only Feynman diagram contributing to `Γ⁽⁴⁾(q²)` is
single-gluon exchange:

```
    Γ⁽⁴⁾(q²)|_OGE = -(g_bare² / q²) · Σ_a (T^a)_{ij}(T^a)_{kl}
                                    · (γ^μ)_{αβ}(γ_μ)_{γδ}        (3.2)
```

Project onto `O_S`: apply the exact SU(N_c) color-singlet Fierz
identity (D12, verified machine-precision by Block 4):

```
    Σ_a (T^a)_{ij}(T^a)_{kl}|_{δ_{ij}δ_{kl} channel} = -1/(2 N_c)  (3.3)
```

and the exact Lorentz-Clifford scalar projection (S2,
verified machine-precision by Block 8: `|c_S| = 1`):

```
    (γ^μ)_{αβ}(γ_μ)_{γδ}|_{(1)_{αβ}(1)_{γδ} channel} = c_S         (3.4)
```

Substituting (3.3) and (3.4) into (3.2):

```
    Γ⁽⁴⁾(q²)|_OGE = -c_S · g_bare² / (2 N_c · q²) · O_S            (3.5)
```

This is the COMPLETE tree-order value of `Γ⁽⁴⁾` from the bare
action: no other tree diagram contributes (D16 = Feynman-rule
completeness of the cited Wilson-staggered + plaquette action).

**Representation B — direct matrix-element computation of y_t_bare
from the H_unit operator content.**

The composite-Higgs structural input (D9) defines `H_unit`
as a composite local operator on the Q_L block:

```
    H_unit(x) := (1/√(N_c · N_iso)) · Σ_{α,a} ψ̄_{α,a}(x) ψ_{α,a}(x)
              =  (1/√6) · (ψ̄ψ)_{(1,1)}(x)                          (3.6)
```

with the canonical normalization `Z = √6` derived in Step 1 and
shown UNIQUE in Step 2 / Block 5 (D17): `H_unit` is the only
unit-normalized scalar bilinear operator on the Q_L block with
`Z² = N_c · N_iso = 6`.

**Definition of y_t_bare via the H_unit-to-top matrix element.**
On the canonical surface (g_bare = 1) the framework's bare Yukawa
coupling y_t_bare is DEFINED as the unit-norm-state matrix element
of the H_unit operator between the vacuum and a single top-pair
state in the (color = top-color, iso = up) component of the Q_L
block:

```
    y_t_bare := ⟨0 | H_unit(0) | t̄_{top,up} t_{top,up}⟩            (3.7)
```

> **Identification-map boundary (audit-prep clarification, 2026-05-06).**
> Equation (3.7) is the **framework's definition** of `y_t_bare`. The
> claim boundary of this note is that this defined readout satisfies the
> exact algebraic identities `(T1)` and `(T2)`. Whether this defined
> readout coincides with the Standard Model top-Yukawa observable as
> measured at low energy is a **separate, downstream question** that
> requires (a) an RG running map from `M_Pl` to the matching scale, and
> (b) a matching prescription connecting the framework's composite-Higgs
> readout to the SM bare-Yukawa vertex. Neither (a) nor (b) is in scope
> for this note; both are explicitly named as out-of-scope in the audit
> boundary above. The prior `audited_renaming` verdicts correctly
> identified that (3.7) is a definition, not a derivation, of the SM
> map; this refresh clarifies that the **audited scope is only the
> framework readout identity**, not the SM map.

Computing this matrix element directly from (3.6):

```
    y_t_bare = (1/√(N_c · N_iso)) · ⟨0 | ψ̄_{top,up} ψ_{top,up}(0)
               | t̄_{top,up} t_{top,up} ⟩
            = (1/√6) · 1
            = 1 / √6                                                (3.8)
```

The first factor (1/√6) is the Clebsch-Gordan weight from (3.6).
The second factor (= 1) is the unit-amplitude Wick contraction of
the bilinear `ψ̄ψ` with the corresponding fermion-pair external
state in canonical fermion normalization — a kinematic identity,
not a dynamical input.

**This evaluation uses ONLY:**
- the explicit operator content of H_unit (3.6) — Clebsch-Gordan
  weight 1/√(N_c · N_iso), from D17 + Steps 1-2;
- canonical fermion-state normalization;
- canonical scalar-composite normalization (Step 1, Z = √6).

It uses **no** information about OGE, no gauge coupling, no
4-fermion coefficient, no matching rule. It is a direct evaluation
of a matrix element of a defined composite operator on a defined
external state.

**Compute Γ⁽⁴⁾(q²)|_H_unit-rep from (3.8) independently.** Tree-level
H_unit-mediated contribution to the same Green's function, with
H_unit Yukawa vertices given by (3.8) on each side:

```
    Γ⁽⁴⁾(q²)|_H_unit-rep = -y_t_bare² / q² · O_S
                         = -(1/√6)² / q² · O_S
                         = -1 / (6 · q²) · O_S                      (3.9)
```

at `q² ≫ m_{H_unit}²` (the physical IR scale `m_{H_unit} ∼ v ≪ M_Pl`
is many orders below the cutoff; this scale separation is a
physical fact about the IR spectrum, not a convention).

**The same-1PI-function consistency identity.**

Representations (A) and (B) are now two INDEPENDENT computations
of the same Green's function `Γ⁽⁴⁾(q²)` in the same cited framework surface:
- (A) is computed from gauge-theory Feynman rules (OGE diagram
  + color/Dirac Fierz projection).
- (B) is computed from the H_unit operator's matrix element with
  the external top state (Clebsch-Gordan + canonical normalization).

Each is computed WITHOUT reference to the other. Comparing:

```
    Γ⁽⁴⁾_A = -c_S · g_bare² / (2 N_c · q²) · O_S
           = -1 · 1² / 6 / q² · O_S    (at canonical g_bare = 1, |c_S| = 1)
           = -1 / (6 q²) · O_S                                       (3.10)

    Γ⁽⁴⁾_B = -1 / (6 q²) · O_S      (3.9 above)                     (3.11)
```

The two values agree at the canonical surface (g_bare = 1). This
agreement is a non-trivial consistency check of the cited framework surface:
the bare action's gauge dynamics (Representation A) and the
operator content of the composite Higgs (Representation B) give
the same Green's function on the load-bearing scalar-singlet
channel.

**The Yukawa coupling y_t_bare = 1/√6 is therefore defined and evaluated**
from H_unit operator content (3.7-3.8). The
agreement (3.10 = 3.11) confirms internal consistency of the
framework but is not the source of the value.

**Inputs used (cited framework inputs plus exact group-theoretic identities):**

1. The bare Cl(3) × Z³ lattice action
   (`MINIMAL_AXIOMS_2026-05-03.md`:32-43; conditional on staggered-Dirac and `g_bare = 1` derivation gates) — contains exactly Wilson plaquette and
   staggered Dirac, no fundamental scalar, no contact 4-fermion.
2. D9: composite-Higgs structural axiom, no independent fundamental
   Yukawa parameter ([`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md):33-40).
3. D16: Feynman-rule completeness of the bare action — at O(α_LM)
   only the OGE diagram contributes to `Γ⁽⁴⁾`.
4. D17: scalar-uniqueness of `H_unit` on the Q_L block (Z² = 6 is
   unique among (1,1) Dirac-scalar composites; verified by Block 5
   numerically against the (1,8), (3,1), (8,3) alternatives).
5. SU(N_c) color-singlet Fierz coefficient `-1/(2 N_c)` (D12,
   exact SU(N_c) identity, Block 4 verified to machine precision).
6. Lorentz-Clifford scalar projection coefficient `|c_S| = 1`
   (S2, exact Clifford-algebra identity, Block 8 verified).
7. Physical IR scale separation `m_{H_unit} ≪ M_Pl` (electroweak
   scale `v ∼ 246 GeV` gives `m_H/M_Pl ∼ 10^{-17}`). This is a
   physical fact about the IR spectrum of the theory, not a
   matching convention at the cutoff.

There is no second theory, no matching rule, no auxiliary mass
freedom, no spectral assumption. The note records only that one
1PI Green's function on the Q_L scalar-singlet channel equals
itself when computed two algebraically equivalent ways.

### Step 4: Canonical-surface ratio

The Wilson gauge coupling on the canonical surface (D13 + D14 + D15):

```
    g_s(M_Pl) = sqrt(4 pi alpha_LM) = g_bare / sqrt(u_0)              (4.1)
```

with `alpha_LM = alpha_bare / u_0` (CMT at n_link = 1 per vertex).

The bare Yukawa (3.8) also inherits a `1/sqrt(u_0)` tadpole factor at
canonical-surface matching: the Yukawa vertex on the composite surface
involves one fermion-bilinear hopping link (D15, `n_link = 1`), and
`H_unit` itself is a local composite with the same tadpole dressing as
the gauge link:

```
    y_t(M_Pl) = y_t_bare / sqrt(u_0)
              = (g_bare / sqrt(6)) / sqrt(u_0)
              = g_s(M_Pl) / sqrt(6)                                   (4.2)
```

Taking the ratio, the `1/sqrt(u_0)` cancels:

```
    y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)                               (4.3)
```

This is the support-tier structural identification recorded by the note.

### Boundary of the identification

```
    y_t_bare = g_bare / sqrt(6)              (T1, exact tree-level algebra)
    y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)      (T2, exact on canonical surface)
```

These are exact algebraic identities on the stated canonical evaluation
surface. `y_t_bare` here is the framework's defined readout (Eq. 3.7),
not the SM observable; see the identification-map boundary clarification
following Eq. (3.7).

No precision bound, no NLO claim, no systematic is attached to this
identification. Perturbative and higher-order corrections are out of scope
and are discussed in the support note
`UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`.
Downstream quantitative reuse carries whatever systematic the
downstream package carries independently; the note does not
narrow that.

This is a framework-native structural identification within
`A_min = {Cl(3), Z^3}` plus the named open-gate `admitted_context_inputs`
(staggered-Dirac realization, `g_bare = 1`), using the chain (D1-D15)
and canonical-surface normalization choices (C1-C2 — both admitted as
open-gate context inputs per `MINIMAL_AXIOMS_2026-05-03.md`). No new
axioms. No framework conventions beyond canonical normalization. No
package-status-doc imports.

---

## Scale/scheme statement

What is identified where:

1. **At M_Pl on the canonical surface**: the RATIO `y_t/g_s = 1/sqrt(6)`
   is the structural identification within A_min via D1-D15 + C1-C2 as
   above. UV boundary condition.

2. **At v on the matching surface**: `y_t(v)` is obtained by backward
   RGE from `y_t(M_Pl)`. The `sqrt(8/9)` color-projection correction
   from YUKAWA_COLOR_PROJECTION_THEOREM:265-299 is applied at this
   matching step, not at the UV BC. The two operations are on different
   scales and do not compete.

3. **No blanket equality** is claimed across M_Pl and v schemes; only
   the M_Pl ratio is identified here.
