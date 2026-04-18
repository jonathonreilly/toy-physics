# P1 I_S Revision Verification Note (Critical Review of the 3x Upward Revision Claim)

**Date:** 2026-04-17
**Status:** critical-review verification layer on top of the prior P1 citation note
(`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`).
**Verdict (up front, Abstract §0):** the cited-literature upward revision of P1 from
the packaged `1.92%` nominal to `~5.77%` is **structurally honest but semantically
partial**. The packaged `1.92%` was never a framework-native lattice-to-MSbar matching
derivation for the composite `H_unit` bilinear — the UV gauge-to-Yukawa bridge note
records it explicitly as *the magnitude of the 1-loop vertex correction on the tadpole-
improved PT surface (standard vertex-correction formula)*. It is a continuum-vertex
heuristic written with lattice inputs, not a lattice BZ integral. The cited
`I_S ∈ [4, 10]` is a different object — it is a genuine lattice-to-MSbar BZ matching
coefficient for the staggered scalar density on the Wilson plaquette gauge action at
`β ≃ 6`. The two are **not the same quantity** in different conventions
(**Possibility B is rejected**), they are two different approaches to bounding the
same NLO scale on the `y_t(M_Pl)/g_s(M_Pl)` readout.
**Runner:** `scripts/frontier_yt_p1_i_s_revision_verification.py`
**Log:** `logs/retained/yt_p1_i_s_revision_verification_2026-04-17.log`

---

## Authority notice

This note is a **verification / critical-review** layer. It does **not** modify:

- the master obstruction theorem (referenced in the prior citation note as
  `docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`);
- the retained Ward-identity theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), which is an exact tree-level
  algebraic identity with no precision claim attached;
- the packaged `delta_PT = 1.92%` value in
  `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`, which remains defensible in
  its stated role as an OPEN-status continuum-vertex magnitude heuristic;
- the prior citation note
  `docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`, whose literature-
  bracket reading of `I_S ∈ [4, 10]` is internally consistent;
- the prior symbolic reduction
  `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py` (21/21 PASS), whose
  structural result `I_1 = I_S` on the retained conserved-current surface is
  unchanged by this note.

What this note adds is narrower: a **deterministic check** of whether the claimed
3x upward revision corresponds to Possibility A (revision correct and the packaged
value is a mis-identified `I_S = 2`), Possibility B (convention-mismatch false
alarm), or Possibility C (the packaged value and the cited `I_S` are two distinct
NLO contributions, potentially additive or superseding). The verdict is stated
upfront and then verified arithmetically and semantically.

---

## Abstract (§0 Verdict)

**Verdict:** Possibility A in **magnitude** (the upward revision is directionally
correct), Possibility C in **semantics** (the packaged value and the cited `I_S`
are **not** the same 1-loop object computed in different conventions — they are
two different approaches to the same NLO scale). Specifically:

