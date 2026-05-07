# Final Synthesis — Cl(3) Action Derivation, 2026-05-07

## What was attempted

A fresh first-principles derivation of the framework's gauge action,
ignoring Wilson, heat-kernel, Manton, and the existing 4D Lagrangian
framing of the bridge gap.

**Strategy:**
1. Reframe from 4D Euclidean to 3+1 Hamiltonian (Z³ + emergent time
   matches the framework's substrate primitives).
2. Derive what's forced by Cl(3) Tr-form + RP + locality (electric
   sector forced; magnetic sector reduced to character coefficients
   `{m_λ}` with one continuum-matching constraint).
3. Test action-form ambiguity numerically on the simplest gauge-
   invariant SU(3) quantum mechanical observable.
4. Search for a Cl(3) algebraic principle that forces single-irrep
   (Wilson-form) magnetic operator.
5. Estimate multi-plaquette / lattice-density corrections.

## What was rigorously established

| Result | Status |
|---|---|
| Cl(3) primitives (A1+A2) force `N_c=3`, `T_F=1/2`, `C_2(fund)=4/3` | already known, recapped |
| 3+1 Hamiltonian framing is more parsimonious than 4D Lagrangian | **established** (uses A2 directly; doesn't import 4D Euclidean isotropy) |
| Electric sector of `H` forced exactly by Cl(3) Tr-form | **established** |
| Magnetic sector reduces to `Σ_λ m_λ Re χ_λ(U_p)` with one continuum-matching constraint | **established** |
| Action-form ambiguity persists at Hamiltonian ground-state level | **established numerically** (140% spread at g²=1) |
| `B.7` Cl(3)-primitive-operations argument forces Wilson-form magnetic operator under explicit "single-loop-traversal" minimality axiom | **established conditionally** (one new admitted axiom) |
| Single-plaquette KS toy at canonical Wilson-form, g²=1 gives ⟨P⟩ = 0.2181 ± 10⁻¹⁰ | **established numerically** (12 decimals stable at C₂≤16) |
| K-rescaling identity: `H_K(g²) ↔ H_1(g²/√K)` | **established analytically** |

## What turned out NOT to close

| Hoped-for closure | Reality |
|---|---|
| 3+1 Hamiltonian framing eliminates the action-form ambiguity | **REFUTED** — 140% spread at canonical g²=1 |
| Mean-field K=4 multi-plaquette gives 0.589 ≈ MC by new physics | **REFUTED** — K-scaling identity shows K=4 g²=1 = K=1 g²=0.5; this is a Wilson coupling rescaling, not new content |
| Cl(3) primitives force Wilson-form without additional axioms | **PARTIAL** — forces it conditional on "single-loop-traversal" minimality (a new admitted axiom A2.5) |

## The framework's actual first-principles prediction

Under:
- A1 (Cl(3) at sites)
- A2 (Z³ substrate)
- 3+1 Hamiltonian framing (uses A2 directly)
- Wilson-form magnetic operator (forced by B.7 + the proposed A2.5 minimality)
- Canonical Tr-form Cl(3) `Tr(T_a T_b) = δ_{ab}/2`
- Open `g_bare = 1` gate (admitted)
- Single-plaquette gauge-invariant SU(3) toy (the simplest non-trivial setup)

The framework predicts:

```
⟨P⟩_framework, single-plaquette KS, g²=1  =  0.218104  ±  10⁻¹⁰
```

Compared to lattice MC `⟨P⟩(β=6) = 0.5934`, **gap = 0.375**, far from
the bridge-gap tolerance `ε_witness ~ 3×10⁻⁴`.

## What that gap means

The 0.375 gap between framework single-plaquette KS prediction and 4D
isotropic Wilson MC at β=6 has three possible interpretations:

### (A) Single-plaquette toy is too small (finite-volume effect)

The toy has 1 effective gauge link / 1 plaquette. A real 3D KS lattice
has 3 plaquettes per site and 4 plaquettes per link with non-trivial
correlations. The thermodynamic limit could shift ⟨P⟩ substantially.

A genuine multi-link / multi-plaquette computation (DMRG, tensor
network, or KS Hamiltonian Monte Carlo) is required to test this.
Mean-field K-rescaling does NOT count — K-rescaling is mathematically
equivalent to coupling rescaling and contains no information beyond
the single-plaquette toy.

### (B) `g_bare = 1` is wrong

The framework's open `g_bare = 1` gate may resolve to a different value
of the canonical coupling. If the actually-derived `g_bare` corresponds
to KS `g² ≈ 0.5` instead of `g² = 1`, the single-plaquette toy gives
⟨P⟩ ≈ 0.589 — within 1% of MC.

This would mean: the bridge gap is essentially `g_bare` in the
3+1 Hamiltonian framing, not "what action functional".

### (C) The framework's actual theory is not Wilson-style continuous SU(3) lattice gauge theory

The framework's primitives might give a discrete spin-foam or
topological theory, where the bridge-gap target `⟨P⟩(β=6) = 0.5934`
is itself ill-posed.

This is the deepest possibility and remains untested.

## Genuinely new content vs prior work

| Prior bridge-gap work (4D Lagrangian) | This work (3+1 Hamiltonian) |
|---|---|
| Tested 7 routes within Wilson 4D framing — all exhausted | Reframed substrate from 4D Euclidean to 3+1 Hamiltonian |
| Found Wilson is admitted-as-import, not derived | Found electric sector IS forced; magnetic still has ambiguity, reduced from `S(U)` to `{m_λ}` |
| Action-form spread ~5-10% at finite β | Action-form spread 140% at canonical g²=1 in Hamiltonian |
| HK 1-plaq closed form: 0.5134 | Single-plaq KS: 0.2181 (Wilson-form), 0.0277 (HK-form) |
| Industrial SDP demoted as fallback | B.7 single-loop-traversal axiom proposed as bridge-gap closure path |
| 3 routes (A/B/C) to close, all hard | 3 candidate paths: A2.5 minimality + g_bare closure + multi-plaquette computation |

## Where the bridge gap actually moved to

**Pre-block**: "Find the framework's gauge action functional `S(U): SU(3) → ℝ`."

**Post-block** (this work): three independent open gates, any one of
which closes a portion of the bridge:

1. **A2.5 (minimality axiom)**: admit "single-loop-traversal" minimality
   as a framework primitive; under A2.5 + Block B continuum-matching,
   B.7 forces Wilson-form magnetic operator uniquely. **This is much
   weaker than admitting Wilson as a convention** — it admits a locality
   structure that derives Wilson, not Wilson itself.

2. **g_bare = 1 closure** (already an open gate): the canonical coupling
   `g²` value at the framework's evaluation point. If `g_bare` resolves
   to g²=0.5 instead of g²=1, the framework's prediction matches MC
   within 1% in the single-plaquette toy.

3. **Multi-plaquette ground-state computation**: requires DMRG / tensor
   network / Hamiltonian MC. The single-plaquette toy is structurally
   limited; a real multi-link computation is the proper test.

## Recommended next research steps

In order of difficulty:

1. **Adopt or argue for A2.5** as a framework axiom refinement.
   - Pro: closes the Block C 140% action-form ambiguity.
   - Con: introduces a new admitted axiom.
   - Justification candidates: substrate locality, operator-dimension
     RG argument, Cl(3) algebra cohomology.

2. **Probe `g_bare` resolution**: re-examine the `G_BARE_DERIVATION_NOTE`
   and its open audit verdict. Specifically test whether the canonical
   Cl(3) Tr-form gives `g_KS² = 1` or `g_KS² = 0.5` in the 3+1
   Hamiltonian framing (these differ by a factor of 2 from the 4D
   Lagrangian convention).

3. **Multi-link DMRG / iPEPS computation**: implement a 2-plaquette or
   small-lattice ground state with proper SU(3) Hilbert space
   truncation. Compare to single-plaquette toy, see if the prediction
   moves toward the MC value.

4. **Cl(3) spin-foam computation**: set up the SU(3)-recoupling spin-foam
   on a 3D cubical complex, compute the single-plaquette amplitude.
   This is the "no continuous action functional at all" possibility (C).

## Honest verdict

The 3+1 Hamiltonian reframing:
- **closes** one piece of the action problem (electric sector, fully forced),
- **reduces** another piece (magnetic sector, character coefficients),
- **transforms** a third piece (B.7 forcing under A2.5 minimality),
- **does not close** the bridge gap as a whole.

The framework's first-principles prediction in the single-plaquette KS
toy at canonical g²=1 is `0.218104`. This is a falsifiable number.
Whether it matches Nature depends on closing two more open gates
(A2.5 minimality, g_bare = 1) and one engineering computation
(multi-plaquette extrapolation).

The new-physics content is:
- 3+1 Hamiltonian framing is genuinely more parsimonious than 4D
  Lagrangian (better matches A2).
- The electric sector is forced exactly by Cl(3) Tr-form.
- The action-form ambiguity is a precise locality / minimality axiom
  away from being closed (A2.5).
- The bridge gap reduces from "what action functional" to "what
  locality axiom + what `g_bare` value", which is **substantively
  smaller** than the original problem.

This is the new-physics output the user asked for. It is not "the
bridge gap is closed". It is "the bridge gap has been refactored into
three smaller, more tractable open gates, with one clean numerical
prediction".
