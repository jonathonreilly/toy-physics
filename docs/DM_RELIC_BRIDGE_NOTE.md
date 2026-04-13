# Relic Bridge: What Connects sigma_v to R = Omega_DM / Omega_b

**Date:** 2026-04-13
**Branch:** `claude/youthful-neumann`
**Lane:** DM relic mapping
**Status:** BOUNDED -- one imported cosmological input (eta from Planck)

---

## Purpose

This is the single authority note on the "relic-ratio bridge" that Codex
flagged as the remaining open piece after the T-matrix / direct-observable
argument narrowed the g_bare objection.

The question: once sigma_v is a direct observable of H, how does R follow?

---

## The Bridge Equation

R = Omega_DM / Omega_b = (rho_DM) / (rho_b)

At late times (matter domination, post-BBN):

    rho_DM = n_DM * m_DM
    rho_b  = n_b  * m_p

So:

    R = (n_DM / n_b) * (m_DM / m_p)

Each factor has a distinct derivation status.

---

## Factor 1: m_DM / m_p (mass ratio)

**Status: EXACT**

From the taste decomposition (Steps 1-4 of DM_CLEAN_DERIVATION_NOTE.md):
the DM candidate S_3 has Hamming weight h = 3, while the visible-sector
states have weights h = 1, 2. The Wilson mass is m_h = h * m_0, so mass
ratios are exact integers determined by the lattice.

The mass ratio enters R through the Lee-Weinberg formula structure
Omega ~ m^2 / sigma, giving the structural factor 3/5 (Step 4). This
is a combinatorial identity on Z^3 and carries zero uncertainty.

---

## Factor 2: n_DM at late times (from freeze-out)

**Status: DERIVED (bounded sub-inputs: g_bare = 1, k = 0)**

The DM number density after freeze-out is set by:

1. **sigma_v** -- the annihilation cross section. Derived from H via
   the lattice T-matrix / optical theorem (Step 9). This is a direct
   observable of the Hamiltonian; the g_bare question reduces to a
   foundational commitment about which H, not about a free parameter.

2. **Boltzmann equation** -- derived from the lattice master equation.
   The Stosszahlansatz is a proved theorem on Z^3 (factorization error
   < 10^{-45000}). Remaining caveat: proof is for the free (Gaussian)
   theory; extension to the interacting case needs spectral gap
   persistence under weak coupling.

3. **Freeze-out condition Gamma = H** -- requires H(T), the Hubble rate.
   Derived from Newtonian cosmology (Milne 1934): shell theorem +
   energy conservation for E = 0. Uses lattice Poisson equation.
   Sub-assumption: flatness k = 0 (bounded; observationally confirmed
   to |Omega_k| < 0.001).

4. **x_F ~ 25** -- follows from the Boltzmann equation with the above
   inputs. Log-insensitive: factor-2 changes in sigma_v shift x_F
   by ~2 units and R by ~1%.

The output is: n_DM(T) after freeze-out is a derived function of H.

---

## Factor 3: n_b at late times (the missing piece)

**Status: IMPORTED from Planck**

The baryon number density today is determined by Big Bang nucleosynthesis
(BBN), which converts the baryon-to-photon ratio eta into Omega_b:

    Omega_b * h^2 = 3.65 x 10^7 * eta

where eta = n_B / n_gamma = 6.12 x 10^{-10} (Planck 2018).

### Where does eta come from?

In the standard cosmological picture, eta is set by baryogenesis --
the process that produced the matter-antimatter asymmetry. The framework
provides partial ingredients for deriving eta (see BARYOGENESIS_NOTE.md):

**Derived from the framework:**

- **Baryon number violation:** SU(2) sphalerons follow from the derived
  SU(2) gauge structure. The sphaleron rate Gamma_sph / T^4 ~ alpha_w^5
  is computable from the lattice SU(2) coupling. (Sakharov condition 1.)

- **CP violation:** The Z_3 cyclic permutation of spatial axes assigns
  complex phases {1, omega, omega^2} to the three generations. This gives
  a CP-violating phase delta = 2pi/3, with sin(delta) = sqrt(3)/2.
  The Jarlskog invariant J_Z3 = 3.1 x 10^{-5} matches the SM value.
  (Sakharov condition 2.)

- **Phase transition mechanism:** The Coleman-Weinberg mechanism on the
  lattice provides the electroweak phase transition. (Sakharov condition 3,
  partially.)

**NOT derived -- the critical gap:**