- The packaged `delta_PT = α_LM · C_F / (2π) = 1.924%` is a **continuum vertex-
  correction magnitude** written with canonical-surface inputs. It is a
  heuristic "size-of-NLO" estimate of the standard continuum vertex-correction
  magnitude, NOT a lattice BZ integration for any specific operator. The UV
  gauge-to-Yukawa bridge note labels it explicitly as such (line 197: "the
  magnitude of the 1-loop vertex correction on the tadpole-improved PT
  surface").
- The cited `I_S ≈ 6` (range `[4, 10]`) is a **lattice-to-MSbar BZ integral** for
  the staggered scalar density operator on the Wilson plaquette gauge action at
  `β ≃ 6`, with tadpole improvement. This is a distinct object; it is a real
  quantity in the staggered lattice-QCD literature and is not reducible to the
  continuum vertex-correction magnitude by any convention switch.
- **Possibility B (false alarm) is rejected**: no normalization convention
  reconciles the two numbers. The packaged `1.92%` is not "the same quantity as
  I_S in a different normalization". It is a different quantity that happens to
  equal `(α/(4π)) · C_F · 2` when algebraically rewritten — but the "2" is a
  numerical artifact of the convention conversion, not a claimed operator-
  matching BZ integral.
- **Possibility A (revision correct) is correct in magnitude**: the actual
  lattice-to-MSbar scalar-density matching coefficient is indeed materially
  larger than the continuum vertex-correction magnitude — the cited `[4, 10]`
  bracket is a faithful reading of published staggered-fermion matching
  literature, and the resulting `P1 ∈ [3.85%, 9.62%]` range is the correct
  size-of-NLO estimate for the composite `H_unit` scalar-bilinear matching on
  the canonical surface.
- **Possibility C (additive / distinct contributions) captures the semantics**:
  the two quantities should not simply replace one another. At full NLO the
  `y_t(M_Pl)/g_s(M_Pl)` readout picks up (i) a continuum vertex-correction
  piece (captured heuristically by the packaged `1.92%`) and (ii) a lattice
  scalar-density matching piece (captured by the cited `I_S`). In a complete
  lattice-to-MSbar bridge, the lattice-side matching piece is the leading one
  and the "continuum vertex-correction" heuristic is implicitly absorbed into
  it. So the appropriate use is: **report the P1 budget in the lattice-matching
  language**, at `I_S ∈ [4, 10]` central `~6`, giving `P1 ∈ [3.85%, 9.62%]`
  central `~5.77%`. Do **not** add the `1.92%` on top; it is absorbed into the
  lattice matching (and in any event, the two are not strictly commensurate at
  this level of rigor).

**Revised P1 contribution (central, on the framework canonical surface):**

```
    P1_central  ≃  5.77%       (α_LM / (4π) · C_F · I_S ;  I_S = 6)
    P1 range    ≃  [3.85%, 9.62%]     (I_S ∈ [4, 10])
```

with the **explicit caveat** that `I_S` is cited from staggered-QCD literature
at `O(1)` precision, not derived framework-native. The packaged `1.92%` remains
defensible in its stated support-only role (continuum vertex-correction
heuristic) and should **not** be dropped from the support note; it should be
read as a *lower-bound floor* associated with the continuum-only evaluation,
not as the framework-specific P1.

**Confidence level in the verdict: HIGH** on the semantic question (Possibility
B is clearly rejected), **MODERATE** on the quantitative question (the cited
`I_S ≈ 6` is an honest literature bracket but has `O(1)` citation uncertainty
and is not framework-native). The 3x upward revision is directionally correct;
the precise numerical value requires a framework-native BZ integration that is
not provided in either this note or the prior citation note.

---

## 1. Retained foundations

This note inherits without modification:

- `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` at `SU(3)` (D7 + S1);
- Canonical surface `⟨P⟩ = 0.5934`, `u_0 = 0.87768`, `α_LM = 0.09067`,
  `α_LM / (4π) = 0.00721` (from `scripts/canonical_plaquette_surface.py`);
- Color-tensor decomposition `Δ_R = C_F · I_1 + C_A · I_2 + T_F n_f · I_3`
  (from the prior color-factor reduction, referenced by the citation note);
- Ward-identity tree-level identity `y_t_bare = g_bare / √6` from
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (exact algebraic, no NLO claim);
- Conserved-current reduction `I_V = 0` on the retained staggered
  point-split current surface, hence `I_1 = I_S` (from
  `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`, 21/21 PASS).

---

## 2. Reconstruction of the packaged `1.92%`

### 2.1 Literal source

The packaged value is defined in
`docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md` (the "NLO corrections" section,
lines 192–199):

```
    **Perturbative 1-loop vertex correction (derived):**
        C_F = (N_c^2 - 1) / (2 N_c) = 4/3 for SU(3)
        delta_PT = alpha_LM * C_F / (2 pi) = 1.92%

    This is the magnitude of the 1-loop vertex correction on the tadpole-
    improved PT surface (standard vertex-correction formula, retained in
    Block 9 of the runner).
```

Three structural facts read off this source:

(a) The coefficient `C_F / (2π)` is the **standard continuum-QED/QCD vertex-
    correction prefactor** (e.g., `δZ_ψ^{1-loop} = −(α/(2π)) · C_F · [½ + …]` or
    the Ward-related vertex factor `F_1(0) = 1 + (α/(2π)) · C_F · [0 + IR]`).

(b) The word "magnitude" is used — i.e. this is a characteristic scale of NLO,
    not a specific operator-matching coefficient.

(c) The source labels the status "OPEN; support-only; not part of authority
    theorem", with the explicit caveat "Any downstream package that reuses the
    theorem's exact algebraic identity ... and wants a quantitative precision
    claim must carry its own systematic ... or leave the systematic OPEN."

### 2.2 What the packaged value is NOT

The packaged `delta_PT` is **not**:

- a lattice-to-MSbar BZ integral for any specific operator (no BZ domain is
  specified, no specific propagators are integrated);
- the matching coefficient of the lattice scalar density `ψ̄ ψ` (not an operator-
  specific quantity at all);
- the `C_F · I_S` term of the retained decomposition `Δ_R = C_F · I_1 + …`
  (`I_S` is a specific lattice BZ integral over staggered fermion and Wilson
  gluon propagators; the packaged `δ_PT` is not of this form).

It is a continuum vertex-correction magnitude evaluated at the canonical-surface
coupling `α_LM`, nothing more.

### 2.3 Algebraic identity in `α/(4π)` convention

As a *consequence* of the standard vertex-correction formula
`α · C_F / (2π) = (α / (4π)) · C_F · 2`, one can algebraically rewrite:

```
    delta_PT  =  α_LM · C_F / (2π)  =  (α_LM / (4π)) · C_F · 2
```

The `2` on the right-hand side is a **conversion factor**, not a claimed BZ
integral value. The citation note (§1.6) reads this `2` as if it were
`I_S_standard = 2`. This reading is only correct if one asserts that the
packaged `δ_PT` is already in the form `(α/(4π)) · C_F · I_S` with some `I_S`
value. It isn't — the packaged `δ_PT` is in the form `(α / (2π)) · C_F`, and
the numerical coincidence with `(α / (4π)) · C_F · 2` is a trivial convention
identity that doesn't imply `δ_PT` is a BZ integration output.

**Conclusion of §2:** The packaged `1.92%` is a continuum vertex-correction
magnitude, not a lattice BZ integral. The "implicit `I_S = 2`" label in the
citation note is a convention-conversion reading, not a property of the
packaged derivation itself.

---

## 3. Reconstruction of the cited `I_S ≈ 6`

### 3.1 Literal definition (from the prior citation note §2.1)

```
    Z_S^{lat → MSbar}(μ = 1/a)
        =  1  +  (α_s · C_F / (4π)) · I_S(β, tadpole_improvement, operator_form)
        +  O(α_s^2)
```

with `I_S` a pure BZ integral over the lattice Feynman rules (staggered
fermion propagator `D_ψ(k) = Σ sin²(k_μ a) / a²` and Wilson gluon propagator
`D_g(k) = (4/a²) Σ sin²(k_ρ a/2)`), evaluated specifically for the scalar
bilinear `ψ̄ ψ` on the 1-link staggered lattice.

This is an **operator-specific BZ integration**. The BZ domain is
`[-π/a, π/a]^4`, the propagators are the retained lattice Feynman rules, the
operator is the scalar density with `H_unit = (1/√6) Σ ψ̄ψ` normalization, and
the scheme is MSbar at `μ = 1/a` after subtracting the logarithmic divergence.

### 3.2 Literature values

The staggered lattice-QCD literature evaluates `I_S` (or the corresponding
named matching coefficient in various conventions) for the tadpole-improved
staggered scalar density on Wilson plaquette gauge action. The cited range is:

| Convention / scheme                         | `I_S` range        | Representative citations                     |
|---------------------------------------------|---------------------|-----------------------------------------------|
| Un-improved Wilson + staggered scalar       | `[10, 20]`          | Kilcup–Sharpe 1987, Sharpe 1994              |
| Tadpole-improved Wilson + 1-link staggered  | `[4, 10]`           | Bhattacharya–Sharpe 1998, BGKS 1999          |
| Standard fundamental-Yukawa continuum       | `2` (exact)         | reference point only                          |

The tadpole-improved bracket `I_S ∈ [4, 10]` with literature-cluster central
`~6` is the retained citation (citation note §2.2–2.4).

### 3.3 What the cited `I_S` is NOT

The cited `I_S ≈ 6` is **not**:

- the "standard vertex-correction magnitude" `C_F · α / (2π)` — that is a
  continuum quantity; the BZ integral on the lattice explicitly includes
  lattice artifacts (Wilson plaquette gluon propagator deviation from
  continuum `k²`, staggered taste sum, tadpole improvement factor);
- a framework-native derivation on the `Cl(3) × Z^3` canonical action — it is
  a lattice-QCD literature value for the *closest* analogue
  (tadpole-improved staggered scalar density at `β ≃ 6`), with explicit `O(1)`
  citation uncertainty per the prior note §2.4;
- the full `Δ_R` — it is only the `C_F · I_1 = C_F · I_S` piece, with `C_A · I_2`
  and `T_F n_f · I_3` pieces still OPEN (citation note §7).

### 3.4 Physical reason for `I_S ≠ 2`

The prior citation note §2.3 gives two structural reasons the lattice scalar-
density matching coefficient is materially larger than the continuum
fundamental-Yukawa value `2`:

1. **Staggered taste structure.** The BZ integrand retains a nontrivial taste
   sum over the staggered `η`-phase structure (D1–D4) that is absent from the
   continuum fundamental-Yukawa vertex.
2. **Wilson plaquette gluon propagator.** The lattice gluon propagator differs
   from the continuum `k²` by `O((k a)^4)` terms, which integrate to a finite
   `O(1)` shift in `I_S`.

Both are intrinsic to the canonical staggered surface and persist under tadpole
improvement (which reduces magnitude but does not remove the shift).

**Conclusion of §3:** The cited `I_S ≈ 6` is a lattice BZ integral specific to
the staggered scalar density on the Wilson plaquette action, not a continuum
vertex-correction magnitude. The two quantities are structurally distinct.

---

## 4. Comparison analysis: same quantity? different? additive?

### 4.1 Possibility B (false alarm): rejected

Possibility B asserts that the packaged `δ_PT` and the cited `I_S` are the
same physical quantity in different conventions (e.g., `α/(2π)` vs `α/(4π)`
normalization, or different operator bases).

This is rejected by the following observations:

(a) **Different objects.** `δ_PT` is dimensionless `α · C_F / (2π)`, a
    continuum scale. `I_S` is dimensionless `α · C_F · I_S / (4π)` where `I_S`
    is a lattice BZ integral. The dimensionality is the same (both are
    corrections to `ln(Z_S)`), but the *definition* is different: one is a
    continuum vertex-correction magnitude; the other is a lattice-to-MSbar
    BZ integration for a specific operator.

(b) **No convention switch reconciles them.** `α/(2π) = 2 α/(4π)`, so the
    trivial conversion gives `α · C_F / (2π) = (α / (4π)) · C_F · 2`. The
    "2" on the right is a convention factor, not a BZ integral value. The
    cited `I_S ≈ 6` is a *different* number — it is the result of an actual
    BZ integration over lattice propagators, not a convention coefficient.

(c) **Physical mechanism.** The cited `I_S` is larger than `2` for two
    *specific* physical reasons (§3.4) that are absent in the continuum
    vertex-correction magnitude. The two reasons are intrinsic to the lattice
    regulator; no convention switch on the continuum side can reproduce them.

Possibility B would require that `I_S = 2` *on the lattice* for the staggered
scalar density — which is contradicted by the literature cluster at `~6`.
Therefore Possibility B is rejected.

### 4.2 Possibility A (revision correct in magnitude): confirmed directionally

Possibility A asserts that the packaged `1.92%` implicitly uses `I_S = 2` and
this is a mis-identification on the composite-H_unit surface.

This is **partially** correct:

- **Directionally correct**: the lattice-to-MSbar matching coefficient for the
  staggered scalar density IS materially larger than `2` in the `α/(4π)`
  convention, and the resulting P1 is materially larger than `1.92%`.
  This is confirmed by the staggered-QCD literature.

- **Semantically imprecise**: the packaged `1.92%` does NOT actually "assume
  `I_S = 2`" — it is a different quantity (continuum vertex-correction
  magnitude) that happens to equal `(α/(4π)) · C_F · 2` after convention
  conversion. The mis-identification is not that the packaged value chose the
  wrong `I_S`; rather, the packaged value was never a lattice `I_S`-style
  quantity to begin with, and the later attempt to read the packaged `1.92%`
  as `(α/(4π)) · C_F · I_S_standard` is a convention-switch re-interpretation.

