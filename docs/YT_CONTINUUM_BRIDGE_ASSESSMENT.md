# y_t Continuum Bridge: Honest Assessment of the Three Blockers

**Date:** 2026-04-13
**Lane:** Renormalized y_t matching
**Status:** BOUNDED -- all three blockers remain open, with a single shared root cause

---

## Executive Summary

The three y_t blockers (low-energy continuum running, alpha_s(M_Pl) chain,
lattice-to-continuum matching) all reduce to one question: does the lattice
Hamiltonian have a well-defined low-energy QFT description?

The answer is: almost certainly yes, but proving it from within the framework
requires invoking Wilsonian universality, which is standard physics -- not a
framework derivation. This is the irreducible residual. It cannot be closed
by further algebra.

---

## The Three Blockers

### Blocker 1: Low-Energy Continuum Running

**The claim:** SM RGE beta coefficients are computed from derived particle
content (gauge group, N_c, n_f, representations -- all retained). Running the
RGE is "just solving an ODE on derived inputs."

**What is actually derived:**
- The beta coefficients ARE derived. Every numerical input (N_c = 3, n_f = 6,
  gauge group, representations) follows from the retained framework surface.
- The ODE itself is a mathematical operation.

**What is NOT derived:**
- The RGE assumes a continuum QFT exists as the correct effective description
  at energies E << M_Pl.
- The existence of this continuum EFT is the thing that needs justification.
- The beta function formula itself (b_3 = 11*N_c/3 - 2*n_f/3, etc.) is
  derived in CONTINUUM perturbation theory. Applying it requires that the
  low-energy physics IS described by a continuum QFT.

**Honest verdict:** The beta coefficients are derived. The applicability of
the continuum RGE to the lattice's low-energy sector is not derived -- it is
assumed via Wilsonian universality.

### Blocker 2: alpha_s(M_Pl) Chain

**The chain:** g_bare = 1 (framework) --> alpha_lat = g^2/(4*pi) = 0.0796
--> alpha_V = 0.093 via 1-loop tadpole-improved matching.

**What is actually derived:**
- g_bare = 1 from Cl(3) normalization (framework axiom A5).
- alpha_lat is a definition.
- The Lepage-Mackenzie tadpole coefficient c_V^(1) = 2.136 is computable
  from lattice Feynman diagrams on the defined action.

**What is NOT derived:**
- The tadpole-improved matching to alpha_V is a lattice perturbation theory
  computation that assumes a continuum scheme (V-scheme) exists at the lattice
  scale.
- Converting alpha_V to alpha_MS-bar requires the existence of a continuum
  description.
- This is the same gap as Blocker 1: a continuum EFT must exist.

**Honest verdict:** g = 1 is framework. The chain to alpha_V is algebraic.
But interpreting alpha_V as a CONTINUUM coupling requires the same
universality bridge.

### Blocker 3: Lattice-to-Continuum Matching

**The claim:** At mu = 1/a = M_Pl, the matching step y_t^{MS-bar}(M_Pl) =
y_t^{lat}(a) * (1 + delta_match) is conditional on A5, the same axiom as
generation physicality.

**What is actually derived:**
- The lattice theory at the cutoff IS the UV completion (axiom A5).
- The bare relation y_t/g_s = 1/sqrt(6) is exact on the lattice (Ratio
  Protection Theorem, 32/32 checks).
- delta_match is perturbatively small: O(alpha_s/pi) ~ 3%.

**What is NOT derived:**
- The matching assumes there IS a continuum theory to match TO.
- The matching coefficient delta_match is computed in continuum perturbation
  theory -- the lattice side is known, but the continuum side requires that
  a continuum QFT exists as the effective description.

**Honest verdict:** The lattice side is exact. The continuum side requires
the same universality bridge.

---

## The Single Root Cause

All three blockers reduce to:

> Does the Cl(3) lattice Hamiltonian on Z^3 have a continuum QFT as its
> low-energy effective description?

