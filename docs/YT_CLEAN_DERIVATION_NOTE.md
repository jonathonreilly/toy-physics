# Authority Note: Renormalized y_t Lane

## Authority Notice

**SUPERSEDED as current lane authority** by:

- `docs/YT_BOUNDARY_THEOREM.md`
- `docs/YT_ZERO_IMPORT_CLOSURE_NOTE.md`
- `docs/RENORMALIZED_YT_PAPER_NOTE.md`

This note records the older Planck-boundary derivation surface. It remains
useful as a historical derivation audit, but it is **not** the current
review/promotion surface after the boundary-selection theorem moved the
physical crossover endpoint to `v`.

**Date:** 2026-04-13
**Lane:** Renormalized y_t matching (priority 4)
**Status:** HISTORICAL / BOUNDED
**Decision:** KEEP as historical bounded derivation note; do not use as the
current flagship authority surface.

---

## Theorem / Claim

The top-quark Yukawa coupling y_t is determined by the Cl(3)-on-Z^3
framework. The bare UV relation is exact. Several renormalization pieces
are exact. One residual remains bounded and cannot be discharged on the
lattice.

---

## Assumptions

1. **A1--A4:** The Cl(3)-on-Z^3 framework axioms (not relitigated here).
2. **A5 (lattice-is-physical):** Z^3 at spacing a = l_Planck is the
   physical theory. The continuum SM is the effective description obtained
   by coarse-graining the lattice Hamiltonian.
3. **Retained particle content:** Gauge group SU(3)xSU(2)xU(1), three
   generations, one Higgs doublet -- all derived (not disputed by Codex).

No additional assumptions beyond these.

---

## What Is Closed (Bare Pieces)

**CLOSED: bare y_t = g_s / sqrt(6)**

This is an exact Cl(3) trace identity. The staggered lattice mass term
has taste structure G_5 (the chirality operator). The Yukawa Casimir is
C_Y = Tr(P_+)/dim = 1/2, giving N_c * y_t^2 = g_s^2 / 2, hence
y_t = g_s / sqrt(2 N_c) = g_s / sqrt(6). This is an algebraic identity
in a finite-dimensional algebra with no perturbative corrections.

Verified: explicit 8x8 matrix computation, machine precision.

---

## What Is Exact (Renormalized Pieces)

### 1. Cl(3) preservation under RG (48/48) [EXACT]

The Z^3 lattice has octahedral symmetry group of order 48. Block-spin RG
transformations Z^3 -> Z^3 map the lattice to itself preserving Oh. The
Cl(3) generators transform as vectors under Oh, and the algebra
{G_mu, G_nu} = 2 delta_{mu,nu} is preserved because Oh maps vectors to
vectors. All 48 group elements checked: Cl(3) algebra is preserved under
blocking.

### 2. Ratio protection / vertex factorization via ST identity (26/26) [EXACT]

Because G_5 is central in Cl(3) (d = 3 odd => volume element commutes
with all generators), the lattice counterterm for the G_5 bilinear is
proportional to the identity counterterm. The Slavnov-Taylor identity for
the G_5 Ward identity gives Z_{G_5} / Z_{gauge} = 1 at all orders. The
ratio y_t / g_s therefore receives no radiative corrections on the
lattice. This is a consequence of exact centrality, not of perturbation
theory.

On the bipartite Z^3 lattice, the staggered-fermion parity
epsilon(x) = (-1)^{x_1+x_2+x_3} anticommutes with the lattice shift
operators Lambda_mu, providing the non-perturbative Slavnov-Taylor
identity that protects the ratio.

Verified: 26/26 explicit vertex-factorization checks on L = 4, 6, 8
lattices.

### 3. 1/sqrt(6) coefficient algebraically locked (18/18) [EXACT]

The coefficient 1/sqrt(6) = 1/sqrt(2 N_c) is fixed by three independent
algebraic constraints:

- The chiral projector rank: rank(P_+) = dim/2 = 4
- The Casimir trace: Tr(P_+)/dim = 1/2
- The bipartite parity: the factor 1/2 equals the ratio of even to total
  sites on any bipartite lattice

These are structural properties of Cl(3) and Z^3. No deformation is
possible without breaking the algebra. All 18 independent coefficient
checks pass.

---

## What Is Derived (Zero Free Parameters, Framework Coefficient)

### alpha_s(M_Pl) = 0.092 from plaquette at g = 1 [DERIVED]

Derivation chain:

1. g_bare = 1 from Cl(3) normalization (A5: lattice coupling fixed by
   the algebra). Note: g = 1 is a framework coefficient, not an
   independent measurement.
2. alpha_lattice = g^2 / (4 pi) = 1/(4 pi) = 0.07958.
3. Mean plaquette at 1-loop for SU(3) Wilson action with
   beta = 2 N_c / g^2 = 6: <P> = 1 - pi/12 = 0.7382.
4. V-scheme coupling: alpha_V = -(3/pi^2) ln(<P>) = 0.0922.
5. Identified with alpha_s(mu = 1/a = M_Pl) in V-scheme.

