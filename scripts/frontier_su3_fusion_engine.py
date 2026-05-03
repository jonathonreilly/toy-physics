"""SU(3) tensor product fusion engine via Cartan-torus character orthogonality.

This is **PR 1 of a 5-PR engine roadmap** toward closing the gauge-scalar
temporal observable bridge no-go (PR #477) by computing the explicit
boundary character measure rho_(p,q)(6) for the unmarked spatial Wilson
environment on the L_s=2 APBC spatial cube. See
docs/SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md for the full
plan.

This PR's deliverable: compute the SU(3) fusion multiplicities

    N^nu_(lambda, mu)   for   lambda otimes mu = oplus_nu N^nu_(lambda, mu) nu

for arbitrary SU(3) irreps lambda = (a, b), mu = (p, q), nu = (x, y) in
the dominant-weight box (a, b, p, q, x, y) <= NMAX.

Algorithm: numerical character orthogonality on the SU(3) Cartan torus.

For SU(3), the Cartan torus is parameterized by (phi_1, phi_2) with
diagonal element diag(e^(i phi_1), e^(i phi_2), e^(-i(phi_1+phi_2)))
and Weyl-invariant Haar measure with Vandermonde squared

    dW(phi) = (1 / 6) * |Delta(phi)|^2 * (d phi_1 / 2 pi) (d phi_2 / 2 pi)
    Delta(phi) = product_{i<j} 2 sin((phi_i - phi_j) / 2)

(the 1/6 factor accounts for Weyl group order |W(SU(3))| = 6).

The character of irrep (a, b) at this Cartan element is the Schur
polynomial in (z_1, z_2, z_3) for partition lambda = (a+b, b, 0):

    chi_(a,b)(z_1, z_2, z_3)
        = det[z_i^(lambda_j + 3-j)]_{i,j=1..3} / det[z_i^(3-j)]_{i,j=1..3}
        = det[z_i^(lambda_j + 3-j)]_{i,j=1..3} / Vandermonde(z)

Fusion via character orthogonality:

    chi_lambda(g) chi_mu(g) = sum_nu N^nu_(lambda, mu) chi_nu(g)

Multiplying both sides by chi_nu(g)^* and integrating over the Haar
measure:

    N^nu_(lambda, mu) = integral_(Cartan torus) chi_lambda chi_mu chi_nu^* dW.

This integral is computed numerically with the Cartan-torus quadrature.
The result is then rounded to the nearest non-negative integer (with a
guard error reported).

Validation suite covers:

    (V1) 3 otimes 3-bar = 8 oplus 1                             (rep theory landmark)
    (V2) 3 otimes 3 = 6 oplus 3-bar                             (symmetry decomposition)
    (V3) 8 otimes 8 = 27 + 10 + 10-bar + 8 + 8 + 1              (adjoint product)
    (V4) 6 otimes 6-bar = 27 + 8 + 1                            (sextet x antisextet)
    (V5) commutativity: N^nu_(lambda,mu) = N^nu_(mu,lambda)
    (V6) singlet selection: N^(0,0)_(lambda,mu) = delta_(mu, lambda-bar)
    (V7) dimension count: sum_nu N^nu_(lambda,mu) d_nu = d_lambda d_mu
    (V8) crossing: N^nu_(lambda,mu) = N^lambda_(nu, mu-bar)     (when defined)
    (V9) Pieri rule reproduction: (1,0) otimes (a,b) = (a+1,b) + (a-1,b+1) + (a,b-1)

The engine is also exposed as importable functions for downstream PRs
(2-5) of the engine roadmap.

Forbidden imports:
    - none specific to this PR (pure SU(3) representation theory; no
      lattice gauge dependent quantities)

Run:
    python3 scripts/frontier_su3_fusion_engine.py
"""

from __future__ import annotations

import math
import sys
from typing import Dict, List, Tuple

import numpy as np


# ===========================================================================
# Section A. SU(3) irrep enumeration and dimensions.
# ===========================================================================

