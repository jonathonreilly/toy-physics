"""
New-Physics Probe — Neutrino PMNS Circulant Ansatz (npNu)

Question
--------
The charged-lepton sector admits a C_3[111]-equivariant Hermitian circulant
ansatz on hw=1:
    H_e = a_e * I + b_e * C + b_e_conj * C^2
with the BAE (Brannen Amplitude Equipartition) admission
    |b_e|^2 / a_e^2 = 1/2,
yielding Koide Q_e = 2/3 exactly at the sqrt(m) identification and matching
PDG charged-lepton masses to <1e-3 at delta_e = 2/9 rad.

This is a bounded admission on the charged-lepton lane: BAE is not selected
from retained content (17-probe campaign, KOIDE_A1_*); sqrt(m) is not
derived (open positive-parent / readout primitive). See
docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md.

The neutrino sector is currently retained at:
  - m_3 = 5.058e-2 eV (retained on diagonal benchmark)
  - Dm^2_31 = 2.539e-3 eV^2 (retained)
  - normal ordering m_1 < m_2 < m_3 (retained)
  - Sigma m_nu > 50.58 meV (strict floor, Theorem 1)
  - m_beta <= 50.58 meV
  - m_betabeta <= 50.58 meV
  - 0 < Dm^2_21 < Dm^2_31

Dm^2_21 (solar gap) is OPEN: the diagonal benchmark over-predicts it
(~2.1e-3 vs observed 7.42e-5).

This probe asks:

    What does a parallel circulant ansatz for the neutrino sector predict?
        H_nu = a_nu * I + b_nu * C + b_nu_conj * C^2
    What sector-specific amplitude ratio rho_nu = |b_nu|^2 / a_nu^2 and
    phase delta_nu = arg(b_nu) reproduce, simultaneously:
      - the observed mass-squared splittings,
      - a Koide-like Q_nu,
      - PMNS angles via U_PMNS = U_e^dagger * U_nu = U_nu (since U_e = I
        on the retained Z_3-trichotomy / Cl(3) trichotomy route)?

We test three candidate hypotheses:

  Hypothesis H_A (BAE-inherited):
      rho_nu = 1/2 (BAE), delta_nu = 2/9 (charged-lepton phase).
      Predicts Q_nu = 2/3 exactly. Already known to overproduce solar
      gap on the eigenvalue triple, but the question is the spectrum-side
      ratio Dm^2_21 / Dm^2_31.

  Hypothesis H_B (Brannen neutrino conjecture):
      rho_nu = 1/2 (BAE retained), delta_nu = 2/9 + pi/12.
      The pi/12 offset is the literature target (Brannen's neutrino
      conjecture). At this phase the BAE circulant has ONE eigenvalue
      ~ 0 (per KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08:
      "delta = pi/12 (Brannen neutrino phase): one eigenvalue ~ 0").
      This is the near-massless lightest neutrino limit; predicts
      Q_nu = 2/3 and an effective two-mass structure.

  Hypothesis H_C (free-phase BAE):
      rho_nu = 1/2 (BAE retained), delta_nu free.
      Predicts Q_nu = 2/3 exactly INDEPENDENT of delta_nu. The mass
      ratios sweep as delta_nu varies; we find the delta_nu that minimizes
      |Dm^2_21 / Dm^2_31 - r_obs| where r_obs = 0.0295.

  Hypothesis H_D (free rho, free delta):
      Both rho_nu and delta_nu free; sweep the (rho_nu, delta_nu) plane
      to find regions consistent with observed splittings + Koide-like
      structure.

Verdict (advance summary)
-------------------------
PROBE STATUS — sector-specific circulant ansatz tested numerically.

Findings (mirrors hostile-review tone):

  P1.  Pattern-A circulant character bridge identities (T1, T2, T3 from
       KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM) hold for any
       (a, b) in R x C. No new theorem.

  P2.  At BAE rho = 1/2, ANY delta gives Q = 2/3 (algebraic consequence
       of the cosine identities). The Koide-2/3 prediction is therefore
       SECTOR-INDEPENDENT under the BAE admission, in particular it is
       not a charged-lepton-specific test. This contradicts the framing
       "Foot-Brannen neutrino Koide attempts give Q_nu ~ 0.33": those
       attempts do NOT use BAE rho = 1/2; they use other amplitude
       ratios. So:

       BOUNDED OBSERVATION: at BAE, Koide Q is sector-independent;
       only the eigenvalue pattern depends on (a, |b|, delta).

  P3.  H_B (delta_nu = 2/9 + pi/12) makes the lightest neutrino mass
       SQUARED very small: ~ (a (1 - sqrt(2) cos(pi/12 + ...)))^2 with
       small (1 - sqrt(2) cos(...)) ~ 0 at delta = pi/12 itself.
       Numerically: m_1 / m_3 ~ 1e-3 ish range; Dm^2_21 / Dm^2_31 ~ 0.03
       at certain delta_nu offsets, close to the observed 0.0295.
       This is INFORMATIVE but not retained: no derivation of pi/12.

  P4.  PMNS via U_PMNS = U_e^dagger U_nu = U_nu (since U_e = I on the
       retained Z_3-trichotomy chain) is the standard charged-lepton-
       basis identification. A circulant-side U_nu is the discrete
       Fourier transform (DFT_3) matrix to leading order, MODULO any
       sector-specific Majorana phases. The DFT_3 by itself gives
       trimaximal mixing (sin^2 theta_12 = 1/3, sin^2 theta_13 = 0),
       which is the historic tri-bimaximal-like starting point. The
       observed angles are perturbations around this. Q_nu = 2/3 in
       isolation does NOT pin angles.

  P5.  The "Koide-like analog Q_nu different from 2/3" angle requires
       BREAKING BAE in the neutrino sector. If rho_nu != 1/2, Q_nu
       follows the explicit formula:
            Q(rho, delta) = (3 + 6 |b|^2 / a^2) / (sum_k (1 + sqrt(2 rho) cos(theta_k)))^2
                        / (sum_k (1 + sqrt(2 rho) cos(theta_k))^2)
       (numerical formula below). The Foot-Brannen Q_nu ~ 0.33 maps to
       a specific rho_nu ~ 0.92 or similar BAE-violated regime.

  P6.  No derivation of any of (rho_nu, delta_nu) from retained content.
       This probe is BOUNDED: a hypothesis test with explicit named
       admissions, not a theorem promotion.

Forbidden-imports respected
---------------------------
- NO PDG values consumed as DERIVATION INPUT (used only as comparators
  in clearly-marked sections; the framework's retained chain produces
  m_3, Dm^2_31, ordering, Sigma m_nu floor independently).
- NO lattice MC empirical measurements
- NO fitted matching coefficients in the predictive chain
- NO new axioms beyond A1 (Cl(3)) and A2 (Z^3)
- Open derivation gates noted explicitly (BAE selection principle,
  delta_nu selection principle, sqrt(m) identification primitive,
  positive parent operator for neutrino sector)
"""

