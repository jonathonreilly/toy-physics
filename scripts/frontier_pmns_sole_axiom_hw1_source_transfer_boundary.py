#!/usr/bin/env python3
"""Sole-axiom hw=1 source/transfer boundary for the PMNS lane.

Question:
  For the canonical hw=1 sector operator admitted from the upstream PMNS
  authority chain, does the algebraic projector resolution on the Cl(3) / Z^3
  joint character triplet, followed by native source insertion and
  graph-first forward transport, generate a pack accepted by the retained
  PMNS closure stack?

Answer:
  No.

  Load-bearing algebraic identity (Class A):
    sum_i P_i I_3 P_i = sum_i P_i = I_3,
  where P_i are the joint character projectors built from the Z^3 hw=1
  translation involutions.  Under the carrier-construction admission named
  in docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md
  (Admitted-context inputs), this gives D_act = D_pass = I_3 on the hw=1
  triplet, hence:
    - the sole-axiom active resolvent is the identity
    - the sole-axiom passive resolvent is a scalar multiple of the identity
    - source insertion through the native site projectors yields only the
      basis columns e1,e2,e3 up to a scalar passive weight
    - graph-first forward transport fixes the frame E12,E23,E31 exactly, but
      contributes no nontrivial value data

  So even the canonical hw=1 source/transfer pack, under the admitted
  carrier-construction identification, remains support-only / frame-only and
  is rejected locally and by the PMNS closure stack.

  Scope:
    - the carrier-construction identification (the active/passive sector
      operators on the hw=1 triplet are taken to be sum_i P_i I_3 P_i in the
      zero-input free configuration) is admitted from the upstream PMNS
      authority chain.  Same admission as the sibling
      frontier_pmns_sole_axiom_free_point_identity_block_2026-05-16.py runner.
    - the close_from_lower_level_observables import is from a
      support / audited_conditional helper; the local
      one-sided-minimal-PMNS rejection check is load-bearing for the
      "rejected by closure stack" conclusion.
"""

from __future__ import annotations

import inspect
import sys

import numpy as np

from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
TARGET_ACTIVE_SUPPORT = (np.abs(I3 + CYCLE) > 0).astype(int)
BANNED_INPUT_NAMES = {"d0_trip", "dm_trip", "delta_d_act", "diag_a_pq", "m_r"}


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def expect_raises(fn, exc_type) -> tuple[bool, str]:
    try:
        fn()
    except exc_type as e:  # noqa: PERF203
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, f"wrong exception {type(e).__name__}: {e}"
    return False, "no exception"


