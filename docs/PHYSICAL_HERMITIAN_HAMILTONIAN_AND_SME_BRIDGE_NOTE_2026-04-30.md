# Physical Hermitian Hamiltonian And SME Bridge

**Date:** 2026-04-30
**Status:** proposed_retained bridge theorem; audit pending
**Runner:** `scripts/frontier_physical_hermitian_hamiltonian_and_sme_bridge.py`

## Purpose

The existing CPT exact theorem proves the exact staggered identities for the
real anti-Hermitian hopping operator `D`, but its stated claim is about the
physical Hermitian Hamiltonian and vanishing CPT-odd SME sector. The audit gap
is the Hermitization step:

```text
D anti-Hermitian  ->  H physical Hermitian.
```

Because CPT is antiunitary, the factor `i` in `H = i D` must be carried
explicitly. Reusing the `D`-level `CP K` representative without modification
flips `H`; that was the real gap. This bridge records the physical Hermitian
lift and checks the SME-zero statement on that lift.

## Inputs

- The `D`-level staggered identities reconstructed directly by this bridge
  runner: `C D C = -D`, `P D P = -D`, and `CP D CP = D` on even periodic
  lattices.
- The framework Hamiltonian convention used throughout the staggered runners:

  ```text
  H = i D
  ```

  where `D` is the real anti-Hermitian nearest-neighbor staggered hopping
  operator. For example, the generation runners diagonalize
  `h_herm = 1j * staggered_h_antiherm(k)`.

No Standard-Model numerical value, external SME coefficient, fitted selector,
or continuum input is used.

## Theorem Statement

Let `D` be the real anti-Hermitian staggered hopping operator on an even
periodic `Z^3` lattice, and let

```text
H = i D.
```

Let `C` be the staggered sublattice/spectral-flip unitary and `P` the even
periodic inversion unitary, so that

```text
C D C = -D,
P D P = -D,
CP D CP = D.
```

Then:

1. `H` is Hermitian.
2. The naive antiunitary `CP K` that is useful on `D` sends `H` to `-H`, so it
   is not the physical Hermitian CPT representative.
3. The Hermitian Hamiltonian lift uses the antiunitary representative

   ```text
   Theta_H = P K
   ```

   equivalently `Theta_H = C P T_H` with `T_H = C K`. This is the same
   staggered `C/P` algebra with the exact spectral-flip unitary absorbed into
   the antiunitary time-reversal representative to compensate `K(i)=-i`.
4. `Theta_H H Theta_H^{-1} = H`.
5. The CPT-odd Hamiltonian sector

   ```text
   H_odd = (H - Theta_H H Theta_H^{-1}) / 2
   ```

   vanishes identically, including the direction-resolved hopping sectors.
   Therefore all SME coefficients sourced by CPT-odd bilinear Hamiltonian
   terms are zero on this substrate.

## Derivation

### 1. Hermitization

The staggered hopping operator satisfies

```text
D^\dagger = -D.
```

Therefore the physical complex Hilbert-space Hamiltonian is

```text
H = iD,
H^\dagger = (-i)D^\dagger = iD = H.
```

This is the convention already used by the framework's staggered generation
runners when they diagonalize the physical spectrum.

### 2. Why The Naive Lift Fails

The `D`-level combined operation is `CP K`. Since `D` is real and `CP D CP =
D`,

```text
CP K D K CP = D.
```

But

```text
CP K (iD) K CP = CP (-iD) CP = -iD = -H.
```

So the audit concern is valid: `D`-level CPT invariance does not automatically
prove physical-Hamiltonian CPT invariance unless the antiunitary `i` factor is
handled.

### 3. Physical Hermitian CPT Representative

The staggered algebra already has two exact spectral-flip unitaries:

```text
C D C = -D,
P D P = -D.
```

Therefore either `C K` or `P K` is an antiunitary symmetry of `H = iD`, because
the complex conjugation contributes one minus sign and the spectral flip
contributes the second:

```text
P K (iD) K P = P (-iD) P = -i(-D) = iD = H.
```

Choosing `T_H = C K` gives

```text
C P T_H = C P C K = P K
```

