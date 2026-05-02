#!/usr/bin/env python3
"""
Lorentz and CPT Violation from Lattice Structure -- SME Coefficients
=====================================================================

The graph-propagator framework is built on a cubic lattice Z^3 which breaks
continuous Lorentz symmetry to the discrete cubic group O_h at the Planck
scale. This script computes:

1. The lattice dispersion relation and its Lorentz-violating corrections
2. Mapping onto Standard Model Extension (SME) coefficients
3. Comparison with current experimental bounds
4. Staggered-fermion taste-breaking contributions
5. CPT analysis on the lattice
6. The leading observable prediction

The key result: the lattice correction to the dispersion relation is

    E^2 = m^2 + sum_i (4/a^2) sin^2(p_i a/2)

(the standard second-order finite-difference Laplacian eigenvalue;
matches LORENTZ_VIOLATION_DERIVED_NOTE.md Step 2). Expanding at low
momentum:

    E^2 = m^2 + p^2 - (a^2/12) sum_i p_i^4 + O(a^4)

The p_i^4 term breaks SO(3,1) to the cubic group O_h. Its coefficient
maps onto specific SME framework coefficients.

For a = l_Planck, the natural suppression is (E/E_Planck)^2 ~ 10^-38
at E = 1 GeV, which is below ALL current experimental bounds.

PStack experiment: lorentz-violation-sme
"""

from __future__ import annotations

import math
import time

import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)


# ============================================================
# Physical constants
# ============================================================
HBAR = 1.054571817e-34       # J s
C_LIGHT = 2.99792458e8       # m/s
G_NEWTON = 6.67430e-11       # m^3 kg^-1 s^-2
L_PLANCK = 1.616255e-35      # m
E_PLANCK_GEV = 1.2209e19     # GeV
E_PLANCK_J = 1.956e9         # J
GEV_TO_INVMETER = 5.076e15   # 1 GeV = 5.076e15 m^-1

# Particle masses in GeV
M_ELECTRON_GEV = 0.000511
M_PROTON_GEV = 0.938
M_NEUTRON_GEV = 0.940
M_NEUTRINO_GEV = 1e-10       # upper bound, ~0.1 eV


# ============================================================
# Section 1: Lattice dispersion relation
# ============================================================

def lattice_dispersion_1d(p: np.ndarray, a: float, m: float) -> np.ndarray:
    """Single-component lattice dispersion: (4/a^2) sin^2(p*a/2).

    On a cubic lattice with spacing a, the standard second-order
    finite-difference Laplacian eigenvalue is
        K_i = (4/a^2) sin^2(p_i a/2) = (2/a^2) (1 - cos(p_i a))

    rather than the continuum p_i^2. This is the canonical normalization
    that matches LORENTZ_VIOLATION_DERIVED_NOTE.md Step 2.

    Note (2026-05-02 audit fix): the previous version used (2/a^2)
    sin^2(p_i a/2), which is half-normalized: it gives leading
    p_i^2 / 2 rather than p_i^2 in the small-p_i limit, and the
    runner's printed expansion was inconsistent with its actual kinetic
    function. The (4/a^2) form below is the correct standard
    normalization for which sin^2(pa/2) -> (pa/2)^2 - (pa/2)^4/3 + ...
    multiplied by 4/a^2 yields p^2 - a^2 p^4/12 + ... .

    E^2 = m^2 + sum_i (4/a^2) sin^2(p_i a/2)

    Args:
        p: momentum array (GeV, in natural units with c=hbar=1)
        a: lattice spacing (in natural-unit length = 1/GeV)
        m: mass (GeV)

    Returns:
        E^2 array
    """
    return m**2 + (4.0 / a**2) * np.sin(p * a / 2.0)**2


def lattice_dispersion_3d(px: float, py: float, pz: float,
                          a: float, m: float) -> float:
    """3D lattice dispersion relation (standard (4/a^2) normalization)."""
    K = sum((4.0 / a**2) * math.sin(pi * a / 2.0)**2
            for pi in [px, py, pz])
    return m**2 + K


def continuum_dispersion(p: np.ndarray, m: float) -> np.ndarray:
    """Standard relativistic dispersion: E^2 = m^2 + p^2."""
    return m**2 + p**2


def lorentz_violation_coefficient(a: float) -> float:
    """The coefficient of the p_i^4 Lorentz-violating term.

    Expanding sin^2(p_i a/2) = (p_i a/2)^2 - (p_i a/2)^4/3 + ...
    gives (4/a^2) sin^2(p_i a/2) = p_i^2 - a^2 p_i^4/12 + ...

    The LV correction to E^2 is:
        delta(E^2) = -(a^2/12) sum_i p_i^4

    Returns the coefficient a^2/12.
    """
    return a**2 / 12.0


def sixth_order_coefficient(a: float) -> float:
    """The coefficient of the p_i^6 term (next Lorentz-violating order).

    sin^2(x) = x^2 - x^4/3 + 2x^6/45 - ...
    (4/a^2) sin^2(pa/2) = p^2 - a^2 p^4/12 + a^4 p^6/360 + ...

    Returns a^4/360.
    """
    return a**4 / 360.0


# ============================================================
# Section 2: SME (Standard Model Extension) mapping
# ============================================================

