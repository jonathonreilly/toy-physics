#!/usr/bin/env python3
"""
Higgs Mass Convergence with CORRECTED y_t = 0.918 (after sqrt(8/9) color projection)
=====================================================================================

PURPOSE: Verify m_H convergence pattern NOW that y_t is corrected to match SM.

Previous (uncorrected): y_t = 0.979 -> framework-SM gap ~24.7 GeV (order-independent).
Now (corrected):        y_t = 0.918 -> framework should track SM at each loop order.

FRAMEWORK INPUTS (all derived, zero imports):
  y_t(v)     = backward Ward * sqrt(8/9)  (~0.918)
  g_2(v)     = taste staircase * sqrt(9/8) (EW color projection)
  g_1(v)     = taste staircase * sqrt(9/8) (EW color projection)
  g_3(v)     = 1.139  (alpha_s = 0.1033)
  v          = 246.3 GeV

SM COMPARISON (y_t = 0.917, same procedure):
  g_2(v) = 0.653, g_1(v) = 0.462, alpha_s(m_t) ~ 0.1085

Self-contained: numpy + scipy only.
PStack experiment: higgs-mass-corrected-yt
"""

from __future__ import annotations
import sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

np.set_printoptions(precision=10, linewidth=120)

# =====================================================================
#  CONSTANTS
# =====================================================================

PI = np.pi
ZETA3 = 1.2020569031595943
ZETA4 = PI**4 / 90.0

FAC_1LOOP = 1.0 / (16.0 * PI**2)
FAC_2LOOP = FAC_1LOOP**2
FAC_3LOOP = FAC_1LOOP**3

N_C = 3
C_F = (N_C**2 - 1) / (2 * N_C)   # 4/3
C_A = float(N_C)                  # 3
T_F = 0.5

M_PL = 1.2209e19            # GeV
M_H_OBS = 125.25            # GeV
M_T_POLE_REF = 172.69       # GeV
M_B_MSBAR = 4.18
M_C_MSBAR = 1.27

# Framework-derived
PLAQ = 0.5934
R_CONN = (N_C**2 - 1.0) / N_C**2   # 8/9
SQRT_R_CONN = np.sqrt(R_CONN)       # sqrt(8/9) = 0.9428
SQRT_INV_R_CONN = np.sqrt(1.0 / R_CONN)  # sqrt(9/8) = 1.0607

U0 = PLAQ**0.25
ALPHA_BARE = 1.0 / (4.0 * PI)
ALPHA_S_V = ALPHA_BARE / U0**2      # 0.1033
C_APBC = (7.0 / 8.0)**0.25
ALPHA_LM = ALPHA_BARE / U0
V_DERIVED = M_PL * C_APBC * ALPHA_LM**16   # 246.3 GeV

G3_V = np.sqrt(4.0 * PI * ALPHA_S_V)   # 1.139

# Ward BC at M_Pl
G3_PL = np.sqrt(4.0 * PI * ALPHA_LM)
YT_PL = G3_PL / np.sqrt(6.0)

T_V = np.log(V_DERIVED)
T_PL = np.log(M_PL)

# SM comparison
V_OBS = 246.22
G1_SM = 0.462
G2_SM = 0.653
G3_SM = np.sqrt(4.0 * PI * 0.1085)
YT_SM = 0.917    # SM MSbar y_t at v (Buttazzo et al. convention)


# =====================================================================
#  EW COUPLINGS: TASTE STAIRCASE + sqrt(9/8) COLOR PROJECTION
# =====================================================================

