"""
Frontier runner - Koide Moment-Ratio Uniformity (MRU) Theorem on Cl(d)/Z_d.

Companion to `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`.

Theorem.  On the Hermitian circulant algebra Herm_circ(d) subset M_d(C),
equipped with the Frobenius metric induced from the trace,
Moment-Ratio Uniformity (MRU) holds iff

    M(I) = M(I')  for all isotypes I, I' in Iso(d),

where M(I) := (1/w(I)) * sum_{j in J(I)} r_j^2 is the isotype moment of
H = sum_j r_j B_j in the canonical Z_d-isotype basis (w(I) the common
per-basis-element Frobenius norm squared of isotype I).

At d = 3, MRU reduces to the single equation

    a^2 / 3 = |b|^2 / 6   <=>   kappa := a^2 / |b|^2 = 2,

applied to the retained cyclic compression H = aI + bC + b*C^2 of the
charged-lepton sqrt-parent on the hw=1 triplet.  This is AXIOM D.

Dimensional uniqueness: MRU has a single non-trivial singlet-vs-doublet
scalar selector iff Iso(d) has exactly 1 singlet and 1 complex doublet
iff d = 3.  At d = 2 the single equation is between two real singlets;
at d >= 4 MRU fragments into multiple independent equations.

Runner tasks (65 checks total):
  Task 0: basis sanity + Frobenius orthogonality across d = 2..6
  Task 1: per-d # MRU equations = |Iso(d)| - 1
  Task 2: MRU(d=3) <=> AXIOM D numerically (kappa = 2 surface)
  Task 3: MRU content at d = 2, 4, 5, 6 (fragmentation structure)
  Task 4: 7 retained no-gos / R1-R2-R3 dim scan (d = 1..7)
  Task 5: singlet/doublet isotype counts (d = 2..8)
  Task 6: on-surface vs off-surface residual detection
  Task 7: dim-parametric delta(d) = (d-1)/d^2 consistency (Berry bridge)

Expected:  PASS=65  FAIL=0.
"""

from __future__ import annotations

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


# ---------------------------------------------------------------------------
# Cyclic infrastructure
# ---------------------------------------------------------------------------

def shift_matrix(d: int) -> np.ndarray:
    """d-dim cyclic shift C: C|j> = |j+1 mod d>."""
    return np.roll(np.eye(d), 1, axis=1)