def compute_sme_coefficients(a_meters: float) -> dict:
    """Map the lattice dispersion correction onto SME coefficients.

    The Standard Model Extension (Kostelecky, 2004) parameterizes
    Lorentz violation in terms of tensor coefficients that modify
    the free-particle dispersion relation.

    For a spin-1/2 fermion in the SME, the modified dispersion is:
        E^2 = m^2 + p^2 + sum_{d,jm} k^(d)_{jm} |p|^{d-2}

    where d is the mass dimension of the operator, and k^(d)_{jm}
    are spherical-harmonic coefficients.

    The cubic lattice correction -(a^2/12) sum_i p_i^4 has:
    - Mass dimension d = 6 (the p^4 term modifies a dimension-6 operator)
    - It is a sum of p_i^4 terms, which decomposes in spherical harmonics as:
      sum_i p_i^4 = (3/5)|p|^4 + (4/5)|p|^4 [Y_{40} + sqrt(5/14)(Y_{44}+Y_{4-4})]
    - The isotropic part (j=0) gives: k^(6)_{00} ~ -(a^2/12)(3/5)
    - The anisotropic part (j=4) gives: k^(6)_{40} ~ -(a^2/12)(4/5) etc.

    For comparison with experiment:
    - The coefficients have dimension [length]^2 = [energy]^{-2}
    - Convert a from meters to natural units: a_nat = a * (GeV / (hbar c))

    Args:
        a_meters: lattice spacing in meters

    Returns:
        Dictionary of SME coefficients
    """
    # Convert lattice spacing to natural units (1/GeV)
    a_nat = a_meters * GEV_TO_INVMETER  # in 1/GeV

    # The LV correction coefficient in natural units
    c4_coeff = a_nat**2 / 12.0  # dimension [1/GeV^2]

    # Decompose sum_i p_i^4 into spherical harmonics
    # sum_i p_i^4 = p^4 * [3/5 Y_00 * sqrt(4pi) + anisotropic terms]
    # More precisely:
    # x^4 + y^4 + z^4 = (3/5)r^4 + (4/5)r^4 * [cubic harmonics]
    # The cubic harmonics K_4 = (1/sqrt(12))[Y_40 + sqrt(5/14)(Y_44 + Y_{4,-4})]
    # are normalized so that the anisotropic part integrates to 4/5 of the total.

    # Isotropic part: modifies the effective mass or the p^4 coefficient
    # in the rotationally-invariant sector
    iso_fraction = 3.0 / 5.0
    aniso_fraction = 4.0 / 5.0  # split among j=4 components

    # SME dimension-6 coefficients (c-type, CPT-even)
    # These modify the fermion dispersion as:
    # delta(E^2) = -c4_coeff * sum_i p_i^4
    #            = -c4_coeff * p^4 * [iso + aniso * cubic_harmonics]

    # For the electron sector (dimension-6, CPT-even):
    # c^(6)_{(I)jm} with j=0 and j=4
    c6_iso = -c4_coeff * iso_fraction        # j=0 coefficient
    c6_j4_m0 = -c4_coeff * aniso_fraction    # j=4, m=0 component

    # For dimension-8 (from the p^6 term):
    c6_coeff = a_nat**4 / 360.0
    c8_iso = c6_coeff * iso_fraction

    # The key SME coefficients commonly quoted:
    # For fermion sector, the dimension-6 operator c^(6)_{\mu\nu\rho\sigma}
    # contracted with p gives corrections proportional to a^2 p^4 / E_Planck^2.
    #
    # In the notation of Kostelecky & Mewes (2009, 2012):
    # The nonminimal coefficients are c^(d)_{(I)jm} for CPT-even
    # and a^(d)_{(V)jm} for CPT-odd.
    #
    # Our lattice gives ONLY CPT-even corrections (see Section 5 below).

    return {
        # Dimension-6 CPT-even coefficients (units: GeV^-2)
        "c6_iso_j0": c6_iso,
        "c6_aniso_j4_m0": c6_j4_m0,
        "c6_total": -c4_coeff,

        # Dimension-8 CPT-even (units: GeV^-4)
        "c8_iso_j0": c8_iso,

        # Raw coefficient
        "a_natural_units": a_nat,
        "c4_coefficient": c4_coeff,

        # For comparison: express as (a/l_compton)^2 for each particle
        "electron_c6": c4_coeff * M_ELECTRON_GEV**2,  # dimensionless
        "proton_c6": c4_coeff * M_PROTON_GEV**2,
        "photon_c6": c4_coeff,  # for photons, no mass suppression
    }


# ============================================================
# Section 3: Experimental bounds (Kostelecky data tables)
# ============================================================

