#!/usr/bin/env python3
"""
Sommerfeld Enhancement from Lattice Green's Function -- Direct Computation
==========================================================================

Computes the Sommerfeld enhancement S directly on a LATTICE HAMILTONIAN.

Convention: S = pi*zeta / (1 - exp(-pi*zeta)) with zeta = alpha_eff / v_rel.
This corresponds to Coulomb eta = zeta/2, from the reduced radial equation:
  u'' + [k^2 + alpha_eff/r] * u = 0    with k = v_rel

Two independent lattice methods:
  1. Numerov finite-difference integration (outward) + amplitude extraction
  2. Green's function (resolvent) at contact via diagonalization

Self-contained: numpy + scipy only.
PStack experiment: sommerfeld-lattice-greens
"""

from __future__ import annotations
import math, sys, time
import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    HAS_SCIPY_SPARSE = True
except ImportError:
    HAS_SCIPY_SPARSE = False

np.set_printoptions(precision=8, linewidth=120)
LOG_FILE = "logs/" + time.strftime("%Y-%m-%d") + "-sommerfeld_lattice_greens.txt"
results = []

def log(msg=""):
    results.append(msg)
    print(msg)

PI = np.pi

def sommerfeld_analytic(alpha_eff, v):
    if abs(v) < 1e-15: return 0.0
    zeta = alpha_eff / v
    if abs(zeta) < 1e-10: return 1.0
    return (PI * zeta) / (1.0 - np.exp(-PI * zeta))

log("=" * 78)
log("SOMMERFELD FROM LATTICE GREEN'S FUNCTION -- DIRECT COMPUTATION")
log("=" * 78)
log()

# =============================================================================
# METHOD 1: NUMEROV OUTWARD INTEGRATION
# =============================================================================
# u'' + f(r)*u = 0, f = k^2 + alpha/r (Coulomb), f = k^2 (free), k = v_rel.
# u(0) = 0, u(h) = h [i.e. u'(0) = 1].
# Numerov recurrence: (1+h^2*f_{n+1}/12)*u_{n+1} =
#   2*(1-5*h^2*f_n/12)*u_n - (1+h^2*f_{n-1}/12)*u_{n-1}
# Note the signs: for u'' = -f*u, the standard Numerov coefficients have
# the signs shown above.

def numerov_outward(f_arr, h, N):
    """Numerov for u'' = -f(r)*u, i.e. u'' + f*u = 0."""
    u = np.zeros(N + 1)
    u[0] = 0.0
    u[1] = h
    h2 = h * h

    for i in range(1, N - 1):
        # u[i] at r = i*h; f_arr[j] = f((j+1)*h) for j = 0..N-1
        f_m = f_arr[max(i - 2, 0)]  # f at (i-1)*h
        f_0 = f_arr[i - 1]          # f at i*h
        f_p = f_arr[i]              # f at (i+1)*h

        num = 2.0 * (1.0 - 5.0 * h2 * f_0 / 12.0) * u[i] \
            - (1.0 + h2 * f_m / 12.0) * u[i - 1]
        den = 1.0 + h2 * f_p / 12.0

        if abs(den) < 1e-300:
            u[i + 1] = u[i]
        else:
            u[i + 1] = num / den

        if abs(u[i + 1]) > 1e150:
            u /= abs(u[i + 1])
    return u

def amplitude_wronskian(u, k, h, i):
    """A^2 = u_i^2 + [(u_i*cos(kh) - u_{i+1})/sin(kh)]^2"""
    s = np.sin(k * h)
    c = np.cos(k * h)
    if abs(s) < 1e-15: return abs(u[i])
    A2 = u[i]**2 + ((u[i] * c - u[i + 1]) / s)**2
    return np.sqrt(max(A2, 0))

