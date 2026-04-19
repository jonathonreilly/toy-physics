#!/usr/bin/env python3
"""
Part C fix: running mass scan with correct threshold treatment.

Bug in frontier_koide_gap_0p0066_attack.py Part C:
  - run_mass() integrates ALL masses from their pole to mu, including m_τ
    below its threshold. This preserves all mass ratios (κ is scale-invariant).
  - Correct treatment: hold m_l at pole for μ < m_l (each lepton only runs
    ABOVE its own mass threshold). This is the MS-bar decoupling scheme.
  - Also: sign was wrong — masses DECREASE at higher μ in QED (d ln m/d ln μ < 0).

Physics: for μ ∈ (m_μ, m_τ):
  - m_e and m_μ both run downward from their poles.
  - m_τ stays at pole mass (not yet active).
  - m_τ/m_μ grows as μ increases → κ(μ) evolves nontrivially.
  - Crossing κ(μ) = κ_prod1 gives μ_K.
"""
import math, numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad

PI    = math.pi
GAMMA = 0.5
E1    = math.sqrt(8/3)
E2    = math.sqrt(8)/3
S     = math.sqrt(6)/3
ALPHA_EM = 7.2973535693e-3
M_e, M_mu, M_tau = 0.51099895, 105.6583755, 1776.86

T_M = np.array([[1,0,0],[0,0,1],[0,1,0]], dtype=complex)
T_D = np.array([[0,-1,1],[-1,1,0],[1,0,-1]], dtype=complex)
T_Q = np.array([[0,1,1],[1,0,1],[1,1,0]], dtype=complex)

def H3(m, d=S, q=S, g=GAMMA):
    H = np.array([[0,E1,-E1-1j*g],[E1,0,-E2],[-E1+1j*g,-E2,0]], dtype=complex)
    return H + m*T_M + d*T_D + q*T_Q

def koide_root_small(v, w):
    return 2*(v+w) - math.sqrt(3*(v*v+4*v*w+w*w))

def slots_uvw(m, d=S, q=S, g=GAMMA):
    eH = expm(H3(m,d,q,g))
    v  = float(np.real(eH[2,2])); w = float(np.real(eH[1,1]))
    u  = koide_root_small(v,w)
    return u, v, w, u*v*w, (v-w)/(v+w)

def kappa_pdg_from_masses(me, mmu, mtau):
    sqm = np.sqrt([me,mmu,mtau]); d = sqm/np.linalg.norm(sqm)
    def koide_amp(k):
        w = (1-k)/(1+k)
        if w<=0: return 1.0
        u = koide_root_small(1.0,w)
        if u<=0: return 1.0
        a = np.array([u,1.0,w])
        return -float(np.dot(a/np.linalg.norm(a),d))
    r = minimize_scalar(koide_amp, bounds=(-0.9999,-0.0001), method="bounded",
                        options={"xatol":1e-14})
    return float(r.x)

KAPPA_PDG = kappa_pdg_from_masses(M_e, M_mu, M_tau)
m_prod1   = brentq(lambda m: slots_uvw(m)[3]-1.0, -1.3, -1.0, xtol=1e-14)
KAPPA_PROD1 = slots_uvw(m_prod1)[4]

print("="*68)
print("RUNNING MASS SCAN — CORRECTED THRESHOLD TREATMENT")
print(f"  κ_PDG   = {KAPPA_PDG:.12f}")
print(f"  κ_prod1 = {KAPPA_PROD1:.12f}")
print(f"  Δκ      = κ_prod1 - κ_PDG = {KAPPA_PROD1-KAPPA_PDG:.6e}")

# ── Correct running coupling α(μ) with threshold matching ────────────────────
def alpha_qed(mu):
    """1-loop QED running coupling, threshold matching at m_e, m_μ, m_τ."""
    a = ALPHA_EM
    if mu > M_e:
        a = 1/(1/ALPHA_EM - math.log(mu**2/M_e**2)/(3*PI))
    if mu > M_mu:
        a = 1/(1/a - math.log(mu**2/M_mu**2)/(3*PI))
    if mu > M_tau:
        a = 1/(1/a - math.log(mu**2/M_tau**2)/(3*PI))
    return a

# ── Correct mass running: hold m_l at pole for μ < m_l ──────────────────────
def run_mass_threshold(m_pole, mu_mev):
    """Run m_pole DOWN to mu_mev.
    Only runs if mu_mev > m_pole (mass active at this scale).
    Uses correct sign: d(ln m)/d(ln μ) = -3α(μ)/(2π) < 0.
    """
    if mu_mev <= m_pole:
        return m_pole  # not yet active — hold at pole
    def integrand(lnmu):
        return -3*alpha_qed(math.exp(lnmu))/(2*PI)  # NEGATIVE → mass decreases
    integral, _ = quad(integrand, math.log(m_pole), math.log(mu_mev))
    return m_pole * math.exp(integral)