### 4.3 Possibility C (distinct contributions): captures the semantics

Possibility C asserts that the packaged `1.92%` and the cited `I_S` are
distinct NLO contributions, potentially additive.

This is the **correct semantic framing**:

- The packaged `1.92%` is a continuum vertex-correction magnitude (a heuristic
  scale-of-NLO).
- The cited `I_S ≈ 6` is a lattice-to-MSbar matching coefficient for the
  staggered scalar density (a specific operator-matching BZ integral).

These are NOT additive on the same ledger, because in a complete lattice-to-
MSbar bridge, the lattice-matching piece (cited `I_S`) already includes the
continuum-vertex-correction content as its **asymptotic limit**. The "standard
vertex-correction formula" gives `I_S_continuum = 2` as the continuum analogue
of the lattice BZ integral; the lattice value `I_S_lat ≈ 6` **replaces** (not
"adds to") the continuum value on the lattice surface.

**Correct accounting**: the framework-specific P1 is evaluated with the
lattice `I_S`, not the continuum heuristic. The packaged `1.92%` was a
*placeholder* (explicitly OPEN / support-only in its source), and the
appropriate replacement is `P1 ∈ [3.85%, 9.62%]` central `~5.77%`. The `1.92%`
is not added on top; it is *superseded* by the lattice value.

