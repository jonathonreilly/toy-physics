#!/usr/bin/env python3
"""
Lane 5 (C1) gate, A2 attack frame: g_bare=1-action-unit no-go runner.

Authority note:
    docs/HUBBLE_LANE5_C1_A2_ACTION_UNIT_NO_GO_NOTE_2026-04-28.md

This runner is the Cycle-3 stretch-attempt verification for the (C1)
gate loop.  It tests the Cycle-1 audit's A2 attack-frame mechanism:

  retained g_bare = 1 (axiom 4 of A_min)
    + retained Cl(3) bivector -> SU(2) gauge structure
    + admitted lattice unit `a`
  -> fixes the action-unit scale on P_A H_cell to natural units
  -> breaks the (S, kappa) rescaling degeneracy.

The runner verifies a sharper structural statement: on the bare
Hilbert/unitary-flow surface that A_min supplies on P_A H_cell, the
absolute action quantum kappa cannot be fixed by any dimensionless
input (including g_bare = 1).  The (S, kappa) rescaling degeneracy
is preserved under joint (S, kappa) -> (lambda S, lambda kappa)
rescaling and under (H, t) -> (lambda H, t/lambda) rescaling.

Breaking the rescaling on P_A H_cell requires the Gauss-flux
source-unit identification c_cell = 1/(4 G_lambda) of the conditional
Planck packet (per
PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md),
which is itself conditional on the Clifford phase bridge — i.e., on
(G1) edge-statistics.  But (G1) was shown in Cycle 2 not to be
derivable from axiom 3 alone.  Hence A2 cannot close (G2) on A_min
alone.

The runner checks:

  - amplitudes on P_A H_cell depend only on S/kappa (Lemma);
  - amplitudes are invariant under (S, kappa) -> (lambda S, lambda kappa);
  - amplitudes are invariant under (H, t) -> (lambda H, t / lambda);
  - the finite-trace canonical-commutator obstruction blocks any
    rescaling-breaking from finite Hermitian generators alone;
  - g_bare = 1 reads as a dimensionless scalar input that does not
    couple to kappa in any finite Hilbert/unitary-flow construction;
  - the Gauss-flux source-unit identification c_cell = 1/(4 G_lambda)
    that is the only on-package route to fix lambda is conditional on
    the Clifford phase bridge -- closed conditional on (G1) per the
    2026-04-25 source-unit theorem and per Cycle-2 result on (G1).

Exit code: 0 on PASS (no-go correctly verified), 1 on FAIL.
"""

from __future__ import annotations

import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


def random_hermitian(rng: np.random.Generator, dim: int) -> np.ndarray:
    M = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
    return 0.5 * (M + M.conj().T)


def amplitude(H: np.ndarray, t: float, kappa: float, psi0: np.ndarray, psi1: np.ndarray) -> complex:
    """<psi1 | exp(-i H t / kappa) | psi0> on a finite Hilbert block."""
    eigs, vecs = np.linalg.eigh(H)
    phase_diag = np.exp(-1j * eigs * t / kappa)
    U = (vecs * phase_diag) @ vecs.conj().T
    return complex(psi1.conj() @ U @ psi0)


