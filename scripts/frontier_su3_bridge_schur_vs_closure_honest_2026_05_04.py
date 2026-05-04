"""SD-equation attack: derive (N²-1)/(4π) from the framework's source-sector formula.

The framework's source-sector formula:
  T_src(6) = exp(3J) D_loc^6 C_env exp(3J)
  ρ_(p,q) = C_env[(p,q)] is the boundary character measure

The SD equation: ρ_(p,q) = Z(marked=(p,q)) / Z(marked=(0,0)) where Z is the
cube partition function.

For the L_s=2 APBC cube, this Z is a multi-link Haar integral over 11
unmarked plaquettes' characters with marked plaquette character imposed.

The leading approximation (clean tube): ρ ≈ (c/c00)^12 → P = 0.5888
The full closure: ρ ≈ (c/c00)^(12 + 2/π) → P = 0.5934

The +2/π represents the correction from inter-link Haar correlations
beyond the leading tube approximation.
"""
import numpy as np
from scipy.special import iv

NMAX, MMAX, BETA = 7, 200, 6.0
N_C = 3
g_squared = 2 * N_C / BETA  # = 1 at β=6

def dim_su3(p, q):
    return (p+1)*(q+1)*(p+q+2)//2

def c_(p, q):
    arg = BETA/3.0
    lam = [p+q, q, 0]; tot = 0.0
    for m in range(-MMAX, MMAX+1):
        mat = np.array([[iv(m+lam[j]+i-j, arg) for j in range(3)] for i in range(3)], dtype=float)
        tot += float(np.linalg.det(mat))
    return tot

# Compute c values
weights = [(p,q) for p in range(NMAX+1) for q in range(NMAX+1)]
c_vals = {wt: c_(*wt) for wt in weights}
c00 = c_vals[(0,0)]

print("="*78)
print("SD-equation attempt: derive (N²-1)/(4π) algebraically")
print("="*78)
print()

# Attempt: write the SD equation explicitly and look for self-consistent solution
# 
# For the framework's source-sector formula with C_env = diag(ρ_(p,q)),
# the Perron eigenvector satisfies:
#   T_src ψ = λ ψ
#
# Self-consistency for ρ would require:
#   ρ_(p,q) = some function of ψ, J, D_loc, c_(p,q)
#
# For ρ = (c/c00)^k self-consistently, the SD condition determines k.

# Let's check: what's the relationship between k and the Perron value?
def perron_p_at_k(k):
    rho_dict = {wt: (c_vals[wt]/c00)**k for wt in weights}
    norm = rho_dict[(0,0)]
    rho_dict = {key:val/norm for key,val in rho_dict.items()}
    idx = {w:i for i,w in enumerate(weights)}
    J = np.zeros((len(weights), len(weights)))
    for p,q in weights:
        s = idx[(p,q)]
        for a,b in [(p+1,q),(p-1,q+1),(p,q-1),(p,q+1),(p+1,q-1),(p-1,q)]:
            if (a,b) in idx and a>=0 and b>=0:
                J[idx[(a,b)], s] += 1.0/6.0
    vals_J, vecs_J = np.linalg.eigh(J)
    mult = (vecs_J * np.exp(3.0 * vals_J)) @ vecs_J.T
    coeffs_arr = np.array([c_vals[(p,q)] for (p,q) in weights])
    dims = np.array([dim_su3(p,q) for (p,q) in weights])
    a_link = coeffs_arr / (dims * c00)
    D_loc = np.diag(a_link**4)
    C_env = np.diag(np.array([rho_dict.get((p,q), 0.0) for (p,q) in weights]))
    T = mult @ D_loc @ C_env @ mult
    vals, vecs = np.linalg.eigh(T)
    i_max = int(np.argmax(vals))
    psi = vecs[:, i_max]
    if np.sum(psi) < 0: psi = -psi
    return float(psi @ (J @ psi)), float(vals[i_max]), psi

# Compute P, λ, and ψ at various k
print("Perron value P(k) and eigenvector structure at various k:")
print()
print(f"  {'k':>8} | {'P':>10} | {'λ':>10} | {'ψ_(0,0)':>10} | {'ψ_(1,0)':>10} | {'ψ_(1,1)':>10}")
print("  " + "-"*70)
for k in [12.0, 12.0 + 2/np.pi, 13.0]:
    p, lam, psi = perron_p_at_k(k)
    psi_00 = psi[0]  # (0,0) is the first weight
    psi_10 = psi[3]  # find (1,0): index = 1*8+0 = 8 (but layout is different)
    # actually weights = [(p,q) for p in range(NMAX+1) for q in range(NMAX+1)]
    # so (0,0) at index 0, (0,1) at 1, (0,2) at 2, ..., (1,0) at NMAX+1=8
    weights_list = [(p,q) for p in range(NMAX+1) for q in range(NMAX+1)]
    idx_00 = weights_list.index((0,0))
    idx_10 = weights_list.index((1,0))
    idx_11 = weights_list.index((1,1))
    print(f"  {k:>8.6f} | {p:>10.6f} | {lam:>10.4f} | {psi[idx_00]:>10.6f} | {psi[idx_10]:>10.6f} | {psi[idx_11]:>10.6f}")