def compute_ew_couplings_at_v():
    D_SPATIAL = 3
    G2_SQ_BARE = 1.0 / (D_SPATIAL + 1)     # 1/4
    GY_SQ_BARE = 1.0 / (D_SPATIAL + 2)     # 1/5
    TASTE_WEIGHT = (7.0 / 8.0) * T_F * R_CONN  # 7/18

    mu_k = [ALPHA_LM**(k / 2.0) * M_PL for k in range(5)]
    staircase = [
        (M_PL, mu_k[1], 14),
        (mu_k[1], mu_k[2], 10),
        (mu_k[2], mu_k[3], 4),
        (mu_k[3], V_DERIVED, 0),
    ]

    B_Y_RAW = -41.0 / 6.0
    B_2_SM = 19.0 / 6.0

    inv_aY = 1.0 / (GY_SQ_BARE / (4.0 * PI))
    inv_a2 = 1.0 / (G2_SQ_BARE / (4.0 * PI))

    for mu_hi, mu_lo, n_extra in staircase:
        if mu_lo >= mu_hi:
            continue
        L_seg = np.log(mu_hi / mu_lo)
        n_eff = n_extra * TASTE_WEIGHT
        delta_b_Y = n_eff * (-20.0 / 9.0)
        delta_b_2 = n_eff * (-4.0 / 3.0)
        b_Y_eff = B_Y_RAW + delta_b_Y
        b_2_eff = B_2_SM + delta_b_2
        inv_aY -= b_Y_eff / (2.0 * PI) * L_seg
        inv_a2 -= b_2_eff / (2.0 * PI) * L_seg

    alpha_Y_v = 1.0 / inv_aY
    alpha_2_v = 1.0 / inv_a2

    g1_gut_v = np.sqrt(4.0 * PI * (5.0 / 3.0) * alpha_Y_v) * SQRT_INV_R_CONN
    g2_v = np.sqrt(4.0 * PI * alpha_2_v) * SQRT_INV_R_CONN
    return g1_gut_v, g2_v

G1_V, G2_V = compute_ew_couplings_at_v()


# =====================================================================
#  BETA FUNCTIONS
# =====================================================================

def beta_1loop(t, y, n_f=6):
    g1, g2, g3, yt, lam = y
    g1sq, g2sq, g3sq = g1**2, g2**2, g3**2
    ytsq = yt**2

    dg1 = FAC_1LOOP * (41.0/10.0) * g1**3
    dg2 = FAC_1LOOP * (-19.0/6.0) * g2**3
    dg3 = FAC_1LOOP * (-(11.0 - 2.0*n_f/3.0)) * g3**3
    dyt = FAC_1LOOP * yt * (9.0/2.0*ytsq - 17.0/20.0*g1sq - 9.0/4.0*g2sq - 8.0*g3sq)
    dlam = FAC_1LOOP * (
        24.0*lam**2 + 12.0*lam*ytsq - 6.0*ytsq**2
        - 3.0*lam*(3.0*g2sq + g1sq)
        + 3.0/8.0*(2.0*g2sq**2 + (g2sq + g1sq)**2))
    return [dg1, dg2, dg3, dyt, dlam]


def beta_2loop(t, y, n_f=6):
    g1, g2, g3, yt, lam = y
    g1sq, g2sq, g3sq = g1**2, g2**2, g3**2
    ytsq = yt**2
    lamsq = lam**2

    bg1_1 = (41.0/10.0)*g1**3
    bg2_1 = (-19.0/6.0)*g2**3
    bg3_1 = (-(11.0 - 2.0*n_f/3.0))*g3**3
    byt_1 = yt*(9.0/2.0*ytsq - 17.0/20.0*g1sq - 9.0/4.0*g2sq - 8.0*g3sq)
    blam_1 = (24.0*lamsq + 12.0*lam*ytsq - 6.0*ytsq**2
              - 3.0*lam*(3.0*g2sq + g1sq)
              + 3.0/8.0*(2.0*g2sq**2 + (g2sq + g1sq)**2))

    bg1_2 = g1**3*(199.0/50.0*g1sq + 27.0/10.0*g2sq + 44.0/5.0*g3sq - 17.0/10.0*ytsq)
    bg2_2 = g2**3*(9.0/10.0*g1sq + 35.0/6.0*g2sq + 12.0*g3sq - 3.0/2.0*ytsq)
    bg3_2 = g3**3*(11.0/10.0*g1sq + 9.0/2.0*g2sq - 26.0*g3sq - 2.0*ytsq)
    byt_2 = yt*(-12.0*ytsq**2
        + ytsq*(36.0*g3sq + 225.0/16.0*g2sq + 131.0/80.0*g1sq)
        + 1187.0/216.0*g1sq**2 - 23.0/4.0*g2sq**2 - 108.0*g3sq**2
        + 19.0/15.0*g1sq*g3sq + 9.0/4.0*g2sq*g3sq
        + 6.0*lamsq - 6.0*lam*ytsq)
    blam_2 = (
        -312.0*lam**3 - 144.0*lamsq*ytsq - 3.0*lam*ytsq**2 + 30.0*ytsq**3
        + lamsq*(60.0*g2sq + 20.0*g1sq)
        + lam*(36.0/5.0*g1sq**2 - 8.0/5.0*g1sq*g2sq)
        + lam*ytsq*(-64.0*g3sq + 12.0*g2sq + 4.0/5.0*g1sq)
        + ytsq**2*(16.0*g3sq - 9.0/4.0*g2sq + 17.0/12.0*g1sq)
        + lam*(-73.0/8.0*g2sq**2 + 39.0/4.0*g2sq*g1sq + 629.0/120.0*g1sq**2)
        + 305.0/16.0*g2sq**3 - 289.0/48.0*g2sq**2*g1sq
        - 559.0/240.0*g2sq*g1sq**2 - 379.0/1200.0*g1sq**3)

    dg1 = FAC_1LOOP*bg1_1 + FAC_2LOOP*bg1_2
    dg2 = FAC_1LOOP*bg2_1 + FAC_2LOOP*bg2_2
    dg3 = FAC_1LOOP*bg3_1 + FAC_2LOOP*bg3_2
    dyt = FAC_1LOOP*byt_1 + FAC_2LOOP*byt_2
    dlam = FAC_1LOOP*blam_1 + FAC_2LOOP*blam_2
    return [dg1, dg2, dg3, dyt, dlam]


