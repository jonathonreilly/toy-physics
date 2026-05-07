"""
SU(3) representation theory infrastructure for the full spin-network ED on a
2x2 spatial torus. Implementation note for `outputs/action_first_principles_2026_05_07/w1_full_spinnetwork/`.

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

What this module provides
-------------------------
1. Explicit irrep matrices D^(p,q)(U) for SU(3), constructed via Young
   symmetrizers acting on tensor powers of the fundamental representation
   C^3.  This is the standard "Schur module" construction described in
   Slansky 1981 (Physics Reports 79, eq. (3.8)-(3.10)) and Greiner-Mueller
   "Quantum Mechanics: Symmetries" (Section 9.3).

2. Decomposition lookup tables for tensor products of irreps used by the
   plaquette-fusion magnetic operator:

       (1,0) ⊗ (p,q)   = (p+1, q) ⊕ (p-1, q+1) [if p≥1] ⊕ (p, q-1) [if q≥1]
       (0,1) ⊗ (p,q)   = (p, q+1) ⊕ (p+1, q-1) [if q≥1] ⊕ (p-1, q) [if p≥1]

3. A numerical Clebsch-Gordan / projector machinery: given any (p,q) and
   target (p',q'), build the orthogonal projector onto the (p',q') isotypic
   component inside V_(p,q) ⊗ V_(1,0).  This is constructed using Haar
   averaging of D^(p,q)(U) ⊗ D^(1,0)(U) against D^(p',q')(U)*  -- the
   Schur-Weyl projector formula.

4. Vertex intertwiners on a 4-valent vertex: given four irreps λ_1, λ_2,
   λ_3, λ_4 incident at a vertex, build an orthonormal basis for the
   invariant subspace `Inv(V_λ_1 ⊗ V_λ_2 ⊗ V_λ_3 ⊗ V_λ_4)` via Haar
   projection P_inv = ∫ dU (D^λ_1(U) ⊗ D^λ_2(U) ⊗ D^λ_3(U) ⊗ D^λ_4(U)).

The construction of D^(p,q)(U) by Young symmetrization on (C^3)^⊗(p+2q)
is well-known; see Fulton-Harris "Representation Theory" Lecture 6 for
the rigorous proof.  We numerically construct it and verify

    -- character matches Weyl/Jacobi-Trudi formula on Haar samples
    -- dimensions match (p+1)(q+1)(p+q+2)/2
    -- D^(p,q)(U) is unitary on Haar samples
    -- character orthogonality ∫ |χ_(p,q)|^2 dU = 1 within MC error

These are the four checks that verify the Schur module construction
matches the standard SU(3) irrep theory.

Standard references
-------------------
    Slansky 1981, "Group theory for unified model building", Physics
        Reports 79, sections 3 and Appendix.
    Greiner-Müller, "Quantum Mechanics: Symmetries", 2nd ed., Springer
        1994, Chapter 8 ("Mathematical excursions: Group characters and
        their physical applications") and Chapter 9 ("SU(3) flavour
        symmetry").
    Fulton-Harris, "Representation Theory: A First Course", Springer 1991,
        Lectures 4-6 (Schur functors, irrep construction).
"""

from __future__ import annotations

import numpy as np
import itertools


