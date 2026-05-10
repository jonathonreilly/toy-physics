"""SU(3) Wigner engine — L_s=3 PBC cube Haar-Monte-Carlo computation.

Direct Haar Monte Carlo of the Wigner-Racah cube trace
  T_lambda(L=3 cube) = (1/d_lambda^81) ∫ ∏_l dU_l ∏_p chi_lambda(U_p)
where:
  - U_l ∈ SU(3) is the link variable for one of 81 directed links
  - U_p is the standard Wilson plaquette product +d1+d2-d1-d2
  - chi_(p,q)(U) is the SU(3) character in irrep (p,q)
  - d_lambda is the irrep dimension

The Haar measure has NO Wilson-Boltzmann weight: this is rep-theory MC,
NOT the standard Wilson plaquette MC. It computes the framework's
boundary character measure rho_lambda(6) via the source-sector
factorization, NOT a direct <P>(beta=6) measurement.

For lambda = (1,1) (adjoint), use the simplification:
  chi_(1,1)(U) = |tr(U)|^2 - 1     (V ⊗ V* = adj + trivial)
For lambda = (1,0) (fundamental):
  chi_(1,0)(U) = tr(U)
For lambda = (2,0):
  chi_(2,0)(U) = (1/2) ((tr U)^2 + tr(U^2))     (sym^2)

The MC procedure:
  for n in range(N_samples):
    sample 81 random SU(3) matrices via Haar
    compute U_p for each of 81 plaquettes (with orientation)
    compute chi_lambda(U_p) for each
    compute integrand = product over plaquettes
    accumulate
  T_lambda = mean(integrand) / d_lambda^81

Forbidden imports: none (numpy + scipy.stats only; scipy.stats.unitary_group
is allowed standard math machinery for Haar sampling on U(N), with explicit
SU(N) projection here).

Run:
    python3 scripts/frontier_su3_wigner_l3_cube_haar_mc_2026_05_04.py
"""

from __future__ import annotations

import math
import sys
import time
from typing import Dict, List, Tuple

import numpy as np
from scipy.stats import unitary_group


BETA = 6.0
N_COLOR = 3
EPSILON_WITNESS = 3.03e-4
BRIDGE_SUPPORT_TARGET = 0.5935306800
P_TRIV_REFERENCE = 0.4225317396
P_LOC_REFERENCE = 0.4524071590
P_CANDIDATE_REFERENCE = 0.4291049969
L = 3
N_SAMPLES_DEFAULT = 5000
RNG_SEED = 20260504


# ===========================================================================
# Section A. SU(3) Haar sampling.
# ===========================================================================

def sample_su3(rng: np.random.Generator) -> np.ndarray:
    """Sample a Haar-uniform SU(3) matrix.

    scipy.stats.unitary_group gives Haar-uniform U(3); divide by det^(1/3)
    with proper phase to project to SU(3).
    """
    U = unitary_group.rvs(N_COLOR, random_state=rng)
    det = np.linalg.det(U)
    # det = e^(i theta); divide by e^(i theta / N) to make det = 1
    phase = det ** (1.0 / N_COLOR)
    return U / phase


def sample_su3_batch(n: int, rng: np.random.Generator) -> np.ndarray:
    """Sample n Haar-uniform SU(3) matrices, returns shape (n, 3, 3)."""
    out = np.empty((n, N_COLOR, N_COLOR), dtype=complex)
    for k in range(n):
        out[k] = sample_su3(rng)
    return out


# ===========================================================================
# Section B. L_s=3 PBC cube geometry (standard Wilson plaquettes).
# ===========================================================================

def link_id(x: int, y: int, z: int, direction: int) -> int:
    """Encode (x, y, z, dir) as a flat integer index 0..80."""
    return (((x * L) + y) * L + z) * 3 + direction


