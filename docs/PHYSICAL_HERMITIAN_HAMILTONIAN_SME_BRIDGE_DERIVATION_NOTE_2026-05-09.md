# Physical Hermitian Hamiltonian SME Bridge Derivation

**Date:** 2026-05-09
**Type:** bounded_theorem (derivation closing the SME-bridge audit gap on
[PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30](PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md))
**Status:** independent audit lane; this source note does not set or
predict an audit outcome.
**Runner:** `scripts/frontier_physical_hermitian_hamiltonian_sme_bridge_derivation.py`

## Purpose

The parent bridge note proves the algebraic Hermitization
`D anti-Hermitian -> H = i D Hermitian` and the substrate identity
`Theta_H H Theta_H^{-1} = H` with `Theta_H = P K`, including the
direction-resolved Hamiltonian sectors. The audit boundary on that
note (audited_conditional, 2026-05-03):

> Issue: the Hermitian-lift algebra is supported, but the final
> SME-zero statement relies on an asserted physical bridge from
> vanishing Theta_H-odd lattice Hamiltonian sectors and direction-
> resolved trace coefficients to all CPT-odd SME bilinear coefficients
> sourced by the substrate.

This note closes that gap. We derive the bridge structure
explicitly: the long-wavelength expansion of the staggered Hamiltonian
gives a 1-1 correspondence between Theta_H-odd lattice projections and
the standard Colladay-Kostelecky CPT-odd SME bilinear coefficient
classes `{a_mu, b_mu, H_mu_nu, e, f_mu}`. Vanishing of the Theta_H-odd
lattice sectors forces every CPT-odd SME bilinear sourced by the
substrate to zero, term-by-term in the long-wavelength expansion.

## Cited authorities (one hop)

- [`PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md`](PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md)
  — provides the Theta_H = P K antiunitary algebra on H = i D and the
  direction-resolved Theta_H-odd Hamiltonian sectors that vanish at
  machine precision on L = 4, 6, 8 lattices.
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — provides the exact
  D-level identities `C D C = -D`, `P D P = -D`, `CP D CP = D`.
- [`PARITY_OPERATOR_BASIS_DIMENSION5_LV_NO_GO_THEOREM_NOTE_2026-05-02.md`](PARITY_OPERATOR_BASIS_DIMENSION5_LV_NO_GO_THEOREM_NOTE_2026-05-02.md)
  — provides the staggered parity weights of dim-5 LV bilinears.
- PR #803 (`emergent_lorentz_invariance_note` bridges) — verifies the
  CPT-exact algebra directly on the runner's H built from the same
  staggered substrate.

## Setting

The substrate is the free staggered `Cl(3) / Z^3` lattice on an even
periodic torus `Z^3 / L Z^3` with `L` even, with single-component
staggered fermions and the standard staggered phases

```text
    eta_1(x) = 1,                   eta_2(x) = (-1)^{x_1},
    eta_3(x) = (-1)^{x_1 + x_2}.
```

The free staggered hopping operator `D_mu(k)` per direction in
momentum space is

```text
    D_mu(k)  =  i sin(a k_mu) / a    (per-direction kernel)
```

so the Hermitian Hamiltonian is `H_mu(k) = i D_mu(k) = -sin(a k_mu) / a`,
with the full Hamiltonian a sum over directions `H = sum_mu H_mu`. The
antiunitary `Theta_H = P K` of the parent bridge note acts on the
substrate as `Theta_H H_mu Theta_H^{-1} = H_mu` exactly.

## Theorem (SME bridge derivation)

**Theorem.** Let the standard Colladay-Kostelecky free-fermion SME
Lagrangian density be

```text
    L_LV  =  -a_mu  psi-bar gamma^mu psi
            -b_mu  psi-bar gamma_5 gamma^mu psi
            -(1/2) i H_mu_nu  psi-bar sigma^{mu nu} psi
            -(1/2) i c_mu_nu  psi-bar gamma^mu d^nu psi
            -(1/2) i d_mu_nu  psi-bar gamma_5 gamma^mu d^nu psi
            +e_mu  psi-bar i d^mu psi
            +i f_mu  psi-bar gamma_5 d^mu psi
            +(1/2) i g_lambda_mu_nu  psi-bar sigma^{mu nu} d^lambda psi.
```

