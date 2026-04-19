"""
Frontier runner - Koide / Z_3 Joint Projector Identity.

Companion to `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`.

Certifies the structural identity on C^3:

    Pi_Z3_singlet  ==  Pi_triv                           (I)
    Pi_Z3_doublet  ==  Pi_om + Pi_ombar  ==  I - Pi_triv (II)

where

    C          = regular 3-cycle e_i -> e_{i+1 mod 3}
    omega      = exp(2 pi i / 3)
    Pi_triv    = v_triv v_triv^dag, v_triv = (1,1,1)/sqrt(3)
    Pi_om      = v_om v_om^dag,     v_om   = (1, omega, omega^2)/sqrt(3)
    Pi_ombar   = v_ombar v_ombar^dag, v_ombar = (1, omega^2, omega)/sqrt(3)
    Pi_Z3_*    = U_Z3 diag(...) U_Z3^dag with U_Z3 = DFT_3.

Consequence: the charged-lepton Koide lane and the DM neutrino
source-surface lane inherit one and the same C_3 isotypic
decomposition of C^3. The CKM ray sqrt(1/6) + i sqrt(5/6) is a
separate rank-1 direction with no distinguished alignment.

All numerical checks at machine precision.
"""

from __future__ import annotations

import math
import sys

import numpy as np


# ---------------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ---------------------------------------------------------------------------

PASS = 0
FAIL = 0


def check(label, cond, detail=""):
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{status}] {label}" + (f"  ({detail})" if detail else ""))


np.set_printoptions(precision=6, suppress=True, linewidth=160)


# ---------------------------------------------------------------------------
# Section 1 - Regular 3-cycle C and its C_3 eigenvectors on C^3
# ---------------------------------------------------------------------------

print("=" * 72)
print("Section 1 - C_3 isotypic decomposition on C^3")
print("=" * 72)

OMEGA = np.exp(2j * np.pi / 3)
I3 = np.eye(3, dtype=complex)

# Regular 3-cycle.
C = np.array(
    [[0, 0, 1],
     [1, 0, 0],
     [0, 1, 0]],
    dtype=complex,
)
C2 = C @ C

check("C^3 == I on C^3", np.linalg.norm(C @ C2 - I3) < 1e-14)
check("Tr(C) == 0", abs(np.trace(C)) < 1e-14)
check("Tr(C^2) == 0", abs(np.trace(C2)) < 1e-14)

# C_3 eigenvectors (columns of DFT_3). Labels chosen so that
#   C v_lam = lam v_lam.  With the chosen C (left-shift e_i -> e_{i+1 mod 3}),
#   v_om  = (1, omega^*, omega)/sqrt(3)    has eigenvalue omega,
#   v_ombar = (1, omega, omega^*)/sqrt(3)   has eigenvalue omega^*.
v_triv = np.array([1, 1, 1], dtype=complex) / math.sqrt(3)
v_om = np.array([1, np.conjugate(OMEGA), OMEGA], dtype=complex) / math.sqrt(3)
v_ombar = np.array([1, OMEGA, np.conjugate(OMEGA)], dtype=complex) / math.sqrt(3)

check(
    "C v_triv  = 1   * v_triv",
    np.linalg.norm(C @ v_triv - 1 * v_triv) < 1e-14,
)
check(
    "C v_om    = omega * v_om",
    np.linalg.norm(C @ v_om - OMEGA * v_om) < 1e-14,
)
check(
    "C v_ombar = omega^* v_ombar",
    np.linalg.norm(C @ v_ombar - np.conjugate(OMEGA) * v_ombar) < 1e-14,
)


def outer(v):
    return np.outer(v, np.conjugate(v))


Pi_triv = outer(v_triv)
Pi_om = outer(v_om)
Pi_ombar = outer(v_ombar)


