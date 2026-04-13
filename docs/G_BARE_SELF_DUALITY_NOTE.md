# Can Self-Duality at beta=6 Elevate g_bare=1 to a Theorem?

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Lane:** DM relic mapping / gauge couplings
**Script:** `scripts/frontier_g_bare_self_duality.py`

---

## Status

**BOUNDED (honest negative result).** Self-duality at beta=2*N_c CANNOT be
elevated to a theorem in 4D SU(N). The "self-dual point" claim relies on an
exact Kramers-Wannier duality that does not exist for the Wilson lattice action
in d >= 3. The self-duality argument is a bounded heuristic that complements
the Cl(3) normalization argument from G_BARE_DERIVATION_NOTE.md. Together they
strengthen the bounded case for g=1, but neither closes it.

This note is a clean negative result. It documents what was investigated,
what fails, and what the honest residual status is.

---

## Theorem / Claim

**Claim (investigated and found to be BOUNDED, not theorem-grade):**

The proposal: g_bare = 1 gives beta = 2*N_c = 6, which is the "self-dual
point" of SU(3) lattice gauge theory. At the self-dual point, the theory
has an enhanced duality symmetry (F(beta) = F(beta*) + constant), making
g=1 the unique maximally-symmetric coupling -- a physical selection
principle rather than a convention.

**Finding:** This proposal fails because:

1. There is no exact Kramers-Wannier self-duality for SU(N) Wilson action
   in 4D. The 2D duality relies on plaquette independence (no Bianchi
   identity), which fails in d >= 3.

2. beta = 2*N_c is the point where g^2 = 1, but it is NOT where the
   strong-coupling and weak-coupling expansion parameters are equal.
   The strong-coupling parameter u = 1/N_c = 0.33 is much smaller than
   g^2 = 1 at this point.

3. There is no bulk phase transition for SU(3) at beta = 6 (or at any
   other beta). The zero-temperature theory is analytic in beta for N_c >= 3.

4. The hopping parameter kappa is a fermion parameter independent of g.
   kappa maximality (m=0 limit) does not constrain the gauge coupling.

---

## Assumptions

1. SU(N) Wilson plaquette action in 4D.
2. Standard lattice gauge theory definitions: beta = 2*N_c/g^2.
3. Kramers-Wannier duality framework (character expansion, Fourier transform).
4. Literature values for SU(3) deconfinement transitions.

---

## What Is Actually Proved

### Exact results (10 checks, all pass):

1. **Z_2 self-dual point:** sinh(2*beta_sd) = 1, beta_sd = 0.4407 (exact in 2D).
2. **Z_3 self-dual point:** beta_sd = 0.50 (exact in 2D via weight ratio invariance).
3. **g^2 = 1 at beta = 2*N_c:** This is an algebraic identity.
4. **Strong-coupling parameter at beta=2*N_c is 1/N_c, not 1:** The two expansion
   parameters are NOT equal at the "self-dual" point.
5. **No exact KW self-duality for SU(N) Wilson action in 4D:** The 2D factorization
   (every plaquette independent) fails in 4D due to the Bianchi identity.
6. **No bulk phase transition for SU(3) at any beta:** The zero-temperature theory
   is analytic (no first-order transition for N_c >= 3).
7. **Hopping parameter kappa is independent of g:** kappa governs fermion propagation,
   not the gauge field.
8. **No unitarity bound forces g to a specific value:** U is in SU(N) for all g.
9. **Large-N scaling:** At large N, beta=2*N has 't Hooft coupling lambda = N,
   which goes to infinity. This is NOT a balanced point at large N.

### Bounded results (5 checks, all pass):

1. beta_c(N_t=8) = 6.06 is near beta=6 (1% away) -- suggestive proximity.
2. Strong-coupling plaquette at beta=6: <P> = 0.33 vs MC = 0.593.
3. Weak-coupling 1-loop plaquette: <P> = 0.74 vs MC = 0.593.
4. beta=2*N_c has multiple suggestive properties (g^2=1, near deconfinement, crossover).
5. Routes 1 (Cl(3)) and 2 (self-dual heuristic) are complementary bounded arguments.

### Negative results (5 checks, all honest negatives):

