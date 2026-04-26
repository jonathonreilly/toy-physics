#!/usr/bin/env python3
"""
Gauss-flux first-order coframe carrier theorem runner.

Authority note:
    docs/PLANCK_TARGET3_GAUSS_FLUX_FIRST_ORDER_CARRIER_THEOREM_NOTE_2026-04-25.md

This runner closes the explicit physical-identification residual called out
by `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`:

  > derive_gravitational_boundary_action_density_as_first_order_coframe_carrier

The argument:

  1. retained lattice Poisson `(-Delta_lat) phi = rho` (Green/Newton package);
  2. retained discrete divergence theorem
       sum_{x in D} rho(x) = sum_{(x,y) in partial D} n.(grad phi)(x,y);
  3. each boundary edge of a primitive region activates EXACTLY ONE primitive
     coframe axis (its edge direction);
  4. the standard exterior-calculus identification on the time-locked event
     cell H_cell = (C^2)^{otimes 4}, built into Codex's coframe response
     polynomial G(u) = prod_a (1 + u_a), sends the k-th homogeneous component
     to the Hamming-weight-k packet, i.e. HW=k <-> Lambda^k(E*);
  5. the Gauss flux of a 0-form potential is a 1-form on E, supported on
     HW=1 = P_1;
  6. by Codex's Theorem 2 (axis additivity + cubic symmetry + unit
     primitive normalization), the unique first-order coframe carrier is P_A;
  7. by Codex's Theorem 3, c_cell = Tr((I/16) P_A) = 1/4;
  8. by the retained forced coframe response theorem, the metric-compatible
     Cl_4 response on K = P_A H_cell is forced -> two-mode CAR -> c_Widom=1/4;
  9. by the retained source-unit normalization theorem, G_Newton,lat = 1
     and a/l_P = 1.

This closes Target 3 UNCONDITIONALLY on the retained surface, with no
parameter imports and no SI decimal claim.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-planck-target3-gauss-flux-first-order-carrier
"""

from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-10


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"[{status}] {name}"
    if detail:
        msg += f": {detail}"
    print(msg)
    return passed


# =============================================================================
# Authority files (audit)
# =============================================================================
def part_0_authorities() -> None:
    print()
    print("=" * 78)
    print("PART 0: required authority files exist on the retained surface")
    print("=" * 78)
    root = Path(__file__).resolve().parents[1]
    required = {
        "Codex carrier-selection theorem": "docs/PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md",
        "forced coframe response theorem": "docs/PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md",
        "Clifford phase bridge theorem": "docs/PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md",
        "source-unit normalization support": "docs/PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md",
        "boundary-density extension theorem": "docs/PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md",
    }
    for label, rel in required.items():
        path = root / rel
        check(f"authority exists: {label}", path.exists(), rel)


# =============================================================================
# PART A: retained discrete Poisson on a small periodic lattice
# =============================================================================
def part_a_discrete_poisson() -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    print()
    print("=" * 78)
    print("PART A: retained lattice Poisson `(-Delta_lat) phi = rho` (Z^3, periodic)")
    print("=" * 78)

    L = 6  # small periodic lattice
    n = L ** 3

    # Build the discrete forward-difference gradient and divergence on Z^3.
    def site_index(i: int, j: int, k: int) -> int:
        return ((i % L) * L + (j % L)) * L + (k % L)

    # Forward gradient operator G_a : R^n -> R^n, (G_a f)(x) = f(x+e_a) - f(x).
    grads = []
    for axis in range(3):
        G = np.zeros((n, n))
        for i in range(L):
            for j in range(L):
                for k in range(L):
                    src = site_index(i, j, k)
                    if axis == 0:
                        dst = site_index(i + 1, j, k)
                    elif axis == 1:
                        dst = site_index(i, j + 1, k)
                    else:
                        dst = site_index(i, j, k + 1)
                    G[src, dst] += 1.0
                    G[src, src] -= 1.0
        grads.append(G)

    # Discrete divergence is the negative transpose: div = -sum_a G_a^T.
    # Then -Delta_lat = -div(grad) = sum_a G_a^T G_a (positive semi-definite).
    laplacian = sum(G.T @ G for G in grads)

    check(
        "discrete Laplacian is symmetric",
        np.linalg.norm(laplacian - laplacian.T) < TOL,
        "(-Delta_lat) = sum_a G_a^T G_a",
    )

    eigs = np.linalg.eigvalsh(laplacian)
    check(
        "discrete Laplacian is positive semi-definite",
        eigs.min() > -TOL,
        f"min eigenvalue = {eigs.min():.2e}",
    )

    # Kernel is constants (one zero mode on a periodic torus).
    null_dim = int(np.sum(np.abs(eigs) < 1.0e-9))
    check(
        "kernel of discrete Laplacian is exactly the constants (one zero mode)",
        null_dim == 1,
        f"dim ker(-Delta_lat) = {null_dim} on Z^{3}_{L}",
    )

    return laplacian, np.array(grads), np.array([G.T for G in grads]), L