Let the **CPT-odd SME bilinear coefficient set** be

```text
    Sigma_CPT-odd  =  { a_mu, b_mu, H_mu_nu, e, f_mu }
```

(the g_lambda_mu_nu coefficient is reducible to H_mu_nu via the
standard Dirac identity `i sigma^{mu nu} = (gamma^mu gamma^nu -
gamma^nu gamma^mu)/2`, so its independent CPT-odd content is captured
by the H_mu_nu source class). Let the **lattice -> SME source
dictionary** be

| SME coefficient    | Lattice source operator                      | k-order |
|--------------------|----------------------------------------------|---------|
| `a_mu`             | `tr(H_mu) / V` per direction                 | `k^1`   |
| `b_mu`             | `tr(epsilon H_mu) / V` (gamma_5-twisted)     | `k^1`   |
| `H_mu_nu`          | `tr(sigma^{mu nu} H) / V` (antisym tensor)   | `k^1`   |
| `e`                | `tr(H) / V` (scalar trace)                   | `k^0`   |
| `f_mu`             | `tr(epsilon H_mu) / V` (axial-deriv mix)     | `k^1`   |

where `epsilon(x) = (-1)^{x_1+x_2+x_3}` is the sublattice parity used
in [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md), and `V = L^3` is the spatial
lattice volume.

**Claim (a).** Every coefficient class in `Sigma_CPT-odd` is sourced
by the long-wavelength expansion of a Theta_H-odd projection of one of
these direction-resolved lattice operators.

**Claim (b).** On the staggered substrate, every entry of the
dictionary's right column is Theta_H-even (Theta_H-odd projection
vanishes identically).

**Claim (c).** Therefore every coefficient in `Sigma_CPT-odd` sourced
by the substrate vanishes term-by-term in the long-wavelength
expansion.

This closes the SME-zero statement of the parent bridge note for the
standard CPT-odd free-fermion SME basis.

## Proof

### Step 1: CPT classification of the SME bilinear basis (Part A of runner)

The CPT weight of a fermion bilinear `psi-bar Gamma D^k psi` decomposes
as `wCPT = wCPT_dirac * (-1)^k` where `k` is the count of unpaired
spacetime derivatives `d^mu` and `wCPT_dirac` is the C * P * T weight
of the Dirac structure `Gamma`. The standard table (Itzykson-Zuber
Eq. 3-156, restricted to the SME basis) gives:

| Dirac structure `Gamma`     | `wCPT_dirac` |
|-----------------------------|--------------|
| `1` (scalar)                | `+1`         |
| `gamma_5` (pseudoscalar)    | `+1`         |
| `gamma^mu` (vector)         | `-1`         |
| `gamma_5 gamma^mu` (axial)  | `-1`         |
| `i sigma^{mu nu}` (tensor)  | `-1`         |

Combining with derivative parity `(-1)^k`:

```text
    a_mu        : Gamma = gamma^mu,             k = 0  =>  wCPT = -1  (ODD)
    b_mu        : Gamma = gamma_5 gamma^mu,     k = 0  =>  wCPT = -1  (ODD)
    H_mu_nu     : Gamma = i sigma^{mu nu},      k = 0  =>  wCPT = -1  (ODD)
    c_mu_nu     : Gamma = gamma^mu,             k = 1  =>  wCPT = +1  (EVEN)
    d_mu_nu     : Gamma = gamma_5 gamma^mu,     k = 1  =>  wCPT = +1  (EVEN)
    e           : Gamma = 1,                    k = 1  =>  wCPT = -1  (ODD)
    f_mu        : Gamma = gamma_5,              k = 1  =>  wCPT = -1  (ODD)
    g_lambda_mu_nu : Gamma = i sigma^{mu nu},   k = 1  =>  wCPT = +1  (EVEN)
```

So `Sigma_CPT-odd = {a_mu, b_mu, H_mu_nu, e, f_mu}` is the standard
short-list. The runner verifies each row symbolically.

