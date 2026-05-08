"""
Exact SU(3) tensor product decomposition (Clebsch-Gordan series).

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

Algorithm
---------
For SU(3) irreps λ=(p,q), the tensor product (p_1,q_1) ⊗ (p_2,q_2)
decomposes into irreps with multiplicities given by an explicit formula
(Speiser, or Coleman, or Greiner-Müller §8.5).

Implementation: we use the "young diagram" approach via partition arithmetic.
For SU(3), partition λ = (p+q, q, 0).  Tensor product with (1,0) or (0,1)
gives explicit formulas.  General tensor products are computed by iterating
single-row tensors using the standard recursion.

Verification
------------
Test against well-known cases:
    3 ⊗ 3 = 6 + 3̄
    3 ⊗ 3̄ = 1 + 8
    8 ⊗ 8 = 1 + 8 + 8 + 10 + 10̄ + 27
    3 ⊗ 6 = 8 + 10
    3 ⊗ 6̄ = 3̄ + 15
    6 ⊗ 6 = 6̄ + 15 + 15'  [where 15 = (2,1), 15' = (4,0)]

References
----------
Greiner-Müller §8.5; Slansky 1981 §3; King 1971; Speiser 1964.
"""

from __future__ import annotations

from functools import lru_cache


def dim_su3(p, q):
    return ((p + 1) * (q + 1) * (p + q + 2)) // 2


def conjugate_pq(lam):
    return (lam[1], lam[0])


# ---------------------------------------------------------------------------
# Tensor product (p1, q1) ⊗ (p2, q2) for SU(3)
# ---------------------------------------------------------------------------
# Standard formula (Coleman 1965, Greiner-Müller §8.5):
#
# (p1, q1) ⊗ (p2, q2) = sum over (a, b) and (c, d) and (e, f) such that...
#
# For our purposes, we use the iterative recursion:
# Start with (p2, q2).  Tensor with each (1,0) p1 times to get (p1, q1=0)
# in front (using (1,0) ⊗ (p,q) = (p+1,q) + (p-1, q+1) + (p, q-1)),
# then tensor with (0,1) q1 times.
#
# Equivalently, the multiplicity formula (Schwinger / Biedenharn):
#
# N^{(p,q)}_{(p_1,q_1), (p_2,q_2)} = number of ways to fill a Young
# diagram such that ... (rule complicated).
#
# We implement via direct iteration:

@lru_cache(maxsize=None)
def fund_tensor(p, q):
    """(1,0) ⊗ (p,q): list of (p',q') irreps, each with multiplicity 1."""
    out = [(p + 1, q)]
    if p >= 1:
        out.append((p - 1, q + 1))
    if q >= 1:
        out.append((p, q - 1))
    return out


@lru_cache(maxsize=None)
def antifund_tensor(p, q):
    """(0,1) ⊗ (p,q): list of (p',q') irreps, each with multiplicity 1."""
    out = [(p, q + 1)]
    if q >= 1:
        out.append((p + 1, q - 1))
    if p >= 1:
        out.append((p - 1, q))
    return out


def tensor_product_with_count(d1, d2):
    """Compute tensor product of two SU(3) reps given as multiplicity dicts.

    d1, d2: dict {(p,q): multiplicity}.

    Returns: dict {(p,q): multiplicity}.
    """
    out = {}
    for (p1, q1), m1 in d1.items():
        for (p2, q2), m2 in d2.items():
            mult = m1 * m2
            for irrep in tensor_pq_pq(p1, q1, p2, q2):
                out[irrep] = out.get(irrep, 0) + mult
    return out