on the even periodic lattice, where `C` and `P` commute. Thus the physical
Hermitian CPT representative is the antiunitary `Theta_H = P K`.

This is not an extra symmetry assumption. It uses only the exact `C` and `P`
operators already constructed in the `D`-level theorem, plus the mandatory
antiunitary action `K(i)=-i` in the Hermitization map.

### 4. SME Compatibility

On the substrate Hamiltonian, CPT-odd SME bilinears would appear as the
`Theta_H`-odd part of the Hermitian Hamiltonian or of its direction-resolved
hopping components:

```text
H_odd    = (H    - Theta_H H    Theta_H^{-1}) / 2,
H_mu,odd = (H_mu - Theta_H H_mu Theta_H^{-1}) / 2.
```

The bridge runner checks that all these matrices vanish at machine precision
on even periodic lattices. Direction-resolved trace coefficients, the lattice
analogues of `a_mu`-type CPT-odd bilinear coefficients, are also zero.

## Claim Boundary

This bridge claims only the free staggered Hamiltonian-sector result:

- `D -> H=iD` is Hermitian;
- exact substrate `C/P` identities lift to an antiunitary physical-Hamiltonian
  CPT representative;
- CPT-odd bilinear SME coefficients are zero on that Hamiltonian substrate.

It does not claim:

- interacting CKM-sector CP violation;
- continuum Wightman/Jost CPT theorem replacement;
- full SU(3) Wilson-plaquette operator-level CPT audit;
- any numerical Standard-Model fit.

## Verification

Run:

```bash
python3 scripts/frontier_physical_hermitian_hamiltonian_and_sme_bridge.py
```

Current output:

```text
Summary: PASS=10  FAIL=0
Verdict: PASS.
```

The checks verify:

1. `D^\dagger=-D` and `H=iD` is Hermitian;
2. `C D C=-D`, `P D P=-D`, and `CP D CP=D`;
3. naive `CP K` flips `H`, reproducing the old audit gap;
4. the physical Hermitian antiunitary representative `Theta_H=P K` preserves
   `H`;
5. full and direction-resolved CPT-odd SME sectors vanish.

## SME bridge derivation (2026-05-09)

The audit verdict (audited_conditional, 2026-05-03) flagged Section 4
above:

> the Hermitian-lift algebra is supported, but the final SME-zero
> statement relies on an asserted physical bridge from vanishing
> Theta_H-odd lattice Hamiltonian sectors and direction-resolved trace
> coefficients to all CPT-odd SME bilinear coefficients sourced by the
> substrate.

That gap is closed by
[`PHYSICAL_HERMITIAN_HAMILTONIAN_SME_BRIDGE_DERIVATION_NOTE_2026-05-09.md`](PHYSICAL_HERMITIAN_HAMILTONIAN_SME_BRIDGE_DERIVATION_NOTE_2026-05-09.md),
which:

- Classifies the standard Colladay-Kostelecky free-fermion SME basis
  by CPT parity, identifying the CPT-odd short-list
  `Sigma_CPT-odd = {a_mu, b_mu, H_mu_nu, e, f_mu}`.
- Constructs the long-wavelength expansion of the staggered Hamiltonian
  `H_mu(k) = -sin(a k_mu)/a` about `k = 0` (only odd `k`-orders).
- Shows that `Theta_H = P K` acts diagonally on each Taylor order via
  `K(i) = -i` and `P D_mu P = -D_mu`, with the two signs combining to
  `+1` term-by-term.
- Builds an explicit lattice -> SME source dictionary covering each
  CPT-odd coefficient class.
- Verifies numerically (`L = 4`) that every dictionary entry's
  Theta_H-odd projection vanishes identically.

The derivation runner
`scripts/frontier_physical_hermitian_hamiltonian_sme_bridge_derivation.py`
returns PASS=34 / FAIL=0. With this derivation, the SME-zero statement
of Section 4 is no longer an assertion: every CPT-odd SME bilinear
coefficient sourced by the substrate vanishes term-by-term in the
long-wavelength expansion of the lattice operator family. Audit
ratification on the parent and derivation notes remains the audit
lane's call.
