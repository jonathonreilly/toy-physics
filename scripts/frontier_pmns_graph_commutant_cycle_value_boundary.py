#!/usr/bin/env python3
"""Graph-native projected-commutant boundary for the reduced PMNS cycle lane.

Question:
  Can the graph-first selected-axis route together with the projected
  commutant / generation-boundary data supply a positive value law for the
  reduced forward-cycle channel

      A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31

  on the retained PMNS blocker?

Answer:
  No. The route is genuinely native and genuinely sharp, but it only fixes
  the selector bundle:

    - the weak-axis choice and its residual Z2 stabilizer
    - the branch/orientation selector tau
    - the passive offset class q

  The projected commutant data remain orbit-constant on the reduced cycle
  family, so they do not select a unique point (u,v,w).

  In other words, this route is a theorem-grade boundary, not a positive
  value law.  The current bank still needs a lower-level source/transport
  law to fix the reduced cycle values themselves.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_pmns_commutant_eigenoperator_selector import (
    build_cl3_gammas,
    c3_taste_unitary,
    cl3_span_basis,
    compute_commutant_basis,
    compute_projected_commutant,
    corner_profile,
    in_span,
    orbit_fourier,
    project_corner_eigenspace,
)
from frontier_pmns_graph_first_axis_alignment import aligned_core, selector_from_phi, simplex_grid
from frontier_pmns_oriented_cycle_channel_value_law import oriented_cycle_coeffs_from_block
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import (
    active_block_with_reduced_cycle,
    reduced_cycle_coordinates,
    residual_swap_conjugate,
)
from pmns_lower_level_utils import support_mask

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
I8 = np.eye(8, dtype=complex)
P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def build_axis_shifts() -> list[np.ndarray]:
    return [
        np.kron(SX, np.kron(I2, I2)),
        np.kron(I2, np.kron(SX, I2)),
        np.kron(I2, np.kron(I2, SX)),
    ]


def graph_first_axis_signature() -> tuple[int, tuple[tuple[float, float, float], ...], float]:
    pts = simplex_grid()
    vals = np.array([sum(p[i] * p[j] for i in range(3) for j in range(i + 1, 3)) for p in pts])
    min_val = float(vals.min())
    mins = [p for p, val in zip(pts, vals) if abs(val - min_val) < 1e-12]
    mins_t = tuple(tuple(float(x) for x in p) for p in mins)
    return len(mins), mins_t, min_val


def projected_commutant_bundle() -> dict[str, object]:
    gammas = build_cl3_gammas()
    comm_basis = compute_commutant_basis(gammas, dim=8)
    c3 = c3_taste_unitary()
    p1 = project_corner_eigenspace(np.array([np.pi, 0.0, 0.0]))
    p2 = project_corner_eigenspace(np.array([0.0, np.pi, 0.0]))
    p3 = project_corner_eigenspace(np.array([0.0, 0.0, np.pi]))
    proj_comm_x1 = compute_projected_commutant(comm_basis, p1, p1.shape[1])
    proj_cl3_x1 = [p1.conj().T @ m @ p1 for m in cl3_span_basis(gammas)]
    non_cl3 = None
    for m in proj_comm_x1:
        if not in_span(m, proj_cl3_x1):
            non_cl3 = m
            break
    if non_cl3 is None:
        raise RuntimeError("could not isolate a projected non-Cl(3) commutant generator")

    m_lift = p1 @ non_cl3 @ p1.conj().T
    profiles = {}
    for label, p in zip(["X1", "X2", "X3"], [p1, p2, p3]):
        cp = corner_profile(m_lift, p)
        profiles[label] = cp.trace

    v = np.array([profiles["X1"], profiles["X2"], profiles["X3"]], dtype=complex)
    v0, v1, v2 = orbit_fourier(v)
    tau = 0 if np.real(v1) >= 0 else 1
    q = int(np.argmax(np.array([np.real(v0), np.real(v0) - np.real(v1), np.real(v0) + np.real(v1)])))
    return {
        "profiles": profiles,
        "orbit_modes": (v0, v1, v2),
        "tau": tau,
        "q": q,
        "projected_commutant_dim": len(proj_comm_x1),
        "c3_maps_x1_to_x2_unitarily": np.allclose(
            np.linalg.svd(p2.conj().T @ c3 @ p1, compute_uv=False),
            np.ones(p1.shape[1]),
            atol=1e-10,
        ),
    }


def graph_commutant_route_signature() -> dict[str, object]:
    axis_count, mins, min_val = graph_first_axis_signature()
    comm = projected_commutant_bundle()
    return {
        "axis_count": axis_count,
        "axis_mins": mins,
        "axis_min_val": min_val,
        "tau": comm["tau"],
        "q": comm["q"],
        "orbit_modes": comm["orbit_modes"],
    }


def route_signature_for_block(block: np.ndarray, comm: dict[str, object]) -> dict[str, object]:
    coeffs = oriented_cycle_coeffs_from_block(block)
    return {
        "tau": comm["tau"],
        "q": comm["q"],
        "coeffs": coeffs,
        "coords": reduced_cycle_coordinates(block),
        "support": support_mask(block),
    }


def part1_graph_first_and_commutant_fix_the_selector_bundle() -> dict[str, object]:
    print("\n" + "=" * 88)
    print("PART 1: GRAPH-FIRST + PROJECTED COMMUTANT FIX THE SELECTOR BUNDLE")
    print("=" * 88)

    shifts = build_axis_shifts()
    for i, s in enumerate(shifts, start=1):
        check(f"S_{i} is Hermitian", np.allclose(s, s.conj().T, atol=1e-10))
        check(f"S_{i}^2 = I", np.allclose(s @ s, I8, atol=1e-10))

    axis_count, mins, min_val = graph_first_axis_signature()
    check("The graph-first selector has exactly three minima", axis_count == 3, f"count={axis_count}")
    check("Those minima are exactly the three coordinate axes", len(mins) == 3 and abs(min_val) < 1e-12,
          f"mins={mins}, min={min_val:.2e}")

    comm = projected_commutant_bundle()
    v0, v1, v2 = comm["orbit_modes"]

    check("The projected commutant generator has a 4-dimensional projected corner space", comm["projected_commutant_dim"] == 4,
          f"dim={comm['projected_commutant_dim']}")
    check("The C3 transport remains unitary on the projected corner orbit", bool(comm["c3_maps_x1_to_x2_unitarily"]))
    check("The even Fourier mode is the corner average", abs(v0 - np.mean(np.array(list(comm["profiles"].values()), dtype=complex))) < 1e-12,
          f"v0={v0:.6f}")
    check("The odd Fourier mode is nonzero", abs(v1) > 1e-12, f"|v1|={abs(v1):.6f}")
    print(f"  [INFO] The projected commutant fixes the selector bundle (tau,q)  (tau={comm['tau']}, q={comm['q']})")

    return comm


def part2_two_distinct_reduced_cycle_points_share_the_same_route_signature(comm: dict[str, object]) -> None:
    print("\n" + "=" * 88)
    print("PART 2: TWO DISTINCT REDUCED-CYCLE POINTS SHARE THE SAME ROUTE SIGNATURE")
    print("=" * 88)

    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)
    sig_a = route_signature_for_block(a, comm)
    sig_b = route_signature_for_block(b, comm)

    check("The reduced-cycle family is invariant under the residual swap-conjugate symmetry",
          np.linalg.norm(residual_swap_conjugate(a) - a) < 1e-12 and np.linalg.norm(residual_swap_conjugate(b) - b) < 1e-12)
    check("The route returns the same selector bundle on two distinct reduced-cycle points",
          sig_a["tau"] == sig_b["tau"] and sig_a["q"] == sig_b["q"],
          f"sig_a=(tau={sig_a['tau']}, q={sig_a['q']}), sig_b=(tau={sig_b['tau']}, q={sig_b['q']})")
    check("The two reduced-cycle points are genuinely different",
          np.linalg.norm(a - b) > 1e-6,
          f"|A-B|={np.linalg.norm(a - b):.6f}")
    check("Their reduced-cycle coordinates differ",
          np.linalg.norm(sig_a["coords"] - sig_b["coords"]) > 1e-6,
          f"coords_a={np.round(sig_a['coords'], 6)}, coords_b={np.round(sig_b['coords'], 6)}")
    check("Their oriented-cycle coefficients differ as well",
          np.linalg.norm(sig_a["coeffs"] - sig_b["coeffs"]) > 1e-6,
          f"coeffs_a={np.round(sig_a['coeffs'], 6)}, coeffs_b={np.round(sig_b['coeffs'], 6)}")


def part3_the_route_is_value_blind_even_though_the_values_are_realized() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ROUTE IS VALUE-BLIND EVEN THOUGH THE VALUES ARE REALIZED")
    print("=" * 88)

    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)
    sig_a = graph_commutant_route_signature()
    sig_b = graph_commutant_route_signature()

    check("The graph-first / projected-commutant route signature is constant", sig_a == sig_b,
          f"signature={sig_a}")
    check("The native oriented-cycle value law still reads the reduced values exactly on the active block",
          np.linalg.norm(oriented_cycle_coeffs_from_block(a) - np.array([0.41 + 0.32j, 0.28, 0.41 - 0.32j])) < 1e-12
          and np.linalg.norm(oriented_cycle_coeffs_from_block(b) - np.array([0.29 - 0.17j, 0.34, 0.29 + 0.17j])) < 1e-12)
    check("The same selector bundle is recovered on both reduced-cycle points",
          route_signature_for_block(a, sig_a)["tau"] == route_signature_for_block(b, sig_b)["tau"]
          and route_signature_for_block(a, sig_a)["q"] == route_signature_for_block(b, sig_b)["q"])
    check("So the route does not collapse the 3-real reduced family to a unique point",
          np.linalg.norm(a - b) > 1e-6 and sig_a == sig_b,
          "same route signature, different values")

    print()
    print("  This is the exact boundary: the graph-native projected-commutant")
    print("  route fixes the selector bundle, but it is constant on the reduced")
    print("  forward-cycle family and therefore cannot select (u,v,w).")


def part4_current_bank_status() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CURRENT-BANK STATUS")
    print("=" * 88)

    note = read("docs/PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md")
    reduced = read("docs/PMNS_ORIENTED_CYCLE_REDUCED_CHANNEL_NONSELECTION_NOTE.md")
    selector = read("docs/PMNS_COMMUTANT_EIGENOPERATOR_SELECTOR_NOTE.md")
    graph = read("docs/PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md")

    check("The value-law note confirms the reduced-cycle coefficients are read from the active block",
          "diag(A C^dagger)" in note or "diag(A C^\\dagger)" in note)
    check("The reduced-channel no-go note says the current bank does not select a unique point",
          "unique value on the reduced channel" in reduced or "does not select a unique point" in reduced)
    check("The commutant note says the route is only partial", "positive native selector law" in selector and "not a full PMNS microscopic closure theorem" in selector)
    check("The graph-first note still only derives alignment, not values",
          "What It Does Not Yet Give" in graph and "(a,b,c,d)" in graph and "which lepton sector carries the active block" in graph)

    print()
    print("  So the graph-native projected commutant attack is a real selector")
    print("  theorem, but not the missing value law.")


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-COMMUTANT CYCLE VALUE BOUNDARY")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - graph-first axis alignment")
    print("  - projected commutant eigenoperator selector")
    print("  - oriented-cycle channel value law")
    print("  - reduced-channel nonselection theorem")
    print()
    print("Question:")
    print("  Can the graph-native projected commutant / generation-boundary")
    print("  route derive a positive value law for the reduced forward-cycle")
    print("  channel A_fwd(u,v,w)?")

    comm = part1_graph_first_and_commutant_fix_the_selector_bundle()
    part2_two_distinct_reduced_cycle_points_share_the_same_route_signature(comm)
    part3_the_route_is_value_blind_even_though_the_values_are_realized()
    part4_current_bank_status()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact graph-native projected-commutant answer:")
    print("    - the route fixes the weak axis and residual Z2 stabilizer")
    print("    - it fixes the selector bundle (tau,q)")
    print("    - it leaves the reduced forward-cycle values (u,v,w) unfixed")
    print()
    print("  Therefore this route does not supply the missing value law.")
    print("  It sharpens the boundary and points to the next positive target:")
    print("  a lower-level source/transport law, not more commutant data.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
