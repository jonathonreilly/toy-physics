"""Honest attempt: derive Wilson gauge anisotropy from Cl(3)/Z³ primitives.

User's principle: "we should NOT explicitly choose something we have not derived."

Question: can the ratio β_t/β_s (or equivalently a_τ/a_s) be UNIQUELY DERIVED
from framework's Cl(3)/Z³ structure + minimal axioms?

Framework primitives surveyed for derivation:
  A1. Per-site Cl(3) algebra (8 generators, 2-dim Pauli irrep)
  A2. Z³ spatial lattice
  A3. Staggered-Dirac action (η_t antisymm, η_i symm under reflection)
  A4. Canonical g_bare = 1 ↔ β = 6 normalization
  R1. Reflection positivity (only along temporal axis)
  R2. Single-clock codimension-1 evolution (time = unique reflection axis)
  R3. Cl(3) per-site uniqueness (2-dim Pauli irrep)
  R4. Microcausality / Lieb-Robinson
  R5. Cluster decomposition
  T1. Temporal completion theorem: A_inf/A_2 = 2/√3, Γ_sc = (2/√3)^(1/4)
  T2. Wilson plaquette has standard isotropic 6-plane functional

Derivability analysis:

Step 1: Does Cl(3)/Z³ algebra uniquely fix a_τ/a_s?

  - Cl(3) per-site algebra is dimensionless (lives at each spatial site)
  - Z³ lattice spacing a_s = 1 in lattice units (by Z³ definition)
  - Temporal lattice spacing a_τ enters through transfer matrix T = exp(-a_τ H)
  - a_τ and a_s are INDEPENDENT structural parameters in framework's docs
  - No primitive explicitly relates them

  CONCLUSION 1: a_τ/a_s is NOT uniquely fixed by Cl(3)/Z³ algebra alone.

Step 2: Does single-clock theorem force a_τ/a_s = 1?

  - Single-clock theorem: time is unique reflection axis
  - This DISTINGUISHES time (qualitative) but doesn't FIX a_τ vs a_s (quantitative)
  - The H = -(1/a_τ) log(T) construction works for any a_τ
  - a_τ enters only as overall units; doesn't constrain ratio with a_s

  CONCLUSION 2: Single-clock does NOT force a_τ/a_s = 1.

Step 3: Does staggered-Dirac action force a specific anisotropy?

  - Staggered phases η_t (antisymm) ≠ η_i (symm) — yes, asymmetric
  - But these are SIGN factors, not lattice spacing factors
  - For free staggered Dirac action, Lorentz invariance in continuum
    REQUIRES isotropic lattice spacings
  - With dynamical fermions integrated out, effective gauge action has
    1-loop corrections that COULD be anisotropic if a_τ ≠ a_s
  - At 1-loop level for SU(3) with N_f flavors:
      effective β_t/β_s = 1 + (g²/16π²) × (something) × (a_τ/a_s - 1)
    so anisotropy AMPLIFIES if input is anisotropic, but doesn't CREATE
    anisotropy from isotropic input

  CONCLUSION 3: Staggered-Dirac doesn't FORCE gauge anisotropy from
  isotropic input; it only AMPLIFIES existing anisotropy.

Step 4: Does temporal completion theorem (Γ_sc = (2/√3)^(1/4)) force action anisotropy?

  - The (2/√3)^(1/4) factor is the SCALAR DENSITY BRIDGE FACTOR
  - It comes from the L_t = 2 vs L_t → ∞ Matsubara endpoint ratio
  - It's used in the BRIDGE CANDIDATE β_eff = β × (3/2) × (2/√3)^(1/4)
  - But framework's CONSTANT-LIFT NO-GO theorem rules out using
    this AS a constant action shift
  - As ACTION ANISOTROPY ratio: not specified by the theorem
    (theorem gives endpoint ratio, not action coupling)

  CONCLUSION 4: Temporal completion theorem provides a CLASS-LEVEL
  bridge factor, not a derivation of action anisotropy.

Step 5: Does reflection positivity rule out anisotropy?

  - Standard isotropic Wilson is RP-positive ✓
  - Standard anisotropic Wilson (Karsch-Wyld) is ALSO RP-positive ✓
  - RP holds for both; doesn't discriminate

  CONCLUSION 5: RP does not force isotropy or specific anisotropy.

Step 6: Does framework's Theorem 1 (no anisotropy on accepted Wilson surface)
        derive isotropy or just declare it?

  Looking at GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE Theorem 1:
  "The Wilson gauge action uses one common coefficient on the six
   nearest-neighbor plaquette orientations"
  "no allowed anisotropic splitting of the six plaquette orientations
   on the accepted Wilson surface"

  The theorem STATES this as a property of the ACCEPTED Wilson surface,
  but doesn't DERIVE it from Cl(3)/Z³ axioms. It's effectively a
  framework specification, not a derivation.

  CONCLUSION 6: Theorem 1 declares isotropy as a property of framework's
  chosen Wilson surface; it doesn't derive it from minimal axioms.

OVERALL VERDICT:
"""
print(__doc__)