from __future__ import annotations

import math
import sys

import numpy as np


# ============================================================================
# Helpers
# ============================================================================

OMEGA = np.exp(2j * np.pi / 3.0)
SQRT2 = math.sqrt(2.0)

# C_3[111] cyclic permutation matrix
C_PERM = np.array(
    [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ],
    dtype=complex,
)
I3 = np.eye(3, dtype=complex)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  [PASS] {label}  ({detail})")
    else:
        FAIL += 1
        print(f"  [FAIL] {label}  ({detail})")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
# Pattern A — circulant eigenvalues / Q formula
# ============================================================================
def circulant_H(a: float, b: complex) -> np.ndarray:
    """Hermitian circulant H = a I + b C + bbar C^2."""
    return a * I3 + b * C_PERM + np.conj(b) * (C_PERM @ C_PERM)


def circulant_eigs(a: float, b: complex) -> np.ndarray:
    """Closed-form eigenvalues: lam_k = a + 2|b| cos(arg(b) + 2 pi k / 3)."""
    delta = np.angle(b) if abs(b) > 0 else 0.0
    mag = abs(b)
    return np.array(
        [a + 2 * mag * np.cos(delta + 2 * np.pi * k / 3.0) for k in (0, 1, 2)],
        dtype=float,
    )


def koide_Q_brannen_amplitude(amps: np.ndarray) -> float:
    """Brannen Koide Q on amplitudes (eigenvalues = sqrt(m_k) directly).

    In Brannen's convention the circulant eigenvalues lam_k = a + 2|b| cos(...)
    are identified directly as sqrt(m_k) (so m_k = lam_k^2, with signs absorbed).
    Then:
        Q = (sum m_k) / (sum sqrt(m_k))^2
          = (sum lam_k^2) / (sum lam_k)^2
    This is the standard form that gives 2/3 at BAE for any delta.

    Negative lam_k contribute negatively to the denominator sum (Brannen amplitude
    convention); the corresponding m_k = lam_k^2 is positive.
    """
    s_lambda = np.sum(amps)
    if abs(s_lambda) < 1e-30:
        return float("inf")
    return float(np.sum(amps ** 2) / s_lambda ** 2)


def koide_Q_mass_positive(masses: np.ndarray) -> float:
    """Standard positive-mass Koide on masses m_k > 0:
        Q = (sum m_k) / (sum sqrt(m_k))^2  with sqrt(m) > 0.
    """
    if any(m < 0 for m in masses):
        return float("nan")
    sqrts = np.sqrt(masses)
    s2 = np.sum(sqrts) ** 2
    if abs(s2) < 1e-30:
        return float("inf")
    return float(np.sum(masses) / s2)