def projector_invariants(name, P, rank_expected):
    herm = np.linalg.norm(P - P.conjugate().T)
    idemp = np.linalg.norm(P @ P - P)
    tr = np.trace(P).real
    r = int(np.round(tr))
    print(f"   {name}: ||P-P^dag||={herm:.2e}, ||P^2-P||={idemp:.2e}, "
          f"Tr={tr:.6f}, rank={r}")
    return herm < 1e-13, idemp < 1e-13, r == rank_expected, abs(tr - rank_expected) < 1e-12


for name, P, r in [("Pi_triv  ", Pi_triv, 1),
                   ("Pi_om    ", Pi_om, 1),
                   ("Pi_ombar ", Pi_ombar, 1)]:
    h, i, rr, tr = projector_invariants(name, P, r)
    check(f"{name.strip()} Hermitian", h)
    check(f"{name.strip()} idempotent", i)
    check(f"{name.strip()} rank 1", rr and tr)


# Pi_triv + Pi_om + Pi_ombar == I (Peter-Weyl completeness).
completeness = np.linalg.norm(Pi_triv + Pi_om + Pi_ombar - I3)
check("Pi_triv + Pi_om + Pi_ombar == I", completeness < 1e-13,
      f"||.||={completeness:.2e}")

# Pairwise orthogonality.
for a_name, A in [("Pi_triv", Pi_triv), ("Pi_om", Pi_om), ("Pi_ombar", Pi_ombar)]:
    for b_name, B in [("Pi_triv", Pi_triv), ("Pi_om", Pi_om), ("Pi_ombar", Pi_ombar)]:
        if a_name == b_name:
            continue
        ortho = np.linalg.norm(A @ B)
        check(f"Orthogonality {a_name} * {b_name} == 0", ortho < 1e-13,
              f"||.||={ortho:.2e}")


# Closed Fourier form:  Pi_triv = (I + C + C^2)/3, etc.
Pi_triv_F = (I3 + C + C2) / 3.0
Pi_om_F = (I3 + np.conjugate(OMEGA) * C + OMEGA * C2) / 3.0
Pi_ombar_F = (I3 + OMEGA * C + np.conjugate(OMEGA) * C2) / 3.0

check(
    "Pi_triv == (I + C + C^2)/3",
    np.linalg.norm(Pi_triv - Pi_triv_F) < 1e-13,
)
check(
    "Pi_om == (I + omega^* C + omega C^2)/3",
    np.linalg.norm(Pi_om - Pi_om_F) < 1e-13,
)
check(
    "Pi_ombar == (I + omega C + omega^* C^2)/3",
    np.linalg.norm(Pi_ombar - Pi_ombar_F) < 1e-13,
)


# ---------------------------------------------------------------------------
# Section 2 - DM Z_3 basis U_Z3 and its diagonal-block projectors
# ---------------------------------------------------------------------------

print()
print("=" * 72)
print("Section 2 - Z_3 basis U_Z3 (DFT_3) and diagonal-block projectors")
print("=" * 72)

U_Z3 = (1 / math.sqrt(3)) * np.array(
    [[1, 1, 1],
     [1, OMEGA, OMEGA ** 2],
     [1, OMEGA ** 2, OMEGA]],
    dtype=complex,
)

unit_err = np.linalg.norm(U_Z3.conjugate().T @ U_Z3 - I3)
check("U_Z3 is unitary", unit_err < 1e-13, f"||U^dag U - I||={unit_err:.2e}")

# Confirm columns are C-eigenvectors. With the retained convention
# U_Z3 = (1/sqrt(3))[[1,1,1],[1,omega,omega^2],[1,omega^2,omega]], the
# three columns carry C-eigenvalues (1, omega^*, omega) in that order.
for j, (lam_name, lam) in enumerate([("1", 1.0),
                                     ("omega^*", np.conjugate(OMEGA)),
                                     ("omega", OMEGA)]):
    col = U_Z3[:, j]
    err = np.linalg.norm(C @ col - lam * col)
    check(f"column {j} of U_Z3 is C-eigenvector (lambda={lam_name})",
          err < 1e-13, f"res={err:.2e}")