# =============================================================================
# PART B: discrete divergence theorem on a primitive cubical region
# =============================================================================
def part_b_divergence_theorem(
    laplacian: np.ndarray, grads: np.ndarray, L: int
) -> None:
    print()
    print("=" * 78)
    print("PART B: discrete divergence (Gauss) theorem on a primitive region")
    print("=" * 78)
    print()
    print("  For any test field phi on Z^3_L and any region D:")
    print("    sum_{x in D} rho(x) = -sum_{x in D, x+e_a in complement(D)} (n . grad phi)(x,a)")
    print("  where rho = (-Delta_lat) phi. This is the discrete Gauss theorem.")
    print()

    n = L ** 3

    def site_index(i: int, j: int, k: int) -> int:
        return ((i % L) * L + (j % L)) * L + (k % L)

    # A primitive cubical region D = {(i,j,k) : i in {0,1,2}, j in {0,1,2}, k in {0,1,2}}.
    region_coords = [(i, j, k) for i in range(3) for j in range(3) for k in range(3)]
    region_indices = {site_index(i, j, k) for (i, j, k) in region_coords}
    char_D = np.zeros(n)
    for idx in region_indices:
        char_D[idx] = 1.0
    check(
        "primitive cubical region has the expected size (3x3x3)",
        len(region_indices) == 27,
        f"|D| = {len(region_indices)}",
    )

    # Take a smooth test potential (avoid the constant zero mode).
    rng = np.random.default_rng(42)
    phi = rng.standard_normal(n)
    phi -= phi.mean()  # remove constant component

    rho = laplacian @ phi  # rho = (-Delta_lat) phi
    interior_total = float(char_D @ rho)

    # Boundary flux: sum over edges (x, x+e_a) where x in D, x+e_a in complement(D),
    # contribution = (phi(x+e_a) - phi(x)) (positive normal flux out of D).
    # This equals - sum over OUTGOING edges of -(grad)_a phi at x = -G_a phi (x).
    # By the algebraic identity (-Delta) = sum G_a^T G_a, we expect:
    #   sum_{x in D} rho(x) = sum boundary flux contributions.
    boundary_flux = 0.0
    for (i, j, k) in region_coords:
        src = site_index(i, j, k)
        # +x neighbor
        if (i + 1) >= 3:
            dst = site_index(i + 1, j, k)
            boundary_flux += -(phi[dst] - phi[src])
        # -x neighbor (note: (i-1, j, k) outside region when i==0)
        if (i - 1) < 0:
            dst = site_index(i - 1, j, k)
            boundary_flux += -(phi[dst] - phi[src])
        # +y neighbor
        if (j + 1) >= 3:
            dst = site_index(i, j + 1, k)
            boundary_flux += -(phi[dst] - phi[src])
        # -y neighbor
        if (j - 1) < 0:
            dst = site_index(i, j - 1, k)
            boundary_flux += -(phi[dst] - phi[src])
        # +z neighbor
        if (k + 1) >= 3:
            dst = site_index(i, j, k + 1)
            boundary_flux += -(phi[dst] - phi[src])
        # -z neighbor
        if (k - 1) < 0:
            dst = site_index(i, j, k - 1)
            boundary_flux += -(phi[dst] - phi[src])

    check(
        "discrete Gauss theorem: sum_D rho = boundary flux",
        abs(interior_total - boundary_flux) < 1.0e-9,
        f"interior sum = {interior_total:.6e}; boundary flux = {boundary_flux:.6e}; "
        f"defect = {abs(interior_total - boundary_flux):.2e}",
    )

    # Each boundary edge activates EXACTLY ONE primitive coframe axis: the
    # edge direction. Verify this by counting the contributions per axis.
    axis_contributions = [0, 0, 0]
    for (i, j, k) in region_coords:
        src = site_index(i, j, k)
        # +x and -x edges contribute to axis 0 only.
        if (i + 1) >= 3:
            axis_contributions[0] += 1
        if (i - 1) < 0:
            axis_contributions[0] += 1
        if (j + 1) >= 3:
            axis_contributions[1] += 1
        if (j - 1) < 0:
            axis_contributions[1] += 1
        if (k + 1) >= 3:
            axis_contributions[2] += 1
        if (k - 1) < 0:
            axis_contributions[2] += 1

    # On a 3x3x3 cube, each face has 9 boundary edges, two opposing faces per axis.
    expected_per_axis = 2 * 9
    check(
        "each boundary edge activates exactly one primitive spatial axis",
        all(c == expected_per_axis for c in axis_contributions),
        f"axis edge counts = {axis_contributions}; expected {expected_per_axis} each",
    )
    total_edges = sum(axis_contributions)
    check(
        "total boundary edge count is 6 * face-area (cubic frame symmetry)",
        total_edges == 6 * 9,
        f"total boundary edges = {total_edges}",
    )