def chi_pq_jacobi_trudi(U: np.ndarray, p: int, q: int) -> np.ndarray:
    """Independent Jacobi-Trudi character formula for SU(3) irrep (p, q).

    Used for cross-check against `D^(p,q)(U)` Schur-Weyl construction.

    For SU(3), partition λ = (p+q, q, 0) corresponds to irrep (p, q).
    Jacobi-Trudi:  s_λ = det[h_{λ_i + j - i}]   where h_k = complete
    homogeneous symmetric polynomials in eigenvalues.
    Power sums p_k = Tr(U^k); Newton's identity gives h_k.
    """
    if (p, q) == (0, 0):
        return np.ones(U.shape[0], dtype=complex)
    max_k = p + q + 2
    Uk = [np.eye(3, dtype=complex)[np.newaxis] * np.ones((U.shape[0], 1, 1))]
    Uk.append(U.copy())
    for k in range(2, max_k + 1):
        Uk.append(np.einsum('nij,njk->nik', Uk[-1], U))
    p_pow = [
        np.trace(Uk[k], axis1=1, axis2=2) if k > 0
        else 3.0 * np.ones(U.shape[0], dtype=complex)
        for k in range(0, max_k + 1)
    ]
    h = [np.ones(U.shape[0], dtype=complex)]
    for k in range(1, max_k + 1):
        h_k = np.zeros(U.shape[0], dtype=complex)
        for i in range(1, k + 1):
            h_k = h_k + p_pow[i] * h[k - i]
        h.append(h_k / k)
    def safe_h(k):
        if k < 0 or k > len(h) - 1:
            return np.zeros(U.shape[0], dtype=complex)
        return h[k]
    a, b, c = p + q, q, 0
    M = np.zeros((3, 3, U.shape[0]), dtype=complex)
    M[0, 0] = safe_h(a); M[0, 1] = safe_h(a + 1); M[0, 2] = safe_h(a + 2)
    M[1, 0] = safe_h(b - 1); M[1, 1] = safe_h(b); M[1, 2] = safe_h(b + 1)
    M[2, 0] = safe_h(c - 2); M[2, 1] = safe_h(c - 1); M[2, 2] = safe_h(c)
    det = (M[0, 0] * (M[1, 1] * M[2, 2] - M[1, 2] * M[2, 1])
            - M[0, 1] * (M[1, 0] * M[2, 2] - M[1, 2] * M[2, 0])
            + M[0, 2] * (M[1, 0] * M[2, 1] - M[1, 1] * M[2, 0]))
    return det


# ---------------------------------------------------------------------------
# Basic SU(3) representation theory
# ---------------------------------------------------------------------------

def casimir_su3(p: int, q: int) -> float:
    """SU(3) quadratic Casimir at trace-form Tr(T_a T_b) = δ_ab/2."""
    return (p * p + p * q + q * q + 3 * p + 3 * q) / 3.0


def conjugate(lam):
    """Conjugate of SU(3) irrep (p,q) is (q,p)."""
    return (lam[1], lam[0])


def dim_su3(p: int, q: int) -> int:
    """Dimension of irrep (p,q): (p+1)(q+1)(p+q+2)/2."""
    return ((p + 1) * (q + 1) * (p + q + 2)) // 2


def fund_tensor_pq(p: int, q: int):
    """Decompose (1,0) ⊗ (p,q) into SU(3) irreps."""
    out = [(p + 1, q)]
    if p >= 1:
        out.append((p - 1, q + 1))
    if q >= 1:
        out.append((p, q - 1))
    return out


def antifund_tensor_pq(p: int, q: int):
    """Decompose (0,1) ⊗ (p,q) into SU(3) irreps."""
    out = [(p, q + 1)]
    if q >= 1:
        out.append((p + 1, q - 1))
    if p >= 1:
        out.append((p - 1, q))
    return out


# ---------------------------------------------------------------------------
# Haar SU(3) sampling (reused from prior infrastructure)
# ---------------------------------------------------------------------------

def sample_su3(N: int, seed: int = 42) -> np.ndarray:
    """N matrices uniform on SU(3) via QR + det fix (Haar)."""
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((N, 3, 3)) + 1j * rng.standard_normal((N, 3, 3))
    Q, R = np.linalg.qr(Z)
    diag_R = np.diagonal(R, axis1=1, axis2=2)
    phases = diag_R / np.abs(diag_R)
    Q = Q * np.conj(phases)[:, np.newaxis, :]
    detQ = np.linalg.det(Q)
    Q[:, :, -1] *= np.conj(detQ)[:, np.newaxis]
    return Q