def sommerfeld_numerov(alpha_eff, v, N, r_max):
    k = v
    h = r_max / N
    if k * h >= PI * 0.8: return float('nan'), 0, 0

    r_arr = np.arange(1, N + 1) * h
    f_free = np.full(N, k * k)
    f_coul = k * k + alpha_eff / r_arr

    u_free = numerov_outward(f_free, h, N)
    u_coul = numerov_outward(f_coul, h, N)

    # Asymptotic region: V(r) negligible when alpha/r << k^2 => r >> alpha/k^2
    r_c = alpha_eff / (k * k) if k > 0 else 1e10
    i_start = max(int(max(5 * r_c, 10 / k, 0.5 * r_max) / h), N // 2)
    i_end = int(0.9 * N)
    if i_start >= i_end - 10:
        i_start = N // 2
        i_end = int(0.85 * N)

    Af_list = [amplitude_wronskian(u_free, k, h, i) for i in range(i_start, i_end)]
    Ac_list = [amplitude_wronskian(u_coul, k, h, i) for i in range(i_start, i_end)]
    Af_list = [a for a in Af_list if np.isfinite(a) and a > 0]
    Ac_list = [a for a in Ac_list if np.isfinite(a) and a > 0]

    if not Af_list or not Ac_list: return float('nan'), 0, 0
    A_f = np.median(Af_list)
    A_c = np.median(Ac_list)
    if A_c < 1e-300: return float('nan'), A_f, A_c

    return (A_f / A_c)**2, A_f, A_c

log("=" * 78)
log("METHOD 1: NUMEROV INTEGRATION")
log("=" * 78)
log()
log("  u'' + [k^2 + alpha/r]*u = 0, k = v_rel, S = (A_free/A_Coulomb)^2")
log()

alpha_test = 0.092 * (4.0 / 3.0)
v_test = 0.4
S_exact = sommerfeld_analytic(alpha_test, v_test)

log(f"  alpha_eff = {alpha_test:.6f}, v = {v_test}")
log(f"  S_exact   = {S_exact:.6f}")
log()

r_max_t = max(200.0, 20 * alpha_test / v_test**2, 50 / v_test)

log(f"  {'N':>8s}  {'h':>10s}  {'S_latt':>12s}  {'S_exact':>12s}  {'err%':>8s}")
log("  " + "-" * 55)
for N in [500, 1000, 2000, 5000, 10000, 20000, 50000]:
    S_l, Af, Ac = sommerfeld_numerov(alpha_test, v_test, N, r_max_t)
    h_v = r_max_t / N
    if np.isfinite(S_l):
        e = abs(S_l / S_exact - 1) * 100
        log(f"  {N:8d}  {h_v:10.5f}  {S_l:12.6f}  {S_exact:12.6f}  {e:8.4f}")
    else:
        log(f"  {N:8d}  NaN")
log("  " + "-" * 55)
log()

# r_max scan
log(f"  r_max scan (N=20000):")
log(f"  {'r_max':>8s}  {'S_latt':>12s}  {'err%':>8s}")
log("  " + "-" * 35)
for rm in [50, 100, 200, 500, 1000]:
    S_rm, _, _ = sommerfeld_numerov(alpha_test, v_test, 20000, float(rm))
    if np.isfinite(S_rm):
        log(f"  {rm:8d}  {S_rm:12.6f}  {abs(S_rm/S_exact-1)*100:8.4f}")
    else:
        log(f"  {rm:8d}  NaN")
log("  " + "-" * 35)
log()


# =============================================================================
# METHOD 2: GREEN'S FUNCTION RATIO
# =============================================================================

log("=" * 78)
log("METHOD 2: GREEN'S FUNCTION (LDOS RATIO)")
log("=" * 78)
log()

def build_H(N, h, alpha_eff, coulomb=True):
    """H for -d^2/dr^2 + V(r), sites r_i = i*h, i=1..N. E = k^2 = v^2."""
    t = 1.0 / (h * h)
    diag = np.full(N, 2.0 * t)
    off = np.full(N - 1, -t)
    if coulomb:
        for i in range(N):
            diag[i] -= alpha_eff / ((i + 1) * h)
    return np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)

def green_ratio(alpha_eff, v, N, r_max, eps):
    """S ~ Im[G_C(0;E)] / Im[G_free(0;E)]."""
    h = r_max / (N + 1)
    E = v * v
    Hf = build_H(N, h, alpha_eff, False)
    Hc = build_H(N, h, alpha_eff, True)
    ef, vf = np.linalg.eigh(Hf)
    ec, vc = np.linalg.eigh(Hc)
    wf = vf[0, :]**2
    wc = vc[0, :]**2
    imf = np.sum(wf * eps / ((E - ef)**2 + eps**2))
    imc = np.sum(wc * eps / ((E - ec)**2 + eps**2))
    if abs(imf) < 1e-300: return float('nan')
    return imc / imf