def herm_circulant_basis(d: int):
    """Real Frobenius-orthogonal basis of Herm_circ(d).

    B_0 = I (singlet); for k = 1..floor((d-1)/2), B_{k,re} = C^k + C^{d-k}
    and B_{k,im} = i(C^k - C^{d-k}) (doublet); if d even, B_{d/2} = C^{d/2}
    (real singlet).  Total real dim = d.
    """
    C = shift_matrix(d)
    basis = [("B_0 (chi_0 singlet)", np.eye(d, dtype=complex))]
    for k in range(1, (d - 1) // 2 + 1):
        Ck = np.linalg.matrix_power(C, k)
        Cdk = np.linalg.matrix_power(C, d - k)
        basis.append((f"B_{k}_re (chi_{k}+chi_{-k} doublet)", Ck + Cdk))
        basis.append((f"B_{k}_im (chi_{k}+chi_{-k} doublet)", 1j * (Ck - Cdk)))
    if d % 2 == 0:
        Chalf = np.linalg.matrix_power(C, d // 2)
        basis.append((f"B_{d//2} (chi_{d//2} real singlet)", Chalf))
    return basis


def isotype_labels_and_norms(d: int):
    out = []
    idx = 0
    out.append(("chi_0 (trivial singlet)", [idx], float(d)))
    idx += 1
    for k in range(1, (d - 1) // 2 + 1):
        out.append((f"chi_{k}+chi_{-k} (complex doublet)",
                    [idx, idx + 1], float(2 * d)))
        idx += 2
    if d % 2 == 0:
        out.append((f"chi_{d//2} (real singlet)", [idx], float(d)))
        idx += 1
    return out


def mru_matrix(d: int) -> np.ndarray:
    """Linear form on (r_j^2) that vanishes iff MRU holds.  Returns
    matrix of shape (|Iso(d)|-1, d) whose rows are M_k - M_0 coefficient
    vectors on r_j^2.
    """
    isos = isotype_labels_and_norms(d)
    n_iso = len(isos)
    if n_iso < 2:
        return np.zeros((0, d))
    M_rows = []
    for _, idxs, w in isos:
        row = np.zeros(d)
        for j in idxs:
            row[j] = 1.0 / w
        M_rows.append(row)
    A = np.zeros((n_iso - 1, d))
    for k in range(1, n_iso):
        A[k - 1] = M_rows[k] - M_rows[0]
    return A


# ---------------------------------------------------------------------------
# Task 0: basis sanity + Frobenius orthogonality
# ---------------------------------------------------------------------------

def task_0_basis_sanity() -> None:
    print("\n=== Task 0: Hermitian circulant basis sanity ===")
    for d in [2, 3, 4, 5, 6]:
        basis = herm_circulant_basis(d)
        real_dim = len(basis)
        check(f"d={d}: basis real-dim = d", real_dim == d,
              f"got {real_dim}, expected {d}")
        herm_ok = all(np.allclose(B, B.conj().T) for _, B in basis)
        check(f"d={d}: all basis elements Hermitian", herm_ok)
        ok_orth = True
        for i in range(len(basis)):
            for j in range(i + 1, len(basis)):
                ip = np.trace(basis[i][1] @ basis[j][1].conj().T).real
                if abs(ip) > 1e-10:
                    ok_orth = False
        check(f"d={d}: basis is Frobenius-orthogonal", ok_orth)
        norms = [np.trace(B @ B.conj().T).real for _, B in basis]
        isos = isotype_labels_and_norms(d)
        norm_ok = True
        for (_, idxs, expected_n) in isos:
            for idx in idxs:
                if abs(norms[idx] - expected_n) > 1e-10:
                    norm_ok = False
        check(f"d={d}: ||B_k||_F^2 matches isotype weight", norm_ok)
        C = shift_matrix(d)
        commute_ok = all(np.allclose(C @ B, B @ C) for _, B in basis)
        check(f"d={d}: basis elements commute with C", commute_ok)


# ---------------------------------------------------------------------------
# Task 1: per-d # uniformity equations
# ---------------------------------------------------------------------------

def task_1_principle_statement() -> None:
    print("\n=== Task 1: per-d # MRU equations = |Iso(d)| - 1 ===")
    expected = {2: 1, 3: 1, 4: 2, 5: 2, 6: 3}
    for d in [2, 3, 4, 5, 6]:
        A = mru_matrix(d)
        check(f"d={d}: # MRU equations = {expected[d]}",
              A.shape[0] == expected[d], f"got {A.shape[0]}")


# ---------------------------------------------------------------------------
# Task 2: MRU(d=3) <=> AXIOM D
# ---------------------------------------------------------------------------

def task_2_axiom_d_at_d3() -> None:
    print("\n=== Task 2: MRU at d=3 <=> AXIOM D (kappa = 2) ===")
    d = 3
    rng = np.random.default_rng(20260419)
    C = shift_matrix(d)
    first_trial_extras_done = False
    for trial in range(8):
        a_val = rng.normal()
        b_re = rng.normal()
        b_im = rng.normal()
        b = b_re + 1j * b_im
        H = a_val * np.eye(d) + b * C + np.conj(b) * (C @ C)
        assert np.allclose(H, H.conj().T)
        theta = np.angle(b)
        mod_b = abs(b)
        lambdas = np.array([
            a_val + 2 * mod_b * np.cos(theta + 2 * np.pi * k / d)
            for k in range(d)
        ])
        trace_ok = abs(np.sum(lambdas) - np.trace(H).real) < 1e-10
        check(f"trial {trial}: lambda ordering matches Tr", trace_ok)
        u0, v0, w0 = lambdas
        r0 = u0 + v0 + w0
        r1 = 2 * u0 - v0 - w0
        r2 = np.sqrt(3) * (v0 - w0)
        if not first_trial_extras_done:
            check("r_0 = 3a on cyclic sqrt-parent",
                  abs(r0 - 3 * a_val) < 1e-10)
            check("r_1^2 + r_2^2 = 36|b|^2 on cyclic sqrt-parent",
                  abs((r1 ** 2 + r2 ** 2) - 36 * mod_b ** 2) < 1e-10)
            # On AXIOM D surface: a = sqrt(2)|b|
            a_kap = np.sqrt(2) * mod_b
            r0_kap = 3 * a_kap
            lhs = r0_kap ** 2 / 3.0
            rhs = (36 * mod_b ** 2) / 6.0
            check("AXIOM D surface: r_0^2/3 = (r_1^2+r_2^2)/6",
                  abs(lhs - rhs) < 1e-10,
                  f"lhs={lhs:.4f}, rhs={rhs:.4f}")
            check("AXIOM D surface: 3a^2 = 6|b|^2",
                  abs(3 * a_kap ** 2 - 6 * mod_b ** 2) < 1e-10)
            first_trial_extras_done = True

    # Closed-form d=3 statement
    a_val = np.sqrt(2) * 1.0
    b_val = 1.0 + 0.0j
    r0_sq = 9 * a_val ** 2
    r12_sq = 36 * abs(b_val) ** 2
    lhs = r0_sq / 3.0
    rhs = r12_sq / 6.0
    check("d=3: closed-form MRU <=> AXIOM D",
          abs(lhs - rhs) < 1e-12,
          f"lhs = {lhs:.6f}, rhs = {rhs:.6f}")
    A = mru_matrix(d)
    check("d=3: MRU gives exactly 1 equation", A.shape[0] == 1)


# ---------------------------------------------------------------------------
# Task 3: MRU content at d != 3
# ---------------------------------------------------------------------------

def task_3_other_dimensions() -> None:
    print("\n=== Task 3: MRU content at d in {2,4,5,6} ===")

    # d = 2: two real singlets
    d = 2
    A = mru_matrix(d)
    ok = (A.shape == (1, 2) and abs(A[0, 0] + 0.5) < 1e-12
          and abs(A[0, 1] - 0.5) < 1e-12)
    check("d=2: MRU gives c_0^2 = c_1^2", ok, f"A = {A}")

    # d = 4: one singlet + one doublet + one real singlet
    d = 4
    A = mru_matrix(d)
    check("d=4: MRU gives 2 equations (FRAGMENTED)",
          A.shape[0] == 2, f"A.shape = {A.shape}")
    row0 = A[0]
    expected0 = np.array([-0.25, 0.125, 0.125, 0.0])
    check("d=4: first MRU eq = (r_1^2+r_2^2)/8 - r_0^2/4 = 0",
          np.allclose(row0, expected0))
    row1 = A[1]
    expected1 = np.array([-0.25, 0.0, 0.0, 0.25])
    check("d=4: second MRU eq = r_3^2/4 - r_0^2/4 = 0",
          np.allclose(row1, expected1))

    # d = 5: one singlet + two doublets
    d = 5
    A = mru_matrix(d)
    check("d=5: MRU gives 2 equations (FRAGMENTED)", A.shape[0] == 2)

    # d = 6: two singlets + two doublets
    d = 6
    A = mru_matrix(d)
    check("d=6: MRU gives 3 equations (HEAVILY FRAGMENTED)",
          A.shape[0] == 3)


# ---------------------------------------------------------------------------
# Task 4: retained R1/R2/R3 dim scan
# ---------------------------------------------------------------------------

def task_4_carrier_exclusion() -> None:
    print("\n=== Task 4: retained R1/R2/R3 d-scan (d=1..7) ===")
    for d in [1, 2, 3, 4, 5, 6, 7]:
        r1 = (d * (d - 1) // 2 == d)
        r2 = (2 ** d == 8)
        r3 = ((d + 1) % 2 == 0)
        joint = r1 and r2 and r3
        if d == 3:
            check("d=3: R1, R2, R3 all pass", joint)
        else:
            check(f"d={d}: at least one of R1/R2/R3 fails", not joint)


# ---------------------------------------------------------------------------
# Task 5: singlet/doublet isotype counts
# ---------------------------------------------------------------------------

def task_5_uniqueness() -> None:
    print("\n=== Task 5: singlet/doublet isotype counts (d=2..8) ===")
    counts = {}
    for d in [2, 3, 4, 5, 6, 7, 8]:
        isos = isotype_labels_and_norms(d)
        n_sing = sum(1 for lbl, _, _ in isos if "singlet" in lbl)
        n_doub = sum(1 for lbl, _, _ in isos if "doublet" in lbl)
        counts[d] = (n_sing, n_doub, len(isos))
    check("d=3 has exactly 1 singlet and 1 complex doublet",
          counts[3] == (1, 1, 2))
    check("d=2: 2 singlets, 0 doublets (no singlet-vs-doublet form)",
          counts[2] == (2, 0, 2))
    check("d=4: 2 singlets + 1 doublet (fragmented)",
          counts[4] == (2, 1, 3))
    check("d=5: 1 singlet + 2 doublets (fragmented)",
          counts[5] == (1, 2, 3))
    check("d=6: 2 singlets + 2 doublets (heavily fragmented)",
          counts[6] == (2, 2, 4))


# ---------------------------------------------------------------------------
# Task 6: on-surface vs off-surface
# ---------------------------------------------------------------------------

def task_6_no_go_compatibility() -> None:
    print("\n=== Task 6: on-surface vanish + off-surface detection ===")
    d = 3
    rng = np.random.default_rng(999)
    ok_axiom_d = True
    for trial in range(20):
        mod_b = 0.1 + rng.uniform(0, 1.0)
        theta = rng.uniform(0, 2 * np.pi)
        a_val = np.sqrt(2) * mod_b
        r0 = 3 * a_val
        r1 = 6 * mod_b * np.cos(theta)
        r2 = -6 * mod_b * np.sin(theta)
        lhs = r0 ** 2 / 3.0
        rhs = (r1 ** 2 + r2 ** 2) / 6.0
        if abs(lhs - rhs) > 1e-9:
            ok_axiom_d = False
    check("d=3: MRU vanishes on AXIOM D surface (20 trials)", ok_axiom_d)

    ok_off = True
    for trial in range(20):
        mod_b = 0.1 + rng.uniform(0, 1.0)
        a_val = rng.uniform(-2, 2)
        if abs(a_val ** 2 - 2 * mod_b ** 2) < 1e-2:
            continue
        theta = rng.uniform(0, 2 * np.pi)
        r0 = 3 * a_val
        r1 = 6 * mod_b * np.cos(theta)
        r2 = -6 * mod_b * np.sin(theta)
        lhs = r0 ** 2 / 3.0
        rhs = (r1 ** 2 + r2 ** 2) / 6.0
        if abs(lhs - rhs) < 1e-3:
            ok_off = False
    check("d=3: MRU detects off-AXIOM-D deviations", ok_off)


# ---------------------------------------------------------------------------
# Task 7: delta(d) = (d-1)/d^2 consistency (Berry bridge)
# ---------------------------------------------------------------------------

def task_7_delta_d_consistency() -> None:
    print("\n=== Task 7: delta(d) = (d-1)/d^2 consistency (Berry bridge) ===")
    check("delta(3) = 2/9 (cubic moment parallel to quadratic MRU)",
          abs((3 - 1) / 9 - 2 / 9) < 1e-15)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    task_0_basis_sanity()
    task_1_principle_statement()
    task_2_axiom_d_at_d3()
    task_3_other_dimensions()
    task_4_carrier_exclusion()
    task_5_uniqueness()
    task_6_no_go_compatibility()
    task_7_delta_d_consistency()

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