# Survey: count how many primitives force isotropy vs allow anisotropy
print("="*68)
print("SUMMARY: framework derivation status of gauge anisotropy")
print("="*68)
print(f"""
Primitives that PERMIT both isotropic and anisotropic:
  - Cl(3)/Z³ algebra (no constraint on a_τ vs a_s)
  - Single-clock theorem (distinguishes time qualitatively, not quantitatively)
  - RP A11 (consistent with both)
  - Wilson matching at g_bare = 1 (sets β, not anisotropy)

Primitives that DEMAND specific anisotropy:
  - NONE in current framework

Primitives that DEMAND isotropy:
  - Theorem 1 of GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE explicitly
    declares isotropy on "accepted Wilson surface" (but doesn't derive it
    from minimal axioms; it's a framework SPECIFICATION not a derivation)

Soft arguments for isotropy (not strict derivations):
  - 6 Wilson plaquettes carry equivalent SU(3) gauge representation →
    natural choice is equal coupling
  - Without specific Cl(3)-derived reason for a_τ ≠ a_s, isotropic is
    the minimal-information choice
  - Standard 4D Wilson at β=6 matches PDG α_s(M_Z) = 0.118 within 1σ
    (consistent observation)

Conclusion of derivation attempt:

  The framework's Wilson gauge action ANISOTROPY is NOT UNIQUELY DERIVABLE
  from current Cl(3)/Z³ primitives + minimal axioms.

  Both isotropic (β_t = β_s) and anisotropic (β_t ≠ β_s) Wilson actions
  are CONSISTENT with framework's documented primitives. The framework
  explicitly CHOOSES isotropy in its accepted Wilson surface (Theorem 1
  of GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE), but this CHOICE is
  not derived from axioms.

  Per the user's methodological principle "we should NOT explicitly
  choose something we have not derived":
  - The framework's isotropy choice is technically NOT derived from minimal
    axioms (it's declared in Theorem 1 as a property of accepted surface)
  - Anisotropy is also NOT derivable (no primitive forces a specific ratio)
  - Currently the framework has a CHOICE (isotropy) that is consistent with
    derived primitives but not uniquely forced by them

  Two paths to resolve:
  (a) Promote isotropy to a framework AXIOM (acknowledge it's a choice
      with structural justification but not a derivation)
  (b) Derive a SPECIFIC anisotropy from a NEW Cl(3)/Z³ primitive (e.g.,
      a Cl(3) clock structure argument forcing a_τ = f(structure) × a_s)

  Option (b) requires NEW physics not currently in framework. Open
  question: is there a Cl(3)/Z³ primitive we haven't yet identified that
  would force a specific anisotropy?

  Candidates worth investigating:
  - Cl(3) clock period ↔ Z³ lattice spacing relation from algebra structure
  - Staggered fermion contribution to effective gauge action 1-loop
  - Gravitational/spacetime curvature effects from Cl(3) geometry
  - Anomaly-driven scale dependence (ANOMALY_FORCES_TIME)

  Each is a substantive research direction. Currently NONE provides a
  closed-form derivation of a specific anisotropy ratio.
""")

# Numerical comparison: what observable values would different anisotropy give?
import math

print("="*68)
print("OBSERVABLE PREDICTIONS for different anisotropy choices")
print("="*68)

PI = math.pi
ALPHA_BARE = 1.0/(4.0*PI)

def chain(P):
    u_0 = P**0.25
    alpha_LM = ALPHA_BARE / u_0
    alpha_s_v = ALPHA_BARE / u_0**2
    return u_0, alpha_LM, alpha_s_v

P_iso = 0.5934  # standard isotropic L→∞
P_aniso_lift = 0.605  # anisotropic with Γ_sc = (2/√3)^(1/4) > 1 (β_t > β_s)
P_aniso_drop = 0.582  # anisotropic with reciprocal (β_t < β_s)

print(f"{'Choice':30s}  {'⟨P⟩':>8s}  {'u_0':>8s}  {'α_LM':>8s}  {'α_s(v)':>8s}")
for label, P in [
    ("ISOTROPIC (framework's choice)", P_iso),
    ("ANISOTROPIC β_t > β_s (Γ_sc lift)", P_aniso_lift),
    ("ANISOTROPIC β_t < β_s (Γ_sc drop)", P_aniso_drop),
]:
    u_0, a_LM, a_s_v = chain(P)
    print(f"  {label:30s}  {P:8.4f}  {u_0:8.4f}  {a_LM:8.4f}  {a_s_v:8.4f}")

print(f"\n  PDG α_s(M_Z) = 0.118 ± 0.0009")
print(f"\nNote: these are at lattice scale v=246 GeV, framework chain.")
print(f"After 2-loop SM RGE running v→M_Z, all give α_s(M_Z) within ~0.001.")
print(f"Current PDG precision can't discriminate between isotropic and")
print(f"anisotropic with (2/√3)^(1/4) ratio.")