# ---------------------------------------------------------------------------
# Explicit D^(p,q)(U) construction via Young symmetrizer
# ---------------------------------------------------------------------------
#
# For SU(3) with partition λ = (p+q, q, 0), the representation V_λ is the
# Schur module S^λ(C^3).  It can be realized as a subspace of the tensor
# power (C^3)^⊗n where n = p+2q.
#
# Concretely, the Young symmetrizer associated with the standard tableau
# of shape λ projects onto V_λ inside (C^3)^⊗n.  We build:
#
#   1. The Young projector P_λ acting on (C^3)^⊗n.
#   2. An orthonormal basis B_λ for the image of P_λ.
#   3. D^(p,q)(U) := B_λ^† · (U^⊗n) · B_λ.
#
# This realization is well-defined up to a unitary change of basis in V_λ.

def young_projector_pq(p: int, q: int):
    """Build Young projector for partition λ = (p+q, q, 0) on (C^3)^⊗n.

    Returns:
        P  -- (3^n, 3^n) projector matrix onto S^λ(C^3)
        B  -- (3^n, dim) orthonormal column basis (B B^† = P, B^† B = I)
        n  -- tensor order = p + 2q

    The construction follows Fulton-Harris Lecture 4: the Young
    symmetrizer is c_λ = a_λ b_λ where a_λ = sum over row-stabilizer,
    b_λ = sum_σ sgn(σ) σ over column-stabilizer.  We normalize so that
    P = c_λ / ||c_λ||^2 is an orthogonal projector by computing it
    explicitly and orthonormalizing its image.
    """
    # Special-case trivial rep (p=q=0)
    if p == 0 and q == 0:
        return np.array([[1.0]]), np.array([[1.0]]), 0

    # Tensor order
    n = p + 2 * q
    if n == 0:
        return np.array([[1.0]]), np.array([[1.0]]), 0

    # Build standard Young tableau: fill rows left-to-right with 1..n
    #   row 0: cells (0,0), (0,1), ..., (0, p+q-1)   -- length p+q
    #   row 1: cells (1,0), (1,1), ..., (1, q-1)     -- length q
    #   row 2: empty                                  -- length 0
    # Cell labels (row, col), index in tableau = sequential
    cells = []
    for c in range(p + q):
        cells.append((0, c))
    for c in range(q):
        cells.append((1, c))
    # cells[i] = (row, col) of the i-th box

    # Row-stabilizer: permutations that preserve the row of each cell
    row_groups = []
    rows = {}
    for i, (r, _) in enumerate(cells):
        rows.setdefault(r, []).append(i)
    for r in sorted(rows):
        row_groups.append(rows[r])

    # Column-stabilizer: permutations preserving the column of each cell
    col_groups = []
    cols = {}
    for i, (_, c) in enumerate(cells):
        cols.setdefault(c, []).append(i)
    for c in sorted(cols):
        col_groups.append(cols[c])

    # Total dim of (C^3)^⊗n
    D = 3 ** n

    # Build product of permutations from generator groups via brute force
    # enumeration. n is small (≤ 5 for p+q ≤ 5 minus q=0, ≤ 7 for q=2 etc)
    def enumerate_group_perms(groups):
        """Enumerate all permutations of [0..n-1] preserving each group."""
        # Each group permutes independently
        perms_per_group = []
        for grp in groups:
            perms_per_group.append(list(itertools.permutations(grp)))
        results = []
        for combo in itertools.product(*perms_per_group):
            sigma = list(range(n))
            for grp_orig, grp_perm in zip(groups, combo):
                for src, dst in zip(grp_orig, grp_perm):
                    sigma[src] = dst
            # sigma[i] = where i goes
            results.append(tuple(sigma))
        return results

    def parity(sigma):
        """Parity of permutation sigma (list)."""
        s = list(sigma)
        n_local = len(s)
        seen = [False] * n_local
        sign = 1
        for i in range(n_local):
            if seen[i]:
                continue
            j = i
            cycle_len = 0
            while not seen[j]:
                seen[j] = True
                j = s[j]
                cycle_len += 1
            if cycle_len > 0 and cycle_len % 2 == 0:
                sign = -sign
        return sign

    # Apply permutation σ to a tensor basis vector indexed by tuple(i_0,...,i_{n-1}):
    # σ sends position k → position σ(k).  In the standard convention,
    # the matrix entry on basis is determined by reindexing.
    # We use convention: (σ · v)_{i_0,...,i_{n-1}} = v_{i_{σ^{-1}(0)},...,i_{σ^{-1}(n-1)}}
    # so that the matrix is M_{ij}^σ = δ_{i_k, j_{σ^{-1}(k)}}
    # We instead apply σ on indices directly (left action):
    #   (σ · v)(i_0,...,i_{n-1}) = v(i_{σ(0)},...,i_{σ(n-1)})
    # This is the standard tensor permutation matrix.

    def perm_to_matrix(sigma):
        """Build the n-fold tensor permutation matrix from sigma.

        Acts on (C^3)^⊗n as σ(v_1 ⊗ ... ⊗ v_n) = v_{σ^{-1}(1)} ⊗ ... ⊗ v_{σ^{-1}(n)}.
        Matrix entries: M[I, J] = 1 if J permuted by σ gives I.
        """
        if n == 0:
            return np.array([[1.0]])
        # σ acting on left: (σ v)_I = v_{σ^{-1}(I)} where σ^{-1}(I)_k = I_{σ(k)}
        # Equivalently M[I, J] = δ_{I, J ∘ σ} where (J ∘ σ)_k = J_{σ(k)}
        # Build by enumerating
        M = np.zeros((D, D))
        sigma_inv = [0] * n
        for k in range(n):
            sigma_inv[sigma[k]] = k
        # M[I, J] = 1 if I_k = J_{σ^{-1}(k)} for all k, i.e., I = (J permuted by σ^{-1})
        for J in range(D):
            # decode J into (j_0, ..., j_{n-1})
            j = []
            jj = J
            for _ in range(n):
                j.append(jj % 3)
                jj //= 3
            # I_k = j[σ^{-1}(k)]
            i = [j[sigma_inv[k]] for k in range(n)]
            # encode
            I = 0
            for k in range(n - 1, -1, -1):
                I = I * 3 + i[k]
            M[I, J] = 1.0
        return M

    # Build a_λ = sum over row-stabilizer
    a_lambda = np.zeros((D, D))
    row_perms = enumerate_group_perms(row_groups)
    for sigma in row_perms:
        a_lambda = a_lambda + perm_to_matrix(sigma)

    # Build b_λ = sum_{τ in col-stab} sgn(τ) τ
    b_lambda = np.zeros((D, D))
    col_perms = enumerate_group_perms(col_groups)
    for tau in col_perms:
        sgn = parity(tau)
        b_lambda = b_lambda + sgn * perm_to_matrix(tau)

    # Young symmetrizer: c_λ = a_λ · b_λ  (or b_λ · a_λ -- both isomorphic).
    # We use c_λ = a_λ @ b_λ as in Fulton-Harris.
    c_lambda = a_lambda @ b_lambda

    # The image of c_lambda is V_λ ⊗ (some multiplicity) inside (C^3)^⊗n.
    # For SU(3), partition λ=(p+q,q,0) with at most 3 rows, the multiplicity
    # space is the Specht module S^λ.  However, we only want **one copy**
    # of V_λ.  Standard practice: take the column space of c_lambda as a
    # subspace of (C^3)^⊗n and orthonormalize.  This may give us more than
    # one copy of V_λ (multiplicity = dim(S^λ) = number of standard Young
    # tableaux of shape λ).  We reduce by SVD on the action of SU(3) and
    # selecting one irreducible component.
    #
    # SIMPLER: use the fact that for SU(3) the image of c_λ on (C^3)^⊗n
    # contains dim S^λ copies of V_λ, all isomorphic.  We take the FIRST
    # copy by orthonormalizing column-by-column with Gram-Schmidt and
    # then selecting dim(V_λ) basis vectors via random Haar testing.

    # Get image space via SVD
    U_full, s_full, _ = np.linalg.svd(c_lambda)
    rank_tol = 1e-10 * (s_full[0] if len(s_full) > 0 else 1.0)
    rank = int(np.sum(s_full > rank_tol))
    # Image basis (full multiplicity):
    B_full = U_full[:, :rank]  # shape (D, rank)

    # The dimension of V_λ for SU(3):
    target_dim = dim_su3(p, q)

    # If rank == target_dim, we have a single copy.
    if rank == target_dim:
        return c_lambda, B_full, n

    # Otherwise rank = target_dim * mult, where mult = dim S^λ.  We must
    # extract a single irreducible copy.  Strategy: pick a random vector
    # v in V_λ-image, then build the SU(3)-orbit span by averaging
    # D^*(g) v over Haar g.  The dimension of this orbit is dim(V_λ).
    #
    # Do this by:
    #   1. Taking v = first column of B_full
    #   2. Computing v_g = U^⊗n v for many Haar U
    #   3. SVD of stacked v_g matrix to get target_dim orthonormal cols.
    #
    # Alternate cleaner approach: pre-multiplicity-decomposition via
    # symmetric group action.  For SU(3), n ≤ 5 typically, so (C^3)^⊗n
    # has small dim and we can do this fast.
    rng = np.random.default_rng(42 + 1000 * p + q)
    v = B_full[:, 0:1]  # take first vector
    # Apply random U's, collect orbit
    orbit = []
    for _ in range(max(target_dim * 4, 16)):
        Z = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
        Q_mat, R_mat = np.linalg.qr(Z)
        diag_R = np.diag(R_mat)
        phases = diag_R / np.abs(diag_R)
        Q_mat = Q_mat * np.conj(phases)[np.newaxis, :]
        Q_mat[:, -1] *= np.conj(np.linalg.det(Q_mat))
        # U^⊗n
        U_n = Q_mat
        for _ in range(n - 1):
            U_n = np.kron(U_n, Q_mat)
        v_g = U_n @ v
        orbit.append(v_g.ravel())

    orbit_mat = np.column_stack(orbit)
    U_o, s_o, _ = np.linalg.svd(orbit_mat, full_matrices=False)
    o_tol = 1e-8 * s_o[0]
    rank_orbit = int(np.sum(s_o > o_tol))
    if rank_orbit != target_dim:
        # Hmm; sometimes the orbit doesn't fill V_λ if v is special.
        # Try with more Haar samples and a different starting v.
        for trial in range(5):
            v = B_full[:, trial % rank:trial % rank + 1]
            orbit = []
            for _ in range(max(target_dim * 8, 32)):
                Z = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
                Q_mat, R_mat = np.linalg.qr(Z)
                diag_R = np.diag(R_mat)
                phases = diag_R / np.abs(diag_R)
                Q_mat = Q_mat * np.conj(phases)[np.newaxis, :]
                Q_mat[:, -1] *= np.conj(np.linalg.det(Q_mat))
                U_n = Q_mat
                for _ in range(n - 1):
                    U_n = np.kron(U_n, Q_mat)
                v_g = U_n @ v
                orbit.append(v_g.ravel())
            orbit_mat = np.column_stack(orbit)
            U_o, s_o, _ = np.linalg.svd(orbit_mat, full_matrices=False)
            o_tol = 1e-8 * s_o[0]
            rank_orbit = int(np.sum(s_o > o_tol))
            if rank_orbit == target_dim:
                break

    # Take target_dim columns of U_o as the orthonormal basis of V_λ
    B = U_o[:, :target_dim]
    return c_lambda, B, n


