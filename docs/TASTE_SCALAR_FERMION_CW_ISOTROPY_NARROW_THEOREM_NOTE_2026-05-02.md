# Taste-Scalar Fermion Coleman-Weinberg Isotropy — Narrow Theorem

**Date:** 2026-05-02
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Primary runner:** `scripts/frontier_taste_scalar_fermion_cw_isotropy_narrow.py`

## Claim scope (proposed)

> On `ℂ⁸ = (ℂ²)^{⊗3}` with commuting taste-shift involutions `S_i = σ_x ⊗ I ⊗ I, I ⊗ σ_x ⊗ I, I ⊗ I ⊗ σ_x` and the linear taste Hamiltonian
> `H(φ) = Σ_i φ_i S_i`, the one-loop fermion Coleman-Weinberg Hessian
> at the axis-aligned point `φ = (v, 0, 0)` (with `v ≠ 0`) is
> exactly isotropic:
> ```
> ∂²V_f / ∂φ_i ∂φ_j  =  δ_{ij} · C(v)
> ```
> for any smooth `f` such that `V_f(φ) = Σ_s f(λ_s(φ)²)`.

The narrow scope is **purely the fermion Coleman-Weinberg isotropy
identity** on the binary taste block. The parent audit handoff's safe
boundary was the exact fermion Coleman-Weinberg block; this narrow theorem
keeps only that algebraic scope.

The narrow theorem **does not** claim:

- gauge-loop or scalar-loop contributions to the Hessian (these use
  separate split models that are bounded — out of scope here);
- electroweak minimum selection or phase-transition consequences (separate downstream);
- Higgs-mass splitting from any non-fermionic source (separate);
- a Standard-Model Higgs-sector prediction.

## Formal inputs

| Input | Status | Role |
|---|---|---|
| (none, formally) | — | The theorem is purely algebraic on the binary product space `ℂ⁸ = (ℂ²)^{⊗3}` with `σ_x` shift operators — no external authority is load-bearing. |

The note operates on the abstract Cl(3)/Z³ taste-cube structure. While
this structure is the framework's setup, the load-bearing step does not
depend on any specific cited authority — it's an algebraic identity on
binary products of σ_x operators.

## Load-bearing step (class A)

```text
Setup: C^8 = (C^2)^{⊗3}, simultaneous shift-eigenbasis |s_1, s_2, s_3⟩
       with s_i ∈ {0, 1}.
Operators: S_i = σ_x acting on tensor factor i.
Eigenvalue: S_i |s⟩ = (-1)^{s_i} |s⟩ in the simultaneous S_i eigenbasis.
            Equivalently, rotate each tensor factor so σ_x is diagonal;
            the formal identity is basis-independent.

H(φ) = Σ_i φ_i S_i  →  λ_s(φ) = Σ_i φ_i (-1)^{s_i}    [exact eigenvalue]

At φ = (v, 0, 0):  λ_s(v, 0, 0) = v · (-1)^{s_1}, so |λ_s| = v ∀s.
                   Therefore  f(λ_s²) = f(v²)  ∀s.

Hessian:
    ∂²V_f / ∂φ_i ∂φ_j |_{φ=(v,0,0)}
       = Σ_s [ 2 f'(λ_s²) (∂λ_s/∂φ_i)(∂λ_s/∂φ_j)
              + 2 λ_s f''(λ_s²) λ_s (∂λ_s/∂φ_i)(∂λ_s/∂φ_j) ... ]
         simplified at λ_s² = v² uniform:
       = [coeff in v] · Σ_s (-1)^{s_i} · (-1)^{s_j}

Binary orthogonality sum:
    Σ_{s ∈ {0,1}^3} (-1)^{s_i} · (-1)^{s_j}
       = (Σ_{s_i ∈ {0,1}} (-1)^{2 s_i}) · (Σ_{s_j ≠ i} 1) · 4   if i = j
       = 8 · δ_{ij}                                           [exact]

Therefore Hessian = δ_{ij} · C(v) where C(v) absorbs the 8 and the
f-derivatives.   ∎
```

This is class (A) — algebraic identity on binary product structure.
No external authority is load-bearing.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_taste_scalar_fermion_cw_isotropy_narrow.py
```

Verifies, at exact rational precision via Python `Fraction`:

1. Binary orthogonality sum `Σ_s (-1)^{s_i}(-1)^{s_j} = 8 δ_{ij}` for all
   pairs `(i, j) ∈ {1, 2, 3}²`.
2. Eigenvalue `λ_s(φ) = Σ_i φ_i (-1)^{s_i}` is exact for any φ.
3. At `φ = (v, 0, 0)`: `λ_s² = v²` uniformly across all 8 basis states
   (verified for `v ∈ {1, 2, -3, 7/11}`).
4. Hessian off-diagonal `∂²/∂φ_i ∂φ_j` for `i ≠ j` evaluates to 0 at
   the axis-aligned minimum (concrete numerical test for several `f`
   choices: `f(x) = x`, `f(x) = x²`, `f(x) = log(1 + x)`).
5. Hessian diagonal `∂²/∂φ_i ∂φ_i` evaluates to a common value; concrete
   examples have nonzero common value.

## Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  Pure algebraic isotropy identity for one-loop fermion Coleman-Weinberg
  Hessian on Cl(3)/Z³ taste block at axis-aligned point phi=(v,0,0).
  Gauge-loop, scalar-loop, EW-phase-transition, and Higgs-sector
  consequences explicitly out of scope.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
```

Audit status is set only by the independent audit lane. This note is safe to
land as an unaudited, graph-visible bounded-theorem candidate with no
declared dependency edges because the load-bearing identity is self-contained
algebra on binary products. Retained-bounded effective status requires
independent audit of this row.

## What this theorem closes

The exact fermion Coleman-Weinberg isotropy half of the parent
`TASTE_SCALAR_ISOTROPY_THEOREM_NOTE`. The parent audit handoff named this
as the safe algebraic scope.

## What this theorem does NOT close

- Gauge-loop Hessian contributions (separate bounded model).
- Scalar-loop Hessian contributions (separate bounded model).
- Electroweak minimum selection, phase transition, or thermal scalar-cubic
  claims (separate bounded lanes).
- The full Higgs-sector spectrum (separate).

## Cross-references

- `TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md` — parent with a conditional audit
  verdict; this narrow theorem carves out the fermion CW isotropy half
  cleanly.
- Cycles 1-7 (PRs #292-302) — sister narrow theorems on different lanes.


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_dirac_realization_gate_note_2026-05-03](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