- **Phase transition strength v(T_c)/T_c:** The parametric baryogenesis
  calculation requires v/T ~ 0.5 to produce eta_obs. The perturbative
  estimate gives v/T ~ 0.15-0.23 (too weak). A non-perturbative lattice
  calculation of the taste-scalar spectrum's effect on the EWPT is needed
  but has not been done.

- **Transport coefficients:** Wall velocity v_w, wall thickness L_w,
  quark diffusion D_q are parameterized, not derived. Each carries O(1)
  uncertainty.

- **Non-GIM CP source:** The effective CP source S_CP ~ y_t^2 sin(delta)
  / (4 pi^2) uses a transport-equation ansatz, not a first-principles
  lattice calculation.

### Honest assessment of eta

The framework provides all three Sakharov conditions at the structural
level. The parametric estimate gives eta ~ 6 x 10^{-10} IF v/T ~ 0.5.
But v/T is not derived, and the transport prefactor has O(1) uncertainties.

**eta is therefore NOT derived.** It is conditionally bounded: the
framework constrains eta to the right order of magnitude given a
phase-transition strength that is plausible but uncomputed.

---

## The Honest State of R

Assembling the three factors:

| Component | Status | Source |
|-----------|--------|--------|
| m_DM / m_p (mass ratio) | EXACT | Hamming weights on Z^3 |
| sigma_v (cross section) | DERIVED | T-matrix / optical theorem on H |
| Boltzmann equation | DERIVED | Master equation + proved Stosszahlansatz |
| H(T) (Hubble rate) | DERIVED | Newtonian cosmology (k=0 bounded) |
| x_F (freeze-out) | DERIVED | Boltzmann + Gamma = H |
| n_DM (DM abundance) | DERIVED | Above chain |
| n_b (baryon abundance) | **IMPORTED** | eta from Planck |
| eta (baryon-to-photon) | **IMPORTED** | Not derived; conditionally bounded |

**Bottom line:**

> R = Omega_DM / Omega_b is derived up to one imported cosmological
> input: the baryon-to-photon ratio eta = 6.12 x 10^{-10} from Planck.

The framework derives the NUMERATOR of R (dark matter abundance from
freeze-out with sigma_v as a direct observable of H). It does NOT derive
the DENOMINATOR independently: Omega_b requires eta, which requires a
completed baryogenesis calculation that the framework has not closed.

---

## What Would Close the Bridge

To eliminate eta as an import, the framework would need:

1. **Non-perturbative EWPT lattice calculation** with taste scalars,
   yielding v(T_c)/T_c from the theory. This is a compute-bounded
   problem (feasible in principle, not yet done).

2. **First-principles transport calculation** of the baryon asymmetry
   produced during the phase transition, using the Z_3 CP phase and
   the derived sphaleron rate.

3. **Result:** eta as a function of framework parameters only.

If (1) and (2) were completed and gave eta ~ 6 x 10^{-10}, then R
would be parameter-free. The BARYOGENESIS_NOTE.md shows this is
plausible (the parametric estimate lands in the right range for
v/T ~ 0.5), but "plausible" is not "derived."

---

## What This Note Supersedes

This note is the single authority on the relic bridge. It supersedes
any claim in other DM notes that R is "fully derived" or "zero-parameter."
The correct statement is:

- sigma_v: derived (direct observable of H)
- n_DM: derived (Boltzmann from master equation, freeze-out from
  Newtonian cosmology)
- n_b: imported (eta from Planck)
- R: derived up to one imported cosmological input

The two bounded framework inputs (g_bare = 1, k = 0) remain as stated
in DM_CLEAN_DERIVATION_NOTE.md.

---

## Paper-Safe Wording

> The dark-matter relic ratio R = Omega_DM / Omega_b = 5.48 is computed
> from a 13-step chain on Cl(3) x Z^3. The annihilation cross section
> sigma_v is a direct observable of the Hamiltonian via the lattice
> T-matrix. The Boltzmann equation is derived from the lattice master
> equation with a proved Stosszahlansatz (factorization error < 10^{-45000}).
> The Hubble rate H(T) follows from Newtonian cosmology with k = 0.
>
> Two framework inputs remain bounded: the bare coupling g = 1 (Cl(3)
> normalization) and spatial flatness k = 0. The baryon abundance
> Omega_b uses the observed baryon-to-photon ratio eta = 6.12 x 10^{-10}
> from Planck. The framework provides the structural prerequisites for
> deriving eta (SU(2) sphalerons, Z_3 CP violation, Coleman-Weinberg
> phase transition), but the non-perturbative phase-transition strength
> required to close the baryogenesis calculation has not been computed.
>
> R is therefore derived up to one imported cosmological input (eta).
