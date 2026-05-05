"""Path A: test framework's downstream α_s(M_Z) using P=0.4225 vs P=0.5934.

EXPLICIT FRAMEWORK-NATIVE vs IMPORTED labeling:

FRAMEWORK-NATIVE (Cl(3)/Z³ 3+1D primitives):
  - α_bare = 1/(4π) = 0.07958 (canonical Cl(3) connection norm, G_BARE_DERIVATION_NOTE)
  - u_0 = ⟨P⟩^(1/4) (tadpole improvement on V-invariant L_s=2 APBC)
  - α_LM = α_bare/u_0 (ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24)
  - α_s(v) = α_bare/u_0² (framework's lattice-scale α_s)
  - v = 246.282818290129 GeV (Higgs VEV / framework's lattice scale,
                              framework-derived from EW hierarchy theorem)

IMPORTED (per framework's own bounded scope in
QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md):
  - 2-loop SM RGE coefficients (Machacek-Vaughn 1984; Arason et al 1992)
  - PDG quark-mass thresholds: m_t=172.69, m_b=4.18, m_c=1.27 GeV
  - PDG-fit boundary values g_1(v)=0.46228, g_2(v)=0.65184, y_t(v)=0.93737, λ(v)=0.13
  - M_Z = 91.1876 GeV (PDG)

The framework EXPLICITLY documents this scope: "v → M_Z transfer is
standard SM 2-loop RGE infrastructure plus PDG quark-mass thresholds,
NOT a framework-native derivation."

So this test is the "framework boundary value + standard SM bridge"
combination that the framework already uses for its α_s(M_Z) lane. We just
swap the input P value and compare outputs.

Test:
  P = 0.5934 (MC anchor — framework's currently retained value)
  P = 0.4225 (framework's V-inv Schur native at L_s=2 APBC)
"""
import sys
sys.path.insert(0, 'scripts')

import numpy as np
from scipy.integrate import solve_ivp

PI = np.pi
M_Z = 91.1876
V_FRAMEWORK = 246.282818290129
ALPHA_BARE = 1.0/(4*PI)

# Standard QCD thresholds
M_T_POLE = 172.69
M_B_MSBAR = 4.18
M_C_MSBAR = 1.27

ALPHA_S_MZ_PDG = 0.1180
ALPHA_S_MZ_PDG_SIGMA = 0.0009

def b_3_one_loop(n_f):
    return -(11.0 - 2.0*n_f/3.0)

def beta_2loop_full(t, y, n_f_active):
    g1, g2, g3, yt, lam = y
    fac = 1.0/(16*PI**2)
    fac2 = fac**2
    g1sq, g2sq, g3sq, ytsq = g1**2, g2**2, g3**2, yt**2

    b1_1l = 41.0/10.0
    b2_1l = -(19.0/6.0)
    b3_1l = b_3_one_loop(n_f_active)

    beta_g1_1 = b1_1l * g1**3
    beta_g2_1 = b2_1l * g2**3
    beta_g3_1 = b3_1l * g3**3
    beta_yt_1 = yt * (9.0/2.0*ytsq - 17.0/20.0*g1sq - 9.0/4.0*g2sq - 8.0*g3sq)
    beta_lam_1 = (24.0*lam**2 + 12.0*lam*ytsq - 6.0*ytsq**2
                  - 3.0*lam*(3.0*g2sq + g1sq)
                  + 3.0/8.0*(2.0*g2sq**2 + (g2sq + g1sq)**2))

    beta_g1_2 = g1**3 * (199.0/50.0*g1sq + 27.0/10.0*g2sq + 44.0/5.0*g3sq - 17.0/10.0*ytsq)
    beta_g2_2 = g2**3 * (9.0/10.0*g1sq + 35.0/6.0*g2sq + 12.0*g3sq - 3.0/2.0*ytsq)
    beta_g3_2 = g3**3 * (11.0/10.0*g1sq + 9.0/2.0*g2sq - 26.0*g3sq - 2.0*ytsq)
    beta_yt_2 = yt * (-12.0*ytsq**2 + ytsq*(36.0*g3sq + 225.0/16.0*g2sq + 131.0/80.0*g1sq)
                      + 1187.0/216.0*g1sq**2 - 23.0/4.0*g2sq**2 - 108.0*g3sq**2
                      + 19.0/15.0*g1sq*g3sq + 9.0/4.0*g2sq*g3sq + 6.0*lam**2 - 6.0*lam*ytsq)

    return [fac*beta_g1_1 + fac2*beta_g1_2,
            fac*beta_g2_1 + fac2*beta_g2_2,
            fac*beta_g3_1 + fac2*beta_g3_2,
            fac*beta_yt_1 + fac2*beta_yt_2,
            fac*beta_lam_1]