Pi_Z3_singlet = U_Z3 @ np.diag([1.0, 0.0, 0.0]).astype(complex) @ U_Z3.conjugate().T
Pi_Z3_doublet = U_Z3 @ np.diag([0.0, 1.0, 1.0]).astype(complex) @ U_Z3.conjugate().T

for name, P, r in [("Pi_Z3_singlet", Pi_Z3_singlet, 1),
                   ("Pi_Z3_doublet", Pi_Z3_doublet, 2)]:
    h, i, rr, tr = projector_invariants(name, P, r)
    check(f"{name} Hermitian", h)
    check(f"{name} idempotent", i)
    check(f"{name} rank {r}", rr and tr)


# ---------------------------------------------------------------------------
# Section 3 - The main identity:  Pi_Z3 == Pi_Koide (exact matrix equality)
# ---------------------------------------------------------------------------

print()
print("=" * 72)
print("Section 3 - Matrix identities Pi_Z3_* == Pi_Koide_*")
print("=" * 72)

Pi_K_doublet = Pi_om + Pi_ombar

err_singlet = np.linalg.norm(Pi_Z3_singlet - Pi_triv)
err_doublet_a = np.linalg.norm(Pi_Z3_doublet - Pi_K_doublet)
err_doublet_b = np.linalg.norm(Pi_Z3_doublet - (I3 - Pi_triv))

check("Pi_Z3_singlet == Pi_triv", err_singlet < 1e-13, f"||.||={err_singlet:.2e}")
check(
    "Pi_Z3_doublet == Pi_om + Pi_ombar",
    err_doublet_a < 1e-13,
    f"||.||={err_doublet_a:.2e}",
)
check(
    "Pi_Z3_doublet == I - Pi_triv",
    err_doublet_b < 1e-13,
    f"||.||={err_doublet_b:.2e}",
)


# ---------------------------------------------------------------------------
# Section 4 - CKM ray separateness: unitary-equivalent but not structurally aligned
# ---------------------------------------------------------------------------

print()
print("=" * 72)
print("Section 4 - CKM ray rank-1 projector on C^3 (no C_3 alignment)")
print("=" * 72)

ckm_ray = complex(math.sqrt(1 / 6), math.sqrt(5 / 6))
u_CKM = np.array([1.0, 0.0, ckm_ray], dtype=complex)
u_CKM = u_CKM / np.linalg.norm(u_CKM)
Pi_CKM = np.outer(u_CKM, np.conjugate(u_CKM))

check("|ckm_ray| == 1", abs(abs(ckm_ray) - 1.0) < 1e-14,
      f"|ckm_ray|={abs(ckm_ray):.12f}")
check("Pi_CKM rank 1", abs(np.trace(Pi_CKM).real - 1.0) < 1e-13)
check("Pi_CKM Hermitian", np.linalg.norm(Pi_CKM - Pi_CKM.conjugate().T) < 1e-13)
check("Pi_CKM idempotent", np.linalg.norm(Pi_CKM @ Pi_CKM - Pi_CKM) < 1e-13)

# Overlaps with C_3 eigenvectors - no overlap is pinned to 0 or 1.
overlaps = {
    "v_triv": abs(np.vdot(v_triv, u_CKM)) ** 2,
    "v_om": abs(np.vdot(v_om, u_CKM)) ** 2,
    "v_ombar": abs(np.vdot(v_ombar, u_CKM)) ** 2,
}
for name, val in overlaps.items():
    print(f"   |<{name}|u_CKM>|^2 = {val:.6f}")

check(
    "Pi_CKM sums to 1 over C_3 basis",
    abs(sum(overlaps.values()) - 1.0) < 1e-13,
    f"sum={sum(overlaps.values()):.6f}",
)
check(
    "No overlap is pinned to exactly 0 or 1 (ckm_ray is not a C_3 eigenvector)",
    all(1e-4 < v < 1 - 1e-4 for v in overlaps.values()),
    f"overlaps={[round(v,6) for v in overlaps.values()]}",
)
check(
    "Pi_CKM is NOT equal to Pi_triv",
    np.linalg.norm(Pi_CKM - Pi_triv) > 0.1,
    f"||Pi_CKM - Pi_triv||={np.linalg.norm(Pi_CKM - Pi_triv):.4f}",
)
check(
    "Pi_CKM is NOT equal to Pi_Z3_singlet",
    np.linalg.norm(Pi_CKM - Pi_Z3_singlet) > 0.1,
)