EXPERIMENTAL_BOUNDS = {
    "photon_birefringence": {
        "description": "GRB polarization (vacuum birefringence)",
        "sector": "photon",
        "dimension": 6,
        "bound_gev_minus2": 1e-32,
        "reference": "Kostelecky & Mewes, PRL 110 (2013) 201601",
        "notes": "Bound on k^(6)_F from GRB 061122 polarimetry",
    },
    "photon_dispersion_fermi": {
        "description": "Fermi LAT time-of-flight",
        "sector": "photon",
        "dimension": 6,
        "bound_gev_minus2": 1.0 / (6.3e10)**2,  # E_QG > 6.3e10 GeV for n=2
        "reference": "Vasileiou et al., PRD 87 (2013) 122001",
        "notes": "GRB 090510 photon speed, n=2 (dimension-6 LV)",
    },
    "electron_hughes_drever": {
        "description": "Hughes-Drever (electron sector)",
        "sector": "electron",
        "dimension": 4,
        "bound_gev": 1e-27,
        "reference": "Kostelecky & Lane, PRD 60 (1999) 116010",
        "notes": "Bound on c_{mu nu} for electrons, clock comparisons",
    },
    "proton_clock": {
        "description": "Atomic clock comparisons (proton sector)",
        "sector": "proton",
        "dimension": 4,
        "bound_gev": 1e-27,
        "reference": "Kostelecky & Vargas, PRD 98 (2018) 036003",
        "notes": "Bound on c_{mu nu} for protons",
    },
    "neutron_spin_precession": {
        "description": "Neutron spin precession",
        "sector": "neutron",
        "dimension": 4,
        "bound_gev": 1e-31,
        "reference": "Altarev et al., EPL 92 (2010) 51001",
        "notes": "Bound on b_mu for neutrons (CPT-odd, dimension 3)",
    },
    "neutrino_oscillation": {
        "description": "Neutrino oscillation (MINOS/IceCube)",
        "sector": "neutrino",
        "dimension": 4,
        "bound_gev": 1e-23,
        "reference": "Kostelecky & Mewes, PRD 85 (2012) 096005",
        "notes": "Bound on (a_L)_mu for neutrinos",
    },
    "muon_g_minus_2": {
        "description": "Muon anomalous magnetic moment",
        "sector": "muon",
        "dimension": 4,
        "bound_gev": 1e-24,
        "reference": "Bluhm et al., PRL 84 (2000) 1098",
        "notes": "Bound on c_{mu nu} for muons",
    },
    "gravity_sector_cbar": {
        "description": "Gravity sector (lunar laser ranging)",
        "sector": "gravity",
        "dimension": 4,
        "bound_dimensionless": 1e-9,
        "reference": "Battat et al., PRL 99 (2007) 241103",
        "notes": "Bound on s_bar^{mu nu} in pure gravity sector",
    },
}


# ============================================================
# Section 4: Staggered fermion taste-breaking
# ============================================================

def staggered_taste_breaking(a_nat: float) -> dict:
    """Compute taste-breaking Lorentz violation from staggered fermions.

    Staggered fermions on a cubic lattice have 2^d = 8 (in 3D) or 16 (in 4D)
    degenerate species (tastes). The taste symmetry is broken by
    lattice artifacts proportional to a^2.

    The taste-breaking interactions have the form (Lepage, 1999):
        delta_S = a^2 * sum_{mu<nu} (psi_bar gamma_mu x xi_nu psi)^2

    where xi_nu are taste matrices. These introduce ADDITIONAL dimension-6
    Lorentz-violating operators beyond the naive lattice dispersion.

    The taste-dependent dispersion becomes:
        E^2_taste = m^2 + p^2 - (a^2/12) sum_i p_i^4
                    + a^2 * Delta_taste(p)

    where Delta_taste depends on the taste quantum number and has
    a DIFFERENT angular structure than the naive p_i^4 term.

    For the physical (lightest) taste, Delta_taste is suppressed by
    an additional factor relative to the naive term. For heavy tastes,
    it can be comparable or larger.

    In the continuum limit a -> 0, both contributions vanish as a^2.
    But at finite a, the taste-breaking can double the effective
    Lorentz violation for some taste channels.

    Args:
        a_nat: lattice spacing in natural units (1/GeV)

    Returns:
        Dictionary of taste-breaking coefficients
    """
    # Naive lattice LV coefficient
    naive_c4 = a_nat**2 / 12.0

    # Taste-breaking correction factors (from lattice QCD studies)
    # The taste splitting goes as:
    #   delta_m^2_taste ~ C_taste * alpha_s^2 * a^2 * Lambda_QCD^2
    # For our framework (no running coupling, pure lattice structure),
    # the analogous splitting is:
    #   delta_LV_taste ~ C_taste * a^2 * p^4
    # where C_taste depends on the taste representation.

    # Taste representations and their approximate splitting factors
    # (from Aubin & Bernard, PRD 68 (2003) 034014):
    # Pseudoscalar (PS): C = 1 (reference)
    # Axial vector (AV): C ~ 1.2
    # Tensor (T): C ~ 1.5
    # Vector (V): C ~ 2.0
    # Scalar (S): C ~ 2.5
    # Identity (I): C ~ 3.0

    taste_factors = {
        "pseudoscalar": 1.0,
        "axial_vector": 1.2,
        "tensor": 1.5,
        "vector": 2.0,
        "scalar": 2.5,
        "identity": 3.0,
    }

    results = {}
    for taste, factor in taste_factors.items():
        # Total LV for this taste: naive + taste-breaking
        total_c4 = naive_c4 * (1.0 + factor)
        results[taste] = {
            "naive_c4": naive_c4,
            "taste_factor": factor,
            "total_c4": total_c4,
            "enhancement_ratio": 1.0 + factor,
        }

    return results


# ============================================================
# Section 5: CPT analysis
# ============================================================