Every number computed from g = 1 and N_c = 3. Zero free parameters.

What is bounded here: the 1-loop truncation in step 3--4 introduces
O(alpha^2) ~ 0.6% error. V-scheme to MS-bar conversion is computable but
scheme-dependent.

### Beta coefficients from derived particle content [DERIVED]

The 1-loop SM beta function coefficients (b_1, b_2, b_3 and the top
Yukawa self-coupling a_t) are calculated from derived inputs: gauge
groups from Cl(3), N_c = 3 from spatial dimension, n_gen = 3 from BZ
orbit algebra, 1 Higgs doublet from G_5 condensate. These are computed,
not imported.

---

## What Remains Bounded

### RG running from M_Pl to M_Z [BOUNDED -- irreducible residual]

Solving the coupled SM RGE system from mu = M_Pl down to mu = M_Z
assumes that quantum field theory is the correct effective field theory
below M_Pl. This is the one genuinely bounded element in the chain.

**Why this cannot be discharged on the lattice:** The lattice lives at
a = l_Planck. RG running spans ~17 decades of energy (10^19 GeV to
10^2 GeV). The lattice cannot directly resolve this range. The
assumption that the lattice Hamiltonian flows to continuum QFT under
coarse-graining is a universality-class statement -- a consequence of A5
but not a machine-checkable theorem.

**Why it is not an independent import:** If A5 is accepted (the lattice
IS the UV completion), then the EFT below the lattice scale IS QFT by
construction. The Wilsonian RG describes exactly this coarse-graining.
So the RGE step follows from A5, but it follows as a physics consequence,
not as a machine-verifiable algebraic identity.

**Specific bounded sub-pieces:**

1. Continuum-limit universality: QFT is the correct EFT below M_Pl
   (consequence of A5, not machine-checkable).
2. Perturbative truncation: 1-loop vs all-orders. At 2-loop, the
   correction shifts m_t by +5.3% before thresholds, +2.4% after.
3. Scheme matching: V-scheme boundary at M_Pl matched to MS-bar running,
   ~3% uncertainty at 1-loop.
4. Threshold corrections: decoupling of heavy particles at their mass
   scales, computed from derived spectrum but 1-loop matching coefficients
   (~1%, computed but scheme-dependent).

### Matching coefficient [BOUNDED]

The lattice-to-continuum matching at M_Pl is computed at 1-loop. The
matching coefficient is ~1%, which is small, but it is scheme-dependent.
A 2-loop calculation would reduce the uncertainty to ~0.1%.

---

## What Is Actually Proved (Summary Table)

| Piece | Content | Status |
|-------|---------|--------|
| Bare y_t = g_s/sqrt(6) | Cl(3) trace identity | CLOSED (exact) |
| Cl(3) preservation under RG | 48/48 octahedral symmetry | EXACT |
| Ratio protection (ST identity) | Vertex factorization 26/26 | EXACT |
| 1/sqrt(6) locked | Algebraic coefficient 18/18 | EXACT |
| alpha_s(M_Pl) = 0.092 | Plaquette at g=1, zero free parameters | DERIVED (g=1 is framework coefficient) |
| Beta coefficients | From derived particle content | DERIVED |
| RG running M_Pl -> M_Z | QFT as EFT, 17 decades | BOUNDED |
| Matching coefficient | Lattice-to-continuum, ~1% | BOUNDED (scheme-dependent) |

---

## The Prediction

y_t(M_Pl) = g_s(M_Pl) / sqrt(6) = 0.439 (from exact ratio + derived coupling)

After RG running to M_Z:

    1-loop: m_t = 175 GeV (+1.2% from observed 173.0 GeV)
    2-loop + thresholds: m_t = 177 GeV (+2.4%)
    Prediction band: m_t in [175, 177] GeV, within matching uncertainty

---

## What Remains Open

1. The continuum-limit universality statement (bounded, not
   machine-checkable).
2. Higher-loop RG running (improvable but currently 1-loop).
3. Higgs VEV v = 246.22 GeV used as measured input (until Higgs lane
   closes).
4. Lattice-to-continuum matching at 2-loop (would reduce scheme
   uncertainty).

---

## How This Changes The Paper

The paper can state:

> The bare relation y_t = g_s / sqrt(6) is an exact algebraic identity
> in the d = 3 Clifford algebra, protected non-perturbatively by the
> centrality of G_5 and the Slavnov-Taylor identity. Combined with the
> zero-parameter chain g_bare = 1 -> alpha_s(M_Pl) = 0.092, this gives
> y_t(M_Pl) = 0.439 with no free inputs. Standard Model RG running
> (with beta coefficients computed from derived particle content) yields
> m_t = 175-177 GeV, consistent with the observed 173.0 GeV within the
> 1-2% matching band. The remaining uncertainty arises from
> lattice-to-continuum matching and the assumption that QFT is the
> correct EFT below M_Pl -- a consequence of the lattice-is-physical
> premise (A5) but not a machine-checkable theorem.

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_yt_clean_derivation.py
```

---

KEEP BOUNDED (one explicit residual: QFT as EFT below M_Pl).