@lru_cache(maxsize=None)
def tensor_pq_pq(p1, q1, p2, q2):
    """Compute (p1, q1) ⊗ (p2, q2) for SU(3).

    Returns a tuple (with possible repetitions for multiplicity > 1) of
    (p, q) labels of irreps in the decomposition.

    Algorithm: iterate p1 fundamentals + q1 antifundamentals applied to
    (p2, q2), using fund_tensor and antifund_tensor.  Track multiplicities
    via dict accumulator.
    """
    # Start with (p2, q2)
    current = {(p2, q2): 1}
    # Apply fundamental p1 times
    for _ in range(p1):
        new = {}
        for (p, q), m in current.items():
            for irrep in fund_tensor(p, q):
                new[irrep] = new.get(irrep, 0) + m
        current = new
    # Apply antifundamental q1 times
    for _ in range(q1):
        new = {}
        for (p, q), m in current.items():
            for irrep in antifund_tensor(p, q):
                new[irrep] = new.get(irrep, 0) + m
        current = new
    # Return as (irrep, multiplicity) pairs
    # But we computed (p2,q2) ⊗ ((1,0)^p1 ⊗ (0,1)^q1)
    # which contains (p1, q1) plus other stuff.  This is NOT the same as
    # (p1, q1) ⊗ (p2, q2) because (1,0)^p1 ⊗ (0,1)^q1 contains many irreps,
    # only one being (p1, q1).
    #
    # CORRECT approach: project onto the (p1, q1)-isotypic component first,
    # then tensor with (p2, q2).  This is what the LR rule does.

    # The above WRONG.  Let me redo.
    raise NotImplementedError("Wrong approach; see tensor_pq_pq_v2.")


def tensor_pq_pq_v2(p1, q1, p2, q2):
    """Compute (p1, q1) ⊗ (p2, q2) decomposition.

    Standard SU(3) tensor product formula (Greiner-Müller §8.5 or
    Coleman 1965): for partition λ_1 = (p1+q1, q1, 0) and λ_2 = (p2+q2, q2, 0),
    the LR rule gives the multiplicities.

    Implementation: for SU(3) we use the explicit "Young-tableau-fill"
    approach.  Place p2 boxes labeled '1' and q2 boxes labeled '2' into
    the Young diagram of (p1,q1) such that:
        - In each row, the labels are non-decreasing
        - In each column, the labels are strictly increasing
        - The "lattice property" of the resulting word holds

    For SU(3) (3-row diagrams), we can use a much simpler closed form via
    the decomposition recipes due to King 1971 / Black-King-Wybourne.

    Practical implementation via SymPy-style:
    """
    # Use the Speiser/Coleman closed form for SU(3) tensor products.
    # The formula is:
    #
    # (p1,q1) ⊗ (p2,q2) =
    #   ⊕_{a=0}^{min(p1,p2)} ⊕_{b=0}^{min(q1,q2)} ⊕_{c=0}^{min(p1-a, q2-b)} ⊕_{d=0}^{min(q1-b, p2-a)}
    #   (p1+p2-a-d-c, q1+q2-b-c-d)  [if non-negative...]
    #   times multiplicity given by complicated combinatorics.
    #
    # Simpler: use sympy for tensor product decomposition.
    try:
        from sympy.physics.quantum.cg import CG
        # No straightforward sympy SU(3) routine; we'll implement directly.
    except ImportError:
        pass

    # Direct algorithm: use the well-known fact that (p1, q1) ⊗ (p2, q2)
    # can be computed by repeatedly applying the LR rule for 3-row partitions.
    #
    # For SU(3), partition (p+q, q, 0) corresponds to irrep (p, q).
    # The LR rule: the multiplicity of (μ_1, μ_2, μ_3) in (λ_1, λ_2, λ_3)
    # ⊗ (ν_1, ν_2, ν_3) equals the number of LR tableaux of shape μ/λ
    # and content ν.

    # We use sympy's permutation module to count.
    # OR: implement directly via standard SU(3) recursion.

    # Actually, the simplest implementation is via repeated tensoring with
    # fund/antifund, but iterating (p1,q1) builders correctly.
    #
    # Build (p1, q1) as the highest-weight component of (1,0)^p1 ⊗ (0,1)^q1.
    # By the cancellation rule: (1,0) ⊗ (0,1) = (1,1) + (0,0), so we get
    # both (p1, q1) and lower-rank irreps.  Thus (1,0)^p1 ⊗ (0,1)^q1 ≠ (p1, q1).

    # Correct approach: USE THE LR RULE directly.
    return _LR_decomp_su3((p1, q1), (p2, q2))


