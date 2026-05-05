# Plaquette Analytic Retained: Roadmap

**Date:** 2026-05-04
**PR:** [#528](https://github.com/jonathonreilly/cl3-lattice-framework/pull/528)
**Goal:** fully analytic SDP closure of `⟨P⟩(β=6)` from framework primitives

## Current state (committed in PR #528)

### What's built

1. **SDP infrastructure** (`scripts/frontier_su3_sdp_*.py`):
   - 5×5 Gram matrix [I, W(1,1), W(1,2), W(2,2), W(1,3)]
   - PSD constraint from RP A11 (framework-derived)
   - Wilson loop bounds, monotonicity, area-law lower bounds
   - CVXPY solver with SCS backend

2. **Wilson loop tower** (`scripts/frontier_su3_wilson_loop_*.py`):
   - Strong-coupling LO via Bessel-determinant character coefficients
   - L=4 and L=6 framework MC measurements for all 6 loops
   - Both analytic (no MC) and MC-pinned variants

3. **Bounds achieved**:
   - **MC-pinned SDP** (W tower from L=6 MC): `⟨P⟩(β=6) ∈ [0.5900, 0.6051]`
     - Width 2.5%, matches Anderson-Kruczenski/Kazakov-Zheng level
     - Contains standard MC L→∞ value 0.5934 ✓
   - **Fully analytic SDP** (no MC): `⟨P⟩(β=6) ∈ [0.4390, 1.0000]`
     - Wide bound (78% width)
     - Loose because no Migdal-Makeenko EQUALITY constraints

### What's missing for tight fully analytic bound

The gap between [0.439, 1.000] (analytic, loose) and [0.590, 0.605] (MC-pinned, tight) is bridged by **Migdal-Makeenko loop equations**. These are EXACT algebraic identities relating Wilson loops of different sizes, derived from path-integral invariance under link variations.

## Migdal-Makeenko equations: the missing piece

### The general loop equation

For SU(N) lattice gauge theory at coupling `β = 2N/g²`:

Take Wilson loop `W(C)` and apply path-integral invariance under
`U_l → e^{iε t_a} U_l` for link `l ∈ C`:

```
0 = ⟨∂_l W(C)⟩ - (β/N) ⟨W(C) ∂_l S⟩
```

Expanding and using SU(N) Fierz identity Σ_a (t_a)_{ij}(t_a)_{kl} = (1/2)(δ_{il}δ_{kj} - (1/N)δ_{ij}δ_{kl}):

```
(N²-1)/(2N²) · ⟨W(C)⟩ × (number of links in C)
  = (β/(2N²)) · Σ_{l ∈ C} Σ_{p containing l} [⟨W(C ⊕ p)⟩ - (1/N) ⟨W(C) · W(p)⟩]
```

Where `C ⊕ p` is the joined Wilson loop combining C with adjacent plaquette p.

### Specific form for 1×1 plaquette

For the simplest case `C = 1×1 plaquette P`:
- 4 links, each in 6 plaquettes (4D hypercubic, including P itself)
- "Joined" loops include: 1×2 rectangle, 2×1 rectangle, L-shape, T-shape (when joining out-of-plane)

The explicit equation involves:
```
(8/3) · ⟨P⟩ = (β/3) · [terms involving 1×2, 2×1 rectangles + out-of-plane joinings]
              - (β/9) · ⟨P²⟩ (Fierz singlet contribution)
              + (cluster decomposition terms)
```

For SU(3) at β=6, this is a specific equality constraint relating ⟨P⟩, ⟨W(1×2)⟩, ⟨P²⟩, and out-of-plane multi-plaquette correlators.

### Implementation challenges

Building this rigorously requires:

1. **Enumeration of all "joined" Wilson loops** for each base loop C:
   - For 1×1 plaquette: 4 links × 5 other-plaquettes-per-link = 20 joinings
   - But many joinings give equivalent loops by lattice symmetry
   - Need careful symmetry accounting

2. **SU(3) Fierz algebra** for trace identities:
   - Σ_a (t_a t_a) appearing in link integrations
   - Requires representation theory of SU(3) generators

3. **3D-specific loop topology**:
   - Out-of-plane joinings introduce 3D loops not just planar
   - Each gives different ⟨W⟩ contribution

4. **Higher-order corrections**:
   - Strong-coupling expansion to β^9 or β^13 (framework's mixed-cumulant
     theorem provides framework-derived corrections beyond β^5)

## Estimated effort to full analytic retained

| Phase | Effort (days) | Output |
|---|---:|---|
| 1. Specific MM equation for 1×1 plaquette | 3-5 | First non-trivial linear constraint |
| 2. MM equations for 1×2, 2×2 | 3-5 | More constraints, tighter SDP |
| 3. SU(3) Fierz library (reusable) | 3-5 | Foundation for higher loops |
| 4. Integrate into SDP, verify tight bound | 2-3 | Anderson-Kruczenski level (~3%) |
| 5. Extend to 6+ loop tower (Kazakov-Zheng level) | 5-7 | ~1-2% bound |
| TOTAL | **15-25 days** at AI cycle speed | Nature/Nobel-quality analytic closure |

## Alternative paths

### Path A: Susceptibility-flow ODE integration

Use framework's exact theorem `β_eff'(β) = χ_L(β)/χ_1plaq(β_eff(β))`
- Compute χ_1plaq exactly via Bessel formula
- Bound χ_L from framework primitives (cluster decomposition, etc.)
- Numerically integrate to get β_eff(6), hence P(6) = P_1plaq(β_eff(6))

Estimated: 5-7 days for ~1% bound.

### Path B: Padé-Borel resummation of mixed-cumulant series

Framework's mixed-cumulant theorem: P(β) = β/18 + β^5/472392 + O(β^9)
- Extend series to β^9, β^13, β^17 via higher-order cumulant theorems
- Apply Padé approximant or Borel summation
- Get analytic estimate at β=6 with controlled errors

Estimated: 7-10 days for ~5-10% bound.

### Path C: Full Anderson-Kruczenski (recommended)

Implement full MM equations as described above.
- Most rigorous, matches published bootstrap state of art
- Estimated: 15-25 days for ~1-3% bound

## Recommended sequence for Path 2

1. **Phase 1 (next 3-5 days)**: implement specific MM equation for 1×1 plaquette
   - Derive explicit SU(3) form via Fierz algebra
   - Add as equality constraint to SDP
   - Re-run, see how much the analytic bound tightens

2. **Phase 2 (5-7 days)**: extend to 1×2 and 2×2 loops
   - Build symmetry-aware loop joining enumerator
   - Add 2-3 more equality constraints to SDP

3. **Phase 3 (5-7 days)**: full tower with Kazakov-Zheng level constraints
   - 6-loop bootstrap with all relevant MM equations
   - Should achieve ~1-2% analytic bound

4. **Verification**: SDP bound should bracket standard MC L→∞ value 0.5934
   to within 1-2% precision.

## What "fully analytic retained" means

For ⟨P⟩(β=6) to reach `analytic_retained` status, the framework needs:

1. **Closed-form bound** (no MC): SDP gives [P_min, P_max] with P_min ≤ 0.5934 ≤ P_max
2. **All inputs framework-native**: RP A11, mixed-cumulant onset, isotropy theorem, MM equations all derivable from minimal axioms
3. **Bound tight enough for downstream physics**: ~1-2% (matches PDG α_s precision floor)
4. **Independent audit ratification**

This is the Nobel-quality analytic closure target.

For PRACTICAL purposes (downstream science already enabled):
- Numerical retained via L→∞ MC extrapolation (PR #528): SUFFICIENT
- Analytic retained: long-term Nobel goal, not blocking current work

## For the immediate session

Given the substantial Migdal-Makeenko engineering effort, the recommended
next concrete step is **either**:

**(A) Continue Path 2 deeply** — invest 1-2 weeks building the full MM
equations + tight SDP bound. Most ambitious, highest payoff.

**(B) Pivot to downstream science** with retained ⟨P⟩ — apply the now-
retained value in matter/EW/mass derivations. Per user's stated approach
("other workers can push downstream science"), this is parallelized.

**(C) Path A (susceptibility-flow ODE)** — alternative analytic path,
~5-7 days for ~1% bound. Less rigorous than full MM but tractable in a
shorter timeframe.

Per user's request "full analytic retained for this lane, the other workers
can push downstream science": option (A) is the canonical answer. The
SDP infrastructure is in place; the next sprint is MM equation implementation.