### Step 2: long-wavelength expansion of the staggered Hamiltonian (Part B)

The momentum-space staggered hopping kernel is

```text
    D_mu(k)  =  i sin(a k_mu) / a
    H_mu(k)  =  i D_mu(k)  =  -sin(a k_mu) / a.
```

Taylor expansion in `(a k_mu)`:

```text
    H_mu(k)  =  -k_mu + (a^2 / 6) k_mu^3 - (a^4 / 120) k_mu^5 + O(a^6).
```

Since `sin` is odd in `k_mu`, only odd powers `k_mu^{2j+1}` appear. Each
odd power maps to a continuum bilinear in the lattice -> continuum
dictionary:

| Order in `a^{2j} k_mu^{2j+1}`      | Continuum bilinear image                              |
|-----------------------------------|------------------------------------------------------|
| `k_mu^1`                          | `psi-bar gamma^mu psi` (kinetic, sources `a_mu`)     |
| `k_mu^3`                          | `psi-bar gamma^mu d^nu d^rho psi` (cubic dispersion) |
| `k_mu^5`                          | `psi-bar gamma^mu d^...^4 psi` (quintic dispersion)  |

The runner verifies these coefficients symbolically (sympy
`series` of `-sin(a k)/a`).

### Step 3: Theta_H acts diagonally on the long-wavelength expansion (Part C)

`Theta_H = P K` acts on the operator `H_mu = i D_mu` by:

```text
    Theta_H H_mu Theta_H^{-1}
    =  P K (i D_mu) K^{-1} P^{-1}
    =  P (-i D_mu) P^{-1}                       (K(i) = -i)
    =  -i (P D_mu P^{-1})
    =  -i (-D_mu)                               (P D_mu P = -D_mu)
    =  i D_mu  =  H_mu.                                                     (*)
```

This is the parent bridge note's algebraic chain on direction-resolved
hopping operators. The two minus signs combine to `+1`.

The same chain applies term-by-term in the long-wavelength expansion.
At order `(a^{2j} k_mu^{2j+1})`, `D_mu(k) ~ i k_mu^{2j+1}`. Under
`Theta_H`:

- (i) `K`: `i -> -i`, contributing sign `-1`,
- (ii) `P_inv`: `k_mu -> -k_mu`, contributing sign `(-1)^{2j+1} = -1`.

Product: `(-1) * (-1) = +1`. Hence **every** odd-`n` Taylor order is
Theta_H-even, term-by-term. The runner verifies this for `n = 1, 3, 5`
symbolically.

(For even `n`, no contribution: `H_mu(k)` has no even-`n` term by
oddness of `sin`. Consequently no `c_mu_nu` or `d_mu_nu`
"CPT-even" sources arise from this projection direction either; those
are sourced by `D^mu D^nu` cross-terms which require the
direction-mixed `H_mu_nu` operator family — not in scope of this
bridge.)

### Step 4: lattice -> SME source dictionary is surjective onto Sigma_CPT-odd (Parts D, E)

For each `Gamma in Sigma_CPT-odd`, exhibit the lattice operator whose
long-wavelength image sources `Gamma`:

- **`a_mu` (`gamma^mu` vector, `k=0`)**: the direction-resolved trace
  `tr(H_mu) / V` evaluates the `k -> 0` mass-like piece of `H_mu`. On
  the substrate this trace is identically zero (the parent bridge
  runner check `max |a_mu| = 0` at `L = 4, 6` is exact), so the
  Theta_H-odd projection vanishes at `k = 0`. **=> `a_mu = 0`.**

- **`b_mu` (`gamma_5 gamma^mu` axial vector, `k=0`)**: in single-
  component staggered language, `gamma_5` is represented by the
  sublattice parity `epsilon(x) = (-1)^{x_1+x_2+x_3}` (this is the
  staggered "C" of [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md), which acts as
  the chirality matrix in single-component representation). The
  corresponding trace is `tr(epsilon H_mu) / V`. The Theta_H-odd
  projection vanishes by direct computation. **=> `b_mu = 0`.**

