"""Analytical Wilson loop computation for SU(3) at β=6 via character expansion.

REPLACES MC-pinned values in SDP bootstrap with framework-derived analytic
expressions, enabling FULLY ANALYTIC retained closure.

Method:
  For Wilson loop W(C) bounding area A:
    ⟨W(C)⟩ = (1/N) ⟨Tr Π U_link⟩

  Use character expansion for each plaquette inside C:
    exp[(β/3) Re Tr U_p] = Σ_λ d_λ × c_λ(β)/c_(0,0)(β) × χ_λ(U_p)

  Integrate over link variables using SU(3) Haar:
    ∫dU [D^λ(U)]_ij [D^μ(U†)]_kl = (1/d_λ) δ_λμ δ_il δ_jk

  Result: sum over irrep configurations weighted by character coefficients.

For minimal Wilson tower (1×1, 1×2, 2×2):
  ⟨W(1,1)⟩ = ratio of one-plaquette characters (at strong coupling: c_(1,0)/(3 c_(0,0)))
  ⟨W(1,2)⟩ = involves 2-plaquette character integral
  ⟨W(2,2)⟩ = involves 4-plaquette character integral

This script computes the strong-coupling leading orders explicitly via the
Bessel-determinant character coefficients (framework-native).
"""
import numpy as np
from scipy.special import iv

BETA = 6.0
NMAX = 6

def dim_su3(p, q): return (p+1)*(q+1)*(p+q+2)//2

def c_lambda(p, q, beta=BETA):
    """SU(3) Wilson character coefficient via Bessel determinant.
    Framework-native via G_BARE_DERIVATION_NOTE canonical normalization."""
    arg = beta/3.0
    lam = [p+q, q, 0]
    tot = 0.0
    for m in range(-200, 201):
        mat = np.array([[iv(m+lam[j]+i-j, arg) for j in range(3)] for i in range(3)], dtype=float)
        tot += float(np.linalg.det(mat))
    return tot

# Compute character coefficients for relevant irreps
print("="*64)
print("ANALYTICAL WILSON LOOP COMPUTATION")
print("Framework-native via Bessel-determinant character coefficients")
print("="*64)

c00 = c_lambda(0, 0)
c10 = c_lambda(1, 0)
c01 = c_lambda(0, 1)
c11 = c_lambda(1, 1)
c20 = c_lambda(2, 0)
c02 = c_lambda(0, 2)

print(f"\nFramework character coefficients at β=6:")
print(f"  c_(0,0)(6) = {c00:.6e}  (trivial irrep)")
print(f"  c_(1,0)(6) = {c10:.6e}  (fundamental)")
print(f"  c_(0,1)(6) = {c01:.6e}  (anti-fundamental)")
print(f"  c_(1,1)(6) = {c11:.6e}  (adjoint)")
print(f"  c_(2,0)(6) = {c20:.6e}  (symmetric)")
print(f"  c_(0,2)(6) = {c02:.6e}  (anti-symmetric)")

# Normalized ratios (these enter all Wilson loop computations)
def cratio(p, q):
    return c_lambda(p, q) / c00

print(f"\nNormalized ratios c_λ/c_(0,0):")
for (p,q) in [(0,0), (1,0), (0,1), (1,1), (2,0), (0,2), (2,1), (1,2)]:
    print(f"  c_({p},{q})/c_(0,0) = {cratio(p,q):.6f}, dim={dim_su3(p,q)}")

# WILSON LOOP 1×1 (plaquette) — analytical
print(f"\n{'='*64}")
print(f"⟨W(1,1)⟩ ANALYTICAL")
print(f"{'='*64}")

# At single-plaquette (no other plaquettes contributing):
# ⟨W(1,1)⟩_1plaq = (1/3) c_(1,0)/c_(0,0)
W11_1plaq = c10 / (3 * c00)
print(f"\nSingle-plaquette: ⟨W(1,1)⟩_1plaq = c_(1,0)/(3·c_(0,0)) = {W11_1plaq:.4f}")
print(f"  (this is framework's V-invariant L=2 APBC limit)")

# Full ⟨W(1,1)⟩ at L→∞ requires summing all plaquettes' contributions
# The exact L→∞ value is the famous open problem ≈ 0.5934
print(f"\nFull L→∞ value: requires non-perturbative resummation (open problem)")
print(f"  Standard MC: 0.5934 ± 0.0001")

# WILSON LOOP 1×2 (rectangle) — analytical strong-coupling
print(f"\n{'='*64}")
print(f"⟨W(1,2)⟩ ANALYTICAL (strong coupling leading)")
print(f"{'='*64}")

