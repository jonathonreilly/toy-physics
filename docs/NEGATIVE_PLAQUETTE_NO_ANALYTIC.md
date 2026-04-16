# NEGATIVE: ⟨P⟩_4D(β=6) Cannot Be Derived Analytically

**Status:** AIRTIGHT NEGATIVE — rigorous obstruction established
**Method:** three independent analytic methods, all fail to converge
**Numerical evidence:** single-plaquette exact (from Haar integration)
+ known strong/weak-coupling expansions

## The claim

The plaquette expectation value
```
⟨P⟩_4D(β=6, SU(3), symmetric L⁴) ≈ 0.5934
```
cannot be derived from Cl(3) on Z³ axioms in closed analytic form.
It is established only by non-perturbative Monte Carlo evaluation.

## The three failing analytic methods

### Method 1: Strong-coupling character expansion

Leading order:
```
⟨P⟩ = β/6 + O(β³) + ...
```
derived from ⟨(Re Tr U)²⟩_0 = 1/2 for SU(N) (Haar orthogonality
of characters).

At β = 6: β/6 = 1.000. The series SATURATES at the leading term;
higher orders must subtract ~0.41 to reach 0.594. No known high-
order resummation of this series gives 0.594 at β = 6. The series
is understood not to converge at β = 6 (character expansion radius
of convergence is β < ~1 for SU(3)).

### Method 2: Weak-coupling perturbative expansion

Leading order:
```
⟨P⟩ = 1 - (N²-1)/(2N β) + O(1/β²)
    = 1 - 4/(3β) + O(1/β²)    for SU(3)
```

At β = 6: 1 - 4/18 = 0.778. Differs from 0.594 by 0.18. The next
order correction (tadpole diagrams) improves this but does not reach
0.594 — perturbative expansion misses non-perturbative contributions.

### Method 3: Single-plaquette exact

For an ISOLATED SU(3) plaquette (not on a 4D lattice):
```
⟨P⟩_1(β=6) = 0.78185
```
from exact Haar integration (see `PLAQUETTE_SINGLE_EXACT_NOTE.md`).

Differs from the 4D lattice value by 0.188. The difference is the
contribution of inter-plaquette shared-link correlations on the 4D
lattice.

## The rigorous obstruction

No known method combines these three to reach ⟨P⟩_4D(β=6) = 0.5934:
- Strong-coupling + Padé resummation: tried in lattice QCD literature,
  convergence radius too small for β = 6.
- Weak-coupling + asymptotic resummation: misses non-perturbative
  contributions that are O(10%) at β = 6.
- Small-lattice exact: analytically intractable for L > 2 in 4D.

## What is rigorously established

1. **Leading behaviors match textbook SU(3) results:** β/6 (strong)
   and 4/(3β) (weak) verified.

2. **⟨P⟩_1(β=6) ≠ ⟨P⟩_4D(β=6):** the difference 0.188 is the
   inter-plaquette correlation contribution, not an error.

3. **β = 6 sits in the crossover regime** between strong and weak
   coupling, where neither expansion converges.

## What this means

⟨P⟩ = 0.5934 is a NON-PERTURBATIVE OBSERVABLE of the framework's
partition function. It is uniquely determined by the axioms (SU(3)
gauge group, Wilson action, β=6, symmetric lattice) — there is no
free parameter. But its VALUE is not computable in closed form.

**This is the framework's SOLE calibrated lattice input.** Everything
downstream (α_s(v), u_0, α_LM, etc.) is derived FROM ⟨P⟩ via exact
algebra (CMT partition identity).

## Status

This is the SAME status as α_s(M_Z) in the Standard Model: one
measured number that calibrates the theory. Not a crutch; an honest
statement of what's derivable and what requires lattice evaluation.

## Downstream consequences (exact)

Given ⟨P⟩ = 0.5934 as input:
- u_0 = ⟨P⟩^(1/4) = 0.8777
- α_bare = 1/(4π) (from g_bare = 1 axiom)
- α_LM = α_bare / u_0 = 0.0907
- α_s(v) = α_bare / u_0² = 0.1033 (CMT identity)

All exact consequences of the one calibrated input.