If YES: all three blockers close simultaneously.
If NO (or UNPROVED): all three stay bounded.

---

## Can This Be Proved From Within the Framework?

### The standard physics argument (Wilsonian universality)

In standard lattice field theory, the universality theorem says: lattice
theories in the same universality class as a continuum QFT produce that QFT
at long distances. This is how lattice QCD works -- Wilson's lattice action
at finite spacing a gives continuum QCD as a --> 0.

### Why the standard argument does NOT directly apply

Our framework has NO continuum limit. The taste-physicality theorem
(retained) says the lattice spacing a = l_Planck is physical. There is no
a --> 0 limit. The lattice IS the theory at all scales.

This means:
- The framework is NOT in the universality class of any continuum QFT
  (universality classes are defined by the continuum limit).
- The standard universality theorem (which concerns the a --> 0 limit)
  does not apply in its textbook form.

### What CAN be said

Even without a continuum limit, the low-energy spectrum of the lattice
Hamiltonian CAN be described by an effective QFT. This is not the same as
universality -- it is Wilsonian effective field theory:

1. **The lattice Hamiltonian defines a quantum theory** with a Hilbert space,
   energy eigenstates, and a well-defined spectrum.

2. **At energies E << M_Pl = 1/a, lattice effects are suppressed** by
   powers of (E*a)^2 = (E/M_Pl)^2. This is a kinematic fact: modes with
   wavelength >> a do not resolve the lattice structure.

3. **The low-energy sector can be described by a local effective Lagrangian**
   organized as an expansion in E/M_Pl. The leading terms are dimension-4
   operators (renormalizable QFT). Higher-dimension operators are suppressed
   by (E/M_Pl)^n.

4. **The symmetries of the lattice (gauge invariance, Cl(3) structure)
   constrain the effective Lagrangian** to have the SM form: SU(3) x SU(2)
   x U(1) gauge theory with the derived matter content.

This is how condensed matter physics works: the lattice IS the fundamental
physics, but long-wavelength behavior is described by a continuum EFT. No one
doubts that the Hubbard model on a crystal lattice has a continuum
low-energy description, even though the crystal has no "continuum limit."

### The honest gap

The argument in points 1-4 above is physically compelling and almost
certainly correct. But it is NOT a theorem derived from the framework axioms.
It relies on:

- **Wilsonian EFT logic:** the claim that integrating out UV modes produces
  a local effective Lagrangian. This is standard physics -- it is the
  foundation of modern QFT -- but it is not proved from Cl(3) on Z^3.

- **Locality of the effective description:** the claim that the long-distance
  physics is LOCAL (described by a local Lagrangian density). This follows
  from cluster decomposition, which can be proved for gapped lattice systems
  but is more subtle for gapless (massless gauge) theories.

- **Universality of the leading terms:** the claim that the dimension-4
  operators dominate at low energies. This requires a mass gap or at least
  infrared regularity.

None of these are controversial in physics. But none are derived from the
framework axioms. They are consequences of general principles of quantum
mechanics and statistical mechanics applied to the lattice system.

---

## Can Any Blocker Be Closed Independently?

No. The three blockers are not independent. They are three manifestations
of the same gap:

| Blocker | What it needs | Root cause |
|---------|--------------|------------|
| SM running | Continuum RGE applies | Continuum EFT exists |
| alpha_s(M_Pl) | Lattice coupling maps to continuum scheme | Continuum EFT exists |
| Matching | Continuum theory to match to | Continuum EFT exists |

Closing any one without the others would be inconsistent: you cannot run
the SM RGE if you do not have a continuum EFT, and you cannot match to a
continuum theory that does not exist.

---

## The Irreducible Residual

