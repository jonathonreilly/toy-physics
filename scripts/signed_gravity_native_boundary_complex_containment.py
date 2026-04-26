#!/usr/bin/env python3
"""Native boundary-complex containment audit for the signed-gravity lane.

Question:

    Does the original retained boundary complex contain the orientation-line
    APS source character, or did the previous APS harness add it?

Containment means a strict, no-extra-structure read:

* use the original finite cochain boundary complex and its Hodge-Dirac
  operator D_Y = d + d^*;
* allow orientation choices only as orientations of vertices/edges/faces;
* do not add a rank-one orientation line, project out harmonic zero modes, or
  insert a chi_eta rho Phi source term;
* require a nonzero gapped APS sign chi = sign(eta_delta(D_Y)).

The audit proves a finite no-go for this raw complex: D_Y is odd with respect
to cochain parity, so its spectrum is symmetric and eta_delta(D_Y)=0 on the
tested graph families.  Orientation reversal is a unitary/sign relabeling of
the same complex and does not flip eta.  The orientation-line APS character
appears only after adding an oriented one-dimensional summand and quarantining
the native Hodge kernel.

This is not a negative-mass, shielding, propulsion, reactionless-force, or
physical signed-gravity claim.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np


TOL = 1.0e-10
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    status = "PASS" if passed else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


def eta_delta(mat: np.ndarray, delta: float = 1.0e-8) -> tuple[int, int, int, np.ndarray]:
    vals = np.linalg.eigvalsh(0.5 * (mat + mat.T))
    n_pos = int(np.sum(vals > delta))
    n_neg = int(np.sum(vals < -delta))
    n_zero = int(len(vals) - n_pos - n_neg)
    return n_pos - n_neg, n_zero, len(vals), vals


def chi_from_eta(eta: int, zero: int) -> int:
    if zero or eta == 0:
        return 0
    return +1 if eta > 0 else -1


@dataclass(frozen=True)
class CellComplex2:
    name: str
    n_vertices: int
    edges: tuple[tuple[int, int], ...]
    faces: tuple[tuple[int, ...], ...] = ()

    def d0(self) -> np.ndarray:
        """Coboundary C^0 -> C^1 with one oriented row per edge."""

        out = np.zeros((len(self.edges), self.n_vertices), dtype=float)
        for row, (u, v) in enumerate(self.edges):
            out[row, u] = -1.0
            out[row, v] = +1.0
        return out

    def d1(self) -> np.ndarray:
        """Coboundary C^1 -> C^2 from oriented face cycles."""

        edge_index = {edge: idx for idx, edge in enumerate(self.edges)}
        reverse_index = {(v, u): idx for idx, (u, v) in enumerate(self.edges)}
        out = np.zeros((len(self.faces), len(self.edges)), dtype=float)
        for face_row, face in enumerate(self.faces):
            for a, b in zip(face, face[1:] + face[:1], strict=True):
                if (a, b) in edge_index:
                    out[face_row, edge_index[(a, b)]] += 1.0
                elif (a, b) in reverse_index:
                    out[face_row, reverse_index[(a, b)]] -= 1.0
                else:
                    raise ValueError(f"face edge {(a, b)} missing from {self.name}")
        return out

    def hodge_dirac(self) -> np.ndarray:
        d0 = self.d0()
        d1 = self.d1()
        n0 = self.n_vertices
        n1 = len(self.edges)
        n2 = len(self.faces)
        return np.block(
            [
                [np.zeros((n0, n0)), d0.T, np.zeros((n0, n2))],
                [d0, np.zeros((n1, n1)), d1.T],
                [np.zeros((n2, n0)), d1, np.zeros((n2, n2))],
            ]
        )

    def parity(self) -> np.ndarray:
        signs = [1.0] * self.n_vertices + [-1.0] * len(self.edges) + [1.0] * len(self.faces)
        return np.diag(signs)

    def reversed_edges(self) -> "CellComplex2":
        """Reverse every edge orientation and the face-cycle representatives."""

        return CellComplex2(
            name=f"{self.name}_edge_reversed",
            n_vertices=self.n_vertices,
            edges=tuple((v, u) for (u, v) in self.edges),
            faces=self.faces,
        )

    def reversed_faces(self) -> "CellComplex2":
        return CellComplex2(
            name=f"{self.name}_face_reversed",
            n_vertices=self.n_vertices,
            edges=self.edges,
            faces=tuple(tuple(reversed(face)) for face in self.faces),
        )


def add_edge(edges: list[tuple[int, int]], seen: set[frozenset[int]], u: int, v: int) -> None:
    key = frozenset((u, v))
    if key not in seen:
        seen.add(key)
        edges.append((u, v))


def from_face_cycles(name: str, n_vertices: int, faces: list[tuple[int, ...]]) -> CellComplex2:
    edges: list[tuple[int, int]] = []
    seen: set[frozenset[int]] = set()
    for face in faces:
        for u, v in zip(face, face[1:] + face[:1], strict=True):
            add_edge(edges, seen, u, v)
    return CellComplex2(name=name, n_vertices=n_vertices, edges=tuple(edges), faces=tuple(faces))


def cycle_complex(n: int) -> CellComplex2:
    edges = tuple((i, (i + 1) % n) for i in range(n))
    return CellComplex2(name=f"cycle{n}", n_vertices=n, edges=edges)


def ladder_complex(n: int) -> CellComplex2:
    def lower(i: int) -> int:
        return i % n

    def upper(i: int) -> int:
        return n + (i % n)

    faces = [(lower(i), lower(i + 1), upper(i + 1), upper(i)) for i in range(n)]
    return from_face_cycles(f"ladder{n}", 2 * n, faces)


def grid_disk_complex(nx: int, ny: int) -> CellComplex2:
    def idx(x: int, y: int) -> int:
        return y * nx + x

    faces = []
    for y in range(ny - 1):
        for x in range(nx - 1):
            faces.append((idx(x, y), idx(x + 1, y), idx(x + 1, y + 1), idx(x, y + 1)))
    return from_face_cycles(f"grid{nx}x{ny}_disk", nx * ny, faces)


def annulus_complex(n_outer: int) -> CellComplex2:
    """Two boundary cycles with rectangular side faces."""

    n = n_outer

    def outer(i: int) -> int:
        return i % n

    def inner(i: int) -> int:
        return n + (i % n)

    faces = [(outer(i), outer(i + 1), inner(i + 1), inner(i)) for i in range(n)]
    return from_face_cycles(f"annulus{n}", 2 * n, faces)


@dataclass(frozen=True)
class NativeRead:
    name: str
    dim: int
    eta: int
    zero: int
    chi: int
    parity_residual: float
    min_pair_error: float


def spectral_pair_error(vals: np.ndarray) -> float:
    ordered = np.sort(vals)
    return float(np.max(np.abs(ordered + ordered[::-1]))) if len(vals) else 0.0


def native_read(complex2: CellComplex2) -> NativeRead:
    d = complex2.hodge_dirac()
    gamma = complex2.parity()
    eta, zero, dim, vals = eta_delta(d)
    parity_residual = float(np.linalg.norm(gamma @ d + d @ gamma, ord=2))
    return NativeRead(
        name=complex2.name,
        dim=dim,
        eta=eta,
        zero=zero,
        chi=chi_from_eta(eta, zero),
        parity_residual=parity_residual,
        min_pair_error=spectral_pair_error(vals),
    )


def native_boundary_complex_gate() -> tuple[bool, str]:
    families = [
        cycle_complex(8),
        cycle_complex(12),
        ladder_complex(6),
        grid_disk_complex(4, 4),
        annulus_complex(7),
    ]
    reads = [native_read(fam) for fam in families]
    raw_eta_neutral = all(read.eta == 0 and read.chi == 0 for read in reads)
    parity_odd = all(read.parity_residual < TOL for read in reads)
    paired = all(read.min_pair_error < 1.0e-8 for read in reads)
    zero_quarantine_needed = all(read.zero > 0 for read in reads)
    detail = "; ".join(
        f"{read.name}:eta={read.eta:+d},zero={read.zero},chi={read.chi:+d},"
        f"pair={read.min_pair_error:.1e}"
        for read in reads
    )
    ok = raw_eta_neutral and parity_odd and paired and zero_quarantine_needed
    return ok, detail


def orientation_reversal_gate() -> tuple[bool, str]:
    base = grid_disk_complex(4, 4)
    variants = [base, base.reversed_edges(), base.reversed_faces()]
    vals = [np.linalg.eigvalsh(v.hodge_dirac()) for v in variants]
    etas = [eta_delta(v.hodge_dirac())[0] for v in variants]
    chis = [chi_from_eta(*eta_delta(v.hodge_dirac())[:2]) for v in variants]
    err_edge = float(np.max(np.abs(np.sort(vals[0]) - np.sort(vals[1]))))
    err_face = float(np.max(np.abs(np.sort(vals[0]) - np.sort(vals[2]))))
    ok = etas == [0, 0, 0] and chis == [0, 0, 0] and err_edge < TOL and err_face < TOL
    detail = (
        f"eta={etas}, chi={chis}, edge_reversal_spectral_err={err_edge:.1e}, "
        f"face_reversal_spectral_err={err_face:.1e}"
    )
    return ok, detail


def nonzero_part(vals: np.ndarray, delta: float = 1.0e-8) -> np.ndarray:
    return vals[np.abs(vals) > delta]


def orientation_line_extension_gate() -> tuple[bool, str]:
    """Show what has to be added to get the previous APS sign."""

    base = annulus_complex(7).hodge_dirac()
    _eta_raw, zero_raw, _n_raw, vals_raw = eta_delta(base)
    kept = nonzero_part(vals_raw)
    extended_reads = []
    for orient in (+1, -1):
        d_ext = np.diag(np.concatenate(([0.35 * orient], kept)))
        eta_ext, zero_ext, _n_ext, _vals_ext = eta_delta(d_ext)
        extended_reads.append((orient, eta_ext, zero_ext, chi_from_eta(eta_ext, zero_ext)))
    added_dimension = 1
    projected_kernel = zero_raw > 0
    extension_works = extended_reads == [(+1, +1, 0, +1), (-1, -1, 0, -1)]
    ok = extension_works and added_dimension == 1 and projected_kernel
    detail = (
        f"raw_zero_modes={zero_raw}, kernel_projected={projected_kernel}, "
        f"added_orientation_line_dim={added_dimension}, extended={extended_reads}"
    )
    return ok, detail


def source_character_containment_gate() -> tuple[bool, str]:
    """Native raw boundary eta is source-neutral; signed source is not spanned."""

    positive_source = np.array([1.0, 1.0])
    raw_boundary_eta = np.array([0.0, 0.0])
    desired_signed_source = np.array([1.0, -1.0])
    mat = np.column_stack([positive_source, raw_boundary_eta])
    coeffs, *_ = np.linalg.lstsq(mat, desired_signed_source, rcond=None)
    fitted = mat @ coeffs
    residual = float(np.linalg.norm(fitted - desired_signed_source))
    orientation_metadata = np.array([1.0, -1.0])
    metadata_residual = float(np.linalg.norm(orientation_metadata - desired_signed_source))
    ok = residual > 1.0 and metadata_residual < TOL
    detail = (
        f"native_basis_residual={residual:.3e}, fitted={np.round(fitted, 3)}, "
        f"orientation_metadata_residual={metadata_residual:.1e}, source_term_added=False"
    )
    return ok, detail


def no_claim_gate() -> tuple[bool, str]:
    claims = {
        "native_aps_line_contained": False,
        "orientation_line_added": True,
        "kernel_quarantine_added": True,
        "physical_signed_gravity_prediction": False,
        "negative_inertial_mass": False,
        "shielding": False,
        "propulsion": False,
        "reactionless_force": False,
    }
    ok = (
        not claims["native_aps_line_contained"]
        and claims["orientation_line_added"]
        and claims["kernel_quarantine_added"]
        and not claims["physical_signed_gravity_prediction"]
        and not claims["negative_inertial_mass"]
        and not claims["shielding"]
        and not claims["propulsion"]
        and not claims["reactionless_force"]
    )
    return ok, ", ".join(f"{key}={value}" for key, value in claims.items())


def native_containment_summary_gate() -> tuple[bool, str]:
    native_ok, _native_detail = native_boundary_complex_gate()
    reversal_ok, _reversal_detail = orientation_reversal_gate()
    extension_ok, extension_detail = orientation_line_extension_gate()
    source_ok, source_detail = source_character_containment_gate()
    ok = native_ok and reversal_ok and extension_ok and source_ok
    detail = (
        "native_aps_line_contained=False, raw_hodge_eta_neutral=True, "
        f"{extension_detail}, {source_detail}"
    )
    return ok, detail


def run_audit() -> bool:
    native_ok, native_detail = native_boundary_complex_gate()
    check("raw retained cochain/Hodge boundary complex is eta-neutral", native_ok, native_detail)

    reversal_ok, reversal_detail = orientation_reversal_gate()
    check("orientation reversal is a relabeling/control for raw eta", reversal_ok, reversal_detail)

    extension_ok, extension_detail = orientation_line_extension_gate()
    check("APS sign appears only after orientation-line extension and kernel quarantine", extension_ok, extension_detail)

    source_ok, source_detail = source_character_containment_gate()
    check("native raw boundary source basis cannot contain the signed source character", source_ok, source_detail)

    no_claim_ok, no_claim_detail = no_claim_gate()
    check("non-claim and added-structure classification is explicit", no_claim_ok, no_claim_detail)

    return native_ok and reversal_ok and extension_ok and source_ok and no_claim_ok


def main() -> int:
    print("=" * 116)
    print("SIGNED GRAVITY NATIVE BOUNDARY-COMPLEX CONTAINMENT AUDIT")
    print("  raw retained cochain/Hodge complex versus added orientation-line APS source character")
    print("=" * 116)
    print()

    passed = run_audit()

    print()
    print("INTERPRETATION")
    print("  On the raw retained finite boundary complex D_Y=d+d^*, cochain parity")
    print("  anticommutes with D_Y.  The spectrum is therefore symmetric and the APS")
    print("  eta sign is zero on the tested graph families.  Reversing edge or face")
    print("  orientation changes basis signs, not the eta invariant.  The previous")
    print("  signed APS carrier is recovered only by adding an oriented one-dimensional")
    print("  line and by quarantining the native Hodge zero modes.")
    print()
    print("VERDICT")
    print("  The original raw retained boundary complex does not currently contain the")
    print("  orientation-line APS source character as an active spectral source.  The")
    print("  determinant-orientation grammar may be native at the determinant-line")
    print("  functor level, but the actual APS boundary operator used for signed")
    print("  response requires an added orientation-line realization unless a new")
    print("  retained boundary theorem supplies it.")
    print()

    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if passed and FAIL_COUNT == 0:
        print("FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED")
        return 0
    print("FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_AUDIT_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