# Cache of pre-built representations
_REP_CACHE = {}


def get_irrep_basis(p: int, q: int):
    """Return cached (B, n) for irrep (p,q): B is (3^n, dim) orthonormal,
    n is tensor order p+2q.  Special-cases trivial.
    """
    if (p, q) in _REP_CACHE:
        return _REP_CACHE[(p, q)]
    if p == 0 and q == 0:
        result = (np.array([[1.0 + 0j]]), 0)
        _REP_CACHE[(0, 0)] = result
        return result
    _, B, n = young_projector_pq(p, q)
    B = B.astype(complex)
    result = (B, n)
    _REP_CACHE[(p, q)] = result
    return result


def D_pq(U: np.ndarray, p: int, q: int) -> np.ndarray:
    """Compute D^(p,q)(U) : V_λ → V_λ matrix.

    Args:
        U: (3,3) SU(3) matrix
        p, q: irrep labels

    Returns:
        D: (dim, dim) complex matrix where dim = dim_su3(p,q)
    """
    if p == 0 and q == 0:
        return np.array([[1.0 + 0j]])
    B, n = get_irrep_basis(p, q)
    # U^⊗n
    U_n = U
    for _ in range(n - 1):
        U_n = np.kron(U_n, U)
    return np.conj(B.T) @ U_n @ B