def _LR_decomp_su3(lam1, lam2):
    """Decompose (p1,q1) ⊗ (p2,q2) using direct iteration over the smaller rep.

    Strategy: iterate over the GT (Gelfand-Tsetlin) basis of lam2 and use
    the rule that

        (p1,q1) ⊗ (p2,q2) = ⊕ (p_,q_) with multiplicities

    Direct algorithm from Klimyk-Vilenkin Vol 3 or implementational practice:

    Use weight-multiplicity table for each irrep.  Tensor of irreps has
    weight-multiplicity = convolution of individual weight multiplicities.
    Then decompose into irreps via Weyl character formula (lighten by
    Casimir-eigenvalue ordering).

    For SU(3) this is tractable for small irreps.

    Implementation here: use the partitioning of weight space.
    """
    # Get weight multiplicities for each irrep
    wm1 = weight_multiplicity_su3(*lam1)
    wm2 = weight_multiplicity_su3(*lam2)

    # Convolve weights
    wm_prod = {}
    for w1, m1 in wm1.items():
        for w2, m2 in wm2.items():
            w_sum = (w1[0] + w2[0], w1[1] + w2[1])
            wm_prod[w_sum] = wm_prod.get(w_sum, 0) + m1 * m2

    # Now decompose into irreps by greedy highest-weight subtraction.
    # SU(3) irreps have unique highest weight; we iterate starting from
    # the highest weight present in wm_prod.

    decomp = {}
    while wm_prod:
        # Find highest weight: in dominant chamber.
        # Dominant SU(3) weights: (a, b) with a ≥ 0, b ≥ 0 wait but our
        # weights are integer pairs in some basis.  We use the convention
        # (m_1, m_2) where m_1 = number of fundamentals minus number of
        # anti-fundamentals along axis 1 (3 dim weights collapsed to 2).
        # Actually let me be very careful.

        # Reset: SU(3) weights are 2-dim, in the basis of (e_1 - e_2) and
        # (e_2 - e_3) for the simple roots... use Dynkin labels (m, n).

        # Highest weight of irrep (p, q) in Dynkin labels = (p, q).
        # General weight in Dynkin labels: (a, b) ∈ Z².
        # Dominant: a ≥ 0, b ≥ 0.

        # Our weight-multiplicity dict's keys should be Dynkin pairs.
        # Let's use this convention throughout.

        # Find highest weight present: lex-max (a + 2b, a) gives a unique
        # highest in dominant chamber.
        dominant = [w for w, m in wm_prod.items() if w[0] >= 0 and w[1] >= 0 and m > 0]
        if not dominant:
            break
        # Highest by sum of components weighted by Casimir
        # Use the Casimir / level test: irrep (p, q) has highest weight
        # (p, q), and (p, q) > (p', q') if (p+q, q) > (p'+q', q') lex.
        hw = max(dominant, key=lambda w: (w[0] + w[1], w[0]))
        p, q = hw
        m_hw = wm_prod[hw]
        decomp[(p, q)] = decomp.get((p, q), 0) + m_hw

        # Subtract weight multiplicities of (p, q)
        wm_pq = weight_multiplicity_su3(p, q)
        for w, mult in wm_pq.items():
            wm_prod[w] = wm_prod.get(w, 0) - m_hw * mult
            if wm_prod[w] <= 0:
                if wm_prod[w] < 0:
                    # Should not happen if weights are correct
                    pass
                wm_prod.pop(w)

    return decomp