def running_masses(mu_mev):
    """Lepton masses at scale μ with correct threshold decoupling."""
    me   = run_mass_threshold(M_e,   mu_mev)
    mmu  = run_mass_threshold(M_mu,  mu_mev)
    mtau = run_mass_threshold(M_tau, mu_mev)
    return me, mmu, mtau

# ── Scan κ(μ) over a range spanning all thresholds ────────────────────────────
print("\nScan κ(μ) vs μ:")
print(f"  {'μ (MeV)':>12}  {'κ(μ)':>18}  {'κ-κ_prod1':>14}  {'me,mμ,mτ MeV':}")
scan_points = [0.5, 1, 5, 50, 105.658, 110, 130, 150, 164, 170,
               200, 300, 500, 800, 1000, 1500, 1776.86, 3000]
kappa_scan = []
for mu in scan_points:
    me_, mmu_, mtau_ = running_masses(mu)
    k = kappa_pdg_from_masses(me_, mmu_, mtau_)
    kappa_scan.append((mu, k, me_, mmu_, mtau_))
    dk = k - KAPPA_PROD1
    print(f"  {mu:>12.3f}  {k:>18.12f}  {dk:>+14.6e}  "
          f"({me_:.6f}, {mmu_:.4f}, {mtau_:.4f})")

# ── Find crossing κ(μ) = κ_prod1 ─────────────────────────────────────────────
print(f"\nSearching for crossing κ(μ) = κ_prod1 = {KAPPA_PROD1:.12f} ...")

def kappa_minus_kprod1(log_mu):
    mu = math.exp(log_mu)
    me_, mmu_, mtau_ = running_masses(mu)
    return kappa_pdg_from_masses(me_, mmu_, mtau_) - KAPPA_PROD1

# Fine grid over (m_e, 10*m_τ)
log_mus = np.linspace(math.log(0.5), math.log(2e4), 2000)
kvals   = []
for lm in log_mus:
    try:
        kvals.append(kappa_minus_kprod1(lm))
    except:
        kvals.append(float('nan'))

crossings = []
for i in range(len(log_mus)-1):
    k1, k2 = kvals[i], kvals[i+1]
    if math.isnan(k1) or math.isnan(k2): continue
    if k1*k2 < 0:
        try:
            lm_c = brentq(kappa_minus_kprod1, log_mus[i], log_mus[i+1], xtol=1e-12)
            crossings.append(math.exp(lm_c))
        except: pass