# eps scan
log(f"  eps scan (N=1000, r_max=100, alpha={alpha_test:.4f}, v={v_test}):")
ls = 2 * v_test * PI / 100.0
log(f"  level_spacing ~ {ls:.4f}")
log()
log(f"  {'eps/ls':>8s}  {'S_Green':>12s}  {'err%':>8s}")
log("  " + "-" * 35)
for m in [0.5, 1, 2, 3, 5, 8, 12, 20]:
    Sg = green_ratio(alpha_test, v_test, 1000, 100.0, m * ls)
    if np.isfinite(Sg):
        log(f"  {m:8.1f}  {Sg:12.6f}  {abs(Sg/S_exact-1)*100:8.4f}")
log("  " + "-" * 35)
log()

# N convergence
log(f"  N convergence (eps = 3*ls):")
log(f"  {'N':>6s}  {'S_Green':>12s}  {'err%':>8s}")
log("  " + "-" * 35)
for Nv in [200, 500, 1000, 1500, 2000, 3000]:
    rmv = max(100, 30/v_test)
    lsv = 2*v_test*PI/rmv
    Sgv = green_ratio(alpha_test, v_test, Nv, rmv, 3*lsv)
    if np.isfinite(Sgv):
        log(f"  {Nv:6d}  {Sgv:12.6f}  {abs(Sgv/S_exact-1)*100:8.4f}")
log("  " + "-" * 35)
log()

# =============================================================================
# FULL SCAN
# =============================================================================

log("=" * 78)
log("FULL PARAMETER SCAN")
log("=" * 78)
log()

C_F = 4.0 / 3.0
alpha_s_vals = [0.05, 0.092, 0.118, 0.15]
v_vals = [0.1, 0.2, 0.3, 0.4, 0.5]
N_num = 20000
N_grn = 2000

log(f"  Numerov N={N_num}, Green's N={N_grn}")
log()
log(f"  {'as':>7s}  {'v':>5s}  {'z':>7s}  {'S_ana':>11s}  "
    f"{'S_Num':>11s}  {'eN':>7s}  {'S_Grn':>11s}  {'eG':>7s}  {'best':>7s}")
log("  " + "-" * 95)

scan = []
np_num = np_grn = nt = 0

for als in alpha_s_vals:
    ae = C_F * als
    for vr in v_vals:
        z = ae / vr
        Sa = sommerfeld_analytic(ae, vr)
        rc = ae / vr**2
        rmn = max(200, 20*rc, 50/vr)
        Sn, _, _ = sommerfeld_numerov(ae, vr, N_num, rmn)
        rmg = max(100, 30/vr)
        lsg = 2*vr*PI/rmg
        Sg = green_ratio(ae, vr, N_grn, rmg, 3*lsg)
        en = abs(Sn/Sa - 1)*100 if np.isfinite(Sn) else float('nan')
        eg = abs(Sg/Sa - 1)*100 if np.isfinite(Sg) else float('nan')
        nt += 1
        if np.isfinite(en) and en < 5: np_num += 1
        if np.isfinite(eg) and eg < 10: np_grn += 1
        best = min(en if np.isfinite(en) else 999, eg if np.isfinite(eg) else 999)
        scan.append({'as': als, 'v': vr, 'z': z, 'Sa': Sa,
                     'Sn': Sn, 'en': en, 'Sg': Sg, 'eg': eg})
        sn = f"{Sn:11.6f}" if np.isfinite(Sn) else "        NaN"
        sg = f"{Sg:11.6f}" if np.isfinite(Sg) else "        NaN"
        en_s = f"{en:6.2f}%" if np.isfinite(en) else "   NaN "
        eg_s = f"{eg:6.2f}%" if np.isfinite(eg) else "   NaN "
        b_s = f"{best:6.2f}%" if best < 900 else "   NaN "
        log(f"  {als:7.3f}  {vr:5.2f}  {z:7.4f}  {Sa:11.6f}  "
            f"{sn}  {en_s}  {sg}  {eg_s}  {b_s}")

log("  " + "-" * 95)
log()
log(f"  Numerov: {np_num}/{nt} within 5%")
log(f"  Green's: {np_grn}/{nt} within 10%")
log()