def beta_3loop(t, y, n_f=6):
    g1, g2, g3, yt, lam = y
    g1sq, g2sq, g3sq = g1**2, g2**2, g3**2
    ytsq = yt**2
    lamsq = lam**2
    g3_4 = g3sq**2
    g3_6 = g3sq*g3_4

    dy_2l = beta_2loop(t, y, n_f=n_f)

    # 3-loop g3
    b2_g3 = 2857.0/2.0 - 5033.0*n_f/18.0 + 325.0*n_f**2/54.0
    bg3_3 = -b2_g3*g3**7 + g3**5*ytsq*(-20.0) + g3**3*ytsq**2*6.0

    # 3-loop y_t (QCD anomalous dimension)
    gamma_2 = (
        -1249.0/27.0*C_F*C_A**2
        + (-48.0*ZETA3 + 140.0/27.0)*C_F**2*C_A
        + (32.0*ZETA3 - 68.0/27.0)*C_F**3
        + n_f*T_F*(160.0/27.0 - 32.0*ZETA3/3.0)*C_F*C_A
        + n_f*T_F*(32.0*ZETA3/3.0 + 4.0/27.0)*C_F**2
        + n_f**2*T_F**2*(-16.0/27.0)*C_F)
    byt_3_qcd = -yt*gamma_2*g3_6
    byt_3_mix = yt*(
        ytsq*g3_4*(-16.0*C_F**2 - 32.0/3.0*C_F*C_A + 8.0/3.0*C_F*n_f*T_F)
        + ytsq**2*g3sq*48.0*C_F - ytsq**3*12.0)
    byt_3_ew = yt*(ytsq*g2sq*g3sq*(-9.0) + ytsq*g1sq*g3sq*(-17.0/15.0))
    byt_3 = byt_3_qcd + byt_3_mix + byt_3_ew

    # 3-loop lambda
    c_g4y4 = (-192.0*C_F**2*(1.0 + 4.0*ZETA3/3.0)
              + 96.0*C_F*C_A*(-3.0/2.0 + ZETA3)
              - 32.0*C_F*T_F*n_f*(1.0 + 4.0*ZETA3/3.0)
              + 64.0*C_F**2*C_A*ZETA3 - 96.0*C_F*C_A*ZETA3)
    blam_3 = c_g4y4*g3_4*ytsq**2
    blam_3 += (96.0*C_F*(1.0 + 12.0*ZETA3) - 24.0*(3.0 + 8.0*ZETA3))*g3sq*ytsq**3
    blam_3 += (-60.0 - 288.0*ZETA3 + 32.0*ZETA4)*ytsq**4
    blam_3 += 192.0*C_F*(C_F + C_A/2.0)*g3_4*ytsq*lam
    blam_3 += (-96.0*C_F*(3.0 + 4.0*ZETA3))*g3sq*ytsq**2*lam
    blam_3 += (72.0 + 288.0*ZETA3 - 96.0*ZETA4)*ytsq**3*lam
    blam_3 += lamsq*(g3sq*ytsq*128.0*C_F - ytsq**2*12.0 + lam*ytsq*120.0)
    blam_3 += lam**3*(-312.0*lam + 192.0*ytsq - 72.0*g2sq)
    blam_3 += ytsq**2*(g2sq**2*(-3.0) + g1sq**2*(-1.0/3.0)
                        + g2sq*g3sq*16.0*C_F + g1sq*g3sq*16.0/9.0*C_F)

    bg1_3 = g1**3*g1sq*(g1sq*(-388613.0/18000.0) + g2sq*(-1677.0/200.0)
                         + g3sq*(3404.0/225.0) + ytsq*(-2827.0/200.0))
    bg2_3 = g2**3*g2sq*(g2sq*(324953.0/1800.0) + g1sq*(-593.0/120.0)
                         + g3sq*(76.0/3.0) + ytsq*(-729.0/8.0))

    dg1 = dy_2l[0] + FAC_3LOOP*bg1_3
    dg2 = dy_2l[1] + FAC_3LOOP*bg2_3
    dg3 = dy_2l[2] + FAC_3LOOP*bg3_3
    dyt = dy_2l[3] + FAC_3LOOP*byt_3
    dlam = dy_2l[4] + FAC_3LOOP*blam_3
    return [dg1, dg2, dg3, dyt, dlam]