print(f"  Found {len(crossings)} crossing(s):")
for mu_K in crossings:
    me_K, mmu_K, mtau_K = running_masses(mu_K)
    k_K = kappa_pdg_from_masses(me_K, mmu_K, mtau_K)
    Q_K = (math.sqrt(me_K)+math.sqrt(mmu_K)+math.sqrt(mtau_K))**2 / \
          (me_K+mmu_K+mtau_K)   # standard Koide Q = sum_sqrts² / sum_masses ≈ 3/2
    aK  = alpha_qed(mu_K)

    print(f"\n  μ_K = {mu_K:.6f} MeV  =  {mu_K/M_mu:.6f} × m_μ")
    print(f"  κ(μ_K)   = {k_K:.12f}  (target κ_prod1 = {KAPPA_PROD1:.12f})")
    print(f"  Δκ       = {k_K-KAPPA_PROD1:.4e}")
    print(f"  Koide Q(μ_K) = {Q_K:.10f}  (Q at pole = {(math.sqrt(M_e)+math.sqrt(M_mu)+math.sqrt(M_tau))**2/(M_e+M_mu+M_tau):.10f})")
    print(f"  α(μ_K)   = {aK:.10f}")
    print(f"  Running masses at μ_K:")
    print(f"    m_e(μ_K)  = {me_K:.8f} MeV  Δ = {(me_K-M_e)/M_e*100:+.4f}%")
    print(f"    m_μ(μ_K)  = {mmu_K:.6f} MeV  Δ = {(mmu_K-M_mu)/M_mu*100:+.4f}%")
    print(f"    m_τ(μ_K)  = {mtau_K:.4f} MeV  (pole mass, not yet active)")

    # Does the gap close at μ_K? Use uvw loop formula with α(μ_K)
    C2 = S*E1  # = 4/3
    uvw_at_muK = 1 - (aK/(2*PI))*(1 + 2*C2*aK)
    m_loop_muK = brentq(lambda m: slots_uvw(m)[3]-uvw_at_muK, -1.3, -1.0, xtol=1e-14)
    kappa_at_mloop_muK = slots_uvw(m_loop_muK)[4]

    print(f"\n  Gap closure test at μ_K:")
    print(f"    uvw formula at α(μ_K) gives m_loop(μ_K) = {m_loop_muK:.12f}")
    print(f"    κ at m_loop(μ_K) = {kappa_at_mloop_muK:.12f}")
    print(f"    κ_prod1          = {KAPPA_PROD1:.12f}")
    print(f"    κ_PDG (pole)     = {KAPPA_PDG:.12f}")
    print(f"    Gap κ_prod1 - κ_PDG = {KAPPA_PROD1-KAPPA_PDG:.6e}")
    print(f"    Residual at μ_K  = {kappa_at_mloop_muK-KAPPA_PDG:.6e}")
    print(f"    Fraction closed  = {(kappa_at_mloop_muK-KAPPA_PDG)/(KAPPA_PROD1-KAPPA_PDG)*100:.2f}%")

    # Natural scale identification
    print(f"\n  Natural scale test:")
    naturals = [
        ("m_μ",           M_mu),
        ("m_μ × S",       M_mu*S),
        ("m_μ × E1",      M_mu*E1),
        ("m_μ × (4/3)",   M_mu*(4/3)),
        ("m_μ × E1²",     M_mu*(8/3)),
        ("m_μ × 1/S",     M_mu/S),
        ("√(m_e × m_τ)",  math.sqrt(M_e*M_tau)),
        ("√(m_μ × m_τ)",  math.sqrt(M_mu*M_tau)),
        ("m_μ^(2/3)×m_τ^(1/3)", M_mu**(2/3)*M_tau**(1/3)),
        ("(3/2)×m_μ",     1.5*M_mu),
        ("π/2 × m_μ",     PI/2*M_mu),
        ("e × m_μ",       math.e*M_mu),
        ("m_π = 139.57",  139.57),
        ("Λ_QCD = 217",   217.0),
        ("m_K = 494",     494.0),
        ("m_μ/α_EM",      M_mu/ALPHA_EM),
    ]
    for label, scale in naturals:
        frac = mu_K/scale
        err  = abs(frac-1)*100
        if err < 5:
            print(f"    μ_K ≈ {label} = {scale:.4f} MeV  (err={err:.3f}%)"
                  + ("  ***" if err<0.5 else ""))

if not crossings:
    print("  No crossing found — κ(μ) does not cross κ_prod1 in scan range.")
    # Print range of κ to diagnose
    kval_arr = [k for k in kvals if not math.isnan(k)]
    print(f"  κ(μ) range over scan: [{min(kval_arr)+KAPPA_PROD1:.10f}, {max(kval_arr)+KAPPA_PROD1:.10f}]")
    print(f"  κ_prod1 = {KAPPA_PROD1:.10f}")

# ── Scale invariance proof: mass ratios constant in each interval ─────────────
print("\n" + "="*68)
print("DIAGNOSIS: Scale invariance in each threshold interval")
print()
for mu_A, mu_B in [(110, 200), (200, 500), (500, 1700)]:
    meA, mmuA, mtauA = running_masses(mu_A)
    meB, mmuB, mtauB = running_masses(mu_B)
    r_e_mu_A  = meA/mmuA;   r_e_mu_B  = meB/mmuB
    r_tau_mu_A= mtauA/mmuA; r_tau_mu_B= mtauB/mmuB
    print(f"  μ = [{mu_A}, {mu_B}] MeV:")
    print(f"    m_e/m_μ:  {r_e_mu_A:.10f} → {r_e_mu_B:.10f}  "
          f"Δ = {abs(r_e_mu_B-r_e_mu_A)/r_e_mu_A*100:.6f}%")
    print(f"    m_τ/m_μ:  {r_tau_mu_A:.6f} → {r_tau_mu_B:.6f}  "
          f"Δ = {abs(r_tau_mu_B-r_tau_mu_A)/r_tau_mu_A*100:.6f}%")
    # κ change
    kA = kappa_pdg_from_masses(meA, mmuA, mtauA)
    kB = kappa_pdg_from_masses(meB, mmuB, mtauB)
    print(f"    κ: {kA:.10f} → {kB:.10f}  Δκ = {kB-kA:.4e}")
    print()