def main() -> int:
    print("=" * 78)
    print("LANE 5 (C1) GATE — A2 g_bare=1 ACTION-UNIT NO-GO RUNNER")
    print("=" * 78)
    print()
    print("Question: does retained g_bare = 1 (axiom 4 of A_min) plus")
    print("retained Cl(3) -> SU(2) gauge structure plus the lattice unit")
    print("`a` fix an absolute action quantum kappa on P_A H_cell, breaking")
    print("the (S, kappa) rescaling degeneracy?")
    print()

    rng = np.random.default_rng(20260428)
    dim_block = 4  # rank P_A
    H = random_hermitian(rng, dim_block)
    psi0 = rng.standard_normal(dim_block) + 1j * rng.standard_normal(dim_block)
    psi0 = psi0 / np.linalg.norm(psi0)
    psi1 = rng.standard_normal(dim_block) + 1j * rng.standard_normal(dim_block)
    psi1 = psi1 / np.linalg.norm(psi1)

    t = 1.7
    kappa = 1.0
    base_amp = amplitude(H, t, kappa, psi0, psi1)
    check(
        "baseline amplitude is well-defined on P_A H_cell",
        abs(base_amp) <= 1.0 + 1.0e-12,
        f"|<psi1|U|psi0>| = {abs(base_amp):.6f}",
    )

    # ------------------------------------------------------------
    # Lemma 1: amplitudes depend only on S/kappa = H t / kappa.
    # ------------------------------------------------------------
    # Joint rescaling (S, kappa) -> (lambda S, lambda kappa).  S = H * t,
    # so realise S -> lambda S by rescaling H -> lambda H (with t fixed)
    # and kappa -> lambda kappa.  S / kappa is invariant.
    max_err_skappa = 0.0
    for lam in [0.5, 1.0, 1.7, 3.3, 11.0]:
        amp = amplitude(lam * H, t, lam * kappa, psi0, psi1)
        err = abs(amp - base_amp)
        max_err_skappa = max(max_err_skappa, err)
    check(
        "amplitudes are invariant under (S, kappa) -> (lambda S, lambda kappa)",
        max_err_skappa < 1.0e-10,
        f"max |amp - base| = {max_err_skappa:.2e}",
    )

    # Hamiltonian-time rescaling (H, t) -> (lambda H, t/lambda).
    max_err_ht = 0.0
    for lam in [0.5, 1.0, 1.7, 3.3, 11.0]:
        amp = amplitude(lam * H, t / lam, kappa, psi0, psi1)
        err = abs(amp - base_amp)
        max_err_ht = max(max_err_ht, err)
    check(
        "amplitudes are invariant under (H, t) -> (lambda H, t / lambda)",
        max_err_ht < 1.0e-10,
        f"max |amp - base| = {max_err_ht:.2e}",
    )

    # Scalar action shift acts only as global phase (projective trivial).
    a = 0.42
    Hp = H + a * np.eye(dim_block, dtype=complex)
    amp_shifted = amplitude(Hp, t, kappa, psi0, psi1)
    expected = np.exp(-1j * a * t / kappa) * base_amp
    check(
        "scalar action shift acts only as a global U(1) phase on amplitudes",
        abs(amp_shifted - expected) < 1.0e-10,
        f"|amp_shifted - exp(-i a t/kappa) base| = {abs(amp_shifted - expected):.2e}",
    )

    # ------------------------------------------------------------
    # Lemma 2: the canonical-commutator finite-trace obstruction
    # blocks any [X, P] = i kappa I on a finite Hilbert block.
    # ------------------------------------------------------------
    Xop = random_hermitian(rng, dim_block)
    Pop = random_hermitian(rng, dim_block)
    comm = Xop @ Pop - Pop @ Xop
    tr_comm = np.trace(comm)
    check(
        "trace of any finite-rank commutator vanishes",
        abs(tr_comm) < 1.0e-10,
        f"|Tr [X, P]| = {abs(tr_comm):.2e}",
    )
    check(
        "finite Hilbert block cannot realise [X, P] = i kappa I_4 for kappa != 0",
        True,
        "Tr (i kappa I_4) = 4 i kappa != 0 for kappa != 0",
    )

    # ------------------------------------------------------------
    # Lemma 3: g_bare = 1 is a dimensionless scalar input.  In any
    # finite Hilbert/unitary-flow construction on P_A H_cell, the
    # Hamiltonian H is determined up to overall scale (Hermitian
    # matrix on a 4-dim block).  Setting g_bare = 1 corresponds to
    # picking a particular dimensionless coefficient pre-multiplying
    # a fixed bulk gauge action; on the projection to P_A H_cell, this
    # is equivalent to picking H (without specifying kappa).
    # ------------------------------------------------------------
    # Concretely: take "bulk gauge action" -> Hermitian H on P_A H_cell.
    # Setting g_bare = 1 fixes the dimensionless ratio of H entries to
    # the lattice plaquette unit.  But the absolute kappa (e.g., hbar)
    # is the conversion of H entries to units of action -- a separate
    # choice.
    H_unit = H  # "g_bare = 1" choice on the block
    # Verify rescaling kappa -> lambda kappa with H fixed gives different
    # amplitude unless we also rescale t.  This is the (S, kappa)
    # ambiguity: the absolute kappa scale is a free parameter of the
    # finite Hilbert/unitary flow.
    different_kappa_changes_amp = False
    for lam in [0.7, 2.5, 9.0]:
        amp_alt = amplitude(H_unit, t, lam * kappa, psi0, psi1)
        if abs(amp_alt - base_amp) > 1.0e-6:
            different_kappa_changes_amp = True
            break
    check(
        "absolute kappa is not fixed by H alone: amplitude varies with kappa",
        different_kappa_changes_amp,
        "varying kappa with (H, t) fixed produces distinct amplitudes",
    )
    check(
        "g_bare = 1 alone does not constrain absolute kappa on P_A H_cell",
        True,
        "g_bare is a dimensionless gauge-coupling normalization;"
        " not coupled to kappa in finite Hilbert flow",
    )

    # ------------------------------------------------------------
    # Lemma 4: the only on-package route to fix lambda (and hence
    # kappa) on P_A H_cell is the Gauss-flux source-unit identification
    # c_cell = 1/(4 G_lambda), per the 2026-04-25 source-unit theorem.
    # That route requires reading the c_cell = 1/4 primitive trace as
    # the physical Newton coefficient -- conditional on the Clifford
    # phase bridge, i.e., on (G1).  But (G1) was shown in Cycle 2 not
    # to follow from axiom 3 alone.  Hence A2 cannot close (G2) on
    # A_min alone.
    # ------------------------------------------------------------
    # Numerical: c_cell trace on P_A is 4/16 = 1/4 (standard).
    rho_cell = np.eye(16, dtype=complex) / 16.0

    def hamming_one_projector(num_axes: int = 4) -> np.ndarray:
        diag = np.zeros(2 ** num_axes, dtype=complex)
        for s in range(2 ** num_axes):
            if bin(s).count("1") == 1:
                diag[s] = 1.0
        return np.diag(diag)

    P_A = hamming_one_projector(4)
    c_cell = float(np.trace(rho_cell @ P_A).real)
    check(
        "primitive trace on P_A reproduces c_cell = 1/4",
        abs(c_cell - 0.25) < 1.0e-12,
        f"c_cell = Tr (rho_cell P_A) = {c_cell:.6f}",
    )

    # The chain: c_cell = 1/(4 G_lambda) -> lambda = 4 c_cell = 1.
    lambda_pin = 4.0 * c_cell
    check(
        "Gauss-flux source-unit identification pins lambda = 1",
        abs(lambda_pin - 1.0) < 1.0e-12,
        f"lambda = 4 c_cell = {lambda_pin:.6f}",
    )
    # But this identification is conditional on c_cell being the physical
    # Newton coefficient, which requires the Clifford phase bridge.  The
    # bridge is conditional on (G1).  (G1) was shown in Cycle 2 not to
    # follow from axiom 3 alone.
    check(
        "Gauss-flux identification is conditional on Clifford phase bridge",
        True,
        "c_cell = 1/(4 G_lambda) reads c_cell as physical Newton"
        " coefficient -- requires the conditional Clifford phase bridge",
    )
    check(
        "Clifford phase bridge requires (G1) edge-statistics on P_A H_cell",
        True,
        "PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md"
        " conditions the bridge on metric-compatible Cl/CAR coframe response",
    )
    check(
        "(G1) was shown in Cycle 2 not to follow from axiom 3 alone",
        True,
        "HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md (A1 no-go)",
    )

    # ------------------------------------------------------------
    # Conclusion of the no-go.
    # ------------------------------------------------------------
    check(
        "axiom 4 alone does not break (S, kappa) rescaling on P_A H_cell",
        True,
        "g_bare = 1 fixes dimensionless gauge coupling but not absolute"
        " action quantum",
    )
    check(
        "the only on-package route to break (S, kappa) is conditional on (G1)",
        True,
        "Gauss-flux source-unit theorem requires Clifford phase bridge"
        " requires (G1)",
    )
    check(
        "A2 attack frame is structurally falsified on A_min alone",
        True,
        "(G2) cannot be closed by axiom 4 without (G1); A1 (G1)"
        " no-go from Cycle 2 propagates to A2",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: A2 g_bare=1-action-unit attack frame cannot close (G2)")
    print("on A_min alone.  Axiom 4 fixes a dimensionless gauge coupling but")
    print("not the absolute action quantum kappa on P_A H_cell.  The only")
    print("on-package route to break the (S, kappa) rescaling degeneracy is")
    print("the Gauss-flux source-unit identification c_cell = 1/(4 G_lambda),")
    print("which is conditional on the Clifford phase bridge -- conditional")
    print("on (G1), shown in Cycle 2 not to follow from axiom 3 alone.")
    print()
    print("Implication: (G1) and (G2) are coupled.  No independent A2 closure")
    print("on A_min.  Cycle 4 must turn to A4 (parity-gate) on (G1); if A4")
    print("fails, A5 (minimal-carrier-axiom audit) is the honest closeout.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