def threshold_segments(t_start, t_end):
    thresholds = [
        (np.log(M_T_POLE), 6, 5),
        (np.log(M_B_MSBAR), 5, 4),
        (np.log(M_C_MSBAR), 4, 3),
    ]
    running_down = t_start > t_end
    thresholds.sort(key=lambda x: -x[0] if running_down else x[0])
    active = [(t_th, na, nb) for t_th, na, nb in thresholds
              if (t_end < t_th < t_start if running_down else t_start < t_th < t_end)]

    mu_start = np.exp(t_start)
    if mu_start > M_T_POLE: nf = 6
    elif mu_start > M_B_MSBAR: nf = 5
    elif mu_start > M_C_MSBAR: nf = 4
    else: nf = 3

    segments = []
    cur = t_start; nf_cur = nf
    for t_th, na, nb in active:
        segments.append((cur, t_th, nf_cur))
        cur = t_th
        nf_cur = nb if running_down else na
    segments.append((cur, t_end, nf_cur))
    return segments

def run_v_to_mz(g3_at_v, g1_at_v=0.46228, g2_at_v=0.65184, yt_at_v=0.93737, lam_at_v=0.13):
    """Run framework's 2-loop SM RGE from v to M_Z, return α_s(M_Z)."""
    t_v = np.log(V_FRAMEWORK)
    t_mz = np.log(M_Z)
    y_cur = [g1_at_v, g2_at_v, g3_at_v, yt_at_v, lam_at_v]
    for t_s, t_e, nfa in threshold_segments(t_v, t_mz):
        if abs(t_s - t_e) < 1e-12: continue
        sol = solve_ivp(lambda t, y: beta_2loop_full(t, y, nfa),
                        [t_s, t_e], y_cur, method='RK45',
                        rtol=1e-10, atol=1e-12, max_step=0.5)
        y_cur = list(sol.y[:, -1])
    g3_mz = y_cur[2]
    return g3_mz**2 / (4*PI)

def predict_alpha_s_mz(P_value):
    """Full framework chain: P → u_0 → α_s(v) → α_s(M_Z) via 2-loop SM RGE."""
    u_0 = P_value ** 0.25
    alpha_LM = ALPHA_BARE / u_0
    alpha_s_v = ALPHA_BARE / u_0**2
    g3_v = np.sqrt(4*PI*alpha_s_v)
    alpha_s_mz = run_v_to_mz(g3_v)
    return {
        'P': P_value,
        'u_0': u_0,
        'alpha_LM': alpha_LM,
        'alpha_s_v': alpha_s_v,
        'g_s_v': g3_v,
        'alpha_s_mz': alpha_s_mz,
        'dev_from_pdg': alpha_s_mz - ALPHA_S_MZ_PDG,
        'rel_dev_from_pdg': (alpha_s_mz - ALPHA_S_MZ_PDG) / ALPHA_S_MZ_PDG,
    }

print("="*78)
print("PATH A test: framework's downstream α_s(M_Z) at P = 0.5934 vs P = 0.4225")
print("="*78)
print(f"\nUsing framework's EXACT 2-loop SM RGE running")
print(f"(from scripts/frontier_qcd_low_energy_running_bridge.py)")
print(f"\nBoundary: α_s(v = {V_FRAMEWORK:.2f} GeV) → α_s(M_Z = {M_Z:.4f} GeV)")
print(f"With proper SM thresholds at m_t={M_T_POLE}, m_b={M_B_MSBAR}, m_c={M_C_MSBAR}")
print(f"PDG: α_s(M_Z) = {ALPHA_S_MZ_PDG} ± {ALPHA_S_MZ_PDG_SIGMA}")
print()

# Test 1: P = 0.5934 (MC anchor — framework's currently retained value)
result_5934 = predict_alpha_s_mz(0.5934)
# Test 2: P = 0.4225 (framework's V-inv Schur native prediction)
result_4225 = predict_alpha_s_mz(0.4225)

print("─"*78)
print(f"{'Quantity':30s} {'P=0.5934 (MC)':>20s} {'P=0.4225 (V-inv)':>20s}")
print("─"*78)
keys_to_show = ['P', 'u_0', 'alpha_LM', 'alpha_s_v', 'alpha_s_mz']
for key in keys_to_show:
    label = {'P': 'P (input)', 'u_0': 'u_0 = P^(1/4)',
             'alpha_LM': 'α_LM = α_bare/u_0',
             'alpha_s_v': 'α_s(v=246.28 GeV)',
             'alpha_s_mz': 'α_s(M_Z=91.19 GeV)'}.get(key, key)
    v1 = result_5934[key]
    v2 = result_4225[key]
    print(f"{label:30s} {v1:20.6f} {v2:20.6f}")
print("─"*78)
print(f"{'PDG α_s(M_Z) reference:':30s} {ALPHA_S_MZ_PDG:20.6f}")
print(f"{'Deviation from PDG:':30s} {result_5934['dev_from_pdg']:+20.6f} {result_4225['dev_from_pdg']:+20.6f}")
print(f"{'  as % of PDG:':30s} {100*result_5934['rel_dev_from_pdg']:+19.3f}% {100*result_4225['rel_dev_from_pdg']:+19.3f}%")
print(f"{'  as σ (PDG sigma=0.0009):':30s} {result_5934['dev_from_pdg']/ALPHA_S_MZ_PDG_SIGMA:+19.2f}σ {result_4225['dev_from_pdg']/ALPHA_S_MZ_PDG_SIGMA:+19.2f}σ")
print("─"*78)