@lru_cache(maxsize=None)
def weight_multiplicity_su3(p, q):
    """Weight-multiplicity dict for SU(3) irrep (p, q) in Dynkin labels.

    Returns dict {(a, b): multiplicity} where (a, b) are the Dynkin labels
    of the weight (eigenvalues of the two simple roots).

    Algorithm: Freudenthal recursion or direct enumeration of weight space.

    For SU(3): the weight diagram is a hexagon (or triangle for (p,0) or (0,q)).
    The weights of (p, q) are obtained from the highest weight (p, q) by
    iterated subtraction of simple roots α_1 = (2, -1), α_2 = (-1, 2).
    Multiplicities: distance from boundary in shells.
    """
    # Start with highest weight (p, q) at multiplicity 1.
    # Generate all weights in the convex hull = Weyl orbit + shells.
    weights = {}
    # Use the "shell" formula for SU(3): weights with multiplicity equal to
    # the layer number (1, 2, 3, ...) up to min(p, q), then constant min(p,q)+1, then decrease.

    # Weights are in Dynkin basis.  Highest weight = (p, q).
    # Subtract simple roots: α_1 = (2, -1), α_2 = (-1, 2).
    # The reflection group: (a, b) → (-a, a+b), (a+b, -b) [s_1, s_2]
    # The Weyl group has 6 elements (= S_3).

    # Algorithm: BFS from (p, q), subtracting α_1, α_2, building a queue
    # of weights to process.  For each weight, the multiplicity is given
    # by Kostant's partition function or Freudenthal recursion.

    # For SU(3) there's a closed form: the multiplicity of weight (a, b)
    # in irrep (p, q) is the number of "shells" at depth d, where the
    # depth is min over weights' distances to boundary.

    # Simpler: enumerate via Freudenthal recursion.
    # Freudenthal: for weight w in irrep with highest weight Λ:
    #   ((Λ + ρ, Λ + ρ) - (w + ρ, w + ρ)) m(w)
    #     = 2 Σ_{α > 0} Σ_{k > 0} (w + k α, α) m(w + k α)
    #
    # where ρ = (1, 1) (half-sum of positive roots), and (·, ·) is the
    # Killing-form-induced bilinear form.

    # Bilinear form for SU(3) Dynkin basis (a, b) → use the formula
    # (a, b) · (c, d) = (1/3) (2 a c + a d + b c + 2 b d) ... let me get this right.

    # For SU(3), the inverse Cartan matrix is (1/3)[[2, 1], [1, 2]].
    # So in Dynkin basis (where simple roots have length 2), the inner
    # product is:
    # (a, b) · (c, d) in Dynkin basis = (1/3) (2ac + ad + bc + 2bd).

    # Highest weight Λ = (p, q).  Λ + ρ = (p+1, q+1).
    # |Λ + ρ|² = (1/3)(2(p+1)² + 2(p+1)(q+1) + 2(q+1)²)
    #          = (2/3)((p+1)² + (p+1)(q+1) + (q+1)²)

    def inner(u, v):
        return (2 * u[0] * v[0] + u[0] * v[1] + u[1] * v[0] + 2 * u[1] * v[1]) / 3.0

    rho = (1, 1)
    Lambda = (p, q)
    Lambda_plus_rho = (Lambda[0] + rho[0], Lambda[1] + rho[1])

    # Generate all weights ≤ Λ in dominance order.
    # Weight w ≤ Λ iff Λ - w is a non-negative integer combination of simple
    # roots: Λ - w = n_1 α_1 + n_2 α_2 with n_1, n_2 ≥ 0.
    # In Dynkin labels: Λ - w = (2 n_1 - n_2, -n_1 + 2 n_2) = α_1 = (2,-1), α_2 = (-1,2).
    # Equivalently: n_1 = (2 (Λ-w)_0 + (Λ-w)_1) / 3, n_2 = ((Λ-w)_0 + 2 (Λ-w)_1) / 3.

    # Enumerate (n_1, n_2) with n_1, n_2 >= 0.  The maximum n_1 + n_2 is
    # bounded by p + q (since the lowest weight of (p, q) is at depth
    # p + q from the highest).  More tightly, we can iterate up to
    # n_1 ≤ p+q, n_2 ≤ p+q.  We then check if w = Λ - n_1 α_1 - n_2 α_2
    # is in the convex hull (by Weyl-symmetry).

    weights_to_visit = []
    weight_mults = {}
    # BFS from highest weight
    weights_to_visit.append((Lambda, 1))
    weight_mults[Lambda] = 1
    # Generate all weights via subtraction of simple roots
    queue = [Lambda]
    visited = {Lambda}
    while queue:
        w = queue.pop(0)
        for alpha in [(2, -1), (-1, 2)]:
            w_new = (w[0] - alpha[0], w[1] - alpha[1])
            if w_new not in visited:
                # Check if w_new is in the irrep weight-set: it must be in
                # the convex hull of Weyl orbit of Λ.  Equivalent: Λ - w_new
                # is a non-neg combo of simple roots.
                diff = (Lambda[0] - w_new[0], Lambda[1] - w_new[1])
                # diff = n_1 α_1 + n_2 α_2 = (2 n_1 - n_2, -n_1 + 2 n_2)
                # n_1 = (2 diff_0 + diff_1) / 3, n_2 = (diff_0 + 2 diff_1) / 3
                num1 = 2 * diff[0] + diff[1]
                num2 = diff[0] + 2 * diff[1]
                if num1 % 3 == 0 and num2 % 3 == 0:
                    n_1 = num1 // 3
                    n_2 = num2 // 3
                    if n_1 >= 0 and n_2 >= 0:
                        # Now also check w_new is in the convex hull:
                        # all 6 Weyl images must satisfy "≤ Λ" condition.
                        if _is_in_irrep_su3(w_new, Lambda):
                            visited.add(w_new)
                            queue.append(w_new)

    # Now compute multiplicities by Freudenthal recursion.
    # Visit weights in decreasing order (closest to Λ first).
    # Order by (Λ - w) "level" = n_1 + n_2.

    def level(w):
        diff = (Lambda[0] - w[0], Lambda[1] - w[1])
        n_1 = (2 * diff[0] + diff[1]) // 3
        n_2 = (diff[0] + 2 * diff[1]) // 3
        return n_1 + n_2

    sorted_weights = sorted(visited, key=lambda w: level(w))

    Lambda_pr_norm = inner(Lambda_plus_rho, Lambda_plus_rho)
    for w in sorted_weights:
        if w == Lambda:
            weight_mults[w] = 1
            continue
        w_pr = (w[0] + rho[0], w[1] + rho[1])
        diff_norm = Lambda_pr_norm - inner(w_pr, w_pr)
        if abs(diff_norm) < 1e-10:
            # w + ρ = ±(Λ + ρ); never happens for w < Λ in convex hull
            continue
        # Sum over positive roots and k > 0
        total = 0.0
        for alpha in [(2, -1), (-1, 2), (1, 1)]:  # positive roots in Dynkin basis
            k = 1
            while True:
                w_plus_k_alpha = (w[0] + k * alpha[0], w[1] + k * alpha[1])
                if w_plus_k_alpha not in weight_mults:
                    break
                total += inner(w_plus_k_alpha, alpha) * weight_mults[w_plus_k_alpha]
                k += 1
        m = 2.0 * total / diff_norm
        weight_mults[w] = int(round(m))

    # Strip zero multiplicities
    weight_mults = {w: m for w, m in weight_mults.items() if m > 0}

    return weight_mults