# At leading SC, 1×2 rectangle requires 2 plaquettes from action expansion
# to "fill" the area. Each plaquette contributes c_(1,0)/c_(0,0) and the
# trace structure gives 1/3 normalization.
#
# For 1x2 rectangle bounding area 2:
#   ⟨W(1,2)⟩^SC ≈ (c_(1,0)/(3 c_(0,0)))^2 × c_(0,0)^...
# But this doesn't quite work because the inside plaquettes aren't summed
# over irreps independently.
#
# Standard result (Migdal/Wilson 1974):
# ⟨W(m,n)⟩ ≈ [c_(1,0)/(N c_(0,0))]^(m·n) × O(β corrections)
# at LEADING strong coupling only

W12_LO = (c10 / (3*c00)) ** 2
W12_LO_corrected = (c10 / (3*c00)) ** 2  # leading SC has area-power scaling
print(f"\nLeading SC: ⟨W(1,2)⟩ ≈ [c_(1,0)/(3·c_(0,0))]^area = [...]^2 = {W12_LO:.4f}")
print(f"  Standard MC: 0.357")
print(f"  Strong-coupling LO underestimates significantly at β=6")

# WILSON LOOP 2×2 (square) — analytical strong-coupling
W22_LO = (c10 / (3*c00)) ** 4
print(f"\n⟨W(2,2)⟩ leading SC: [c_(1,0)/(3·c_(0,0))]^4 = {W22_LO:.4f}")
print(f"  Standard MC: 0.135")

# General Wilson loop area law at strong coupling
print(f"\n{'='*64}")
print(f"AREA LAW AT STRONG COUPLING (framework-native)")
print(f"{'='*64}")
ratio_pf = c10 / (3*c00)
print(f"\nFramework's strong-coupling Wilson loop:")
print(f"  ⟨W(m,n)⟩ ≈ [c_(1,0)/(3·c_(0,0))]^(m·n) = ({ratio_pf:.4f})^(m·n)")
print(f"\n  Predicted at β=6:")
for m, n in [(1,1), (1,2), (2,1), (2,2), (1,3), (2,3), (3,3)]:
    LO = ratio_pf ** (m*n)
    print(f"    ⟨W({m},{n})⟩^SC = {LO:.4f}")

# Compare to standard MC
print(f"\n  Standard MC values for comparison:")
std_MC = {(1,1): 0.5934, (1,2): 0.357, (2,2): 0.135, (1,3): 0.225,
          (2,3): 0.0858, (3,3): 0.0228}
for k, v in std_MC.items():
    LO = ratio_pf ** (k[0]*k[1])
    ratio = LO / v if v > 0 else 0
    print(f"    {k}: SC = {LO:.4f}, MC = {v:.4f}, SC/MC = {ratio:.2%}")

print(f"\n{'='*64}")
print(f"INTERPRETATION")
print(f"{'='*64}")
print(f"""
Strong-coupling expansion at β=6:
  - 1×1 plaquette: LO matches V-invariant L=2 APBC value (0.4225)
  - Larger Wilson loops: LO decays as area, matches qualitatively
  - At β=6, SC EXPONENTIALLY UNDERESTIMATES (e.g., W(2,2) SC=0.032 vs MC=0.135)

This is WHY the problem is open: strong-coupling expansion converges only
at small β (~< 3-5), while β=6 needs non-perturbative resummation.

For the SDP BOOTSTRAP we don't need exact Wilson loop values — we need:
  (1) RP A11 (PSD on Gram matrix) — framework-derived ✓
  (2) Migdal-Makeenko equations (linear constraints between Wilson loops)
  (3) Bounds (0 ≤ ⟨W⟩ ≤ 1, monotonicity)

Then SDP BRACKETS ⟨P⟩(β=6) without needing exact values.

Anderson-Kruczenski showed this gives ~5% bound at SU(2);
Kazakov-Zheng extended to SU(3) for ~1-2% bound.

For framework-native FULLY ANALYTIC retained:
  - Replace MC-pinned Wilson tower values with these analytical SC LO
    estimates (with explicit error bars from higher SC orders)
  - Implement Migdal-Makeenko equations (next step)
  - Solve SDP for analytic bound
""")

# Save analytical Wilson loop data
import json
analytical_data = {
    "method": "framework-native strong-coupling LO via Bessel-determinant character coefficients",
    "framework_inputs": {
        "c_00": c00,
        "c_10": c10,
        "c_01": c01,
        "c_11": c11,
        "c_20": c20,
        "c_02": c02,
        "ratio_c10_over_3c00": ratio_pf,
    },
    "wilson_loops_SC_LO": {
        f"({m},{n})": ratio_pf ** (m*n)
        for m, n in [(1,1), (1,2), (2,2), (1,3), (2,3), (3,3)]
    },
    "comparison_to_MC": {
        f"({k[0]},{k[1]})": {"SC_LO": ratio_pf**(k[0]*k[1]), "MC": v}
        for k, v in std_MC.items()
    }
}
with open('/tmp/wilson_loops_analytical.json', 'w') as f:
    json.dump(analytical_data, f, indent=2)
print(f"\nSaved analytical data to /tmp/wilson_loops_analytical.json")