**Statement:** The y_t prediction chain requires that the Cl(3) lattice
Hamiltonian on Z^3 at spacing a = l_Planck has a well-defined low-energy
effective quantum field theory description. This is physically compelling
(Wilsonian EFT logic, suppression of lattice artifacts by (E/M_Pl)^2,
symmetry constraints on the effective Lagrangian) but it is NOT derived
from the framework axioms. It is an application of standard Wilsonian
reasoning to the framework's lattice system.

**Nature of the gap:** This is not a "missing calculation" that could be
filled by doing more algebra. It is a structural feature: the framework
defines a lattice theory, and claiming predictions for continuum observables
(like m_t measured at colliders) requires a lattice-to-continuum bridge.
That bridge is Wilsonian EFT, which is standard physics, not framework-
derived physics.

**Comparison to other retained results:** The retained results (SU(2),
SU(3), 3+1, generations, etc.) are statements about the lattice theory
ITSELF -- its algebra, its spectrum, its symmetries. They do not require
a continuum EFT. The y_t prediction is different: it is a statement about
a CONTINUUM observable (the top quark pole mass) derived from the lattice
theory. This inherently requires the lattice-to-continuum bridge.

**Size of the residual:** Even granting the bridge, the matching
uncertainty is O(alpha_s/pi) ~ 3-10%. The current prediction m_t = 177 GeV
(2-loop with thresholds) overshoots by 2.4%, within this band.

---

## What the Paper Can Honestly Say

The paper can claim:

1. The bare relation y_t/g_s = 1/sqrt(6) is exact on the lattice (Ratio
   Protection Theorem, d=3 specific, non-perturbative).

2. The Planck-scale coupling alpha_s(M_Pl) = 0.093 follows algebraically
   from g_bare = 1 with zero free parameters.

3. Applying standard Wilsonian EFT reasoning to the lattice system, the
   low-energy effective theory is the SM with the derived gauge group and
   matter content. SM RGE running then gives m_t = 177 GeV (+/- 3-10%
   matching uncertainty).

4. This prediction has ZERO adjustable parameters.

The paper cannot claim:

1. That the continuum EFT is DERIVED from the framework. It is the
   expected low-energy description by Wilsonian reasoning, which is
   standard physics.

2. That the matching is "just A5." A5 says the lattice is physical. It
   does not say the low-energy physics is described by a continuum QFT.
   That requires Wilsonian EFT logic applied to the lattice system.

---

## Verdict

**Can any of the three blockers be closed?** No. They share a single root
cause (existence of a continuum EFT) that cannot be derived from the
framework axioms alone.

**Is this fatal?** No. The irreducible residual is the same bridge that
every lattice QFT calculation uses. Lattice QCD computes hadron masses on
a lattice and compares to continuum measurements -- nobody objects that
this requires Wilsonian universality. The difference here is that our
lattice has no continuum limit (taste-physicality), so the textbook
universality theorem does not apply in its standard form. The Wilsonian
EFT argument (points 1-4 above) still applies, but it is standard physics,
not a framework theorem.

**Paper-safe status:** BOUNDED. The UV theorem surface is strong (exact
ratio, zero free parameters). The low-energy bridge is physically
compelling but relies on standard Wilsonian EFT reasoning applied to the
framework's lattice system. The lane stays bounded until either:

(a) Someone proves a rigorous Wilsonian EFT theorem for the specific
    lattice Hamiltonian (hard, open problem in mathematical physics), or

(b) The paper accepts Wilsonian EFT as part of the standard mathematical
    toolkit (like Perelman for topology, Alexander trick for S^3) -- in
    which case all three blockers close simultaneously.

Option (b) is the honest path. Whether Codex accepts it is a judgment
call about what counts as "standard mathematical toolkit" vs "imported
physics."

---

## Assumptions

1. **A5 (lattice-is-physical):** Z^3 with Cl(3) at a = l_Planck is the
   physical theory.
2. **Retained surface:** Gauge group, matter content, generations all
   derived.
3. **Wilsonian EFT (NOT derived, standard physics):** The low-energy
   sector of the lattice Hamiltonian is described by a local effective
   QFT.
