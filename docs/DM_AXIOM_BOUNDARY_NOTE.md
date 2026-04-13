# DM Axiom Boundary: The Lattice-Is-Physical Axiom Controls the DM Lane

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Lane:** DM relic mapping (priority 3)
**Script:** `scripts/frontier_dm_axiom_boundary.py`
**Runner exit:** PASS=27 FAIL=0 (EXACT=8 DERIVED=6 LOGICAL=13)

---

## 1. Status

**EXACT OBSTRUCTION THEOREM** (same structure as generation axiom boundary).

The DM relic lane is bounded by exactly one irreducible axiom: the
lattice-is-physical axiom (A5). This is the SAME axiom that controls the
generation lane and the S^3 compactification lane. The DM lane does not
require any axiom beyond {A1-A5}.

The lane remains BOUNDED per review.md. This note does not upgrade the
lane status. It identifies the precise boundary: the "bounded" label on
the DM lane reduces to exactly the same foundational question as the
"bounded" label on generations and S^3.

---

## 2. Theorem / Claim

**Theorem (DM Axiom Boundary).**

Let the framework be defined by axioms:

- **(A1)** Cl(3) algebra: {G_mu, G_nu} = 2 delta_{mu,nu} on C^8.
- **(A2)** Z^3 lattice with staggered Hamiltonian.
- **(A3)** Hilbert space is tensor product over lattice sites.
- **(A4)** Unitary evolution: U(t) = exp(-iHt).
- **(A5)** Lattice-is-physical: Z^3 with a = l_Planck is the physical
  substrate, not a regularization of a continuum theory.

Then:

**(I) WITH A5:** g_bare = 1 follows from Cl(3) normalization (the lattice
is the UV completion, g cannot run, the algebra fixes it). sigma_v follows
from the lattice optical theorem. Coulomb potential from the lattice
Green's function. Boltzmann/Friedmann equations derived in the
thermodynamic limit. R = 5.48 with 0 imported inputs.

**(II) WITHOUT A5:** the lattice is a regularization. g_bare is a tunable
parameter (runs toward a->0). sigma_v must be imported from continuum
perturbative QFT. The DM ratio is not predicted.

**(III) SAME A5:** The irreducible axiom is the SAME A5 as for generations
(taste doublers are physical) and S^3 (lattice topology is physical).

**(IV) THERMODYNAMIC VS CONTINUUM LIMIT:** The thermodynamic limit
(N -> infinity at fixed a) is NOT the continuum limit (a -> 0). The DM
chain requires the thermodynamic limit (which exists). A5 forbids the
continuum limit (which would destroy the predictions).

---

## 3. Assumptions

1. **A1-A4:** Standard framework axioms (Cl(3) algebra, Z^3 lattice,
   Hilbert space, unitary evolution). Same as LQCD.
2. **A5:** Lattice-is-physical. This is the ONLY assumption beyond
   standard LQCD.

No additional assumptions are required for the DM lane beyond {A1-A5}.

---

## 4. What Is Actually Proved

### Block 1: WITH A5 (8 EXACT, 5 DERIVED checks)

- Cl(3) normalization {G_mu, G_mu} = 2I verified at all 3 generators.
- g_bare = 1 from Cl(3) normalization + A5.
- beta = 2*N_c/g^2 = 6.
- alpha_bare = g^2/(4pi) = 0.0796.
- sigma_v coefficient = pi from BZ phase space integral in thermodynamic limit.
- Lattice Green's function gives Coulomb-like potential.
- Stefan-Boltzmann convergence verified (lattice corrections expected at finite aT).
- R = 5.48 (0.2% from observed 5.47) from {A1-A5} alone.

### Block 2: WITHOUT A5 (4 LOGICAL checks)

- g_bare is tunable: in LQCD, g varies over [0.93, 1.04] at typical betas.
- sigma_v is a continuum QFT import, not a lattice prediction.
- V(r) is a continuum input, not a lattice output.
- R depends on arbitrary g_bare: not a prediction.

### Block 3: Thermodynamic vs continuum limit (4 checks)

- Wilson mass at hw=1 corners is nonzero, preserved in thermodynamic limit.
- Continuum limit destroys generations (hw>0 species decouple).
- A5 required to distinguish the two limits.
- DOS convergence verified numerically in thermodynamic limit.

### Block 4: Same A5 for all three lanes (5 LOGICAL checks)

- Generations: A5 makes taste doublers physical.
- S^3: A5 makes lattice topology physical.
- DM: A5 fixes g_bare = 1.
- DM chain uses only {A1-A5}: 10/11 steps use A5.
- No extra axiom required for DM lane.

### Block 5: Final axiom count (3 LOGICAL checks)

- The "bounded" label on g_bare IS the A5 question.
- R = 5.48 from {A1-A5} with 0 imports, 0 free parameters.
- All three lanes (generations, S^3, DM) reduce to the same A5.

---

## 5. What Remains Open

1. **A5 itself.** The lattice-is-physical axiom is an ontological commitment,
   not a derivable theorem. It is structurally parallel to foundational
   axioms in other theories (GR: spacetime is Riemannian; QM: states are
   Hilbert space vectors; SM: gauge group is SU(3)xSU(2)xU(1)). It cannot
   be proved or disproved within the mathematical framework.

