# Higgs Lattice-Curvature Coupling λ_curv from V_taste Symmetric-Point Curvature — Narrow Algebraic Theorem

**Date:** 2026-05-10
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.
**Primary runner:** [`scripts/frontier_higgs_lattice_curvature_coupling_narrow.py`](../scripts/frontier_higgs_lattice_curvature_coupling_narrow.py)

## 0. Audit context

The framework currently records two competing statements about the
Higgs scalar quartic coupling at the high scale:

1. [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
   asserts `λ(M_Pl) = 0` from "framework-native composite-Higgs /
   no-elementary-scalar boundary structure." The claim is recorded in
   [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md)'s
   assumption-derivation ledger as
   "the **weakest leg of the input chain** … mechanism-level support
   exists, but an **independent theorem forcing the high-scale quartic
   boundary from the framework remains open**."
2. [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
   Step 5–6 derives the tree-level mean-field formula
   `m_H_tree = v / (2 u_0) = 140.3 GeV`, with the +12% gap to physical
   `m_H = 125.10 GeV` closed by 2-loop CW corrections, lattice-spacing
   convergence, and Wilson-term taste-breaking.

This narrow theorem **does not** attempt to retire (1) or to identify
the framework's tree-level `m_H_tree` with the SM post-EWSB Higgs
pole. Instead it isolates a **distinct dimensionless quantity** —
`λ_curv` — defined purely from V_taste's symmetric-point curvature and
the EW VEV. `λ_curv` is Clifford-fixed and computable from primitives;
the relation between `λ_curv` and the SM EFT's `λ` is left as an
explicit named bridge theorem (the m_H_tree ↔ m_H_pole identification,
which HIGGS_MASS_FROM_AXIOM Step 5(b) explicitly admits is a tree-level
mean-field shortcut with known +12% mismatch).

This is a strict scope-narrowing from a prior draft of this PR that
identified `λ_curv` with the SM EFT's `λ` directly. An independent
audit pre-check flagged the identification as class (F) renaming
rather than class (A) algebraic, because the framework's `m_H_tree` is
the tachyonic-symmetric-point per-channel curvature scale, **not** the
SM post-EWSB Higgs pole. The present scope-narrowed theorem confronts
that distinction head-on by introducing an explicitly distinct symbol.

## 1. Claim scope

> **Theorem (lattice-curvature coupling identity).** Define the
> dimensionless **lattice-curvature coupling** `λ_curv` from the
> framework's tree-level mean-field surface (HIGGS_MASS_FROM_AXIOM
> Step 4–5) via:
>
> ```text
> λ_curv  :=  |∂²V_taste/∂m²|_{m=0}|  /  (N_taste · 2 v²)
>           =  (m_H_tree)²  /  (2 v²)                                          (1)
> ```
>
> where:
> - `V_taste(m) = -8 log(m² + 4u_0²)` is the per-channel taste-trace
>   potential at the symmetric point on the L_s = 2 mean-field APBC
>   surface (admitted from HIGGS_MASS_FROM_AXIOM Step 4);
> - `N_taste = 16` is the staggered taste count from
>   [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
>   (open gate; admitted);
> - `m_H_tree := v / (2 u_0)` is the tree-level mean-field readout per
>   HIGGS_MASS_FROM_AXIOM Step 5–6 (this is the framework's
>   tachyonic-symmetric-point per-channel curvature scale, NOT the SM
>   post-EWSB Higgs pole — see §3 below).
>
> Then **`λ_curv` is Clifford-fixed**:
>
> ```text
> λ_curv  =  1 / (8 u_0²)                                                       (2)
> ```
>
> with the v dependence cancelling exactly.
>
> At `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (gate #7 engineering frontier;
> ⟨P⟩ ≈ 0.594 from PR #685 lattice MC consensus on the framework Wilson
> surface), the numerical value is
>
> ```text
> λ_curv  ≈  0.1623.                                                            (3)
> ```

The narrow theorem **explicitly does NOT** claim:

- that `λ_curv` equals the SM EFT's Higgs scalar quartic `λ` at any
  scale;
- that `λ_curv ≠ 0` retires the framework's `λ(M_Pl) = 0` claim from
  VACUUM_CRITICAL_STABILITY (`λ_curv` and SM `λ` are distinct objects;
  the identification is a separate bridge theorem);
- that this theorem closes Gate #6 (lambda-UV anchor) of the seven-gate
  near-zero-imports map. Gate #6 closure requires the bridge theorem
  λ_curv ↔ SM λ, which is named here as the open piece, not closed;
- a Higgs-mass closure at observed `m_H = 125.10 GeV`;
- an absolute scale identification beyond "the lattice mean-field
  scale where the framework's V_taste curvature is read off, which is
  Planck-scale up to O(1) Wilson coefficient under the Planck pin
  (gate #4 currently `audited_renaming`)."

## 2. Counterfactual Pass — implicit assumptions

| # | Assumption | Forced or imported? | If wrong, what changes? |
|---|---|---|---|
| 1 | V_taste curvature at the symmetric point is well-defined as `∂²V_taste/∂m²|_{m=0}`. | Forced once V_taste's logarithmic form is admitted (HIGGS_MASS_FROM_AXIOM Step 4). | The curvature could be ambiguous (e.g., directional in a multi-component sense); structurally not the case here for a 1D m. |
| 2 | The N_taste normalization is 16 = 2^D in D=4. | Conditional on staggered-Dirac realization open gate. | The numerical λ_curv shifts; structural form `(m_H_tree)²/(2v²)` unchanged. |
| 3 | `λ_curv` is a meaningful dimensionless object distinct from SM λ. | Forced by the definition (1): it's a dim-0 ratio constructed from V_taste curvature, with no claim of SM-EFT matching. | The theorem becomes vacuous; but the definition is operational and well-formed. |
| 4 | `m_H_tree := v/(2u_0)` is the appropriate "tree-level readout" of the curvature. | Imported from HIGGS_MASS_FROM_AXIOM Step 5–6. | If the readout convention changes, the symbol m_H_tree shifts but `λ_curv` would be redefined consistently. |
| 5 | `u_0` is well-defined and Clifford-determinable. | Conditional on Gate #7 (engineering frontier). | Numerical λ_curv shifts; structural form 1/(8u_0²) unchanged. |
| 6 | `λ_curv ↔ SM λ` is an open bridge theorem (not assumed by this theorem). | This is the **honest scope statement**, not an assumption. | If λ_curv = SM λ holds at some scale (a future bridge theorem), the framework would gain a UV anchor; if not, λ_curv remains a structurally clean lattice-curvature object distinct from the EFT quantity. |

The load-bearing assumption is (1)+(4): V_taste curvature is well-
defined and the m_H_tree readout convention is the framework's
admitted tree-level mean-field. (2) and (5) are inherited admissions
named in admitted_context_inputs. (3) and (6) are scope statements,
not assumptions.

## 3. Elon first-principles — m_H_tree vs SM Higgs pole

Strip framework conventions. What does standard QFT say about the two
objects this theorem keeps explicitly distinct?

**Standard SM Higgs pole.** In the SM with V_eff(φ) = -μ²|φ|² + λ|φ|⁴
(plus loop corrections), the post-EWSB Higgs mass is the curvature of
the FULL effective potential at the broken-phase MINIMUM φ = v:

```text
m_H_pole²  =  ∂²V_eff/∂φ²|_{φ=v}  =  2λv²  +  (loop corrections).             (4)
```

This `m_H_pole` is an observable: 125.10 GeV per PDG.

**Framework's m_H_tree.** HIGGS_MASS_FROM_AXIOM Step 4 derives V_taste
via mean-field gauge factorization on the L_s = 2 minimal block:

```text
V_taste(m)  =  -8 log(m² + 4u_0²).                                              (5)
```

The curvature at the SYMMETRIC point m = 0 is

```text
∂²V_taste/∂m²|_{m=0}  =  -4 / u_0²    (negative — tachyonic).                  (6)
```

HIGGS_MASS_FROM_AXIOM Step 5(b) takes the magnitude of this tachyonic
curvature, divides by N_taste, and identifies it with `(m_H/v)²`:

```text
(m_H_tree / v)²  :=  |∂²V_taste/∂m²|_{m=0}|  /  N_taste  =  (4/u_0²) / 16
                  =  1 / (4 u_0²),                                              (7)

m_H_tree  =  v / (2 u_0).                                                       (8)
```

Step 5(b) explicitly admits this identification *"becomes exact in
the limit where (i) all N_taste taste channels degenerate, (ii) gauge
corrections vanish, (iii) the EWSB saddle aligns with the
symmetric-point curvature. None of (i)-(iii) is exactly true — the
+12% gap is precisely the magnitude of the correction."*

**Therefore `m_H_tree ≠ m_H_pole` in general.** The +12% gap from
m_H_tree = 140.3 to m_H_pole_obs = 125.10 GeV is the framework's
explicit acknowledgement of the gap.

This narrow theorem honors the distinction. `λ_curv` is defined via
`m_H_tree` (the symmetric-point curvature scale), NOT via `m_H_pole`.
The relation `λ_curv ↔ SM λ` requires a separate bridge theorem
identifying the symmetric-point curvature with the post-EWSB pole at
some matching scale — which is the open piece HIGGS_MASS_FROM_AXIOM
already names.

## 4. Admitted dependencies

| Authority | Role | Status |
|---|---|---|
| `HIGGS_MASS_FROM_AXIOM_NOTE.md` Step 4–5 | V_taste form + tree-level mean-field formula `m_H_tree = v/(2u_0)` | unaudited |
| `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` | N_taste = 16 = 2^D | open gate |
| `MINIMAL_AXIOMS_2026-05-03.md` | A1 (Cl(3)) + A2 (Z³) | meta |
| `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (Gate #7) | numerical input | engineering frontier |

The bare algebraic identity `λ_curv = 1/(8u_0²)` requires only the
V_taste form + the m_H_tree readout convention. No SM EFT structure,
no Higgs-pole physics, no λ(M_Pl) claim is admitted. The numerical
value (3) inherits Gate #7. No forward-citation of unmerged sibling
PRs (#924, #937) is made — those are referenced only as parallel-track
work.

## 5. Load-bearing step (class A)

```text
From V_taste(m) = -8 log(m² + 4 u_0²) (HIGGS_MASS_FROM_AXIOM Step 4):

  ∂V_taste/∂m  =  -8 · 2m / (m² + 4 u_0²),

  ∂²V_taste/∂m²  =  -8 · [2 / (m² + 4 u_0²)  -  4m² / (m² + 4 u_0²)²].

At m = 0:

  ∂²V_taste/∂m²|_{m=0}  =  -8 · 2 / (4 u_0²)  =  -4 / u_0².                     (i)

Tree-level mean-field readout (HIGGS_MASS_FROM_AXIOM Step 5):

  (m_H_tree / v)²  :=  |∂²V_taste/∂m²|_{m=0}|  /  N_taste
                     =  (4 / u_0²) / 16
                     =  1 / (4 u_0²),                                          (ii)

  m_H_tree         =  v / (2 u_0).                                             (iii)

Definition of λ_curv (this theorem):

  λ_curv  :=  (m_H_tree)²  /  (2 v²)
           =  v²  /  (4 u_0²)  /  (2 v²)
           =  1  /  (8 u_0²).                                                  (iv)

The v dependence cancels: λ_curv depends only on u_0.
```

Note: in step (iv), the `(2 v²)` divisor in the definition of `λ_curv`
is chosen to **structurally parallel** the SM relation
`λ = m²/(2v²)` — but `λ_curv` is **not** identified with SM λ. The
parallel form is convenient for downstream comparison work (a future
bridge theorem) without smuggling in the identification.

This is class (A) — algebraic operations on V_taste, the tree-level
mean-field readout, and the definition (iv). No new admissions
beyond those listed in §4. ∎

## 6. Structural implications (named, not derived)

### 6.1 Numerical value at the framework operating point

At `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (gate #7 engineering frontier):

```text
λ_curv  =  1 / (8 · 0.8776²)  =  1 / (8 · 0.7702)  =  1 / 6.162  ≈  0.1623.
```

`λ_curv` is dimensionless and Clifford-fixed: it depends only on the
plaquette-derived lattice tadpole `u_0`. With ⟨P⟩ converging at
NNNLO ξ=4 below ε_witness per
[`C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md`](C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md),
λ_curv is computable to engineering-frontier precision.

### 6.2 Named open bridge: `λ_curv ↔ SM λ`

The relation between the framework's `λ_curv` and the SM EFT's `λ` is
an open bridge theorem. Two candidate forms:

- **Direct identification:** `λ_curv = λ(μ_*)` at some matching scale
  μ_*. Requires showing the framework's symmetric-point curvature
  equals the SM post-EWSB pole curvature at scale μ_*. Equivalent to
  closing the framework's named tree-level mean-field shortcut from
  HIGGS_MASS_FROM_AXIOM Step 5(b).
- **Bounded matching:** `λ_curv = λ(μ_*) · (1 + ε_match)` with
  `ε_match` named and bounded. The framework's +12% gap from
  m_H_tree = 140.3 to m_H_obs = 125.10 GeV gives `ε_match ≈ 0.26` on
  the scale of `λ`-comparison (since λ ∝ m_H², the +12% in m_H is
  +26% in λ).

This narrow theorem does **not** close either form. It records the
gap as named open work.

### 6.3 Comparison to Shaposhnikov-Wetterich (audit comparator only)

Shaposhnikov-Wetterich (2009) predicted `m_H ≈ 126 GeV` pre-LHC by
imposing `λ(M_Pl) = 0` from an asymptotic-safety UV fixed point. The
framework's `λ_curv ≈ 0.1623` is **not** directly comparable: λ_curv
is a lattice-curvature object, and λ(M_Pl) in S-W is the SM EFT
quantity. The `λ_curv ↔ SM λ` bridge would be needed before
comparison.

If the bridge theorem closes with direct identification at `μ_* ≈ M_Pl
× u_0`, the framework's UV anchor would differ from S-W's at the level
of λ at high scale. This is *speculation, not closed*.

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_higgs_lattice_curvature_coupling_narrow.py
```

Verifies:

1. The V_taste curvature `∂²V_taste/∂m²|_{m=0} = -4/u_0²` symbolically
   via SymPy.
2. The tree-level mean-field readout `m_H_tree = v/(2u_0)` from
   HIGGS_MASS_FROM_AXIOM Step 5.
3. The definition `λ_curv := (m_H_tree)²/(2v²)` — note this is a
   DEFINITION, not an identification with SM λ.
4. The Clifford-fixed identity `λ_curv = 1/(8u_0²)` symbolically with
   v cancellation.
5. Numerical evaluation at `u_0 = 0.8776` gives `λ_curv ≈ 0.1623`.
6. Sign assertion: `λ_curv > 0` (the magnitude convention applied to
   the tachyonic curvature).
7. The runner explicitly distinguishes `λ_curv` from `λ_obs(v)` (the
   PDG-derived SM EFT value at v); the gap is the named open bridge
   theorem.
8. Note structure / scope discipline.

The runner does **not** verify any identification of `λ_curv` with
SM λ — that's outside this theorem's scope.

## 8. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Algebraic identity lambda_curv = 1/(8 u_0^2) where lambda_curv is the
  framework's lattice-curvature coupling defined as (m_H_tree)^2/(2 v^2),
  with m_H_tree = v/(2 u_0) the tree-level mean-field readout from
  HIGGS_MASS_FROM_AXIOM Step 5-6. lambda_curv is EXPLICITLY DISTINCT
  from the SM EFT's Higgs scalar quartic lambda; the lambda_curv <-> SM lambda
  bridge is named here as an open piece, not closed. At u_0 = 0.8776
  (gate #7 frontier), lambda_curv ≈ 0.1623.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only

declared_one_hop_deps:
  - higgs_mass_from_axiom_note
  - staggered_dirac_realization_gate_note_2026-05-03
  - minimal_axioms_2026-05-03
  - c_iso_su3_nnlo_closure_bounded_note_2026-05-10_su3nnlo

admitted_context_inputs:
  - V_taste form V(m) = -8 log(m² + 4 u_0²) (HIGGS_MASS_FROM_AXIOM Step 4)
  - tree-level mean-field readout m_H_tree = v/(2 u_0) (HIGGS_MASS_FROM_AXIOM Step 5)
  - N_taste = 16 = 2^D (staggered-Dirac realization open gate)
  - numerical u_0 ≈ 0.8776 (Gate #7 engineering frontier; structural form
    1/(8 u_0^2) holds independent of numerical value)

forbidden_imports_used: false  # no PDG values are derivation inputs;
                                # observed m_H = 125.10 GeV and lambda_obs(v)
                                # appear only as audit comparators in the runner
proposal_allowed: true
audit_required_before_effective_status_change: true

named_open_bridge:
  bridge_id: lambda_curv_to_sm_lambda
  description: |
    The relation between the framework's lambda_curv (lattice-curvature
    coupling) and the SM EFT's lambda (Higgs scalar quartic) is open.
    HIGGS_MASS_FROM_AXIOM Step 5(b) explicitly admits the m_H_tree <-> m_H_pole
    identification "becomes exact in the limit where (i) N_taste taste channels
    degenerate, (ii) gauge corrections vanish, (iii) EWSB saddle aligns with
    symmetric-point curvature. None of (i)-(iii) is exactly true — the +12%
    gap is the magnitude of the correction." This narrow theorem does not
    close that gap; it makes it explicit and audit-actionable.
```

## 9. What this theorem closes

- **`λ_curv = 1/(8u_0²)` is an exact Clifford-fixed dimensionless
  lattice-curvature coupling.** Class (A) algebraic on V_taste's
  symmetric-point curvature + N_taste normalization + the tree-level
  mean-field readout convention.
- **The implicit lattice-side curvature object is now an explicit
  named symbol** — `λ_curv`, distinct from SM λ, computable from
  primitives plus admissions inherited from HIGGS_MASS_FROM_AXIOM and
  Gate #7.

## 10. What this theorem does NOT close

- **The bridge `λ_curv ↔ SM λ` (lattice-curvature ↔ EFT-pole
  identification).** This is the framework's named open piece (the
  "+12% gap" or "weakest leg of the input chain"). Section 6.2 lists
  two candidate forms; closing either is a separate theorem.
- **Gate #6 (lambda-UV anchor) in full.** Gate #6 closure requires
  the bridge theorem above; this narrow theorem provides the
  Clifford-fixed lattice-side ingredient but not the bridge.
- **The framework's `λ(M_Pl) = 0` claim from VACUUM_CRITICAL_STABILITY.**
  That claim is a *different* assertion (about SM λ) than `λ_curv`; this
  narrow theorem is silent on whether VACUUM_CRITICAL_STABILITY's claim
  holds, fails, or competes with `λ_curv`.
- The Higgs-mass prediction at v.
- The Planck pin (Gate #4 `audited_renaming`).
- The staggered-Dirac realization gate.
- The numerical u_0 (Gate #7 engineering frontier).

## 11. Cross-references

### Parent / structural
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — provides V_taste form (Step 4) and tree-level mean-field readout
  (Step 5–6); Step 5(b) names the +12% gap that becomes the named
  open bridge in §6.2 of this theorem.
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — N_taste = 16 = 2^D origin (open gate).

### Context (parallel-track, not load-bearing)
- [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
  — claims `λ(M_Pl) = 0` for SM λ; *this narrow theorem is silent on
  whether that claim holds; λ_curv is a different object*.
- [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md)
  — assumption-derivation ledger names the open quartic-boundary
  theorem.

### Framework axioms / structural
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md`](C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md)
  — Gate #7 engineering frontier; provides u_0 numerical context.

### Standard physics references (admitted-context literature, not load-bearing)
- Shaposhnikov & Wetterich (2009) — comparator only; their `λ(M_Pl) = 0`
  is for SM λ, not λ_curv.
- Coleman & Weinberg (1973) — radiative corrections framing for the
  named open bridge in §6.2.