def _is_in_irrep_su3(w, Lambda):
    """Check if weight w is in the weight-set of irrep with highest weight Lambda.

    A weight w is in the irrep iff w ≤ Λ in the dominance order, which for
    SU(3) means: for every Weyl image w' of w, Λ - w' ∈ Z_{≥0}-span of simple roots.

    Simpler test: w is in the convex hull of the Weyl orbit of Λ.  For SU(3),
    we can check via the 6 Weyl reflections.
    """
    # Weyl orbit of Λ: 6 elements (or 3 for (p, 0) or (0, q), or 1 for (0, 0)).
    p, q = Lambda
    orbit = set()
    orbit.add((p, q))
    orbit.add((-p, p + q))
    orbit.add((p + q, -q))
    orbit.add((-p - q, p))
    orbit.add((q, -p - q))
    orbit.add((-q, -p))

    # w must be ≤ each element of orbit in dominance, i.e., each orbit_el - w
    # is a non-negative integer combination of simple roots (2,-1) and (-1, 2).
    # The "convex hull" check: we just need that w + ρ has all 6 Weyl-orbit
    # transforms satisfy the constraint.  But the simpler check: w must lie
    # inside the convex polytope.
    # Equivalent: Λ - w = n_1 α_1 + n_2 α_2 with n_1, n_2 ≥ 0 (already checked)
    # AND the same for all Weyl images of Λ.

    for el in orbit:
        diff = (el[0] - w[0], el[1] - w[1])
        num1 = 2 * diff[0] + diff[1]
        num2 = diff[0] + 2 * diff[1]
        if num1 % 3 != 0 or num2 % 3 != 0:
            return False
        n_1 = num1 // 3
        n_2 = num2 // 3
        # We need n_1 + n_2 (sum) compatible with "w in convex hull"
        # Actually the convex hull condition is just that ALL Weyl images
        # have non-negative LR coefficients?  No, that's too strong.
        # Standard fact: w is in irrep iff it is dominated by Λ, equivalently
        # (after applying Weyl group to bring w into dominant chamber)
        # the dominant w_+ is bounded by Λ.

    # Simplification: use the dominant-chamber check
    # Bring w to dominant chamber via Weyl reflections
    a, b = w
    # Apply s_1 if a < 0, s_2 if b < 0, repeatedly.
    for _ in range(20):
        if a >= 0 and b >= 0:
            break
        if a < 0:
            a, b = -a, a + b
        elif b < 0:
            a, b = a + b, -b
    # Now (a, b) is dominant.
    # w in irrep (p, q) iff a ≤ p and b ≤ q (in dominance order),
    # AND a + b ≤ p + q AND (p - a) ≡ (q - b) mod 3 (center character matches).
    # Actually for SU(3), the convex hull in dominant chamber: dominant
    # weight (a, b) is in (p, q) iff:
    #   a ≤ p, b ≤ q  (this is "leq Λ in usual dominance")  → no this is too strong
    # The correct condition: (p - a, q - b) must be expressible as non-neg
    # integer combo of (2, -1) and (-1, 2).  i.e., 2(p-a) - (q-b) ≥ 0 and
    # 2(q-b) - (p-a) ≥ 0 and integer.
    diff_a = p - a
    diff_b = q - b
    num1 = 2 * diff_a + diff_b
    num2 = diff_a + 2 * diff_b
    if num1 < 0 or num2 < 0:
        return False
    if num1 % 3 != 0 or num2 % 3 != 0:
        return False
    return True