### 4.4 One subtle caveat: the Ward-identity cancellation

The Ward-identity theorem (Steps 3A–3E of
`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`) derives `y_t_bare = g_bare / √6`
as an exact **tree-level** algebraic identity in Representations A (direct
OGE computation) and B (direct matrix-element of `H_unit`). At 1-loop,
Representations A and B pick up independent loop corrections. The **ratio**
`y_t(M_Pl) / g_s(M_Pl) = 1/√6` is preserved only if the 1-loop corrections
CANCEL between the two representations.

The cited `I_S` enters Representation B (H_unit scalar-density matching on
the lattice). Representation A has its own 1-loop correction (OGE box
diagrams, gluon self-energy, etc.). In principle, the 1-loop corrections on
both sides could partially cancel, and the **net effect** on
`y_t(M_Pl) / g_s(M_Pl)` could be smaller than the `I_S` correction alone.

This is NOT established here. Neither the prior citation note nor this
verification note attempts a full 1-loop closure of both representations of
the Ward identity. The honest statement is:

> The cited `I_S ≈ 6` is the size of the lattice scalar-density matching
> coefficient on Representation B. The net effect on the Ward ratio
> `y_t(M_Pl) / g_s(M_Pl)` at 1-loop depends on whether the Representation-A
> correction partially cancels it. This cancellation structure is not
> established, so the cited `I_S` bracket should be read as an **upper
> bound** on the P1 contribution from the scalar-density matching, not as
> the net effect on the ratio.