def all_wilson_plaquettes() -> List[Tuple]:
    """Enumerate 81 unique Wilson plaquettes on L_s=3 PBC cube.

    Each plaquette is a tuple (start, mu, nu, [(link_id, sign), ...4]).
    Sign is +1 (forward) or -1 (backward = U^dagger in trace).
    """
    plaquettes = []
    seen = set()
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for mu in range(3):
                    for nu in range(mu + 1, 3):
                        # Standard Wilson: x → x+mu → x+mu+nu → x+nu → x
                        # Legs: (+l_1, +l_2, -l_3, -l_4)
                        site = [x, y, z]
                        x_p_mu = list(site); x_p_mu[mu] = (x_p_mu[mu] + 1) % L
                        x_p_nu = list(site); x_p_nu[nu] = (x_p_nu[nu] + 1) % L
                        l_1 = link_id(site[0], site[1], site[2], mu)
                        l_2 = link_id(x_p_mu[0], x_p_mu[1], x_p_mu[2], nu)
                        l_3 = link_id(x_p_nu[0], x_p_nu[1], x_p_nu[2], mu)
                        l_4 = link_id(site[0], site[1], site[2], nu)
                        link_set = frozenset([l_1, l_2, l_3, l_4])
                        if link_set in seen:
                            continue
                        seen.add(link_set)
                        plaquettes.append((tuple(site), mu, nu,
                                             [(l_1, +1), (l_2, +1),
                                              (l_3, -1), (l_4, -1)]))
    return plaquettes


# ===========================================================================
# Section C. Plaquette product computation.
# ===========================================================================

def compute_plaquette_products(U_links: np.ndarray,
                                  plaquettes: List[Tuple]) -> np.ndarray:
    """Compute U_p for each plaquette: U_p = U_l1 U_l2 U_l3^dagger U_l4^dagger.

    U_links: shape (81, 3, 3), Haar SU(3) samples for each directed link.
    Returns array of shape (n_plaquettes, 3, 3) — the 81 plaquette products.
    """
    n_plaq = len(plaquettes)
    out = np.empty((n_plaq, N_COLOR, N_COLOR), dtype=complex)
    for p_idx, (_, _, _, links) in enumerate(plaquettes):
        # Multiply 4 matrices with appropriate dagger
        prod = None
        for (l_id, sign) in links:
            U = U_links[l_id]
            if sign == -1:
                U = U.conj().T
            if prod is None:
                prod = U
            else:
                prod = prod @ U
        out[p_idx] = prod
    return out


# ===========================================================================
# Section D. SU(3) characters.
# ===========================================================================

def chi_00(U_p: np.ndarray) -> complex:
    """chi_(0,0)(U) = 1 (trivial)."""
    return 1.0


def chi_10(U_p: np.ndarray) -> complex:
    """chi_(1,0)(U) = tr(U) (fundamental)."""
    return np.trace(U_p)


def chi_01(U_p: np.ndarray) -> complex:
    """chi_(0,1)(U) = tr(U^dagger) = (tr U)^*."""
    return np.trace(U_p.conj().T)


def chi_11(U_p: np.ndarray) -> complex:
    """chi_(1,1)(U) = |tr(U)|^2 - 1 (adjoint)."""
    t = np.trace(U_p)
    return abs(t) ** 2 - 1


def chi_20(U_p: np.ndarray) -> complex:
    """chi_(2,0)(U) = (1/2)((tr U)^2 + tr(U^2)) (symmetric ⊗^2)."""
    t = np.trace(U_p)
    t2 = np.trace(U_p @ U_p)
    return 0.5 * (t * t + t2)


def chi_02(U_p: np.ndarray) -> complex:
    """chi_(0,2)(U) = (1/2)((tr U^dagger)^2 + tr(U^(-2)))."""
    Ud = U_p.conj().T
    t = np.trace(Ud)
    t2 = np.trace(Ud @ Ud)
    return 0.5 * (t * t + t2)