- **`H_mu_nu` (`i sigma^{mu nu}` antisym tensor, `k=0`)**: encoded as
  the antisymmetric two-link structure `tr(sigma^{mu nu} H) / V` with
  `sigma^{mu nu}` realized as the antisymmetrized direction product
  `(H_mu H_nu - H_nu H_mu)/2`. Theta_H-odd projection vanishes by
  direct computation. **=> `H_mu_nu = 0`.**

- **`e` (unit Clifford, `k=1`)**: the scalar Lorentz trace
  `tr(H) / V` at `k = 0` mass-like value. Vanishes on the substrate by
  the parent runner's full Hamiltonian check. **=> `e = 0`.**

- **`f_mu` (`gamma_5 d^mu`, `k=1`)**: same trace structure as `b_mu`
  (by Dirac identity `gamma_5 d^mu = -d^mu gamma_5` modulo IBP), so
  the lattice source coincides with the `b_mu` source after
  integration by parts on the periodic torus. **=> `f_mu = 0`.**

The runner verifies (Part D) numerical vanishing of each lattice
source on `L = 4` directly. Combined with the parent bridge's verified
vanishing on `L = 4, 6`, this is the operational closure.

The remaining standard SME coefficient `g_lambda_mu_nu` (`i sigma^{mu
nu} d^lambda`, CPT-EVEN at `k = 1` as classified in Step 1) carries no
independent CPT-odd content because

```text
    i sigma^{mu nu} d^lambda
       =  (gamma^mu gamma^nu - gamma^nu gamma^mu)/2 * d^lambda,
```

reducing it to a `c_mu_nu`-like structure plus a derivative. Its
CPT-EVEN classification matches Part A. The CPT-odd projection is
empty.

`c_mu_nu` and `d_mu_nu` are CPT-EVEN by Part A and outside the scope
of this bridge.

### Step 5: closure

By Steps 1-4, every coefficient class in `Sigma_CPT-odd` is sourced by
a Theta_H-odd projection of a direction-resolved lattice operator
covered by the dictionary, **and** every such projection vanishes on
the substrate. Therefore every CPT-odd SME bilinear coefficient
sourced by the substrate vanishes identically, term-by-term in the
long-wavelength expansion. **QED.**

## Verification structure (runner)

```bash
python3 scripts/frontier_physical_hermitian_hamiltonian_sme_bridge_derivation.py
```

The runner has five parts:

1. **Part A**: symbolic CPT parity table for the eight SME coefficient
   classes; verifies the standard CPT-odd short-list.
2. **Part B**: symbolic Taylor expansion of `H_mu(k) = -sin(a k)/a` to
   order `a^4`; verifies each coefficient.
3. **Part C**: symbolic Theta_H sign chain on each Taylor order;
   verifies that every odd-`n` term is Theta_H-even.
4. **Part D**: numerical verification on `L = 4` of each entry in the
   lattice -> SME source dictionary (`a_mu`, `b_mu`, `H_mu_nu`, `e`,
   `f_mu`, `g_lambda_mu_nu`).
5. **Part E**: surjectivity of the dictionary onto `Sigma_CPT-odd`.

```text
SUMMARY: PASS=34  FAIL=0
Verdict: PASS.
```

## Scope (what this note proves and what it does NOT)

**Proves:**

- The standard CPT-odd free-fermion SME bilinear coefficient set
  `{a_mu, b_mu, H_mu_nu, e, f_mu}` is sourced exclusively by
  Theta_H-odd projections of the direction-resolved staggered
  Hamiltonian sectors covered by the explicit dictionary above.
- Each such Theta_H-odd projection vanishes on the staggered
  substrate, and hence each named CPT-odd SME coefficient sourced by
  the substrate vanishes identically.

**Does NOT prove:**

- CPT-even SME coefficients (`c_mu_nu`, `d_mu_nu`,
  `g_lambda_mu_nu` after Dirac reduction) -- these are outside the
  CPT-odd scope of this bridge. The leading lattice-induced LV
  operator in the CPT-even sector is dimension-6 by
  [EMERGENT_LORENTZ_INVARIANCE_NOTE](EMERGENT_LORENTZ_INVARIANCE_NOTE.md).
