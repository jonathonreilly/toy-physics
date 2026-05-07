# Bridge Gap — Heat-Kernel Thermodynamic ⟨P⟩(6) Stretch Attempt (Block 03)

**Date:** 2026-05-06
**Type:** stretch attempt + named obstruction
**Claim type:** open_gate
**Status:** stretch-attempt note + named obstruction packet on the
multi-plaquette / thermodynamic ⟨P⟩_HK(β=6) under heat-kernel Casimir-
diagonal action. NOT a closure. NOT a derivation of a specific
thermodynamic value. Documents what the Casimir-diagonal structure
buys (decisively cleaner than Wilson) and what residual non-perturbative
input is still needed.
**Authority role:** branch-local stretch-attempt source-note. Audit
verdict and effective status are set only by the independent audit
lane.
**Loop:** bridge-gap-new-physics-20260506 (Block 03 / R3.A)
**Branch (intended):** physics-loop/bridge-gap-new-physics-block03-20260506 (PR_BACKLOG — cluster cap hit at Block 02)

## Question

Given Block 01's `t(6) = 1` and Block 02's exact closed-form for
single-plaquette `⟨P⟩_HK,1plaq(6) = exp(-2/3) ≈ 0.5134`, can the
**multi-plaquette / thermodynamic** `⟨P⟩_HK(6)` on a 3+1D Wilson-style
lattice be derived in closed form (or to ε_witness precision) under
the framework's Casimir-diagonal action — a structural step that fails
for Wilson because of Bessel-determinant character coefficients?

## Setup

The thermodynamic Wilson plaquette under heat-kernel action on a
periodic 4D lattice Λ with `|P|` plaquettes and `|E|` directed links:

```
Z_HK,Λ(t) = ∫ Π_{p ∈ P} P_t(U_p) · Π_{e ∈ E} dU_e                          (1)
          = ∫ Π_p [Σ_{λ_p} d_{λ_p} exp(-t·C_2(λ_p)/2) χ_{λ_p}(U_p)] · DU.
```

Each plaquette holonomy `U_p` is a product of four (possibly inverted)
link variables. Expanding each character `χ_{λ_p}(U_p)` and using Schur
orthogonality on the link integrations gives a Wigner-Racah graph
trace.

## Step 1: Casimir-diagonal factorization (positive content)

The HK character expansion factorizes per plaquette into a Casimir-
suppressed weight times a character:

```
P_t(U_p) = Σ_{λ_p} W_λ(t) · χ_{λ_p}(U_p),
W_λ(t) := d_λ · exp(-t · C_2(λ) / 2).                                       (2)
```

This is structurally **simpler than Wilson**:

| Quantity | Wilson | Heat-kernel |
|---|---|---|
| Per-plaquette char weight | `c_λ(β)` (Bessel determinant) | `d_λ · exp(-t · C_2(λ)/2)` |
| t/β dependence | non-trivial Bessel ratio | exp(-t · C_2 / 2) — **factorizable** |
| Casimir-diagonal? | NO — `c_λ(β)` mixes Casimir / dimension non-trivially | YES — exact Casimir suppression |
| Closed form per-plaquette? | NO at finite-β | YES at any β=2N_c/g², t=g² |
| Single-plaquette ⟨Re Tr U⟩? | infinite Bessel series, requires V=1 PF ODE for closed form | exactly 2 characters via Schur |

**Theorem (Block 03 partial — Casimir-diagonal structure).** The
heat-kernel multi-plaquette partition function (1) admits an exact
character expansion of the form:

```
Z_HK,Λ(t) = Σ_{(λ_p)} (Π_p W_{λ_p}(t)) · F_Λ((λ_p)),                       (T3.a)
```

where the sum runs over irrep assignments `(λ_p)` to plaquettes, and
`F_Λ((λ_p))` is the **graph trace** computing the Wigner-Racah
contraction over link integrations. `F_Λ` is t-INDEPENDENT — it depends
only on the lattice geometry and the irrep labels, not on β/t.

This factorization separates the **β-dependent Casimir suppression** (in
W) from the **β-independent geometric data** (in F). For Wilson, the
analogous factorization fails because `c_λ(β)` is not separable into
"dimension × β-only function".

## Step 2: ⟨P⟩_HK in factored form

```
⟨(1/N_c) Re Tr U_{p_0}⟩_HK,Λ(t)
  = (1/N_c) · (1/2) · [⟨χ_{(1,0)}(U_{p_0})⟩ + ⟨χ_{(0,1)}(U_{p_0})⟩]_HK
  = (1/N_c) · Σ_{(λ_p)} (Π_p W_{λ_p}(t)) · F_Λ^{(p_0,1,0)}((λ_p)) / Z_HK,Λ(t),  (T3.b)
```

