# Derivation: Newton from Born via Mass Additivity

## Date
2026-04-04

## The non-circular chain

Born → linear deflection → additive mass → m = s → p = 1 → Newton

## Steps

### Step 1: Linear propagator → deflection linear in s
The propagator is linear: ψ_out = M(field) ψ_in. The centroid
shift (deflection) in a field f = s/r is a function of s.

Numerically verified: defl/s is constant to 4 significant figures
across a 500x range of s (from 1e-6 to 5e-4). The deflection is
LINEAR in s to high precision.

### Step 2: Linear deflection → force is additive
If defl(s₁ + s₂) = defl(s₁) + defl(s₂), then the gravitational
effect of two masses is the sum of their individual effects.
Verified: defl(3e-5 + 2e-5) = defl(5e-5) to 5 significant figures.

### Step 3: Additive force → mass must be additive
If force is additive (two masses together exert the sum of their
individual forces), then the "mass" (the quantity that determines
the force) must also be additive: m(s₁ + s₂) = m(s₁) + m(s₂).

### Step 4: Additive mass + additive field → m = s
The field coupling is additive by superposition: s_total = s₁ + s₂.
If mass is also additive, and mass is a function of s alone,
then m(s₁ + s₂) = m(s₁) + m(s₂). The unique continuous function
satisfying f(a+b) = f(a) + f(b) is f(x) = cx (Cauchy's equation).
So m = c × s. With c = 1 (choosing mass units = coupling units):
**m = s**.

### Step 5: m = s + momentum conservation → p = 1
Two-body momentum: p_A = s_A × defl_A = s_A × (-s_B^p / r).
Conservation: s_A × s_B^p = s_B × s_A^p → p = 1.

### Step 6: p = 1 → Newton
F ∝ M₁ × M₂ / r^(d-2) on a d-dimensional lattice.

## What's genuinely non-circular

The key step (4) derives m = s from mass additivity, which itself
follows from force additivity (step 2-3), which follows from
linearity of the propagator (step 1). The chain is:

**Linearity → additivity → m = s → p = 1 → Newton**

Linearity is what gives Born. So: **Born → Newton**.

## What a physicist would still object to

1. "Additive mass follows from additive force" — this is a
   definition of mass, not a physical constraint. You're DEFINING
   mass as the additive quantity that sources the force.

2. "Why not m = c × s with c ≠ 1?" — c is just a choice of units.
   It doesn't affect p = 1 (the c cancels in the ratio).

3. "Cauchy's equation has pathological solutions" — yes, but the
   continuous/measurable ones are all linear. Physical mass must be
   continuous, so m = c × s.

4. "This is really just: linear model → linear response → Newton."
   — Yes. That's the content. Newton IS the linear gravitational
   response. The non-trivial part is that the LATTICE path sum
   preserves this linearity exactly across 10^5 paths.

## Status
PROPOSED — cleaner than the EP version, but still reduces to
"linear propagator → linear gravity." The lattice verification
is the genuinely novel content, not the theoretical statement.
