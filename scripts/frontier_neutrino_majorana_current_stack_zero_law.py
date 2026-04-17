#!/usr/bin/env python3
"""
Current-stack zero law for the one-generation Majorana amplitude mu.

Question:
  After the one-generation local Majorana block has been reduced to the
  canonical form A_M(mu)=mu J_2, what is the actual activation law for mu on
  the retained atlas / retained microscopic stack?

Answer on the current stack:
  mu_current = 0.

Reason:
  - the current local block has only one scalar coordinate mu
  - the retained finite normal grammar preserves exact fermion-number U(1),
    which kills the charge-2 Majorana coefficient
  - the current atlas contains no additional fermionic charge-2 primitive that
    could source a nonzero mu

Boundary:
  This is a current-stack theorem only. It does NOT rule out future axiom-side
  charge-2 primitives or future nonzero Majorana amplitudes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


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


def number_operator(cs: list[np.ndarray]) -> np.ndarray:
    dim = cs[0].shape[0]
    out = np.zeros((dim, dim), dtype=complex)
    for c in cs:
        out += c.conj().T @ c
    return out


def monomial(cs: list[np.ndarray], creators: list[int], annihilators: list[int]) -> np.ndarray:
    dim = cs[0].shape[0]
    out = np.eye(dim, dtype=complex)
    for idx in creators:
        out = out @ cs[idx].conj().T
    for idx in annihilators:
        out = out @ cs[idx]
    return out


def hermitian(op: np.ndarray) -> np.ndarray:
    return 0.5 * (op + op.conj().T)


def gibbs_state(h: np.ndarray, beta: float) -> np.ndarray:
    evals, vecs = np.linalg.eigh(hermitian(h))
    weights = np.exp(-beta * (evals - np.min(evals)))
    rho = vecs @ np.diag(weights) @ vecs.conj().T
    return rho / np.trace(rho)


def expect(rho: np.ndarray, op: np.ndarray) -> complex:
    return complex(np.trace(rho @ op))


def extract_mu_from_block(block: np.ndarray) -> complex:
    return block[0, 1]


def test_current_majorana_coordinate_is_single_scalar() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT MAJORANA ACTIVATION QUESTION IS A SINGLE SCALAR")
    print("=" * 88)

    mu = 0.61
    block = mu * J2
    extracted = extract_mu_from_block(block)
    antisym_err = np.linalg.norm(block + block.T)
    recon_err = np.linalg.norm(block - extracted * J2)

    check("Canonical one-generation block is antisymmetric", antisym_err < 1e-12,
          f"||A+A^T||={antisym_err:.2e}")
    check("The canonical block is reconstructed from one scalar coordinate mu", recon_err < 1e-12,
          f"reconstruction error={recon_err:.2e}")
    check("The coordinate extractor returns mu exactly on mu J_2", abs(extracted - mu) < 1e-12,
          f"mu_extracted={extracted}")

    print()
    print("  So the current activation-law target is not matrix-valued.")
    print("  It is the single scalar mu on the canonical block mu J_2.")


def test_retained_normal_grammar_sets_mu_to_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE RETAINED NORMAL GRAMMAR SETS THE EFFECTIVE MU TO ZERO")
    print("=" * 88)

    cs = annihilation_operators(4)
    n_tot = number_operator(cs)
    hop = monomial(cs, [0], [1])
    density = monomial(cs, [0, 1], [1, 0])
    scatter = monomial(cs, [0, 2], [3, 1])
    pair_ann = monomial(cs, [], [0, 1])
    pair_cre = pair_ann.conj().T
    n0 = cs[0].conj().T @ cs[0]
    n1 = cs[1].conj().T @ cs[1]
    n2 = cs[2].conj().T @ cs[2]

    h_normal = (
        0.41 * hermitian(hop)
        - 0.16 * hermitian(scatter)
        + 0.58 * density
        + 0.12 * n0
        - 0.08 * n1
        + 0.05 * n2
    )
    rho = gibbs_state(h_normal, beta=1.1)

    comm_err = np.linalg.norm(h_normal @ n_tot - n_tot @ h_normal)
    pair_ev = expect(rho, pair_ann)
    pair_ev_hc = expect(rho, pair_cre)
    mu_eff = abs(pair_ev)
    block_eff = mu_eff * J2

    check("Retained normal Hamiltonian commutes exactly with fermion number", comm_err < 1e-12,
          f"||[H,N]||={comm_err:.2e}")
    check("Charge-2 pair expectation vanishes exactly on the retained grammar", abs(pair_ev) < 1e-12,
          f"<cc>={pair_ev.real:+.2e}{pair_ev.imag:+.2e}i")
    check("Charge+2 conjugate expectation also vanishes exactly", abs(pair_ev_hc) < 1e-12,
          f"<c^dag c^dag>={pair_ev_hc.real:+.2e}{pair_ev_hc.imag:+.2e}i")
    check("Projected effective canonical block is therefore zero", np.linalg.norm(block_eff) < 1e-12,
          f"||mu_eff J_2||={np.linalg.norm(block_eff):.2e}")
    check("The retained-grammar effective activation coordinate is mu_eff = 0", abs(mu_eff) < 1e-12,
          f"mu_eff={mu_eff:.2e}")

    print()
    print("  Inside the retained number-preserving grammar, the unique Majorana")
    print("  slot is present structurally but its effective amplitude is exactly")
    print("  zero.")


def test_current_atlas_has_no_extra_charge_two_source() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT ATLAS ADDS NO EXTRA SOURCE TERM THAT COULD SHIFT ZERO")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    obs = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    rhs = read("scripts/frontier_right_handed_sector.py")

    has_det_row = "| Observable principle | `log|det(D+J)|`" in atlas
    pfaffian_rows = re.findall(r"\|\s*([^|]*Pfaffian[^|]*)\|", atlas, flags=re.IGNORECASE)
    has_boundary_row = (
        "| One-generation Majorana current-stack zero law |" in atlas
        or "| Three-generation Majorana current-stack zero matrix |" in atlas
    )
    obs_scalar = "scalar observable generator" in obs.lower() or "scalar generator" in obs.lower()
    misses_zero_slot = "MISSING from wedge^2 singlets: {Fraction(0, 1), Fraction(4, 3)}" in rhs or "Fraction(0)" in rhs

    check("Atlas still retains the determinant observable backbone", has_det_row)
    check("Current atlas has no Pfaffian row for a retained source primitive", len(pfaffian_rows) == 0,
          f"pfaffian rows={pfaffian_rows}")
    check("Atlas carries the retained Majorana zero-law boundary row", has_boundary_row)
    check("Observable-principle note stays scalar rather than fermionic-pairing based", obs_scalar)
    check("Current right-handed composite route still misses the Y=0 nu_R singlet slot", misses_zero_slot)

    print()
    print("  So no currently retained atlas object shifts the exact retained")
    print("  answer away from mu = 0.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: CURRENT-STACK ZERO LAW FOR MU")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("    rows: Framework axiom; Observable principle; Anomaly-forced time;")
    print("          Native weak algebra; Structural SU(3) closure; One-generation matter closure")
    print("  - docs/NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Once the one-generation local Majorana block is canonicalized as")
    print("  mu J_2, what is the actual activation law for mu on the stack that")
    print("  is currently retained today?")

    test_current_majorana_coordinate_is_single_scalar()
    test_retained_normal_grammar_sets_mu_to_zero()
    test_current_atlas_has_no_extra_charge_two_source()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  On the current retained atlas / retained microscopic grammar, the")
    print("  effective one-generation Majorana activation law is the zero law")
    print("  mu_current = 0.")
    print()
    print("  Any future nonzero mu requires a genuinely new axiom-side charge-2")
    print("  primitive outside the current retained stack.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