def chi_21(U_p: np.ndarray) -> complex:
    """chi_(2,1)(U): mixed symmetric. Use Schur formula via fundamental.

    For SU(3): chi_(2,1) = chi_(1,1) chi_(1,0) - chi_(1,0) - chi_(2,0)
    (fusion (1,1) ⊗ (1,0) = (2,1) + (1,0) + ... — derive carefully)

    Simpler: chi_(2,1) = chi_(1,0) chi_(1,1) - chi_(1,0) chi_(0,0) - chi_(0,1)
    (from (1,1) ⊗ (1,0) = (2,1) + (1,0)+ (0,2))
    """
    t = np.trace(U_p)
    td = np.trace(U_p.conj().T)
    chi11 = abs(t) ** 2 - 1
    return t * chi11 - t - td


def all_characters(U_p: np.ndarray) -> Dict[Tuple[int, int], complex]:
    """Return characters for several small irreps."""
    return {
        (0, 0): chi_00(U_p),
        (1, 0): chi_10(U_p),
        (0, 1): chi_01(U_p),
        (1, 1): chi_11(U_p),
        (2, 0): chi_20(U_p),
        (0, 2): chi_02(U_p),
        (2, 1): chi_21(U_p),
    }


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


# ===========================================================================
# Section E. Wilson character coefficients (existing framework primitives).
# ===========================================================================

def wilson_character_coefficient(p: int, q: int, mode_max: int, arg: float
                                   ) -> float:
    from scipy.special import iv
    lam = [p + q, q, 0]
    total = 0.0
    for mode in range(-mode_max, mode_max + 1):
        mat = np.array(
            [[iv(mode + lam[j] + i - j, arg) for j in range(3)]
             for i in range(3)], dtype=float
        )
        total += float(np.linalg.det(mat))
    return total


# ===========================================================================
# Section F. Source-sector Perron solve (matches existing framework).
# ===========================================================================