# ---------------------------------------------------------------------------
# Section 5 - sign(H_framework) at retained DM points: not aligned with Pi_*
# ---------------------------------------------------------------------------

print()
print("=" * 72)
print("Section 5 - sign(H_framework) at retained DM points")
print("=" * 72)


def H_Z3(m, delta, q, a_star=0.1 + 0.2j, b_star=0.05 - 0.1j):
    """Live Hermitian source surface K_Z3 at (m, delta, q_+)."""
    K = np.zeros((3, 3), dtype=complex)
    s2 = math.sqrt(2)
    s3 = math.sqrt(3)
    K[0, 0] = m + 2 * q - 4 * s2 / 9
    K[0, 1] = a_star
    K[1, 0] = np.conjugate(a_star)
    K[0, 2] = b_star
    K[2, 0] = np.conjugate(b_star)
    K[1, 1] = -q + 2 * s2 / 9 - 1 / (2 * s3)
    K[2, 2] = -q + 2 * s2 / 9 + 1 / (2 * s3)
    K[1, 2] = m - 4 * s2 / 9 + 1j * (s3 * delta - 4 * s2 / 3)
    K[2, 1] = np.conjugate(K[1, 2])
    return K


retained_points = [(0.0, 0.2, 1.0), (0.0, 0.9, 2.0), (1.2, 0.2, 2.5)]

for (m, delta, q) in retained_points:
    H = H_Z3(m, delta, q)
    # Symmetrize defensively.
    H = 0.5 * (H + H.conjugate().T)
    evals, evecs = np.linalg.eigh(H)

    pos_mask = evals > 1e-10
    Pi_pos = np.zeros_like(H)
    for i, is_pos in enumerate(pos_mask):
        if is_pos:
            v = evecs[:, i:i + 1]
            Pi_pos = Pi_pos + v @ v.conjugate().T

    rank_pos = int(np.sum(pos_mask))
    d_triv = np.linalg.norm(Pi_pos - Pi_triv)
    d_db = np.linalg.norm(Pi_pos - Pi_Z3_doublet)
    d_sing = np.linalg.norm(Pi_pos - Pi_Z3_singlet)
    print(
        f"   (m, delta, q)={m, delta, q}: rank(Pi_+)={rank_pos}, "
        f"||Pi_+ - Pi_triv||={d_triv:.4f}, "
        f"||Pi_+ - Pi_Z3_doublet||={d_db:.4f}"
    )
    check(
        f"Pi_+ at {m, delta, q} is NOT Pi_triv",
        d_triv > 0.1,
        f"||.||={d_triv:.4f}",
    )
    check(
        f"Pi_+ at {m, delta, q} is NOT Pi_Z3_doublet",
        d_db > 0.1,
        f"||.||={d_db:.4f}",
    )
    check(
        f"Pi_+ at {m, delta, q} is NOT Pi_Z3_singlet",
        d_sing > 0.1,
        f"||.||={d_sing:.4f}",
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print()
print("=" * 72)
print("Joint projector identity certification summary")
print("=" * 72)
print(
    "\n"
    "Pi_Z3_singlet == Pi_triv          and\n"
    "Pi_Z3_doublet == Pi_om + Pi_ombar == I - Pi_triv\n"
    "as exact 3x3 matrix identities. Koide and DM lanes share one C_3\n"
    "isotypic decomposition. CKM ray is a separate rank-1 direction.\n"
)
print(f"PASS={PASS} FAIL={FAIL}")
sys.exit(0 if FAIL == 0 else 1)