where `F_Λ^{(p_0,1,0)}` is the graph trace **with the marked plaquette
`p_0` carrying an extra `χ_{(1,0)}` insertion** beside its usual
`χ_{λ_{p_0}}`.

By Schur orthogonality, the link integrations on each link couple
`λ_{p_0}` and `(1,0)` characters at the marked plaquette into specific
SU(3) irrep block contributions, while the other plaquettes remain
in their original `λ_p` representations. The result is a Wigner-Racah
weighted sum over `(λ_p)`-tuples.

## Step 3: What this buys vs Wilson

In Wilson's strong-coupling expansion of `⟨P⟩(β=6)`, the famous open
problem is that the strong-coupling series has finite radius of
convergence (around β_c ≈ 5.7-5.9 deconfinement crossover), and the
β=6 evaluation point is at or past the radius — series diverges,
Padé/Borel resummation is non-rigorous.

For HK at canonical t=1 (Block 01), the analogous question is whether
the **t-expansion** of (T3.b) at small t around the strong-coupling
limit converges at t=1.

Here the factorized form (T3.a)+(T3.b) gives a structural advantage:
each term's t-dependence is `Π_p exp(-t·C_2(λ_p)/2)` — explicit
exponentials in t. The series in irrep labels `(λ_p)` is over a
**discrete lattice of Casimir values**:

```
Π_p exp(-t · C_2(λ_p) / 2) = exp(-t/2 · Σ_p C_2(λ_p)).                      (3)
```

For (λ_p) growing in total Casimir, the suppression is exponential.
At t = 1, the dominant contributions come from low-total-Casimir
configurations, which is a **finite, enumerable set** for any finite
threshold.

## Step 4: The remaining open question (Block 03 obstruction)

The structural advantage (Step 3) does NOT automatically close the
thermodynamic limit. Two open issues remain:

### Obstruction (O3.1): graph-trace combinatorics

`F_Λ((λ_p))` is the t-independent Wigner-Racah graph trace. For a
periodic 4D lattice, `F_Λ` involves contractions over `|E|` link
integrations, each producing 6j/9j-symbols. As `|Λ| → ∞`, the
combinatorial complexity of `F_Λ` grows exponentially.

For Wilson on the L_s=2 cube,
[`SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md`](SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md)
established a finite character-truncated computation giving 0.4291.
The same machinery adapted to HK weights (`d_λ exp(-t·C_2/2)` instead
of `c_λ(β)`) would give an analogous L_s=2 finite result.

But L_s=2 is structurally insufficient — per the exhausted-routes
consolidation (route 1.2), even with Wilson the L_s=2 cube gives gap
~543× ε_witness. HK at L_s=2 would similarly be insufficient for
ε_witness precision; **the thermodynamic limit `L → ∞` requires
controlled extrapolation**.

For HK, the controlled extrapolation has structural support that Wilson
lacks: each L_s contributes a Casimir-suppressed term, and the Casimir
spectrum gives an EXPONENTIAL DECAY in correlation length per plaquette.
But translating this into a rigorous thermodynamic-limit theorem
requires cluster-decomposition machinery + an exponential-decay
estimate, neither of which is currently a retained framework primitive.

### Obstruction (O3.2): convergence of the (λ_p)-sum at t=1

For SU(3), the smallest non-trivial Casimir is C_2(1,0) = 4/3, giving
suppression factor exp(-2/3) ≈ 0.5 per non-trivial plaquette. For a
lattice with `|P|` plaquettes, the leading correction to all-trivial
(λ_p ≡ (0,0)) is from configurations with one plaquette at (1,0) or
(0,1):

```
leading correction ~ |P| · exp(-t·(4/3)/2) · χ_{(1,0)}(...) ~ |P| · 0.5
```

For finite |P|, this correction is small. For `|P| → ∞`, it diverges
— the multi-plaquette HK partition function is NOT trivially evaluated
at t=1 by truncating to (1,0) sectors. Instead, the thermodynamic limit
involves a **strong-coupling expansion in `Π_p exp(-C_2/2)`** that
converges only if the Casimir gap (1,0)→(2,0) etc. compensates for
the |P|-growth — i.e., if there's an exponential clustering bound that
the framework's primitives don't yet provide.