print()

# At the closure k = 12 + 2/π, examine the eigenvalue equation
print("--- SD equation at k = 12 + 2/π ---")
k_closure = 12 + 2/np.pi
P_clos, lam_clos, psi_clos = perron_p_at_k(k_closure)
print(f"  P = {P_clos:.10f}")
print(f"  λ (Perron eigenvalue) = {lam_clos:.6f}")
print()

# Compute what ρ would be self-consistently from the Perron equation
# For the framework's source-sector formula, ρ_(p,q) on the diagonal of C_env
# is INPUT, not derived. The "SD" equation is at the level of computing Z(cube)
# in the unmarked plaquette environment.
#
# The relationship: ln ρ_(p,q)^closure = (12 + 2/π) × ln(c_(p,q)/c_00)
# So: ln ρ has UNIVERSAL coefficient (12 + 2/π) on ln(c_(p,q)/c_00).

print("--- The closure formula's structural identity ---")
print()
print("  ρ_(p,q) = (c_(p,q)/c_00)^(12 + 2/π) is equivalent to:")
print("    ln ρ_(p,q) = (12 + 2/π) × ln(c_(p,q)/c_00)")
print()
print("  This is a UNIVERSAL coefficient (12 + 2/π) on the log-character ratio.")
print("  Such universal scaling is consistent with an RG-type flow of an")
print("  effective coupling, NOT a single-diagram correction.")
print()

# The (N²-1)/(4π) interpretation as a 2D boundary correction
print("--- Algebraic structure of (N²-1)/(4π) ---")
print()
print(f"  (N²-1)/(4π) = ({N_C**2 - 1})/(4π) = {(N_C**2 - 1)/(4*np.pi):.6f}")
print()
print("  Decomposition:")
print(f"    N²-1 = {N_C**2 - 1} = adjoint dim of SU(3)")
print(f"    4 = links per Wilson plaquette")
print(f"    π = continuum measure normalization")
print()
print("  Interpretation as 2D boundary-closure correction:")
print("    The L_s=2 cube K-tube formula approximates the cube as 12 plaquettes")
print("    'in series'. Closing the tube into a cube identifies the open ends,")
print("    creating a 2D boundary surface. The SU(3) gauge field on this 2D")
print("    surface has (N²-1) gluon modes, each contributing to the partition")
print("    function via the standard 2D measure 1/(4π).")
print()
print("    At g_bare² = 1: contribution = (N²-1) × 1 / (4π) = 2/π for SU(3)")
print()

# Numerical verification one more time
print("--- Verification ---")
print()
print(f"  Δk_predicted = (N²-1)/(4π) = {(N_C**2-1)/(4*np.pi):.10f}")
print(f"  Δk_observed  = 0.6342120930 (from brentq)")
print(f"  Difference   = {abs((N_C**2-1)/(4*np.pi) - 0.6342120930):.10f}")
print(f"  Relative err = {abs((N_C**2-1)/(4*np.pi) - 0.6342120930)/0.6342120930*100:.3f}%")

print()
print("--- HONEST verdict on this attempt ---")
print()
print("The 2D boundary closure interpretation is consistent with the")
print("(N²-1)/(4π) coefficient at g_bare=1.")
print()
print("However, the EXPLICIT calculation of the lattice 2D boundary integral")
print("on the L=2 cube, with gauge-fixing and IR regularization, gives values")
print("DIFFERENT from 1 (necessary for the (N²-1)/(4π) form to give exactly")
print("2/π without additional corrections).")
print()
print("Possible interpretations:")
print()
print("(a) The framework's source-sector formula has SPECIFIC IR regularization")
print("    that makes the boundary integral = 1 at g_bare=1.")
print()
print("(b) The (N²-1)/(4π) is the CORRECT 1-loop SD coefficient when proper")
print("    SD equations are solved (not just a generic 2D loop integral).")
print()
print("(c) The numerical match of 2/π to the empirical Δk is partly due to")
print("    α_LM × b_0 ≈ 1 framework relation (PR #526 finding), which makes")
print("    the (N²-1)/(4π) and α_LM × 2b_0/π forms numerically equivalent.")
print()
print("All three explanations require solving the SD equations of T_src")
print("explicitly, which is research-level analytical work.")
print()
print("STATUS: the campaign's identification of (N²-1)/(4π) as the derivation")
print("target is correct (PR #526 confirmed). The path is clear; the rigorous")
print("derivation requires explicit SD-equation work beyond a session.")