# =====================================================================
#  RGE UTILITIES
# =====================================================================

def run_segment(y0, t_start, t_end, beta_fn, n_f=6, max_step=0.5):
    def rhs(t, y):
        return beta_fn(t, y, n_f=n_f)
    sol = solve_ivp(rhs, [t_start, t_end], y0,
                    method='RK45', rtol=1e-10, atol=1e-12, max_step=max_step)
    if not sol.success:
        raise RuntimeError(f"RGE failed: {sol.message}")
    return sol


def run_with_thresholds(y0, t_start, t_end, beta_fn, max_step=0.5):
    thresholds = [
        (np.log(M_T_POLE_REF), 6, 5),
        (np.log(M_B_MSBAR), 5, 4),
        (np.log(M_C_MSBAR), 4, 3),
    ]
    running_down = t_start > t_end
    thresholds.sort(key=lambda x: -x[0] if running_down else x[0])
    active = [(t_th, na, nb) for t_th, na, nb in thresholds
              if (t_end < t_th < t_start if running_down else t_start < t_th < t_end)]

    mu_start = np.exp(t_start)
    if mu_start > M_T_POLE_REF: nf = 6
    elif mu_start > M_B_MSBAR:  nf = 5
    elif mu_start > M_C_MSBAR:  nf = 4
    else:                       nf = 3

    segments = []
    cur = t_start
    nf_cur = nf
    for t_th, na, nb in active:
        segments.append((cur, t_th, nf_cur))
        cur = t_th
        nf_cur = nb if running_down else na
    segments.append((cur, t_end, nf_cur))

    y_cur = list(y0)
    for t_s, t_e, nfa in segments:
        if abs(t_s - t_e) < 1e-10:
            continue
        sol = run_segment(y_cur, t_s, t_e, beta_fn, n_f=nfa, max_step=max_step)
        y_cur = list(sol.y[:, -1])
    return np.array(y_cur)


def compute_mH(yt_v, g1_v, g2_v, g3_v, v_ew, beta_fn, label):
    t_v = np.log(v_ew)
    t_pl = np.log(M_PL)

    y0_up = [g1_v, g2_v, g3_v, yt_v, 0.1]
    y_pl = run_with_thresholds(y0_up, t_v, t_pl, beta_fn, max_step=1.0)

    y0_down = [y_pl[0], y_pl[1], y_pl[2], y_pl[3], 0.0]
    y_v = run_with_thresholds(y0_down, t_pl, t_v, beta_fn, max_step=0.5)

    lam_v = y_v[4]
    m_H = np.sqrt(max(2.0 * lam_v, 0)) * v_ew
    return {"label": label, "lam_v": lam_v, "m_H": m_H,
            "yt_pl": y_pl[3], "yt_v_out": y_v[3]}