This is structurally **the same kind of obstruction as Wilson's
β⁶-completion freedom** in
[`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md) —
the framework's retained primitives don't pin the multi-plaquette
correlation structure tightly enough to close the thermodynamic
limit, even for the cleaner HK action.

## Theorem 3 (Block 03 partial — named obstruction)

**Theorem (T3, partial closure).** Under heat-kernel measure with
canonical Brownian time `t = 1`:

(T3.a) The multi-plaquette partition function admits an exact
factorization:
`Z_HK,Λ(t) = Σ_{(λ_p)} (Π_p W_{λ_p}(t)) · F_Λ((λ_p))`
where `W_λ(t) = d_λ · exp(-t·C_2(λ)/2)` is per-plaquette Casimir-
suppressed weight, and `F_Λ((λ_p))` is the t-independent Wigner-Racah
graph trace.

(T3.b) The thermodynamic limit `⟨P⟩_HK(t = 1, Λ → ∞)` is a SPECIFIC
finite number determined by this factorization PLUS a controlled cluster-
decomposition / exponential-clustering estimate on the Casimir-graded
correlation structure.

(T3.c) **Open:** the cluster-decomposition / exponential-clustering
estimate is NOT in the framework's current retained primitive stack;
it is a non-perturbative input analogous to the Wilson β⁶-completion
freedom.

**Proof.** Step 1-4. ∎

## Status, scope, and what this does NOT close

```yaml
actual_current_surface_status: stretch_attempt + named_obstruction
target_claim_type: open_gate
conditional_surface_status: |
  Inherits Block 01-02 conditionals (a)-(e). Adds Block-03-specific:
   (f) the thermodynamic ⟨P⟩_HK(6) on Λ → ∞ depends on a controlled
       cluster-decomposition / exponential-clustering estimate that is
       NOT in the framework's retained primitive stack.
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Theorem (T3) closes the structural part of the multi-plaquette HK
  evaluation: (T3.a) the partition function factorizes into Casimir-
  suppressed plaquette weights × t-independent Wigner-Racah graph
  trace. (T3.b) the thermodynamic limit follows from this factorization
  PLUS a cluster-decomposition estimate. (T3.c) names the missing
  estimate as the bridge-gap-grade open obstruction.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- The structural form of the multi-plaquette HK partition function is
  decisively cleaner than Wilson: Casimir-diagonal factorization (T3.a)
  separates β-dependent from geometric data; Wilson's Bessel-determinant
  case does not factorize this way.
- The single-plaquette closed form (Block 02, exact in 2 characters)
  generalizes structurally — multi-plaquette is a Wigner-Racah graph
  trace over Casimir-suppressed irrep assignments.
- Names the ε_witness-grade obstruction sharply: the cluster-decomposition
  / exponential-clustering estimate on the Casimir-graded correlation
  structure.

## What this does NOT close

- A specific closed-form value for `⟨P⟩_HK(6)` in the thermodynamic
  limit. The factorization (T3.a) is exact but uncomputed.
- An L_s=2 finite-cube computation analogous to the Wilson case, which
  could be done via direct adaptation of `frontier_su3_cube_full_rho_perron_2026_05_04.py`
  to HK weights. (Recommended next-cycle task.)
- The cluster-decomposition / exponential-clustering estimate that
  bounds `|⟨P⟩_HK(6) - ⟨P⟩_HK,Λ_finite(6)|`.
- Block 04's action-form uniqueness question — Wilson vs HK uniqueness
  is the next cycle.

## Path forward (for Block 04 and beyond)

Two paths from here:

**Path A (computational, finite-cube):** adapt the existing L_s=2
cube full-ρ Perron runner to HK weights. Compute `⟨P⟩_HK,L_s=2(6)`
and compare to:
- Wilson L_s=2 cube: 0.4291
- Wilson 1-plaq: 0.4225
- HK 1-plaq (Block 02): 0.5134
- Lattice MC thermo: ≈ 0.5934

A clean L_s=2 HK computation should close to a specific value via the
same character-truncation machinery.

**Path B (analytic, thermodynamic):** derive the cluster-decomposition
/ exponential-clustering estimate from retained primitives (A11 RP,
Lieb-Robinson, single-clock, per-site Cl(3) dim 2). If retained
primitives suffice, the thermodynamic limit closes; if not, identify
the missing primitive as the next research target.

Both paths are next-cycle work, scoped beyond this stretch attempt's
~90m deep block.

## Cross-references

- Predecessor (this loop): [`BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md`](BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md) (Block 02)
- Sister Wilson L_s=2: [`SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md`](SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md) (Wilson L_s=2 = 0.4291)
- Wilson β⁶-completion freedom: [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)
- Existing cube Perron infra: [`scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py`](../scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py)
- Casimir retained: [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
- Standard methodology: same as Block 01-02 (Drouffe-Zuber 1983 "Strong coupling and mean field methods in lattice gauge theories" Phys Rep 102 contains the heat-kernel multi-plaquette character expansion in detail)