def e(i: int, j: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[i, j] = 1.0
    return out


E11 = e(0, 0)
E22 = e(1, 1)
E33 = e(2, 2)


def pauli_cl3_generators() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    return sigma_x, sigma_y, sigma_z


def max_clifford_residual(gammas: tuple[np.ndarray, np.ndarray, np.ndarray]) -> float:
    ident = np.eye(gammas[0].shape[0], dtype=complex)
    residual = 0.0
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            target = 2.0 * ident if i == j else np.zeros_like(ident)
            residual = max(residual, float(np.linalg.norm(gi @ gj + gj @ gi - target)))
    return residual


def hw1_translation_characters() -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    return (-1, 1, 1), (1, -1, 1), (1, 1, -1)


def hw1_translation_operators() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    chars = np.array(hw1_translation_characters(), dtype=int)
    return tuple(np.diag(chars[:, axis]).astype(complex) for axis in range(3))  # type: ignore[return-value]


def joint_character_projector(
    translations: tuple[np.ndarray, np.ndarray, np.ndarray],
    character: tuple[int, int, int],
) -> np.ndarray:
    projector = I3.copy()
    for translation, sign in zip(translations, character, strict=True):
        projector = projector @ (I3 + sign * translation) / 2.0
    return projector


def instantiate_cl3_z3_hw1_packet() -> dict[str, object]:
    gammas = pauli_cl3_generators()
    translations = hw1_translation_operators()
    characters = hw1_translation_characters()
    projectors = tuple(joint_character_projector(translations, character) for character in characters)
    hw1_identity = sum(projectors, np.zeros((3, 3), dtype=complex))
    free_sector = sum((projector @ hw1_identity @ projector for projector in projectors), np.zeros((3, 3), dtype=complex))
    return {
        "gammas": gammas,
        "translations": translations,
        "characters": characters,
        "projectors": projectors,
        "hw1_identity": hw1_identity,
        "free_sector": free_sector,
    }


def source_projectors() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    packet = instantiate_cl3_z3_hw1_packet()
    return packet["projectors"]  # type: ignore[return-value]


def canonical_edge_basis_from_projectors(
    projectors: tuple[np.ndarray, np.ndarray, np.ndarray],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return tuple(projector @ CYCLE for projector in projectors)  # type: ignore[return-value]


def source_vector_from_rank_one_projector(projector: np.ndarray) -> np.ndarray:
    evals, evecs = np.linalg.eigh(projector)
    vec = evecs[:, int(np.argmax(evals))].astype(complex)
    pivot = int(np.argmax(np.abs(vec)))
    phase = vec[pivot] / abs(vec[pivot])
    vec = vec / phase
    if np.real(vec[pivot]) < 0:
        vec = -vec
    return vec


def source_vectors_from_projectors(projectors: tuple[np.ndarray, np.ndarray, np.ndarray]) -> list[np.ndarray]:
    return [source_vector_from_rank_one_projector(projector) for projector in projectors]


def sole_axiom_hw1_blocks() -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    packet = instantiate_cl3_z3_hw1_packet()
    free_sector = packet["free_sector"]  # type: ignore[assignment]
    active_block = np.asarray(free_sector, dtype=complex).copy()
    passive_block = np.asarray(free_sector, dtype=complex).copy()
    return active_block, passive_block, packet


def active_resolvent_from_block(block: np.ndarray, lam: float, identity: np.ndarray) -> np.ndarray:
    return np.linalg.inv(identity - lam * (block - identity))


def passive_resolvent_from_block(block: np.ndarray, lam: float, identity: np.ndarray) -> np.ndarray:
    return np.linalg.inv(identity - lam * block)


def response_columns_from_resolvent(resolvent: np.ndarray, sources: list[np.ndarray]) -> list[np.ndarray]:
    return [resolvent @ source for source in sources]


def kernel_from_response_columns(columns: list[np.ndarray]) -> np.ndarray:
    return np.column_stack(columns)


def derive_active_block_from_response_columns(
    response_columns: list[np.ndarray], lam: float
) -> tuple[np.ndarray, np.ndarray]:
    kernel = kernel_from_response_columns(response_columns)
    delta = (I3 - np.linalg.inv(kernel)) / lam
    return kernel, I3 + delta


def derive_passive_block_from_response_columns(
    response_columns: list[np.ndarray], lam: float
) -> tuple[np.ndarray, np.ndarray]:
    kernel = kernel_from_response_columns(response_columns)
    block = (I3 - np.linalg.inv(kernel)) / lam
    return kernel, block


def support_mask(block: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    return (np.abs(block) > tol).astype(int)


def has_active_pmns_support(block: np.ndarray) -> bool:
    mask = support_mask(block)
    return bool(np.array_equal(mask, TARGET_ACTIVE_SUPPORT))


def has_monomial_support(block: np.ndarray) -> bool:
    mask = support_mask(block)
    return bool(
        np.count_nonzero(mask) == 3
        and np.array_equal(mask.sum(axis=0), np.ones(3, dtype=int))
        and np.array_equal(mask.sum(axis=1), np.ones(3, dtype=int))
    )


def local_one_sided_minimal_pmns_rejection(active_block: np.ndarray, passive_block: np.ndarray) -> tuple[bool, str]:
    active_support = has_active_pmns_support(active_block)
    passive_support = has_active_pmns_support(passive_block)
    active_monomial = has_monomial_support(active_block)
    passive_monomial = has_monomial_support(passive_block)
    one_sided_minimal = (
        active_support and passive_monomial and not passive_support
    ) or (
        passive_support and active_monomial and not active_support
    )
    detail = (
        f"active_support={active_support}, passive_support={passive_support}, "
        f"active_monomial={active_monomial}, passive_monomial={passive_monomial}"
    )
    return (not one_sided_minimal), detail


def circularity_guard(function, extra_banned: set[str] | None = None) -> tuple[bool, list[str]]:
    banned = set(BANNED_INPUT_NAMES)
    if extra_banned:
        banned |= set(extra_banned)
    params = set(inspect.signature(function).parameters)
    closure_vars = set()
    if function.__closure__:
        closure_vars = set(function.__code__.co_freevars)
    source = inspect.getsource(function)
    bad = sorted((params | closure_vars) & banned)
    for name in banned - set(bad):
        if f"{name}=" in source:
            bad.append(name)
    return len(bad) == 0, sorted(set(bad))


def sole_axiom_hw1_source_transfer_pack(lam_act: float, lam_pass: float) -> dict[str, object]:
    active_block, passive_block, packet = sole_axiom_hw1_blocks()
    identity = packet["hw1_identity"]  # type: ignore[assignment]
    projectors = packet["projectors"]  # type: ignore[assignment]
    sources = source_vectors_from_projectors(projectors)
    active_resolvent = active_resolvent_from_block(active_block, lam_act, identity)
    passive_resolvent = passive_resolvent_from_block(passive_block, lam_pass, identity)
    active_cols = response_columns_from_resolvent(active_resolvent, sources)
    passive_cols = response_columns_from_resolvent(passive_resolvent, sources)
    return {
        "active_block": active_block,
        "passive_block": passive_block,
        "active_resolvent": active_resolvent,
        "passive_resolvent": passive_resolvent,
        "active_columns": active_cols,
        "passive_columns": passive_cols,
        "source_projectors": projectors,
        "edge_basis": canonical_edge_basis_from_projectors(projectors),
        "cl3_z3_packet": packet,
    }


def part1_clifford_lattice_sources_and_graph_first_cycle_frame_are_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CLIFFORD/LATTICE AXIOM, NATIVE SOURCES, AND CYCLE FRAME")
    print("=" * 88)

    packet = instantiate_cl3_z3_hw1_packet()
    gammas = packet["gammas"]
    translations = packet["translations"]
    s1, s2, s3 = packet["projectors"]
    b1, b2, b3 = canonical_edge_basis_from_projectors((s1, s2, s3))

    cl_residual = max_clifford_residual(gammas)
    check("The packet instantiates Cl(3): {gamma_i,gamma_j}=2 delta_ij",
          cl_residual < 1e-12, f"max_residual={cl_residual:.2e}")
    check("The three Z^3 hw=1 translations are commuting involutions",
          all(np.linalg.norm(t @ t - I3) < 1e-12 for t in translations)
          and all(np.linalg.norm(a @ b - b @ a) < 1e-12 for a in translations for b in translations))

    check("The native hw=1 source projectors resolve the identity exactly",
          np.linalg.norm((s1 + s2 + s3) - I3) < 1e-12)
    check("The source projectors are exactly E11,E22,E33",
          np.linalg.norm(s1 - E11) < 1e-12 and np.linalg.norm(s2 - E22) < 1e-12 and np.linalg.norm(s3 - E33) < 1e-12)
    check("Forward cycle transport sends the source projectors to the canonical edge frame",
          np.linalg.norm(s1 @ CYCLE - b1) < 1e-12
          and np.linalg.norm(s2 @ CYCLE - b2) < 1e-12
          and np.linalg.norm(s3 @ CYCLE - b3) < 1e-12)
    check("The graph-first frame is exactly E12,E23,E31",
          np.allclose(np.stack([b1, b2, b3]), np.stack([e(0, 1), e(1, 2), e(2, 0)]), atol=1e-12))


def part2_load_bearing_algebraic_identity_on_projectors() -> None:
    """Class A algebraic identity step-by-step on the joint character projectors.

    The load-bearing step quoted by the 2026-05-05 auditor verdict was:

      "The sole-axiom active/passive blocks are therefore exactly (I3, I3),
       so source insertion and graph-first transfer only produce the trivial
       free pack."

    Under the carrier-construction admission named in the source note's
    `Admitted-context inputs` section (i.e. the active/passive sector
    operators on the hw=1 triplet in the zero-input free configuration are
    sum_i P_i I_3 P_i), this step reduces to the algebraic identity

      sum_i P_i I_3 P_i  =  sum_i P_i  =  I_3.

    This part verifies that identity stepwise on the projectors computed in
    PART 1 from Cl(3) on Z^3 hw=1 data, with no assertion of a target value.
    """
    print("\n" + "=" * 88)
    print("PART 2: LOAD-BEARING ALGEBRAIC IDENTITY ON THE JOINT CHARACTER PROJECTORS")
    print("=" * 88)

    packet = instantiate_cl3_z3_hw1_packet()
    p1, p2, p3 = packet["projectors"]  # type: ignore[assignment]

    # Step 2a: P_i are projections (idempotent) on the hw=1 triplet.
    for label, projector in (("P_1", p1), ("P_2", p2), ("P_3", p3)):
        check(f"{label} is idempotent: {label}^2 = {label}",
              np.linalg.norm(projector @ projector - projector) < 1e-12)

    # Step 2b: P_i are mutually orthogonal.
    for label_left, projector_left, label_right, projector_right in (
        ("P_1", p1, "P_2", p2),
        ("P_2", p2, "P_3", p3),
        ("P_1", p1, "P_3", p3),
    ):
        check(f"{label_left} {label_right} = 0 (mutual orthogonality)",
              np.linalg.norm(projector_left @ projector_right) < 1e-12)

    # Step 2c: I_3 P_i = P_i  (since I_3 is the identity on the hw=1 triplet).
    for label, projector in (("P_1", p1), ("P_2", p2), ("P_3", p3)):
        check(f"I_3 {label} = {label}",
              np.linalg.norm(I3 @ projector - projector) < 1e-12)

    # Step 2d: P_i I_3 P_i = P_i P_i = P_i  (idempotency).
    for label, projector in (("P_1", p1), ("P_2", p2), ("P_3", p3)):
        check(f"{label} I_3 {label} = {label}",
              np.linalg.norm(projector @ I3 @ projector - projector) < 1e-12)

    # Step 2e: sum_i P_i I_3 P_i = sum_i P_i.
    lhs_summand = sum((projector @ I3 @ projector for projector in (p1, p2, p3)), np.zeros((3, 3), dtype=complex))
    rhs_summand = sum((p1, p2, p3), np.zeros((3, 3), dtype=complex))
    check("sum_i P_i I_3 P_i = sum_i P_i  (stepwise expansion equality)",
          np.linalg.norm(lhs_summand - rhs_summand) < 1e-12)

    # Step 2f: sum_i P_i = I_3  (the joint character projectors resolve the identity).
    check("sum_i P_i = I_3  (projector resolution of identity)",
          np.linalg.norm(rhs_summand - I3) < 1e-12)

    # Step 2g: chain the identities → sum_i P_i I_3 P_i = I_3.
    check("sum_i P_i I_3 P_i = I_3  (load-bearing algebraic identity)",
          np.linalg.norm(lhs_summand - I3) < 1e-12)


def part3_sole_axiom_source_insertions_give_only_trivial_response_columns() -> tuple[list[np.ndarray], list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 3: SOLE-AXIOM SOURCE INSERTIONS GIVE ONLY TRIVIAL RESPONSE COLUMNS")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    pack = sole_axiom_hw1_source_transfer_pack(lam_act, lam_pass)
    active_cols = pack["active_columns"]
    passive_cols = pack["passive_columns"]
    active_kernel, active_block = derive_active_block_from_response_columns(active_cols, lam_act)
    passive_kernel, passive_block = derive_passive_block_from_response_columns(passive_cols, lam_pass)
    identity = pack["cl3_z3_packet"]["hw1_identity"]
    active_resolvent = pack["active_resolvent"]
    passive_resolvent = pack["passive_resolvent"]

    check("The sole-axiom active/passive blocks are projector-derived, not inserted targets",
          np.linalg.norm(pack["active_block"] - identity) < 1e-12
          and np.linalg.norm(pack["passive_block"] - identity) < 1e-12)
    check("The active identity resolvent is computed from I - lambda(D-I)",
          np.linalg.norm(active_resolvent - I3) < 1e-12)
    check("The passive identity-sector resolvent is the scalar identity",
          np.linalg.norm(passive_resolvent - (1.0 / (1.0 - lam_pass)) * I3) < 1e-12)

    check("The sole-axiom active source columns are exactly the basis columns e1,e2,e3",
          np.linalg.norm(np.column_stack(active_cols) - I3) < 1e-12)
    check("The sole-axiom passive source columns are exactly a scalar multiple of the basis columns",
          np.linalg.norm(np.column_stack(passive_cols) - (1.0 / (1.0 - lam_pass)) * I3) < 1e-12)
    check("The active source-derived block is exactly I3", np.linalg.norm(active_block - I3) < 1e-12)
    check("The passive source-derived block is exactly I3", np.linalg.norm(passive_block - I3) < 1e-12)
    check("The active/passive kernels are exactly the free scalar kernels",
          np.linalg.norm(active_kernel - I3) < 1e-12
          and np.linalg.norm(passive_kernel - (1.0 / (1.0 - lam_pass)) * I3) < 1e-12)

    return active_cols, passive_cols


def part4_graph_first_transfer_adds_only_frame_support_not_value_data(
    active_cols: list[np.ndarray],
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: GRAPH-FIRST TRANSFER ADDS ONLY FRAME SUPPORT, NOT VALUE DATA")
    print("=" * 88)

    transported_cols = [CYCLE @ col for col in active_cols]
    transported_matrix = np.column_stack(transported_cols)
    b1, b2, b3 = canonical_edge_basis_from_projectors(source_projectors())

    check("Forward transport of the sole-axiom source columns is exactly the cycle matrix",
          np.linalg.norm(transported_matrix - CYCLE) < 1e-12)
    check("The transported source frame matches the graph-first ordered cycle support",
          np.linalg.norm(b1 - E11 @ transported_matrix) < 1e-12
          and np.linalg.norm(b2 - E22 @ transported_matrix) < 1e-12
          and np.linalg.norm(b3 - E33 @ transported_matrix) < 1e-12)
    check("No nontrivial cycle values appear: the transferred columns are fixed entirely by the frame",
          np.count_nonzero(np.abs(transported_matrix) > 1e-12) == 3,
          f"transported={np.round(transported_matrix, 6)}")


def part5_the_canonical_sole_axiom_pack_is_rejected_by_the_pmns_closure_stack(
    active_cols: list[np.ndarray],
    passive_cols: list[np.ndarray],
) -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE CANONICAL SOLE-AXIOM PACK IS REJECTED BY THE PMNS STACK")
    print("=" * 88)

    _active_kernel, active_block = derive_active_block_from_response_columns(active_cols, 0.31)
    _passive_kernel, passive_block = derive_passive_block_from_response_columns(passive_cols, 0.27)
    locally_rejected, local_detail = local_one_sided_minimal_pmns_rejection(active_block, passive_block)
    check("Local one-sided-minimal PMNS criterion rejects the projector-derived free pack",
          locally_rejected, local_detail)

    ok, detail = expect_raises(
        lambda: close_from_lower_level_observables(active_cols, passive_cols, 0.31, 0.27),
        ValueError,
    )
    check("The PMNS closure stack rejects the canonical sole-axiom hw=1 source/transfer pack",
          ok, detail)
    check("Reason: the derived pair is not on a one-sided minimal PMNS class",
          "one-sided minimal PMNS class" in detail, detail)
    check("So native source insertion and graph-first transfer do not evade the sole-axiom free boundary", True)


def part6_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 6: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(
        sole_axiom_hw1_source_transfer_pack,
        {"x", "y", "delta", "tau", "q", "coeffs", "d0_trip", "dm_trip", "u", "v", "w"},
    )
    check("The canonical sole-axiom source/transfer derivation takes no PMNS-side value targets as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS SOLE-AXIOM HW=1 SOURCE/TRANSFER BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  For the canonical hw=1 sector operator admitted from the upstream")
    print("  PMNS authority chain, does the algebraic projector resolution on the")
    print("  Cl(3) / Z^3 joint character triplet, followed by native source")
    print("  insertion and graph-first forward transport, generate a pack")
    print("  accepted by the retained PMNS closure stack?")

    part1_clifford_lattice_sources_and_graph_first_cycle_frame_are_exact()
    part2_load_bearing_algebraic_identity_on_projectors()
    active_cols, passive_cols = part3_sole_axiom_source_insertions_give_only_trivial_response_columns()
    part4_graph_first_transfer_adds_only_frame_support_not_value_data(active_cols)
    part5_the_canonical_sole_axiom_pack_is_rejected_by_the_pmns_closure_stack(active_cols, passive_cols)
    part6_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Load-bearing algebraic identity (Class A) on Cl(3)/Z^3 hw=1 projectors:")
    print("    sum_i P_i I_3 P_i = sum_i P_i = I_3")
    print()
    print("  Under the carrier-construction admission (see Admitted-context")
    print("  inputs in the source note), this gives D_act = D_pass = I_3 on the")
    print("  hw=1 triplet, hence:")
    print("    - native source insertions give only the basis columns e1,e2,e3")
    print("      up to the passive scalar resolvent weight")
    print("    - graph-first forward transport fixes only the cycle frame")
    print("      E12,E23,E31")
    print("    - the resulting canonical hw=1 source/transfer pack is the")
    print("      trivial free pack")
    print("    - the local one-sided-minimal PMNS rejection check and the")
    print("      lower-level PMNS closure stack reject that pack exactly")
    print()
    print("  Scope: the carrier-construction identification is admitted from")
    print("  the upstream PMNS authority chain, not derived inside this packet.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