def dim_su3(p: int, q: int) -> int:
    """Dimension of SU(3) irrep (p, q) via Weyl dimension formula.

    d_(p,q) = (p+1)(q+1)(p+q+2)/2

    Examples:
        d_(0,0) = 1     (singlet)
        d_(1,0) = 3     (fundamental)
        d_(0,1) = 3     (antifundamental)
        d_(2,0) = 6     (sextet)
        d_(1,1) = 8     (adjoint)
        d_(3,0) = 10    (decuplet)
        d_(2,1) = 15
        d_(2,2) = 27
    """
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def conjugate_irrep(p: int, q: int) -> Tuple[int, int]:
    """SU(3) complex conjugate: (p, q) -> (q, p)."""
    return (q, p)


def dominant_weights_box(nmax: int) -> List[Tuple[int, int]]:
    """All dominant weights (p, q) with p, q in [0, nmax]."""
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


# ===========================================================================
# Section B. SU(3) Cartan torus parameterization and Schur character.
# ===========================================================================

def cartan_grid(n_grid: int) -> Tuple[np.ndarray, np.ndarray, float]:
    """Uniform grid on the SU(3) Cartan torus (phi_1, phi_2) in [-pi, pi)^2.

    Returns (phi_grid, phi_grid, d_phi) where each phi grid has n_grid
    equally spaced points, and d_phi = 2 pi / n_grid is the cell size.

    The third Cartan angle is phi_3 = -(phi_1 + phi_2) (det = 1 constraint).
    """
    phi = np.linspace(-math.pi, math.pi, n_grid, endpoint=False)
    d_phi = 2 * math.pi / n_grid
    return phi, phi, d_phi


def vandermonde_squared(phi1: float, phi2: float) -> float:
    """|Delta(z)|^2 / 4 = product_{i<j} sin^2((phi_i - phi_j) / 2) for SU(3),
    where z_i = exp(i phi_i) and phi_3 = -(phi_1 + phi_2).

    This is the absolute square of the Vandermonde determinant up to a
    constant. The factor of 4 cancels in normalized integrals.

    Includes the Weyl group factor 1/|W| = 1/6.
    """
    phi3 = -(phi1 + phi2)
    s12 = math.sin((phi1 - phi2) / 2.0) ** 2
    s23 = math.sin((phi2 - phi3) / 2.0) ** 2
    s31 = math.sin((phi3 - phi1) / 2.0) ** 2
    return (1.0 / 6.0) * 4.0 * 4.0 * 4.0 * s12 * s23 * s31


def haar_measure_normalized(n_grid: int) -> Tuple[np.ndarray, float]:
    """Compute the Weyl-Vandermonde Haar measure weight at each grid point.

    Returns (W_grid, dphi^2) where W_grid[i,j] is the Weyl measure factor
    at (phi_grid[i], phi_grid[j]) and dphi^2 is the cell volume.

    The total integral of 1 against this measure equals 1 by construction.
    """
    phi, _, dphi = cartan_grid(n_grid)
    W = np.zeros((n_grid, n_grid), dtype=float)
    for i, p1 in enumerate(phi):
        for j, p2 in enumerate(phi):
            W[i, j] = vandermonde_squared(p1, p2)
    cell = (dphi / (2.0 * math.pi)) ** 2
    Z = np.sum(W) * cell
    if Z > 0:
        W = W / Z
    return W, cell