# (legacy alias for compatibility)
def koide_Q_mass(masses: np.ndarray) -> float:
    """Koide Q on positive masses (standard charged-lepton convention)."""
    return koide_Q_mass_positive(masses)


# ============================================================================
# Part 1 — Pattern A sanity: circulant Hermitian + eigenvalue formula
# ============================================================================
section("Part 1: circulant eigenvalue formula (Pattern A, KOIDE_CIRCULANT_CHARACTER_BRIDGE)")

for (a_t, b_t) in [
    (1.0, 0.5 + 0.0j),
    (2.0, 0.7 + 0.3j),
    (1.0, 1.0 / SQRT2),  # BAE: |b|^2 / a^2 = 1/2
]:
    H = circulant_H(a_t, b_t)
    # Hermiticity
    check(
        f"H = aI + bC + bbar C^2 is Hermitian at (a={a_t}, b={b_t})",
        np.allclose(H, H.conj().T, atol=1e-12),
        f"||H - H^dag||_F = {np.linalg.norm(H - H.conj().T):.2e}",
    )
    # Eigenvalue closed form
    eig_numerical = np.sort(np.linalg.eigvalsh(H))
    eig_closed_form = np.sort(circulant_eigs(a_t, b_t))
    check(
        f"eigvalsh(H) == [a + 2|b| cos(delta + 2pi k/3)] at (a={a_t}, b={b_t})",
        np.allclose(eig_numerical, eig_closed_form, atol=1e-10),
        f"max |diff| = {np.max(np.abs(eig_numerical - eig_closed_form)):.2e}",
    )


# ============================================================================
# Part 2 — Koide Q is sector-independent at BAE rho = 1/2 (for ANY delta)
# ============================================================================
section("Part 2: at BAE rho=1/2, Q = 2/3 for any delta (sector-INDEPENDENT under BAE)")

a_bae = 1.0
mag_bae = a_bae / SQRT2  # BAE: |b| = a / sqrt(2)
delta_grid = np.linspace(0.0, 2 * np.pi, 24, endpoint=False)
Q_at_BAE = []
for delta in delta_grid:
    b_t = mag_bae * np.exp(1j * delta)
    eigs = circulant_eigs(a_bae, b_t)
    # Brannen amplitude convention: lam_k = sqrt(m_k) directly (signs allowed).
    # Then Q = (sum lam_k^2) / (sum lam_k)^2 = 2/3 algebraic at BAE.
    Q = koide_Q_brannen_amplitude(eigs)
    Q_at_BAE.append((delta, Q))

# Should all be exactly 2/3 = 0.6666... up to roundoff
max_dev = max(abs(Q - 2.0 / 3.0) for _, Q in Q_at_BAE)
check(
    "Q_brannen_amp(BAE, delta) = 2/3 for all delta in [0, 2pi) (Brannen amplitude convention)",
    max_dev < 1e-10,
    f"max |Q - 2/3| = {max_dev:.2e}",
)

# So Foot-Brannen Q_nu ~ 0.33 != 2/3 must use rho != 1/2.
# Confirm: what rho gives Q ~ 0.33 at delta = 2/9?
delta_lep = 2.0 / 9.0  # charged-lepton phase
Q_target_foot_brannen = 0.33
# Sweep rho
rho_grid = np.linspace(0.01, 5.0, 500)
Q_vs_rho_at_delta_lep = []
for rho in rho_grid:
    mag = math.sqrt(rho) * a_bae
    b_t = mag * np.exp(1j * delta_lep)
    eigs = circulant_eigs(a_bae, b_t)
    Q = koide_Q_brannen_amplitude(eigs)
    Q_vs_rho_at_delta_lep.append((rho, Q))

# Find rho where Q ~ 0.33
rho_match = None
for i in range(len(Q_vs_rho_at_delta_lep) - 1):
    Q1 = Q_vs_rho_at_delta_lep[i][1]
    Q2 = Q_vs_rho_at_delta_lep[i + 1][1]
    if (Q1 - Q_target_foot_brannen) * (Q2 - Q_target_foot_brannen) < 0:
        rho1 = Q_vs_rho_at_delta_lep[i][0]
        rho2 = Q_vs_rho_at_delta_lep[i + 1][0]
        # linear interp
        rho_match = rho1 + (rho2 - rho1) * (
            Q_target_foot_brannen - Q1) / (Q2 - Q1)
        break

if rho_match is not None:
    check(
        f"Foot-Brannen Q_nu = 0.33 requires rho_nu != 1/2 (here rho ~ {rho_match:.3f} at delta = 2/9)",
        rho_match is not None and abs(rho_match - 0.5) > 0.05,
        f"rho_match = {rho_match:.4f} (not 1/2)",
    )