This is a further caveat on top of the `O(1)` citation uncertainty.

---

## 5. Dimensional analysis cross-check

### 5.1 Packaged value

```
    delta_PT  =  α_LM · C_F / (2π)
              =  0.09066784 × (4/3) / (2π)
              =  0.01924
              =  1.9240 %
```

### 5.2 Cited interpretation (α/(4π) convention)

```
    P1(I_S)  =  (α_LM / (4π)) · C_F · I_S
             =  0.00721473 × (4/3) × I_S
             =  0.00961964 × I_S

    I_S = 2   :   P1 = 0.01924 = 1.92 %     (= packaged by convention identity)
    I_S = 4   :   P1 = 0.03848 = 3.85 %
    I_S = 6   :   P1 = 0.05772 = 5.77 %     (central cited)
    I_S = 8   :   P1 = 0.07696 = 7.70 %
    I_S = 10  :   P1 = 0.09620 = 9.62 %
```

### 5.3 Convention identity check

```
    α / (2π)  =  2 · α / (4π)
    α · C_F / (2π)  =  (α / (4π)) · C_F · 2
```

This identity is exact; both sides evaluate to `0.01924` at the canonical surface.
The "2" is a convention factor, not an `I_S` value in any physical sense.

### 5.4 Both in the same units

Both `delta_PT` (packaged) and `P1(I_S)` (cited) are dimensionless corrections
to the Yukawa/gauge ratio at 1-loop. They have the same units, so numerical
comparison is meaningful. The ratio `P1(I_S=6) / delta_PT_packaged = 3.0` is
structurally consistent — *if* one accepts the reading that `delta_PT` should
be replaced by `P1(I_S)` with the lattice-specific `I_S`.