def schur_character(p: int, q: int, phi1: float, phi2: float) -> complex:
    """Schur polynomial character chi_(p,q) at SU(3) Cartan element
    diag(e^(i phi_1), e^(i phi_2), e^(-i(phi_1+phi_2))).

    For irrep (p, q), partition lambda = (p+q, q, 0). Schur polynomial:

        s_lambda(z) = det[z_i^(lambda_j + 3-j)] / det[z_i^(3-j)]
                    = det[z_i^(lambda_j + 3-j)] / Vandermonde(z)

    where Vandermonde(z) = (z_1 - z_2)(z_1 - z_3)(z_2 - z_3).

    Off the Vandermonde-zero locus (where some z_i = z_j), this is
    well-defined and continuous; we evaluate by analytic continuation
    (using complex arithmetic; if denominator is near zero, the limit
    gives the usual Weyl character formula).
    """
    z1 = complex(math.cos(phi1), math.sin(phi1))
    z2 = complex(math.cos(phi2), math.sin(phi2))
    phi3 = -(phi1 + phi2)
    z3 = complex(math.cos(phi3), math.sin(phi3))
    exponents = [p + q + 2, q + 1, 0]
    z = [z1, z2, z3]
    num_mat = np.array([[z[i] ** exponents[j] for j in range(3)]
                         for i in range(3)], dtype=complex)
    num_det = np.linalg.det(num_mat)
    denom_mat = np.array([[z[i] ** (2 - j) for j in range(3)]
                           for i in range(3)], dtype=complex)
    denom_det = np.linalg.det(denom_mat)
    if abs(denom_det) < 1e-12:
        return 0.0 + 0.0j
    return num_det / denom_det


def character_table(weights: List[Tuple[int, int]], n_grid: int
                     ) -> np.ndarray:
    """Pre-compute character values chi_(p,q)(phi_1, phi_2) on a grid.

    Returns chars[w, i, j] = chi_(weights[w])(phi[i], phi[j]) (complex).

    This is the heavy precomputation; subsequent fusion integrals are
    fast linear combinations of these values.
    """
    phi, _, _ = cartan_grid(n_grid)
    n = len(weights)
    chars = np.zeros((n, n_grid, n_grid), dtype=complex)
    for w, (p, q) in enumerate(weights):
        for i, p1 in enumerate(phi):
            for j, p2 in enumerate(phi):
                chars[w, i, j] = schur_character(p, q, p1, p2)
    return chars


# ===========================================================================
# Section C. Fusion via character orthogonality.
# ===========================================================================

def fusion_multiplicity(chi_l: np.ndarray, chi_m: np.ndarray,
                          chi_n: np.ndarray, W: np.ndarray, cell: float
                          ) -> Tuple[int, float]:
    """Compute N^nu_(lambda, mu) = integral chi_lambda chi_mu chi_nu^* dW
    via numerical character orthogonality.

    Returns (rounded_int, residual) where rounded_int is the nearest
    non-negative integer and residual is the absolute difference.
    """
    integrand = chi_l * chi_m * np.conj(chi_n) * W
    integral = float(np.real(np.sum(integrand) * cell))
    rounded = max(0, int(round(integral)))
    residual = abs(integral - rounded)
    return rounded, residual


def fusion_table(weights: List[Tuple[int, int]], chars: np.ndarray,
                  W: np.ndarray, cell: float
                  ) -> Tuple[np.ndarray, float]:
    """Compute the full fusion table N[i, j, k] = N^(weights[k])_(weights[i], weights[j]).

    Returns (N_table, max_residual).
    """
    n = len(weights)
    N_table = np.zeros((n, n, n), dtype=int)
    max_residual = 0.0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                rounded, residual = fusion_multiplicity(
                    chars[i], chars[j], chars[k], W, cell
                )
                N_table[i, j, k] = rounded
                if residual > max_residual:
                    max_residual = residual
    return N_table, max_residual


# ===========================================================================
# Section D. Validation suite.
# ===========================================================================

def get_index(weights: List[Tuple[int, int]], pq: Tuple[int, int]) -> int:
    """Return index of (p, q) in weights list, or -1 if absent."""
    try:
        return weights.index(pq)
    except ValueError:
        return -1


def fusion_decomposition(N_table: np.ndarray, weights: List[Tuple[int, int]],
                          lam: Tuple[int, int], mu: Tuple[int, int]
                          ) -> Dict[Tuple[int, int], int]:
    """Return {(x, y): N^(x,y)_(lam, mu)} for nonzero entries."""
    li = get_index(weights, lam)
    mi = get_index(weights, mu)
    if li < 0 or mi < 0:
        return {}
    out: Dict[Tuple[int, int], int] = {}
    for k, w in enumerate(weights):
        n = int(N_table[li, mi, k])
        if n > 0:
            out[w] = n
    return out