# =====================================================================
#  BACKWARD WARD SCAN
# =====================================================================

def backward_ward_scan(g1_v, g2_v, g3_v):
    def residual(yt_v_trial):
        y0 = [g1_v, g2_v, g3_v, yt_v_trial, 0.129]
        y_final = run_with_thresholds(y0, T_V, T_PL, beta_2loop, max_step=1.0)
        return y_final[3] - YT_PL

    yt_trials = np.linspace(0.5, 1.3, 30)
    residuals = []
    for yt in yt_trials:
        try:
            residuals.append(residual(yt))
        except RuntimeError:
            residuals.append(np.nan)
    residuals = np.array(residuals)

    for i in range(len(residuals) - 1):
        if (not np.isnan(residuals[i]) and not np.isnan(residuals[i+1])
                and residuals[i] * residuals[i+1] < 0):
            return brentq(residual, yt_trials[i], yt_trials[i+1], xtol=1e-10)
    raise RuntimeError("Backward Ward scan: no root found")


# =====================================================================
#  NNLO THRESHOLD
# =====================================================================

def nnlo_threshold_lambda(yt, g3, g2, g1):
    as_pi = g3**2 / (4.0*PI*PI)
    x_t = yt**2 / (16.0*PI**2)
    delta = -x_t*yt**2*as_pi*C_F*3.0
    delta += -x_t*yt**2*as_pi**2*(16.0*C_F**2 + 12.0*C_F*C_A - 8.0/3.0*C_F*6*T_F)/3.0
    delta += -x_t**2*yt**2*as_pi*24.0*C_F
    delta += -x_t**2*(3.0/4.0*g2**2 + 1.0/12.0*g1**2)
    return delta


# =====================================================================
#  MAIN
# =====================================================================

print("=" * 78)
print("HIGGS MASS CONVERGENCE: CORRECTED y_t (sqrt(8/9) color projection)")
print("lambda(M_Pl) = 0 -> m_H at 1-loop, 2-loop, 2+3-loop, 3-loop+NNLO")
print("=" * 78)
print()
t0 = time.time()

# Backward Ward scan
print("BACKWARD WARD SCAN")
print(f"  g_1(v) = {G1_V:.6f}  (taste staircase + sqrt(9/8))")
print(f"  g_2(v) = {G2_V:.6f}  (taste staircase + sqrt(9/8))")
print(f"  g_3(v) = {G3_V:.6f}  (alpha_s = {ALPHA_S_V:.6f})")
print(f"  v      = {V_DERIVED:.2f} GeV")
print()

yt_ward = backward_ward_scan(G1_V, G2_V, G3_V)
yt_corrected = yt_ward * SQRT_R_CONN

print(f"  y_t(Ward, uncorrected)   = {yt_ward:.6f}")
print(f"  y_t(physical) = Ward * sqrt(8/9) = {yt_corrected:.6f}")
print(f"  SM y_t(v)                = {YT_SM:.6f}")
print(f"  |framework - SM|         = {abs(yt_corrected - YT_SM):.4f}")
print()

# Framework at each loop order
print("=" * 78)
print(f"FRAMEWORK: y_t = {yt_corrected:.6f}")
print("=" * 78)
print()

fw_1l = compute_mH(yt_corrected, G1_V, G2_V, G3_V, V_DERIVED, beta_1loop, "FW 1L")
fw_2l = compute_mH(yt_corrected, G1_V, G2_V, G3_V, V_DERIVED, beta_2loop, "FW 2L")
fw_3l = compute_mH(yt_corrected, G1_V, G2_V, G3_V, V_DERIVED, beta_3loop, "FW 3L")

d_nnlo_fw = nnlo_threshold_lambda(fw_3l['yt_v_out'], G3_V, G2_V, G1_V)
lam_fw_nnlo = fw_3l['lam_v'] + d_nnlo_fw
mH_fw_nnlo = np.sqrt(max(2.0*lam_fw_nnlo, 0)) * V_DERIVED