def D_pq_batch(U_batch: np.ndarray, p: int, q: int) -> np.ndarray:
    """Vectorized D^(p,q) over a batch of (N,3,3) SU(3) matrices.

    Returns: (N, dim, dim) complex.
    """
    if p == 0 and q == 0:
        return np.ones((U_batch.shape[0], 1, 1), dtype=complex)
    B, n = get_irrep_basis(p, q)
    # Build U^⊗n for each sample
    N = U_batch.shape[0]
    U_n = U_batch
    for _ in range(n - 1):
        # Outer-tensor over the 3x3 block.
        # U_n shape (N, 3^k, 3^k); U_batch shape (N, 3, 3) → (N, 3^(k+1), 3^(k+1))
        a = U_n.shape[1]
        # einsum-based kron
        U_n = (U_n[:, :, None, :, None] * U_batch[:, None, :, None, :]).reshape(N, 3 * a, 3 * a)
    # Apply B^† ... B
    return np.einsum('ai,nij,jb->nab', np.conj(B.T), U_n, B)


# ---------------------------------------------------------------------------
# Verification utilities
# ---------------------------------------------------------------------------

def chi_pq_from_D(U: np.ndarray, p: int, q: int) -> complex:
    """Character via trace of D^(p,q)(U)."""
    return np.trace(D_pq(U, p, q))


