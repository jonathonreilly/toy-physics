# Proton Lifetime Derived from Cl(3) on Z^3
**Primary runner:** [`scripts/frontier_proton_lifetime_derived.py`](../scripts/frontier_proton_lifetime_derived.py) (PASS=25/0)

## Status

**Bounded prediction** -- sharp falsifiable.

The numerical result tau_p ~ 10^{47.6} years is a bounded prediction: the
lattice-derived ingredients (leptoquark operators, mediating scale M_X = M_Planck)
are exact framework consequences, but the decay rate formula and coupling constant
are imported from standard EFT / gauge unification.

**Current publication disposition:** bounded companion only. Not on the
retained flagship claim surface.

## Theorem / Claim

**Claim:** The Cl(3)-on-Z^3 framework predicts the proton lifetime

    tau_p ~ 4 x 10^47 years   (log10 ~ 47.6)

This is 10^{13.5} longer than minimal SU(5) GUT predictions, and 10^{13} above
the current Super-K bound. It is a sharp falsifiable prediction: observation of
proton decay at tau < 10^40 years would rule out the framework.

## Assumptions

1. **Framework package pin:** The physical theory is `Cl(3)` on `Z^3`, and on
   the accepted physical-lattice reading the absolute spacing is carried as the
   current package pin `a^(-1) = M_Pl`.

2. **Taste space decomposition:** (C^2)^3 = C^8 decomposes under Hamming-weight
   grading as 8 = 1 + 3 + 3* + 1, where the triplets are the quark sector and
   the singlets are the lepton sector. **[EXACT from the algebra]**

3. **Gauge sector:** SU(3) x SU(2) x U(1) generators preserve the Hamming-weight
   subspaces. **[EXACT]**

4. **Leptoquark operators exist:** The full 64-dim operator algebra on the taste
   space contains operators with nonzero matrix elements between triplet and
   singlet subspaces. These are leptoquark operators. **[EXACT]**

5. **Mediating scale:** Since the leptoquark operators arise from the full lattice
   algebra (not the gauge sector), their effective mass is taken at the lattice
   cutoff `M_X = M_Pl ~ 1.22 x 10^19 GeV` on the current Planck-scale package
   pin. **[PACKAGE PIN, not yet a derived theorem]**

6. **Decay rate formula:** The standard dimension-6 EFT formula applies:
   Gamma = alpha^2 * m_p^5 / M_X^4. **[IMPORTED from EFT]**

7. **Coupling constant:** alpha_GUT ~ 1/25 at the unification scale.
   **[IMPORTED from gauge coupling unification]**

## What Is Actually Proved

### Exact results (from the lattice algebra):

- The taste space (C^2)^3 decomposes as 1 + 3 + 3* + 1 under Hamming weight.
  The triplets carry quark quantum numbers, the singlets carry lepton quantum numbers.

- The SU(3) x SU(2) x U(1) gauge algebra acts within the Hamming-weight subspaces.
  It does not mix quarks and leptons.

- There exist operators in the full Cl(3) algebra that DO mix quarks and leptons.
  The script finds 36 such leptoquark operators out of 64 total operators in the
  tensor-product Pauli basis.

- Baryon number B (= 1/3 on triplets, 0 on singlets) commutes with all SU(3)
  generators. B does NOT commute with SU(2) generators -- this is the sphaleron
  structure (B+L anomalous, B-L anomaly-free on the retained content).

- B-L is anomaly-free on the retained 16-state one-generation content:
  the six-trace packet
  `grav^2(B-L)`, `(B-L)^3`, `SU(3)^2(B-L)`, `SU(2)^2(B-L)`,
  `Y^2(B-L)`, and `Y(B-L)^2` cancels exactly; the retained `nu_R`
  slot is load-bearing for the linear and cubic B-L traces. See
  [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md).

### Framework-dependent results:

- `M_X = M_Pl`. This follows from the current Planck-scale package pin for the
  physical lattice. It is not yet derived from dynamics.

### Imported physics:

- The dimension-6 proton decay rate formula Gamma = alpha^2 * m_p^5 / M_X^4
  is standard EFT technology, not derived from the lattice.

- alpha_GUT = 1/25 is the standard unified coupling at the GUT/Planck scale.

- QCD matrix elements (hadronic wave function overlaps, etc.) are not computed.

## What Remains Open

1. **The decay rate formula itself is not derived from the lattice.** We use the
   standard dimension-6 EFT result. A first-principles lattice derivation of the
   proton decay rate would require computing the effective four-fermion operator
   coefficient from the Cl(3) algebra, which is not done here.

2. **The coupling alpha_GUT = 1/25 is imported.** The framework does not yet
   derive the numerical value of the unified coupling from the lattice.

3. **Hadronic matrix elements** (proton wave function overlaps with the decay
   operator) are not computed from the lattice.

4. **The Z_3 generation selection rule** (only charge-0 quarks can decay to
   charge-0 leptons, giving an additional ~1/3 suppression) is noted in the
   existing frontier_proton_decay.py but is not included in the headline number.
   Including it would push the lifetime even higher.

## How This Changes The Paper

This result is a **supporting prediction**, not one of the four live open gates.
It can be cited in the paper as:

> The framework predicts proton decay at tau ~ 10^{47} years, far beyond the
> reach of current and planned experiments (Super-K bound: 10^{34}, Hyper-K
> projected: 10^{35}). This is a sharp falsifiable prediction: observation of
> proton decay at any experimentally accessible timescale would rule out the
> framework.

This strengthens the paper by providing a concrete, quantitative, falsifiable
prediction that distinguishes the framework from standard GUTs.

**It does NOT close any of the four live gates** (S^3, DM, y_t, CKM).

## Commands Run

```
python3 scripts/frontier_proton_lifetime_derived.py
```

Expected output: PASS=N FAIL=0 with log10(tau_p) ~ 47.6.

## Derivation Chain Summary

```
Cl(3) on Z^3
    |
    v
(C^2)^3 = C^8 taste space
    |
    v
Hamming-weight grading: 8 = 1 + 3 + 3* + 1
    |                          |         |
    |                     quarks (T1,T2) leptons (S0,S3)
    v
SU(3)xSU(2)xU(1) preserves subspaces  (gauge sector)
    |
    v
Full Cl(3) algebra contains 36 leptoquark operators
    |       (operators mixing quark <-> lepton subspaces)
    v
These operators are OUTSIDE gauge sector => effective mass = lattice cutoff
    |
    v
M_X = M_Planck ~ 1.22 x 10^19 GeV
    |
    v
Gamma = alpha^2 * m_p^5 / M_X^4        [imported EFT formula]
    |
    v
tau_p = hbar / Gamma ~ 4 x 10^47 years
    |
    v
FALSIFIABLE: tau_p >> 10^35 (Hyper-K)
             If proton decay seen at tau < 10^40 => framework ruled out
```