# SM at each loop order
sm_1l = compute_mH(YT_SM, G1_SM, G2_SM, G3_SM, V_OBS, beta_1loop, "SM 1L")
sm_2l = compute_mH(YT_SM, G1_SM, G2_SM, G3_SM, V_OBS, beta_2loop, "SM 2L")
sm_3l = compute_mH(YT_SM, G1_SM, G2_SM, G3_SM, V_OBS, beta_3loop, "SM 3L")

d_nnlo_sm = nnlo_threshold_lambda(sm_3l['yt_v_out'], G3_SM, G2_SM, G1_SM)
lam_sm_nnlo = sm_3l['lam_v'] + d_nnlo_sm
mH_sm_nnlo = np.sqrt(max(2.0*lam_sm_nnlo, 0)) * V_OBS

# Old uncorrected for comparison
old_1l = compute_mH(0.979, 0.464, 0.648, G3_V, V_DERIVED, beta_1loop, "Old 1L")
old_2l = compute_mH(0.979, 0.464, 0.648, G3_V, V_DERIVED, beta_2loop, "Old 2L")
old_3l = compute_mH(0.979, 0.464, 0.648, G3_V, V_DERIVED, beta_3loop, "Old 3L")

# =====================================================================
#  CONVERGENCE TABLE
# =====================================================================

print("=" * 78)
print("CONVERGENCE TABLE: lambda(M_Pl) = 0 -> m_H  [GeV]")
print("=" * 78)
print()
print(f"  {'Order':<16s} | {'FW(new)':>9s} | {'SM':>9s} | {'Gap':>9s} | {'Old FW':>9s} | {'Old gap':>9s}")
print(f"  {'-'*16}-+-{'-'*9}-+-{'-'*9}-+-{'-'*9}-+-{'-'*9}-+-{'-'*9}")

rows = [
    ("1-loop",       fw_1l['m_H'],  sm_1l['m_H'],  old_1l['m_H']),
    ("2-loop",       fw_2l['m_H'],  sm_2l['m_H'],  old_2l['m_H']),
    ("2+3-loop",     fw_3l['m_H'],  sm_3l['m_H'],  old_3l['m_H']),
    ("3-loop+NNLO",  mH_fw_nnlo,    mH_sm_nnlo,    old_3l['m_H']),
]

for label, fw, sm, old in rows:
    gap_new = fw - sm
    gap_old = old - sm
    print(f"  {label:<16s} | {fw:9.2f} | {sm:9.2f} | {gap_new:+9.2f} | {old:9.2f} | {gap_old:+9.2f}")

print()

# =====================================================================
#  SUMMARY
# =====================================================================

print("=" * 78)
print("SUMMARY")
print("=" * 78)
print()
print(f"  y_t(framework, corrected)  = {yt_corrected:.6f}")
print(f"  y_t(SM, Buttazzo et al.)   = {YT_SM:.6f}")
print(f"  Delta y_t                  = {yt_corrected - YT_SM:+.4f}")
print()
print(f"  Framework m_H (3L+NNLO)   = {mH_fw_nnlo:.2f} GeV")
print(f"  SM m_H (3L+NNLO)          = {mH_sm_nnlo:.2f} GeV")
print(f"  Gap (new)                  = {mH_fw_nnlo - mH_sm_nnlo:+.2f} GeV")
print(f"  Gap (old, y_t=0.979)       ~ 24.7 GeV (order-independent)")
print()
print(f"  Observed m_H               = {M_H_OBS:.2f} GeV")
print(f"  Framework deviation        = {(mH_fw_nnlo - M_H_OBS)/M_H_OBS*100:+.1f}%")
print()

# Check: is the series converging toward 125?
print("  CONVERGENCE CHECK:")
print(f"    1L -> 2L shift (FW):  {fw_2l['m_H'] - fw_1l['m_H']:+.2f} GeV")
print(f"    2L -> 3L shift (FW):  {fw_3l['m_H'] - fw_2l['m_H']:+.2f} GeV")
print(f"    3L -> NNLO shift:     {mH_fw_nnlo - fw_3l['m_H']:+.2f} GeV")
print()

elapsed = time.time() - t0
print(f"Completed in {elapsed:.1f} seconds.")