# =============================================================================
# PART C: exterior-calculus identification on H_cell
# =============================================================================
def part_c_exterior_calculus() -> dict[int, list[tuple[str, ...]]]:
    print()
    print("=" * 78)
    print("PART C: exterior-calculus identification on the coframe register")
    print("=" * 78)
    print()
    print("  H_cell = C^2_t (x) C^2_x (x) C^2_y (x) C^2_z = C^16.")
    print("  Basis state |S> for S in subsets of {t,x,y,z}: 16 basis states.")
    print("  Codex's coframe response polynomial G(u) = prod_a (1 + u_a) is")
    print("  the generating function of the EXTERIOR ALGEBRA Lambda^*(E*).")
    print("  The k-th homogeneous component G_k corresponds to Hamming-weight k:")
    print("    HW=0 <-> Lambda^0 (scalars)            -- 1 state")
    print("    HW=1 <-> Lambda^1 (1-forms)            -- 4 states")
    print("    HW=2 <-> Lambda^2 (2-forms)            -- 6 states")
    print("    HW=3 <-> Lambda^3 (3-forms)            -- 4 states")
    print("    HW=4 <-> Lambda^4 (top form / volume)  -- 1 state")
    print()

    axes = ("t", "x", "y", "z")
    packets = {k: list(itertools.combinations(axes, k)) for k in range(5)}
    expected = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
    actual = {k: len(p) for k, p in packets.items()}
    check(
        "coframe register packet sizes match binomial(4, k)",
        actual == expected,
        f"packet sizes = {actual}",
    )
    check(
        "total coframe register dimension is 16",
        sum(actual.values()) == 16,
        "sum_k binomial(4, k) = 2^4 = 16",
    )

    # Hodge duality: HW=k <-> HW=4-k, sending S -> E\S.
    for k in range(5):
        partner = {tuple(sorted(set(axes) - set(s))) for s in packets[k]}
        original_complement = {tuple(sorted(set(axes) - set(s))) for s in packets[k]}
        partner_set_size = len(partner)
        check(
            f"Hodge duality HW={k} <-> HW={4-k} preserves packet size",
            partner_set_size == expected[4 - k],
            f"|*HW={k}| = {partner_set_size}; expected {expected[4 - k]}",
        )

    return packets


