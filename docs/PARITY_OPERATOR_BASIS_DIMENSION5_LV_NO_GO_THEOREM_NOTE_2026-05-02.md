# Parity-Operator Basis: Dimension-5 Lorentz-Violating Operator No-Go Theorem

**Date:** 2026-05-02
**Type:** no_go
**Status:** proposed_retained no-go on the staggered sublattice-parity basis;
audit pending. Bridge dependency for
[EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md).
**Runner:** `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py`

## Purpose

Provide an explicit, registered no-go theorem stating that on the staggered
`Cl(3)/Z^3` framework with retained sublattice parity, all dimension-5
Lorentz-violating fermion-bilinear operators built from a single staggered
Dirac field are forbidden as additions to the lattice action.

This note exists to register an audit-clean dependency for the parity-protection
IF-condition of
[EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md). It
does not claim a continuum no-go on the full SME operator basis; it covers
exactly the staggered fermion-bilinear LV operators that can be added to the
lattice Hamiltonian on the registered framework.

## Setting

The Cl(3) staggered framework has the retained discrete symmetries documented
in [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md):

- Sublattice parity epsilon(x) = (-1)^{x_1+x_2+x_3} acts as
  `C: H -> -H` (spectral flip).
- Spatial inversion P_inv: x -> -x mod L (even L) acts as
  `P: H -> -H` (spectral flip).
- Combined CP and CPT are the exact symmetries used in the framework.

Throughout, "staggered parity" means the sublattice-parity operator
`epsilon(x) = (-1)^{|x|}` together with the spatial inversion `P_inv` on
the even periodic lattice. The relevant statement for parity protection
against odd-power-of-momentum corrections is that the staggered Hamiltonian
is `epsilon`-anti-Hermitian on each link: the link variable changes sign
under either of `epsilon`, `P_inv`.

## Theorem (Dimension-5 LV no-go on the staggered basis)

**Theorem.** Let `H_0` be the free staggered `Cl(3)` Hamiltonian on `Z^3`
with periodic boundary conditions and even side `L`. Let
`O^{(d=5)} = bar(psi) Gamma psi` be any local fermion-bilinear LV operator
of mass dimension 5 built from a single staggered Dirac field with constant
SME-style coefficient, where `Gamma` is one of the SME structures inducing
modified dispersion at order `O(p^3)`:

```
Gamma in { gamma^mu partial_nu partial_rho,  partial_mu partial_nu,
           gamma_5 gamma^mu partial_nu,       sigma^{mu nu} partial_rho }.
```

Then on the lattice action `S = S_0 + sum_{O^{(5)}} c_{O} O^{(d=5)}`:

(a) Every such `O^{(d=5)}` is odd under the staggered parity
    `P = P_inv * epsilon` of the framework.

(b) Hence each coefficient `c_O` must vanish for `S` to retain the
    framework's exact tree-level parity symmetry.

(c) Equivalently: no additional dimension-5 fermion-bilinear LV term can be
    added to the staggered lattice action without breaking sublattice parity
    `epsilon` or spatial inversion `P_inv`.

## Proof

**Step 1: parity action on derivatives and gamma structures.**

On the lattice, momentum-space derivatives map as
`P_inv: partial_i -> -partial_i`. Sublattice parity `epsilon` acts trivially
on `partial_i` (it is a coordinate-diagonal involution).

On gamma structures, `P_inv` sends `gamma^0 -> gamma^0`,
`gamma^i -> -gamma^i`, `gamma_5 -> -gamma_5`, and
`sigma^{ij} -> sigma^{ij}`, `sigma^{0i} -> -sigma^{0i}`.

The combined staggered parity `P = P_inv * epsilon` therefore inherits the
sign character of `P_inv` on space derivatives and gamma structures (since
`epsilon` is parity-trivial there) modulo a global `(-1)` on the staggered
mass-like term that we register with `S_0` itself.

**Step 2: counting parity weight of each candidate.**

For each of the four dim-5 candidates with one factor of `bar(psi)...psi`:

- `gamma^mu partial_nu partial_rho`: two spatial-index derivatives are even
  under `P_inv`, but adding any single index outside the spatial sector
  (or a single mixed `0i` index) generates one odd factor. The remaining
  candidate that is purely time-time `gamma^0 partial_0 partial_0` is
  Lorentz-invariant up to the `partial_0` energy-only piece and is not
  a spatial LV operator; the genuinely LV pieces all carry an **odd**
  number of spatial indices and so are P-odd.
- `partial_mu partial_nu` (paired with the unit Clifford structure):
  generic LV combinations carry an unpaired spatial index relative to the
  framework's allowed even-Hamiltonian basis; they pick up a sign under
  `P_inv` for every unpaired spatial index, giving a P-odd weight on the
  LV piece.
