# Bridge Gap — Single-Plaquette Heat-Kernel Closed Form (Block 02)

**Date:** 2026-05-06
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded support theorem on the framework's heat-kernel
single-plaquette evaluation surface, conditional on the same premises
as Block 01 (canonical Tr-form, g_bare = 1 open gate, heat-kernel as
Cl(3)-native action candidate, leading-order small-U matching). It is
NOT a Resolution-A closure of the bridge gap; it derives the exact
closed-form single-plaquette heat-kernel expectation under Block 01's
derived Brownian time, and explicitly demonstrates that the heat-kernel
single-plaquette evaluation is closed in **exactly two character terms**
without any NMAX truncation (in contrast to Wilson's infinite Bessel-
determinant series).
**Authority role:** branch-local source-note proposal. Audit verdict
and effective status are set only by the independent audit lane.
**Loop:** bridge-gap-new-physics-20260506 (Block 02 / R2.A)
**Branch (intended):** physics-loop/bridge-gap-new-physics-block02-20260506
**Primary runner:** [`scripts/probe_hk_plaquette_closed_form.py`](../scripts/probe_hk_plaquette_closed_form.py)

## Question

Given Block 01's derived Brownian time `t(β=6) = 1` from canonical
Tr-form + small-U matching (per
[`BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md)),
what is the closed-form single-plaquette expectation `⟨(1/N_c) Re Tr U⟩`
under the heat-kernel measure `P_t(U)` at `t = 1`?

## Answer

The closed form is exact and finite, requiring only the (1,0) and (0,1)
fundamental representations:

```
⟨(1/3) Re Tr U⟩_HK,1plaq(t) = exp(-2 t / 3).                                (T2)
```

At Block 01's `t(6) = 1`:

```
⟨P⟩_HK,1plaq(6) = exp(-2/3) = 0.5134171190...                              (T2.6)
```

This is **exact rational/transcendental**, not a truncated character sum.
No NMAX cutoff is needed — Schur orthogonality forces all higher
representations `(p,q)` with `p + q ≥ 2` to contribute exactly zero to
the single-plaquette `Re Tr U` expectation.

## Setup

### Premises (A_min for this block)

Inherits Block 01's A_min plus:

| ID | Statement | Class |
|---|---|---|
| (Block 01) | t(β = 6) = 1 from canonical Tr-form + small-U Wilson-HK match | bounded support theorem (just-landed) |
| C2 | `C_2(1,0) = 4/3` exact | retained per [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md) |
| SO | Schur orthogonality on SU(3) Haar measure | standard math machinery |
| HK | Heat-kernel character expansion `P_t(U) = Σ_λ d_λ exp(-t·C_2(λ)/2) χ_λ(U)` | derived from Block 01 §Step 2 |

### Forbidden imports (no load-bearing role)

Same as Block 01: no PDG / lattice MC values, no fitted coefficients,
no same-surface family arguments, no Wilson Bessel-determinant
character coefficients as motivation.

## Derivation

### Step 1: Re Tr U as a sum of fundamental characters

For `U ∈ SU(3)`, the trace observable decomposes:

```
Re Tr U = (1/2)(Tr U + Tr U†) = (1/2)(χ_{(1,0)}(U) + χ_{(0,1)}(U))         (1)
```

since `χ_{(1,0)}(U) = Tr U` (fundamental rep character) and
`χ_{(0,1)}(U) = Tr U† = (Tr U)*` (conjugate fundamental).

### Step 2: Heat-kernel character expansion

By Block 01 Step 2 / equation (4):

```
P_t(U) = Σ_λ d_λ · exp(-t · C_2(λ) / 2) · χ_λ(U).                          (2)
```

### Step 3: Schur orthogonality

For SU(3), the conjugate of irrep `λ = (p, q)` is `λ̄ = (q, p)`. Schur
orthogonality on the SU(3) Haar measure gives:

```
∫_{SU(3)} χ_λ(U) · χ_μ(U) dU = δ_{μ, λ̄}.                                  (3)
```

In particular:

```
∫ χ_{(1,0)} · χ_{(p,q)} dU = δ_{(p,q), (0,1)},                              (4a)
∫ χ_{(0,1)} · χ_{(p,q)} dU = δ_{(p,q), (1,0)}.                              (4b)
```

### Step 4: Partition function normalization

The heat-kernel measure is normalized as a probability density. Setting
`λ = (0,0)` (trivial rep, `d_{(0,0)} = 1`, `C_2(0,0) = 0`) and using
that all other reps integrate to zero against the trivial character:

```
Z_HK,1plaq(t) := ∫ P_t(U) dU = Σ_λ d_λ exp(-t·C_2/2) ∫ χ_λ dU
                             = Σ_λ d_λ exp(-t·C_2/2) δ_{λ, (0,0)}
                             = d_{(0,0)} · exp(0) = 1.                       (5)
```

### Step 5: Numerator — single-plaquette ⟨Re Tr U⟩

Combining (1), (2), (4):

```
∫ Re Tr U · P_t(U) dU
  = (1/2) ∫ (χ_{(1,0)} + χ_{(0,1)}) · Σ_λ d_λ exp(-t·C_2/2) χ_λ dU
  = (1/2) Σ_λ d_λ exp(-t·C_2/2) · [δ_{λ, (0,1)} + δ_{λ, (1,0)}]
  = (1/2) · [d_{(0,1)} exp(-t·C_2(0,1)/2) + d_{(1,0)} exp(-t·C_2(1,0)/2)].  (6)
```

By the conjugate-pair symmetry `(0,1) ↔ (1,0)`:

```
d_{(1,0)} = d_{(0,1)} = 3,                                                  (7a)
C_2(1,0) = C_2(0,1) = 4/3   (retained per SU3_CASIMIR_FUNDAMENTAL).         (7b)
```

Substituting (7) into (6):

```
∫ Re Tr U · P_t(U) dU = (1/2) · [3 · exp(-t·(4/3)/2) + 3 · exp(-t·(4/3)/2)]
                      = (1/2) · 6 · exp(-2t/3)
                      = 3 · exp(-2t/3).                                     (8)
```

### Step 6: Final result

```
⟨(1/N_c) Re Tr U⟩_HK,1plaq(t) = (1/3) · 3 · exp(-2t/3) / 1
                              = exp(-2t/3).                                 (T2)
```

At Block 01's `t(6) = 1`:

```
⟨P⟩_HK,1plaq(6) = exp(-2/3).                                                (T2.6)
```

The numerical value:

```
⟨P⟩_HK,1plaq(6) = 0.5134171190032592 ...                                    (T2.6, decimal)
```

## Theorem 2 (Block 02 deliverable)

**Theorem (T2).** Under heat-kernel measure `P_t(U)` on a single SU(3)
plaquette with Brownian time `t`, and using retained Casimir
`C_2(1,0) = 4/3` (premise C2):

```
⟨(1/N_c) Re Tr U⟩_HK,1plaq(t) = exp(-2 t / 3),
```

with the exact equality holding without character truncation (only the
fundamental and conjugate-fundamental representations contribute). At
Block 01's canonical Brownian time `t(6) = 1`:

```
⟨P⟩_HK,1plaq(6) = exp(-2/3) ≈ 0.5134171190.
```

**Proof.** Steps 1-6. ∎

## Comparison to Wilson at the same evaluation point

| Quantity | Closed-form expression | Numerical value |
|---|---|---|
| `⟨P⟩_W,1plaq(6)` (Wilson) | `(d/dβ) log J(β=6)`, `J` = SU(3) Bessel-det integral | 0.4225317396 |
| `⟨P⟩_HK,1plaq(6)` (heat-kernel, this block) | `exp(-2/3)` exact | 0.5134171190 |
| Lattice MC `⟨P⟩(6)` (full thermodynamic) | none — open problem | ≈ 0.5934 (comparator only) |

**Difference:** `⟨P⟩_HK,1plaq(6) - ⟨P⟩_W,1plaq(6) = 0.0908853794`,
about 21% relative to the Wilson value.

**Closeness to MC comparator:** `0.5934 - 0.5134 = 0.0800`, about
`264× ε_witness` where `ε_witness ≈ 3.030×10⁻⁴` is the bridge-gap
witness scale. This is the SINGLE-PLAQUETTE prediction; the
thermodynamic ⟨P⟩_HK(6) (Block 03 target) under Casimir-diagonal action
factorizes per plaquette and may close additional gap.

**Critically:** the comparison above shows that **the framework's
actually-derived single-plaquette value depends on which action is
forced** (Wilson vs heat-kernel). The two closed forms differ by ~21%,
not within ε_witness. The four cluster-obstruction lanes' downstream
quantitative chains (`u_0 = ⟨P⟩^(1/4)`, `α_s(v) = α_bare/u_0²`, etc.)
would shift accordingly under the two action choices.

## Structural contrast: closed-form vs Bessel-determinant

The Wilson single-plaquette generating function is an **infinite series**
in characters:

```
Z_W,1plaq(β) = ∫ exp(β·(1/N_c)Re Tr U) dU = Σ_λ c_λ(β),
c_λ(β) = Bessel-determinant character coefficient,
```

with `c_λ` a complicated transcendental function of β. The V=1 PF ODE
([`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md))
shows that this generating function satisfies a rank-3 holonomic ODE,
allowing exact-arithmetic evaluation, but the closed form involves
infinite-character truncation in character-space.