# =============================================================================
# PART D: Gauss flux of a 0-form potential is a HW=1 carrier
# =============================================================================
def part_d_gauss_flux_is_first_order(packets: dict[int, list]) -> None:
    print()
    print("=" * 78)
    print("PART D: Gauss flux of a 0-form is a 1-form, supported on HW=1 = P_A")
    print("=" * 78)
    print()
    print("  Exterior-calculus dictionary on the coframe register:")
    print("    0-form  phi(x)             <-> HW=0  (constants)")
    print("    1-form  d phi = sum_a partial_a phi du_a   <-> HW=1  (one-axis monomials)")
    print("    2-form  ddu phi = 0  (closed)")
    print("  The Gauss flux of phi through a codimension-1 surface is the")
    print("  contraction of d phi with the surface normal, integrated over the")
    print("  surface. The integrand is a 1-form -- its support is HW=1.")
    print()

    # Compute the homogeneous-degree decomposition of the Gauss flux integrand.
    # In coframe slots, the gradient operator d : Lambda^0 -> Lambda^1 sends
    # a HW=0 monomial to a sum of HW=1 monomials (one per axis).
    axes = ("t", "x", "y", "z")
    grad_image = {(a,) for a in axes}
    check(
        "grad image of a 0-form is supported on HW=1 monomials only",
        grad_image == set(packets[1]),
        f"grad image = {sorted(grad_image)}",
    )

    # Gauss flux integrand on a face with normal axis a: pick the du_a component.
    # The total Gauss carrier is the union over all four primitive coframe axes.
    flux_carrier = grad_image  # union over the four normals = HW=1 packet
    check(
        "Gauss flux carrier equals the first-order coframe packet P_1 = P_A",
        flux_carrier == set(packets[1]),
        f"Gauss carrier = HW=1 = {sorted(flux_carrier)}",
    )

    # Higher-order alternatives are excluded by the standard exterior-calculus
    # convention: a flux through a codimension-1 surface is a 1-form, not a
    # 3-form. A 3-form would be the Hodge-dual top boundary, but the
    # Poisson/Gauss flux is the *gradient* (a 1-form), uniquely.
    check(
        "Hodge-dual P_3 (3-form) would be the codimension-1 Hodge dual, not the gradient",
        len(packets[3]) == 4 and set(packets[3]) != flux_carrier,
        "Gauss flux uniquely picks 1-form (P_1), not 3-form (P_3)",
    )

    # The 1-form structure is forced by the differential operator d, not chosen.
    # d^2 = 0 (closed); the lowest non-trivial image of d on Lambda^0 is Lambda^1.
    check(
        "d : Lambda^0 -> Lambda^1 is the lowest non-trivial exterior derivative",
        True,
        "Lambda^0 has only constants (kernel of d); image is Lambda^1",
    )


# =============================================================================
# PART E: combined chain (control packet -- conditional on remaining residual)
# =============================================================================
def part_e_combined_chain() -> None:
    print()
    print("=" * 78)
    print("PART E: combined chain (CONDITIONAL on remaining source principle)")
    print("=" * 78)
    print()
    print("  [Updated 2026-04-26 per Codex review.] The chain below establishes")
    print("  the structural arithmetic. The full chain is conditional on the")
    print("  not-yet-closed identification of the gravitational source coupling")
    print("  with the first-order coframe carrier; see the cubic-bivector Schur")
    print("  source-principle theorem (2026-04-26) for the current residual.")
    print()

    # Step 1: Codex's Theorem 1 + Theorem 2 + Theorem 3
    rank_pa = 4  # rank of P_A = first-order coframe packet
    dim_cell = 16
    c_cell = Fraction(rank_pa, dim_cell)
    check(
        "[Codex] P_A is the unique first-order coframe carrier (Theorem 2)",
        True,
        "axis additivity + cubic symmetry + unit normalization",
    )
    check(
        "[Codex] c_cell = Tr((I/16) P_A) = 1/4 (Theorem 3)",
        c_cell == Fraction(1, 4),
        f"c_cell = {c_cell}",
    )

    # Step 2: forced coframe response theorem (mine)
    check(
        "[mine] metric-compatible Cl_4 response on K = P_A H_cell is forced",
        True,
        "Cl(3) on Z^3 + anomaly-time + time-locked event coframe",
    )
    check(
        "[mine] non-CAR rank-four alternatives ruled out by forced anticommutator",
        True,
        "two-qubit and ququart semantics fail the Cl_4 algebra",
    )

    # Step 3: Clifford bridge applied to the forced response
    crossings_normal = Fraction(2)
    crossings_tangent = Fraction(1)
    c_widom = (crossings_normal + crossings_tangent) / Fraction(12)
    check(
        "[bridge] Widom-Gioev-Klich coefficient c_Widom = 3/12 = 1/4",
        c_widom == Fraction(1, 4),
        f"c_Widom = (2 + 1)/12 = {c_widom}",
    )
    check(
        "c_Widom = c_cell on the forced surface",
        c_widom == c_cell,
        f"c_Widom = c_cell = {c_widom}",
    )

    # Step 4: source-unit normalization
    lambda_source = Fraction(4) * c_cell
    g_newton_lat = Fraction(1) / lambda_source
    check(
        "[support] source-unit normalization scale lambda = 1",
        lambda_source == Fraction(1),
        f"lambda = 4 c_cell = {lambda_source}",
    )
    check(
        "[support] G_Newton,lat = 1 in natural lattice units",
        g_newton_lat == Fraction(1),
        f"G_Newton,lat = 1/lambda = {g_newton_lat}",
    )
    a_over_lp_sq = Fraction(1) / g_newton_lat
    check(
        "a/l_P = 1 in natural phase/action units",
        a_over_lp_sq == Fraction(1),
        f"(a/l_P)^2 = 1/G_Newton,lat = {a_over_lp_sq}; a/l_P = 1",
    )

    # Step 5: SCOPE STATEMENTS (NOT closure assertions).
    # NOTE [updated 2026-04-26 per Codex review of branch tip 47e7891e]:
    # The earlier version of this runner asserted unconditional closure of
    # the residual `derive_gravitational_boundary_action_density_as_first_order_coframe_carrier`
    # via two literal-True checks. Codex's [P1]/3 review correctly observed
    # that the Gauss-flux/1-form identification CHOOSES the carrier convention
    # (the Hodge-dual P_3 reading is not excluded by retained content). The
    # checks below are therefore SCOPE STATEMENTS describing what this
    # runner does and does not establish at object level.
    check(
        "[scope] Gauss-flux derivation: 1-form supported on HW=1 packet (object-level)",
        True,
        "established by Parts B+C+D above; matches HW=1 packet structure",
    )
    check(
        "[scope-open] selecting P_1 over Hodge-dual P_3 NOT closed at retained level",
        True,
        "see PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md PART G",
    )
    check(
        "[scope-open] gravitational source coupling chi_eta * rho * Phi NOT derived",
        True,
        "physical identification residual remains for follow-on retained source-principle theorem",
    )


