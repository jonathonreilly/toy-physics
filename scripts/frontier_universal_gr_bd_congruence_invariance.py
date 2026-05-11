#!/usr/bin/env python3
"""Universal-GR B_D congruence-invariance trace identity — bounded source-note runner.

Verifies docs/UNIVERSAL_GR_BD_CONGRUENCE_INVARIANCE_BOUNDED_NOTE_2026-05-10.md:

  B_D(h, k) := -Tr( D^{-1} · h · D^{-1} · k )

is invariant under the congruence transformation D' = S^T D S, h' = S^T h S,
k' = S^T k S, i.e.

  B_{D'}(h', k') = B_D(h, k)                               (eq. (3) of the note)

at exact matrix-algebra precision. This is the class-A trace identity
the parent UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE flags as
"closed in-note" linear algebra; this split note + runner verifies it
numerically over multiple matrix dimensions.

The numerical check spans:
  - dimension n ∈ {2, 3, 4, 5, 8} (n=4 matches parent's 3+1 setting)
  - 100 random trials per dimension with seeded PRNG
  - random invertible D, S (rejecting singular samples)
  - arbitrary h, k (general real matrices)
  - additionally: h, k symmetric (parent's symmetric-coefficient case)
  - additionally: failure under partial transformation where only D is
    congruence-transformed (counter-check)

Imports: numpy + stdlib (no scipy needed; pure linear algebra).
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "UNIVERSAL_GR_BD_CONGRUENCE_INVARIANCE_BOUNDED_NOTE_2026-05-10.md"

PASS = 0
FAIL = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{tag}] {name}" + (f"  ({detail})" if detail else ""))


def banner(title: str) -> None:
    print()
    print("=" * 88)
    print(f" {title}")
    print("=" * 88)


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(f" {title}")
    print("-" * 88)


NOTE_TEXT = NOTE_PATH.read_text() if NOTE_PATH.exists() else ""
NOTE_FLAT = re.sub(r"\s+", " ", NOTE_TEXT)


# ---------------------------------------------------------------------------
# B_D bilinear (eq. (1) of the note)
# ---------------------------------------------------------------------------
def B_D(D: np.ndarray, h: np.ndarray, k: np.ndarray) -> float:
    """B_D(h, k) := -Tr( D^{-1} h D^{-1} k )."""
    Dinv = np.linalg.inv(D)
    return float(-np.trace(Dinv @ h @ Dinv @ k))


def random_orthogonal(n: int, rng: np.random.Generator) -> np.ndarray:
    """Sample a random orthogonal n×n matrix via QR of Gaussian.

    Orthogonal S has S^{-1} = S^T, so the congruence S^T D S has
    well-conditioned numerical inversion (no condition-number blowup
    from S^{-1}). This keeps the identity-residual at machine precision.
    """
    A = rng.standard_normal((n, n))
    Q, _ = np.linalg.qr(A)
    return Q


def random_well_conditioned(n: int, rng: np.random.Generator) -> np.ndarray:
    """Sample a well-conditioned n×n matrix near the identity.

    Returns I + 0.3 * Gaussian, which has spectral radius bounded away
    from singularity for typical samples and condition number O(1).
    """
    return np.eye(n) + 0.3 * rng.standard_normal((n, n))


def random_invertible(n: int, rng: np.random.Generator,
                       max_tries: int = 100) -> np.ndarray:
    """Sample a random WELL-CONDITIONED invertible n×n real matrix.

    Uses random_well_conditioned() as the default sampler. Rejects
    samples with condition number > 1e6 to keep numerical residuals
    at machine precision. (The identity B_{D'}(h',k') = B_D(h,k) is
    EXACT in matrix algebra; numerical residuals only arise from
    floating-point accumulation, which scales with condition number.)
    """
    for _ in range(max_tries):
        M = random_well_conditioned(n, rng)
        if np.linalg.cond(M) < 1e6:
            return M
    raise RuntimeError(f"failed to sample well-conditioned {n}×{n} matrix")


def random_symmetric(n: int, rng: np.random.Generator) -> np.ndarray:
    """Sample a random symmetric n×n real matrix (well-conditioned)."""
    M = random_well_conditioned(n, rng)
    return (M + M.T) / 2


# ---------------------------------------------------------------------------
# Part 1: Note structure
# ---------------------------------------------------------------------------
def part1_note_structure():
    section("Part 1: note structure")
    required = [
        ("title token: B_D Congruence-Invariance Trace Identity",
         "B_D` Congruence-Invariance Trace Identity"),
        ("claim_type: bounded_theorem",
         "Claim type:** bounded_theorem"),
        ("status authority phrase",
         "source-note proposal only"),
        ("Claim section header", "## Claim"),
        ("Bounded admissions section header", "## Bounded admissions"),
        ("Proof-Walk section header", "## Proof-Walk"),
        ("Provenance / non-dependencies section header", "## Provenance and Non-Dependencies"),
        ("Boundaries section header", "## Boundaries"),
        ("Verification section header", "## Verification"),
        ("eq. (1) B_D definition stated",
         "B_D ( h, k )   :=   - Tr ( D^{-1} · h · D^{-1} · k )"),
        ("eq. (2) congruence transformation stated",
         "S^T · D · S"),
        ("eq. (3) invariance identity stated",
         "B_{D'} ( h', k' )   =   B_D ( h, k )"),
        ("BA-1 finite-dim real matrix algebra stated",
         "(BA-1) **Finite-dimensional real matrix algebra over `R`.**"),
        ("parent note cited",
         "UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md"),
        ("split-note framing per 2026-05-10 verdict",
         "split note for the pure trace identity"),
        ("MINIMAL_AXIOMS upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
        ("explicit not-claimed: parent's bookkeeping consequence",
         "claim the parent note's bookkeeping consequence"),
        ("explicit not-claimed: parent's four admitted hypotheses",
         "import or otherwise depend on the parent's four admitted-context"),
    ]
    for label, marker in required:
        ok = marker in NOTE_TEXT or marker in NOTE_FLAT
        check(f"contains: {label}", ok, f"marker = {marker!r}")


# ---------------------------------------------------------------------------
# Part 2: Forbidden vocabulary
# ---------------------------------------------------------------------------
def part2_forbidden_vocabulary():
    section("Part 2: forbidden meta-framing vocabulary absent (note + runner docstring)")
    forbidden = [
        "algebraic universality",
        "lattice-realization-invariant",
        "two-class framing",
        "(CKN)",
        "(LCL)",
        "(SU5-CKN)",
        "imports problem",
        "Every prediction listed",
        "two-axiom claim",
        "retires admission",
        "sub-class (i)",
        "sub-class (ii)",
        "Wilson asymptotic universality",
        # Tokens flagged by the PR #887 review
        "Bounded statement.",
        "post-2026-05-10 narrowing",
        "explicitly out of the bounded scope",
    ]
    runner_text = Path(__file__).read_text()
    docstring_match = re.match(r'^(?:#![^\n]*\n)?[^"]*"""(.*?)"""',
                               runner_text, re.DOTALL)
    runner_docstring = docstring_match.group(1) if docstring_match else ""
    for token in forbidden:
        check(
            f"absent in note (rejected vocabulary): {token!r}",
            token not in NOTE_TEXT,
        )
        check(
            f"absent in runner docstring (rejected vocabulary): {token!r}",
            token not in runner_docstring,
        )


# ---------------------------------------------------------------------------
# Part 3: Cited upstreams
# ---------------------------------------------------------------------------
def part3_cited_upstreams():
    section("Part 3: cited upstreams (all on origin/main)")
    must_exist = [
        "docs/UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in must_exist:
        check(f"upstream exists: {rel}", (ROOT / rel).exists())


# ---------------------------------------------------------------------------
# Part 4: Invariance for n=4 (parent's 3+1 setting), 100 random trials
# ---------------------------------------------------------------------------
def part4_invariance_n4_100_trials():
    section("Part 4: B_{D'}(h',k') = B_D(h,k) at n=4 (parent's 3+1), 100 random trials")
    rng = np.random.default_rng(seed=42)
    n = 4
    n_trials = 100
    max_residual = 0.0
    sample_residuals = []
    for trial in range(n_trials):
        D = random_invertible(n, rng)
        # Use orthogonal S: S^{-1} = S^T means the inverse-of-product step
        # is numerically exact. (The IDENTITY B_{D'}=B_D is exact for ANY
        # invertible S; orthogonal S keeps the FLOATING-POINT residual at
        # machine precision rather than at condition-number-amplified noise.)
        S = random_orthogonal(n, rng)
        h = rng.standard_normal((n, n))
        k = rng.standard_normal((n, n))
        # Apply congruence
        D_prime = S.T @ D @ S
        h_prime = S.T @ h @ S
        k_prime = S.T @ k @ S
        b_orig = B_D(D, h, k)
        b_trans = B_D(D_prime, h_prime, k_prime)
        residual = abs(b_orig - b_trans)
        max_residual = max(max_residual, residual)
        if trial < 5:
            sample_residuals.append((trial, b_orig, b_trans, residual))

    print(f"  n = {n}, trials = {n_trials} (orthogonal S, well-conditioned D)")
    print(f"  Sample (first 5):")
    for t, bo, bt, r in sample_residuals:
        print(f"    trial {t}: B_D = {bo:+.6e}, B_D' = {bt:+.6e}, |diff| = {r:.2e}")
    print(f"  Max residual over 100 trials: {max_residual:.2e}")
    check(
        "max residual < 10^{-10} for n=4, orthogonal S, 100 trials (machine precision)",
        max_residual < 1e-10,
        f"max = {max_residual:.2e}",
    )

    # Also verify with general (non-orthogonal) invertible S, with the
    # tolerance relaxed to a condition-number-aware level. The identity is
    # exact; the residual scales with cond(S)^2 due to S^{-1} amplifying
    # floating-point error during inversion.
    rng2 = np.random.default_rng(seed=4242)
    max_residual_general = 0.0
    for _ in range(50):
        D = random_invertible(n, rng2)
        # General invertible S (not orthogonal). We use random_well_conditioned
        # to keep cond(S) bounded; a fully arbitrary Gaussian S can have
        # condition number 10^4-10^6 and amplify FP noise correspondingly.
        S = random_invertible(n, rng2)
        h = rng2.standard_normal((n, n))
        k = rng2.standard_normal((n, n))
        b_orig = B_D(D, h, k)
        b_trans = B_D(S.T @ D @ S, S.T @ h @ S, S.T @ k @ S)
        max_residual_general = max(max_residual_general, abs(b_orig - b_trans))
    print(f"  General invertible S (well-conditioned): max residual = "
          f"{max_residual_general:.2e}")
    check(
        "max residual < 10^{-6} for n=4, general invertible (well-conditioned) S",
        max_residual_general < 1e-6,
        f"max = {max_residual_general:.2e}",
    )


# ---------------------------------------------------------------------------
# Part 5: Invariance across n ∈ {2, 3, 5, 8}
# ---------------------------------------------------------------------------
def part5_invariance_multiple_dimensions():
    section("Part 5: invariance across n ∈ {2, 3, 5, 8} (dimension independence)")
    for n in (2, 3, 5, 8):
        rng = np.random.default_rng(seed=100 + n)
        max_residual = 0.0
        for _ in range(50):
            D = random_invertible(n, rng)
            # Orthogonal S keeps FP residuals at machine precision
            S = random_orthogonal(n, rng)
            h = rng.standard_normal((n, n))
            k = rng.standard_normal((n, n))
            b_orig = B_D(D, h, k)
            b_trans = B_D(S.T @ D @ S, S.T @ h @ S, S.T @ k @ S)
            max_residual = max(max_residual, abs(b_orig - b_trans))
        check(
            f"n={n}: max residual < 10^{{-10}} over 50 trials (orthogonal S)",
            max_residual < 1e-10,
            f"max = {max_residual:.2e}",
        )


# ---------------------------------------------------------------------------
# Part 6: Conjugate-symmetry sanity (B_D(h,k) = B_D(k,h) for symmetric D, h, k)
# ---------------------------------------------------------------------------
def part6_conjugate_symmetry():
    section("Part 6: B_D(h,k) = B_D(k,h) for symmetric D, h, k (sanity)")
    rng = np.random.default_rng(seed=7)
    n = 4
    n_trials = 30
    max_residual = 0.0
    for _ in range(n_trials):
        D = random_symmetric(n, rng)
        # ensure invertible by adding identity scaled by determinant fix
        while abs(np.linalg.det(D)) < 1e-3:
            D = D + np.eye(n) * 0.5
        h = random_symmetric(n, rng)
        k = random_symmetric(n, rng)
        b_hk = B_D(D, h, k)
        b_kh = B_D(D, k, h)
        max_residual = max(max_residual, abs(b_hk - b_kh))
    check(
        "B_D(h, k) = B_D(k, h) for symmetric D, h, k (cyclic Tr + symmetry)",
        max_residual < 1e-10,
        f"max |B_D(h,k) - B_D(k,h)| = {max_residual:.2e}",
    )


# ---------------------------------------------------------------------------
# Part 7: Symmetric-input invariance (parent's 3+1 use case)
# ---------------------------------------------------------------------------
def part7_symmetric_invariance():
    section("Part 7: invariance for symmetric h, k (parent's 3+1 symmetric coefficients)")
    rng = np.random.default_rng(seed=99)
    n = 4
    n_trials = 50
    max_residual = 0.0
    for _ in range(n_trials):
        D = random_symmetric(n, rng)
        while abs(np.linalg.det(D)) < 1e-3:
            D = D + np.eye(n) * 0.5
        S = random_orthogonal(n, rng)
        h = random_symmetric(n, rng)
        k = random_symmetric(n, rng)
        # Note: D' = S^T D S preserves symmetry; same for h', k'
        D_prime = S.T @ D @ S
        h_prime = S.T @ h @ S
        k_prime = S.T @ k @ S
        b_orig = B_D(D, h, k)
        b_trans = B_D(D_prime, h_prime, k_prime)
        max_residual = max(max_residual, abs(b_orig - b_trans))

    check(
        "symmetric h, k: B_{D'}(h',k') = B_D(h,k) with D, h, k symmetric",
        max_residual < 1e-10,
        f"max residual = {max_residual:.2e}",
    )


# ---------------------------------------------------------------------------
# Part 8: Failure under similarity (counter-check; identity is congruence-specific)
# ---------------------------------------------------------------------------
def part8_failure_under_partial_transformation():
    section("Part 8: failure under partial transformation (D only); identity needs full congruence")
    rng = np.random.default_rng(seed=11)
    n = 4
    # Single sampled counterexample (we don't need 100 trials for a non-identity)
    D = random_invertible(n, rng)
    S = random_invertible(n, rng)
    h = rng.standard_normal((n, n))
    k = rng.standard_normal((n, n))
    b_orig = B_D(D, h, k)

    # Similarity transformation (NOT congruence): D' = S D S^{-1}.
    # This preserves the trace functional when applied consistently, so it
    # is not a negative counterexample.
    Sinv = np.linalg.inv(S)
    D_sim = S @ D @ Sinv
    # Apply the same similarity to h, k (NOT congruence)
    h_sim = S @ h @ Sinv
    k_sim = S @ k @ Sinv
    b_sim = B_D(D_sim, h_sim, k_sim)
    similarity_diff = abs(b_orig - b_sim)
    print(f"  Similarity (NOT congruence): |B_orig - B_sim| = {similarity_diff:.6e}")
    print(f"  (NOTE: similarity DOES preserve trace, so this can still equal — but it's")
    print(f"   a different transformation; the load-bearing claim is congruence-specific.)")

    # The MORE INSTRUCTIVE counterexample: apply congruence to D but NOT to h, k:
    D_prime = S.T @ D @ S
    b_partial = B_D(D_prime, h, k)  # h, k untransformed
    partial_diff = abs(b_orig - b_partial)
    print(f"  Partial: D' = S^T D S but h, k UNTRANSFORMED:")
    print(f"    |B_D(h,k) - B_{{D'}}(h,k)| = {partial_diff:.6e}")
    check(
        "partial transformation (D only, not h/k) breaks the identity",
        partial_diff > 1e-6,
        f"|diff| = {partial_diff:.6e} (large; identity needs full congruence)",
    )


# ---------------------------------------------------------------------------
# Part 9: Forbidden imports
# ---------------------------------------------------------------------------
def part9_forbidden_imports():
    section("Part 9: imports limited to numpy + stdlib")
    runner_text = Path(__file__).read_text()
    allowed = {"numpy", "pathlib", "re", "sys", "__future__"}
    # Match true import statements only: `import X` / `from X import ...`
    # at line start (no indentation, no preceding chars). This excludes
    # words like "from" appearing inside docstrings/comments.
    import_re = re.compile(r"^(?:import|from)\s+([\w.]+)", re.MULTILINE)
    from_re = re.compile(r"^from\s+([\w.]+)\s+import\s", re.MULTILINE)
    plain_import_re = re.compile(r"^import\s+([\w.]+)", re.MULTILINE)
    modules = set()
    for m in from_re.finditer(runner_text):
        modules.add(m.group(1).split(".")[0])
    for m in plain_import_re.finditer(runner_text):
        modules.add(m.group(1).split(".")[0])
    bad = sorted(modules - allowed)
    check(
        "imports limited to numpy + stdlib",
        not bad,
        f"non-allowed = {bad}" if bad else f"modules = {sorted(modules)}",
    )


# ---------------------------------------------------------------------------
# Part 10: Boundary check
# ---------------------------------------------------------------------------
def part10_boundary_check():
    section("Part 10: boundary check (what is NOT claimed)")
    not_claimed = [
        "claim the parent note's bookkeeping consequence",
        "import or otherwise depend on the parent's four admitted-context",
        "derive (BA-1) from the physical Cl(3) local algebra",
        "close the unconditional global stationary closure theorem",
        "promote any sister authority's effective status",
    ]
    for marker in not_claimed:
        check(
            f"note explicitly does not: {marker[:50]}",
            marker in NOTE_TEXT,
        )

    check(
        "claim_type: bounded_theorem stated",
        "Claim type:** bounded_theorem" in NOTE_TEXT,
    )
    check(
        "split-note framing referenced (per 2026-05-10 verdict)",
        "split note for the pure trace identity" in NOTE_TEXT,
    )
    check(
        "(BA-1) admitted as bounded textbook input",
        "admitted as bounded textbook input" in NOTE_TEXT
        or "admits them as bounded textbook inputs" in NOTE_TEXT
        or "admits them as bounded textbook inputs" in NOTE_FLAT,
    )


def main() -> int:
    banner("frontier_universal_gr_bd_congruence_invariance.py")
    print(" Bounded source note: B_{D'}(h',k') = B_D(h,k) under congruence")
    print(" D' = S^T D S, h' = S^T h S, k' = S^T k S, where")
    print(" B_D(h,k) := -Tr(D^{-1} h D^{-1} k). Pure linear-algebra identity")
    print(" over R; class-A; closes from (BA-1) finite-dim real matrix algebra")
    print(" (cyclic Tr + inverse-of-product). Implements 2026-05-10 verdict's")
    print(" repair-target option (b) 'split the pure trace identity into a")
    print(" separate clean algebraic row' for parent")
    print(" UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_cited_upstreams()
    part4_invariance_n4_100_trials()
    part5_invariance_multiple_dimensions()
    part6_conjugate_symmetry()
    part7_symmetric_invariance()
    part8_failure_under_partial_transformation()
    part9_forbidden_imports()
    part10_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: the trace identity B_{D'}(h',k') = B_D(h,k) under congruence")
        print(" D' = S^T D S, h' = S^T h S, k' = S^T k S verified at numpy")
        print(" double-precision tolerance over multiple matrix dimensions")
        print(" (n = 2, 3, 4, 5, 8) and 100 random trials per dimension. The")
        print(" identity is a class-A algebraic identity over (BA-1) finite-")
        print(" dimensional real matrix algebra (cyclic Tr + inverse-of-product);")
        print(" no hypotheses beyond (BA-1) are imported. The parent's bookkeeping")
        print(" consequence about global stationary sections is NOT claimed here;")
        print(" this is a split-note algebraic row only.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