def verify_irrep_basics(p: int, q: int, N_samples: int = 200, verbose: bool = False):
    """Verify dim, unitarity, character orthogonality for irrep (p,q)."""
    expected_dim = dim_su3(p, q)
    D0 = D_pq(np.eye(3, dtype=complex), p, q)
    actual_dim = D0.shape[0]

    samples = sample_su3(N_samples, seed=1234 + 100 * p + q)
    Ds = D_pq_batch(samples, p, q)

    # Unitarity check: D D^† = I
    DD = np.einsum('nij,nkj->nik', Ds, np.conj(Ds))
    err_unit = np.max(np.abs(DD - np.eye(actual_dim)[np.newaxis]))

    # Character orthogonality: ∫ |χ_(p,q)|^2 dU = 1
    chars = np.einsum('nii->n', Ds)
    char_norm = np.mean(np.abs(chars) ** 2).real

    # Compare with Jacobi-Trudi formula (defined locally in this module)
    chi_jt_vals = chi_pq_jacobi_trudi(samples, p, q)
    chi_diff = np.max(np.abs(chars - chi_jt_vals))

    if verbose:
        print(f"  ({p},{q}): dim={actual_dim} (expected {expected_dim}), "
              f"unit_err={err_unit:.2e}, ⟨|χ|²⟩={char_norm:.4f}, "
              f"|χ_D - χ_JT|={chi_diff:.2e}")

    # Character orthogonality MC error scales as O(1/sqrt(N)) and the
    # variance grows with dim^2, so we use a relaxed tolerance for high-dim
    # irreps with small N.
    ok = (
        actual_dim == expected_dim
        and err_unit < 1e-7
        and abs(char_norm - 1.0) < max(0.15, expected_dim * 0.05)
        and chi_diff < 1e-7
    )
    return {
        'p': p, 'q': q,
        'dim_actual': actual_dim,
        'dim_expected': expected_dim,
        'unit_err': float(err_unit),
        'char_norm': float(char_norm),
        'chi_diff': float(chi_diff),
        'ok': ok,
    }