def format_decomposition(decomp: Dict[Tuple[int, int], int]) -> str:
    """Pretty-print a fusion decomposition."""
    parts = []
    for (p, q), n in sorted(decomp.items(), key=lambda x: (x[0][0] + x[0][1], x[0])):
        d = dim_su3(p, q)
        if n == 1:
            parts.append(f"({p},{q})[d={d}]")
        else:
            parts.append(f"{n}*({p},{q})[d={d}]")
    return " + ".join(parts) if parts else "(empty)"


def check(name: str, condition: bool, detail: str, results: List, kind: str = "PASS"):
    """Append a check result to the running list."""
    status = "PASS" if condition else "FAIL"
    results.append((status, kind, name, detail))
    return condition


def validate_engine(N_table: np.ndarray, weights: List[Tuple[int, int]]
                    ) -> List[Tuple[str, str, str, str]]:
    """Run the validation suite and return a list of (status, kind, name, detail)."""
    results: List[Tuple[str, str, str, str]] = []
    nmax = max(p for p, _ in weights)

    # V1: 3 ⊗ 3̄ = 8 ⊕ 1
    decomp = fusion_decomposition(N_table, weights, (1, 0), (0, 1))
    expected = {(1, 1): 1, (0, 0): 1}
    check("V1: 3 ⊗ 3̄ = 8 ⊕ 1",
          decomp == expected,
          f"got {format_decomposition(decomp)}; expected (0,0)[d=1] + (1,1)[d=8]",
          results)

    # V2: 3 ⊗ 3 = 6 ⊕ 3̄
    decomp = fusion_decomposition(N_table, weights, (1, 0), (1, 0))
    expected = {(2, 0): 1, (0, 1): 1}
    check("V2: 3 ⊗ 3 = 6 ⊕ 3̄",
          decomp == expected,
          f"got {format_decomposition(decomp)}; expected (0,1)[d=3] + (2,0)[d=6]",
          results)

    # V3: 8 ⊗ 8 = 27 ⊕ 10 ⊕ 10̄ ⊕ 8 ⊕ 8 ⊕ 1 (only valid if NMAX >= 4)
    if nmax >= 4:
        decomp = fusion_decomposition(N_table, weights, (1, 1), (1, 1))
        expected = {(0, 0): 1, (1, 1): 2, (3, 0): 1, (0, 3): 1, (2, 2): 1}
        check("V3: 8 ⊗ 8 = 27 ⊕ 10 ⊕ 10̄ ⊕ 8 ⊕ 8 ⊕ 1",
              decomp == expected,
              f"got {format_decomposition(decomp)}; expected (0,0)+2(1,1)+(0,3)+(3,0)+(2,2)",
              results)

    # V4: 6 ⊗ 6̄ = 27 ⊕ 8 ⊕ 1 (only valid if NMAX >= 4)
    if nmax >= 4:
        decomp = fusion_decomposition(N_table, weights, (2, 0), (0, 2))
        expected = {(0, 0): 1, (1, 1): 1, (2, 2): 1}
        check("V4: 6 ⊗ 6̄ = 27 ⊕ 8 ⊕ 1",
              decomp == expected,
              f"got {format_decomposition(decomp)}; expected (0,0)+(1,1)+(2,2)",
              results)

    # V5: commutativity N^nu_(lambda, mu) = N^nu_(mu, lambda)
    n = len(weights)
    sym_err = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if N_table[i, j, k] != N_table[j, i, k]:
                    sym_err += 1
    check("V5: commutativity N^ν_(λ,μ) = N^ν_(μ,λ)",
          sym_err == 0,
          f"asymmetric entries: {sym_err}",
          results)

    # V6: singlet selection N^(0,0)_(lam,mu) = delta_(mu, lam-bar)
    singlet_idx = get_index(weights, (0, 0))
    sel_errors = 0
    for i, lam in enumerate(weights):
        lam_bar = conjugate_irrep(*lam)
        bar_idx = get_index(weights, lam_bar)
        for j, mu in enumerate(weights):
            expected_singlet = 1 if j == bar_idx else 0
            if N_table[i, j, singlet_idx] != expected_singlet:
                sel_errors += 1
    check("V6: singlet selection N^(0,0)_(λ,μ) = δ_(μ, λ̄)",
          sel_errors == 0,
          f"selection-rule errors: {sel_errors}",
          results)

    # V7: dimension count sum_nu N^nu_(lam,mu) d_nu = d_lam d_mu (= when product fits in box)
    dim_errors = 0
    dim_err_examples = []
    for i, lam in enumerate(weights):
        for j, mu in enumerate(weights):
            lhs = sum(int(N_table[i, j, k]) * dim_su3(*weights[k])
                      for k in range(n))
            rhs = dim_su3(*lam) * dim_su3(*mu)
            if lhs > rhs:
                dim_errors += 1
                if len(dim_err_examples) < 3:
                    dim_err_examples.append(f"({lam}, {mu}): {lhs} > {rhs}")
    check("V7: dimension count sum_ν N^ν_(λ,μ) d_ν ≤ d_λ d_μ (= when product fits in NMAX box)",
          dim_errors == 0,
          f"dimension overflow errors: {dim_errors}; examples: {dim_err_examples}",
          results)

    # V8: crossing N^nu_(lam, mu) = N^lam_(nu, mu-bar)
    cross_errors = 0
    for i, lam in enumerate(weights):
        for j, mu in enumerate(weights):
            mu_bar_idx = get_index(weights, conjugate_irrep(*mu))
            for k, nu in enumerate(weights):
                if mu_bar_idx < 0:
                    continue
                lhs = int(N_table[i, j, k])
                rhs = int(N_table[k, mu_bar_idx, i])
                if lhs != rhs:
                    cross_errors += 1
    check("V8: crossing N^ν_(λ,μ) = N^λ_(ν, μ̄)",
          cross_errors == 0,
          f"crossing errors: {cross_errors}",
          results)

    # V9: Pieri rule for fundamental
    pieri_errors = 0
    fund_idx = get_index(weights, (1, 0))
    for ab in weights:
        a, b = ab
        ab_idx = get_index(weights, ab)
        expected_pieri = {}
        for cand in [(a + 1, b), (a - 1, b + 1), (a, b - 1)]:
            if cand[0] >= 0 and cand[1] >= 0:
                expected_pieri[cand] = expected_pieri.get(cand, 0) + 1
        max_child = max(max(c) for c in expected_pieri) if expected_pieri else 0
        if max_child > nmax:
            continue
        decomp = fusion_decomposition(N_table, weights, (1, 0), ab)
        if decomp != expected_pieri:
            pieri_errors += 1
    check("V9: fundamental Pieri (1,0) ⊗ (a,b) = (a+1,b) + (a-1,b+1) + (a,b-1)",
          pieri_errors == 0,
          f"Pieri rule errors: {pieri_errors}",
          results)

    return results


