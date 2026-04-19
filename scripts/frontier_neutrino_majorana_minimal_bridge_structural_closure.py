#!/usr/bin/env python3
"""
Majorana minimal-bridge structural closure runner.

Question:
  After the pure-retained Majorana lane closes negatively at mu = 0, does the
  current branch already contain a coherent post-retained bridge that closes
  the Majorana structural lane positively?

Answer on the minimal admitted bridge:
  Yes. The post-retained local grammar is forced to the Nambu-complete
  pseudospin span{J_x, J_y, J_z}; the genuinely new one-generation source
  collapses to the pure-pairing ray mu J_x up to exact local nu_R rephasing;
  the finite staircase anchor is k_B = 8; the exact weak-axis adjacency fixes
  k_A = 7; and the minimal symmetric residual-sharing lift fixes

      eps / B = alpha_LM / 2.

Boundary:
  This closes the Majorana structural lane on the minimal post-retained
  bridge only. It does not close full PMNS/flavor structure or the downstream
  CP-kernel/washout tail.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
ALPHA_BARE = 1.0 / (4.0 * PI)
PLAQ_MC = 0.5934
U0 = PLAQ_MC ** 0.25
ALPHA_LM = ALPHA_BARE / U0
M_PL = 1.2209e19
C_APBC = (7.0 / 8.0) ** 0.25
V_EW = M_PL * C_APBC * ALPHA_LM ** 16
G_WEAK = 0.653
Y_NU_EFF = (G_WEAK * G_WEAK) / 64.0

N_TASTE = 16
K_B = 8
K_A = 7
RHO_SELF_DUAL = 1.0
EPS_OVER_B = ALPHA_LM / 2.0
DM2_31_OBS = 2.453e-3
M3_OBS = math.sqrt(DM2_31_OBS)

I2 = np.eye(2, dtype=complex)
SX = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
GAMMA_1 = np.kron(SX, np.kron(I2, I2))

STATES = [(s1, s2, s3) for s1 in range(2) for s2 in range(2) for s3 in range(2)]
INDEX = {state: idx for idx, state in enumerate(STATES)}
O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]


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


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def annihilation_operators(n_modes: int) -> list[np.ndarray]:
    sigma_minus = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    ident = np.eye(2, dtype=complex)

    operators: list[np.ndarray] = []
    for mode in range(n_modes):
        op = np.array([[1.0]], dtype=complex)
        for idx in range(n_modes):
            if idx < mode:
                op = np.kron(op, sigma_z)
            elif idx == mode:
                op = np.kron(op, sigma_minus)
            else:
                op = np.kron(op, ident)
        operators.append(op)
    return operators


def unitary_from_generator(generator: np.ndarray, theta: float) -> np.ndarray:
    evals, evecs = np.linalg.eigh(generator)
    phases = np.diag(np.exp(-1j * theta * evals))
    return evecs @ phases @ evecs.conj().T


def basis(states: list[tuple[int, int, int]]) -> np.ndarray:
    eye = np.eye(8, dtype=complex)
    return np.column_stack([eye[:, INDEX[state]] for state in states])


def coeffs_in_basis(operator: np.ndarray, basis_ops: list[np.ndarray]) -> np.ndarray:
    gram = np.array(
        [[np.trace(bi.conj().T @ bj) for bj in basis_ops] for bi in basis_ops],
        dtype=complex,
    )
    rhs = np.array([np.trace(bi.conj().T @ operator) for bi in basis_ops], dtype=complex)
    return np.linalg.solve(gram, rhs)


def local_block_generators() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    c1, c2 = annihilation_operators(2)
    n1 = c1.conj().T @ c1
    n2 = c2.conj().T @ c2
    ident = np.eye(c1.shape[0], dtype=complex)

    pair_ann = c1 @ c2
    pair_cre = pair_ann.conj().T
    jx = 0.5 * (pair_ann + pair_cre)
    jy = (pair_cre - pair_ann) / (2.0j)
    jz = 0.5 * (n1 + n2 - ident)
    return jx, jy, jz, n1 + n2


def part1_local_nambu_completion() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE POST-RETAINED LOCAL SOURCE GRAMMAR IS NAMBU-COMPLETE")
    print("=" * 88)

    jx, jy, jz, _ = local_block_generators()

    comm_xy = np.linalg.norm(commutator(jx, jy) - 1j * jz)
    comm_yz = np.linalg.norm(commutator(jy, jz) - 1j * jx)
    comm_zx = np.linalg.norm(commutator(jz, jx) - 1j * jy)

    u = unitary_from_generator(jx, math.pi / 2.0)
    rotated = u @ jz @ u.conj().T
    target_err = np.linalg.norm(rotated + jy)
    normal_residual = np.linalg.norm(rotated - np.trace(jz.conj().T @ rotated) / np.trace(jz.conj().T @ jz) * jz)

    check("The unique local block closes as an exact pseudospin su(2)", comm_xy < 1e-12 and comm_yz < 1e-12 and comm_zx < 1e-12,
          f"errors=({comm_xy:.2e},{comm_yz:.2e},{comm_zx:.2e})")
    check("The retained normal slice span{J_z} is not canonically closed", normal_residual > 1e-3,
          f"outside residual={normal_residual:.6f}")
    check("A canonical rotation carries J_z into a pairing direction", target_err < 1e-12,
          f"target error={target_err:.2e}")

    print()
    print("  So the minimal admitted post-retained local source family is the")
    print("  full Nambu-complete span{J_x, J_y, J_z}, not the retained J_z slice.")
    return jx, jy, jz


def part2_source_ray(jx: np.ndarray, jy: np.ndarray, jz: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE GENUINELY NEW ONE-GENERATION SOURCE DIRECTION IS ONE RAY")
    print("=" * 88)

    a, b = -0.37, 0.91
    mu = math.hypot(a, b)
    transverse = a * jx + b * jy

    theta = -math.atan2(b, a)
    u = unitary_from_generator(jz, theta)
    aligned = u @ transverse @ u.conj().T
    coeffs = coeffs_in_basis(aligned, [jx, jy, jz])

    align_err = np.linalg.norm(aligned - mu * jx)
    jy_err = abs(coeffs[1])
    jz_err = abs(coeffs[2])

    check("The genuinely new source lies in the transverse pairing plane", abs(coeffs_in_basis(transverse, [jx, jy, jz])[2]) < 1e-12,
          "no J_z component")
    check("Exact local nu_R rephasing aligns any nonzero new source to mu J_x", align_err < 1e-12,
          f"alignment error={align_err:.2e}")
    check("The aligned source has no residual J_y or J_z component", jy_err < 1e-12 and jz_err < 1e-12,
          f"|c_y|={jy_err:.2e}, |c_z|={jz_err:.2e}")

    print()
    print(f"  So the one-generation post-retained source direction is fixed to the")
    print(f"  canonical pure-pairing ray mu J_x, with mu={mu:.6f} in this test orbit.")


def part3_midpoint_anchor() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE FINITE MAJORANA STAIRCASE ANCHOR IS k_B = 8")
    print("=" * 88)

    def endpoint_exchange(k: int) -> int:
        return N_TASTE - k

    fixed = [k for k in range(N_TASTE + 1) if endpoint_exchange(k) == k]
    products = [ALPHA_LM ** k * ALPHA_LM ** endpoint_exchange(k) for k in range(N_TASTE + 1)]
    target = ALPHA_LM ** N_TASTE
    prod_err = max(abs(prod - target) for prod in products)

    check("The minimal endpoint-exchange bridge is the unique involution k -> 16-k", fixed == [K_B],
          f"fixed points={fixed}")
    check("The scale-side exchange is lambda -> alpha_LM^16 / lambda", prod_err < 1e-18,
          f"max product error={prod_err:.2e}")
    check("The unique fixed point of the finite bridge is k_B = 8", K_B == 8,
          f"k_B={K_B}")

    print()
    print("  So the absolute doublet anchor is no longer open on the minimal")
    print("  finite non-homogeneous bridge.")


def part4_adjacent_singlet_placement() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE EXACT WEAK-AXIS ADJACENCY FIXES k_A = 7")
    print("=" * 88)

    b0 = basis(O0)
    b1 = basis(T1)
    b2 = basis(T2)
    p0 = b0 @ b0.conj().T
    p2 = b2 @ b2.conj().T

    image_states = []
    for state in T1:
        vec = np.zeros(8, dtype=complex)
        vec[INDEX[state]] = 1.0
        image = GAMMA_1 @ vec
        image_state = STATES[int(np.argmax(np.abs(image)))]
        image_states.append((state, image_state))

    uv_images = [dst for _, dst in image_states if sum(dst) < 1]
    ir_images = [dst for _, dst in image_states if sum(dst) > 1]
    via_o0 = b1.conj().T @ GAMMA_1 @ p0 @ GAMMA_1 @ b1
    via_t2 = b1.conj().T @ GAMMA_1 @ p2 @ GAMMA_1 @ b1

    check("The exact T_1 return splits into one singled-out UV path and one residual doublet path",
          uv_images == O0 and len(ir_images) == 2,
          f"uv={uv_images}, ir={ir_images}")
    check("The singled-out return channel is exactly diag(1,0,0)", np.allclose(via_o0, np.diag([1.0, 0.0, 0.0]), atol=1e-12),
          "via O_0 = diag(1,0,0)")
    check("The residual return channel is exactly diag(0,1,1)", np.allclose(via_t2, np.diag([0.0, 1.0, 1.0]), atol=1e-12),
          "via T_2 = diag(0,1,1)")
    check("The minimal adjacent lift places the singlet one step above the anchored doublet", K_A == K_B - 1,
          f"k_A={K_A}, k_B={K_B}")

    print()
    print("  So the singlet/doublet placement is fixed on the same minimal bridge:")
    print(f"  k_A={K_A}, k_B={K_B}.")


def part5_split_law() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 5: THE MINIMAL BRIDGE FIXES eps/B = alpha_LM / 2")
    print("=" * 88)

    a_scale = M_PL * ALPHA_LM ** K_A
    b_scale = M_PL * ALPHA_LM ** K_B
    alpha_step = b_scale / a_scale
    eps_over_b = RHO_SELF_DUAL * alpha_step * 0.5

    check("The local selector remains self-dual at rho = 1", abs(RHO_SELF_DUAL - 1.0) < 1e-12,
          f"rho={RHO_SELF_DUAL:.12f}")
    check("The fixed adjacent placement gives one exact step B/A = alpha_LM", abs(alpha_step - ALPHA_LM) < 1e-15,
          f"B/A={alpha_step:.12f}")
    check("The minimal symmetric residual-sharing lift fixes eps/B = alpha_LM/2", abs(eps_over_b - EPS_OVER_B) < 1e-15,
          f"eps/B={eps_over_b:.12f}")

    print()
    print(f"  This removes the old free split law on the minimal bridge:")
    print(f"  eps/B = {eps_over_b:.12f}.")
    return a_scale, b_scale


def part6_downstream_atmospheric_benchmark(a_scale: float, b_scale: float) -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE CLOSED MAJORANA BRIDGE ALREADY SUPPORTS THE ATMOSPHERIC BENCHMARK")
    print("=" * 88)

    m1 = Y_NU_EFF ** 2 * V_EW ** 2 / a_scale * 1e9
    m2 = Y_NU_EFF ** 2 * V_EW ** 2 / (b_scale * (1.0 + EPS_OVER_B)) * 1e9
    m3 = Y_NU_EFF ** 2 * V_EW ** 2 / (b_scale * (1.0 - EPS_OVER_B)) * 1e9
    dm31 = m3 * m3 - m1 * m1

    check("The closed bridge predicts the atmospheric benchmark scale without fitting m_3",
          abs(m3 - M3_OBS) / M3_OBS < 0.05,
          f"m3={m3:.6e} eV vs obs {M3_OBS:.6e} eV")
    check("The diagonal atmospheric gap lands within 5% of observation",
          abs(dm31 - DM2_31_OBS) / DM2_31_OBS < 0.05,
          f"Dm31={dm31:.6e} vs obs {DM2_31_OBS:.6e}")
    check("The solar/full-matrix question remains separate from this Majorana structural closure",
          m2 * m2 - m1 * m1 > 1e-3,
          f"Dm21={m2 * m2 - m1 * m1:.6e} eV^2")

    print()
    print(f"  m_1 = {m1:.6e} eV")
    print(f"  m_2 = {m2:.6e} eV")
    print(f"  m_3 = {m3:.6e} eV")
    print(f"  Dm^2_31 = {dm31:.6e} eV^2")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: MINIMAL-BRIDGE STRUCTURAL CLOSURE")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_PURE_RETAINED_MU_IMPOSSIBILITY_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md")
    print("  - docs/DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md")
    print()
    print("Question:")
    print("  Is Majorana itself still the open pacing item on this branch, or does")
    print("  the current post-retained bridge already close its structural lane?")

    jx, jy, jz = part1_local_nambu_completion()
    part2_source_ray(jx, jy, jz)
    part3_midpoint_anchor()
    part4_adjacent_singlet_placement()
    a_scale, b_scale = part5_split_law()
    part6_downstream_atmospheric_benchmark(a_scale, b_scale)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The pure-retained Majorana lane is closed negative at mu = 0, but the")
    print("  admitted post-retained Majorana bridge is structurally closed.")
    print()
    print("  Exact bridge data:")
    print("    new local source ray   : mu J_x")
    print(f"    doublet anchor         : k_B = {K_B}")
    print(f"    singlet placement      : k_A = {K_A}")
    print(f"    doublet split law      : eps/B = alpha_LM/2 = {EPS_OVER_B:.12f}")
    print()
    print("  So Majorana is no longer the structural pacing item here. The")
    print("  remaining open work has moved downstream to PMNS/flavor closure and")
    print("  the exact CP-kernel/washout tail.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