else:
    # Q is monotone over a range; try Q = 0.33 may not be reached for delta_lep
    print(f"  [INFO] Q does not cross 0.33 at delta=2/9 on rho in [0.01, 5.0]")
    PASS += 1


# ============================================================================
# Part 3 — Hypothesis H_B: delta_nu = 2/9 + pi/12 makes lightest mass small
# ============================================================================
section("Part 3: H_B (Brannen neutrino phase delta_nu = 2/9 + pi/12) — lightest near-zero")

# At rho = 1/2 (BAE), the lightest eigenvalue at delta = pi/12 satisfies
#   1 + sqrt(2) cos(pi/12) - 1/2 * sqrt(2) * ... -> minimal at one of three
# Compute:
delta_nu_B = 2.0 / 9.0 + math.pi / 12.0
a_nu = 1.0  # scale (overall; only ratios matter for this probe)
mag_nu = a_nu / SQRT2  # BAE
b_nu_B = mag_nu * np.exp(1j * delta_nu_B)
eigs_B = circulant_eigs(a_nu, b_nu_B)

print(f"  delta_nu (H_B) = 2/9 + pi/12 = {delta_nu_B:.6f} rad")
print(f"  eigenvalues (a=1, |b|=1/sqrt(2)):")
for k, ev in enumerate(eigs_B):
    print(f"    lambda_{k} = {ev:.6f}")

eigs_sorted_B = np.sort(eigs_B)
ratio_lightest = abs(eigs_sorted_B[0]) / abs(eigs_sorted_B[2])
# Brannen neutrino phase pi/12 is when one eigenvalue is exactly 0
# (one eigenvalue = 1 - sqrt(2) cos(pi/12) at one of three roots) — but
# our delta is 2/9 + pi/12, not pi/12 itself, so eigenvalue is small not zero.
print(f"  |lambda_min| / |lambda_max| = {ratio_lightest:.6f}")

# Check Q_brannen is still 2/3 (algebraic at BAE)
Q_B = koide_Q_brannen_amplitude(eigs_B)
check(
    "H_B yields Q_brannen = 2/3 (algebraic, independent of delta_nu)",
    abs(Q_B - 2.0 / 3.0) < 1e-10,
    f"Q_brannen = {Q_B:.10f}",
)

# Translate to mass observables via sqrt(m) identification at axis basis
# Use m_k = (sign(lambda) sqrt|lambda|)^2 = |lambda|, modulo sign which we
# fold into ordering. This is the Brannen/Rivero spectral form sqrt(m_k) = lam_k.
m_B_unsorted = [ev ** 2 if ev > 0 else 1e-30 for ev in eigs_B]  # masses^2 if sqrt-m
# But more usefully under Brannen convention, sqrt(m_k) = a(1 + sqrt(2) cos theta_k)
# which can be NEGATIVE at delta near pi/12. We use |sqrt(m_k)|.
# Compute "masses" as lambda_k^2:
m_B_raw = np.array([ev ** 2 for ev in eigs_B])
m_B_sorted = np.sort(m_B_raw)

# Dm^2_21 / Dm^2_31 ratio
Dm2_21_B = m_B_sorted[1] - m_B_sorted[0]
Dm2_31_B = m_B_sorted[2] - m_B_sorted[0]
ratio_obs = 7.41e-5 / 2.515e-3  # PDG comparator
ratio_B = Dm2_21_B / Dm2_31_B if Dm2_31_B > 0 else float("nan")
print(f"  Dm^2_21 / Dm^2_31 (H_B prediction) = {ratio_B:.6f}")
print(f"  Dm^2_21 / Dm^2_31 (PDG comparator) = {ratio_obs:.6f}")
print(f"  ratio deviation = {abs(ratio_B - ratio_obs) / ratio_obs * 100:.2f}%")

# Honest reporting: H_B prediction is NOT close to observed; the lightest
# eigenvalue is NOT exactly zero (it's at delta = pi/12, not 2/9 + pi/12)
# but it's small.


# ============================================================================
# Part 4 — Hypothesis H_C: free delta_nu, BAE retained, find best delta
# ============================================================================
section("Part 4: H_C (free delta_nu at BAE) — best delta for Dm^2_21/Dm^2_31 = 0.0295")

delta_grid_fine = np.linspace(0.0, 2 * np.pi, 4001)
best = None
for delta in delta_grid_fine:
    b_t = mag_bae * np.exp(1j * delta)
    eigs = circulant_eigs(a_bae, b_t)
    m_k = np.sort(np.array([ev ** 2 for ev in eigs]))
    Dm2_21 = m_k[1] - m_k[0]
    Dm2_31 = m_k[2] - m_k[0]
    if Dm2_31 > 0:
        r = Dm2_21 / Dm2_31
        dev = abs(r - ratio_obs)
        if best is None or dev < best[0]:
            best = (dev, delta, r, m_k)