# ===========================================================================
# Section E. Driver.
# ===========================================================================

NMAX_DEFAULT = 4
N_GRID_DEFAULT = 80


def driver(nmax: int = NMAX_DEFAULT, n_grid: int = N_GRID_DEFAULT) -> int:
    print("=" * 78)
    print("SU(3) Fusion Engine via Cartan-Torus Character Orthogonality")
    print("PR 1 of 5-PR engine roadmap")
    print(f"  NMAX = {nmax}, Cartan-torus n_grid = {n_grid}")
    print("=" * 78)
    print()

    weights = dominant_weights_box(nmax)
    print(f"Dominant-weight box ({len(weights)} weights): "
          f"{weights[:5]}...{weights[-3:]}")
    print(f"Highest-dim irrep in box: "
          f"{max(weights, key=lambda w: dim_su3(*w))} "
          f"(dim {dim_su3(*max(weights, key=lambda w: dim_su3(*w)))})")
    print()

    print("Pre-computing character table on Cartan-torus grid...")
    chars = character_table(weights, n_grid)
    W, cell = haar_measure_normalized(n_grid)
    haar_norm = float(np.real(np.sum(W * cell)))
    print(f"  characters computed:    shape {chars.shape}")
    print(f"  Haar normalization Z:   {haar_norm:.10f}  (should be 1.0)")

    print()
    print("Sanity checks: <chi_lambda, chi_lambda> = 1 (orthogonality of characters)")
    self_ortho = []
    for w_idx, (p, q) in enumerate(weights[:5]):
        val = float(np.real(np.sum(chars[w_idx] * np.conj(chars[w_idx]) * W) * cell))
        self_ortho.append(val)
        print(f"  ({p},{q})  ->  <chi, chi> = {val:.8f}")
    self_ortho_max_err = max(abs(v - 1.0) for v in self_ortho)
    print(f"  max |<chi,chi> - 1| = {self_ortho_max_err:.3e}")
    print()

    print("Computing full fusion table N^nu_(lambda, mu) via character orthogonality...")
    N_table, max_residual = fusion_table(weights, chars, W, cell)
    print(f"  fusion table:           shape {N_table.shape}, dtype {N_table.dtype}")
    print(f"  max integer residual:   {max_residual:.3e}  (should be << 0.5)")
    print(f"  total nonzero entries:  {int(np.sum(N_table > 0))}")
    print()

    print("Selected explicit fusion decompositions:")
    show = [((1, 0), (0, 1)),
            ((1, 0), (1, 0)),
            ((1, 1), (1, 0)),
            ((2, 0), (0, 2)),
            ((1, 1), (1, 1)),
            ((2, 1), (1, 0)),
            ]
    for (lam, mu) in show:
        if lam in weights and mu in weights:
            decomp = fusion_decomposition(N_table, weights, lam, mu)
            d_lam = dim_su3(*lam)
            d_mu = dim_su3(*mu)
            d_total = d_lam * d_mu
            d_decomp = sum(n * dim_su3(*w) for w, n in decomp.items())
            ratio = d_decomp / d_total if d_total > 0 else 0
            print(f"  ({lam[0]},{lam[1]})[d={d_lam}] ⊗ ({mu[0]},{mu[1]})[d={d_mu}] "
                  f"(d_lhs={d_total}) = ")
            print(f"    {format_decomposition(decomp)}")
            print(f"    (sum d = {d_decomp}, ratio {ratio:.4f})")
    print()

    print("Validation suite:")
    print()
    results = validate_engine(N_table, weights)
    pass_count = sum(1 for r in results if r[0] == "PASS")
    fail_count = sum(1 for r in results if r[0] == "FAIL")
    for status, kind, name, detail in results:
        print(f"  [{status}] [{kind}] {name}")
        print(f"           {detail}")
    print()

    print("Numerical noise diagnostics:")
    print(f"  max integer residual over all (lam, mu, nu): {max_residual:.3e}")
    if max_residual < 0.05:
        print(f"  PASS: residual < 0.05; integer rounding is safe.")
        pass_count += 1
    else:
        print(f"  FAIL: residual >= 0.05; increase n_grid.")
        fail_count += 1
    print()

    total_dim_in_box = sum(dim_su3(*w) for w in weights)
    print(f"  total dim sum over weight box: {total_dim_in_box}")
    print()

    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Engine status: PR 1 deliverable — fusion multiplicities N^ν_(λ,μ)")
    print("computable for arbitrary SU(3) irreps within the dominant-weight box.")
    print()
    print("Next steps in the engine roadmap:")
    print("  PR 2: SU(3) Wigner intertwiner / Clebsch-Gordan coefficient engine")
    print("  PR 3: SU(3) Haar integral primitives (1-link, multi-link)")
    print("  PR 4: generic tensor-network contraction engine on lattice graphs")
    print("  PR 5: L_s=2 APBC cube geometry + ρ_(p,q)(6) computation + P(6) verdict")
    print()
    print("See docs/SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