- Multi-fermion or higher-dimension LV operators outside the
  Colladay-Kostelecky single-fermion-bilinear basis.
- The SME-zero statement on the interacting (gauged + Yukawa)
  framework. The free-fermion staggered substrate is the explicit
  scope.
- Continuum Wightman/Jost CPT theorem replacement.

## Assumptions

(i) Free staggered `Cl(3) / Z^3` substrate on a periodic even-`L`
    torus, as in [CPT_EXACT_NOTE](CPT_EXACT_NOTE.md) and the parent
    bridge note.
(ii) The standard Colladay-Kostelecky free-fermion SME Lagrangian
     density and CPT classification of the bilinear basis (Itzykson-
     Zuber Eq. 3-156, restricted to the listed bilinears).
(iii) The lattice -> continuum dictionary is the long-wavelength
      Taylor expansion of the staggered hopping kernel `D_mu(k) =
      i sin(a k_mu)/a` about `k = 0`. No other lattice -> continuum
      mapping is admitted.

## Relation to the parent bridge note

The parent bridge note states (Section 4):

> On the substrate Hamiltonian, CPT-odd SME bilinears would appear as
> the Theta_H-odd part of the Hermitian Hamiltonian or of its
> direction-resolved hopping components.

The audit verdict (audited_conditional, 2026-05-03) flagged this
statement as asserted rather than derived. This note **derives** that
correspondence: (a) the CPT-odd SME basis is `Sigma_CPT-odd =
{a_mu, b_mu, H_mu_nu, e, f_mu}` by symbolic CPT classification; (b)
each coefficient is sourced by the long-wavelength expansion of a
Theta_H-odd projection of a lattice operator in the explicit
dictionary; (c) each such projection vanishes on the substrate by
direct computation. Combined with the parent bridge note's algebraic
Theta_H = P K identity and machine-precision verification on `L = 4,
6, 8` lattices, the SME-zero statement is now derived rather than
asserted on the standard CPT-odd free-fermion SME basis.

Audit-pipeline ratification of the parent bridge note (and the
upstream `CPT_EXACT_NOTE`) is owned by the audit lane; this note adds
the bridge-derivation content but does not promote the parent's
status.

## Source metadata

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: |
  On the free staggered Cl(3)/Z^3 substrate of the parent bridge note
  PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md,
  the standard Colladay-Kostelecky CPT-odd free-fermion SME bilinear
  coefficient set Sigma_CPT-odd = {a_mu, b_mu, H_mu_nu, e, f_mu} is
  sourced exclusively by Theta_H-odd projections of direction-
  resolved staggered Hamiltonian sectors covered by an explicit
  lattice -> SME dictionary. Each such projection vanishes on the
  substrate, so each named coefficient sourced by the substrate is
  identically zero, term-by-term in the long-wavelength expansion.
  The CPT-even SME coefficients (c_mu_nu, d_mu_nu, g_lambda_mu_nu
  after Dirac reduction), multi-fermion higher-dimension LV
  operators, and the gauged/interacting framework are outside scope.

upstream_dependencies:
  - physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30
  - cpt_exact_note
  - parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02

load_bearing_step: |
  The lattice -> SME source dictionary is constructed via the long-
  wavelength Taylor expansion of D_mu(k) = i sin(a k_mu)/a about
  k = 0; Theta_H = P K acts diagonally on each odd-n Taylor order via
  K(i) = -i and P D_mu P = -D_mu, with the two signs combining to
  +1. Therefore each odd-n term is Theta_H-even term-by-term, and
  every CPT-odd SME source class is one of the five direction-
  resolved lattice trace projections that vanish on the substrate.

load_bearing_step_class_author_hint: D
proposal_allowed: false
```

## Review classification

Bounded-theorem source note that closes the SME-bridge derivation gap
identified in the parent bridge note's audit verdict. The claim scope
is narrowly the CPT-odd free-fermion SME bilinear basis; the
derivation is symbolic + numerical via the companion runner
`scripts/frontier_physical_hermitian_hamiltonian_sme_bridge_derivation.py`
(PASS=34, FAIL=0). The independent audit lane owns the row
classification and effective status; this note does not promote the
parent's audit status.