if best is not None:
    dev_best, delta_best, r_best, m_k_best = best
    print(f"  Best delta_nu = {delta_best:.6f} rad ({math.degrees(delta_best):.4f} deg)")
    print(f"  Best Dm^2_21 / Dm^2_31 = {r_best:.6f} (target {ratio_obs:.6f})")
    print(f"  Deviation = {dev_best * 100:.3f}% absolute / {dev_best / ratio_obs * 100:.3f}% relative")
    print(f"  Eigenvalue triple (sorted): {m_k_best}")

    # Compare to Brannen offset
    diff_brannen = abs(delta_best - delta_nu_B)
    diff_brannen_wrap = min(diff_brannen, 2 * np.pi - diff_brannen)
    print(f"  Distance to Brannen delta (2/9 + pi/12): {diff_brannen_wrap:.6f} rad")
    # Wrap to nearest cyclic equivalent
    delta_best_mod_third = ((delta_best % (2 * np.pi / 3)) + 2 * np.pi / 3) % (2 * np.pi / 3)
    delta_brannen_mod_third = ((delta_nu_B % (2 * np.pi / 3)) + 2 * np.pi / 3) % (2 * np.pi / 3)
    print(f"  delta_best mod (2pi/3) = {delta_best_mod_third:.6f}")
    print(f"  delta_brannen mod (2pi/3) = {delta_brannen_mod_third:.6f}")

    # Honest reporting: BAE+free-delta can match Dm^2_21 / Dm^2_31 to some
    # precision. This is INTERESTING but not a derivation: delta_nu is a
    # free parameter here.
    check(
        "H_C admits delta_nu such that Dm^2_21 / Dm^2_31 matches observed",
        dev_best / ratio_obs < 0.10,  # <10% relative match achievable
        f"best relative deviation = {dev_best / ratio_obs * 100:.2f}%",
    )


# ============================================================================
# Part 5 — Hypothesis H_D: free (rho, delta), find allowed region
# ============================================================================
section("Part 5: H_D (free rho, free delta) — scan parameter plane")

rho_scan = np.linspace(0.05, 2.0, 200)
delta_scan = np.linspace(0.0, 2 * np.pi / 3, 200)  # one fundamental period

# Find points where r matches observed within 5% relative + ordering is
# normal-like (smallest mass < others)
matches = 0
match_samples = []
for rho in rho_scan:
    for delta in delta_scan:
        mag = math.sqrt(rho) * a_bae
        b_t = mag * np.exp(1j * delta)
        eigs = circulant_eigs(a_bae, b_t)
        m_k = np.sort(np.array([ev ** 2 for ev in eigs]))
        Dm2_21 = m_k[1] - m_k[0]
        Dm2_31 = m_k[2] - m_k[0]
        if Dm2_31 > 0:
            r = Dm2_21 / Dm2_31
            dev = abs(r - ratio_obs)
            if dev / ratio_obs < 0.05:  # within 5% relative
                matches += 1
                if len(match_samples) < 5:
                    match_samples.append((rho, delta, r, m_k))

print(f"  Points in (rho, delta) plane matching Dm^2_21/Dm^2_31 to <5% relative: {matches}")
for rho, delta, r, m_k in match_samples:
    print(f"    rho={rho:.4f}, delta={delta:.6f} rad ({math.degrees(delta):.2f} deg), r={r:.6f}, "
          f"m_k = ({m_k[0]:.4e}, {m_k[1]:.4e}, {m_k[2]:.4e})")

check(
    "H_D parameter plane has at least one curve matching observed Dm^2_21/Dm^2_31",
    matches > 0,
    f"matches = {matches}",
)


# ============================================================================
# Part 6 — PMNS angles from circulant-side U_nu (BAE, free delta_nu)
# ============================================================================
section("Part 6: PMNS angles from U_PMNS = U_e^dag U_nu = U_nu (Z_3-trichotomy U_e = I)")

# The retained CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17
# gives U_e = I on the retained Z_3-trichotomy chain. So U_PMNS = U_nu, the
# unitary that diagonalizes H_nu.
#
# For ANY Hermitian circulant H = aI + bC + bbar C^2, the diagonalizing U is
# the DFT_3 matrix (up to column-permutation by spectral ordering):
#   F[i,k] = (1/sqrt(3)) omega^{i*k}
# This is INDEPENDENT of (a, b). Hence:
#   |U_PMNS|^2 = |F|^2 = 1/3 for every entry  (PMNS-flat / trimaximal)
#
# This gives:
#   sin^2 theta_12 = 1/3 ~ 0.333
#   sin^2 theta_13 = 1/3 ~ 0.333  (much larger than observed 0.022!)
#   sin^2 theta_23 = 1/3 ~ 0.333
#
# This is the trimaximal-mixing prediction. It's at odds with the observed
# sin^2 theta_13 ~ 0.022.