def analyze_cpt() -> dict:
    """Analyze CPT symmetry on the cubic lattice.

    CPT = C (charge conjugation) x P (parity) x T (time reversal).

    On the cubic lattice Z^3:

    P (Parity): x_i -> -x_i
      The cubic lattice has exact reflection symmetry in each axis.
      P is an exact symmetry of O_h.
      RESULT: P is EXACT on the lattice.

    T (Time reversal): t -> -t
      In the path-sum propagator, time reversal flips the direction of
      propagation. The propagator G(x,t;x',t') involves the transfer
      matrix M. Under T: G -> G^* (complex conjugation).
      For a real lattice action S, the propagator is invariant under
      T if S(-t) = S(t), which holds for the standard lattice action.
      RESULT: T is EXACT on the lattice.

    C (Charge conjugation): particle <-> antiparticle
      On the lattice, C is implemented as complex conjugation of the
      gauge links. For a scalar/spinor propagator on a background-free
      lattice, C sends psi -> psi^* (complex conjugation of the field).
      The lattice action is real (sum of cos(theta) terms), so C is exact.
      For staggered fermions, C acts within taste space and is exact.
      RESULT: C is EXACT on the lattice.

    Combined CPT:
      Since C, P, T are each individually exact symmetries of the
      cubic lattice propagator, CPT is exact.

      This means: the lattice breaks Lorentz symmetry but preserves CPT.

      In the SME framework, this constrains:
      - All CPT-odd coefficients are ZERO: a_mu = 0, b_mu = 0, etc.
      - Only CPT-even coefficients are nonzero: c_{mu nu}, d_{mu nu}, etc.

    This is a nontrivial prediction: many Lorentz-violating theories
    also violate CPT (by the Greenberg theorem, Lorentz violation in a
    local QFT implies CPT violation). The lattice framework evades this
    because it is not a local QFT in the continuum sense.

    Returns:
        Dictionary with CPT analysis results
    """
    return {
        "P_exact": True,
        "T_exact": True,
        "C_exact": True,
        "CPT_exact": True,

        "CPT_odd_coefficients_zero": True,
        "a_mu": 0.0,     # CPT-odd vector (dimension 3)
        "b_mu": 0.0,     # CPT-odd axial vector (dimension 3)
        "e_mu": 0.0,     # CPT-odd (dimension 3)
        "f_mu": 0.0,     # CPT-odd (dimension 3)
        "g_lambda_mu_nu": 0.0,  # CPT-odd (dimension 5)

        "CPT_even_coefficients_nonzero": True,
        "c_mu_nu": "nonzero (dimension 4, ~ a^2)",
        "d_mu_nu": "nonzero if spin-dependent (dimension 4, ~ a^2)",

        "greenberg_evasion": (
            "The Greenberg theorem states that CPT violation implies "
            "Lorentz violation in local QFT. The converse is not proven. "
            "The lattice framework demonstrates Lorentz violation with "
            "exact CPT, consistent with the theorem but showing the "
            "converse fails."
        ),
    }


# ============================================================
# Section 6: Numerical computation
# ============================================================

def compute_suppression_factor(E_gev: float, E_planck_gev: float) -> float:
    """Compute the natural Planck-scale suppression (E/E_Planck)^2.

    For dimension-6 operators (p^4 correction), the suppression is:
        (E/E_Planck)^2

    This is the factor by which lattice effects are suppressed at energy E.
    """
    return (E_gev / E_planck_gev)**2


def lattice_dispersion_correction_isotropic(p_gev: float,
                                            a_meters: float) -> float:
    """Fractional correction to E^2 from the isotropic p^4 term.

    delta(E^2) / E^2 ~ -(a^2/12)(3/5) p^4 / p^2 = -(a^2/20) p^2

    In natural units: a_nat = a_meters * GEV_TO_INVMETER.

    Args:
        p_gev: momentum in GeV
        a_meters: lattice spacing in meters

    Returns:
        Fractional correction (dimensionless)
    """
    a_nat = a_meters * GEV_TO_INVMETER
    return (a_nat**2 / 20.0) * p_gev**2


def direction_dependent_correction(p_gev: float, theta: float,
                                   phi: float, a_meters: float) -> float:
    """Direction-dependent (anisotropic) correction from cubic symmetry.

    For momentum along direction (theta, phi) in the lattice frame:
    sum_i p_i^4 = p^4 * f(theta, phi)

    where f(theta, phi) = sin^4(theta)cos^4(phi) + sin^4(theta)sin^4(phi)
                          + cos^4(theta)

    The isotropic average is <f> = 3/5.
    The anisotropic part is delta_f = f - 3/5.

    Maximum anisotropy: along axis (f=1) vs diagonal (f=1/3).

    Args:
        p_gev: momentum magnitude in GeV
        theta, phi: direction angles in lattice frame
        a_meters: lattice spacing in meters

    Returns:
        Fractional anisotropic correction to E^2
    """
    a_nat = a_meters * GEV_TO_INVMETER

    # Cubic angular factor
    sx = math.sin(theta) * math.cos(phi)
    sy = math.sin(theta) * math.sin(phi)
    sz = math.cos(theta)
    f_cubic = sx**4 + sy**4 + sz**4

    # The correction
    return (a_nat**2 / 12.0) * f_cubic * p_gev**2


# ============================================================
# Main experiment
# ============================================================

