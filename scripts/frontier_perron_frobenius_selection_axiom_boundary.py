#!/usr/bin/env python3
"""
Perron-Frobenius selection axiom boundary on the current exact stack.

Question:
  Does the current exact Cl(3) on Z^3 stack already promote the existing
  sector-level Perron / dominant-mode theorems into one common sole-axiom
  physical-state selector?

Answer:
  No. Sector-local PF theorems are already exact once a positive operator is
  explicit. The current bank now has a Wilson parent/compression theorem on the
  gauge surface, but it still lacks the nontrivial sole-axiom PMNS
  source/transfer pack, a canonical projection theorem from that parent object
  to PMNS, and unique framework-point plaquette Perron data after the explicit
  spatial-environment kernel/rim map data are included.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS = 0
FAIL = 0
SUPPORT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS += 1
    else:
        FAIL += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def support(name: str, detail: str = "") -> None:
    global SUPPORT
    SUPPORT += 1
    msg = f"  [INFO] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def leading_mode(matrix: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    evals, evecs = np.linalg.eigh(matrix)
    order = np.argsort(evals)[::-1]
    evals = evals[order]
    vec = evecs[:, order[0]]
    if np.sum(vec) < 0:
        vec = -vec
    return float(evals[0]), vec, evals


def part1_reference_surface() -> None:
    print()
    print("=" * 88)
    print("PART 1: CURRENT-STACK REFERENCE SURFACE")
    print("=" * 88)

    plaquette_pf = read("docs/GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md")
    check(
        "Plaquette Perron note records one unique normalized strictly positive Perron vector",
        "one unique normalized strictly positive Perron vector" in plaquette_pf,
    )
    check(
        "Plaquette Perron note records exact reduction of the finite transfer problem to one Perron state",
        "there is one exact Perron state for the finite Wilson transfer problem" in plaquette_pf,
    )

    plaquette_open = read("docs/GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md")
    check(
        "Plaquette underdetermination note records distinct admissible residual operators can change Perron moments",
        "distinct admissible residual source-sector environment operators can induce distinct Perron moments" in plaquette_open
        and "produce different Perron moments" in plaquette_open,
    )

    pmns_transfer = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    check(
        "PMNS transfer note records a unique dominant symmetric mode",
        "unique dominant" in pmns_transfer and "doubly-degenerate orthogonal mode" in pmns_transfer,
    )
    check(
        "PMNS transfer note records failure to determine the 5-real corner-breaking source",
        "does **not** determine the generic `5`-real" in pmns_transfer
        and "corner-breaking source" in pmns_transfer,
    )

    pmns_hw1 = read("docs/PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    check(
        "PMNS hw=1 boundary note records exact closure if the nontrivial pack is supplied",
        "if the `hw=1` source/transfer pack is supplied" in pmns_hw1
        and "closes exactly" in pmns_hw1,
    )

    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    check(
        "PMNS sole-axiom boundary note records the canonical pack stays trivial",
        "stays trivial" in pmns_sole and "exactly `(I3, I3)`" in pmns_sole,
    )

    strong_cp = read("docs/STRONG_CP_THETA_ZERO_NOTE.md")
    check(
        "Strong-CP note records positive topological-sector weighting",
        "topological-sector weights are strictly positive" in strong_cp
        or "Z_Q >= 0" in strong_cp,
    )
    check(
        "Strong-CP note records the theta=0 selection inequality",
        "triangle inequality" in strong_cp and "free energy is minimized at" in strong_cp,
    )

    wilson_transfer = read("docs/GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md")
    check(
        "Wilson transfer note records an explicit positive self-adjoint one-clock transfer operator",
        "positive self-adjoint transfer operator" in wilson_transfer
        and "Z_(L_s,L_t)(beta) = Tr[T_(L_s,beta)^(L_t)]" in wilson_transfer,
    )

    parent_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    check(
        "Wilson parent/compression note records canonical plaquette and theta descendants from one parent object",
        "parent partition object" in parent_note
        and "Plaquette source-sector compression" in parent_note
        and "Topological Fourier descendant" in parent_note,
    )

    spatial_under = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_UNDERDETERMINATION_NOTE_2026-04-17.md")
    check(
        "Plaquette spatial-environment underdetermination note records distinct admissible S_6^env / eta_6 pairs can change beta=6 PF data",
        "S_6^env" in spatial_under
        and "eta_6" in spatial_under
        and "different plaquette PF data" in spatial_under,
    )

    spatial_construct = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CONSTRUCTION_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Plaquette spatial-environment construction-boundary note records K_6^env and the rim map to eta_6 as the earliest missing constructive datum",
        "K_6^env" in spatial_construct
        and "eta_6" in spatial_construct
        and "earliest missing constructive datum" in spatial_construct,
    )

    spatial_integral = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_ONE_SLAB_ORTHOGONAL_KERNEL_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md")
    check(
        "Plaquette one-slab integral-boundary note records K_beta^env is already fixed as a Wilson/Haar slab integral while explicit beta=6 evaluation remains open",
        "one-slab orthogonal kernel is exactly the Wilson/Haar integral" in spatial_integral
        and "does **not** yet evaluate those objects in explicit closed form at `beta = 6`" in spatial_integral,
    )

    rim_integral = read("docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md")
    check(
        "Plaquette full-slice rim-lift note records B_beta(W) is already fixed as a local Wilson/Haar rim integral while explicit beta=6 evaluation remains open",
        "full-slice local rim lift is the exact slice-space boundary function" in rim_integral
        and "explicit closed-form" in rim_integral
        and "beta = 6" in rim_integral,
    )

    beta6_reduction = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md")
    check(
        "Plaquette beta=6 evaluation-seam reduction note records the remaining seam is exactly class-sector matrix-element evaluation with canonical compressed W-dependence",
        "remaining explicit `beta = 6` problem is exactly evaluation" in beta6_reduction
        and "class-sector matrix elements" in beta6_reduction
        and "compressed `W`-dependence is already canonical" in beta6_reduction,
    )

    spatial_kernel = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_KERNEL_RIM_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    check(
        "Plaquette kernel/rim compression note records that explicit K_6^env and B_6 canonically generate S_6^env, rho_(p,q)(6), and the downstream PF data",
        "K_6^env" in spatial_kernel
        and "S_6^env" in spatial_kernel
        and "rho_(p,q)(6)" in spatial_kernel
        and "downstream plaquette PF data" in spatial_kernel
        and "canonically" in spatial_kernel,
    )

    rim_boundary = read("docs/GAUGE_VACUUM_PLAQUETTE_RIM_COUPLING_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Plaquette rim-coupling boundary note records explicit beta=6 evaluation of B_6(W) remains open even though the integral-expression class is fixed",
        "B_beta(W)" in rim_boundary
        and "explicit `beta = 6` evaluation of the Wilson rim-coupling lift `B_6(W)`" in rim_boundary,
    )

    rim_functional = read("docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md")
    check(
        "Plaquette compressed rim-functional uniqueness note records the retained left boundary functional is already the universal K(W)",
        "universal Peter-Weyl evaluation functional" in rim_functional
        and "retained left boundary functional is unique" in rim_functional,
    )

    scalar_insuff = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md")
    check(
        "Plaquette beta=6 scalar-value insufficiency note records that one same-surface scalar plaquette value does not determine v_6 or rho_(p,q)(6)",
        "only one scalar constraint" in scalar_insuff
        and "does **not** determine" in scalar_insuff
        and "v_6" in scalar_insuff
        and "rho_(p,q)(6)" in scalar_insuff,
    )

    retained_sampling = read("docs/GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md")
    check(
        "Plaquette retained class-sampling inversion note records that a retained finite coefficient vector is exactly recoverable from enough generic marked-holonomy samples",
        "retained coefficient vector is recovered exactly" in retained_sampling
        and "too few samples remain underdetermined" in retained_sampling
        and "finite inversion problem" in retained_sampling,
    )

    hermitian_nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    check(
        "Wilson-to-Hermitian current-bank nonrealization note records the missing step-2A bridge is not already hidden elsewhere in the current exact bank",
        "current exact bank does **not** already contain the missing" in hermitian_nonreal
        and "under another name" in hermitian_nonreal
        and "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in hermitian_nonreal,
    )

    sym_reduction = read("docs/GAUGE_VACUUM_PLAQUETTE_CONJUGATION_SYMMETRIC_RETAINED_SAMPLING_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Plaquette conjugation-symmetric retained-sampling reduction note records that conjugation symmetry lowers the physical retained sample burden to orbit count",
        "conjugation-orbit count" in sym_reduction
        and "orbit count" in sym_reduction
        and "three generic" in sym_reduction,
    )

    first_three = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_RECONSTRUCTION_NOTE_2026-04-17.md")
    check(
        "Plaquette first symmetric three-sample reconstruction note records that the first retained coefficient triple is recoverable from three explicit rational-angle holonomies",
        "three explicit regular rational-angle marked holonomies" in first_three
        and "decouples the `chi_(1,1)` orbit" in first_three
        and "three named same-surface sample values" in first_three,
    )

    radical_map = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette exact radical-form three-sample map note records that the sample matrix and inverse are explicit algebraic data, with structural W_A decoupling and only the three named sample values left to evaluate",
        "exact radical-form sample matrix" in radical_map
        and "exact algebraic map" in radical_map
        and "antipodal pair" in radical_map
        and "Z_6^env(W_A)" in radical_map
        and "Z_6^env(W_B)" in radical_map
        and "Z_6^env(W_C)" in radical_map,
    )

    constraint_boundary = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CURRENT_STACK_CONSTRAINT_BOUNDARY_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette current-stack constraint-boundary note records that the three named samples are not collapsed by conjugacy, inverse-conjugacy, or the current source-observable stack",
        "pairwise neither conjugate nor" in constraint_boundary
        and "inverse-conjugate" in constraint_boundary
        and "holonomy-resolved relations" in constraint_boundary
        and "no additional symmetry or source-observable collapse below the three named" in constraint_boundary,
    )

    local_partial = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette local Wilson partial-evaluation note records that the named seam already has exact local sample-side values even though the full environment amplitudes remain open",
        "exact sample-side values of `J(W_A), J(W_B), J(W_C)`" in local_partial
        and "exact sample-side values of the local Wilson one-plaquette weight" in local_partial
        and "normalized local one-plaquette sample values" in local_partial
        and "do **not** yet identify" in local_partial
        and "Z_6^env(W_A)" in local_partial
        and "B_6(W)" in local_partial,
    )

    local_obstruction = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette local-Wilson retained positive-cone obstruction note records that the explicit local three-sample block already fails the retained positive-cone test, so nonlocal K_6^env / B_6(W) completion is mathematically necessary",
        "does **not** lie in the exact first symmetric retained positive cone" in local_obstruction
        and "negative adjoint coefficient" in local_obstruction
        and "mathematically necessary" in local_obstruction
        and "K_6^env / B_6(W)" in local_obstruction,
    )

    tau_wedge = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_CONTROLLED_RETAINED_COEFFICIENT_WEDGE_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette tau-controlled retained-coefficient wedge note records explicit linear coefficient bounds in terms of one still-open tail mass Tau_(>1)",
        "outer wedge" in tau_wedge
        and "rho10 <= k10 (1 + tau)" in tau_wedge
        and "rho11 <= k11 (1 + tau)" in tau_wedge
        and "does **not** solve" in tau_wedge,
    )

    tau_nonderivation = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_UPPER_BOUND_NONDERIVATION_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette tau upper-bound nonderivation note records that the current seam constraints alone still admit arbitrarily large Tau_(>1), so no finite theorem-grade upper bound follows yet",
        "no finite theorem-grade upper bound on `Tau_(>1)`" in tau_nonderivation
        and "arbitrarily large `Tau_(>1)`" in tau_nonderivation
        and "`Z_hat_6(e) = 1 + T`" in tau_nonderivation
        and "`Tau_(>1) = T`" in tau_nonderivation,
    )

    tau_bound_route = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_BOUND_ROUTE_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette tau-bound route note records the sharp local-Wilson repair barrier tau >= 0.701560040093..., so no tau < 0.7 first-seam repair exists on that route",
        "`tau >= tau_*`" in tau_bound_route
        and "0.7015600400931378..." in tau_bound_route
        and "0.07110955014685417..." in tau_bound_route
        and "no route with `tau < 0.7015600400931378...` can repair" in tau_bound_route,
    )

    evaluator_route = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette environment-evaluator route note records that the three named values factor through one fixed three-row operator acting on one common beta-side vector, but the current stack still does not determine that vector",
        "`mathbf_Z_6 = E_3(v_6)`" in evaluator_route
        and "the three-row sample operator is the" in evaluator_route
        and "explicit radical matrix" in evaluator_route
        and "does **not** determine that beta-side vector" in evaluator_route
        and "does **not** yet furnish an actual evaluator" in evaluator_route,
    )

    identity_tau = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_IDENTITY_TAU_INSUFFICIENCY_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette identity-Tau insufficiency note records that even fixed Z_hat_6(e) together with fixed Tau_(>1) still leaves an affine retained fiber, so the retained pair and retained three-sample triple remain underdetermined",
        "fixed identity value plus" in identity_tau
        and "whole affine fiber of admissible retained" in identity_tau
        and "`18 rho_(1,0)(6) + 64 rho_(1,1)(6) = C`" in identity_tau
        and "the retained three-sample triple varies nontrivially" in identity_tau
        and "still do **not** determine the" in identity_tau,
    )

    fixed_retained_tau = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_FIXED_RETAINED_PAIR_TAU_NONCOLLAPSE_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette fixed-retained-pair/Tau noncollapse note records that even fixed (rho_(1,0), rho_(1,1), Tau_(>1)) still leaves nontrivial propagated-triple variation on the current coefficient-side bank",
        ("exact closure of `(rho_(1,0)(6), rho_(1,1)(6), Tau_(>1))`" in fixed_retained_tau
         or "fixing `(rho_(1,0)(6), rho_(1,1)(6))` and fixing `Tau_(>1)" in fixed_retained_tau)
        and "two-orbit higher slice" in fixed_retained_tau
        and "`Tau_(>1) = 72 u + 200 v`" in fixed_retained_tau
        and "still varies on the current coefficient-side bank" in fixed_retained_tau,
    )

    propagated_operator_nonclosure = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_OPERATOR_SIDE_NONCLOSURE_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette propagated-triple operator-side nonclosure note records that even exact evaluation of the minimal propagated triple still leaves nonunique higher-orbit beta-side data and so still does not close the operator-side beta=6 object",
        ("minimal propagated target" in propagated_operator_nonclosure
         or "minimal propagated three-sample target" in propagated_operator_nonclosure)
        and "still does **not** determine the full beta-side vector" in propagated_operator_nonclosure
        and ("four-orbit higher slice" in propagated_operator_nonclosure
             or "explicit four-orbit higher slice" in propagated_operator_nonclosure)
        and "same exact propagated retained triple" in propagated_operator_nonclosure
        and ("still **not** the whole operator-side closure datum" in propagated_operator_nonclosure
             or "still not an operator-side *closure* datum" in propagated_operator_nonclosure),
    )

    higher_orbit = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_IDENTITY_PLUS_THREE_SAMPLE_HIGHER_ORBIT_UNDERDETERMINATION_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette identity-plus-three-sample higher-orbit underdetermination note records that even the full first sample packet still leaves higher-orbit beta-side freedom",
        "full first sample packet" in higher_orbit
        and "nontrivial kernel by dimension alone" in higher_orbit
        and "explicit positive witness pair with the same first sample packet" in higher_orbit
        and "higher-orbit beta-side coefficients would still not be" in higher_orbit,
    )

    finite_packet = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md"
    )
    check(
        "Plaquette finite-sample-packet nonclosure note records that no finite marked-holonomy sample packet can by itself determine the full beta-side vector",
        "no finite sample packet" in finite_packet
        and "nontrivial kernel" in finite_packet
        and "two nonnegative higher-orbit coefficient stacks" in finite_packet
        and "full beta-side vector `v_6`" in finite_packet,
    )

    global_closure = read("docs/PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md")
    check(
        "Global current-stack closure note records that sector-local PF theorems are exact but one common sole-axiom global PF selector is still not derivable",
        "sector-local PF / dominant-mode theorems" in global_closure
        and "does **not** yet derive one common sole-axiom global PF selector" in global_closure
        and "PMNS-side global obstruction" in global_closure
        and "Plaquette-side global obstruction" in global_closure
        and "operator-plus-projection" in global_closure,
    )

    parent_intertwiner = read("docs/PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Parent/intertwiner boundary note records that step 1 is exact on the Wilson gauge surface but not yet globally across the live retained sectors",
        "step 1 is closed only on the Wilson gauge surface" in parent_intertwiner
        and "does **not** yet close step 1 globally" in parent_intertwiner
        and "Wilson-to-PMNS intertwiner / projection theorem" in parent_intertwiner
        and "more work on step 1 is still required" in parent_intertwiner,
    )

    three_step = read("docs/PERRON_FROBENIUS_THREE_STEP_GLOBAL_PROGRAM_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Three-step global-program boundary note records that step 1 is partial, step 2 is the actual bottleneck, and step 3 is downstream and not yet available",
        "Step 1:" in three_step
        and "partially closed" in three_step
        and "Step 2:" in three_step
        and "still no Wilson-to-PMNS descendant / intertwiner theorem" in three_step
        and "Step 3:" in three_step
        and "not closed" in three_step,
    )

    step2_boundary = read("docs/PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Wilson-to-PMNS descendant boundary note records that the actual step-2 bottleneck is cross-sector provenance, not lack of internal PMNS exact structure",
        "Wilson-to-PMNS descendant / intertwiner theorem" in step2_boundary
        and "cross-sector provenance" in step2_boundary
        and "internal PMNS" in step2_boundary
        and "step 2" in step2_boundary,
    )

    all_paths = read("docs/PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md")
    check(
        "All-paths attack-program note records the exact full PF work order and assigns the published-math templates to steps 1, 2, and 3",
        "Step-1 strengthening path" in all_paths
        and "Step-2A Hermitian descendant path" in all_paths
        and "Step-2B current path" in all_paths
        and "Plaquette operator sidecar" in all_paths
        and "Step-3 compatibility path" in all_paths
        and "10.1007/BF01614090" in all_paths
        and "10.1090/S0002-9939-1955-0069403-4" in all_paths
        and "10.1112/jlms/s2-17.2.345" in all_paths,
    )

    pmns_target = read("docs/PERRON_FROBENIUS_PMNS_DESCENDANT_TARGET_DECOMPOSITION_NOTE_2026-04-17.md")
    check(
        "PMNS descendant-target decomposition note records that step 2 itself splits into a Wilson-to-Hermitian descendant target and a residual Wilson-to-J_chi target if needed",
        "Hermitian descendant target" in pmns_target
        and "Residual non-Hermitian current target" in pmns_target
        and "`dW_e^H`, `H_e`" in pmns_target
        and "`J_chi`" in pmns_target
        and "aligned seed carrier is too small" in pmns_target,
    )

    proof_standard = read("docs/PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md")
    check(
        "External-theory proof-standard note records that atlas rows are index objects and external PF theory is only a hypothesis template unless the repo matches the hypotheses itself",
        "Atlas rows are index objects, not proof objects." in proof_standard
        and "Published mathematics is a hypothesis template, not a plug-in closure." in proof_standard
        and "No conclusion may be imported at wider scope" in proof_standard
        and "Luescher cannot be cited as if it already proves the repo’s global parent" in proof_standard
        and "Stinespring cannot be cited as if it already gives the missing" in proof_standard
        and "Evans-Hoegh-Krohn cannot be cited as if it already gives common-state" in proof_standard
        and "compatibility before the descendant theorem exists" in proof_standard,
    )

    hermitian_target = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Wilson-to-Hermitian descendant reduction note records that the first honest step-2A codomain is the charged-sector chain Wilson -> D_- -> dW_e^H -> H_e",
        "Wilson-to-Hermitian descendant theorem" in hermitian_target
        and "`Wilson -> D_- -> dW_e^H -> H_e`" in hermitian_target
        and "Schur pushforward" in hermitian_target
        and "selected transport packet" in hermitian_target
        and "projected-source triplet channels" in hermitian_target,
    )

    hermitian_boundary = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_STACK_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Wilson-to-Hermitian current-stack boundary note records that step 2A is no longer blocked by codomain ambiguity but by the missing Wilson-to-D_- / Wilson-to-dW_e^H descendant law",
        "the PMNS-side Hermitian codomain is already exact once microscopic `D` is" in hermitian_boundary
        and "constructive existence and minimal sheet-selection reduction are already" in hermitian_boundary
        and "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in hermitian_boundary,
    )

    step2_positive = read("docs/PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md")
    check(
        "Step-2 minimal positive-completion note records the exact two-stage positive target class: one Wilson-to-Hermitian descendant law plus at most one reduced PMNS bridge amplitude",
        "minimal positive step-2 completion class is now two-stage" in step2_positive
        and "Wilson -> D_- -> dW_e^H -> H_e" in step2_positive
        and "`B_red = a_sel (chi_N_nu - chi_N_e)`" in step2_positive,
    )

    shape_boundary = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Step-2 bridge-candidate-shape note records that scalar-only and support-only constructions are excluded and the admissible positive bridge is matrix-valued and cross-sector",
        "scalar-only and support-only candidate classes" in shape_boundary
        and "matrix-valued cross-sector descendant/intertwiner law" in shape_boundary,
    )

    operator_form = read("docs/PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Step-2 operator-form note records that any future positive step-2A theorem must be operator-level compression/intertwiner into charged-sector data",
        "operator-level descendant/intertwiner law" in operator_form
        and "`I_e^* T_Wilson I_e -> D_-`" in operator_form
        and "`P_e T_Wilson P_e -> dW_e^H`" in operator_form,
    )

    charged_embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Step-2 charged-embedding boundary note records that the next missing primitive is an explicit Wilson-side charged embedding/compression object for E_e",
        "explicit **Wilson-side charged embedding /" in charged_embedding
        and "`E_e`" in charged_embedding
        and "explicit Wilson-side operator `I_e` or `P_e`" in charged_embedding
        and "charged embedding/compression object on the Wilson parent space" in charged_embedding,
    )

    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Step-2 charged-support pullback boundary note records that the existing support bank cannot itself pull back E_e into a Wilson-side embedding/compression object",
        "does **not** supply a Wilson-side charged" in support_pullback
        and "support bank" in support_pullback
        and "not yet on the Wilson parent space" in support_pullback
        and "be obtained as a pure pullback of `E_e`" in support_pullback,
    )

    microscopic_target = read("docs/PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 microscopic-channel target note records that the live unresolved content is exactly a Wilson-to-charged microscopic channel, with Wilson -> D_- as the cleanest strong target",
        "Wilson-to-charged microscopic channel" in microscopic_target
        and "remaining unresolved content is not" in microscopic_target
        and "support labeling" in microscopic_target
        and "projector readout" in microscopic_target
        and "Wilson-to-`D_-` law" in microscopic_target,
    )

    direct_dweh = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Step-2 direct-dW_e^H route reduction note records that Wilson -> dW_e^H is a fully typed compressed route whose only remaining PMNS-side blocker is the right-sensitive selector on dW_e^H",
        "direct `dW_e^H` route is already sharply reduced" in direct_dweh
        and "the compressed target: `Wilson -> dW_e^H`" in direct_dweh
        and "only remaining PMNS-side" in direct_dweh
        and "right-sensitive selector on `dW_e^H`" in direct_dweh,
    )

    two_route = read("docs/PERRON_FROBENIUS_STEP2_TWO_ROUTE_CURRENT_BANK_CLOSURE_NOTE_2026-04-17.md")
    check(
        "Step-2 two-route current-bank closure note records that the honest upstream step-2A route space is exhausted by Wilson -> D_- and Wilson -> dW_e^H, and the current bank realizes neither",
        "route space is exhausted by exactly two routes" in two_route
        and "`Wilson -> D_-`" in two_route
        and "`Wilson -> dW_e^H`" in two_route
        and "current exact bank already realizes neither route" in two_route,
    )

    strong_breaking = read("docs/PERRON_FROBENIUS_STEP2_STRONG_ROUTE_BREAKING_SOURCE_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 strong-route breaking-source target note records that Wilson -> D_- is already reduced to the off-seed 5-real breaking-source law beyond the aligned seed patch",
        "live strong-route content is only the" in strong_breaking
        and "off-seed breaking-source law" in strong_breaking
        and "aligned seed patch" in strong_breaking
        and "`(xi_1, xi_2, eta_1, eta_2, delta)`" in strong_breaking,
    )

    active_five = read("docs/PERRON_FROBENIUS_STEP2_ACTIVE_FIVE_REAL_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 active-five-real target note records that the active off-seed five-real packet is the smallest live D_-level target, while the compressed route factors through the smaller dW_e^H law",
        "smallest live `D_-`-level target on step 2A" in active_five
        and "off-seed `5`-real source" in active_five
        and "smaller charged Hermitian projected-source" in active_five
        and "`dW_e^H`" in active_five,
    )

    active_five_nonreal = read("docs/PERRON_FROBENIUS_STEP2_ACTIVE_FIVE_REAL_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    check(
        "Step-2 active-five-real current-bank nonrealization note records that the current exact bank still does not determine the active off-seed five-real packet",
        "current exact bank still does **not** determine the active" in active_five_nonreal
        and "off-seed `5`-real source" in active_five_nonreal
        and "next missing construction is one exact packet" in active_five_nonreal,
    )

    source_family = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 charged-source-family target note records that the compressed route is blocked by one Wilson-side charged source family/channel primitive rather than missing downstream reconstruction algebra",
        "remaining constructive primitive on the compressed route is" in source_family
        and "Wilson-side charged source family / channel" in source_family
        and "not more downstream" in source_family
        and "reconstruction algebra" in source_family,
    )

    source_family_nonreal = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    check(
        "Step-2 charged-source-family current-bank nonrealization note records that the current exact bank does not already realize the remaining compressed-route primitive",
        "current exact bank does **not** already realize the Wilson-side" in source_family_nonreal
        and "charged source family / channel primitive" in source_family_nonreal
        and "genuinely constructive one-primitive gap" in source_family_nonreal,
    )

    source_family_nine = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_CHARGED_SOURCE_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 nine-channel charged-source target note records that the compressed primitive may be posed as a finite nine-channel charged Hermitian response family on E_e",
        "finite **nine-channel charged Hermitian source family**" in source_family_nine
        and "nine real linear responses" in source_family_nine
        and "finite nine-channel charged Hermitian source family on `E_e`" in source_family_nine
        and "does **not** bypass the charged-embedding problem" in source_family_nine,
    )

    embedded_candidate = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_CANDIDATE_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Step-2 rank-3 embedded nine-probe candidate-boundary note records that the strongest live positive compressed-route class is a rank-3 charged embedding/compression together with the induced nine-probe Hermitian response family",
        "rank-3 Wilson-side charged embedding/compression `I_e` or `P_e`" in embedded_candidate
        and "embedded nine-probe Hermitian source family" in embedded_candidate
        and "everything weaker than the embedded rank-3" in embedded_candidate,
    )

    embedded_explicit = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "Step-2 rank-3 embedded nine-probe explicit-response boundary note sharpens that live class to formula-level operator/source form and closes the sharper current-bank no-go on that class itself",
        "`J_a(t) = t I_e B_a I_e^*`" in embedded_explicit
        and "`M_e := I_e^* D^(-1) I_e`" in embedded_explicit
        and "`H_e^(cand) := (M_e + M_e^*) / 2`" in embedded_explicit
        and "`(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`" in embedded_explicit
        and "current exact bank still does **not** realize" in embedded_explicit,
    )

    resolvent_target = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 Hermitian resolvent-compression target note reduces the explicit-response family to one operator identity H_e^(cand) = H_e and carries the sharper current-bank no-go at that same level",
        "`H_e^(cand) := (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`" in resolvent_target
        and "the following are equivalent" in resolvent_target
        and "`(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`" in resolvent_target
        and "basis `B_1, ..., B_9`" in resolvent_target
        and "current bank still does **not** realize even that sharper target" in resolvent_target,
    )

    matrix_source = read("docs/PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson matrix-source embedding target note sharpens theorem-grade I_e / P_e to an equivalent rank-3 Wilson matrix-source embedding Phi_e and carries the sharper invariant-form no-go at that same level",
        "rank-3 Wilson **matrix-source embedding**" in matrix_source
        and "`Phi_e : Mat_3(C) -> End(H_W)`" in matrix_source
        and "`Phi_e(X) = I_e X I_e^*`" in matrix_source
        and "`Phi_e(1_3) = P_e`" in matrix_source
        and "the following are equivalent" in matrix_source
        and "still does **not** realize theorem-grade rank-3 Wilson" in matrix_source,
    )

    nine_channel_min = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_MINIMALITY_NOTE_2026-04-17.md")
    check(
        "Step-2 nine-channel minimality note records that nine real Wilson response channels are dimensionally minimal for arbitrary Herm(3) data and that eight or fewer generic channels cannot close the compressed route without extra structure",
        "exact minimal finite number of real response channels" in nine_channel_min
        and ("determine arbitrary `H_e` is `9`" in nine_channel_min
             or "target data is `9`" in nine_channel_min)
        and ("eight or fewer real channels cannot separate all" in nine_channel_min
             or "eight or fewer real channels cannot separate all Hermitian" in nine_channel_min),
    )

    hermitian_source = read("docs/PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 Hermitian source-embedding target note records that the compressed response theorem uses only the Hermitian restriction Psi_e of the stronger Wilson source algebra Phi_e and that the current bank still realizes neither one",
        "`Psi_e := Phi_e |_(Herm(3)) : Herm(3) -> Herm(H_W)`" in hermitian_source
        and "two exact attack surfaces" in hermitian_source
        and "stronger invariant algebra route through full `Phi_e`" in hermitian_source
        and "weaker minimal response route through the Hermitian source embedding" in hermitian_source
        and "still does **not** realize theorem-grade Hermitian source embedding" in hermitian_source,
    )

    compressed_block = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_RESOLVENT_BLOCK_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson compressed-resolvent block target note records that Phi_e plus H_e^(cand)=H_e collapses to one invariant rank-3 Wilson block law P_e S_W P_e |_(Ran(P_e)) ~= H_e, and that the current bank still realizes none of that block data",
        "`S_W := (D^(-1) + (D^(-1))^*) / 2`" in compressed_block
        and "`P_e S_W P_e = I_e H_e I_e^*`" in compressed_block
        and "unitarily equivalent to `H_e`" in compressed_block
        and "strongest honest next Wilson compressed-route theorem surface" in compressed_block
        and "still does **not** realize even that sharper object" in compressed_block,
    )

    compressed_block_spectral = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson compressed-block spectral-reduction note records that once the rank-3 Wilson support exists, the compressed block law reduces to the three scalar spectral identities Tr(B_e^k)=Tr(H_e^k), k=1,2,3, while the current bank still does not reach even that post-support stage",
        "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in compressed_block_spectral
        and "three scalar spectral identities" in compressed_block_spectral
        and "current exact bank still does **not** realize" in compressed_block_spectral
        and "three-scalar verification stage" in compressed_block_spectral,
    )

    packet_realization = read("docs/PERRON_FROBENIUS_STEP2_WILSON_HERMITIAN_SOURCE_PACKET_REALIZATION_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson Hermitian source-packet realization note records that theorem-grade Wilson support realization is exactly equivalent to one finite 9-element Hermitian source packet with explicit matrix-unit reconstruction identities, while the current bank still does not realize even that finite packet",
        "`9`-tuple of Hermitian Wilson operators" in packet_realization
        and "`F_12 = (S_4 + i S_5)/2`" in packet_realization
        and "satisfy the exact matrix-unit relations" in packet_realization
        and "current exact bank still does **not** realize even this finite packet" in packet_realization,
    )

    finite_certificate = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FINITE_CERTIFICATE_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson finite-certificate target note records that the whole compressed Wilson route is one finite 9+3 certificate: a 9-element Hermitian support packet plus 3 scalar spectral identities, while the current bank still fails at the first support-side layer",
        "The whole Wilson compressed route is now equivalent to one finite certificate" in finite_certificate
        and "`9`-element Hermitian support packet" in finite_certificate
        and "`3` scalar spectral identities" in finite_certificate
        and "finite checklist" in finite_certificate
        and "still does **not** realize the full finite certificate" in finite_certificate
        and "still fails at the first layer" in finite_certificate,
    )

    seven_packet = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson seven-packet chain-reduction note records that theorem-grade Wilson support realization is already equivalent to a smaller nearest-neighbor 7-packet chain certificate, with the (1,3) corner downstream and the current bank still failing at that sharper support layer",
        "nearest-neighbor Hermitian chain packet" in seven_packet
        and "The `(1,3)` corner is algebraically downstream of the chain" in seven_packet
        and "one nearest-neighbor `7`-packet plus finite chain identities" in seven_packet
        and "current bank still does **not** realize even this sharper" in seven_packet
        and "nearest-neighbor `7`-packet" in seven_packet,
    )

    sharp_certificate = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SHARP_FINITE_CERTIFICATE_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson sharp finite-certificate target note records that the whole compressed Wilson route is now exactly one 7+3 certificate: a nearest-neighbor 7-packet support layer plus 3 scalar spectral identities, with the current bank still failing at the first support layer",
        "one sharp finite `7 + 3` certificate" in sharp_certificate
        and "nearest-neighbor Hermitian `7`-packet" in sharp_certificate
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in sharp_certificate
        and "current bank still does **not** realize even the first `7`-packet layer" in sharp_certificate
        and "support-side first" in sharp_certificate,
    )

    four_packet = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson four-packet off-diagonal reduction note records that theorem-grade Wilson support realization is already equivalent to an off-diagonal Hermitian 4-packet, with diagonal support data downstream and the current bank still failing at that sharper support layer",
        "off-diagonal Hermitian nearest-neighbor `4`-packet" in four_packet
        and "The diagonal matrix units are already products of the off-diagonal chain" in four_packet
        and "one Hermitian off-diagonal `4`-packet plus finite chain identities" in four_packet
        and "current bank still does **not** realize even this sharper off-diagonal" in four_packet,
    )

    sharpest_certificate = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SHARPEST_FINITE_CERTIFICATE_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 Wilson sharpest finite-certificate target note records that the whole compressed Wilson route is now exactly one 4+3 certificate: an off-diagonal Hermitian 4-packet support layer plus 3 scalar spectral identities, with the current bank still failing at the first support layer",
        "one sharpest finite `4 + 3` certificate" in sharpest_certificate
        and "off-diagonal Hermitian nearest-neighbor `4`-packet" in sharpest_certificate
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in sharpest_certificate
        and "current bank still does **not** realize even the first `4`-packet layer" in sharpest_certificate
        and "support-side first" in sharpest_certificate,
    )

    four_packet_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md")
    check(
        "Step-2 Wilson four-packet minimality note records that the Hermitian off-diagonal sharpest support route is dimensionally minimal at four real channels, so no honest three-channel generic shortcut exists on that lane",
        "`dim_R V_off = 4`" in four_packet_min
        and "If `m < 4`, then `L` cannot be injective." in four_packet_min
        and "exact minimal finite number of real Hermitian Wilson source" in four_packet_min
        and "is `4`" in four_packet_min
        and "three or fewer generic channels" in four_packet_min,
    )

    two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md")
    check(
        "Step-2 Wilson two-edge chain-reduction note records the physical-lattice reading of the sharpest Wilson support target: one adjacent directed nearest-neighbor two-edge chain, with reversals, diagonals, and the long corner all downstream",
        "adjacent directed two-edge chain" in two_edge
        and "the lattice is treated as physical" in two_edge
        and "reverse edges are adjoints" in two_edge
        and "diagonal support data are products" in two_edge
        and "the long corner is the chain product" in two_edge
        and "current bank still does **not** realize even this physical adjacent" in two_edge,
    )

    two_edge_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md")
    check(
        "Step-2 Wilson two-edge chain minimality note records that the physical-lattice Wilson support route is dimensionally minimal at one adjacent directed two-edge chain, so no honest one-edge generic shortcut exists on that lane",
        "`dim_C V_edge = 2`" in two_edge_min
        and "If `m < 2`, then `L` cannot be injective." in two_edge_min
        and "exact minimal finite number of complex directed edge channels" in two_edge_min
        and "is `2`" in two_edge_min
        and "no honest physical-lattice sharpest-route closure can use one generic directed edge channel" in two_edge_min,
    )

    physical_sharpest = read("docs/PERRON_FROBENIUS_STEP2_WILSON_PHYSICAL_SHARPEST_CERTIFICATE_TARGET_NOTE_2026-04-18.md")
    check(
        "Step-2 Wilson physical sharpest-certificate target note records that the whole compressed Wilson route now has the physical local form one adjacent two-edge chain plus only the 3 scalar spectral identities, with the current bank still failing already at the local support layer",
        "whole Wilson compressed route is now equivalent to one local physical" in physical_sharpest
        and "`2-edge + 3` certificate" in physical_sharpest
        and "adjacent directed nearest-neighbor two-edge chain" in physical_sharpest
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in physical_sharpest
        and "first local two-edge" in physical_sharpest
        and "does **not** realize" in physical_sharpest,
    )

    local_two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_TWO_EDGE_SOURCE_TARGET_NOTE_2026-04-18.md")
    check(
        "Step-2 Wilson local two-edge source-target note records that the remaining compressed-route constructive primitive is no longer an abstract charged source family but one local adjacent two-edge Wilson source law on the physical lattice, while the current bank still does not realize even that sharper local source law",
        "longer best read as an abstract charged source family" in local_two_edge
        and "one local adjacent two-edge Wilson source law" in local_two_edge
        and "physical nearest-neighbor lattice" in local_two_edge
        and "current bank still does **not** realize even this sharper local source" in local_two_edge
        and "a positive Wilson-to-`dW_e^H` theorem" in local_two_edge,
    )

    local_four_source = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md")
    check(
        "Step-2 Wilson local Hermitian four-source reduction note records that the remaining local Wilson primitive is already equivalent to one local Hermitian nearest-neighbor 4-source packet, with the current bank still failing even that sharper packet",
        "local Hermitian nearest-neighbor `4`-source packet" in local_four_source
        and "`E_12 = (X_12 + i Y_12)/2`" in local_four_source
        and "`E_23 = (X_23 + i Y_23)/2`" in local_four_source
        and "current bank still does **not** realize even this sharper local" in local_four_source
        and "a positive Wilson-to-`dW_e^H` theorem" in local_four_source,
    )

    local_hermitian_cert = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_SHARPEST_CERTIFICATE_NOTE_2026-04-18.md")
    check(
        "Step-2 Wilson local Hermitian sharpest-certificate note records that the whole Wilson compressed route now has the local Hermitian 4+3 form: one nearest-neighbor 4-source packet plus only the 3 scalar spectral identities, with the current bank still failing already at the first local Hermitian layer",
        "local Hermitian `4 + 3` certificate" in local_hermitian_cert
        and "local Hermitian nearest-neighbor `4`-source packet" in local_hermitian_cert
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in local_hermitian_cert
        and "current bank still does **not** realize the local Hermitian" in local_hermitian_cert
        and "a positive Wilson-to-`dW_e^H` theorem" in local_hermitian_cert,
    )

    pmns_native_exhaust = read("docs/PMNS_SOLE_AXIOM_NATIVE_CURRENT_ROUTE_EXHAUSTION_NOTE_2026-04-17.md")
    check(
        "PMNS sole-axiom native-current route-exhaustion note records that no overlooked exact PMNS-native route to nonzero J_chi remains on the current bank and that the next honest PMNS-native target is now a sharper fixed-slice current-image collapse law",
        "no overlooked exact PMNS-native route on the current" in pmns_native_exhaust
        and "nearest native dynamical positives" in pmns_native_exhaust
        and "point-blind" in pmns_native_exhaust
        and "graph-first current-image collapse law" in pmns_native_exhaust
        and "fixed-slice nontrivial-current" in pmns_native_exhaust
        and "selector bundle" in pmns_native_exhaust,
    )

    pmns_fixed_slice_noncollapse = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_SELECTOR_HOLONOMY_NONCOLLAPSE_NOTE_2026-04-17.md")
    check(
        "PMNS graph-first fixed-slice selector/holonomy noncollapse note records that fixing w, the selector bundle (tau, q), and one exact native twisted-flux holonomy still does not collapse chi",
        "same exact selector bundle `(tau, q)`" in pmns_fixed_slice_noncollapse
        and "same exact one-angle twisted-flux holonomy" in pmns_fixed_slice_noncollapse
        and "distinct nonzero currents `chi != chi'`" in pmns_fixed_slice_noncollapse
        and "fixed-slice current-image collapse law **beyond**" in pmns_fixed_slice_noncollapse,
    )

    pmns_two_holonomy = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md")
    check(
        "PMNS graph-first fixed-slice two-holonomy collapse note records that fixed w plus any two independent native holonomies reconstruct chi exactly on the readout side, while leaving the nonzero-J_chi production problem open",
        "two independent native holonomies collapse the fixed slice exactly" in pmns_two_holonomy
        and ("chi = u + i v is recovered exactly" in pmns_two_holonomy
             or "recover `chi` exactly" in pmns_two_holonomy
             or "recover `chi` exactly." in pmns_two_holonomy)
        and ("remaining PMNS-native blocker is no longer fixed-slice readout" in pmns_two_holonomy
             or "remaining PMNS-native blocker is no longer fixed-slice readout." in pmns_two_holonomy)
        and ("actually produces nonzero `J_chi = chi`" in pmns_two_holonomy
             or "that actually produces nonzero `J_chi = chi`" in pmns_two_holonomy),
    )

    pmns_two_holonomy_production = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md")
    check(
        "PMNS graph-first fixed-slice two-holonomy production-boundary note records that after fixed-slice readout closure the remaining native blocker is exactly a nontrivial fixed-slice holonomy-pair source law, equivalently nonzero chi",
        "nontrivial fixed-slice native holonomy" in pmns_two_holonomy_production
        and "equivalently nonzero `chi = J_chi`" in pmns_two_holonomy_production
        and (
            "current bank still does **not** realize that source law" in pmns_two_holonomy_production
            or "current exact PMNS-native bank still does **not** supply this" in pmns_two_holonomy_production
            or "no such sole-axiom source law is yet present" in pmns_two_holonomy_production
        ),
    )

    route_audit = read("docs/PERRON_FROBENIUS_REMAINING_PATHS_ROUTE_AUDIT_NOTE_2026-04-17.md")
    check(
        "Remaining-paths route-audit note records that the PMNS strong and compressed routes now both reduce to one Wilson-side charged construction, with the compressed dW_e^H route the cleaner first target",
        "one common upstream need" in route_audit
        and "Wilson-side charged embedding / source-family object" in route_audit
        and "compressed route is therefore the cleaner first target" in route_audit
        and "smallest live `D_-`-level target" in route_audit,
    )
    check(
        "Remaining-paths route-audit note records that the plaquette beta=6 lane is now a compressed class-sector operator-evaluation problem, with the rim side further advanced than the bulk side and no overlooked stronger repo-wide no-go replacing explicit class-sector evaluation",
        "compressed class-sector level" in route_audit
        and "`S_6^env = P_cls K_6^env P_cls`" in route_audit
        and "`eta_6(W) = P_cls B_6(W)`" in route_audit
        and "rim side is already further advanced than the bulk side" in route_audit
        and "strongest current negatives are downstream only" in route_audit
        and "no overlooked stronger repo-wide no-go replaces the need" in route_audit,
    )

    active_five_target = read("docs/PERRON_FROBENIUS_STEP2_ACTIVE_FIVE_REAL_TARGET_NOTE_2026-04-17.md")
    check(
        "Step-2 active five-real target note records that on the strong PMNS-native route the smallest live D_-level step-2A target is exactly the active off-seed five-real packet, while the compressed route already factors further",
        "smallest live" in active_five_target and "`D_-`-level microscopic target" in active_five_target
        and "active off-seed `5`-real source" in active_five_target
        and "compressed route already reduces further" in active_five_target
        and "larger `D_-`-side unknowns are no longer honest live targets" in active_five_target,
    )

    active_five_nonreal = read("docs/PERRON_FROBENIUS_STEP2_ACTIVE_FIVE_REAL_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    check(
        "Step-2 active five-real current-bank nonrealization note records that the current exact bank still does not determine that off-seed packet, so the PMNS-side current-producing obstruction is pinned to one exact packet",
        "still does **not** realize the active off-seed" in active_five_nonreal
        and "next missing construction is one exact packet, not a family" in active_five_nonreal
        and "missing global PF closure" in active_five_nonreal
        and "vague provenance rhetoric" in active_five_nonreal,
    )

    propagated_triple = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_TARGET_NOTE_2026-04-17.md")
    check(
        "First propagated retained-triple target note records that the next honest plaquette evaluator target is the propagated three-sample triple rather than the full infinite class-sector matrix",
        "The first honest next evaluative target is:" in propagated_triple
        and "the propagated retained three-sample output" in propagated_triple
        and "`(Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C))`" in propagated_triple
        and "full infinite class-sector matrix of `S_6^env`" in propagated_triple
        and "full family `W -> eta_6(W)`" in propagated_triple,
    )

    identity_rim = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Plaquette beta=6 identity-rim reduction note records that explicit class-sector beta=6 closure depends on bulk data plus the identity rim datum eta_6(e), while generic W-dependence is already downstream through K(W)",
        "`eta_6(e) = P_cls B_6(e)`" in identity_rim
        and ("bulk matrix elements" in identity_rim
             or "compressed bulk matrix elements" in identity_rim)
        and ("generic marked-holonomy dependence is already downstream through `K(W)`" in identity_rim
             or "generic marked-holonomy dependence is already carried by the universal" in identity_rim)
        and ("not the full generic `W -> B_6(W)` family" in identity_rim
             or "not the full `W`-family of rim lifts" in identity_rim),
    )

    compressed_rim = read("docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md")
    check(
        "Plaquette compressed rim-evaluation theorem note records that after compression the boundary class function is exactly Z_beta^env(W)=<K(W), v_beta>, so the compressed W-dependence is explicit and only the beta-dependent coefficient vector remains unknown",
        "`Z_beta^env(W) = <K(W), v_beta>`" in compressed_rim
        and "`K(W)`" in compressed_rim
        and "the `W`-dependence is already explicit" in compressed_rim
        and "remaining unknown is only the beta-dependent vector `v_beta`" in compressed_rim,
    )

    cyclic_bulk = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Plaquette beta=6 identity-rim cyclic-bulk reduction note records that the live upstream bulk object is only the eta_6(e)-cyclic compression of S_6^env, and that even fixed identity rim plus fixed propagated triple still does not determine that reduced cyclic object",
        "live upstream bulk object is" in cyclic_bulk
        and "`eta_6(e)`-cyclic compression of `S_6^env`" in cyclic_bulk
        and "same fixed identity rim state `eta`" in cyclic_bulk
        and "same exact propagated retained triple" in cyclic_bulk
        and "does **not** determine the reduced cyclic bulk" in cyclic_bulk,
    )

    finite_krylov = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_KRYLOV_BULK_REDUCTION_NOTE_2026-04-17.md")
    check(
        "Plaquette beta=6 identity-rim finite-Krylov bulk reduction note records that at fixed depth the live bulk target is only the eta_6(e)-generated finite Krylov block, and that even the propagated triple still does not determine its first nontrivial block",
        "finite Krylov space" in finite_krylov
        and "the sharp fixed-depth bulk target" in finite_krylov
        and "same exact propagated retained triple" in finite_krylov
        and "different first `2 x 2` Krylov/Lanczos bulk blocks" in finite_krylov,
    )


def part2_sector_local_witnesses() -> None:
    print()
    print("=" * 88)
    print("PART 2: SECTOR-LOCAL POSITIVITY / DOMINANT-MODE WITNESSES")
    print("=" * 88)

    # Plaquette-like positive self-adjoint transfer witness.
    t_plaq = np.array(
        [
            [1.20, 0.35, 0.22],
            [0.35, 1.05, 0.28],
            [0.22, 0.28, 0.94],
        ],
        dtype=float,
    )
    lam0, psi0, evals = leading_mode(t_plaq)
    gap = lam0 - float(evals[1])
    check(
        "Strictly positive self-adjoint transfer witness has a simple dominant eigenvalue",
        gap > 1e-8,
        f"gap={gap:.6f}",
    )
    check(
        "Perron vector of the positive transfer witness is strictly positive",
        float(np.min(psi0)) > 0.0,
        f"positivity floor={np.min(psi0):.6f}",
    )

    # PMNS aligned transfer witness: T_seed = x I + y (C + C^2).
    xbar = 0.73
    ybar = 0.11
    cycle = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
        ]
    )
    t_seed = xbar * np.eye(3) + ybar * (cycle + cycle @ cycle)
    lam_seed, psi_seed, evals_seed = leading_mode(t_seed)
    expected = np.array([xbar + 2.0 * ybar, xbar - ybar, xbar - ybar])
    check(
        "Circulant PMNS transfer witness has eigenvalues (x+2y, x-y, x-y)",
        np.max(np.abs(evals_seed - expected)) < 1e-12,
        f"evals={np.round(evals_seed, 12)}",
    )
    symmetric_mode = np.ones(3) / math.sqrt(3.0)
    check(
        "PMNS transfer witness has a unique symmetric dominant mode",
        abs(lam_seed - evals_seed[0]) < 1e-12
        and np.linalg.norm(np.abs(psi_seed) - symmetric_mode) < 1e-10,
        f"mode={np.round(np.abs(psi_seed), 12)}",
    )
    x_rec = (evals_seed[0] + 2.0 * evals_seed[1]) / 3.0
    y_rec = (evals_seed[0] - evals_seed[1]) / 3.0
    check(
        "Dominant and orthogonal PMNS modes reconstruct the aligned seed pair",
        abs(x_rec - xbar) < 1e-12 and abs(y_rec - ybar) < 1e-12,
        f"(x_rec,y_rec)=({x_rec:.6f},{y_rec:.6f})",
    )

    # Strong-CP positivity witness.
    q_vals = np.arange(-2, 3)
    z_q = np.array([0.40, 0.95, 1.80, 0.95, 0.40], dtype=float)
    thetas = np.linspace(-math.pi, math.pi, 721)
    z_theta = np.array([abs(np.sum(z_q * np.exp(1j * theta * q_vals))) for theta in thetas])
    theta_max = float(thetas[int(np.argmax(z_theta))])
    check(
        "Positive sector weights satisfy |Z(theta)| <= Z(0) on a sampled family",
        float(np.max(z_theta)) <= float(np.sum(z_q)) + 1e-12,
        f"max|Z|={np.max(z_theta):.6f}, Z(0)={np.sum(z_q):.6f}",
    )
    check(
        "The sampled positive-weight family is maximized at theta = 0",
        abs(theta_max) < 1e-2,
        f"theta_max={theta_max:.6f}",
    )


def part3_cross_sector_boundary() -> None:
    print()
    print("=" * 88)
    print("PART 3: WHY THE CURRENT STACK IS NOT YET A GLOBAL PF SELECTOR")
    print("=" * 88)

    # Plaquette-like underdetermination witness:
    # same explicit J, same local factor, different admissible residual operators.
    j_op = np.array(
        [
            [0.20, 0.80, 0.35],
            [0.80, -0.10, 0.55],
            [0.35, 0.55, 0.30],
        ],
        dtype=float,
    )
    m_fac = np.array(
        [
            [2.00, 0.60, 0.25],
            [0.60, 1.70, 0.40],
            [0.25, 0.40, 1.55],
        ],
        dtype=float,
    )
    d_loc = np.diag([1.00, 1.35, 1.80])
    r_a = np.diag([1.00, 1.10, 1.90])
    r_b = np.diag([1.80, 1.10, 1.00])
    t_a = m_fac @ d_loc @ r_a @ m_fac
    t_b = m_fac @ d_loc @ r_b @ m_fac

    lam_a, psi_a, evals_a = leading_mode(t_a)
    lam_b, psi_b, evals_b = leading_mode(t_b)
    exp_a = float(psi_a @ j_op @ psi_a)
    exp_b = float(psi_b @ j_op @ psi_b)
    check(
        "Two admissible positive factorized operators each have a unique strictly positive Perron state",
        (lam_a - float(evals_a[1]) > 1e-8)
        and (lam_b - float(evals_b[1]) > 1e-8)
        and float(np.min(psi_a)) > 0.0
        and float(np.min(psi_b)) > 0.0,
        f"floors=({np.min(psi_a):.6f},{np.min(psi_b):.6f})",
    )
    check(
        "Different residual operators can change the Perron expectation of the same source operator J",
        abs(exp_a - exp_b) > 1e-4,
        f"<J>_A={exp_a:.6f}, <J>_B={exp_b:.6f}",
    )

    support(
        "Current-stack reading",
        "sector-local PF selection is exact once a positive operator is explicit, and the Wilson surface now has a parent/compression theorem, but the PMNS-side projection theorem is still missing",
    )
    support(
        "PMNS boundary",
        "the aligned dominant-mode law is positive and exact, while the strongest sole-axiom hw=1 source/transfer pack still collapses to the trivial identity family",
    )
    support(
        "PMNS projection boundary",
        "the current stack still lacks a canonical projection theorem carrying the Wilson parent structure into the PMNS aligned transfer surface",
    )
    support(
        "All-paths attack order",
        "the lane is now explicitly split into step-1 strengthening, step-2A Hermitian descendant, step-2B non-Hermitian current, plaquette operator-sidecar closure, and only then step-3 compatibility",
    )
    support(
        "Remaining-path convergence",
        "the strong and compressed PMNS-side routes now both point back to one genuinely new Wilson-side charged embedding/source-family, best first aimed at the compressed dW_e^H codomain, while the plaquette beta=6 lane is now best read at the compressed class-sector operator level S_6^env / eta_6 with the rim side further advanced than the bulk side",
    )
    support(
        "Compressed finite target",
        "the compressed PMNS-side primitive is now sharper than a generic source-family placeholder: because dW_e^H reconstructs H_e from nine Hermitian-basis responses, the minimal constructive Wilson-side target may already be posed as a finite nine-channel charged Hermitian response family on E_e",
    )
    support(
        "Compressed strongest live candidate",
        "the strongest live positive compressed-route class is now sharper still: a rank-3 Wilson-side charged embedding/compression together with the induced embedded nine-probe Hermitian response family, with scalar-only, support-only, and hidden-current-bank classes already dead",
    )
    support(
        "Compressed explicit-response sharpening",
        "the strongest live compressed-route class is now formula-level explicit too: for embedded probes J_a(t) = t I_e B_a I_e^*, the nine Wilson first variations reconstruct the Hermitian compression H_e^(cand) = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2, so the exact positive target is to prove d/dt W[t I_e X I_e^*]|_(t=0) = Re Tr(X H_e) on Herm(3), while the current bank still does not instantiate even that sharpened class",
    )
    support(
        "PMNS fixed-slice sharpening",
        "the PMNS-native sole-axiom lane is sharper negatively too: even after fixing w, the selector bundle (tau, q), and one exact native twisted-flux holonomy, the current bank still realizes distinct nonzero chi, so the next honest native target is a genuinely new fixed-slice current-image collapse law beyond the current selector/holonomy bank",
    )
    support(
        "Compressed resolvent-compression sharpening",
        "the explicit-response family now sharpens one level further: its full family form and its nine basis probes are only the coordinate presentation of one operator identity, namely H_e^(cand) = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e, so the strongest honest next compressed-route theorem surface is exactly that Hermitian resolvent-compression identity",
    )
    support(
        "Compressed matrix-source sharpening",
        "the Wilson primitive now sharpens one level further too: theorem-grade I_e / P_e is exactly equivalent to theorem-grade realization of a rank-3 Wilson matrix-source embedding Phi_e : Mat_3(C) -> End(H_W) with Phi_e(X) = I_e X I_e^* and Phi_e(1_3) = P_e, so the strongest honest next compressed-route Wilson object is that invariant source-algebra realization class together with the same Hermitian resolvent-compression identity",
    )
    support(
        "Compressed minimal channel count",
        "the finite Wilson compressed-route target is now dimensionally sharp too: nine real response channels are not just sufficient but minimal for arbitrary Herm(3) data, so eight or fewer generic channels cannot close the compressed route without extra structure",
    )
    support(
        "Compressed Hermitian source-plane sharpening",
        "the Wilson compressed theorem now has a weaker exact source-side target too: full matrix-source embedding Phi_e is still a clean sufficient invariant package, but the response theorem itself only uses the Hermitian restriction Psi_e : Herm(3) -> Herm(H_W), whose image is the nine-dimensional Wilson Hermitian source plane carrying the minimal finite response family; and the current bank still does not instantiate even that weaker object",
    )
    support(
        "Compressed Wilson block-law sharpening",
        "the Wilson compressed route is cleaner still: theorem-grade Phi_e together with H_e^(cand) = H_e is exactly equivalent to one invariant rank-3 Wilson compressed-resolvent block law P_e S_W P_e |_(Ran(P_e)) ~= H_e, so the live positive Wilson target is now best read as a single projector-compression theorem rather than separate source-embedding and response identities",
    )
    support(
        "Compressed Wilson spectral reduction",
        "once a rank-3 Wilson support projector exists, the remaining Wilson verification target is smaller still: the compressed Hermitian block need only match H_e through the three scalar spectral identities Tr(B_e^k)=Tr(H_e^k) for k=1,2,3, rather than by a full coordinate-level 3x3 matrix comparison",
    )
    support(
        "Compressed Wilson finite packet reduction",
        "the Wilson support problem is sharper still before that stage: theorem-grade support realization is exactly equivalent to one finite 9-element Hermitian Wilson source packet whose reconstructed matrix units satisfy the explicit matrix-unit table, so the live Wilson construction problem is already a finite packet-and-identities problem rather than an abstract embedding search",
    )
    support(
        "Compressed Wilson finite certificate",
        "the whole Wilson compressed route is now finite end-to-end: first a 9-element Hermitian support packet realizing the rank-3 Wilson support, then only the 3 scalar spectral identities Tr(B_e^k)=Tr(H_e^k) for k=1,2,3; and the current bank still fails on the first support-side layer rather than on the later spectral packet",
    )
    support(
        "Compressed Wilson seven-packet chain reduction",
        "the Wilson support target is sharper still below the 9-packet layer: the long (1,3) corner is already downstream of nearest-neighbor chain data, so theorem-grade support realization is already equivalent to a smaller 7-element nearest-neighbor Hermitian source packet plus finite chain identities, and the current bank still fails even at that sharper support layer",
    )
    support(
        "Compressed Wilson sharp finite certificate",
        "the whole Wilson compressed route is now sharper end-to-end too: not 9+3 but one 7+3 certificate, namely a nearest-neighbor 7-packet support layer followed by only the 3 scalar spectral identities Tr(B_e^k)=Tr(H_e^k), and the current bank still fails already at the first support-side layer",
    )
    support(
        "Compressed Wilson four-packet reduction",
        "the Wilson support target is sharper still below the 7-packet layer: the diagonal support data are already downstream of the off-diagonal nearest-neighbor chain, so theorem-grade support realization is already equivalent to one Hermitian off-diagonal 4-packet plus finite chain identities, and the current bank still fails even at that sharper support layer",
    )
    support(
        "Compressed Wilson sharpest finite certificate",
        "the whole Wilson compressed route is now sharpest end-to-end too: not 7+3 but one 4+3 certificate, namely an off-diagonal Hermitian 4-packet support layer followed by only the 3 scalar spectral identities Tr(B_e^k)=Tr(H_e^k), and the current bank still fails already at the first support-side layer",
    )
    support(
        "Compressed Wilson four-packet minimality",
        "that sharpest 4-packet support layer is now known to be dimensionally minimal on the Hermitian Wilson lane too: the off-diagonal nearest-neighbor source space has real dimension 4, so no honest generic 3-channel shortcut can determine arbitrary sharpest-route support data",
    )
    support(
        "Compressed Wilson physical two-edge chain",
        "because the lattice is physical, the sharpest Wilson support target now has the right local reading too: it is one adjacent directed nearest-neighbor two-edge chain, with reverse edges, diagonal support data, and the long corner all downstream of that local chain",
    )
    support(
        "Compressed Wilson physical two-edge minimality",
        "that physical local reading is now minimal too: the sharpest Wilson support lane lives on a two-dimensional complex edge-source space, so no honest generic one-edge shortcut can determine arbitrary physical two-edge chain data",
    )
    support(
        "Compressed Wilson physical sharpest certificate",
        "the whole Wilson compressed route now has the right local physical form end-to-end: one adjacent directed nearest-neighbor two-edge chain on the lattice, then only the 3 scalar spectral identities Tr(B_e^k)=Tr(H_e^k) for k=1,2,3",
    )
    support(
        "Compressed Wilson local two-edge source target",
        "the remaining positive Wilson primitive is now sharper than an abstract charged source family: it is one local adjacent two-edge Wilson source law on the physical nearest-neighbor lattice, and the current bank still does not instantiate even that local source layer",
    )
    support(
        "Compressed Wilson local Hermitian four-source reduction",
        "the remaining local Wilson primitive is now sharper still than the two-edge source law: it is exactly one local Hermitian nearest-neighbor 4-source packet, obtained by taking the Hermitian and skew-Hermitian edge combinations on the adjacent two-edge chain, and the current bank still does not instantiate even that packet",
    )
    support(
        "Compressed Wilson local Hermitian sharpest certificate",
        "the whole Wilson compressed route now has a matching local Hermitian constructive package too: one nearest-neighbor Hermitian 4-source packet on the physical lattice, then only the 3 scalar spectral identities Tr(B_e^k)=Tr(H_e^k) for k=1,2,3",
    )
    support(
        "PMNS fixed-slice readout closure",
        "the PMNS-native fixed-slice frontier is now closed on the readout side: once w is fixed, any two independent native holonomies reconstruct chi exactly, so the remaining native blocker is no longer collapse/readout but a sole-axiom law that actually produces nonzero J_chi",
    )
    support(
        "PMNS fixed-slice production reduction",
        "the PMNS-native production seam is now sharper still: after fixed-slice readout closure, producing nonzero J_chi is exactly equivalent to producing a nontrivial fixed-slice native holonomy pair, and the current bank still does not realize that source law",
    )
    support(
        "PMNS active five-real packet target",
        "on the strong PMNS-native microscopic lane the remaining current-producing content is now sharper than a generic source family: it is exactly the active off-seed five-real packet beyond the already fixed seed pair, while the compressed route already factors to a smaller charged projected-source law",
    )
    support(
        "PMNS active five-real packet nonrealization",
        "the current bank still does not determine that active off-seed five-real packet, so the sharpest exact PMNS-native strong-lane obstruction is now one unresolved packet rather than a diffuse family of microscopic unknowns",
    )
    support(
        "PMNS-native exhaustion",
        "the PMNS-native sole-axiom lane is now exhausted more sharply too: there is no overlooked exact native route to nonzero J_chi on the current bank, one-angle selector/holonomy data still do not collapse chi, and the remaining honest target is production of nonzero chi rather than another fixed-slice route scan",
    )
    support(
        "Plaquette finite target",
        "the plaquette beta=6 operator lane is now sharper than a generic class-sector evaluation prompt too: the first honest next evaluative target is the propagated retained three-sample triple (Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C)), equivalently the first retained propagated coefficient triple of v_6",
    )
    support(
        "Plaquette identity-rim reduction",
        "the plaquette operator-side seam is sharper in structure too: explicit class-sector beta=6 closure depends on the bulk class-sector data together with the identity rim datum eta_6(e) = P_cls B_6(e), while generic marked-holonomy dependence is already downstream through the universal evaluation functional K(W)",
    )
    support(
        "Plaquette compressed rim evaluation",
        "the plaquette rim side is sharper too: after compression to the marked class sector the boundary law is already explicit as Z_beta^env(W) = <K(W), v_beta>, so generic W-dependence is fully canonical there and the remaining compressed unknown is only the beta-dependent coefficient vector v_beta",
    )
    support(
        "Plaquette cyclic-bulk reduction",
        "the plaquette bulk seam is sharper still: the live upstream operator object is not the whole compressed bulk operator S_6^env but only its eta_6(e)-cyclic compression, equivalently the cyclic spectral measure / Jacobi data seen from the identity rim state, and even fixed eta_6(e) together with the exact propagated retained triple still does not determine that reduced cyclic object on the current bank",
    )
    support(
        "Plaquette finite-Krylov bulk reduction",
        "at fixed propagation depth the plaquette bulk front is sharper again: not even the whole eta_6(e)-cyclic object is the honest target, only the finite eta_6(e)-generated Krylov block matters; but the current propagated retained triple still does not determine even its first nontrivial 2 x 2 Krylov/Lanczos block",
    )
    support(
        "Plaquette evaluator boundary",
        "the exact local Wilson three-sample block is already explicit and already fails the first retained positive cone, no tau < 0.701560040093... local-Wilson first-seam repair exists, the actual three-sample route already factors through one fixed left operator acting on one still-underdetermined beta-side vector, even fixed Z_hat_6(e) plus fixed Tau_(>1) still leaves an affine retained fiber, even fixed (rho_(1,0), rho_(1,1), Tau_(>1)) still leaves higher-orbit noncollapse of the propagated triple, and no finite marked-holonomy sample packet can by itself determine the full beta-side vector, so the current stack still does not furnish an actual evaluator for Z_6^env(W_i)",
    )
    support(
        "Plaquette target-self nonclosure",
        "the plaquette operator-side frontier is sharper again: even exact evaluation of the minimal propagated retained triple itself would still not determine the full beta-side vector or the unresolved beta=6 operator data, because already on an explicit four-orbit higher slice the propagated-triple map has nontrivial kernel and supports distinct nonnegative higher-orbit coefficient stacks with the same exact propagated triple",
    )


def main() -> int:
    print("=" * 88)
    print("PERRON-FROBENIUS SELECTION AXIOM BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the current exact stack already yield one common sole-axiom")
    print("  Perron-Frobenius selector across the retained sectors?")

    part1_reference_surface()
    part2_sector_local_witnesses()
    part3_cross_sector_boundary()

    print()
    print("=" * 88)
    print("VERDICT")
    print("=" * 88)
    print()
    print("  - Plaquette sector: yes, exact PF reduction once the transfer operator is fixed.")
    print("  - Strong-CP sector: yes, positivity already selects theta = 0 on the retained surface.")
    print("  - Wilson gauge surface: yes, one parent object with canonical plaquette/theta descendants.")
    print("  - PMNS aligned transfer sector: yes, exact dominant-mode law on the aligned seed patch.")
    print("  - Global sole-axiom PF selector across sectors: current stack closed negatively; not derivable yet.")
    print("  - Step 1 status: partial only; exact on the Wilson surface, not yet a global parent/intertwiner theorem.")
    print("  - Step 2 status: the actual bottleneck; Wilson-side descendants and internal PMNS support laws exist, but no Wilson-to-PMNS descendant theorem.")
    print("    Step 2 now splits cleanly into:")
    print("      (a) Wilson-to-Hermitian descendant data through the charged-sector chain D_- -> dW_e^H -> H,")
    print("      (b) residual Wilson-to-J_chi current if the Hermitian target still leaves a PMNS last mile.")
    print("    The strong and compressed PMNS-side routes now both point back to one genuinely new Wilson-side charged embedding/source-family,")
    print("      with the compressed Wilson -> dW_e^H codomain the cleaner first target and the strong Wilson -> D_- packet best read as an optional lift only if needed afterward.")
    print("    More sharply, the compressed primitive may already be posed as a finite nine-channel charged Hermitian response family on E_e,")
    print("      because dW_e^H reconstructs H_e from nine real Hermitian-basis responses once the Wilson-side charged realization exists.")
    print("      Nine real channels are now known to be the exact minimal finite count for arbitrary Herm(3) data,")
    print("      so eight or fewer generic channels cannot close the compressed route without additional structure.")
    print("    Strongest live positive compressed-route candidate is now sharper still:")
    print("      a rank-3 Wilson-side charged embedding/compression together with the induced embedded nine-probe Hermitian response family,")
    print("      while scalar-only, support-only, and hidden-current-bank classes are already dead.")
    print("    More sharply still, that class now has an explicit formula-level target:")
    print("      for J_a(t) = t I_e B_a I_e^*, the nine Wilson first variations should reconstruct")
    print("      H_e^(cand) = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2, equivalently")
    print("      d/dt W[t I_e X I_e^*]|_(t=0) = Re Tr(X H_e) on Herm(3);")
    print("      and the current bank still does not instantiate even that sharpened explicit-response class.")
    print("    More sharply still again, the whole explicit-response family is only the coordinate form of one operator identity:")
    print("      H_e^(cand) = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e;")
    print("      so the strongest honest next compressed-route theorem surface is now exactly that Hermitian resolvent-compression identity,")
    print("      and the current bank still does not instantiate even that sharper target because theorem-grade I_e / P_e and theorem-grade identification of H_e^(cand) with H_e are both still missing.")
    print("    More sharply still once again, theorem-grade I_e / P_e is itself exactly equivalent to theorem-grade realization")
    print("      of a rank-3 Wilson matrix-source embedding Phi_e : Mat_3(C) -> End(H_W) with Phi_e(X) = I_e X I_e^* and Phi_e(1_3) = P_e;")
    print("      so the strongest honest next compressed-route Wilson object is now that invariant source-algebra realization class,")
    print("      and the current bank still does not instantiate even that sharper invariant form.")
    print("    More sharply still one level lower, the compressed theorem itself only uses the Hermitian restriction")
    print("      Psi_e := Phi_e |_(Herm(3)) : Herm(3) -> Herm(H_W), whose image is the exact nine-dimensional Wilson Hermitian source plane.")
    print("      So full Phi_e remains a clean sufficient invariant package, but the weaker minimal response-side target is already Psi_e,")
    print("      and the current bank still does not instantiate even that weaker Hermitian source embedding.")
    print("    On the PMNS-native sole-axiom side, there is now no overlooked exact route to nonzero J_chi on the current bank,")
    print("      and one-angle selector/holonomy data still do not collapse chi;")
    print("      but fixed w together with any two independent native holonomies now reconstructs chi exactly on the readout side.")
    print("      So the remaining PMNS-native blocker is no longer fixed-slice collapse/readout but a sole-axiom law that actually produces nonzero J_chi = chi,")
    print("      rather than another route scan or another reuse of existing graph-first native invariants.")
    print("  - Step 3 status: downstream only; common-state compatibility is not yet available.")
    print("    Missing pieces remain:")
    print("      (1) nontrivial sole-axiom PMNS source/transfer pack,")
    print("      (2) canonical projection from the Wilson parent object into PMNS,")
    print("      (3) unique plaquette framework-point Perron data after explicit beta=6 evaluation of K_6^env together with the identity rim datum eta_6(e) = P_cls B_6(e),")
    print("          since even one fixed same-surface plaquette value is still only one scalar constraint,")
    print("          the exact local Wilson three-sample block already lies outside the retained positive cone,")
    print("          no tau < 0.701560040093... first-seam repair exists on the local-Wilson route,")
    print("          and the actual three-sample route already factors through one fixed operator acting on one still-underdetermined beta-side vector,")
    print("          while even fixed Z_hat_6(e) together with fixed Tau_(>1) still leaves an affine retained fiber,")
    print("          while no finite marked-holonomy sample packet can by itself determine the full beta-side vector,")
    print("          while the coefficient side is otherwise only controlled by a Tau_(>1)-dependent outer wedge whose current seam constraints still admit arbitrarily large Tau_(>1),")
    print("          and while the live beta=6 operator lane is now best read at the compressed class-sector level S_6^env / eta_6,")
    print("          with generic marked-holonomy dependence already downstream through K(W) once the common beta-side vector is fixed,")
    print("          with the rim side already further advanced than the bulk side and with no overlooked stronger repo-wide no-go replacing explicit nonlocal class-sector evaluation,")
    print("          while the first honest next evaluative target on that plaquette lane is now the propagated retained three-sample triple (Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C)),")
    print("          equivalently the first retained propagated coefficient triple of v_6, rather than the full infinite class-sector matrix,")
    print("          while even exact evaluation of that propagated triple is now known not to close the full operator-side beta=6 object by itself.")
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    print(f"SUPPORT = {SUPPORT}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