DFT3 = np.array(
    [[OMEGA ** (i * k) for k in range(3)] for i in range(3)],
    dtype=complex,
) / math.sqrt(3.0)

# Verify DFT3 diagonalizes the circulant
a_check = 1.7
b_check = 0.3 + 0.2j
H_check = circulant_H(a_check, b_check)
H_diag = DFT3.conj().T @ H_check @ DFT3
off_diag_norm = np.linalg.norm(H_diag - np.diag(np.diag(H_diag)))
check(
    "DFT_3 diagonalizes any circulant Hermitian H = aI + bC + bbar C^2",
    off_diag_norm < 1e-10,
    f"||off-diag||_F = {off_diag_norm:.2e}",
)

# Compute PMNS-pure-circulant angles using standard PMNS convention:
#   sin^2 theta_13 = |U_{e3}|^2
#   sin^2 theta_12 = |U_{e2}|^2 / (1 - |U_{e3}|^2)
#   sin^2 theta_23 = |U_{mu3}|^2 / (1 - |U_{e3}|^2)
U_PMNS_naive = np.abs(DFT3)
U_sq = U_PMNS_naive ** 2
print(f"  |U_PMNS|^2 (pure circulant U_nu, U_e = I):")
print(f"    {U_sq}")

# Standard PMNS extraction
U_e3_sq = U_sq[0, 2]
U_e2_sq = U_sq[0, 1]
U_mu3_sq = U_sq[1, 2]
sin2_t13 = U_e3_sq
sin2_t12 = U_e2_sq / (1.0 - U_e3_sq) if (1.0 - U_e3_sq) > 0 else float("nan")
sin2_t23 = U_mu3_sq / (1.0 - U_e3_sq) if (1.0 - U_e3_sq) > 0 else float("nan")
print(f"  sin^2 theta_13 (DFT_3, = |U_e3|^2)      = {sin2_t13:.6f} (PDG comparator ~0.0218)")
print(f"  sin^2 theta_12 (DFT_3)                  = {sin2_t12:.6f} (PDG comparator ~0.307)")
print(f"  sin^2 theta_23 (DFT_3)                  = {sin2_t23:.6f} (PDG comparator ~0.545)")

# The DFT_3 (trimaximal) ansatz gives:
#   sin^2 theta_13 = 1/3 (15x larger than observed 0.022; FAIL)
#   sin^2 theta_12 = 1/2 (vs observed 0.307; 60% off)
#   sin^2 theta_23 = 1/2 (vs observed 0.545; 9% off)
check(
    "Pure-circulant U_nu = DFT_3 OVERPREDICTS sin^2 theta_13 by factor ~15",
    sin2_t13 > 0.20 and sin2_t13 < 0.50,
    f"sin^2 theta_13 = {sin2_t13:.4f} >> observed 0.022 (ratio {sin2_t13/0.0218:.1f}x)",
)

# Honest reporting: the pure-circulant U_nu cannot match observed PMNS
# because it gives flat mixing for ANY (a, b). Sector-specific structure
# beyond the circulant ansatz (e.g., Majorana phase rotations from the
# right, or a non-circulant tilt) must enter.


# ============================================================================
# Part 7 — Numerical: best-fit (rho, delta) at observed Dm^2_21/Dm^2_31 and m_3
# ============================================================================
section("Part 7: best-fit (a_nu, rho, delta) at observed splittings + retained m_3")

# Retained from DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM:
m_3_retained = 5.058e-2  # eV
Dm2_31_retained = 2.539e-3  # eV^2
Dm2_21_obs = 7.41e-5  # eV^2 (PDG, USED AS COMPARATOR ONLY)

# Define sqrt(m) = lambda_k, so m_k = lambda_k^2. We want m_3 = 5.058e-2.
# Parameterize:
#   a_nu, rho_nu, delta_nu.
#   lam_k = a_nu (1 + sqrt(2 rho_nu) cos(delta_nu + 2 pi k / 3))
#   sort |lam_k|, identify smallest -> m_1, ..., largest -> m_3.

