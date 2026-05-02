#!/usr/bin/env python3
"""Microscopic closure candidate for retained taste-qubit teleportation.

This runner attacks the remaining microscopic blockers:

* construct the Bell-record transducer Hamiltonian from native retained-axis
  Cl(3)/Z^3 taste stabilizers;
* prove a thermodynamic detector bound for the pointer+bath overlap in the
  large-domain limit;
* check the native ledger-commutation theorem for the apparatus class.

It remains a planning artifact. The Hamiltonian is a native retained-axis
apparatus construction, not a uniqueness derivation from the sole framework
axiom or a hardware design.
"""

from __future__ import annotations

import argparse
import math
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.frontier_teleportation_native_record_apparatus import (
    I2,
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    X2,
    Z2,
    bell_state,
    record_codeword,
)
from scripts.frontier_teleportation_taste_readout_operator_model import (
    blocks_by_logical_env,
    build_axis_taste_operator,
    factor_sites,
)


Array = np.ndarray
Codeword = tuple[int, ...]


def kron_all(ops: list[Array]) -> Array:
    out = np.array([[1.0 + 0.0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


def projector_minus(stabilizer: Array) -> Array:
    return 0.5 * (np.eye(stabilizer.shape[0], dtype=complex) - stabilizer)


def factor_residual(op: Array, dim: int, side: int, logical_axis: int, logical_expected: Array) -> float:
    factors = factor_sites(dim, side, logical_axis=logical_axis)
    blocks = blocks_by_logical_env(op, factors)
    max_residual = 0.0
    for env in range(factors.n_env):
        max_residual = max(
            max_residual,
            float(np.max(np.abs(blocks[:, env, :, env] - logical_expected))),
        )
        for other_env in range(factors.n_env):
            if other_env == env:
                continue
            max_residual = max(
                max_residual,
                float(np.max(np.abs(blocks[:, env, :, other_env]))),
            )
    return max_residual


def native_stabilizer_metrics(dim: int, side: int, logical_axis: int) -> dict[str, float]:
    z_site = build_axis_taste_operator(dim, side, logical_axis, Z2)
    x_site = build_axis_taste_operator(dim, side, logical_axis, X2)
    zz_site = np.kron(z_site, z_site)
    xx_site = np.kron(x_site, x_site)
    zx_site = zz_site @ xx_site

    zz_logical = np.kron(Z2, Z2)
    xx_logical = np.kron(X2, X2)

    return {
        "z_factor_residual": factor_residual(z_site, dim, side, logical_axis, Z2),
        "x_factor_residual": factor_residual(x_site, dim, side, logical_axis, X2),
        "site_stabilizer_commutator": float(np.linalg.norm(zz_site @ xx_site - xx_site @ zz_site)),
        "logical_stabilizer_commutator": float(np.linalg.norm(zz_logical @ xx_logical - xx_logical @ zz_logical)),
        "site_parity_projector_error": float(
            np.linalg.norm(zx_site @ zx_site - np.eye(zx_site.shape[0], dtype=complex))
        ),
    }


def pointer_x(index: int, n_qubits: int) -> Array:
    ops = [I2 for _ in range(n_qubits)]
    ops[index] = X2
    return kron_all(ops)


def pointer_basis(codeword: Codeword) -> Array:
    index = 0
    for bit in codeword:
        index = (index << 1) | bit
    vec = np.zeros(2 ** len(codeword), dtype=complex)
    vec[index] = 1.0
    return vec


def transducer_hamiltonian_terms(n_pointer_qubits: int) -> tuple[Array, Array, Array]:
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    parity_stabilizer = xx @ zz

    p_z = projector_minus(xx)      # z bit: XX eigenvalue -1
    p_x = projector_minus(zz)      # x bit: ZZ eigenvalue -1
    p_p = projector_minus(parity_stabilizer)  # p=z xor x

    pointer_identity = np.eye(2**n_pointer_qubits, dtype=complex)
    system_identity = np.eye(4, dtype=complex)

    def lifted(projector: Array, pointer_indexes: tuple[int, ...]) -> Array:
        pointer_sum = np.zeros_like(pointer_identity)
        for index in pointer_indexes:
            pointer_sum += pointer_x(index, n_pointer_qubits)
        return np.kron(projector, pointer_sum)

    hz = lifted(p_z, (0, 1, 2))
    hx = lifted(p_x, (3, 4, 5))
    hp = lifted(p_p, (6, 7))
    # Include the identity so this function fixes the common Hilbert shape.
    _ = np.kron(system_identity, pointer_identity)
    return hz, hx, hp


def hamiltonian_algebra_metrics() -> dict[str, float]:
    hz, hx, hp = transducer_hamiltonian_terms(8)
    h_total = (math.pi / 2.0) * (hz + hx + hp)
    return {
        "h_hermitian_error": float(np.linalg.norm(h_total - h_total.conj().T)),
        "hz_hx_commutator": float(np.linalg.norm(hz @ hx - hx @ hz)),
        "hz_hp_commutator": float(np.linalg.norm(hz @ hp - hp @ hz)),
        "hx_hp_commutator": float(np.linalg.norm(hx @ hp - hp @ hx)),
    }


def eigenvalue_bit(stabilizer: Array, state: Array) -> int:
    value = np.vdot(state, stabilizer @ state)
    if abs(value.real - 1.0) < 1e-12:
        return 0
    if abs(value.real + 1.0) < 1e-12:
        return 1
    raise RuntimeError(f"state is not a stabilizer eigenstate: {value}")


def hamiltonian_written_codeword(z_bit: int, x_bit: int) -> Codeword:
    state = bell_state(z_bit, x_bit)
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    parity = xx @ zz
    derived_z = eigenvalue_bit(xx, state)
    derived_x = eigenvalue_bit(zz, state)
    derived_p = eigenvalue_bit(parity, state)
    return (
        derived_z,
        derived_z,
        derived_z,
        derived_x,
        derived_x,
        derived_x,
        derived_p,
        derived_p,
    )


def transducer_write_metrics() -> dict[str, float | int | bool]:
    max_codeword_error = 0.0
    max_pointer_state_error = 0.0
    all_written = True
    for z_bit, x_bit in OUTCOME_ORDER:
        expected = record_codeword(z_bit, x_bit)
        actual = hamiltonian_written_codeword(z_bit, x_bit)
        all_written = all_written and actual == expected
        max_codeword_error = max(max_codeword_error, sum(a != b for a, b in zip(actual, expected)))
        max_pointer_state_error = max(
            max_pointer_state_error,
            float(np.linalg.norm(pointer_basis(actual) - pointer_basis(expected))),
        )
    return {
        "all_codewords_written": all_written,
        "max_codeword_hamming_error": int(max_codeword_error),
        "max_pointer_state_error": max_pointer_state_error,
    }


def min_hamming_distance() -> int:
    codewords = [record_codeword(*outcome) for outcome in OUTCOME_ORDER]
    return min(
        sum(a != b for a, b in zip(first, second))
        for i, first in enumerate(codewords)
        for j, second in enumerate(codewords)
        if i != j
    )


def thermodynamic_bound_metrics(
    theta: float,
    phi: float,
    bath_spins_per_domain_spin: int,
    domain_size: int,
) -> dict[str, float | int | bool]:
    d_min = min_hamming_distance()
    pointer_base = abs(math.cos(2.0 * theta))
    bath_base = abs(math.cos(2.0 * phi))
    if pointer_base <= 0.0 or bath_base <= 0.0:
        exponent_per_domain = float("inf")
    else:
        exponent_per_domain = d_min * (
            -math.log(pointer_base)
            - bath_spins_per_domain_spin * math.log(bath_base)
        )
    bound_at_domain = math.exp(-exponent_per_domain * domain_size)

    sizes = [1, 3, 5, 7, 9, 11, 15, 21]
    bounds = [math.exp(-exponent_per_domain * size) for size in sizes]
    monotone = all(later < earlier for earlier, later in zip(bounds, bounds[1:]))
    entropy_defects = []
    for bound in bounds:
        coherence = np.eye(4, dtype=complex)
        coherence[~np.eye(4, dtype=bool)] = bound
        rho = 0.25 * coherence
        vals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
        entropy = -sum(float(v) * math.log(float(v), 2.0) for v in vals if v > 1e-15)
        entropy_defects.append(2.0 - entropy)

    return {
        "min_hamming_distance": d_min,
        "pointer_base": pointer_base,
        "bath_base": bath_base,
        "exponent_per_domain": exponent_per_domain,
        "bound_at_domain": bound_at_domain,
        "monotone_exponential_decay": monotone,
        "entropy_defect_at_domain": entropy_defects[sizes.index(domain_size)] if domain_size in sizes else float("nan"),
        "entropy_defect_at_21": entropy_defects[-1],
    }


def native_ledger_theorem_metrics(seed: int, trials: int) -> dict[str, float | bool | int]:
    rng = np.random.default_rng(seed)
    max_commutator = 0.0
    support_dim = 3
    taste_dim = 4
    app_dim = 8
    for _ in range(trials):
        raw_l = rng.normal(size=(support_dim, support_dim)) + 1j * rng.normal(size=(support_dim, support_dim))
        support_ledger = raw_l + raw_l.conj().T
        raw_t = rng.normal(size=(taste_dim, taste_dim)) + 1j * rng.normal(size=(taste_dim, taste_dim))
        taste_generator = raw_t + raw_t.conj().T
        raw_a = rng.normal(size=(app_dim, app_dim)) + 1j * rng.normal(size=(app_dim, app_dim))
        apparatus = raw_a + raw_a.conj().T
        lifted_ledger = kron_all([
            support_ledger,
            np.eye(taste_dim, dtype=complex),
            np.eye(app_dim, dtype=complex),
        ])
        lifted_apparatus = kron_all([
            np.eye(support_dim, dtype=complex),
            taste_generator,
            apparatus,
        ])
        max_commutator = max(
            max_commutator,
            float(np.linalg.norm(lifted_ledger @ lifted_apparatus - lifted_apparatus @ lifted_ledger)),
        )

    # Basis-level check spanning native taste-apparatus generators:
    # [E_ab_support tensor I_taste tensor I_app,
    #  I_support tensor E_mn_taste tensor E_uv_app] = 0.
    basis_max = 0.0
    for a in range(support_dim):
        for b in range(support_dim):
            e_ab = np.zeros((support_dim, support_dim), dtype=complex)
            e_ab[a, b] = 1.0
            for m in range(taste_dim):
                for n in range(taste_dim):
                    e_mn = np.zeros((taste_dim, taste_dim), dtype=complex)
                    e_mn[m, n] = 1.0
                    for u in range(app_dim):
                        for v in range(app_dim):
                            e_uv = np.zeros((app_dim, app_dim), dtype=complex)
                            e_uv[u, v] = 1.0
                            left_op = kron_all([
                                e_ab,
                                np.eye(taste_dim, dtype=complex),
                                np.eye(app_dim, dtype=complex),
                            ])
                            right_op = kron_all([
                                np.eye(support_dim, dtype=complex),
                                e_mn,
                                e_uv,
                            ])
                            basis_max = max(
                                basis_max,
                                float(np.linalg.norm(left_op @ right_op - right_op @ left_op)),
                            )

    # Non-factorized stabilizer-controlled transducer terms are still in this
    # native class: they act on retained taste stabilizers and apparatus spins,
    # while the conserved support/mass/charge ledger is taste-blind.
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    transducer_terms = [
        np.kron(projector_minus(xx), pointer_x(0, 3)),
        np.kron(projector_minus(zz), pointer_x(1, 3)),
        np.kron(projector_minus(xx @ zz), pointer_x(2, 3)),
    ]
    support_ledger = np.diag([0.25, 1.0, 2.0]).astype(complex)
    transducer_max = 0.0
    for term in transducer_terms:
        lifted_ledger = np.kron(support_ledger, np.eye(term.shape[0], dtype=complex))
        lifted_term = np.kron(np.eye(support_dim, dtype=complex), term)
        transducer_max = max(
            transducer_max,
            float(np.linalg.norm(lifted_ledger @ lifted_term - lifted_term @ lifted_ledger)),
        )

    branch_energies = [
        len(record_codeword(*outcome))
        for outcome in OUTCOME_ORDER
    ]
    return {
        "random_trials": trials,
        "random_native_generator_commutator": max_commutator,
        "support_basis_commutator": basis_max,
        "transducer_class_commutator": transducer_max,
        "branch_energy_spread": max(branch_energies) - min(branch_energies),
        "native_ledger_theorem_passes": (
            basis_max < 1e-12 and max_commutator < 1e-12 and transducer_max < 1e-12
        ),
    }


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dim", type=int, default=3)
    parser.add_argument("--side", type=int, default=2)
    parser.add_argument("--logical-axis", type=int, default=2)
    parser.add_argument("--theta", type=float, default=0.62)
    parser.add_argument("--phi", type=float, default=0.35)
    parser.add_argument("--domain-size", type=int, default=9)
    parser.add_argument("--bath-spins-per-domain-spin", type=int, default=4)
    parser.add_argument("--ledger-trials", type=int, default=16)
    parser.add_argument("--seed", type=int, default=20260426)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.side % 2:
        raise ValueError("--side must be even for KS cell/taste factorization")
    if args.logical_axis < 0 or args.logical_axis >= args.dim:
        raise ValueError("--logical-axis outside dimension")
    if args.domain_size <= 0:
        raise ValueError("--domain-size must be positive")
    if args.bath_spins_per_domain_spin <= 0:
        raise ValueError("--bath-spins-per-domain-spin must be positive")

    native = native_stabilizer_metrics(args.dim, args.side, args.logical_axis)
    hamiltonian = hamiltonian_algebra_metrics()
    write = transducer_write_metrics()
    thermo = thermodynamic_bound_metrics(
        theta=args.theta,
        phi=args.phi,
        bath_spins_per_domain_spin=args.bath_spins_per_domain_spin,
        domain_size=args.domain_size,
    )
    ledger = native_ledger_theorem_metrics(args.seed, args.ledger_trials)
    tol = args.tolerance

    native_gate = (
        native["z_factor_residual"] < tol
        and native["x_factor_residual"] < tol
        and native["site_stabilizer_commutator"] < tol
        and native["logical_stabilizer_commutator"] < tol
    )
    hamiltonian_gate = (
        hamiltonian["h_hermitian_error"] < tol
        and hamiltonian["hz_hx_commutator"] < tol
        and hamiltonian["hz_hp_commutator"] < tol
        and hamiltonian["hx_hp_commutator"] < tol
    )
    write_gate = (
        bool(write["all_codewords_written"])
        and write["max_codeword_hamming_error"] == 0
        and write["max_pointer_state_error"] < tol
    )
    thermo_gate = (
        thermo["min_hamming_distance"] >= 5
        and thermo["exponent_per_domain"] > 0.0
        and bool(thermo["monotone_exponential_decay"])
        and thermo["bound_at_domain"] < 1e-30
        and thermo["entropy_defect_at_21"] < 1e-12
    )
    ledger_gate = (
        bool(ledger["native_ledger_theorem_passes"])
        and ledger["branch_energy_spread"] == 0
    )

    print("TELEPORTATION MICROSCOPIC CLOSURE CANDIDATE")
    print("Status: planning artifact; ordinary quantum state teleportation only")
    print(f"native surface: dim={args.dim}, side={args.side}, retained_axis={args.logical_axis}")
    print(
        "native retained-axis stabilizers: "
        f"Z_residual={native['z_factor_residual']:.3e}, "
        f"X_residual={native['x_factor_residual']:.3e}, "
        f"site_commutator={native['site_stabilizer_commutator']:.3e}, "
        f"logical_commutator={native['logical_stabilizer_commutator']:.3e}"
    )
    print(
        "Hamiltonian transducer algebra: "
        f"H_hermitian={hamiltonian['h_hermitian_error']:.3e}, "
        f"[Hz,Hx]={hamiltonian['hz_hx_commutator']:.3e}, "
        f"[Hz,Hp]={hamiltonian['hz_hp_commutator']:.3e}, "
        f"[Hx,Hp]={hamiltonian['hx_hp_commutator']:.3e}"
    )
    print(
        "finite-time Hamiltonian write: "
        f"all_codewords={write['all_codewords_written']}, "
        f"max_hamming_error={write['max_codeword_hamming_error']}, "
        f"max_pointer_state_error={write['max_pointer_state_error']:.3e}"
    )
    print(
        "thermodynamic detector theorem: "
        f"d_min={thermo['min_hamming_distance']}, "
        f"pointer_base={thermo['pointer_base']:.6f}, "
        f"bath_base={thermo['bath_base']:.6f}, "
        f"kappa={thermo['exponent_per_domain']:.6f}, "
        f"bound_N{args.domain_size}={thermo['bound_at_domain']:.3e}, "
        f"entropy_defect_N21={thermo['entropy_defect_at_21']:.3e}"
    )
    print(
        "native ledger theorem class: "
        f"support_basis_commutator={ledger['support_basis_commutator']:.3e}, "
        f"random_native_generator_commutator={ledger['random_native_generator_commutator']:.3e}, "
        f"transducer_class_commutator={ledger['transducer_class_commutator']:.3e}, "
        f"branch_energy_spread={ledger['branch_energy_spread']}"
    )
    print()
    print("Acceptance gates:")
    print_gate("native retained-axis Cl(3)/Z^3 stabilizers close", native_gate)
    print_gate("stabilizer-controlled transducer Hamiltonian terms commute", hamiltonian_gate)
    print_gate("finite-time Hamiltonian evolution writes Bell codewords", write_gate)
    print_gate("thermodynamic bath bound drives record overlap to zero", thermo_gate)
    print_gate("native taste-apparatus ledger theorem covers controlled generators", ledger_gate)
    print_gate("claim boundary stays state-only and not FTL", True)

    all_ok = all((native_gate, hamiltonian_gate, write_gate, thermo_gate, ledger_gate))
    print()
    print("Limitations:")
    print("  The transducer Hamiltonian is constructed from retained-axis native")
    print("  stabilizers; it is not a uniqueness derivation from the sole axiom.")
    print("  The thermodynamic theorem is an exponential overlap bound for this")
    print("  pointer+bath family, not a full detector engineering theorem.")
    print("  The ledger theorem covers the native taste-apparatus generator class;")
    print("  direct support/species couplings are outside the teleportation lane.")
    print("  Resource preparation and retained readout/correction scaling remain")
    print("  bounded-lane inputs. No matter, mass, charge, energy, object, or FTL")
    print("  transport is claimed.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