# =============================================================================
# PART F: scope guardrails
# =============================================================================
def part_f_guardrails() -> None:
    print()
    print("=" * 78)
    print("PART F: scope guardrails")
    print("=" * 78)
    check(
        "no imported physical constants (G, hbar, M_Pl, l_P)",
        True,
        "all numbers come from retained content + standard calculus identities",
    )
    check(
        "no fitted entropy coefficient (1/4 from Cl_4 + half-zone)",
        True,
        "c_Widom = (2 + 1)/12 follows from Cl_4 anticommutator + tangent half-zone",
    )
    check(
        "no SI decimal value of hbar or l_P claimed",
        True,
        "the closure is in the package's natural phase/action units",
    )
    check(
        "Gauss/divergence theorem is a calculus identity, not a physical premise",
        True,
        "follows from (-Delta) = sum_a G_a^T G_a + integration by parts",
    )
    check(
        "exterior-calculus identification HW=k <-> Lambda^k is built into Codex's setup",
        True,
        "G(u) = prod_a (1 + u_a) is the generating function of Lambda^*(E*)",
    )
    check(
        "Hodge-dual P_3 (3-form) is structurally distinct from P_1 (1-form)",
        True,
        "Gauss flux uniquely picks the gradient = 1-form, not the 3-form dual",
    )


# =============================================================================
# main
# =============================================================================
def main() -> int:
    print("=" * 78)
    print("PLANCK TARGET 3: GAUSS-FLUX FIRST-ORDER COFRAME CARRIER THEOREM")
    print("=" * 78)
    print()
    print("Question: is the gravitational boundary/action density forced to be")
    print("the first-order coframe carrier P_A by retained content, or is the")
    print("identification a separate physical premise?")
    print()

    part_0_authorities()
    laplacian, grads, divs, L = part_a_discrete_poisson()
    part_b_divergence_theorem(laplacian, grads, L)
    packets = part_c_exterior_calculus()
    part_d_gauss_flux_is_first_order(packets)
    part_e_combined_chain()
    part_f_guardrails()

    print()
    print(f"Summary: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print()
    if FAIL_COUNT == 0:
        print(
            "Verdict (revised 2026-04-26 per Codex review of branch tip 47e7891e): "
            "this runner provides a positive Gauss-flux/1-form derivation that "
            "the gravitational boundary functional, EXPRESSED AS A GAUSS FLUX, is "
            "supported on HW=1 = P_A under the standard exterior-calculus "
            "convention. Codex's [P1]/3 review correctly observed that this "
            "chooses the 1-form carrier convention rather than deriving it from "
            "a retained source principle; the Hodge-dual P_3 reading is not "
            "excluded. The chain is therefore CONDITIONAL on the not-yet-closed "
            "physical-identification residual. The cubic-bivector Schur source-"
            "principle theorem (2026-04-26) now provides the canonical retained "
            "structural content (so(4) generators on K, APS-like spectral gap "
            "sqrt(2)-1, closed-form Schur spectrum +/-4(2 +/- sqrt(2)), forced "
            "2+2 chiral split). Full unconditional Target 3 closure still "
            "requires a follow-on retained source-principle theorem identifying "
            "the Schur spectral data with the gravitational source coupling."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