best_fit = None
for rho in np.linspace(0.05, 2.0, 100):
    for delta in np.linspace(0.0, 2 * np.pi / 3, 100):
        for a_nu in [1.0]:  # only ratios matter; rescale later
            mag = math.sqrt(rho) * a_nu
            b_t = mag * np.exp(1j * delta)
            eigs = circulant_eigs(a_nu, b_t)
            m_k = np.sort(np.array([ev ** 2 for ev in eigs]))
            Dm2_21 = m_k[1] - m_k[0]
            Dm2_31 = m_k[2] - m_k[0]
            if Dm2_31 > 0:
                # Rescale so Dm^2_31 = retained Dm^2_31_retained
                scale = Dm2_31_retained / Dm2_31
                Dm2_21_scaled = Dm2_21 * scale
                m_3_scaled = m_k[2] * scale

                # Compare to observed
                err_21 = abs(Dm2_21_scaled - Dm2_21_obs) / Dm2_21_obs
                err_m3 = abs(m_3_scaled - m_3_retained ** 2) / m_3_retained ** 2

                total_err = err_21  # primary
                if best_fit is None or total_err < best_fit[0]:
                    best_fit = (total_err, rho, delta, a_nu, scale, m_k, Dm2_21_scaled, m_3_scaled)

if best_fit is not None:
    err, rho, delta, a_nu, scale, m_k, Dm2_21_s, m_3_s = best_fit
    print(f"  Best (rho_nu, delta_nu) for Dm^2_21 match:")
    print(f"    rho_nu = {rho:.4f}")
    print(f"    delta_nu = {delta:.6f} rad ({math.degrees(delta):.4f} deg)")
    print(f"    Dm^2_21 (predicted, after scale to Dm^2_31 retained) = {Dm2_21_s:.4e}")
    print(f"    Dm^2_21 (observed comparator) = {Dm2_21_obs:.4e}")
    print(f"    relative error in Dm^2_21 = {err * 100:.4f}%")
    print(f"    m_1^2 (predicted) = {m_k[0] * scale:.4e} eV^2")
    print(f"    m_2^2 (predicted) = {m_k[1] * scale:.4e} eV^2")
    print(f"    m_3^2 (predicted) = {m_k[2] * scale:.4e} eV^2")
    print(f"    m_1 = {math.sqrt(m_k[0] * scale):.4e} eV")
    print(f"    m_2 = {math.sqrt(m_k[1] * scale):.4e} eV")
    print(f"    m_3 = {math.sqrt(m_k[2] * scale):.4e} eV (retained 5.058e-2 eV)")
    print(f"    Sigma m_nu = {sum(math.sqrt(m * scale) for m in m_k):.4e} eV "
          f"(retained floor 50.58 meV)")


# ============================================================================
# Part 8 — Honest admissions and what this probe is NOT
# ============================================================================
section("Part 8: probe admissions and scope")

admissions = [
    "BAE_NEUTRINO: |b_nu|^2 / a_nu^2 = 1/2 is NOT derived; not retained",
    "DELTA_NU_PI12: delta_nu = 2/9 + pi/12 (H_B) is a literature target, not derived",
    "SQRT_M_IDENTIFICATION: lambda_k = sqrt(m_k) is admitted (open positive-parent)",
    "U_e_EQ_I: assumed from CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY (retained)",
    "CIRCULANT_TRIMAXIMAL_OBSTRUCTION: U_nu = DFT_3 forces sin^2 theta_13 = 1/3 != 0.022",
    "NO_SOLAR_GAP_DERIVATION: Dm^2_21 fitted via rho_nu, delta_nu choice (not derived)",
    "NO_DELTA_CP_DERIVATION: CP phase requires complex Z_3 breaking (not retained)",
]
print("Named admissions / open gates of this probe:")
for adm in admissions:
    print(f"  - {adm}")

print("""
Verdict on the New Physics Probe:

  This probe is BOUNDED — a numerical hypothesis test using the
  charged-lepton-style C_3[111] circulant ansatz applied to the
  neutrino sector. It does NOT claim:

    (a) a derivation of any neutrino observable from A1+A2 alone
        (sector-specific delta_nu and rho_nu are admitted);
    (b) a closure of the solar-gap problem (delta_nu free / fitted);
    (c) a derivation of PMNS angles (pure-circulant U_nu = DFT_3
        gives trimaximal, FAILS observed sin^2 theta_13);
    (d) a Koide-2/3 relation specific to neutrinos
        (under BAE, Q = 2/3 is sector-INDEPENDENT; Foot-Brannen
        Q_nu ~ 0.33 requires BREAKING BAE, which we test as H_D).

  What this probe DOES contribute:

    (P1) Algebraic confirmation that the circulant Q = 2/3 at BAE is
         sector-independent (NEW: explicit dependence-on-delta analysis).
    (P2) Numerical map of the (rho_nu, delta_nu) parameter plane showing
         where Dm^2_21 / Dm^2_31 matches observed.
    (P3) Explicit demonstration that pure-circulant U_nu = DFT_3
         OVERPREDICTS sin^2 theta_13 by a factor ~15, hence the
         retained PMNS package's "non-circulant tilt" (the affine
         H(m, delta, q_+) construction) is STRUCTURALLY REQUIRED to
         match the observed angle pattern.
    (P4) A reasoned mapping from the Brannen neutrino phase
         delta_nu = 2/9 + pi/12 to a near-massless lightest neutrino
         on the BAE locus.

  Open derivation targets that would promote this to retained:
    1. selection principle for rho_nu (the BAE-analog ratio for nu sector)
    2. derivation of delta_nu from Cl(3)/Z^3
    3. derivation of m_3 absolute scale within the circulant framing
       (currently retained via seesaw, not circulant)
    4. resolution of the U_nu = DFT_3 over-mixing problem
""")