2. **Overall DM lane status.** The lane remains BOUNDED per review.md. This
   note identifies the boundary precisely but does not upgrade the status.

3. **The A5 question is the same for all lanes.** A referee who accepts A5
   gets generations, S^3, AND R = 5.48. A referee who rejects A5 loses all
   three. There is no intermediate position.

---

## 6. How This Changes The Paper

### Key insight

The DM lane's "bounded" status was previously attributed to:

- g_bare = 1 being a "bounded normalization argument" (G_BARE_DERIVATION_NOTE.md)
- The Cl(3) normalization being possibly a "convention vs constraint"
  (Codex review finding 11)

This note shows these are the SAME question as the generation physicality
axiom (A5) and the S^3 compactification axiom (A5). The paper does not have
three separate "bounded" gaps -- it has ONE foundational axiom that controls
all three lanes simultaneously.

### Paper-safe wording

> The DM relic ratio R = 5.48 follows from axioms A1-A5 with zero imported
> inputs. The irreducible assumption is A5 (lattice-is-physical), the same
> axiom required for generation physicality and S^3 compactification. The
> bare coupling g = 1 is fixed by the Cl(3) algebraic normalization when
> the lattice is the UV completion (A5). Without A5, g is tunable, sigma_v
> must be imported, and R is not predicted.

### What the paper should NOT say

- "DM relic lane is CLOSED" -- it is BOUNDED (conditional on A5).
- "g_bare = 1 is derived independently of A5" -- it is not.
- "The DM prediction requires additional assumptions beyond generations"
  -- it does not; it requires the same A5.
- "The thermodynamic limit IS the continuum limit" -- they are different.

---

## 7. The Thermodynamic vs Continuum Limit Distinction

This distinction is central to the DM lane and requires A5:

| Property | Continuum limit (a -> 0) | Thermodynamic limit (N -> inf) |
|----------|--------------------------|-------------------------------|
| Parameter varied | a -> 0 | N -> infinity |
| What is fixed | L = Na | a = l_Planck |
| UV physics | Changes (Lambda_UV -> inf) | Unchanged |
| Generation structure | DESTROYED (1/8 tastes survive) | PRESERVED (all 8 tastes) |
| g_bare | Tunable (runs with a) | Fixed (g = 1 by Cl(3)) |
| Existence in framework | FORBIDDEN by A5 | EXISTS (universe is large) |
| sigma_v | Imported from continuum QFT | Derived from lattice optical theorem |
| R prediction | NOT predicted (g arbitrary) | R = 5.48 (0.2% from observed) |

Without A5, both limits are mathematically valid and the physicist chooses
the continuum limit (standard LQCD). With A5, only the thermodynamic limit
is physical.

---

## 8. DM Derivation Chain Axiom Audit

Every step in the DM chain traces to {A1-A5}:

| Step | Axioms used | Role of A5 |
|------|------------|------------|
| g_bare = 1 | A1 + A5 | Lattice is UV completion -> no running |
| beta = 6 | A1 + A5 | Algebraic consequence of g=1 |
| alpha_plaq = 1/(4pi) | A1 + A5 | Bare coupling at Planck scale |
| sigma_v = pi*alpha^2/m^2 | A1-A5 | Lattice optical theorem + thermo limit |
| V(r) = -C_F*alpha/r | A1-A5 | Lattice Green's function + thermo limit |
| Boltzmann equation | A1-A5 | Master equation on graph + thermo limit |
| Friedmann equation | A1-A5 | Poisson coupling + spectral rho |
| rho ~ T^4 | A1-A5 | Weyl's law on PL manifold + thermo limit |
| x_F = 25 | A1-A5 | Lattice freeze-out in thermo limit |
| g_star = 106.75 | A1-A4 | Taste spectrum counting (no A5 needed) |
| R = 5.48 | A1-A5 | Full chain |

10 of 11 steps use A5. Only the relativistic degrees of freedom count
(g_star) is purely algebraic from A1-A4.

---

## 9. Commands Run

```bash
python3 scripts/frontier_dm_axiom_boundary.py
```

Exit code: 0
EXACT: 8 pass, 0 fail
DERIVED: 6 pass, 0 fail
LOGICAL: 13 pass, 0 fail
TOTAL: PASS=27 FAIL=0

---

## 10. Relationship to Existing Notes

| Note | Status | This work |
|------|--------|-----------|
| G_BARE_DERIVATION_NOTE.md | BOUNDED normalization | Identifies "bounded" = A5 question |
| G_BARE_SELF_DUALITY_NOTE.md | BOUNDED negative result | Unchanged |
| DM_THERMODYNAMIC_CLOSURE_NOTE.md | BOUNDED thermo limit | Clarifies thermo limit requires A5 |
| DM_RELIC_GAP_CLOSURE_NOTE.md | BOUNDED gap closure | Identifies the gap as A5 |
| GENERATION_AXIOM_BOUNDARY_THEOREM_NOTE.md | EXACT obstruction | Same A5 identified here for DM |
| GENERATION_PHYSICALITY_DEEP_ANALYSIS.md | OPEN analysis | Same A5 identified as residual weakness |