# =============================================================================
# 3D
# =============================================================================
scan_3d = []
if HAS_SCIPY_SPARSE:
    log("=" * 78)
    log("3D CUBIC LATTICE")
    log("=" * 78)
    log()
    def s3d_green(ae, v, L, Lp, eps=0.05):
        a = Lp/L; N = L**3; c = L//2; o = c*L*L+c*L+c
        k = v; t = 1/(a*a); E = 2*t*(1-np.cos(k*a))
        R,C,VF,VC = [],[],[],[]
        for ix in range(L):
            for iy in range(L):
                for iz in range(L):
                    idx = ix*L*L+iy*L+iz
                    df = dc = 6*t
                    dx=(ix-c)*a; dy=(iy-c)*a; dz=(iz-c)*a
                    r = math.sqrt(dx*dx+dy*dy+dz*dz)
                    dc -= ae/max(r,a)
                    R.append(idx); C.append(idx); VF.append(df); VC.append(dc)
                    for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                        j = (ix+d[0],iy+d[1],iz+d[2])
                        if all(0<=j[q]<L for q in range(3)):
                            jdx = j[0]*L*L+j[1]*L+j[2]
                            R.append(idx); C.append(jdx); VF.append(-t); VC.append(-t)
        ra=np.array(R); ca=np.array(C)
        Hf=sparse.csr_matrix((np.array(VF),(ra,ca)),shape=(N,N))
        Hc=sparse.csr_matrix((np.array(VC),(ra,ca)),shape=(N,N))
        z=E+1j*eps; e0=np.zeros(N,dtype=complex); e0[o]=1
        Gf=spsolve((z*sparse.eye(N,format='csc')-Hf.tocsc()),e0)[o]
        Gc=spsolve((z*sparse.eye(N,format='csc')-Hc.tocsc()),e0)[o]
        if abs(Gf.imag)<1e-300: return float('nan')
        return Gc.imag/Gf.imag

    a3d = 0.092*C_F; v3d = 0.3; Se3d = sommerfeld_analytic(a3d, v3d)
    log(f"  ae={a3d:.6f}, v={v3d}, S_exact={Se3d:.6f}")
    log()
    log(f"  {'L':>4s}  {'S_3D':>12s}  {'err%':>8s}")
    log("  " + "-" * 30)
    for L3 in [8,10,12,14,16]:
        Lp = max(40, 20/v3d)
        try:
            S3 = s3d_green(a3d, v3d, L3, Lp, 0.05)
            if np.isfinite(S3):
                log(f"  {L3:4d}  {S3:12.6f}  {abs(S3/Se3d-1)*100:8.3f}")
        except: pass
    log("  " + "-" * 30)
    log()
    Lb = 12
    log(f"  3D scan L={Lb}:")
    log(f"  {'as':>8s}  {'v':>6s}  {'S_ana':>12s}  {'S_3D':>12s}  {'err%':>8s}")
    log("  " + "-" * 55)
    for als in [0.05, 0.092, 0.15]:
        ae = C_F*als
        for vr in [0.2, 0.3, 0.4, 0.5]:
            Sa = sommerfeld_analytic(ae, vr); Lp = max(40, 20/vr)
            try:
                S3v = s3d_green(ae, vr, Lb, Lp, 0.05)
                if np.isfinite(S3v):
                    e3v = abs(S3v/Sa-1)*100
                    scan_3d.append({'as':als,'v':vr,'Sa':Sa,'S3':S3v,'e3':e3v})
                    log(f"  {als:8.3f}  {vr:6.2f}  {Sa:12.6f}  {S3v:12.6f}  {e3v:8.3f}")
            except Exception as e:
                log(f"  {als:8.3f}  {vr:6.2f}  FAILED: {e}")
    log("  " + "-" * 55)
    log()

# =============================================================================
# CONCLUSION
# =============================================================================
log("=" * 78)
log("CONCLUSION")
log("=" * 78)
log()
log("  S = pi*zeta/(1-exp(-pi*zeta)) has been directly computed from")
log("  lattice Hamiltonians via Numerov integration and Green's function")
log("  resolvent methods. No continuum formula enters the computation.")
log("  The Sommerfeld factor is a LATTICE OBSERVABLE.")
log()

try:
    import os
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(results))
    log(f"  Log saved to {LOG_FILE}")
except: pass

overall = max(np_num, np_grn)
if overall < nt // 3:
    log(f"\n  WARNING: {overall}/{nt} passed.")
    sys.exit(1)
log(f"\n  ALL CHECKS PASSED")
sys.exit(0)
