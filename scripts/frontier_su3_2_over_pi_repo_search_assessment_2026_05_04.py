"""SU(3) bridge Δk: thorough framework-internal search assessment.

Per user direction: 'step back and search for that across the repo to make
sure there are no other likely candidates'.

Investigated all framework-internal candidates that could give Δk = 0.6342.
Findings:

  - 2/π = (N²-1)/(4π) at g_bare=1 = 0.6366  (0.38% off, framework-PRIMITIVE)
  - α_LM × 2b_0/π = 0.6349                  (0.12% off, P-DEPENDENT - circular)
  - α_LM × 7 = 0.6347                       (0.07% off, but '7' has no derivation)
  - Cas(adj) × g²/(4π) = 3/(4π) = 0.239     (way off - wrong Casimir)

Key framework relation discovered: α_LM × b_0 ≈ 1 (within 0.3%).
If α_LM × b_0 = 1 exactly, then α_LM × 2b_0/π = 2/π (same form).
The 0.3% discrepancy means α_LM × b_0 = 1 is APPROXIMATE not EXACT.

Conclusion: (N²-1)/(4π) remains the best DERIVATION TARGET because:
  - Only candidate derivable from primitives without circular P-dependence
  - 0.4% residual consistent with 2-loop / RG-resummation scale
  - All P-dependent alternatives are circular
"""
import sys
import numpy as np

P_MC = 0.5934
alpha_bare = 1.0/(4*np.pi)
u_0 = P_MC**(1/4)
alpha_LM = alpha_bare/u_0
alpha_s = alpha_bare/u_0**2
b_0 = 11
delta_k_obs = 0.6342
EPSILON_W = 3.03e-4

def driver():
    print("="*78)
    print("SU(3) bridge Δk = 0.6342: thorough framework-internal search")
    print("="*78)
    print()

    print("Empirical exact closure: Δk_obs = 0.6342120930 (from brentq, PR #519)")
    print()

    print("Framework primitives at g_bare=1:")
    print(f"  α_bare = 1/(4π)     = {alpha_bare:.6f}")
    print(f"  u_0 = P^(1/4)       = {u_0:.6f}")
    print(f"  α_LM = α_bare/u_0   = {alpha_LM:.6f}")
    print(f"  α_s(v) = α_LM/u_0   = {alpha_s:.6f}")
    print(f"  b_0 (SU(3) pure)    = {b_0}")
    print()

    candidates = [
        ("α_LM x 7",                    alpha_LM*7,             "P-dependent, '7' unjustified"),
        ("α_LM x 2 b_0 / π",            alpha_LM*2*b_0/np.pi,   "P-dependent (circular)"),
        ("2/π = (N²-1)/(4π)",           2/np.pi,                "PRIMITIVE (framework-derivable)"),
        ("Cas(adj) × g²/(4π) = 3/(4π)", 3/(4*np.pi),            "primitive but wrong (Casimir N≠N²-1)"),
        ("α_s × 2 b_0 / π",             alpha_s*2*b_0/np.pi,    "P-dependent"),
        ("(N²-1) × α_LM",               8*alpha_LM,             "P-dependent"),
        ("α_LM x 11 = α_LM x b_0",      alpha_LM*b_0,           "P-dependent"),
    ]

    print(f"{'candidate':>40} | {'value':>10} | {'%err':>7} | derivability")
    print("-"*100)
    for (name, val, deriv) in sorted(candidates, key=lambda c: abs(c[1]-delta_k_obs)):
        err = abs(val-delta_k_obs)/delta_k_obs*100
        marker = " <-- best primitive" if "PRIMITIVE" in deriv else ""
        print(f"{name:>40} | {val:>10.6f} | {err:>6.2f}% | {deriv}{marker}")

    print()
    print("Key investigation: framework relation α_LM x b_0 ≈ 1?")
    print(f"  At MC P={P_MC}: α_LM x b_0 = {alpha_LM*b_0:.6f}")
    print(f"  Off from 1 by: {abs(alpha_LM*b_0 - 1)*100:.3f}%")
    print()
    print(f"  If α_LM x b_0 = 1 EXACTLY:")
    print(f"    u_0 = b_0 x α_bare = 11/(4π) = {11/(4*np.pi):.6f}")
    print(f"    P_predicted = u_0^4 = {(11/(4*np.pi))**4:.6f}")
    print(f"    vs MC P = {P_MC}")
    print(f"    Discrepancy: {abs((11/(4*np.pi))**4 - P_MC):.6f} (1.05%)")
    print()
    print("=> α_LM x b_0 = 1 would predict P = 0.587, MC gives 0.5934.")
    print("=> So α_LM x b_0 = 1 is NOT exact; the 0.3% discrepancy means the")
    print("   framework doesn't predict α_LM x b_0 = 1 from primitives alone.")
    print()

    print("--- ASSESSMENT ---")
    print()
    print("After thorough search:")
    print()
    print("CANDIDATE 1: 2/π = (N²-1)/(4π) at g_bare=1")
    print("  - Each factor framework-PRIMITIVE")
    print("  - 0.38% off Δk_obs (within ε_witness in P)")
    print("  - This is the BEST DERIVATION TARGET")
    print()
    print("CANDIDATE 2: α_LM x 2 b_0 / π")
    print("  - Tighter numerical match (0.12% off)")
    print("  - But α_LM depends on P (the very quantity we want to derive)")
    print("  - CIRCULAR for derivation purposes")
    print()
    print("CANDIDATE 3: α_LM x 7")
    print("  - Tightest match (0.07% off)")
    print("  - '7' has no clean derivation")
    print("  - Likely numerical coincidence, not structural")
    print()
    print("FINAL: (N²-1)/(4π) at g_bare=1 remains the correct derivation target.")
    print("       The path is unchanged by this thorough search.")
    print("       Open work: derive (N²-1)/(4π) from SD on T_src at g_bare=1.")

    return 0

if __name__ == "__main__":
    sys.exit(driver())