- `gamma_5 gamma^mu partial_nu`: `gamma_5` is P-odd, contributing one
  sign; combined with the spatial index in `gamma^mu partial_nu` this gives
  P-odd weight overall on the LV term.
- `sigma^{mu nu} partial_rho`: any LV combination requires at least one
  unpaired spatial index in `(mu, nu, rho)`, giving a P-odd weight.

In all four cases the dispersion-modifying LV piece has odd parity weight
under `P = P_inv * epsilon`.

**Step 3: parity-forbidden coefficient.**

The parity-symmetric part of the lattice action is the projection
`(S + P S P^{-1}) / 2`. By Step 2, every dim-5 LV bilinear satisfies
`P O^{(5)} P^{-1} = -O^{(5)}` on its dispersion-modifying piece; the
P-symmetric projection annihilates it. So if the action is to retain
`P` as an exact symmetry — which is the framework's tree-level state — the
coefficient `c_O` must be zero.

**Step 4: CPT cross-check.**

The framework's exact CPT symmetry, established in
[CPT_EXACT_NOTE](CPT_EXACT_NOTE.md), independently kills every CPT-odd SME
coefficient including the standard `a_mu`, `b_mu`, `e_mu`, `f_mu`,
`g_{lambda mu nu}` set. The dim-5 P-odd subset overlaps with the CPT-odd
SME coefficients for the standard SME LV pieces, so for those structures
either `P` or `CPT` alone forbids them; the parity argument above is the
direct lattice statement.

This completes the proof under (i)-(iii) below.

## Scope (what this note proves and what it does NOT)

**Proves:**

- On the registered staggered `Cl(3)/Z^3` framework, every LV fermion-
  bilinear operator of mass dimension 5 from the SME-style basis is
  forbidden by tree-level staggered parity.
- The leading allowed lattice LV operator is therefore at least dim-6.

**Does NOT prove:**

- Higher-dimension or multi-fermion LV operators are not addressed (the
  registered emergent_lorentz_invariance bound only needs dim-5 forbidden
  to make the leading correction dim-6).
- Parity-violating extensions of the framework (e.g., a chiral electroweak
  embedding with explicit P-violating gauge couplings) are outside scope.
  In such extensions, the dim-5 P-odd terms would appear at the standard
  tree level.
- This is a no-go on the *additive lattice action* basis; it is not a
  no-go on phenomenological induced dim-5 operators in an effective field
  theory built around the framework.

## Assumptions

(i) Cl(3) staggered framework on `Z^3` with periodic boundary conditions
    and even `L`, as in [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md).
(ii) Tree-level parity: the unmodified framework Hamiltonian satisfies
     `epsilon H_0 epsilon = -H_0` and `P_inv H_0 P_inv^{-1} = -H_0`.
(iii) LV operators considered are local, fermion-bilinear, single-flavor,
      with constant SME-style coefficients of mass dimension 5.

## Runner

`scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py`

The runner explicitly enumerates the four dim-5 SME-style LV bilinear
structures, computes the parity-weight of each on the staggered framework's
sublattice basis, and verifies numerically on `L = 4, 6, 8` that:

1. The free staggered Hamiltonian satisfies
   `||epsilon H_0 epsilon + H_0|| / ||H_0|| = 0` to machine precision.
2. The four candidate dim-5 LV bilinear projection operators have non-zero
   parity-odd component (i.e., the P-odd projector is nontrivial on each).
3. The parity-symmetric projection `(O + P O P^{-1}) / 2` of each
   candidate vanishes within tolerance.

These three checks together verify the algebraic content of the proof.

## Relation to existing notes

- This note formalizes the parity-protection IF-condition of
  [EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
  Step 2.
- It uses the retained
  [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md) for symmetry-machine-precision
  verification of the underlying sublattice parity action.
- It is consistent with the discussion in
  [LORENTZ_VIOLATION_DERIVED_NOTE](LORENTZ_VIOLATION_DERIVED_NOTE.md)
  Step 5 ("No dimension-5 operator appears because the lattice has exact P
  symmetry, which forbids odd powers of momentum"), which states the same
  conclusion in dispersion language. The present note converts that
  remark into an explicit registered no-go on the SME-style operator basis.

## Honest status

This is a **narrow operator-basis no-go**. It does not promote
emergent_lorentz_invariance_note to retained on its own — the hierarchy-scale
identification still has to be ratified at the cell-coefficient/Planck level.
But it does close the parity bridge: a hostile auditor can now follow the
"P-protected against dim-5 LV" claim to a registered no-go theorem with a
runner, instead of a plain-text assertion.