# ---------------------------------------------------------------------------
# Tensor product helpers
# ---------------------------------------------------------------------------

def D_pq_tensor_batch(U_batch: np.ndarray, irreps):
    """Build (N, D_total, D_total) tensor product D^λ_1(U) ⊗ ... ⊗ D^λ_k(U).

    Args:
        U_batch: (N, 3, 3) Haar samples
        irreps: list of (p_i, q_i)

    Returns:
        (N, D_total, D_total) complex array
    """
    blocks = [D_pq_batch(U_batch, p, q) for p, q in irreps]
    out = blocks[0]
    for b in blocks[1:]:
        a = out.shape[1]
        d = b.shape[1]
        out = (out[:, :, None, :, None] * b[:, None, :, None, :]).reshape(
            out.shape[0], a * d, a * d
        )
    return out


# ---------------------------------------------------------------------------
# Vertex intertwiner: P_inv = ∫ dU (D^λ_1 ⊗ ... ⊗ D^λ_k)(U)
# ---------------------------------------------------------------------------

def build_invariant_subspace(irreps, N_haar: int = 1000, seed: int = 7,
                              tol: float = 1e-3, verbose: bool = False):
    """Build orthonormal basis for invariant subspace
    Inv(V_λ_1 ⊗ ... ⊗ V_λ_k) under simultaneous SU(3) action.

    Args:
        irreps: list of (p_i, q_i)
        N_haar: Haar averages used to build P_inv.

    Returns:
        Q: (D_total, n_inv) orthonormal column basis spanning invariants.
        D_total: total tensor product dimension.
        n_inv: dimension of invariant subspace (= multiplicity of trivial in
               λ_1 ⊗ ... ⊗ λ_k).
    """
    samples = sample_su3(N_haar, seed=seed)
    tensors = D_pq_tensor_batch(samples, irreps)
    P_inv = np.mean(tensors, axis=0)
    P_inv = 0.5 * (P_inv + np.conj(P_inv.T))
    evals, evecs = np.linalg.eigh(P_inv)
    # Invariant eigenspaces have eigenvalue ≈ 1; non-invariant ≈ 0.
    keep_mask = evals > 1.0 - tol
    n_inv = int(np.sum(keep_mask))
    Q = evecs[:, keep_mask]
    D_total = P_inv.shape[0]

    # Refine: make Q strictly invariant by re-projecting.
    # Apply more Haar averages on Q itself to clean up MC noise.
    if n_inv > 0:
        clean_samples = sample_su3(2 * N_haar, seed=seed + 1)
        clean_tensors = D_pq_tensor_batch(clean_samples, irreps)
        Q_avg = np.mean(np.einsum('nij,jk->nik', clean_tensors, Q), axis=0)
        # Orthonormalize
        Q_clean, _ = np.linalg.qr(Q_avg)
        Q = Q_clean[:, :n_inv]

    if verbose:
        print(f"  Inv({irreps}): D_total={D_total}, n_inv={n_inv}, "
              f"top evals={evals[-min(5, len(evals)):][::-1].real}")

    return Q, D_total, n_inv