---

## 6. Verdict

### 6.1 Primary verdict: Possibility A (magnitude) + Possibility C (semantics)

- **Possibility B is rejected**: no normalization convention reconciles the
  packaged `1.92%` (continuum vertex-correction magnitude) with the cited
  `I_S ≈ 6` (lattice-to-MSbar BZ matching coefficient). They are distinct
  quantities.
- **Possibility A captures the magnitude of the revision**: the appropriate
  framework-specific P1 estimate on the canonical surface is indeed
  `P1 ∈ [3.85%, 9.62%]` central `~5.77%`, materially larger than the packaged
  `1.92%`. The revision is in the right direction.
- **Possibility C captures the semantics**: the packaged value and the cited
  `I_S` are distinct NLO contributions. The lattice-specific `I_S` **supersedes**
  the continuum vertex-correction heuristic rather than adding to it. Do not
  sum them.

### 6.2 Revised P1 contribution

```
    P1_central  ≃  5.77 %      (α_LM / (4π) · C_F · I_S ;  I_S = 6 central)
    P1 range    ≃  [3.85%, 9.62%]     (I_S ∈ [4, 10])
```

with the caveats:

(a) `I_S` is cited from staggered-QCD literature at `O(1)` precision, not
    framework-native;
(b) the cancellation between Representations A and B of the Ward identity
    at 1-loop is not established, so `I_S` may overcount the net effect on
    the ratio `y_t(M_Pl) / g_s(M_Pl)` (§4.4);
(c) the `C_A` channel (`I_2`) and `T_F n_f` channel (`I_3`) of `Δ_R` remain
    OPEN and are not included in this estimate.

### 6.3 Do the packaged `1.92%` and cited `I_S` sit on the same ledger?

**No, they should not be added.** The packaged `1.92%` is a continuum vertex-
correction magnitude; the cited `I_S · C_F · α/(4π)` is a lattice-to-MSbar
matching coefficient that **contains** the continuum vertex-correction content
as its continuum limit. On the lattice surface, the lattice value supersedes
the continuum heuristic. The correct reporting is:

- On the canonical lattice surface (tadpole-improved Wilson plaquette +
  staggered): P1 ≈ `(α_LM / (4π)) · C_F · I_S_lat` with `I_S_lat` cited.
- The packaged continuum value `1.92%` is a lower bound / sanity check only
  (it is what the matching coefficient would be in a continuum regulator with
  no lattice artifacts).

### 6.4 Confidence level

**HIGH** on the semantic verdict: the packaged value and the cited `I_S` are
distinct quantities; Possibility B is clearly rejected; the revision is in
the right direction.

**MODERATE** on the quantitative value: `I_S ≈ 6` is an honest literature
reading but carries `O(1)` citation uncertainty and is not framework-native.
The range `[4, 10]` is a defensible bracket. A framework-native 1-loop BZ
integration would be required to narrow the uncertainty below `O(1)` and to
close the Ward-cancellation caveat (§4.4).

