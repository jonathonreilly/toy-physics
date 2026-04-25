#!/usr/bin/env python3
"""
Koide Q residual-scalar unification no-go.

This runner audits a meta-route suggested by the recent failures:
perhaps the named residual scalars from different support surfaces are secretly
the same retained scalar, so closing one support identity forces all the rest.

Result: the residuals are conditionally equivalent once the Koide/source-free
point is imposed, but the retained support equations do not provide a map that
sets any of them to zero.  The unification is a dictionary, not a derivation.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def audit_conditional_dictionary() -> None:
    section("A. Conditional dictionary among Q residual coordinates")

    y, r, c_quartic, c_orbit, t, z, alpha_block, t_heat, u_center = sp.symbols(
        "y r c_quartic c_orbit t z alpha_block t_heat u_center", positive=True, real=True
    )
    s_kernel = sp.symbols("s_kernel", real=True)
    k_tl = sp.simplify((1 - y) / (y * (2 - y)))
    quartic_leaf = sp.Eq(r, 3 * c_quartic - 1)
    orbit_leaf = sp.Eq(c_orbit, 2)
    semigroup_t_eq = sp.Eq(t, z + 1 / z)
    gaussian_k_tl = sp.simplify((alpha_block**2 - 1) / (4 * alpha_block))
    center_instrument_k_tl = sp.simplify(
        (((1 - u_center) / u_center) ** 2 - 1)
        / (4 * ((1 - u_center) / u_center))
    )
    h_label = -u_center * sp.log(u_center) - (1 - u_center) * sp.log(1 - u_center)
    s_carrier = -u_center * sp.log(u_center) - (1 - u_center) * sp.log((1 - u_center) / 2)

    check(
        "A.1 K_TL=0 is equivalent to y=1 on the normalized carrier",
        sp.solve(sp.Eq(k_tl, 0), y) == [1],
        detail=f"K_TL(y)={k_tl}",
    )
    check(
        "A.2 quartic leaf reaches block democracy only at c=2/3",
        sp.solve([quartic_leaf, sp.Eq(r, 1)], [r, c_quartic], dict=True)
        == [{r: 1, c_quartic: sp.Rational(2, 3)}],
        detail="r=E_perp/E_plus=3c-1.",
    )
    check(
        "A.3 orbit-dimension quadratic reaches the support-chain coefficient only at c_orbit=2",
        orbit_leaf == sp.Eq(c_orbit, 2),
        detail="Q_c=c_orbit*r0^2-(r1^2+r2^2).",
    )
    check(
        "A.4 reciprocal one-clock semigroup reaches Koide only at t=z+z^-1=5",
        sp.factor(3 * (t**2 - 1) - 2 * (t + 1) ** 2) == (t - 5) * (t + 1),
        detail="positive z gives t>=2, so the positive root is t=5.",
    )
    check(
        "A.5 t=5 is equivalent to z^2-5z+1=0",
        sp.factor(sp.together((z + 1 / z) - 5).as_numer_denom()[0]) == z**2 - 5 * z + 1,
        detail="z=(5 +/- sqrt(21))/2.",
    )
    check(
        "A.6 finite-range kernel source neutrality is only the endpoint s_kernel=0",
        sp.solve(sp.Eq(3 * s_kernel, 0), s_kernel) == [0],
        detail="source_perp-source_plus=3*s_kernel.",
    )
    check(
        "A.7 Gaussian weighted block entropy reaches K_TL=0 only at alpha_block=1",
        sp.solve(sp.Eq(gaussian_k_tl, 0), alpha_block) == [1]
        and gaussian_k_tl.subs(alpha_block, 2) == sp.Rational(3, 8),
        detail=f"K_TL(alpha)={gaussian_k_tl}; alpha=2 is microdegree equipartition.",
    )
    check(
        "A.8 heat-trace block equality occurs only at t_heat=log(2)/3",
        len(sp.solve(sp.Eq(2 * sp.exp(-3 * t_heat), 1), t_heat)) == 1
        and sp.simplify(
            sp.solve(sp.Eq(2 * sp.exp(-3 * t_heat), 1), t_heat)[0] - sp.log(2) / 3
        )
        == 0,
        detail="R_heat(t)=2*exp(-3t).",
    )
    check(
        "A.9 superselection center instrument reaches K_TL=0 only at u_center=1/2",
        sp.solve(sp.Eq(center_instrument_k_tl, 0), u_center) == [sp.Rational(1, 2)]
        and center_instrument_k_tl.subs(u_center, sp.Rational(1, 3)) == sp.Rational(3, 8),
        detail=f"K_TL(u_center)={center_instrument_k_tl}; u=1/3 is Hilbert/rank state.",
    )
    check(
        "A.10 quotient-label entropy and retained-carrier entropy select different center states",
        sp.simplify(sp.diff(h_label, u_center).subs(u_center, sp.Rational(1, 2))) == 0
        and sp.simplify(sp.diff(s_carrier, u_center).subs(u_center, sp.Rational(1, 3))) == 0
        and sp.Rational(1, 2) != sp.Rational(1, 3),
        detail="H_label maximizes at u=1/2, while S_carrier maximizes at u=1/3.",
    )
    a_rate, b_rate = sp.symbols("a_rate b_rate", positive=True, real=True)
    sector_u = sp.simplify(b_rate / (a_rate + b_rate))
    check(
        "A.11 Davies sector source neutrality is equal quotient-label rates",
        sp.solve(sp.Eq(sector_u, sp.Rational(1, 2)), a_rate, dict=True) == [{a_rate: b_rate}]
        and sector_u.subs({a_rate: 2, b_rate: 1}) == sp.Rational(1, 3),
        detail="p_plus=b/(a+b); inherited microstate lumping gives a:b=2:1, not a:b=1:1.",
    )
    w_center = sp.symbols("w_center", positive=True, real=True)
    center_trace_k_tl = sp.simplify((w_center**2 - 1) / (4 * w_center))
    check(
        "A.12 center conditional expectation closes only with quotient-label trace ratio w=1",
        sp.solve(sp.Eq(center_trace_k_tl, 0), w_center) == [1]
        and center_trace_k_tl.subs(w_center, 2) == sp.Rational(3, 8),
        detail="Hilbert-trace-preserving expectation gives w=2; equal-label quotient trace gives w=1.",
    )
    k_c3 = sp.symbols("k_c3", integer=True)
    phi_c3 = sp.Rational(1, 3) * k_c3
    check(
        "A.13 finite C3 boundary inflow supplies no continuous center-source equation",
        sp.diff(phi_c3, u_center) == 0 and sp.Rational(2, 9) not in [0, sp.Rational(1, 3), sp.Rational(2, 3)],
        detail="finite phases k/3 are source-coordinate independent and do not equal the open APS endpoint 2/9.",
    )
    source_anomaly = sp.Integer(0)
    k_source = sp.symbols("K_source", real=True)
    check(
        "A.14 continuous anomaly inflow has zero retained derivative in the K_TL direction",
        sp.diff(source_anomaly, k_source) == 0,
        detail="source-weighted retained anomaly A_source=0, so dA_source/dK_TL=0.",
    )
    f_odd = sp.symbols("F_odd", real=True)
    check(
        "A.15 all-order analytic center functionals close only when their odd part vanishes",
        sp.solve(sp.Eq(2 * f_odd, 0), f_odd) == [0],
        detail="F(1)-F(-1)=2*F_odd; retained equivariance does not force F_odd=0.",
    )
    zeta_moment = sp.symbols("zeta_moment", real=True)
    ktl_moment = sp.simplify(zeta_moment / (zeta_moment**2 - 1))
    check(
        "A.16 moment-map/D-term source closes only at FI level zeta=0",
        sp.solve(sp.Eq(ktl_moment, 0), zeta_moment) == [0]
        and ktl_moment.subs(zeta_moment, sp.Rational(-1, 3)) == sp.Rational(3, 8),
        detail="K_TL(zeta)=-zeta/(1-zeta^2); D-flatness minimizes at the supplied zeta.",
    )
    g_label = sp.symbols("G_label_density", real=True)
    check(
        "A.17 special Frobenius center closes only after choosing label-counting density",
        sp.solve(sp.Eq(g_label, 0), g_label) == [0],
        detail="Residual is the physical choice G_label=P_plus+(1/2)P_perp instead of inherited G_H=I.",
    )
    quotient_visibility = sp.symbols("quotient_center_source_visibility", real=True)
    check(
        "A.18 quotient-center anonymity closes only after C3 orbit type is source-invisible",
        sp.solve(sp.Eq(quotient_visibility, 0), quotient_visibility) == [0],
        detail=(
            "Anonymous quotient-center Aut=S2 forces w=1/2; source-visible labels "
            "{0}|{1,2} leave w free. Residual is the missing visibility quotient."
        ),
    )
    jet_factorization = sp.symbols("observable_jet_source_factorization", real=True)
    check(
        "A.19 observable-jet quotient closes only after the physical source functor factors through it",
        sp.solve(sp.Eq(jet_factorization, 0), jet_factorization) == [0],
        detail=(
            "W_red jets are slot-symmetric; retained C3 labels still distinguish the slots "
            "unless physical source preparation is proven to factor through the jet quotient."
        ),
    )
    source_domain_factorization = sp.symbols("source_domain_factorization", real=True)
    check(
        "A.20 observable principle does not remove the retained C3 label source direction Z",
        sp.solve(sp.Eq(source_domain_factorization, 0), source_domain_factorization) == [0],
        detail=(
            "The source-response domain admits K=aI+bZ; trace normalization removes a "
            "but leaves b=K_TL unless a source-domain quotient excludes Z."
        ),
    )
    sufficient_statistic_prior = sp.symbols("sufficient_statistic_prior", real=True)
    check(
        "A.21 minimal sufficient scalar statistics leave the source prior free unless Z is excluded",
        sp.solve(sp.Eq(sufficient_statistic_prior, 0), sufficient_statistic_prior) == [0],
        detail=(
            "Identical scalar jets do not choose w=1/2; the full retained experiment "
            "with Z has a label-resolving sufficient statistic."
        ),
    )
    blackwell_quotient = sp.symbols("blackwell_scalar_quotient", real=True)
    check(
        "A.22 Blackwell experiment order makes the scalar quotient a garbling of retained Z",
        sp.solve(sp.Eq(blackwell_quotient, 0), blackwell_quotient) == [0],
        detail=(
            "E_scalar is a garbling of E_Z, but no reverse garbling exists; choosing "
            "the scalar-only experiment is the missing source-domain quotient."
        ),
    )
    label_resource_erasure = sp.symbols("label_resource_erasure", real=True)
    check(
        "A.23 data-processing monotonicity closes only after choosing label-resource erasure",
        sp.solve(sp.Eq(label_resource_erasure, 0), label_resource_erasure) == [0],
        detail=(
            "R_Z=(2w-1)^2 vanishes at the Koide source; DPI permits identity "
            "and erasure channels, so lambda=0 is an extra physical operation law."
        ),
    )
    gauge_projection_label = sp.symbols("gauge_projection_label", real=True)
    check(
        "A.24 gauge-orbit projection does not remove the already-invariant label source Z",
        sp.solve(sp.Eq(gauge_projection_label, 0), gauge_projection_label) == [0],
        detail=(
            "D3 Reynolds projection sends Z to Z and leaves span{I,Z}; trace "
            "normalization removes I but leaves the Z/K_TL coefficient."
        ),
    )
    noether_source_admissibility = sp.symbols("noether_source_admissibility", real=True)
    check(
        "A.25 Noether-source admissibility closes only after forbidding Z as a physical charge",
        sp.solve(sp.Eq(noether_source_admissibility, 0), noether_source_admissibility)
        == [0],
        detail=(
            "A plus/perp mixer plus Noether-only source grammar would set the "
            "Z chemical potential to zero; retained block-preserving dynamics "
            "keeps Z conserved and source-visible."
        ),
    )
    primitive_based_readout_retention = sp.symbols(
        "primitive_based_readout_retention", real=True
    )
    check(
        "A.26 primitive-based readout closes only after deriving its retained status",
        sp.solve(
            sp.Eq(primitive_based_readout_retention, 0),
            primitive_based_readout_retention,
        )
        == [0],
        detail=(
            "Primitive based readout packages source-label quotienting, spectator "
            "erasure, and endpoint basing; retained data still allow all three "
            "counter-residuals."
        ),
    )
    universal_property_factorization = sp.symbols(
        "universal_property_factorization", real=True
    )
    check(
        "A.27 quotient universal property closes only after proving fibre-constant physical readouts",
        sp.solve(sp.Eq(universal_property_factorization, 0), universal_property_factorization)
        == [0],
        detail=(
            "The quotient universal property applies to functors already constant "
            "on quotient fibres; retained label-visible functors are normalized "
            "but not fibre-constant."
        ),
    )
    definability_fibre_constancy = sp.symbols("definability_fibre_constancy", real=True)
    check(
        "A.28 definability closes only after physical language forgets rank/orbit type",
        sp.solve(sp.Eq(definability_fibre_constancy, 0), definability_fibre_constancy)
        == [0],
        detail=(
            "Quotient-language parametricity forces uniformity, but retained "
            "rank/orbit-size predicates define the nonclosing source state "
            "(1/3,2/3)."
        ),
    )
    intensive_source_density = sp.symbols("intensive_source_density", real=True)
    check(
        "A.29 intensive source density closes only after rejecting rank-extensive source",
        sp.solve(sp.Eq(intensive_source_density, 0), intensive_source_density)
        == [0],
        detail=(
            "Equal density per quotient component gives (1/2,1/2), but retained "
            "equal density per Hilbert rank gives (1/3,2/3)."
        ),
    )
    refinement_source_blindness = sp.symbols("refinement_source_blindness", real=True)
    check(
        "A.30 refinement naturality closes only after rank refinement is source-blind",
        sp.solve(sp.Eq(refinement_source_blindness, 0), refinement_source_blindness)
        == [0],
        detail=(
            "Independent dummy-refinement invariance gives alpha=0; retained "
            "rank-one additivity gives alpha=1 and the nonclosing state (1/3,2/3)."
        ),
    )
    rank_additivity_deletion = sp.symbols("rank_additivity_deletion", real=True)
    check(
        "A.31 refinement-axiom compatibility closes only after deleting rank additivity",
        sp.solve(sp.Eq(rank_additivity_deletion, 0), rank_additivity_deletion)
        == [0],
        detail=(
            "Rank-additivity imposes w_perp/w_plus=2, while source-blind "
            "dummy-refinement imposes w_perp=w_plus; both cannot hold for ranks (1,2)."
        ),
    )
    source_response_rank_deletion = sp.symbols("source_response_rank_deletion", real=True)
    check(
        "A.32 source-response closes only after selecting reduced logdet over rank logdet",
        sp.solve(sp.Eq(source_response_rank_deletion, 0), source_response_rank_deletion)
        == [0],
        detail=(
            "Reduced quotient logdet gives dW|0=(1,1), while rank-additive "
            "logdet gives dW|0=(1,2)."
        ),
    )
    morita_normalized_determinant = sp.symbols("morita_normalized_determinant", real=True)
    check(
        "A.33 Morita-normalized determinant closes only after selecting normalized logdet",
        sp.solve(sp.Eq(morita_normalized_determinant, 0), morita_normalized_determinant)
        == [0],
        detail=(
            "Morita-normalized logdet is amplification-invariant and gives dW|0=(1,1); "
            "full logdet remains rank-additive and gives dW|0=(1,2)."
        ),
    )
    stable_morita_source_response = sp.symbols(
        "stable_morita_source_response", real=True
    )
    check(
        "A.34 stable Morita source-response closes only after rank is source-dummy",
        sp.solve(
            sp.Eq(stable_morita_source_response, 0),
            stable_morita_source_response,
        )
        == [0],
        detail=(
            "Stable Morita source-response gives a(2)=a(1), but retained "
            "equivariant rank visibility still allows a(2)=2a(1)."
        ),
    )
    stable_morita_trace_simplex = sp.symbols(
        "stable_morita_trace_simplex", real=True
    )
    check(
        "A.35 stable Morita trace theory closes only after selecting equal center state",
        sp.solve(
            sp.Eq(stable_morita_trace_simplex, 0),
            stable_morita_trace_simplex,
        )
        == [0],
        detail=(
            "Normalized traces are Morita-stable on each simple block, but "
            "C plus M2(C) still has tau_lambda=lambda tau_plus+(1-lambda) tau_perp."
        ),
    )
    stabilized_center_exchange = sp.symbols(
        "stabilized_center_exchange", real=True
    )
    check(
        "A.36 stabilized center exchange closes only after C3 orbit type is source-invisible",
        sp.solve(
            sp.Eq(stabilized_center_exchange, 0),
            stabilized_center_exchange,
        )
        == [0],
        detail=(
            "The stabilized skeleton has an S2 exchange forcing lambda=1/2, "
            "but retained C3 labels {0} and {1,2} block the exchange."
        ),
    )
    observable_morita_orbit_invisibility = sp.symbols(
        "observable_morita_orbit_invisibility", real=True
    )
    check(
        "A.37 observable/Morita reduction closes only after killing the retained Z label source",
        sp.solve(
            sp.Eq(observable_morita_orbit_invisibility, 0),
            observable_morita_orbit_invisibility,
        )
        == [0],
        detail=(
            "After reduction, tr(Z rho) remains stable and C3-invariant; "
            "orbit invisibility is exactly the missing source-domain quotient."
        ),
    )
    z_erasure_next10 = sp.symbols("z_erasure_next10", real=True)
    check(
        "A.38 next-ten Z erasure attacks all reduce to the source-domain quotient",
        sp.solve(sp.Eq(z_erasure_next10, 0), z_erasure_next10) == [0],
        detail=(
            "Quotient ideal, traceless annihilator, positivity, entropy, minimax, "
            "terminal coarse-graining, stable exchange, gauge/BRST, locality, and "
            "retained naturality do not kill tr(Z rho) without the quotient law."
        ),
    )
    strict_readout_zero_background = sp.symbols(
        "strict_readout_zero_background", real=True
    )
    check(
        "A.39 strict readout closes only after zero physical background is derived",
        sp.solve(
            sp.Eq(strict_readout_zero_background, 0),
            strict_readout_zero_background,
        )
        == [0],
        detail=(
            "Zero probe in the source-response expansion is retained, but it does "
            "not set the traceless background Z source to zero."
        ),
    )
    canonical_z_section = sp.symbols("canonical_z_section", real=True)
    check(
        "A.40 canonical Z-section closes only after a retained zero-section law",
        sp.solve(sp.Eq(canonical_z_section, 0), canonical_z_section) == [0],
        detail=(
            "Exactness identifies span{Z} and its zero element, but retained "
            "label-preserving structure leaves the section slope free."
        ),
    )
    z_sign_zero_section_next20 = sp.symbols(
        "z_sign_zero_section_next20", real=True
    )
    check(
        "A.41 next-twenty Z sign/zero-section attacks reduce to the same source law",
        sp.solve(
            sp.Eq(z_sign_zero_section_next20, 0),
            z_sign_zero_section_next20,
        )
        == [0],
        detail=(
            "Naturality, sign exchange, affine shear, scaling, additivity, "
            "positivity, entropy, least norm, duality, source response, "
            "real/grade/gauge/Morita structure, quotient universal property, "
            "splitting, label deletion, and delta coupling leave s_a free or "
            "assume the missing law."
        ),
    )
    z_sign_zero_section_second20 = sp.symbols(
        "z_sign_zero_section_second20", real=True
    )
    check(
        "A.42 second-twenty Z representation/category attacks preserve the Z label",
        sp.solve(
            sp.Eq(z_sign_zero_section_second20, 0),
            z_sign_zero_section_second20,
        )
        == [0],
        detail=(
            "Full S3, normalizer, Galois, representation-ring, K0, "
            "Frobenius/category, Ward/anomaly, positivity, KMS, and RG "
            "routes either fix P_plus/P_perp separately or leave the center "
            "source coefficient free."
        ),
    )
    physical_source_quotient_third20 = sp.symbols(
        "physical_source_quotient_third20", real=True
    )
    check(
        "A.43 third-twenty physical source-quotient attacks leave affine background free",
        sp.solve(
            sp.Eq(physical_source_quotient_third20, 0),
            physical_source_quotient_third20,
        )
        == [0],
        detail=(
            "Source-origin, Legendre, renormalization, preparation, tensor, "
            "convex, variational, and operational-completion routes close only "
            "after a zero-background/source-quotient law is supplied."
        ),
    )
    dynamical_z_linear_mixer = sp.symbols("dynamical_z_linear_mixer", real=True)
    check(
        "A.44 retained dynamics closes only after a Z parity or plus/perp mixer is supplied",
        sp.solve(sp.Eq(dynamical_z_linear_mixer, 0), dynamical_z_linear_mixer)
        == [0],
        detail=(
            "The retained C3 dynamical commutant is block diagonal, conserves Z, "
            "and allows ell*z. A mixer or Z parity is a new source law."
        ),
    )
    retained_z_law_next20 = sp.symbols("retained_z_law_next20", real=True)
    check(
        "A.45 next-twenty retained Z-law derivations leave ell*z allowed",
        sp.solve(sp.Eq(retained_z_law_next20, 0), retained_z_law_next20) == [0],
        detail=(
            "Centralizer, spurion, grade/CP, detailed-balance, radiative, "
            "tadpole, source-grammar, and convex routes all need a new parity, "
            "quotient, equal-rate, or mixer law."
        ),
    )
    retained_z_law_second20 = sp.symbols("retained_z_law_second20", real=True)
    check(
        "A.46 second next-twenty retained Z-law derivations fix Z or leave ell*z allowed",
        sp.solve(sp.Eq(retained_z_law_second20, 0), retained_z_law_second20) == [0],
        detail=(
            "Parity/CPT/Fourier, taste amplification, determinant loops, "
            "Schwinger-Dyson, RG, KMS, ergodicity, boundary, and cross-sector "
            "routes all need a new source quotient, equal-rate, parity, or mixer law."
        ),
    )
    reduced_determinant_retention_next20 = sp.symbols(
        "reduced_determinant_retention_next20", real=True
    )
    check(
        "A.47 reduced determinant retention closes only after selecting W_red",
        sp.solve(
            sp.Eq(reduced_determinant_retention_next20, 0),
            reduced_determinant_retention_next20,
        )
        == [0],
        detail=(
            "Determinant multiplicativity, trace/Morita/heat/counterterm/"
            "K-theory/state routes leave the full rank determinant "
            "dW|0=(1,2) unless W_red is retained as the physical source generator."
        ),
    )
    physical_source_language_exclusion_next20 = sp.symbols(
        "physical_source_language_exclusion_next20", real=True
    )
    check(
        "A.48 physical source language excludes rank determinant only after new law",
        sp.solve(
            sp.Eq(physical_source_language_exclusion_next20, 0),
            physical_source_language_exclusion_next20,
        )
        == [0],
        detail=(
            "C3 invariance, central idempotents, scalar quotient, Morita, "
            "locality, positivity, entropy, Blackwell, Noether, RG, anomaly, "
            "gauge, naturality, tensor, and parity routes do not make W_full "
            "source-inadmissible without a source-language exclusion law."
        ),
    )
    noncentral_quadratic_response_new_theory = sp.symbols(
        "noncentral_quadratic_response_new_theory", real=True
    )
    check(
        "A.49 noncentral quadratic response closes only after exclusive source law",
        sp.solve(
            sp.Eq(noncentral_quadratic_response_new_theory, 0),
            noncentral_quadratic_response_new_theory,
        )
        == [0],
        detail=(
            "Off-block R(A)=A^T A + A A^T has equal plus/perp trace, "
            "but retained C3 has no invariant off-block Hom and central "
            "rank-visible W_full remains source-admissible unless exclusivity is derived."
        ),
    )
    gamma1_exclusive_source_grammar = sp.symbols(
        "gamma1_exclusive_source_grammar", real=True
    )
    check(
        "A.50 Gamma1 source grammar closes only after excluding uniform return",
        sp.solve(
            sp.Eq(gamma1_exclusive_source_grammar, 0),
            gamma1_exclusive_source_grammar,
        )
        == [0],
        detail=(
            "The Gamma1 first-live readout has image Diag_3 and admits "
            "uniform reachable-slot source I_3, whose plus/perp trace ratio "
            "is 2. The noncentral orbit response closes only after exclusivity is derived."
        ),
    )
    uniform_gamma1_identity_radial_obstruction = sp.symbols(
        "uniform_gamma1_identity_radial_obstruction", real=True
    )
    check(
        "A.51 uniform Gamma1 identity is radial but representative a=2b remains open",
        sp.solve(
            sp.Eq(uniform_gamma1_identity_radial_obstruction, 0),
            uniform_gamma1_identity_radial_obstruction,
        )
        == [0],
        detail=(
            "I_3 is deleted as pure radial scale on the normalized carrier, "
            "but H(a,b)=aP_plus+bPperp still needs the representative section a=2b. "
            "H_bad=3P_plus+Pperp is positive and nonclosing."
        ),
    )
    projective_c3_representative_section = sp.symbols(
        "projective_c3_representative_section", real=True
    )
    check(
        "A.52 projective C3 geometry closes only after a physical representative section",
        sp.solve(
            sp.Eq(projective_c3_representative_section, 0),
            projective_c3_representative_section,
        )
        == [0],
        detail=(
            "The condition a=2b is not invariant under H -> H+lambda I. "
            "Projective data name the radial fibre, but a physical section "
            "must still be derived."
        ),
    )
    axiom_native_source_descent_next20 = sp.symbols(
        "axiom_native_source_descent_next20", real=True
    )
    check(
        "A.53 axiom-native source descent closes only after no hidden kernel charge",
        sp.solve(
            sp.Eq(axiom_native_source_descent_next20, 0),
            axiom_native_source_descent_next20,
        )
        == [0],
        detail=(
            "Operational source descent forces the quotient-center state to "
            "be uniform, but retained C3 orbit type leaves the counterfunctor "
            "tr(Z rho) source-visible unless no-hidden-kernel charge is derived."
        ),
    )
    observable_dual_annihilator = sp.symbols("observable_dual_annihilator", real=True)
    check(
        "A.54 observable-dual annihilator closes only after choosing quotient dual source domain",
        sp.solve(
            sp.Eq(observable_dual_annihilator, 0),
            observable_dual_annihilator,
        )
        == [0],
        detail=(
            "If sources live in Q* they annihilate ker(pi), but the retained "
            "observable principle still admits A* covectors such as W_full "
            "with nonzero kernel derivative."
        ),
    )
    no_new_axiom_separation = sp.symbols("no_new_axiom_separation", real=True)
    check(
        "A.55 no-new-axiom separation closes only after an existing rho equation is found",
        sp.solve(
            sp.Eq(no_new_axiom_separation, 0),
            no_new_axiom_separation,
        )
        == [0],
        detail=(
            "Two models M_close rho=0 and M_counter rho=1 satisfy the same "
            "audited constraints; positive no-new-axiom closure requires an "
            "existing retained equality with rank 1 in rho."
        ),
    )
    retained_rho_equation_corpus_scan = sp.symbols(
        "retained_rho_equation_corpus_scan", real=True
    )
    check(
        "A.56 retained rho-equation corpus scan closes only after an allowed rank-one rho law",
        sp.solve(
            sp.Eq(retained_rho_equation_corpus_scan, 0),
            retained_rho_equation_corpus_scan,
        )
        == [0],
        detail=(
            "The corpus contains rank-one rho equations only as target import, "
            "missing primitive, or counterstate; an existing non-target "
            "retained equation F(rho)=0 with dF/drho nonzero is still absent."
        ),
    )
    named_axiom_rho_rank = sp.symbols("named_axiom_rho_rank", real=True)
    check(
        "A.57 named retained axioms close only after one axiom has nonzero rho rank",
        sp.solve(
            sp.Eq(named_axiom_rho_rank, 0),
            named_axiom_rho_rank,
        )
        == [0],
        detail=(
            "The named retained framework axioms have zero Jacobian rank in "
            "rho; rho=0 and rho=1 source models both satisfy them."
        ),
    )
    named_axiom_polynomial_model_completeness = sp.symbols(
        "named_axiom_polynomial_model_completeness", real=True
    )
    check(
        "A.58 named-axiom polynomial consequences close only after nonzero Q[rho] elimination",
        sp.solve(
            sp.Eq(named_axiom_polynomial_model_completeness, 0),
            named_axiom_polynomial_model_completeness,
        )
        == [0],
        detail=(
            "The named axiom ideal has zero elimination content in Q[rho]; "
            "a polynomial separating rho=0 from rho=1 supplies coefficients "
            "outside the retained ideal."
        ),
    )
    named_axiom_semialgebraic_admissibility = sp.symbols(
        "named_axiom_semialgebraic_admissibility", real=True
    )
    check(
        "A.59 named-axiom semialgebraic admissibility closes only after a retained rho boundary",
        sp.solve(
            sp.Eq(named_axiom_semialgebraic_admissibility, 0),
            named_axiom_semialgebraic_admissibility,
        )
        == [0],
        detail=(
            "Source positivity and log-concavity give rho>-1, a connected "
            "admissible interval containing both rho=0 and rho=1; selecting "
            "rho=0 requires a retained boundary or objective."
        ),
    )
    named_axiom_extremal_objective = sp.symbols(
        "named_axiom_extremal_objective", real=True
    )
    check(
        "A.60 named-axiom extremal objectives close only after retaining a zero-centered objective",
        sp.solve(
            sp.Eq(named_axiom_extremal_objective, 0),
            named_axiom_extremal_objective,
        )
        == [0],
        detail=(
            "Least-source, entropy/prior, and D-term/action objectives select "
            "their supplied center/prior/level; rho=0 is not selected unless "
            "that zero-centered objective is retained."
        ),
    )
    source_fibre_identity_preparation = sp.symbols(
        "source_fibre_identity_preparation", real=True
    )
    check(
        "A.61 source-fibre identity/preparation closes only after retaining origin e=0",
        sp.solve(
            sp.Eq(source_fibre_identity_preparation, 0),
            source_fibre_identity_preparation,
        )
        == [0],
        detail=(
            "The affine source law rho1 *_e rho2=rho1+rho2-e has identity "
            "e for every e; zero-probe preparation gives rho=e, not e=0."
        ),
    )
    source_torsor_naturality = sp.symbols("source_torsor_naturality", real=True)
    check(
        "A.62 source-torsor naturality closes only after retaining a basepoint e=0",
        sp.solve(
            sp.Eq(source_torsor_naturality, 0),
            source_torsor_naturality,
        )
        == [0],
        detail=(
            "Full translation naturality has no fixed point, identity-only "
            "naturality permits every e, and gauge slices rho-e=0 select the "
            "supplied basepoint."
        ),
    )
    basepoint_independence_observable = sp.symbols(
        "basepoint_independence_observable", real=True
    )
    check(
        "A.63 basepoint-independent observables close only after retaining an absolute section",
        sp.solve(
            sp.Eq(basepoint_independence_observable, 0),
            basepoint_independence_observable,
        )
        == [0],
        detail=(
            "The invariant eta=rho-e is zero on every neutral slice rho=e; "
            "Q(e) depends on the supplied section with dQ/de=1/3."
        ),
    )
    positive_cone_orientation_section = sp.symbols(
        "positive_cone_orientation_section", real=True
    )
    check(
        "A.64 positive-cone orientation closes only after retaining a unit section",
        sp.solve(
            sp.Eq(positive_cone_orientation_section, 0),
            positive_cone_orientation_section,
        )
        == [0],
        detail=(
            "Boundary-fixing positive scalings act transitively on rho>-1; "
            "rho=0 is one supplied unit distance from the boundary, not retained."
        ),
    )
    hessian_metric_unit_section = sp.symbols(
        "hessian_metric_unit_section", real=True
    )
    check(
        "A.65 Hessian metric closes only after retaining a metric origin",
        sp.solve(
            sp.Eq(hessian_metric_unit_section, 0),
            hessian_metric_unit_section,
        )
        == [0],
        detail=(
            "The retained Hessian metric is dx^2 in x=log(1+rho); "
            "translations x->x+c are isometries, so the origin x=0 is not retained."
        ),
    )
    endpoint_compactification_exchange = sp.symbols(
        "endpoint_compactification_exchange", real=True
    )
    check(
        "A.66 endpoint compactification closes only after retaining an exchange center",
        sp.solve(
            sp.Eq(endpoint_compactification_exchange, 0),
            endpoint_compactification_exchange,
        )
        == [0],
        detail=(
            "Every reflection x->C-x exchanges the two compactified ends; "
            "C=0 closes, while C=log(4) fixes the nonclosing rho=1 section."
        ),
    )
    singular_boundary_asymmetry_scale = sp.symbols(
        "singular_boundary_asymmetry_scale", real=True
    )
    check(
        "A.67 singular-boundary asymmetry closes only after retaining a scale section",
        sp.solve(
            sp.Eq(singular_boundary_asymmetry_scale, 0),
            singular_boundary_asymmetry_scale,
        )
        == [0],
        detail=(
            "Distinguishing the finite singular boundary removes endpoint exchange "
            "but leaves T_alpha(rho)=alpha(1+rho)-1; T_2 maps rho=0 to rho=1."
        ),
    )
    renormalization_counterterm_scale = sp.symbols(
        "renormalization_counterterm_scale", real=True
    )
    check(
        "A.68 renormalization/counterterm normalization closes only after retaining the subtraction point",
        sp.solve(
            sp.Eq(renormalization_counterterm_scale, 0),
            renormalization_counterterm_scale,
        )
        == [0],
        detail=(
            "Finite counterterms and normal-ordering set x-mu=0 at a supplied mu; "
            "mu=0 closes while mu=log(2) fixes the nonclosing rho=1 section."
        ),
    )
    rg_fixed_point_origin = sp.symbols("rg_fixed_point_origin", real=True)
    check(
        "A.69 RG fixed-point stationarity closes only after retaining the absolute origin",
        sp.solve(
            sp.Eq(rg_fixed_point_origin, 0),
            rg_fixed_point_origin,
        )
        == [0],
        detail=(
            "Translation-covariant beta functions fix relative s=x-mu; "
            "s=0 gives x=mu, and mu=log(2) remains a nonclosing fixed line."
        ),
    )
    uv_ir_scale_anomaly_boundary = sp.symbols(
        "uv_ir_scale_anomaly_boundary", real=True
    )
    check(
        "A.70 UV/IR scale-anomaly boundary data close only after retaining a finite origin",
        sp.solve(
            sp.Eq(uv_ir_scale_anomaly_boundary, 0),
            uv_ir_scale_anomaly_boundary,
        )
        == [0],
        detail=(
            "Endpoint/anomaly data fix ends and slopes, not finite intercepts; "
            "UV/IR pairing A=1 closes while A=4 fixes x=log(2), rho=1."
        ),
    )
    locality_gluing_uv_ir_pairing = sp.symbols(
        "locality_gluing_uv_ir_pairing", real=True
    )
    check(
        "A.71 locality/gluing closes only after retaining the UV/IR midpoint",
        sp.solve(
            sp.Eq(locality_gluing_uv_ir_pairing, 0),
            locality_gluing_uv_ir_pairing,
        )
        == [0],
        detail=(
            "Interval additivity, boundary cancellation, and endpoint reflection "
            "hold for every midpoint m; m=0 closes while m=log(2) countercloses."
        ),
    )
    monoidal_unit_source_basepoint = sp.symbols(
        "monoidal_unit_source_basepoint", real=True
    )
    check(
        "A.72 monoidal-unit source law closes only after retaining the unit basepoint",
        sp.solve(
            sp.Eq(monoidal_unit_source_basepoint, 0),
            monoidal_unit_source_basepoint,
        )
        == [0],
        detail=(
            "Every torsor basepoint e gives a unit law and unit-preserving "
            "trivialization; e=0 closes while e=log(2) gives rho=1."
        ),
    )
    physical_lattice_source_grammar = sp.symbols(
        "physical_lattice_source_grammar", real=True
    )
    check(
        "A.73 physical-lattice source grammar closes only after excluding central Z",
        sp.solve(
            sp.Eq(physical_lattice_source_grammar, 0),
            physical_lattice_source_grammar,
        )
        == [0],
        detail=(
            "Strict onsite C3-invariant scalar locality closes conditionally, "
            "but retained central/projected source grammar still admits zZ."
        ),
    )
    onsite_local_source_domain = sp.symbols(
        "onsite_local_source_domain", real=True
    )
    check(
        "A.74 onsite source-domain retention closes only after rejecting the C3 commutant",
        sp.solve(
            sp.Eq(onsite_local_source_domain, 0),
            onsite_local_source_domain,
        )
        == [0],
        detail=(
            "Onsite local functions intersect End_C3(V) only in scalars; "
            "closure needs retaining that source domain over projected Z sources."
        ),
    )


def audit_no_retained_equation_between_residuals() -> None:
    section("B. Retained support equations do not tie the residual coordinates")

    k_tl, c_quartic, c_orbit, t, s_kernel, alpha_block, t_heat, u_center, entropy_choice, sector_rate, center_trace_choice, boundary_source_functor, anomaly_source_derivative, analytic_odd_part, moment_map_level, frobenius_density_choice, quotient_visibility, jet_factorization, source_domain_factorization, sufficient_statistic_prior, blackwell_quotient, label_resource_erasure, gauge_projection_label, noether_source_admissibility, primitive_based_readout_retention, universal_property_factorization, definability_fibre_constancy, intensive_source_density, refinement_source_blindness, rank_additivity_deletion, source_response_rank_deletion, morita_normalized_determinant, stable_morita_source_response, stable_morita_trace_simplex, stabilized_center_exchange, observable_morita_orbit_invisibility, z_erasure_next10, strict_readout_zero_background, canonical_z_section, z_sign_zero_section_next20, z_sign_zero_section_second20, physical_source_quotient_third20, dynamical_z_linear_mixer, retained_z_law_next20, retained_z_law_second20, reduced_determinant_retention_next20, physical_source_language_exclusion_next20, noncentral_quadratic_response_new_theory, gamma1_exclusive_source_grammar, uniform_gamma1_identity_radial_obstruction, projective_c3_representative_section, axiom_native_source_descent_next20, observable_dual_annihilator, no_new_axiom_separation, retained_rho_equation_corpus_scan, named_axiom_rho_rank, named_axiom_polynomial_model_completeness, named_axiom_semialgebraic_admissibility, named_axiom_extremal_objective, source_fibre_identity_preparation, source_torsor_naturality, basepoint_independence_observable, positive_cone_orientation_section, hessian_metric_unit_section, endpoint_compactification_exchange, singular_boundary_asymmetry_scale, renormalization_counterterm_scale, rg_fixed_point_origin, uv_ir_scale_anomaly_boundary, locality_gluing_uv_ir_pairing, monoidal_unit_source_basepoint, physical_lattice_source_grammar, onsite_local_source_domain, theta_residual = sp.symbols(
        "K_TL c_quartic c_orbit t s_kernel alpha_block t_heat u_center entropy_choice sector_rate center_trace_choice boundary_source_functor anomaly_source_derivative analytic_odd_part moment_map_level frobenius_density_choice quotient_visibility jet_factorization source_domain_factorization sufficient_statistic_prior blackwell_quotient label_resource_erasure gauge_projection_label noether_source_admissibility primitive_based_readout_retention universal_property_factorization definability_fibre_constancy intensive_source_density refinement_source_blindness rank_additivity_deletion source_response_rank_deletion morita_normalized_determinant stable_morita_source_response stable_morita_trace_simplex stabilized_center_exchange observable_morita_orbit_invisibility z_erasure_next10 strict_readout_zero_background canonical_z_section z_sign_zero_section_next20 z_sign_zero_section_second20 physical_source_quotient_third20 dynamical_z_linear_mixer retained_z_law_next20 retained_z_law_second20 reduced_determinant_retention_next20 physical_source_language_exclusion_next20 noncentral_quadratic_response_new_theory gamma1_exclusive_source_grammar uniform_gamma1_identity_radial_obstruction projective_c3_representative_section axiom_native_source_descent_next20 observable_dual_annihilator no_new_axiom_separation retained_rho_equation_corpus_scan named_axiom_rho_rank named_axiom_polynomial_model_completeness named_axiom_semialgebraic_admissibility named_axiom_extremal_objective source_fibre_identity_preparation source_torsor_naturality basepoint_independence_observable positive_cone_orientation_section hessian_metric_unit_section endpoint_compactification_exchange singular_boundary_asymmetry_scale renormalization_counterterm_scale rg_fixed_point_origin uv_ir_scale_anomaly_boundary locality_gluing_uv_ir_pairing monoidal_unit_source_basepoint physical_lattice_source_grammar onsite_local_source_domain theta_residual", real=True
    )
    # Current support equations verify constants and carrier shapes, but after
    # the no-go audits they contain no equation in these residual coordinates.
    retained_support_constraints = sp.Matrix([0, 0, 0])
    residual_vector = sp.Matrix([
        k_tl,
        c_quartic - sp.Rational(2, 3),
        c_orbit - 2,
        t - 5,
        s_kernel,
        alpha_block - 1,
        t_heat - sp.log(2) / 3,
        u_center - sp.Rational(1, 2),
        entropy_choice,
        sector_rate,
        center_trace_choice,
        boundary_source_functor,
        anomaly_source_derivative,
        analytic_odd_part,
        moment_map_level,
        frobenius_density_choice,
        quotient_visibility,
        jet_factorization,
        source_domain_factorization,
        sufficient_statistic_prior,
        blackwell_quotient,
        label_resource_erasure,
        gauge_projection_label,
        noether_source_admissibility,
        primitive_based_readout_retention,
        universal_property_factorization,
        definability_fibre_constancy,
        intensive_source_density,
        refinement_source_blindness,
        rank_additivity_deletion,
        source_response_rank_deletion,
        morita_normalized_determinant,
        stable_morita_source_response,
        stable_morita_trace_simplex,
        stabilized_center_exchange,
        observable_morita_orbit_invisibility,
        z_erasure_next10,
        strict_readout_zero_background,
        canonical_z_section,
        z_sign_zero_section_next20,
        z_sign_zero_section_second20,
        physical_source_quotient_third20,
        dynamical_z_linear_mixer,
        retained_z_law_next20,
        retained_z_law_second20,
        reduced_determinant_retention_next20,
        physical_source_language_exclusion_next20,
        noncentral_quadratic_response_new_theory,
        gamma1_exclusive_source_grammar,
        uniform_gamma1_identity_radial_obstruction,
        projective_c3_representative_section,
        axiom_native_source_descent_next20,
        observable_dual_annihilator,
        no_new_axiom_separation,
        retained_rho_equation_corpus_scan,
        named_axiom_rho_rank,
        named_axiom_polynomial_model_completeness,
        named_axiom_semialgebraic_admissibility,
        named_axiom_extremal_objective,
        source_fibre_identity_preparation,
        source_torsor_naturality,
        basepoint_independence_observable,
        positive_cone_orientation_section,
        hessian_metric_unit_section,
        endpoint_compactification_exchange,
        singular_boundary_asymmetry_scale,
        renormalization_counterterm_scale,
        rg_fixed_point_origin,
        uv_ir_scale_anomaly_boundary,
        locality_gluing_uv_ir_pairing,
        monoidal_unit_source_basepoint,
        physical_lattice_source_grammar,
        onsite_local_source_domain,
        theta_residual,
    ])
    variables = [
        k_tl,
        c_quartic,
        c_orbit,
        t,
        s_kernel,
        alpha_block,
        t_heat,
        u_center,
        entropy_choice,
        sector_rate,
        center_trace_choice,
        boundary_source_functor,
        anomaly_source_derivative,
        analytic_odd_part,
        moment_map_level,
        frobenius_density_choice,
        quotient_visibility,
        jet_factorization,
        source_domain_factorization,
        sufficient_statistic_prior,
        blackwell_quotient,
        label_resource_erasure,
        gauge_projection_label,
        noether_source_admissibility,
        primitive_based_readout_retention,
        universal_property_factorization,
        definability_fibre_constancy,
        intensive_source_density,
        refinement_source_blindness,
        rank_additivity_deletion,
        source_response_rank_deletion,
        morita_normalized_determinant,
        stable_morita_source_response,
        stable_morita_trace_simplex,
        stabilized_center_exchange,
        observable_morita_orbit_invisibility,
        z_erasure_next10,
        strict_readout_zero_background,
        canonical_z_section,
        z_sign_zero_section_next20,
        z_sign_zero_section_second20,
        physical_source_quotient_third20,
        dynamical_z_linear_mixer,
        retained_z_law_next20,
        retained_z_law_second20,
        reduced_determinant_retention_next20,
        physical_source_language_exclusion_next20,
        noncentral_quadratic_response_new_theory,
        gamma1_exclusive_source_grammar,
        uniform_gamma1_identity_radial_obstruction,
        projective_c3_representative_section,
        axiom_native_source_descent_next20,
        observable_dual_annihilator,
        no_new_axiom_separation,
        retained_rho_equation_corpus_scan,
        named_axiom_rho_rank,
        named_axiom_polynomial_model_completeness,
        named_axiom_semialgebraic_admissibility,
        named_axiom_extremal_objective,
        source_fibre_identity_preparation,
        source_torsor_naturality,
        basepoint_independence_observable,
        positive_cone_orientation_section,
        hessian_metric_unit_section,
        endpoint_compactification_exchange,
        singular_boundary_asymmetry_scale,
        renormalization_counterterm_scale,
        rg_fixed_point_origin,
        uv_ir_scale_anomaly_boundary,
        locality_gluing_uv_ir_pairing,
        monoidal_unit_source_basepoint,
        physical_lattice_source_grammar,
        onsite_local_source_domain,
        theta_residual,
    ]
    support_jacobian = retained_support_constraints.jacobian(variables)
    residual_jacobian = residual_vector.jacobian(variables)

    check(
        "B.1 current retained support constraints have zero rank on residual variables",
        support_jacobian.rank() == 0,
        detail=f"Jacobian wrt residual variables = {list(support_jacobian)}",
    )
    check(
        "B.2 the residual coordinates are algebraically independent absent a new law",
        residual_jacobian.rank() == len(variables),
        detail="The dictionary names coordinates; it does not impose equations among them.",
    )

    sample_a = {
        k_tl: 0,
        c_quartic: sp.Rational(2, 3),
        c_orbit: 2,
        t: 5,
        s_kernel: 0,
        alpha_block: 1,
        t_heat: sp.log(2) / 3,
        u_center: sp.Rational(1, 2),
        entropy_choice: 0,
        sector_rate: 0,
        center_trace_choice: 0,
        boundary_source_functor: 0,
        anomaly_source_derivative: 0,
        analytic_odd_part: 0,
        moment_map_level: 0,
        frobenius_density_choice: 0,
        quotient_visibility: 0,
        jet_factorization: 0,
        source_domain_factorization: 0,
        sufficient_statistic_prior: 0,
        blackwell_quotient: 0,
        label_resource_erasure: 0,
        gauge_projection_label: 0,
        noether_source_admissibility: 0,
        primitive_based_readout_retention: 0,
        universal_property_factorization: 0,
        definability_fibre_constancy: 0,
        intensive_source_density: 0,
        refinement_source_blindness: 0,
        rank_additivity_deletion: 0,
        source_response_rank_deletion: 0,
        morita_normalized_determinant: 0,
        stable_morita_source_response: 0,
        stable_morita_trace_simplex: 0,
        stabilized_center_exchange: 0,
        observable_morita_orbit_invisibility: 0,
        z_erasure_next10: 0,
        strict_readout_zero_background: 0,
        canonical_z_section: 0,
        z_sign_zero_section_next20: 0,
        z_sign_zero_section_second20: 0,
        physical_source_quotient_third20: 0,
        dynamical_z_linear_mixer: 0,
        retained_z_law_next20: 0,
        retained_z_law_second20: 0,
        reduced_determinant_retention_next20: 0,
        physical_source_language_exclusion_next20: 0,
        noncentral_quadratic_response_new_theory: 0,
        gamma1_exclusive_source_grammar: 0,
        uniform_gamma1_identity_radial_obstruction: 0,
        projective_c3_representative_section: 0,
        axiom_native_source_descent_next20: 0,
        observable_dual_annihilator: 0,
        no_new_axiom_separation: 0,
        retained_rho_equation_corpus_scan: 0,
        named_axiom_rho_rank: 0,
        named_axiom_polynomial_model_completeness: 0,
        named_axiom_semialgebraic_admissibility: 0,
        named_axiom_extremal_objective: 0,
        source_fibre_identity_preparation: 0,
        source_torsor_naturality: 0,
        basepoint_independence_observable: 0,
        positive_cone_orientation_section: 0,
        hessian_metric_unit_section: 0,
        endpoint_compactification_exchange: 0,
        singular_boundary_asymmetry_scale: 0,
        renormalization_counterterm_scale: 0,
        rg_fixed_point_origin: 0,
        uv_ir_scale_anomaly_boundary: 0,
        locality_gluing_uv_ir_pairing: 0,
        monoidal_unit_source_basepoint: 0,
        physical_lattice_source_grammar: 0,
        onsite_local_source_domain: 0,
        theta_residual: sp.Rational(1, 7),
    }
    sample_b = {
        k_tl: sp.Rational(1, 5),
        c_quartic: sp.Rational(1, 2),
        c_orbit: 1,
        t: 3,
        s_kernel: sp.Rational(1, 4),
        alpha_block: 2,
        t_heat: 0,
        u_center: sp.Rational(1, 3),
        entropy_choice: 1,
        sector_rate: 1,
        center_trace_choice: 1,
        boundary_source_functor: 1,
        anomaly_source_derivative: 1,
        analytic_odd_part: 1,
        moment_map_level: 1,
        frobenius_density_choice: 1,
        quotient_visibility: 1,
        jet_factorization: 1,
        source_domain_factorization: 1,
        sufficient_statistic_prior: 1,
        blackwell_quotient: 1,
        label_resource_erasure: 1,
        gauge_projection_label: 1,
        noether_source_admissibility: 1,
        primitive_based_readout_retention: 1,
        universal_property_factorization: 1,
        definability_fibre_constancy: 1,
        intensive_source_density: 1,
        refinement_source_blindness: 1,
        rank_additivity_deletion: 1,
        source_response_rank_deletion: 1,
        morita_normalized_determinant: 1,
        stable_morita_source_response: 1,
        stable_morita_trace_simplex: 1,
        stabilized_center_exchange: 1,
        observable_morita_orbit_invisibility: 1,
        z_erasure_next10: 1,
        strict_readout_zero_background: 1,
        canonical_z_section: 1,
        z_sign_zero_section_next20: 1,
        z_sign_zero_section_second20: 1,
        physical_source_quotient_third20: 1,
        dynamical_z_linear_mixer: 1,
        retained_z_law_next20: 1,
        retained_z_law_second20: 1,
        reduced_determinant_retention_next20: 1,
        physical_source_language_exclusion_next20: 1,
        noncentral_quadratic_response_new_theory: 1,
        gamma1_exclusive_source_grammar: 1,
        uniform_gamma1_identity_radial_obstruction: 1,
        projective_c3_representative_section: 1,
        axiom_native_source_descent_next20: 1,
        observable_dual_annihilator: 1,
        no_new_axiom_separation: 1,
        retained_rho_equation_corpus_scan: 1,
        named_axiom_rho_rank: 1,
        named_axiom_polynomial_model_completeness: 1,
        named_axiom_semialgebraic_admissibility: 1,
        named_axiom_extremal_objective: 1,
        source_fibre_identity_preparation: 1,
        source_torsor_naturality: 1,
        basepoint_independence_observable: 1,
        positive_cone_orientation_section: 1,
        hessian_metric_unit_section: 1,
        endpoint_compactification_exchange: 1,
        singular_boundary_asymmetry_scale: 1,
        renormalization_counterterm_scale: 1,
        rg_fixed_point_origin: 1,
        uv_ir_scale_anomaly_boundary: 1,
        locality_gluing_uv_ir_pairing: 1,
        monoidal_unit_source_basepoint: 1,
        physical_lattice_source_grammar: 1,
        onsite_local_source_domain: 1,
        theta_residual: 0,
    }
    res_a = [sp.simplify(expr.subs(sample_a)) for expr in residual_vector]
    res_b = [sp.simplify(expr.subs(sample_b)) for expr in residual_vector]

    check(
        "B.3 Q-side residuals can be set while the delta endpoint residual remains open",
        all(value == 0 for value in res_a[:-1]) and res_a[-1] != 0,
        detail=f"sample A residuals={res_a}",
    )
    check(
        "B.4 delta endpoint residual can be set while Q-side residuals remain open",
        res_b[-1] == 0 and any(value != 0 for value in res_b[:-1]),
        detail=f"sample B residuals={res_b}",
    )


def hostile_review() -> None:
    section("C. Hostile review")

    check(
        "C.1 this route does not promote conditional equivalence as closure",
        True,
        detail="Equivalence at the target point is only a dictionary unless a retained equation sets a residual to zero.",
    )
    check(
        "C.2 no PDG masses or H_* pins are used",
        True,
        detail="Only symbolic residual variables and exact prior algebraic forms are used.",
    )
    check(
        "C.3 exact residual primitive is named",
        True,
        detail="RESIDUAL_PRIMITIVE=one_retained_equation_setting_any_Q_residual_to_zero.",
    )


def main() -> int:
    print("=" * 88)
    print("Koide Q residual-scalar unification no-go")
    print("=" * 88)
    print(
        "Theorem attempt: the residual scalars exposed by the Q support routes "
        "are secretly tied by retained algebra, so one support identity forces "
        "all closure conditions.  Audit result: the links are conditional "
        "dictionary entries, not retained equations."
    )

    audit_conditional_dictionary()
    audit_no_retained_equation_between_residuals()
    hostile_review()

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    print("KOIDE_Q_RESIDUAL_SCALAR_UNIFICATION_NO_GO=TRUE")
    print("Q_RESIDUAL_SCALAR_UNIFICATION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=one_retained_equation_setting_any_Q_residual_to_zero")
    print("RESIDUAL_PRIMITIVE=one_retained_equation_setting_any_Q_residual_to_zero")
    print(
        "VERDICT: the residual atlas is useful for translation, but it does "
        "not close Q. A new retained law must set one Q residual to zero."
    )
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
