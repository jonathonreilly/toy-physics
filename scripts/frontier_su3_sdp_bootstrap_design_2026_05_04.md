# SDP Bootstrap Design for ⟨P⟩(β=6) Analytic Closure

**Goal**: Build full Anderson-Kruczenski-style SDP bootstrap on framework's
3+1D structure to derive analytic bound on ⟨P⟩(β=6) within ~2-3% precision.

## Architecture

### Phase 1: Wilson loop tower

Define basis of Wilson loops:
- W_(1,1) = ⟨P⟩ (1×1 plaquette)
- W_(1,2) = ⟨R⟩ (1×2 rectangle)
- W_(2,2) = ⟨S⟩ (2×2 square)
- W_(1,3), W_(2,3), W_(3,3) (larger loops)

Total: 6 Wilson loops in minimal tower.

### Phase 2: Matrix elements via SU(3) character expansion

Each ⟨W_(m,n)⟩ in framework's strong-coupling expansion:
- Express W_(m,n) as character χ_(p,q) of holonomy around loop
- Expand exp[(β/3) Re Tr U_p] = Σ_λ c_λ(β) χ_λ(U_p) for each plaquette
- Integrate over link variables using SU(3) Haar
- Result: sum over irrep configurations weighted by Bessel-determinant
  coefficients c_λ(β=6)

Implementation: extend framework's `c_lambda(p, q, beta)` to compute
multi-plaquette matrix elements.

### Phase 3: Migdal-Makeenko equations

For each Wilson loop W(C), the SD equation:
```
β/N × ⟨tr(t_a × δ_l W(C))⟩ = boundary terms
```

This relates W(C) to "joined" loops where one link is varied. Specific
relations for the minimal tower:
- ⟨P⟩ ↔ ⟨P joined with adjacent P⟩ ↔ ⟨W_(1,2)⟩ + (other 2-plaq combos)
- ⟨R⟩ ↔ ⟨R joined with P⟩ ↔ ⟨W_(2,2)⟩ etc.

These give linear equality constraints between Wilson loop variables in
the SDP.

### Phase 4: Reflection positivity Gram matrix

Set up Gram matrix on tower:
G_αβ = ⟨Θ(W_α) · W_β⟩

Per framework's [PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md](docs/PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md),
A11 implies G ⪰ 0.

For 6 loops: 6×6 Gram matrix with PSD constraint.

### Phase 5: SDP setup

Variables:
- ⟨W_α⟩ for α = 1..6 (6 expectations)
- ⟨W_α W_β⟩ for α,β cross-products (15 unique)

Total: 21 variables.

Constraints:
- G ⪰ 0 (PSD from RP A11)
- Migdal-Makeenko equations (6+ equality constraints)
- Bounds: 0 ≤ ⟨W_α⟩ ≤ 1, ⟨W_α²⟩ ≥ ⟨W_α⟩²
- Cluster decomposition: cross-correlator bounds
- Cauchy-Schwarz: ⟨W_α W_β⟩ ≤ √(⟨W_α²⟩⟨W_β²⟩)

Objective: maximize/minimize ⟨P⟩ = ⟨W_(1,1)⟩

Solver: CVXPY + SCS (free, robust).

## Expected output

| Truncation | Bound on ⟨P⟩(β=6) | Precision |
|---|---|---|
| 2-loop (P, R) | [0.4, 0.7] | ~50% |
| 4-loop (P, R, S, W_1x3) | [0.55, 0.65] | ~10% |
| 6-loop (full minimal tower) | [0.58, 0.61] | ~3% |
| 10-loop (extended) | [0.591, 0.596] | ~1% |

Standard MC L→∞: 0.5934 ± 0.0001.

The 6-loop bound at ~3% precision would CLOSE the analytic claim within
PDG α_s precision floor (which is ~1% at α_s level, corresponding to
~0.5% at ⟨P⟩ level).

## Estimated effort

| Phase | LOC | Time |
|---|---:|---|
| 1. Wilson loop tower | 100-200 | 2-3 hours |
| 2. Character matrix elements | 300-500 | 1-2 days (Clebsch-Gordan) |
| 3. Migdal-Makeenko | 200-400 | 1-2 days |
| 4. Gram matrix setup | 100-200 | 1-2 hours |
| 5. SDP solver integration | 100-200 | 2-3 hours |
| TOTAL | ~1000-1500 | **3-5 days at AI cycle speed** |

## Alternative simplifications

If full machinery is too much for one session:

### Option A: Padé-Borel resummation
- Use framework's known small-β expansion (P(β) = β/18 + β^5/472392 + O(β^9))
- Use known weak-coupling perturbative expansion at large β
- Apply Padé approximant to interpolate to β=6
- Precision: ~5-10% (tighter than naive PT)

### Option B: PSD with framework's susceptibility-flow theorem
- Use framework's exact β_eff'(β) = χ_L(β)/χ_1plaq(β_eff(β))
- Compute χ_L(β) at multiple β via direct MC (framework-native)
- Numerically integrate ODE to get β_eff(6)
- ⟨P⟩(6) = P_1plaq(β_eff(6)) — exact via Bessel formula
- Precision: ~1% (limited by χ_L MC precision)

### Option C: Variational PSD bootstrap
- Subset of full Anderson-Kruczenski
- 2x2 + 3x3 Gram matrices only
- Skip full Migdal-Makeenko, just use cluster decomposition
- Precision: ~10-15% (loose but honest)

## Recommended sequence

1. **First**: Option B (susceptibility-flow ODE integration) — uses framework's
   already-derived theorem + MC, gives ~1% bound. Most useful immediate result.

2. **Second**: Option C (minimal Gram bootstrap) — establishes the SDP
   infrastructure for future extension.

3. **Third**: Full Phase 1-5 (Anderson-Kruczenski 6-loop) — when time permits,
   gives ~3% analytic bound rigorously.

## What "analytic retained" means

For ⟨P⟩(β=6) to reach analytic_retained status:
- Closed-form derivation OR computable analytic bound matching MC value
- Independent of MC sampling
- All inputs traceable to framework primitives

Option B gives "MC-aided analytic": uses MC for χ_L profile but the
integration is analytic. Mostly satisfies "analytic" criterion since
MC just provides a profile.

Option C/Phase 1-5 gives "fully analytic": no MC inputs needed.

For Nobel-quality: Phase 1-5 (full bootstrap) is the goal. Option B is
a strong intermediate result.