The heat-kernel single-plaquette generating function is **exactly two
characters**:

```
⟨Re Tr U⟩_HK,1plaq(t) = N_c · exp(-2t/3)
```

with no truncation. This **structural difference** — exact in finite
characters versus infinite-series Bessel — is the framework-internal
indication that heat-kernel may be the more "natural" Cl(3)-derived
action: it makes the framework's elementary expectations close in a
small finite number of Casimir-eigenmodes.

This is **suggestive but NOT load-bearing**. Action-form uniqueness
(Block 04 target) is the question of whether this closed-form
naturalness is a derivation criterion or a consequence of Casimir-
diagonal weighting.

## Status, scope, and what this does NOT close

```yaml
actual_current_surface_status: bounded support theorem
target_claim_type: bounded_theorem
conditional_surface_status: |
  Inherits Block 01's conditionals (a)-(d):
   (a) canonical Tr-form (retained at canonical-convention layer);
   (b) g_bare = 1 (open gate);
   (c) heat-kernel as Cl(3)-native action candidate (Block 04 open);
   (d) leading-order small-U matching as time-selection criterion.
  Plus Block 02-specific conditional:
   (e) the claim ⟨P⟩_HK,1plaq(6) = exp(-2/3) is for the SINGLE-plaquette
       evaluation under Casimir-diagonal HK measure. Multi-plaquette /
       thermodynamic evaluation is Block 03 target.
hypothetical_axiom_status: null
admitted_observation_status: |
  Schur orthogonality + heat-kernel character expansion are admitted
  standard machinery. Retained Casimir (C2) and Block 01's t = 1 are
  the load-bearing inputs. No PDG/MC values are load-bearing.
claim_type_reason: |
  Theorem (T2) is a closed-form derivation of the SU(3) heat-kernel
  single-plaquette expectation, given Block 01's derived t and retained
  Casimir. It is bounded support — useful as one input to the four
  cluster lanes IF heat-kernel is the framework's actually-derived
  action (Block 04 still open).
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- The previously-open question "what is the closed-form ⟨P⟩_HK,1plaq(6)?"
  is closed: `⟨P⟩_HK,1plaq(6) = exp(-2/3) ≈ 0.5134171190`, exact.
- The closed form is **exact in two characters** — no NMAX truncation
  needed. This is structurally distinct from Wilson's infinite-Bessel
  case.
- The numerical contrast `0.5134 (HK) vs 0.4225 (Wilson 1-plaq)`
  decisively shows that the framework's actually-derived single-plaquette
  value depends on the action choice. Block 04 must close which.

## What this does NOT close

- Block 03 target: thermodynamic `⟨P⟩_HK(6)` on full lattice with multi-
  plaquette correlations. The single-plaquette value is exact, but the
  multi-plaquette case requires evaluating the lattice partition function
  with HK plaquette weights and Wigner-Racah graph contractions — separate
  derivation.
- Block 04 target: action-form uniqueness. Does Cl(3) Tr-form actually
  force HK over Wilson? The closed-form-in-two-characters property is
  suggestive but not load-bearing.
- The four cluster-obstruction lanes (yt_ew M, gauge-scalar, Higgs mass,
  Koide-Brannen). Their quantitative dependence on the framework's
  derived ⟨P⟩(6) shifts under HK vs Wilson; both Block 03 (thermodynamic)
  and Block 04 (uniqueness) needed before the lanes can re-derive.

## Cross-references

- Predecessor (this loop): [`BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md) (Block 01)
- Sister Wilson side: [`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md) (V=1 PF gives Wilson 0.4225 single-plaquette)
- Casimir retained: [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
- Wilson-as-import: [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
- New-physics opening: [`BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)
- Standard methodology: same as Block 01 (Helgason; Liao 2004; Menotti-Onofri 1981; Drouffe-Zuber 1983)

## Command

```bash
python3 scripts/probe_hk_plaquette_closed_form.py
```

Expected output: exact-arithmetic verification of (T2) — Schur
orthogonality picks out exactly two characters, retained Casimir and
Block 01's t plug into the closed form to give `exp(-2/3)` symbolically
and `0.5134171190` numerically; cross-check against Wilson V=1 PF
single-plaquette 0.4225 to demonstrate the ~21% structural difference.