# ---------------------------------------------------------------------------
# Self-test main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 72)
    print("SU(3) representation infrastructure self-test")
    print("=" * 72)

    print("\n[1] Dimensions and Casimirs")
    test_irreps = [
        (0, 0), (1, 0), (0, 1), (1, 1),
        (2, 0), (0, 2), (2, 1), (1, 2), (3, 0), (0, 3),
    ]
    for p, q in test_irreps:
        print(f"  ({p},{q}): dim={dim_su3(p, q)}, C2={casimir_su3(p, q):.4f}")

    print("\n[2] Verify D^(p,q)(U) construction (200 Haar samples each)")
    all_ok = True
    for p, q in test_irreps:
        if dim_su3(p, q) > 30:
            continue  # skip very large for the basic self-test
        result = verify_irrep_basics(p, q, N_samples=200, verbose=True)
        all_ok = all_ok and result['ok']
    print(f"\n  All {sum(1 for pq in test_irreps if dim_su3(*pq) <= 30)} basic checks passed: {all_ok}")

    print("\n[3] Test tensor-product invariants")
    # 3 ⊗ 3 ⊗ 3 contains 1 trivial (the antisymmetric ε_ijk)
    Q3, D3, n3 = build_invariant_subspace([(1, 0), (1, 0), (1, 0)],
                                           N_haar=500, seed=10, verbose=True)
    print(f"  3⊗3⊗3 → trivial mult = {n3} (expected 1)")
    # 3 ⊗ 3̄ contains 1 trivial (the singlet δ^i_j)
    Q33, D33, n33 = build_invariant_subspace([(1, 0), (0, 1)],
                                              N_haar=500, seed=11, verbose=True)
    print(f"  3⊗3̄ → trivial mult = {n33} (expected 1)")
    # 8 ⊗ 8 contains 1 trivial (the Killing form)
    Q88, D88, n88 = build_invariant_subspace([(1, 1), (1, 1)],
                                              N_haar=500, seed=12, verbose=True)
    print(f"  8⊗8 → trivial mult = {n88} (expected 1)")
    # 4-valent vertex with all (1,0): 3⊗3⊗3⊗3 = 15 + 15' + 6̄ + 3̄ + 3̄ + ... wait, let me check.
    # Actually 3⊗3 = 6+3̄, then (6+3̄)⊗(6+3̄) = ... the trivial mult is computed.
    # For 3⊗3⊗3̄⊗3̄ it should be 2.
    Q4, D4, n4 = build_invariant_subspace([(1, 0), (1, 0), (0, 1), (0, 1)],
                                           N_haar=500, seed=13, verbose=True)
    print(f"  3⊗3⊗3̄⊗3̄ → trivial mult = {n4} (expected 2: 6⊗6̄ has 1, 3̄⊗3 has 1)")

    print("\n[4] Verify 4-valent vertex intertwiner is genuinely invariant")
    # Test a Q against a few random SU(3) elements
    for label, irreps_test in [
        ("3⊗3⊗3", [(1, 0), (1, 0), (1, 0)]),
        ("3⊗3̄", [(1, 0), (0, 1)]),
        ("8⊗8", [(1, 1), (1, 1)]),
    ]:
        Q_test, D_test, n_test = build_invariant_subspace(
            irreps_test, N_haar=500, seed=20
        )
        if n_test == 0:
            continue
        rng = np.random.default_rng(99)
        max_dev = 0.0
        for _ in range(10):
            Z = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
            Q_, R_ = np.linalg.qr(Z)
            diag_R = np.diag(R_)
            phases = diag_R / np.abs(diag_R)
            Q_ = Q_ * np.conj(phases)[np.newaxis, :]
            Q_[:, -1] *= np.conj(np.linalg.det(Q_))
            # Build U^⊗ via tensor products
            tens = D_pq_tensor_batch(Q_[None, :, :], irreps_test)[0]
            # Should leave Q_test invariant (modulo unitary in invariant space)
            transformed = tens @ Q_test
            # Project back: Q_test^† transformed should be unitary, but
            # |Q_test (Q_test^† transformed) - transformed| should be small.
            P_test = Q_test @ np.conj(Q_test.T)
            residual = transformed - P_test @ transformed
            dev = np.max(np.abs(residual))
            max_dev = max(max_dev, dev)
        print(f"  {label}: max |residual| = {max_dev:.2e} (should be small)")

    print("\n[5] Done.")