# ---------------------------------------------------------------------------
# Main tensor product entry point
# ---------------------------------------------------------------------------

def tensor_decomp(lam1, lam2):
    """Compute (p1, q1) ⊗ (p2, q2) decomposition.

    Returns: dict {(p, q): multiplicity}.
    """
    return _LR_decomp_su3(lam1, lam2)


def n_invariant(irreps):
    """Compute multiplicity of trivial rep in tensor product of irreps.

    irreps: list of (p, q).
    Returns: integer multiplicity.
    """
    if len(irreps) == 0:
        return 1
    if len(irreps) == 1:
        p, q = irreps[0]
        return 1 if (p, q) == (0, 0) else 0
    # Reduce iteratively
    current = {irreps[0]: 1}
    for nxt in irreps[1:]:
        new = {}
        for (p, q), m in current.items():
            d = tensor_decomp((p, q), nxt)
            for irrep, mu in d.items():
                new[irrep] = new.get(irrep, 0) + m * mu
        current = new
    return current.get((0, 0), 0)


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 72)
    print("Exact SU(3) Clebsch-Gordan decomposition self-test")
    print("=" * 72)

    # Weight multiplicities for low irreps
    print("\n[1] Weight multiplicities")
    for lam in [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (3, 0), (2, 1), (2, 2)]:
        wm = weight_multiplicity_su3(*lam)
        total = sum(wm.values())
        print(f"  ({lam[0]},{lam[1]}): dim={dim_su3(*lam)}, total weights={total}, "
              f"{'OK' if total == dim_su3(*lam) else 'FAIL'}")

    # Tensor products
    print("\n[2] Tensor product decompositions")

    # 3 ⊗ 3 = 6 + 3̄
    d = tensor_decomp((1, 0), (1, 0))
    print(f"  3 ⊗ 3 = {d}")
    print(f"    expected: 6 (=2,0) + 3̄ (=0,1)")
    assert d == {(2, 0): 1, (0, 1): 1}

    # 3 ⊗ 3̄ = 1 + 8
    d = tensor_decomp((1, 0), (0, 1))
    print(f"  3 ⊗ 3̄ = {d}")
    print(f"    expected: 1 + 8")
    assert d == {(0, 0): 1, (1, 1): 1}

    # 8 ⊗ 8 = 1 + 8 + 8 + 10 + 10̄ + 27
    d = tensor_decomp((1, 1), (1, 1))
    print(f"  8 ⊗ 8 = {d}")
    print(f"    expected: 1 + 8 + 8 + 10 + 10̄ + 27")
    assert d == {(0, 0): 1, (1, 1): 2, (3, 0): 1, (0, 3): 1, (2, 2): 1}

    # 3 ⊗ 6 = 8 + 10
    d = tensor_decomp((1, 0), (2, 0))
    print(f"  3 ⊗ 6 = {d}")
    print(f"    expected: 8 + 10")
    assert d == {(1, 1): 1, (3, 0): 1}

    # 3 ⊗ 6̄ = 3̄ + 15
    d = tensor_decomp((1, 0), (0, 2))
    print(f"  3 ⊗ 6̄ = {d}")
    print(f"    expected: 3̄ + 15")
    assert d == {(0, 1): 1, (1, 2): 1}

    # 6 ⊗ 6 = 6̄ + 15 + 15'
    # where 15 = (2,1), 15' = (4,0)
    d = tensor_decomp((2, 0), (2, 0))
    print(f"  6 ⊗ 6 = {d}")
    print(f"    expected: 6̄ + 15 + 15' (= 0,2 + 2,1 + 4,0)")
    assert d == {(0, 2): 1, (2, 1): 1, (4, 0): 1}

    # n_invariant tests
    print("\n[3] Trivial rep multiplicities")
    print(f"  3 ⊗ 3̄ → 1: {n_invariant([(1, 0), (0, 1)])}  (expected 1)")
    print(f"  3 ⊗ 3 ⊗ 3 → 1: {n_invariant([(1, 0), (1, 0), (1, 0)])}  (expected 1)")
    print(f"  3 ⊗ 3 ⊗ 3̄ ⊗ 3̄ → 1: {n_invariant([(1, 0), (1, 0), (0, 1), (0, 1)])}  (expected 2)")
    print(f"  8 ⊗ 8 → 1: {n_invariant([(1, 1), (1, 1)])}  (expected 1)")
    print(f"  8 ⊗ 8 ⊗ 8 → 1: {n_invariant([(1, 1), (1, 1), (1, 1)])}  (expected 2: (Tr d_abc, Tr f_abc))")

    # Check that n_invariant matches MC-Haar projector dimensions
    # (for verification cross-check when MC machinery is also working)
    print("\n[4] Done.")