---

## 7. Safe claim boundary

This note claims:

> The cited upward revision of P1 from the packaged `1.92%` to `~5.77%` (range
> `[3.85%, 9.62%]`) is **directionally correct in magnitude** (Possibility A)
> and **distinct in semantics** from the packaged value (Possibility C). The
> packaged value is a continuum vertex-correction magnitude, not a lattice BZ
> integral. Possibility B (false-alarm convention mismatch) is rejected. The
> revised P1 should be reported in the lattice-matching language with the
> lattice `I_S` value; the packaged continuum value is superseded, not
> additive, and remains defensible only as a lower-bound sanity check.

It does **not** claim:

- that the revised P1 is framework-native (the cited `I_S` is external
  literature);
- that `I_S ≈ 6` is precise to better than `O(1)` (cited uncertainty remains);
- that the net 1-loop correction to `y_t(M_Pl) / g_s(M_Pl)` equals the cited
  `P1 ≈ 5.77%` (the Representation-A vs Representation-B cancellation at
  1-loop is not established; cited `P1` may overcount);
- that the master obstruction theorem or any publication-surface file should
  be modified on the basis of this verification note;
- that the `C_A` (`I_2`) or `T_F n_f` (`I_3`) channels of `Δ_R` are closed;
  they remain OPEN.

---

## 8. What is retained vs. cited vs. open

**Retained (framework-native, unchanged by this note):**

- `SU(3)` Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`.
- Canonical surface `α_LM = 0.0907`.
- Color-tensor decomposition `Δ_R = C_F · I_1 + C_A · I_2 + T_F n_f · I_3`.
- Conserved-current reduction `I_1 = I_S` on the retained staggered surface.
- Ward-identity tree-level exact identity `y_t_bare = g_bare / √6` (no NLO
  claim attached).
- Packaged `δ_PT = α_LM · C_F / (2π) = 1.924%` (continuum vertex-correction
  magnitude, OPEN / support-only status in its source note).

**Cited (external lattice-QCD literature, with `O(1)` uncertainty):**

- Tadpole-improved staggered scalar-density BZ matching coefficient
  `I_S ∈ [4, 10]` in the `α/(4π)` convention, central `~6`.
- The continuum fundamental-Yukawa value `I_S = 2` as a reference point.

**Open (not closed by this note or the prior citation note):**

- Framework-native 1-loop BZ evaluation of `I_S` on the retained
  `Cl(3) × Z^3` canonical action.
- Representation-A vs Representation-B cancellation at 1-loop on the Ward
  ratio `y_t(M_Pl) / g_s(M_Pl)` (the cited `I_S` may overcount the net
  effect on the ratio).
- `C_A` channel (`I_2`) and `T_F n_f` channel (`I_3`) of `Δ_R`.
- Propagation of the revised P1 into any publication-surface table; no
  publication-surface file is modified by this note.

---

## 9. Validation

The runner `scripts/frontier_yt_p1_i_s_revision_verification.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p1_i_s_revision_verification_2026-04-17.log`. The runner
must return PASS on every check to keep this note on the retained surface.

The runner verifies:

- exact reproduction of the packaged `δ_PT = α_LM · C_F / (2π) = 1.924%`;
- convention identity `α/(2π) = 2 · α/(4π)` giving the algebraic form
  `(α/(4π)) · C_F · 2` — identifying the "2" as a convention factor, not a
  BZ integral value;
- framework-specific P1 at `I_S ∈ {2, 4, 6, 8, 10}` in the `α/(4π)` convention;
- convention-reconciliation check (rejection of Possibility B);
- dimensional consistency (both quantities dimensionless corrections to
  `ln(Z_S)`);
- verdict determination: A (magnitude) + C (semantics), not B;
- revised P1 central `~5.77%`, range `[3.85%, 9.62%]`;
- no modification of the master obstruction theorem, the Ward-identity
  theorem, or the packaged `δ_PT` note;
- structural preservation of the prior symbolic `I_1 = I_S` reduction.