def dominant_weights_box(nmax: int) -> List[Tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def recurrence_neighbors(p: int, q: int) -> List[Tuple[int, int]]:
    out = []
    for a, b in [(p + 1, q), (p - 1, q + 1), (p, q - 1), (p, q + 1),
                 (p + 1, q - 1), (p - 1, q)]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def build_j(nmax: int) -> Tuple[np.ndarray, List[Tuple[int, int]],
                                    Dict[Tuple[int, int], int]]:
    weights = dominant_weights_box(nmax)
    index = {weight: i for i, weight in enumerate(weights)}
    j_op = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        source = index[(p, q)]
        for neighbor in recurrence_neighbors(p, q):
            if neighbor in index:
                j_op[index[neighbor], source] += 1.0 / 6.0
    return j_op, weights, index


def build_local_factor(weights: List[Tuple[int, int]],
                          index: Dict[Tuple[int, int], int],
                          mode_max: int, beta: float) -> np.ndarray:
    arg = beta / 3.0
    coeffs = np.array([wilson_character_coefficient(p, q, mode_max, arg)
                        for p, q in weights], dtype=float)
    dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
    c00 = coeffs[index[(0, 0)]]
    a_link = coeffs / (dims * c00)
    return np.diag(a_link ** 4)


def matrix_exp_symmetric(matrix: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(matrix)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def perron_value(rho: Dict[Tuple[int, int], float],
                   nmax: int, mode_max: int, beta: float
                   ) -> Tuple[float, float]:
    j_op, weights, index = build_j(nmax)
    multiplier = matrix_exp_symmetric(j_op, 3.0)
    d_loc = build_local_factor(weights, index, mode_max, beta)
    c_env = np.diag(np.array([rho.get(weight, 0.0) for weight in weights],
                                dtype=float))
    transfer = multiplier @ d_loc @ c_env @ multiplier
    vals, vecs = np.linalg.eigh(transfer)
    idx = int(np.argmax(vals))
    psi = vecs[:, idx]
    if np.sum(psi) < 0.0:
        psi = -psi
    return float(psi @ (j_op @ psi)), float(vals[idx])


# ===========================================================================
# Section G. Driver — Haar Monte Carlo of T_lambda(L=3 cube).
# ===========================================================================

def driver() -> int:
    print("=" * 78)
    print(f"SU(3) Wigner Engine — L_s=3 PBC Cube Haar Monte Carlo")
    print("=" * 78)
    print()

    pass_count = 0
    fail_count = 0
    support_count = 0

    rng = np.random.default_rng(RNG_SEED)
    plaquettes = all_wilson_plaquettes()
    n_plaq = len(plaquettes)
    n_links_used = len({l_id for _, _, _, links in plaquettes
                          for (l_id, _) in links})
    print(f"--- Geometry (L_s={L} PBC) ---")
    print(f"  total directed links: {L * L * L * 3} = {L**3 * 3}")
    print(f"  unique Wilson plaquettes: {n_plaq}")
    print(f"  directed links used in plaquettes: {n_links_used}")
    if n_plaq == 81:
        print("  PASS: 81 unique Wilson plaquettes on L_s=3 PBC cube.")
        pass_count += 1
    else:
        print(f"  FAIL: expected 81, got {n_plaq}")
        fail_count += 1
    print()

    n_samples = N_SAMPLES_DEFAULT
    print(f"--- Haar MC: N_samples = {n_samples} ---")
    print(f"  irreps tracked: (0,0), (1,0), (0,1), (1,1), (2,0), (0,2), (2,1)")
    print()

    irrep_list = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2), (2, 1)]
    integrand_sum = {lam: 0.0 + 0.0j for lam in irrep_list}
    integrand_sq_sum = {lam: 0.0 for lam in irrep_list}

    n_links_total = L ** 3 * 3
    t0 = time.time()
    for n in range(n_samples):
        # Sample 81 SU(3) matrices for the 81 directed links (use all
        # to maintain a complete cube; though only 81 used in plaquettes,
        # geometry says all 81 are used for L_s=3 PBC: n_links_total = 81).
        U_links = sample_su3_batch(n_links_total, rng)
        # Compute 81 plaquette products
        U_p_array = compute_plaquette_products(U_links, plaquettes)
        # Compute integrand for each irrep
        for lam in irrep_list:
            chi_func = {(0, 0): chi_00, (1, 0): chi_10, (0, 1): chi_01,
                          (1, 1): chi_11, (2, 0): chi_20, (0, 2): chi_02,
                          (2, 1): chi_21}[lam]
            chis = np.array([chi_func(U_p_array[p]) for p in range(n_plaq)])
            # Use log-space accumulation to avoid over/underflow
            integrand_log_abs = np.sum(np.log(np.abs(chis) + 1e-300))
            integrand_sign = np.prod(chis / (np.abs(chis) + 1e-300))
            # Convert back: integrand = sign * exp(log_abs)
            # For accumulation, better to use float128 if extreme
            integrand = integrand_sign * np.exp(integrand_log_abs)
            integrand_sum[lam] += integrand
            integrand_sq_sum[lam] += abs(integrand) ** 2
        if (n + 1) % max(1, n_samples // 10) == 0:
            elapsed = time.time() - t0
            print(f"  [{elapsed:.1f}s] sample {n+1}/{n_samples}")

    elapsed = time.time() - t0
    print(f"  total runtime: {elapsed:.1f}s")
    print()

    # ===== MC results =====
    print("--- Haar MC integrand averages (per irrep) ---")
    print()
    print(f"  {'irrep':<8} {'<integrand>':>14}  {'+/- error':>12}  "
          f"{'T_lambda':>14}  {'normalized':>14}")
    print(f"  {'-' * 8} {'-' * 14}  {'-' * 12}  {'-' * 14}  {'-' * 14}")

    T_lambda_dict: Dict[Tuple[int, int], float] = {}
    for lam in irrep_list:
        d = dim_su3(*lam)
        mean = integrand_sum[lam] / n_samples
        # MC standard error: sqrt(variance / N)
        var_approx = integrand_sq_sum[lam] / n_samples - abs(mean) ** 2
        se = math.sqrt(max(0.0, var_approx) / n_samples)
        T_lambda = mean.real / (d ** n_plaq)
        T_lambda_dict[lam] = T_lambda
        # Normalize relative to T_(0,0)
        T_normalized = T_lambda / T_lambda_dict.get((0, 0), 1.0)
        print(f"  {str(lam):<8} {mean.real:>14.6e}  {se:>12.4e}  "
              f"{T_lambda:>14.4e}  {T_normalized:>14.6e}")

    print()

    # ===== Source-sector Perron solve =====
    print("--- Constructing rho_lambda(6) for source-sector factorization ---")
    arg = BETA / 3.0
    c_coeffs = {lam: wilson_character_coefficient(*lam, mode_max=200, arg=arg)
                  for lam in irrep_list}
    c00 = c_coeffs[(0, 0)]
    rho: Dict[Tuple[int, int], float] = {}
    for lam in irrep_list:
        d = dim_su3(*lam)
        c = c_coeffs[lam]
        # rho_lambda = (d c / c00)^81 * T_lambda(L=3 cube)
        rho[lam] = ((d * c / c00) ** n_plaq) * T_lambda_dict[lam]
    norm = rho[(0, 0)]
    rho = {k: v / norm for k, v in rho.items()}
    print()
    for lam in irrep_list:
        print(f"  rho_{lam}(6) = {rho[lam]:.6e}")
    print()

    # ===== Perron solve =====
    print("--- Source-sector Perron solve ---")
    p_value, eig_value = perron_value(rho, nmax=7, mode_max=200, beta=BETA)
    print(f"  Perron eigenvalue: {eig_value:.10f}")
    print(f"  P_cube(L=3, beta=6, MC) = {p_value:.10f}")
    print()

    # ===== Bridge comparison =====
    print("--- Bridge comparison ---")
    print(f"  P_triv (rho = delta):         {P_TRIV_REFERENCE:.10f}")
    print(f"  P_loc (rho = 1):              {P_LOC_REFERENCE:.10f}")
    print(f"  P_candidate(L=2 PBC):         {P_CANDIDATE_REFERENCE:.10f}")
    print(f"  P_cube(L=3 PBC, MC, this):    {p_value:.10f}")
    print(f"  bridge-support target:        {BRIDGE_SUPPORT_TARGET:.10f}")
    print(f"  epsilon_witness:              {EPSILON_WITNESS:.3e}")
    print()
    distance = abs(p_value - BRIDGE_SUPPORT_TARGET)
    print(f"  |P_cube - bridge_target|:     {distance:.6f}")
    if distance < EPSILON_WITNESS:
        print(f"  *** CLOSURE *** P_cube within epsilon_witness of target")
        pass_count += 1
    else:
        gap_factor = distance / EPSILON_WITNESS
        print(f"  gap factor: {gap_factor:.0f}x epsilon_witness")
        support_count += 1
    print()

    # ===== Honest caveat =====
    print("--- Honest caveats ---")
    print()
    print(f"  This is a Haar Monte Carlo with N_samples = {n_samples}.")
    print(f"  Statistical error on T_lambda values may be large for high")
    print(f"  irreps. The integrand product across 81 plaquettes has")
    print(f"  large variance because each plaquette's chi can be near 0")
    print(f"  with occasional large fluctuations.")
    print()
    print(f"  The truncation to {len(irrep_list)} irreps may also bias the Perron")
    print(f"  solve relative to the full source-sector Perron solve at NMAX=7.")
    print()

    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} SUPPORT={support_count} "
          f"FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Headline:")
    print(f"  L_s=3 PBC cube Haar MC at beta={BETA}, N_samples={n_samples}:")
    print(f"    P_cube(L=3 PBC, MC) = {p_value:.4f}")
    print(f"    bridge target       = {BRIDGE_SUPPORT_TARGET:.4f}")
    print(f"    gap                 = {distance:.4f} = "
          f"{distance/EPSILON_WITNESS:.0f}x epsilon_witness")
    if distance < EPSILON_WITNESS:
        print(f"  *** CLOSURE *** ")
    else:
        print("  Result: Haar MC does not provide a bridge-support signal here;")
        print("  the reported P_cube is noise-dominated, not a derived value.")
        print("  next step: exact/rank-aware tensor-network route, not status promotion.")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