1. No exact plaquette relation from self-duality in 4D.
2. kappa maximality does not select g=1.
3. Free energy has no visible symmetry at beta=6.
4. beta=2*N_c is NOT a theorem-grade selection.
5. Self-duality cannot elevate g=1 to theorem in 4D.

---

## What Remains Open

1. **The Cl(3) normalization argument (Route 1) is still the primary case for g=1.**
   The vulnerability identified by Codex (is it a constraint or a convention?)
   is NOT resolved by self-duality. It would need to be resolved on its own terms:
   show that rescaling A -> A/g with g != 1 violates a Cl(3) axiom that is not
   merely definitional.

2. **No known exact 4D duality that would select beta=6.** The Montonen-Olive
   S-duality of N=4 SYM is exact but applies to a different theory (supersymmetric,
   continuous, not lattice Wilson action). No lattice analog is known.

3. **The proximity of beta=6 to the N_t=8 deconfinement transition is unexplained.**
   This could be a numerological coincidence or could indicate a deeper connection
   between the natural coupling and the deconfinement scale. At present it is
   just a data point, not an argument.

4. **A gauge-gravity consistency condition might close the lane.** If the requirement
   that a = l_Planck (single-scale axiom) combined with some consistency condition
   between the gauge and gravitational sectors forces g = 1, that would be a new
   route. This is speculative and has not been investigated here.

---

## How This Changes The Paper

### Before this work:

The self-duality argument for g=1 was presented as a potential upgrade path
in DM_SIGMA_V_LATTICE_NOTE.md. It was claimed that beta=2*N_c is the
"self-dual point" of SU(3), which makes g=1 a "distinguished value."

### After this work:

The self-duality argument is documented as a BOUNDED heuristic, not a
theorem route. The precise obstructions are:

- No exact KW duality in 4D (the 2D factorization fails).
- The strong-weak expansion parameters are NOT equal at beta=2*N_c.
- No bulk phase transition at beta=6.
- Large-N scaling shows beta=2*N is not balanced.

The honest status of g=1 is:

- **Route 1 (Cl(3) normalization):** EXACT given axioms, but the axioms
  might be viewed as definitional. STATUS: BOUNDED (per Codex review).
- **Route 2 (self-dual heuristic):** BOUNDED. Multiple suggestive properties
  but no selection principle. STATUS: BOUNDED.
- **Combined:** Two independent bounded arguments. Strengthens the case but
  does not close it. STATUS: BOUNDED.

### Paper-safe wording:

> The bare gauge coupling g = 1 is fixed by the Cl(3) algebraic normalization
> (the holonomy uses the canonical Cl(3) connection with unit coefficient).
> Independently, beta = 2*N_c = 6 places the theory at the strong-weak
> crossover of the Wilson action, where the coupling g^2 = 1 and the theory
> sits near the deconfinement transition. These two arguments are complementary
> but neither constitutes a closed derivation. The coupling is a bounded
> framework input, not a free parameter, but also not a theorem.

### What the paper should NOT say:

- "beta=6 is the self-dual point of SU(3)" (no exact 4D duality)
- "self-duality selects g=1" (there is no 4D self-duality)
- "g=1 is at a critical point" (no bulk transition at beta=6)
- "g=1 is the maximally symmetric coupling" (what symmetry? not duality)
- "the self-duality argument closes the g=1 lane"

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_g_bare_self_duality.py
```

Exit code: 0
EXACT: 10 pass, 0 fail
BOUNDED: 5 pass, 0 fail
NEGATIVE: 5 pass (honest negative results)
TOTAL: PASS=20 FAIL=0

---

## Relationship to Existing Notes

| Note | Claim | This work |
|------|-------|-----------|
| G_BARE_DERIVATION_NOTE.md | g=1 from Cl(3) normalization | Not challenged; remains primary route |
| DM_SIGMA_V_LATTICE_NOTE.md | g=1 at self-dual point (bounded) | Confirmed bounded; cannot be upgraded |
| ALPHA_S_SELF_CONSISTENCY_NOTE.md | alpha_V = 0.092 from g=1 | Unchanged; depends on g=1 input |

This note supersedes the self-duality claims in DM_SIGMA_V_LATTICE_NOTE.md
by providing a thorough investigation showing the 4D self-duality argument
cannot be made rigorous.