# Diagnostic: how does dev change with P?
print()
print(f"Sensitivity scan: α_s(M_Z) vs P via the framework's 2-loop chain")
print(f"  {'P':>8s}  {'u_0':>8s}  {'α_s(v)':>10s}  {'α_s(M_Z)':>12s}  {'dev from PDG':>14s}")
for P_test in [0.40, 0.42, 0.4225, 0.45, 0.50, 0.55, 0.5934, 0.65, 0.70]:
    r = predict_alpha_s_mz(P_test)
    flag = ""
    if abs(r['dev_from_pdg']) < 0.0005: flag = "  ← ★ matches PDG within ~0.5σ"
    elif abs(r['dev_from_pdg']) < 0.0010: flag = "  ← within 1σ PDG"
    elif abs(r['dev_from_pdg']) < 0.0020: flag = "  ← within 2σ PDG"
    print(f"  {P_test:8.4f}  {r['u_0']:8.5f}  {r['alpha_s_v']:10.6f}  {r['alpha_s_mz']:12.6f}  {r['dev_from_pdg']:+14.6f}{flag}")

# Find the P value that EXACTLY matches PDG α_s(M_Z) = 0.1180
print()
print(f"Solving for P* such that α_s(M_Z) = PDG 0.1180 EXACTLY ...")
from scipy.optimize import brentq

def deviation(P):
    return predict_alpha_s_mz(P)['alpha_s_mz'] - ALPHA_S_MZ_PDG

P_star = brentq(deviation, 0.4, 0.7, xtol=1e-6)
r_star = predict_alpha_s_mz(P_star)
print(f"  P* = {P_star:.6f}")
print(f"  u_0(P*) = {r_star['u_0']:.6f}")
print(f"  α_s(M_Z) at P* = {r_star['alpha_s_mz']:.6f}  (matches PDG to within rounding)")

# Comparison
print()
print(f"  Distance from candidate P values:")
print(f"    |P* - 0.5934| = {abs(P_star - 0.5934):.4f}")
print(f"    |P* - 0.4225| = {abs(P_star - 0.4225):.4f}")

print()
print("="*78)
print("PATH A INTERPRETATION")
print("="*78)
print(f"""
Framework's chain α_s(M_Z) prediction:
  P=0.5934 (MC) → α_s(M_Z) = {result_5934['alpha_s_mz']:.4f}  (deviation {result_5934['dev_from_pdg']:+.4f}, {result_5934['dev_from_pdg']/ALPHA_S_MZ_PDG_SIGMA:+.1f}σ)
  P=0.4225 (V-inv) → α_s(M_Z) = {result_4225['alpha_s_mz']:.4f}  (deviation {result_4225['dev_from_pdg']:+.4f}, {result_4225['dev_from_pdg']/ALPHA_S_MZ_PDG_SIGMA:+.1f}σ)
  PDG: α_s(M_Z) = {ALPHA_S_MZ_PDG} ± {ALPHA_S_MZ_PDG_SIGMA}
  P* (exact PDG match): {P_star:.4f}

Conclusion:
  - At P=0.5934, framework's chain gives α_s(M_Z) = {result_5934['alpha_s_mz']:.4f}
    matching PDG to ~{abs(result_5934['rel_dev_from_pdg'])*100:.2f}% (this is the "designed" result)
  - At P=0.4225 (framework's actual V-inv Schur), α_s(M_Z) = {result_4225['alpha_s_mz']:.4f}
    deviation of {abs(result_4225['rel_dev_from_pdg'])*100:.1f}% from PDG ({result_4225['dev_from_pdg']/ALPHA_S_MZ_PDG_SIGMA:.1f}σ)
  - The P value that EXACTLY matches PDG α_s(M_Z) is P* = {P_star:.4f}

Implication for the campaign:
  The framework's downstream α_s(M_Z) is HIGHLY sensitive to P (chain has
  α_s(v) = α_bare/u_0² so changes in u_0 = P^(1/4) directly hit α_s).
  At P=0.4225, the framework predicts α_s(M_Z) significantly above PDG.
  This is EVIDENCE that V-invariance L_s=2 APBC alone does NOT capture
  the right gauge physics — the value 0.4225 is a finite-volume artifact
  and the framework needs L→∞ behavior (or V-invariance ↔ L→∞ proof) to
  reach P ≈ 0.59 needed for PDG match.

  The P* = {P_star:.4f} that fits PDG exactly is structurally close to
  MC's 0.5934, suggesting the framework's chain is anchored to the
  thermodynamic-limit gauge sector (which is what MC computes).

  This is a useful PATH A result: it shows the framework needs P ≈ 0.59
  (not 0.4225) to match PDG α_s downstream. The gap from 0.4225 to ~0.59
  is the genuine open derivation problem — and the campaign's target was
  not misframed after all (downstream physics REQUIRES the ~0.59 value).
""")