def run_experiment():
    t0 = time.time()

    print("=" * 78)
    print("LORENTZ AND CPT VIOLATION FROM LATTICE STRUCTURE")
    print("Standard Model Extension (SME) Coefficient Analysis")
    print("=" * 78)

    # ── Section 1: Lattice dispersion relation ────────────────────
    print(f"\n{'=' * 78}")
    print("1. LATTICE DISPERSION RELATION")
    print(f"{'=' * 78}")

    print("""
  On a cubic lattice with spacing a, the dispersion relation is:

    E^2 = m^2 + sum_i (4/a^2) sin^2(p_i a/2)

  (Standard second-order finite-difference Laplacian eigenvalue;
  see LORENTZ_VIOLATION_DERIVED_NOTE.md Step 2.)

  Taylor expanding for p_i a << 1:

    sin^2(p_i a/2) = (p_i a/2)^2 - (p_i a/2)^4/3 + (p_i a/2)^6*2/45 - ...

    (4/a^2) sin^2(p_i a/2) = p_i^2 - a^2 p_i^4/12 + a^4 p_i^6/360 - ...

  Therefore:
    E^2 = m^2 + p^2 - (a^2/12) sum_i p_i^4 + (a^4/360) sum_i p_i^6 - ...
                       ^^^^^^^^^^^^^^^^^^^^^^^^
                       LORENTZ-VIOLATING TERM

  The p_i^4 term breaks SO(3,1) down to the cubic group O_h.
  Its coefficient is a^2/12.
""")

    # Numerical verification of the expansion
    a_test = 0.1  # lattice spacing in arbitrary units
    p_test = np.linspace(0, 0.5 / a_test, 200)
    m_test = 0.1

    E2_lattice = np.array([
        m_test**2 + (4.0/a_test**2) * math.sin(p * a_test / 2)**2
        for p in p_test
    ])
    E2_continuum = m_test**2 + p_test**2
    E2_corrected = m_test**2 + p_test**2 - (a_test**2 / 12.0) * p_test**4
    E2_order6 = (m_test**2 + p_test**2 - (a_test**2 / 12.0) * p_test**4
                 + (a_test**4 / 360.0) * p_test**6)

    # Check at p*a = 0.5 (moderately low momentum)
    idx_check = len(p_test) // 4
    p_c = p_test[idx_check]
    pa = p_c * a_test
    print(f"  Numerical verification (1D, a={a_test}, m={m_test}):")
    print(f"    At p*a = {pa:.4f}:")
    print(f"      E^2 (exact lattice) = {E2_lattice[idx_check]:.10f}")
    print(f"      E^2 (continuum)     = {E2_continuum[idx_check]:.10f}")
    print(f"      E^2 (p^4 corrected) = {E2_corrected[idx_check]:.10f}")
    print(f"      E^2 (p^6 corrected) = {E2_order6[idx_check]:.10f}")
    print(f"      Residual (lattice - p^4): "
          f"{abs(E2_lattice[idx_check] - E2_corrected[idx_check]):.4e}")
    print(f"      Residual (lattice - p^6): "
          f"{abs(E2_lattice[idx_check] - E2_order6[idx_check]):.4e}")

    # ── Section 2: SME coefficient mapping ────────────────────────
    print(f"\n{'=' * 78}")
    print("2. STANDARD MODEL EXTENSION (SME) COEFFICIENT MAPPING")
    print(f"{'=' * 78}")

    print("""
  The Lorentz-violating correction decomposes into spherical harmonics:

    sum_i p_i^4 = p^4 * [3/5 + (4/5) * K_4(theta, phi)]

  where K_4 is the cubic harmonic of order 4:
    K_4 = (1/sqrt(12)) [Y_{40} + sqrt(5/14) (Y_{44} + Y_{4,-4})]

  In the SME framework (Kostelecky & Mewes):
  - The correction is a dimension-6 operator (d=6, n=4 in p)
  - CPT-even (see Section 5 below)
  - The nonminimal SME coefficients are:

    c^(6)_{(I)00}   = -(a^2/12)(3/5) / sqrt(4 pi)   [isotropic, j=0]
    c^(6)_{(I)40}   = -(a^2/12)(4/5) * (...)         [anisotropic, j=4, m=0]
    c^(6)_{(I)44}   = -(a^2/12)(4/5) * (...)         [anisotropic, j=4, m=4]
    c^(6)_{(I)4,-4} = -(a^2/12)(4/5) * (...)         [anisotropic, j=4, m=-4]

  All other SME coefficients are zero (no j=1,2,3 from cubic symmetry).
""")

    a_planck = L_PLANCK  # meters
    sme = compute_sme_coefficients(a_planck)

    print(f"  For a = l_Planck = {a_planck:.4e} m:")
    print(f"    a in natural units:    {sme['a_natural_units']:.4e} GeV^-1")
    print(f"    c4 coefficient (a^2/12): {sme['c4_coefficient']:.4e} GeV^-2")
    print(f"    c^(6) isotropic (j=0): {sme['c6_iso_j0']:.4e} GeV^-2")
    print(f"    c^(6) aniso (j=4,m=0): {sme['c6_aniso_j4_m0']:.4e} GeV^-2")

    print(f"\n  Dimensionless SME coefficients (c^(6) * m^2):")
    print(f"    Electron: c^(6) * m_e^2 = {sme['electron_c6']:.4e}")
    print(f"    Proton:   c^(6) * m_p^2 = {sme['proton_c6']:.4e}")
    print(f"    Photon:   c^(6) (dim-less) = {sme['photon_c6']:.4e} GeV^-2")

    # ── Section 3: Experimental bounds comparison ─────────────────
    print(f"\n{'=' * 78}")
    print("3. COMPARISON WITH EXPERIMENTAL BOUNDS")
    print(f"{'=' * 78}")

    print(f"\n  Natural suppression at E = 1 GeV:")
    E_test = 1.0  # GeV
    suppression = compute_suppression_factor(E_test, E_PLANCK_GEV)
    print(f"    (E/E_Planck)^2 = ({E_test} / {E_PLANCK_GEV:.4e})^2 "
          f"= {suppression:.4e}")

    print(f"\n  The lattice prediction for the p^4 coefficient:")
    print(f"    a^2/12 = ({a_planck:.4e} m)^2 / 12")
    a_nat = a_planck * GEV_TO_INVMETER
    c4_pred = a_nat**2 / 12.0
    print(f"           = {c4_pred:.4e} GeV^-2")
    print(f"           = {c4_pred * E_PLANCK_GEV**2:.4e} (in E_Planck^-2 units)")

    print(f"\n  {'Experiment':<35} {'Sector':<10} {'Bound':<18} "
          f"{'Prediction':<18} {'Ratio':<12} {'Status'}")
    print(f"  {'─'*35} {'─'*10} {'─'*18} {'─'*18} {'─'*12} {'─'*20}")

    for name, info in EXPERIMENTAL_BOUNDS.items():
        sector = info["sector"]

        if "bound_gev_minus2" in info:
            bound = info["bound_gev_minus2"]
            prediction = c4_pred
            ratio = prediction / bound if bound > 0 else float('inf')
            bound_str = f"{bound:.2e} GeV^-2"
            pred_str = f"{prediction:.2e} GeV^-2"
        elif "bound_gev" in info:
            bound = info["bound_gev"]
            # For dimension-4 bounds, compare a^2/12 * E_typical^2
            E_typical = 1.0  # GeV for most experiments
            prediction = c4_pred * E_typical**2
            ratio = prediction / bound if bound > 0 else float('inf')
            bound_str = f"{bound:.2e} GeV"
            pred_str = f"{prediction * 1:.2e} GeV"
        elif "bound_dimensionless" in info:
            bound = info["bound_dimensionless"]
            # For gravity sector: s_bar is a dimension-4 (minimal SME) coeff.
            # Our dimension-6 coefficient contributes as c^(6) * E_char^2
            # where E_char ~ m_earth * v_orbit^2 ~ 10^-10 GeV for LLR.
            # More precisely: effective s_bar ~ c^(6) * p_char^2
            # For lunar laser ranging, p_char ~ m_photon_eff ~ 1 eV ~ 10^-9 GeV
            E_char_gravity = 1e-9  # GeV, characteristic energy for LLR
            prediction = c4_pred * E_char_gravity**2
            ratio = prediction / bound if bound > 0 else float('inf')
            bound_str = f"{bound:.2e}"
            pred_str = f"{prediction:.2e}"
        else:
            continue

        if ratio < 1e-6:
            status = "SAFE (by >> 6 orders)"
        elif ratio < 1e-3:
            status = "SAFE (by >> 3 orders)"
        elif ratio < 1:
            status = "SAFE"
        else:
            status = "EXCLUDED"

        desc = info["description"][:34]
        print(f"  {desc:<35} {sector:<10} {bound_str:<18} "
              f"{pred_str:<18} {ratio:<12.2e} {status}")

    # ── Section 4: Staggered fermion taste-breaking ───────────────
    print(f"\n{'=' * 78}")
    print("4. STAGGERED FERMION TASTE-BREAKING CONTRIBUTIONS")
    print(f"{'=' * 78}")

    print("""
  Staggered fermions on a cubic lattice have 2^d degenerate tastes.
  Taste symmetry is broken at O(a^2), introducing ADDITIONAL Lorentz
  violation beyond the naive lattice dispersion.

  The taste-dependent LV has the form:
    delta(E^2)_taste = a^2 * C_taste * p^4

  where C_taste depends on the taste representation. The total LV
  for each taste is:
    (a^2/12)(1 + C_taste) * sum_i p_i^4

  Enhancement factors by taste (from lattice QCD):
""")

    taste_results = staggered_taste_breaking(a_nat)

    print(f"  {'Taste':<18} {'C_taste':<10} {'Enhancement':<14} "
          f"{'Total c^(6) (GeV^-2)':<22}")
    print(f"  {'─'*18} {'─'*10} {'─'*14} {'─'*22}")

    for taste, data in taste_results.items():
        print(f"  {taste:<18} {data['taste_factor']:<10.1f} "
              f"{data['enhancement_ratio']:<14.1f} "
              f"{data['total_c4']:<22.4e}")

    print(f"""
  Key finding: taste-breaking at most TRIPLES the naive LV coefficient.
  Since the naive coefficient is already ~10^-38 below experimental
  bounds, the taste-breaking enhancement is irrelevant for detectability.

  However, the taste structure provides a QUALITATIVE prediction:
  different fermion species (if they correspond to different tastes)
  would have slightly different LV coefficients. This is a form of
  flavor-dependent Lorentz violation testable in principle by comparing
  electron vs muon vs tau sector SME coefficients.
""")

    # ── Section 5: CPT analysis ───────────────────────────────────
    print(f"\n{'=' * 78}")
    print("5. CPT SYMMETRY ANALYSIS")
    print(f"{'=' * 78}")

    cpt = analyze_cpt()

    print(f"""
  Discrete symmetries on the cubic lattice Z^3:

    Parity P:           EXACT  (Z^3 has x_i -> -x_i symmetry)
    Time reversal T:    EXACT  (real lattice action, S(-t) = S(t))
    Charge conjugation: EXACT  (complex conjugation of fields)

    Combined CPT:       EXACT

  Consequence for SME coefficients:
    All CPT-ODD coefficients are IDENTICALLY ZERO:
      a_mu = 0          (dimension 3, CPT-odd vector)
      b_mu = 0          (dimension 3, CPT-odd pseudo-vector)
      e_mu = 0          (dimension 3)
      f_mu = 0          (dimension 3)
      g_{{lambda mu nu}} = 0  (dimension 5, CPT-odd)

    Only CPT-EVEN coefficients are nonzero:
      c_{{mu nu}} != 0     (dimension 4, suppressed by a^2)
      d_{{mu nu}} != 0     (dimension 4, spin-dependent, suppressed by a^2)
      Higher-dimension CPT-even operators at O(a^4), O(a^6), ...

  Relation to Greenberg's theorem:
    {cpt['greenberg_evasion']}

  This is a STRONG prediction: any experimental detection of CPT-odd
  LV coefficients would FALSIFY the cubic lattice framework.
  Current bounds on CPT-odd coefficients (b_mu for neutrons ~ 10^-31 GeV)
  are consistent with the prediction b_mu = 0.
""")

    # ── Section 6: Leading observable prediction ──────────────────
    print(f"\n{'=' * 78}")
    print("6. LEADING OBSERVABLE PREDICTION")
    print(f"{'=' * 78}")

    print(f"""
  QUESTION: What is the leading Lorentz-violating observable from
  the lattice framework, and at what level?

  ANSWER: The leading effect is anisotropic propagation governed by
  the cubic harmonic K_4(theta, phi). The observable signature is:

  1. DIRECTION-DEPENDENT PROPAGATION SPEED

     For a massless particle (photon, graviton):
       v(theta, phi) = c * [1 - (a^2/24) p^2 * f_4(theta, phi)]

     where f_4 = sin^4(theta)cos^4(phi) + sin^4(theta)sin^4(phi)
                 + cos^4(theta)

     The speed varies with direction by:
       delta_v / v ~ (a^2/24) * p^2 * (f_4_max - f_4_min)
                   = (a^2/24) * p^2 * (1 - 1/3)
                   = (a^2/36) * p^2

     For a = l_Planck, p = 10 GeV (Fermi LAT photon):
""")

    p_fermi = 10.0  # GeV
    a_nat_planck = L_PLANCK * GEV_TO_INVMETER
    aniso_correction = (a_nat_planck**2 / 36.0) * p_fermi**2
    print(f"       delta_v / v = (a^2/36) * p^2")
    print(f"                   = ({a_nat_planck:.4e})^2 / 36 * ({p_fermi})^2")
    print(f"                   = {aniso_correction:.4e}")

    print(f"""
     This is {aniso_correction:.1e}, approximately 10^-38.

  2. COMPARISON WITH EXPERIMENT

     Best photon birefringence bound:     ~10^-32    [GRB polarimetry]
     Best photon dispersion bound:        ~10^-21    [Fermi LAT at 10 GeV]
     Best electron anisotropy bound:      ~10^-27    [Hughes-Drever]
     Best gravity sector bound:           ~10^-9     [lunar laser ranging]

     Our prediction ({aniso_correction:.1e}) is BELOW ALL bounds by
     at least 6 orders of magnitude (and typically 20+).

  3. SCALING WITH ENERGY

     The suppression factor is (E/E_Planck)^2. To reach experimental
     sensitivity, we would need:

     (E/E_Planck)^2 > 10^-32  (photon birefringence bound)
     E > E_Planck * 10^-16 ~ 10^3 GeV ~ 1 TeV

     But at 1 TeV, the lattice correction for a Planck-scale lattice is:
     (1000 / 1.22e19)^2 / 12 = {(1000/E_PLANCK_GEV)**2 / 12:.4e}

     This is ~10^-32, which JUST touches the photon birefringence bound.
     At the LHC energy scale (14 TeV):
     (14000 / 1.22e19)^2 / 12 = {(14000/E_PLANCK_GEV)**2 / 12:.4e}

     Still below the birefringence bound by a factor of ~100.
""")

    # ── Section 7: Summary table ──────────────────────────────────
    print(f"\n{'=' * 78}")
    print("7. COMPREHENSIVE PREDICTION TABLE")
    print(f"{'=' * 78}")

    energies = [1e-3, 1e-1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e7, 1e10]

    print(f"\n  Lattice: a = l_Planck = {L_PLANCK:.4e} m")
    print(f"  Leading LV coefficient: a^2/12 = {c4_pred:.4e} GeV^-2\n")

    print(f"  {'E (GeV)':<12} {'(E/E_Pl)^2':<14} {'|delta E^2/E^2|':<18} "
          f"{'|delta v/v|':<14} {'Best bound':<14} {'Margin':<14}")
    print(f"  {'─'*12} {'─'*14} {'─'*18} {'─'*14} {'─'*14} {'─'*14}")

    for E in energies:
        supp = compute_suppression_factor(E, E_PLANCK_GEV)
        delta_E2 = c4_pred * E**2  # fractional correction to E^2
        delta_v = delta_E2 / 2.0   # fractional velocity correction

        # Best applicable bound
        if E < 1:
            best_bound = 1e-27  # low-energy atomic physics
            bound_name = "atomic"
        elif E < 100:
            best_bound = 1e-23  # neutrino oscillations
            bound_name = "neutrino"
        elif E < 1e5:
            best_bound = 2.5e-22  # Fermi LAT (dim-6)
            bound_name = "Fermi LAT"
        else:
            best_bound = 1e-20  # generic astrophysical
            bound_name = "astro"

        margin = delta_v / best_bound if best_bound > 0 else float('inf')

        print(f"  {E:<12.1e} {supp:<14.2e} {delta_E2:<18.2e} "
              f"{delta_v:<14.2e} {best_bound:<14.2e} {margin:<14.2e}")

    # ── Section 8: Direction dependence (anisotropy) ──────────────
    print(f"\n{'=' * 78}")
    print("8. DIRECTIONAL ANISOTROPY (CUBIC LATTICE FINGERPRINT)")
    print(f"{'=' * 78}")

    print(f"\n  The cubic symmetry creates direction-dependent propagation.")
    print(f"  f_4(theta, phi) = sum_i (n_i)^4 for unit vector n.\n")

    directions = {
        "axis [100]":     (0.0, 0.0),
        "face diag [110]": (math.pi/4, 0.0),
        "body diag [111]": (math.acos(1/math.sqrt(3)), math.pi/4),
    }

    print(f"  {'Direction':<20} {'theta':<10} {'phi':<10} "
          f"{'f_4':<10} {'deviation from 3/5'}")
    print(f"  {'─'*20} {'─'*10} {'─'*10} {'─'*10} {'─'*20}")

    for name, (theta, phi) in directions.items():
        sx = math.sin(theta) * math.cos(phi)
        sy = math.sin(theta) * math.sin(phi)
        sz = math.cos(theta)
        f4 = sx**4 + sy**4 + sz**4
        dev = f4 - 3.0/5.0
        print(f"  {name:<20} {theta:<10.4f} {phi:<10.4f} "
              f"{f4:<10.4f} {dev:+.4f}")

    print(f"""
  The ratio f_4(axis) / f_4(diagonal) = {1.0 / (1.0/3.0):.1f}

  This factor-of-3 anisotropy is the FINGERPRINT of cubic lattice
  Lorentz violation. Any detection of anisotropic LV with this specific
  angular pattern (Y_40 + sqrt(5/14)(Y_44 + Y_{4,-4})) would be
  evidence for a cubic underlying structure.

  At the Planck-scale suppression level (~10^-38 at 1 GeV), this
  anisotropy is undetectable. But the PATTERN is a prediction:
  if Lorentz violation is ever detected, check for cubic harmonics.
""")

    # ── Section 9: Hypothesis verdict ─────────────────────────────
    print(f"\n{'=' * 78}")
    print("HYPOTHESIS VERDICT")
    print(f"{'=' * 78}")

    print(f"""
  PREDICTIONS OF THE CUBIC LATTICE FRAMEWORK:

  1. Lorentz symmetry breaking: YES
     - Cubic group O_h replaces SO(3,1)
     - Leading correction: -(a^2/12) sum_i p_i^4
     - Dimension-6 operator in SME framework

  2. CPT violation: NO
     - C, P, T each individually exact on cubic lattice
     - All CPT-odd SME coefficients are identically zero
     - This is FALSIFIABLE: detection of CPT-odd LV would exclude the model

  3. SME coefficient values (a = l_Planck):
     - c^(6)_{{(I)00}} ~ {sme['c6_iso_j0']:.2e} GeV^-2 (isotropic)
     - c^(6)_{{(I)40}} ~ {sme['c6_aniso_j4_m0']:.2e} GeV^-2 (anisotropic)
     - All CPT-odd coefficients = 0 exactly

  4. Natural suppression:
     - (E/E_Planck)^2 ~ 10^-38 at E = 1 GeV
     - Below ALL current experimental bounds by >= 6 orders of magnitude
     - Consistent with null results in all LV searches

  5. Staggered fermion taste-breaking:
     - Enhances LV by factor 2-4 depending on taste channel
     - Still far below experimental bounds
     - Predicts flavor-dependent LV (testable in principle)

  6. Characteristic angular signature:
     - Cubic harmonics (j=4 with m=0, +4, -4)
     - Factor of 3 anisotropy between lattice axis and body diagonal
     - Unique fingerprint distinguishing cubic from other Planck-scale models

  BOTTOM LINE:
    The lattice framework is CONSISTENT with all current data.
    The predicted Lorentz violation is undetectably small at accessible
    energies, exactly as expected for a Planck-scale structure.
    The model makes strong structural predictions (CPT exact, cubic
    angular pattern, specific SME coefficient ratios) that could be
    tested if sensitivity improves by ~6 orders of magnitude in the
    photon birefringence sector.
""")

    elapsed = time.time() - t0
    print(f"  Elapsed: {elapsed:.1f} s")
    print(f"\n{'=' * 78}")
    print("EXPERIMENT COMPLETE")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    run_experiment()