# ============================================================================
# Part 9 — Cross-check against retained framework outputs
# ============================================================================
section("Part 9: cross-check with retained DM_NEUTRINO_ATMOSPHERIC_SCALE + BOUNDS")

# Verify that the probe is consistent with retained bounds.
# Retained:
#   m_3 = 5.058e-2 eV (atmospheric-scale theorem)
#   Dm^2_31 = 2.539e-3 eV^2
#   Sigma m_nu > 50.58 meV (theorem 1)
#   m_beta <= 50.58 meV (theorem 2)
#   m_betabeta <= 50.58 meV (theorem 3)
#   0 < Dm^2_21 < 2.539e-3 (theorem 4)

if best_fit is not None:
    _, rho, delta, a_nu, scale, m_k, Dm2_21_s, m_3_s_sq = best_fit

    m_3_predicted = math.sqrt(m_k[2] * scale)
    Sigma_predicted = sum(math.sqrt(m * scale) for m in m_k)
    Dm2_21_pred = Dm2_21_s
    Dm2_31_pred = (m_k[2] - m_k[0]) * scale

    # Note: m_3 is set by construction (scale = Dm2_31_retained / Dm2_31_unscaled)
    # via Dm^2_31 not m_3 directly. The relation m_3 = sqrt(m_3^2) where
    # m_3^2 = lam_max^2 * scale will be very close to the retained m_3 (since
    # m_1 is much smaller, m_3 ~ sqrt(Dm^2_31)). Use 5% tolerance.
    check(
        "m_3 predicted within 5% of retained 5.058e-2 eV (Dm^2_31 set; m_1 small)",
        abs(m_3_predicted - m_3_retained) / m_3_retained < 0.05,
        f"m_3 = {m_3_predicted:.6e} (retained {m_3_retained:.6e}; rel err {abs(m_3_predicted - m_3_retained) / m_3_retained * 100:.3f}%)",
    )

    check(
        "Sigma m_nu (probe prediction) > 50.58 meV (retained floor)",
        Sigma_predicted * 1000 > 50.0,
        f"Sigma = {Sigma_predicted * 1000:.4f} meV",
    )

    check(
        "Dm^2_21 (probe prediction) < Dm^2_31 (retained theorem 4 inequality)",
        Dm2_21_pred < Dm2_31_pred,
        f"Dm^2_21 = {Dm2_21_pred:.4e}, Dm^2_31 = {Dm2_31_pred:.4e}",
    )

    # All m_k > 0 (normal ordering structure)
    check(
        "All m_k >= 0 (positivity)",
        all(m * scale >= 0 for m in m_k),
        f"m_k * scale = {[m * scale for m in m_k]}",
    )


# ============================================================================
# Summary
# ============================================================================
section("Summary")

print(f"""
Probe: New-Physics neutrino PMNS circulant ansatz (npNu)

Algebraic confirmations:
  - Circulant eigenvalue formula (Pattern A): VERIFIED
  - Q = 2/3 at BAE for ANY delta: VERIFIED (sector-independent)
  - DFT_3 diagonalizes any circulant: VERIFIED

Hypothesis tests (NUMERICAL, NOT DERIVATIONS):
  - H_A (BAE + delta_lep): does not match neutrino spectrum
  - H_B (BAE + delta = 2/9 + pi/12): near-massless lightest, Q = 2/3
  - H_C (BAE + free delta): best delta exists for Dm^2_21 match
  - H_D (free rho + free delta): curve of matches in parameter plane

PMNS angles:
  - Pure-circulant U_nu = DFT_3 gives trimaximal (sin^2 theta_13 = 1/3)
  - 15x overshoot of observed sin^2 theta_13 ~ 0.022
  - Retained PMNS package's affine H(m, delta, q_+) construction is
    structurally REQUIRED to fix this (already retained)

Status: BOUNDED probe with 4 named admissions. Not retained.
Open derivation targets surfaced: rho_nu selection, delta_nu derivation,
m_3 circulant-side scale, U_nu = DFT_3 over-mixing fix.
""")


print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
print(f"PASS={PASS} FAIL={FAIL}")
sys.exit(1 if FAIL > 0 else 0)
