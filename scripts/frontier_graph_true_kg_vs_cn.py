#!/usr/bin/env python3
"""
Graph Scalar Comparison: CN Lane vs True Local KG
=================================================

Compares two scalar graph theories on the same graphs:

  A. CN scalar lane
     i dpsi/dt = (L + m^2 I + V) psi
     evolved with Crank-Nicolson

  B. True local second-order KG lane
     dphi/dt = pi
     dpi/dt = -(L + m^2 I + V) phi
     evolved with leapfrog on the doubled state (phi, pi)

The goal is not to force agreement. It is to determine whether the
current CN scalar lane is a faithful stand-in for a true local graph KG
theory in the tested regime.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import stats
from scipy.sparse import csr_matrix, diags, eye as speye, lil_matrix
from scipy.sparse.linalg import splu


def idx(x: int, y: int, z: int, n: int) -> int:
    return (x % n) * n * n + (y % n) * n + (z % n)


def cubic_graph(n: int) -> tuple[csr_matrix, np.ndarray]:
    n_nodes = n**3
    adj = lil_matrix((n_nodes, n_nodes), dtype=float)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i = idx(x, y, z, n)
                for dx, dy, dz in [
                    (1, 0, 0),
                    (-1, 0, 0),
                    (0, 1, 0),
                    (0, -1, 0),
                    (0, 0, 1),
                    (0, 0, -1),
                ]:
                    adj[i, idx(x + dx, y + dy, z + dz, n)] = 1.0
    pos = np.array(
        [[x, y, z] for x in range(n) for y in range(n) for z in range(n)],
        dtype=float,
    ) / float(max(n - 1, 1))
    return csr_matrix(adj), pos


def random_geometric_graph(n_nodes: int, radius: float, seed: int = 42) -> tuple[csr_matrix, np.ndarray]:
    rng = np.random.RandomState(seed)
    pos = rng.uniform(0.0, 1.0, size=(n_nodes, 3))
    adj = lil_matrix((n_nodes, n_nodes), dtype=float)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if np.linalg.norm(pos[i] - pos[j]) < radius:
                adj[i, j] = 1.0
                adj[j, i] = 1.0
    return csr_matrix(adj), pos


def graph_laplacian(adj: csr_matrix) -> csr_matrix:
    deg = np.array(adj.sum(axis=1)).flatten()
    return diags(deg) - adj


def gaussian_on_graph(pos: np.ndarray, center_idx: int, sigma: float = 0.12) -> np.ndarray:
    d = np.linalg.norm(pos - pos[center_idx], axis=1)
    psi = np.exp(-(d**2) / (2 * sigma**2)).astype(complex)
    return psi / np.linalg.norm(psi)


def packet_on_graph(
    pos: np.ndarray,
    center_idx: int,
    k0: float,
    sigma: float = 0.14,
    axis: int = 2,
) -> np.ndarray:
    d = np.linalg.norm(pos - pos[center_idx], axis=1)
    env = np.exp(-(d**2) / (2 * sigma**2))
    phase = np.exp(1j * k0 * (pos[:, axis] - pos[center_idx, axis]))
    psi = (env * phase).astype(complex)
    return psi / np.linalg.norm(psi)


def cz(prob: np.ndarray, pos: np.ndarray) -> float:
    total = np.sum(prob)
    if total <= 0:
        return 0.0
    return float(np.sum(prob * pos[:, 2]) / total)


def build_potential(pos: np.ndarray, mass_idx: int, mass: float, g: float, strength: float, eps: float = 0.05) -> np.ndarray:
    d = np.linalg.norm(pos - pos[mass_idx], axis=1)
    return -mass * g * strength / (d + eps)


def cn_propagator(H: csr_matrix, dt: float):
    a_plus = (speye(H.shape[0], dtype=complex) + 0.5j * dt * H).tocsc()
    a_minus = (speye(H.shape[0], dtype=complex) - 0.5j * dt * H).tocsr()
    lu = splu(a_plus)

    def step(psi: np.ndarray) -> np.ndarray:
        return lu.solve(a_minus.dot(psi))

    return step


def evolve_cn(L: csr_matrix, mass: float, dt: float, n_steps: int, psi0: np.ndarray, V: np.ndarray | None = None) -> np.ndarray:
    vdiag = diags(V) if V is not None else diags(np.zeros(L.shape[0]))
    H = (L + (mass**2) * speye(L.shape[0]) + vdiag).astype(complex)
    step = cn_propagator(H, dt)
    psi = psi0.copy()
    for _ in range(n_steps):
        psi = step(psi)
    return psi


def evolve_true_kg(
    L: csr_matrix,
    mass: float,
    dt: float,
    n_steps: int,
    phi0: np.ndarray,
    pi0: np.ndarray | None = None,
    V: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    phi = phi0.copy().astype(complex)
    pi = np.zeros_like(phi) if pi0 is None else pi0.copy().astype(complex)
    v = np.zeros(L.shape[0]) if V is None else V
    m2 = mass**2
    for _ in range(n_steps):
        force = -(L.dot(phi) + m2 * phi + v * phi)
        pi += 0.5 * dt * force
        phi += dt * pi
        force = -(L.dot(phi) + m2 * phi + v * phi)
        pi += 0.5 * dt * force
    return phi, pi


def kg_energy(L: csr_matrix, mass: float, phi: np.ndarray, pi: np.ndarray, V: np.ndarray | None = None) -> float:
    v = np.zeros(L.shape[0]) if V is None else V
    kinetic = float(np.vdot(pi, pi).real)
    potential = float(np.vdot(phi, L.dot(phi) + (mass**2) * phi + v * phi).real)
    return kinetic + potential


def cn_expectation(L: csr_matrix, mass: float, psi: np.ndarray, V: np.ndarray | None = None) -> float:
    vdiag = diags(V) if V is not None else diags(np.zeros(L.shape[0]))
    H = (L + (mass**2) * speye(L.shape[0]) + vdiag).astype(complex)
    return float(np.vdot(psi, H.dot(psi)).real)


def cubic_lambda_axis(k: float) -> float:
    return 2.0 * (1.0 - math.cos(k))


def cubic_lambda_diag(k: float) -> float:
    return 3.0 * cubic_lambda_axis(k)


def cn_omega_sq_from_lambda(mass: float, lam: np.ndarray) -> np.ndarray:
    return (mass**2 + lam) ** 2


def kg_omega_sq_from_lambda(mass: float, lam: np.ndarray) -> np.ndarray:
    return mass**2 + lam


def axis_diag_fit(mass: float, model: str, k2_cut: float = 0.8) -> dict[str, float]:
    f = np.fft.fftfreq(41) * 2 * np.pi
    axis_k2 = np.array([k * k for k in f])
    diag_k2 = np.array([3 * k * k for k in f])
    axis_lam = np.array([cubic_lambda_axis(k) for k in f])
    diag_lam = np.array([cubic_lambda_diag(k) for k in f])
    if model == "cn":
        axis_E2 = cn_omega_sq_from_lambda(mass, axis_lam)
        diag_E2 = cn_omega_sq_from_lambda(mass, diag_lam)
    else:
        axis_E2 = kg_omega_sq_from_lambda(mass, axis_lam)
        diag_E2 = kg_omega_sq_from_lambda(mass, diag_lam)
    ma = axis_k2 < k2_cut
    md = diag_k2 < k2_cut
    sa, ia, ra, _, _ = stats.linregress(axis_k2[ma], axis_E2[ma])
    sd, idg, rd, _, _ = stats.linregress(diag_k2[md], diag_E2[md])
    iso = max(sa, sd) / min(sa, sd)
    return {
        "r2": min(ra**2, rd**2),
        "iso": iso,
        "intercept_axis": ia,
        "intercept_diag": idg,
        "n_axis": int(np.sum(ma)),
        "n_diag": int(np.sum(md)),
        "slope_axis": sa,
        "slope_diag": sd,
    }


def random_spectral_fit(L: csr_matrix, mass: float, model: str, frac: float = 0.3) -> dict[str, float]:
    evals = np.sort(np.linalg.eigvalsh(L.toarray()))
    nz = evals[evals > 1e-10]
    n_fit = max(6, int(len(nz) * frac))
    lam = nz[:n_fit]
    if model == "cn":
        E2 = cn_omega_sq_from_lambda(mass, lam)
    else:
        E2 = kg_omega_sq_from_lambda(mass, lam)
    slope, intercept, r_val, _, _ = stats.linregress(lam, E2)
    return {
        "r2": r_val**2,
        "intercept": intercept,
        "slope": slope,
        "n_fit": n_fit,
    }


def omega_operator_dense(L: csr_matrix, mass: float) -> tuple[np.ndarray, np.ndarray]:
    evals, evecs = np.linalg.eigh(L.toarray())
    omega = np.sqrt(np.maximum(mass**2 + evals, 0.0))
    return evecs, omega


def apply_omega(evecs: np.ndarray, omega: np.ndarray, vec: np.ndarray) -> np.ndarray:
    coeffs = evecs.T.conj() @ vec
    return evecs @ (omega * coeffs)


def estimate_vg_cn(k0: float) -> float:
    return abs(2.0 * math.sin(k0))


def estimate_vg_kg(mass: float, k0: float) -> float:
    omega = math.sqrt(mass**2 + cubic_lambda_axis(k0))
    return abs(math.sin(k0) / omega) if omega > 0 else 0.0


@dataclass
class DynamicsSummary:
    label: str
    gravity_delta: float
    f_r2: float
    growth_all_toward: bool
    growth_monotone: bool
    k_cv: float
    k_same_sign: bool
    invariant_drift: float
    detail: dict


def cn_dynamics_summary(
    L: csr_matrix,
    pos: np.ndarray,
    mass: float,
    dt: float,
    steps: int,
    center_idx: int,
    mass_idx: int,
    g: float,
    strength: float,
) -> DynamicsSummary:
    psi0 = gaussian_on_graph(pos, center_idx)
    V = build_potential(pos, mass_idx, mass, g, strength)
    free = evolve_cn(L, mass, dt, steps, psi0)
    grav = evolve_cn(L, mass, dt, steps, psi0, V=V)
    d = cz(np.abs(grav) ** 2, pos) - cz(np.abs(free) ** 2, pos)

    strengths = np.array([1e-4, 2e-4, 5e-4, 1e-3, 2e-3])
    forces = []
    for s in strengths:
        V_s = build_potential(pos, mass_idx, mass, g, s)
        phi_s = evolve_cn(L, mass, dt, steps, psi0, V=V_s)
        forces.append(cz(np.abs(phi_s) ** 2, pos) - cz(np.abs(free) ** 2, pos))
    slope, intercept = np.polyfit(strengths, forces, 1)
    pred = slope * strengths + intercept
    f_r2 = 1.0 - np.sum((np.array(forces) - pred) ** 2) / np.sum((np.array(forces) - np.mean(forces)) ** 2)

    ns_list = [max(4, steps // 2), steps, int(1.5 * steps), 2 * steps]
    growth = []
    for ns in ns_list:
        free_ns = evolve_cn(L, mass, dt, ns, psi0)
        grav_ns = evolve_cn(L, mass, dt, ns, psi0, V=V)
        growth.append(cz(np.abs(grav_ns) ** 2, pos) - cz(np.abs(free_ns) ** 2, pos))
    growth_all_toward = all(v > 0 for v in growth)
    growth_monotone = all(abs(growth[i + 1]) >= abs(growth[i]) * 0.95 for i in range(len(growth) - 1))

    rows_k = []
    target_travel = 3.0 * dt * steps
    for k0 in [0.15, 0.25, 0.35, 0.45, 0.55]:
        vg = max(estimate_vg_cn(k0), 1e-6)
        ns = max(4, min(2 * steps, int(round(target_travel / (vg * dt)))))
        psi_k = packet_on_graph(pos, center_idx, k0)
        free_k = evolve_cn(L, mass, dt, ns, psi_k)
        grav_k = evolve_cn(L, mass, dt, ns, psi_k, V=V)
        rows_k.append(cz(np.abs(grav_k) ** 2, pos) - cz(np.abs(free_k) ** 2, pos))
    rows_k = np.array(rows_k)
    k_same_sign = np.all(rows_k > 0) or np.all(rows_k < 0)
    k_cv = float(np.std(rows_k) / np.mean(np.abs(rows_k))) if np.mean(np.abs(rows_k)) > 0 else float("inf")

    e0 = cn_expectation(L, mass, psi0, V)
    ef = cn_expectation(L, mass, grav, V)
    invariant_drift = abs(ef - e0) / max(abs(e0), 1e-12)
    return DynamicsSummary(
        label="cn",
        gravity_delta=d,
        f_r2=f_r2,
        growth_all_toward=growth_all_toward,
        growth_monotone=growth_monotone,
        k_cv=k_cv,
        k_same_sign=k_same_sign,
        invariant_drift=invariant_drift,
        detail={
            "forces": forces,
            "growth": growth,
            "rows_k": rows_k.tolist(),
            "steps": ns_list,
        },
    )


def kg_dynamics_summary(
    L: csr_matrix,
    pos: np.ndarray,
    mass: float,
    dt: float,
    steps: int,
    center_idx: int,
    mass_idx: int,
    g: float,
    strength: float,
    omega_data: tuple[np.ndarray, np.ndarray] | None = None,
) -> DynamicsSummary:
    phi0 = gaussian_on_graph(pos, center_idx)
    if omega_data is None:
        pi0 = -1j * mass * phi0
    else:
        pi0 = -1j * apply_omega(omega_data[0], omega_data[1], phi0)
    V = build_potential(pos, mass_idx, mass, g, strength)
    free_phi, free_pi = evolve_true_kg(L, mass, dt, steps, phi0, pi0=pi0, V=None)
    grav_phi, grav_pi = evolve_true_kg(L, mass, dt, steps, phi0, pi0=pi0, V=V)
    d = cz(np.abs(grav_phi) ** 2, pos) - cz(np.abs(free_phi) ** 2, pos)

    strengths = np.array([1e-4, 2e-4, 5e-4, 1e-3, 2e-3])
    forces = []
    for s in strengths:
        V_s = build_potential(pos, mass_idx, mass, g, s)
        phi_s, _ = evolve_true_kg(L, mass, dt, steps, phi0, pi0=pi0, V=V_s)
        forces.append(cz(np.abs(phi_s) ** 2, pos) - cz(np.abs(free_phi) ** 2, pos))
    slope, intercept = np.polyfit(strengths, forces, 1)
    pred = slope * strengths + intercept
    f_r2 = 1.0 - np.sum((np.array(forces) - pred) ** 2) / np.sum((np.array(forces) - np.mean(forces)) ** 2)

    ns_list = [max(4, steps // 2), steps, int(1.5 * steps), 2 * steps]
    growth = []
    for ns in ns_list:
        free_ns, _ = evolve_true_kg(L, mass, dt, ns, phi0, pi0=pi0, V=None)
        grav_ns, _ = evolve_true_kg(L, mass, dt, ns, phi0, pi0=pi0, V=V)
        growth.append(cz(np.abs(grav_ns) ** 2, pos) - cz(np.abs(free_ns) ** 2, pos))
    growth_all_toward = all(v > 0 for v in growth)
    growth_monotone = all(abs(growth[i + 1]) >= abs(growth[i]) * 0.95 for i in range(len(growth) - 1))

    rows_k = []
    target_travel = 3.0 * dt * steps
    for k0 in [0.15, 0.25, 0.35, 0.45, 0.55]:
        vg = max(estimate_vg_kg(mass, k0), 1e-6)
        ns = max(4, min(2 * steps, int(round(target_travel / (vg * dt)))))
        phi_k = packet_on_graph(pos, center_idx, k0)
        if omega_data is None:
            omega0 = math.sqrt(mass**2 + cubic_lambda_axis(k0))
            pi_k = -1j * omega0 * phi_k
        else:
            pi_k = -1j * apply_omega(omega_data[0], omega_data[1], phi_k)
        free_k, _ = evolve_true_kg(L, mass, dt, ns, phi_k, pi0=pi_k, V=None)
        grav_k, _ = evolve_true_kg(L, mass, dt, ns, phi_k, pi0=pi_k, V=V)
        rows_k.append(cz(np.abs(grav_k) ** 2, pos) - cz(np.abs(free_k) ** 2, pos))
    rows_k = np.array(rows_k)
    k_same_sign = np.all(rows_k > 0) or np.all(rows_k < 0)
    k_cv = float(np.std(rows_k) / np.mean(np.abs(rows_k))) if np.mean(np.abs(rows_k)) > 0 else float("inf")

    e0 = kg_energy(L, mass, phi0, pi0, V)
    ef = kg_energy(L, mass, grav_phi, grav_pi, V)
    invariant_drift = abs(ef - e0) / max(abs(e0), 1e-12)
    return DynamicsSummary(
        label="true_kg",
        gravity_delta=d,
        f_r2=f_r2,
        growth_all_toward=growth_all_toward,
        growth_monotone=growth_monotone,
        k_cv=k_cv,
        k_same_sign=k_same_sign,
        invariant_drift=invariant_drift,
        detail={
            "forces": forces,
            "growth": growth,
            "rows_k": rows_k.tolist(),
            "steps": ns_list,
        },
    )


def print_modal_section(title: str, cn_stats: dict[str, float], kg_stats: dict[str, float], mass: float):
    print(f"\n{title}")
    print("-" * len(title))
    print(
        "  CN lane     : "
        f"R^2={cn_stats['r2']:.6f}, slope_axis={cn_stats.get('slope_axis', cn_stats.get('slope', 0.0)):.4f}, "
        f"intercept={cn_stats.get('intercept_axis', cn_stats.get('intercept', 0.0)):.4f}"
    )
    print(
        "  True KG lane: "
        f"R^2={kg_stats['r2']:.6f}, slope_axis={kg_stats.get('slope_axis', kg_stats.get('slope', 0.0)):.4f}, "
        f"intercept={kg_stats.get('intercept_axis', kg_stats.get('intercept', 0.0)):.4f}"
    )
    if "iso" in cn_stats:
        print(
            f"  Isotropy    : CN iso={cn_stats['iso']:.4f} "
            f"(axis={cn_stats['n_axis']}, diag={cn_stats['n_diag']}), "
            f"KG iso={kg_stats['iso']:.4f}"
        )
    print(f"  KG target   : omega^2 = m^2 + lambda, m^2={mass**2:.4f}")


def print_dynamics_section(title: str, cn_dyn: DynamicsSummary, kg_dyn: DynamicsSummary):
    print(f"\n{title}")
    print("-" * len(title))
    print(
        f"  Gravity     : CN {cn_dyn.gravity_delta:+.4e}, KG {kg_dyn.gravity_delta:+.4e}"
    )
    print(
        f"  F~M         : CN R^2={cn_dyn.f_r2:.6f}, KG R^2={kg_dyn.f_r2:.6f}"
    )
    print(
        f"  N-growth    : CN toward={cn_dyn.growth_all_toward}, mono={cn_dyn.growth_monotone}; "
        f"KG toward={kg_dyn.growth_all_toward}, mono={kg_dyn.growth_monotone}"
    )
    print(
        f"  Carrier-k   : CN same_sign={cn_dyn.k_same_sign}, CV={cn_dyn.k_cv:.4f}; "
        f"KG same_sign={kg_dyn.k_same_sign}, CV={kg_dyn.k_cv:.4f}"
    )
    print(
        f"  Invariant   : CN expectation drift={cn_dyn.invariant_drift:.4e}; "
        f"KG energy drift={kg_dyn.invariant_drift:.4e}"
    )


def main():
    mass = 0.3
    g = 5.0
    strength = 5e-4

    print("=" * 78)
    print("GRAPH TRUE KG VS CN SCALAR COMPARISON")
    print("=" * 78)
    print("A: CN lane      i dpsi/dt = (L + m^2 + V) psi")
    print("B: True KG lane dphi/dt = pi, dpi/dt = -(L + m^2 + V) phi")
    print()

    # Cubic graph: modal law + dynamics
    n = 15
    adj_c, pos_c = cubic_graph(n)
    L_c = graph_laplacian(adj_c)
    center = np.mean(pos_c, axis=0)
    ci = int(np.argmin(np.sum((pos_c - center) ** 2, axis=1)))
    target = center.copy()
    target[2] += 3.0 / (n - 1)
    mi = int(np.argmin(np.sum((pos_c - target) ** 2, axis=1)))

    cn_modal_c = axis_diag_fit(mass, "cn")
    kg_modal_c = axis_diag_fit(mass, "kg")
    print_modal_section("Cubic Free-Mode Comparison", cn_modal_c, kg_modal_c, mass)

    cn_dyn_c = cn_dynamics_summary(L_c, pos_c, mass, dt=0.03, steps=18, center_idx=ci, mass_idx=mi, g=g, strength=strength)
    kg_dyn_c = kg_dynamics_summary(L_c, pos_c, mass, dt=0.03, steps=18, center_idx=ci, mass_idx=mi, g=g, strength=strength)
    print_dynamics_section("Cubic Dynamics Comparison", cn_dyn_c, kg_dyn_c)

    # One non-cubic graph: low-mode fit + one operating point.
    adj_r, pos_r = random_geometric_graph(140, radius=0.22, seed=42)
    L_r = graph_laplacian(adj_r)
    center_r = np.mean(pos_r, axis=0)
    ci_r = int(np.argmin(np.sum((pos_r - center_r) ** 2, axis=1)))
    target_r = center_r.copy()
    target_r[2] += 0.2
    mi_r = int(np.argmin(np.sum((pos_r - target_r) ** 2, axis=1)))

    cn_modal_r = random_spectral_fit(L_r, mass, "cn")
    kg_modal_r = random_spectral_fit(L_r, mass, "kg")
    print_modal_section("Random-Graph Low-Mode Comparison", cn_modal_r, kg_modal_r, mass)

    cn_dyn_r = cn_dynamics_summary(L_r, pos_r, mass, dt=0.02, steps=24, center_idx=ci_r, mass_idx=mi_r, g=g, strength=strength)
    omega_r = omega_operator_dense(L_r, mass)
    kg_dyn_r = kg_dynamics_summary(
        L_r,
        pos_r,
        mass,
        dt=0.02,
        steps=24,
        center_idx=ci_r,
        mass_idx=mi_r,
        g=g,
        strength=strength,
        omega_data=omega_r,
    )
    print_dynamics_section("Random-Graph Dynamics Comparison", cn_dyn_r, kg_dyn_r)

    # Verdict
    same_gravity_sign = (cn_dyn_c.gravity_delta > 0) == (kg_dyn_c.gravity_delta > 0)
    same_growth = cn_dyn_c.growth_all_toward == kg_dyn_c.growth_all_toward and cn_dyn_c.growth_monotone == kg_dyn_c.growth_monotone
    modal_match = (
        abs(cn_modal_c["slope_axis"] - kg_modal_c["slope_axis"]) < 0.1
        and abs(cn_modal_c["intercept_axis"] - kg_modal_c["intercept_axis"]) < 0.1
    )
    print("\nVerdict")
    print("-------")
    print(f"  Modal law agreement : {modal_match}")
    print(f"  Gravity sign agreement (cubic) : {same_gravity_sign}")
    print(f"  Growth-pattern agreement (cubic) : {same_growth}")
    print("  Interpretation: if the modal laws diverge strongly while only some gravity rows agree,")
    print("  the CN scalar lane is a useful low-energy control, not a faithful stand-in for true local KG.")


if __name__ == "__main__":
    main()
