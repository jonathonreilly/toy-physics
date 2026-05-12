#!/usr/bin/env python3
"""
Resumable Wilson-staggered top-correlator production harness.

This script is intentionally evidence-conservative.  It implements the
production machinery requested by the direct-correlator y_t lane:

* SU(3) Wilson gauge updates with Cabibbo-Marinari SU(2) subgroup heat-bath
  steps and an optional polar-projection overrelaxation sweep.
* APE smearing of spatial links for the measurement operator.
* Staggered Dirac operator with antiperiodic temporal fermion boundary
  conditions.
* Propagator inversion through conjugate gradient on D^dagger D.
* Point-source staggered correlator measurement, optional same-source scalar
  two-point and source-Higgs cross-correlator instrumentation, effective-mass
  fit, jackknife statistical errors, and strict-runner certificate emission.

The default command runs a reduced-scope smoke/feasibility measurement because
the requested 12^3x24, 16^3x32, and 24^3x48 production campaign with 1000+
thermalization sweeps and 1000+ saved configurations is not feasible as an
interactive PR update.  Use --production-targets to configure the full campaign;
the emitted certificate will still be rejected by the strict runner unless the
required volumes/statistics are actually present.
"""

from __future__ import annotations

import argparse
import cProfile
import io
import json
import math
import platform
import pstats
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg

try:
    from numba import njit
except Exception:  # pragma: no cover - optional acceleration dependency
    njit = None


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator"
PRODUCTION_OUTPUT_DIR = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator_production"
DEFAULT_CERTIFICATE = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator_certificate_2026-04-30.json"
PILOT_OUTPUT_DIR = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator_pilot"
PILOT_CERTIFICATE = REPO_ROOT / "outputs" / "yt_direct_lattice_correlator_pilot_certificate_2026-04-30.json"

NC = 3
NDIM = 4
BETA = 6.0
HBARC_GEV_FM = 0.1973269804
R0_FM = 0.5
R0_OVER_A_BETA6_REFERENCE = 5.37
V_GEV = 246.21965
PDG_TOP_MASS_GEV = 172.56
YT_TARGET = 0.917
NUMBA_AVAILABLE = njit is not None


if NUMBA_AVAILABLE:

    @njit
    def nb_seed(seed: int) -> None:
        np.random.seed(seed)


    @njit
    def nb_eye3() -> np.ndarray:
        out = np.zeros((3, 3), dtype=np.complex128)
        for i in range(3):
            out[i, i] = 1.0 + 0.0j
        return out


    @njit
    def nb_matmul3(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        out = np.zeros((3, 3), dtype=np.complex128)
        for i in range(3):
            for j in range(3):
                s = 0.0 + 0.0j
                for k in range(3):
                    s += a[i, k] * b[k, j]
                out[i, j] = s
        return out


    @njit
    def nb_dagger3(a: np.ndarray) -> np.ndarray:
        out = np.empty((3, 3), dtype=np.complex128)
        for i in range(3):
            for j in range(3):
                out[i, j] = np.conj(a[j, i])
        return out


    @njit
    def nb_det3(a: np.ndarray) -> complex:
        return (
            a[0, 0] * (a[1, 1] * a[2, 2] - a[1, 2] * a[2, 1])
            - a[0, 1] * (a[1, 0] * a[2, 2] - a[1, 2] * a[2, 0])
            + a[0, 2] * (a[1, 0] * a[2, 1] - a[1, 1] * a[2, 0])
        )


    @njit
    def nb_project_su3(mat: np.ndarray) -> np.ndarray:
        out = np.empty((3, 3), dtype=np.complex128)
        norm0 = 0.0
        for i in range(3):
            norm0 += (np.conj(mat[i, 0]) * mat[i, 0]).real
        norm0 = math.sqrt(max(norm0, 1.0e-30))
        for i in range(3):
            out[i, 0] = mat[i, 0] / norm0

        dot01 = 0.0 + 0.0j
        for i in range(3):
            dot01 += np.conj(out[i, 0]) * mat[i, 1]
        norm1 = 0.0
        for i in range(3):
            out[i, 1] = mat[i, 1] - dot01 * out[i, 0]
            norm1 += (np.conj(out[i, 1]) * out[i, 1]).real
        norm1 = math.sqrt(max(norm1, 1.0e-30))
        for i in range(3):
            out[i, 1] /= norm1

        out[0, 2] = np.conj(out[1, 0] * out[2, 1] - out[2, 0] * out[1, 1])
        out[1, 2] = np.conj(out[2, 0] * out[0, 1] - out[0, 0] * out[2, 1])
        out[2, 2] = np.conj(out[0, 0] * out[1, 1] - out[1, 0] * out[0, 1])

        det = nb_det3(out)
        if abs(det) > 1.0e-30:
            for i in range(3):
                out[i, 2] /= det
        return out


    @njit
    def nb_random_su2_quaternion() -> np.ndarray:
        out = np.empty(4, dtype=np.float64)
        norm = 0.0
        for i in range(4):
            v = np.random.normal()
            out[i] = v
            norm += v * v
        norm = math.sqrt(max(norm, 1.0e-30))
        for i in range(4):
            out[i] /= norm
        return out


    @njit
    def nb_quaternion_to_su2(q: np.ndarray) -> np.ndarray:
        out = np.empty((2, 2), dtype=np.complex128)
        a0, a1, a2, a3 = q[0], q[1], q[2], q[3]
        out[0, 0] = a0 + 1j * a3
        out[0, 1] = a2 + 1j * a1
        out[1, 0] = -a2 + 1j * a1
        out[1, 1] = a0 - 1j * a3
        return out


    @njit
    def nb_su2_heatbath_quaternion(k: float) -> np.ndarray:
        if k < 1.0e-10:
            return nb_random_su2_quaternion()
        two_k = 2.0 * k
        a0 = 0.0
        for _ in range(10000):
            r = np.random.random()
            if two_k > 100.0:
                a0 = 1.0 + math.log(max(r + (1.0 - r) * math.exp(-2.0 * two_k), 1.0e-300)) / two_k
            else:
                a0 = math.log(r * math.exp(two_k) + (1.0 - r) * math.exp(-two_k)) / two_k
            if -1.0 <= a0 <= 1.0 and np.random.random() < math.sqrt(max(1.0 - a0 * a0, 0.0)):
                break
        radius = math.sqrt(max(1.0 - a0 * a0, 0.0))
        phi = 2.0 * math.pi * np.random.random()
        cos_theta = 2.0 * np.random.random() - 1.0
        sin_theta = math.sqrt(max(1.0 - cos_theta * cos_theta, 0.0))
        out = np.empty(4, dtype=np.float64)
        out[0] = a0
        out[1] = radius * sin_theta * math.cos(phi)
        out[2] = radius * sin_theta * math.sin(phi)
        out[3] = radius * cos_theta
        return out


    @njit
    def nb_subgroup_pair(subgroup: int) -> tuple[int, int]:
        if subgroup == 0:
            return 0, 1
        if subgroup == 1:
            return 0, 2
        return 1, 2


    @njit
    def nb_extract_su2(mat: np.ndarray, subgroup: int) -> np.ndarray:
        i0, i1 = nb_subgroup_pair(subgroup)
        out = np.empty((2, 2), dtype=np.complex128)
        out[0, 0] = mat[i0, i0]
        out[0, 1] = mat[i0, i1]
        out[1, 0] = mat[i1, i0]
        out[1, 1] = mat[i1, i1]
        return out


    @njit
    def nb_embed_su2(mat: np.ndarray, subgroup: int) -> np.ndarray:
        out = nb_eye3()
        i0, i1 = nb_subgroup_pair(subgroup)
        out[i0, i0] = mat[0, 0]
        out[i0, i1] = mat[0, 1]
        out[i1, i0] = mat[1, 0]
        out[i1, i1] = mat[1, 1]
        return out


    @njit
    def nb_matmul2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        out = np.empty((2, 2), dtype=np.complex128)
        out[0, 0] = a[0, 0] * b[0, 0] + a[0, 1] * b[1, 0]
        out[0, 1] = a[0, 0] * b[0, 1] + a[0, 1] * b[1, 1]
        out[1, 0] = a[1, 0] * b[0, 0] + a[1, 1] * b[1, 0]
        out[1, 1] = a[1, 0] * b[0, 1] + a[1, 1] * b[1, 1]
        return out


    @njit
    def nb_dagger2(a: np.ndarray) -> np.ndarray:
        out = np.empty((2, 2), dtype=np.complex128)
        out[0, 0] = np.conj(a[0, 0])
        out[0, 1] = np.conj(a[1, 0])
        out[1, 0] = np.conj(a[0, 1])
        out[1, 1] = np.conj(a[1, 1])
        return out


    @njit
    def nb_project_su2(mat: np.ndarray) -> np.ndarray:
        det = mat[0, 0] * mat[1, 1] - mat[0, 1] * mat[1, 0]
        if abs(det) < 1.0e-30:
            out = np.zeros((2, 2), dtype=np.complex128)
            out[0, 0] = 1.0 + 0.0j
            out[1, 1] = 1.0 + 0.0j
            return out
        root = np.sqrt(det)
        v00 = mat[0, 0] / root
        v01 = mat[0, 1] / root
        v10 = mat[1, 0] / root
        v11 = mat[1, 1] / root
        a = 0.5 * (v00 + np.conj(v11))
        b = 0.5 * (v10 - np.conj(v01))
        norm = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
        out = np.empty((2, 2), dtype=np.complex128)
        if norm < 1.0e-30:
            out[0, 0] = 1.0 + 0.0j
            out[0, 1] = 0.0 + 0.0j
            out[1, 0] = 0.0 + 0.0j
            out[1, 1] = 1.0 + 0.0j
            return out
        a /= norm
        b /= norm
        out[0, 0] = a
        out[0, 1] = -np.conj(b)
        out[1, 0] = b
        out[1, 1] = np.conj(a)
        return out


    @njit
    def nb_shift(t: int, x: int, y: int, z: int, mu: int, step: int, time_l: int, spatial_l: int) -> tuple[int, int, int, int]:
        if mu == 0:
            return (t + step) % time_l, x, y, z
        if mu == 1:
            return t, (x + step) % spatial_l, y, z
        if mu == 2:
            return t, x, (y + step) % spatial_l, z
        return t, x, y, (z + step) % spatial_l


    @njit
    def nb_staple(u: np.ndarray, t: int, x: int, y: int, z: int, mu: int) -> np.ndarray:
        time_l = u.shape[0]
        spatial_l = u.shape[1]
        acc = np.zeros((3, 3), dtype=np.complex128)
        tp_mu, xp_mu, yp_mu, zp_mu = nb_shift(t, x, y, z, mu, 1, time_l, spatial_l)
        for nu in range(4):
            if nu == mu:
                continue
            tp_nu, xp_nu, yp_nu, zp_nu = nb_shift(t, x, y, z, nu, 1, time_l, spatial_l)
            tm_nu, xm_nu, ym_nu, zm_nu = nb_shift(t, x, y, z, nu, -1, time_l, spatial_l)
            tpm, xpm, ypm, zpm = nb_shift(tp_mu, xp_mu, yp_mu, zp_mu, nu, -1, time_l, spatial_l)

            term = nb_matmul3(
                nb_matmul3(u[tp_mu, xp_mu, yp_mu, zp_mu, nu], nb_dagger3(u[tp_nu, xp_nu, yp_nu, zp_nu, mu])),
                nb_dagger3(u[t, x, y, z, nu]),
            )
            acc += term
            term = nb_matmul3(
                nb_matmul3(nb_dagger3(u[tpm, xpm, ypm, zpm, nu]), nb_dagger3(u[tm_nu, xm_nu, ym_nu, zm_nu, mu])),
                u[tm_nu, xm_nu, ym_nu, zm_nu, nu],
            )
            acc += term
        return acc


    @njit
    def nb_heatbath_link(u: np.ndarray, t: int, x: int, y: int, z: int, mu: int, beta: float) -> None:
        staple = nb_staple(u, t, x, y, z, mu)
        link = u[t, x, y, z, mu].copy()
        for subgroup in range(3):
            w = nb_matmul3(link, staple)
            w2 = nb_extract_su2(w, subgroup)
            det_w2 = w2[0, 0] * w2[1, 1] - w2[0, 1] * w2[1, 0]
            scale = math.sqrt(max(det_w2.real, 0.0))
            if scale < 1.0e-15:
                rotation2 = nb_quaternion_to_su2(nb_random_su2_quaternion())
            else:
                k = (beta / 3.0) * scale
                r_new = nb_quaternion_to_su2(nb_su2_heatbath_quaternion(k))
                rotation2 = nb_matmul2(r_new, nb_dagger2(nb_project_su2(w2)))
            link = nb_matmul3(nb_embed_su2(rotation2, subgroup), link)
        u[t, x, y, z, mu] = nb_project_su3(link)


    @njit
    def nb_heatbath_sweep(u: np.ndarray, beta: float) -> None:
        for t in range(u.shape[0]):
            for x in range(u.shape[1]):
                for y in range(u.shape[2]):
                    for z in range(u.shape[3]):
                        for mu in range(4):
                            nb_heatbath_link(u, t, x, y, z, mu, beta)


    @njit
    def nb_overrelax_link(u: np.ndarray, t: int, x: int, y: int, z: int, mu: int) -> None:
        staple = nb_staple(u, t, x, y, z, mu)
        target = nb_project_su3(nb_dagger3(staple))
        link = nb_matmul3(nb_matmul3(target, nb_dagger3(u[t, x, y, z, mu])), target)
        u[t, x, y, z, mu] = nb_project_su3(link)


    @njit
    def nb_overrelax_sweep(u: np.ndarray) -> None:
        for t in range(u.shape[0]):
            for x in range(u.shape[1]):
                for y in range(u.shape[2]):
                    for z in range(u.shape[3]):
                        for mu in range(4):
                            nb_overrelax_link(u, t, x, y, z, mu)


    @njit
    def nb_plaquette(u: np.ndarray) -> float:
        total = 0.0
        count = 0
        time_l = u.shape[0]
        spatial_l = u.shape[1]
        for t in range(time_l):
            for x in range(spatial_l):
                for y in range(spatial_l):
                    for z in range(spatial_l):
                        for mu in range(4):
                            tp_mu, xp_mu, yp_mu, zp_mu = nb_shift(t, x, y, z, mu, 1, time_l, spatial_l)
                            for nu in range(mu + 1, 4):
                                tp_nu, xp_nu, yp_nu, zp_nu = nb_shift(t, x, y, z, nu, 1, time_l, spatial_l)
                                p = nb_matmul3(
                                    nb_matmul3(
                                        nb_matmul3(u[t, x, y, z, mu], u[tp_mu, xp_mu, yp_mu, zp_mu, nu]),
                                        nb_dagger3(u[tp_nu, xp_nu, yp_nu, zp_nu, mu]),
                                    ),
                                    nb_dagger3(u[t, x, y, z, nu]),
                                )
                                total += (p[0, 0] + p[1, 1] + p[2, 2]).real / 3.0
                                count += 1
        return total / count


    @njit
    def nb_warmup() -> None:
        u = np.zeros((2, 2, 2, 2, 4, 3, 3), dtype=np.complex128)
        for t in range(2):
            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        for mu in range(4):
                            for c in range(3):
                                u[t, x, y, z, mu, c, c] = 1.0 + 0.0j
        nb_seed(17)
        nb_heatbath_sweep(u, 6.0)
        nb_overrelax_sweep(u)
        nb_plaquette(u)


def project_su3(mat: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(mat)
    d = np.diag(r)
    phase = np.ones_like(d)
    mask = np.abs(d) > 1.0e-14
    phase[mask] = d[mask] / np.abs(d[mask])
    q = q @ np.diag(np.conj(phase))
    det = np.linalg.det(q)
    q *= np.exp(-1j * np.angle(det) / 3.0)
    return q


def random_su2_quaternion(rng: np.random.Generator) -> np.ndarray:
    q = rng.normal(size=4)
    q /= np.linalg.norm(q)
    return q


def quaternion_to_su2(q: np.ndarray) -> np.ndarray:
    a0, a1, a2, a3 = q
    return np.array(
        [[a0 + 1j * a3, a2 + 1j * a1], [-a2 + 1j * a1, a0 - 1j * a3]],
        dtype=complex,
    )


def su2_heatbath_quaternion(k: float, rng: np.random.Generator) -> np.ndarray:
    if k < 1.0e-10:
        return random_su2_quaternion(rng)
    two_k = 2.0 * k
    a0 = 0.0
    for _ in range(10000):
        r = rng.random()
        if two_k > 100.0:
            a0 = 1.0 + math.log(max(r + (1.0 - r) * math.exp(-2.0 * two_k), 1.0e-300)) / two_k
        else:
            a0 = math.log(r * math.exp(two_k) + (1.0 - r) * math.exp(-two_k)) / two_k
        if -1.0 <= a0 <= 1.0 and rng.random() < math.sqrt(max(1.0 - a0 * a0, 0.0)):
            break
    else:
        a0 = 0.99
    radius = math.sqrt(max(1.0 - a0 * a0, 0.0))
    phi = 2.0 * math.pi * rng.random()
    cos_theta = 2.0 * rng.random() - 1.0
    sin_theta = math.sqrt(max(1.0 - cos_theta * cos_theta, 0.0))
    return np.array(
        [
            a0,
            radius * sin_theta * math.cos(phi),
            radius * sin_theta * math.sin(phi),
            radius * cos_theta,
        ]
    )


def subgroup_indices(subgroup: int) -> tuple[int, int]:
    if subgroup == 0:
        return (0, 1)
    if subgroup == 1:
        return (0, 2)
    return (1, 2)


def extract_su2(mat: np.ndarray, subgroup: int) -> np.ndarray:
    idx = subgroup_indices(subgroup)
    return mat[np.ix_(idx, idx)]


def embed_su2(mat: np.ndarray, subgroup: int) -> np.ndarray:
    out = np.eye(3, dtype=complex)
    idx = subgroup_indices(subgroup)
    for i2, i3 in enumerate(idx):
        for j2, j3 in enumerate(idx):
            out[i3, j3] = mat[i2, j2]
    return out


def project_su2(mat: np.ndarray) -> np.ndarray:
    det = np.linalg.det(mat)
    if abs(det) < 1.0e-30:
        return np.eye(2, dtype=complex)
    v = mat / np.sqrt(det)
    a = (v[0, 0] + np.conj(v[1, 1])) / 2.0
    b = (v[1, 0] - np.conj(v[0, 1])) / 2.0
    norm = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
    if norm < 1.0e-30:
        return np.eye(2, dtype=complex)
    a /= norm
    b /= norm
    return np.array([[a, -np.conj(b)], [b, np.conj(a)]], dtype=complex)


@dataclass(frozen=True)
class Geometry:
    spatial_l: int
    time_l: int

    @property
    def dims(self) -> tuple[int, int, int, int]:
        return (self.time_l, self.spatial_l, self.spatial_l, self.spatial_l)

    @property
    def volume(self) -> int:
        return self.time_l * self.spatial_l**3

    def site_index(self, coords: tuple[int, int, int, int]) -> int:
        t, x, y, z = coords
        l = self.spatial_l
        return ((t * l + x) * l + y) * l + z

    def site_coords(self, index: int) -> tuple[int, int, int, int]:
        l = self.spatial_l
        z = index % l
        index //= l
        y = index % l
        index //= l
        x = index % l
        t = index // l
        return (t, x, y, z)

    def shifted(self, coords: tuple[int, int, int, int], mu: int, step: int) -> tuple[int, int, int, int]:
        out = list(coords)
        out[mu] = (out[mu] + step) % self.dims[mu]
        return (out[0], out[1], out[2], out[3])


class GaugeField:
    def __init__(self, geom: Geometry) -> None:
        self.geom = geom
        self.u = np.zeros((*geom.dims, NDIM, NC, NC), dtype=complex)
        for coords in np.ndindex(*geom.dims):
            self.u[coords] = np.eye(NC, dtype=complex)

    def copy(self) -> "GaugeField":
        other = GaugeField(self.geom)
        other.u = self.u.copy()
        return other

    def staple(self, coords: tuple[int, int, int, int], mu: int) -> np.ndarray:
        acc = np.zeros((NC, NC), dtype=complex)
        xp_mu = self.geom.shifted(coords, mu, +1)
        for nu in range(NDIM):
            if nu == mu:
                continue
            xp_nu = self.geom.shifted(coords, nu, +1)
            xm_nu = self.geom.shifted(coords, nu, -1)
            xp_mu_m_nu = self.geom.shifted(xp_mu, nu, -1)
            acc += (
                self.u[xp_mu][nu]
                @ self.u[xp_nu][mu].conj().T
                @ self.u[coords][nu].conj().T
            )
            acc += (
                self.u[xp_mu_m_nu][nu].conj().T
                @ self.u[xm_nu][mu].conj().T
                @ self.u[xm_nu][nu]
            )
        return acc

    def heatbath_link(self, coords: tuple[int, int, int, int], mu: int, rng: np.random.Generator) -> None:
        staple = self.staple(coords, mu)
        for subgroup in range(3):
            w = self.u[coords][mu] @ staple
            w2 = extract_su2(w, subgroup)
            det_w2 = np.linalg.det(w2)
            scale = math.sqrt(max(float(np.real(det_w2)), 0.0))
            if scale < 1.0e-15:
                r_new = quaternion_to_su2(random_su2_quaternion(rng))
                rotation = r_new
            else:
                k = (BETA / NC) * scale
                r_new = quaternion_to_su2(su2_heatbath_quaternion(k, rng))
                rotation = r_new @ project_su2(w2).conj().T
            self.u[coords][mu] = embed_su2(rotation, subgroup) @ self.u[coords][mu]
        self.u[coords][mu] = project_su3(self.u[coords][mu])

    def heatbath_sweep(self, rng: np.random.Generator) -> None:
        for coords in np.ndindex(*self.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in range(NDIM):
                self.heatbath_link(c, mu, rng)

    def overrelax_link(self, coords: tuple[int, int, int, int], mu: int) -> None:
        staple = self.staple(coords, mu)
        target = project_su3(staple.conj().T)
        self.u[coords][mu] = project_su3(target @ self.u[coords][mu].conj().T @ target)

    def overrelax_sweep(self) -> None:
        for coords in np.ndindex(*self.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in range(NDIM):
                self.overrelax_link(c, mu)

    def plaquette(self) -> float:
        total = 0.0
        count = 0
        for coords in np.ndindex(*self.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in range(NDIM):
                for nu in range(mu + 1, NDIM):
                    xp_mu = self.geom.shifted(c, mu, +1)
                    xp_nu = self.geom.shifted(c, nu, +1)
                    p = (
                        self.u[c][mu]
                        @ self.u[xp_mu][nu]
                        @ self.u[xp_nu][mu].conj().T
                        @ self.u[c][nu].conj().T
                    )
                    total += float(np.trace(p).real / NC)
                    count += 1
        return total / count


def resolve_engine(args: argparse.Namespace) -> str:
    requested = getattr(args, "engine", "auto")
    if requested == "python":
        return "python"
    if requested == "numba":
        if not NUMBA_AVAILABLE:
            raise RuntimeError("requested --engine numba, but numba is not available")
        return "numba"
    return "numba" if NUMBA_AVAILABLE else "python"


def cold_link_array(geom: Geometry) -> np.ndarray:
    u = np.zeros((*geom.dims, NDIM, NC, NC), dtype=np.complex128)
    for color in range(NC):
        u[..., color, color] = 1.0 + 0.0j
    return u


def gauge_field_from_array(geom: Geometry, u: np.ndarray) -> GaugeField:
    gauge = GaugeField(geom)
    gauge.u = u
    return gauge


def warm_numba_kernels(seed: int) -> float:
    if not NUMBA_AVAILABLE:
        return 0.0
    t0 = time.perf_counter()
    nb_seed(seed)
    nb_warmup()
    return time.perf_counter() - t0


def ape_smear_spatial(gauge: GaugeField, alpha: float, steps: int) -> GaugeField:
    out = gauge.copy()
    for _ in range(steps):
        new_u = out.u.copy()
        for coords in np.ndindex(*out.geom.dims):
            c = (coords[0], coords[1], coords[2], coords[3])
            for mu in (1, 2, 3):
                staple = np.zeros((NC, NC), dtype=complex)
                for nu in (1, 2, 3):
                    if nu == mu:
                        continue
                    xp_mu = out.geom.shifted(c, mu, +1)
                    xp_nu = out.geom.shifted(c, nu, +1)
                    xm_nu = out.geom.shifted(c, nu, -1)
                    xp_mu_m_nu = out.geom.shifted(xp_mu, nu, -1)
                    staple += (
                        out.u[c][nu]
                        @ out.u[xp_nu][mu]
                        @ out.u[xp_mu][nu].conj().T
                    )
                    staple += (
                        out.u[xm_nu][nu].conj().T
                        @ out.u[xm_nu][mu]
                        @ out.u[xp_mu_m_nu][nu]
                    )
                new_u[c][mu] = project_su3((1.0 - alpha) * out.u[c][mu] + (alpha / 4.0) * staple)
        out.u = new_u
    return out


def staggered_eta(mu: int, coords: tuple[int, int, int, int]) -> float:
    return -1.0 if sum(coords[:mu]) % 2 else 1.0


def build_staggered_dirac(gauge: GaugeField, mass: float) -> sparse.csr_matrix:
    geom = gauge.geom
    n = geom.volume * NC
    rows: list[int] = []
    cols: list[int] = []
    vals: list[complex] = []
    for site in range(geom.volume):
        coords = geom.site_coords(site)
        for color in range(NC):
            idx = site * NC + color
            rows.append(idx)
            cols.append(idx)
            vals.append(mass)
        for mu in range(NDIM):
            eta = staggered_eta(mu, coords)
            fwd = geom.shifted(coords, mu, +1)
            bwd = geom.shifted(coords, mu, -1)
            fwd_site = geom.site_index(fwd)
            bwd_site = geom.site_index(bwd)
            apbc_fwd = -1.0 if mu == 0 and coords[0] == geom.time_l - 1 else 1.0
            apbc_bwd = -1.0 if mu == 0 and coords[0] == 0 else 1.0
            u_fwd = gauge.u[coords][mu]
            u_bwd = gauge.u[bwd][mu]
            for a in range(NC):
                row = site * NC + a
                for b in range(NC):
                    rows.append(row)
                    cols.append(fwd_site * NC + b)
                    vals.append(apbc_fwd * 0.5 * eta * u_fwd[a, b])
                    rows.append(row)
                    cols.append(bwd_site * NC + b)
                    vals.append(-apbc_bwd * 0.5 * eta * np.conj(u_bwd[b, a]))
    return sparse.csr_matrix((vals, (rows, cols)), shape=(n, n), dtype=complex)


@dataclass(frozen=True)
class NormalEquationSystem:
    mass: float
    D: sparse.csr_matrix
    dh: sparse.csr_matrix
    normal: sparse.csr_matrix


def build_normal_equation_system(gauge: GaugeField, mass: float) -> NormalEquationSystem:
    D = build_staggered_dirac(gauge, mass)
    dh = D.getH()
    normal = dh @ D
    return NormalEquationSystem(float(mass), D, dh, normal)


def normal_cache_key(mass: float) -> str:
    return f"{float(mass):.15g}"


def get_normal_equation_system(
    cache: dict[str, NormalEquationSystem],
    gauge: GaugeField,
    mass: float,
) -> NormalEquationSystem:
    key = normal_cache_key(mass)
    if key not in cache:
        cache[key] = build_normal_equation_system(gauge, mass)
    return cache[key]


def selected_scalar_fh_lsz_mass(masses: list[float]) -> float:
    return float(masses[len(masses) // 2])


def selected_mass_policy_metadata(masses: list[float], args: argparse.Namespace) -> dict[str, Any]:
    selected_mass = selected_scalar_fh_lsz_mass(masses)
    source_higgs_enabled = bool(getattr(args, "source_higgs_cross_modes_parsed", [])) and int(
        getattr(args, "source_higgs_cross_noises", 0)
    ) > 0 and bool(getattr(args, "source_higgs_operator_certificate_data", {}))
    source_higgs_time_kernel_enabled = bool(
        getattr(args, "source_higgs_time_kernel_modes_parsed", [])
    ) and int(getattr(args, "source_higgs_time_kernel_noises", 0)) > 0 and bool(
        getattr(args, "source_higgs_operator_certificate_data", {})
    )
    wz_smoke_enabled = wz_mass_response_smoke_enabled(args)
    return {
        "policy": "selected_mass_only_for_scalar_fh_lsz",
        "selected_mass_parameter": selected_mass,
        "selected_mass_index": len(masses) // 2,
        "top_correlator_mass_scan_preserved": True,
        "scalar_source_response_selected_mass_only": bool(getattr(args, "scalar_source_shifts_parsed", [])),
        "scalar_two_point_lsz_selected_mass_only": bool(getattr(args, "scalar_two_point_modes_parsed", []))
        and int(getattr(args, "scalar_two_point_noises", 0)) > 0,
        "source_higgs_cross_correlator_selected_mass_only": source_higgs_enabled,
        "source_higgs_time_kernel_selected_mass_only": source_higgs_time_kernel_enabled,
        "wz_mass_response_smoke_selected_mass_only": wz_smoke_enabled,
        "non_selected_masses_scalar_fh_lsz_skipped": [
            float(mass) for mass in masses if abs(float(mass) - selected_mass) > 1.0e-15
        ],
        "normal_equation_cache": {
            "scope": "per saved gauge configuration and smeared measurement gauge",
            "key": "mass/source-shift value",
            "reuse": "D, D^dagger, and D^dagger D are built once per needed mass/source per configuration and reused across point-source and stochastic RHS solves",
        },
        "physical_higgs_normalization": "not_derived",
        "used_as_physical_yukawa_readout": False,
        "strict_limit": (
            "Selected-mass source-coordinate FH/LSZ target time series are "
            "performance/instrumentation support only; they are not physical "
            "y_t evidence until canonical-Higgs/source-overlap or W/Z response "
            "identity gates close."
        ),
    }


def solve_vector_normal_eq_cached(
    system: NormalEquationSystem,
    rhs: np.ndarray,
    rtol: float,
    maxiter: int,
) -> tuple[np.ndarray, int, float]:
    b = system.dh @ rhs
    sol, info = cg(system.normal, b, rtol=rtol, atol=0.0, maxiter=maxiter)
    residual = float(np.linalg.norm(system.normal @ sol - b) / max(np.linalg.norm(b), 1.0e-30))
    return sol, int(info), residual


def solve_vector_normal_eq(D: sparse.csr_matrix, rhs: np.ndarray, rtol: float, maxiter: int) -> tuple[np.ndarray, int, float]:
    dh = D.getH()
    normal = dh @ D
    return solve_vector_normal_eq_cached(NormalEquationSystem(float("nan"), D, dh, normal), rhs, rtol, maxiter)


def solve_propagator_normal_eq_cached(
    system: NormalEquationSystem,
    source_index: int,
    rtol: float,
    maxiter: int,
) -> tuple[np.ndarray, int, float]:
    rhs = np.zeros(system.D.shape[0], dtype=complex)
    rhs[source_index] = 1.0
    return solve_vector_normal_eq_cached(system, rhs, rtol, maxiter)


def solve_propagator_normal_eq(D: sparse.csr_matrix, source_index: int, rtol: float, maxiter: int) -> tuple[np.ndarray, int, float]:
    rhs = np.zeros(D.shape[0], dtype=complex)
    rhs[source_index] = 1.0
    return solve_vector_normal_eq(D, rhs, rtol, maxiter)


def momentum_key(nvec: tuple[int, int, int]) -> str:
    return ",".join(str(n) for n in nvec)


def parse_momentum_modes(spec: str | None) -> list[tuple[int, int, int]]:
    if not spec:
        return []
    modes: list[tuple[int, int, int]] = []
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        vals = [int(x) for x in part.split(",")]
        if len(vals) != 3:
            raise ValueError(f"momentum mode must have three integer components: {part!r}")
        modes.append((vals[0], vals[1], vals[2]))
    return modes


def parse_float_list(spec: str | None) -> list[float]:
    if not spec:
        return []
    return [float(x) for x in spec.split(",") if x.strip()]


def spatial_p_hat_sq(nvec: tuple[int, int, int], spatial_l: int) -> float:
    return sum((2.0 * math.sin(math.pi * n / spatial_l)) ** 2 for n in nvec)


def phase_vector(geom: Geometry, nvec: tuple[int, int, int]) -> np.ndarray:
    phases = np.empty(geom.volume * NC, dtype=np.complex128)
    for site in range(geom.volume):
        _t, x, y, z = geom.site_coords(site)
        phase_arg = (nvec[0] * x + nvec[1] * y + nvec[2] * z) / geom.spatial_l
        phase = np.exp(2.0j * math.pi * phase_arg)
        for color in range(NC):
            phases[site * NC + color] = phase
    return phases


def time_projector_vector(geom: Geometry, time_index: int) -> np.ndarray:
    mask = np.zeros(geom.volume * NC, dtype=np.complex128)
    target = int(time_index) % geom.time_l
    for site in range(geom.volume):
        t, _x, _y, _z = geom.site_coords(site)
        if t == target:
            for color in range(NC):
                mask[site * NC + color] = 1.0 + 0.0j
    return mask


def load_source_higgs_operator_certificate(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"source-Higgs operator certificate not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"source-Higgs operator certificate must be a JSON object: {path}")
    return data


def source_higgs_operator_summary(cert: dict[str, Any], cert_path: Path | None) -> dict[str, Any]:
    if not cert:
        return {
            "operator_id": None,
            "operator_definition": None,
            "identity_certificate": None,
            "normalization_certificate": None,
            "diagonal_vertex": None,
            "sparse_vertex": None,
            "canonical_higgs_operator_identity_passed": False,
            "hunit_used_as_operator": None,
            "static_ew_algebra_used_as_operator": None,
            "certificate_path": str(cert_path) if cert_path is not None else None,
        }
    return {
        "operator_id": cert.get("operator_id"),
        "operator_definition": cert.get("operator_definition"),
        "identity_certificate": cert.get("identity_certificate"),
        "normalization_certificate": cert.get("normalization_certificate"),
        "diagonal_vertex": cert.get("diagonal_vertex"),
        "sparse_vertex": cert.get("sparse_vertex"),
        "canonical_higgs_operator_identity_passed": cert.get("canonical_higgs_operator_identity_passed") is True,
        "hunit_used_as_operator": cert.get("hunit_used_as_operator"),
        "static_ew_algebra_used_as_operator": cert.get("static_ew_algebra_used_as_operator"),
        "certificate_path": str(cert_path) if cert_path is not None else None,
    }


def source_higgs_firewall_from_certificate(cert: dict[str, Any]) -> dict[str, Any]:
    firewall = cert.get("firewall", {}) if isinstance(cert.get("firewall", {}), dict) else {}
    return {
        "used_observed_targets_as_selectors": firewall.get("used_observed_targets_as_selectors"),
        "used_yt_ward_identity": firewall.get("used_yt_ward_identity"),
        "used_alpha_lm_or_plaquette": firewall.get("used_alpha_lm_or_plaquette"),
        "used_hunit_matrix_element_readout": firewall.get("used_hunit_matrix_element_readout"),
        "used_taste_radial_axis_as_canonical_oh": firewall.get("used_taste_radial_axis_as_canonical_oh"),
    }


def source_higgs_operator_is_taste_radial_second_source(cert: dict[str, Any]) -> bool:
    sparse_vertex = cert.get("sparse_vertex", {}) if isinstance(cert.get("sparse_vertex", {}), dict) else {}
    return (
        sparse_vertex.get("kind") == "taste_radial_spatial_hypercube_flip"
        and cert.get("canonical_higgs_operator_identity_passed") is not True
    )


def source_higgs_operator_weights(geom: Geometry, cert: dict[str, Any]) -> np.ndarray:
    vertex = cert.get("diagonal_vertex", {}) if isinstance(cert.get("diagonal_vertex", {}), dict) else {}
    kind = str(vertex.get("kind", ""))
    n = geom.volume * NC
    if kind == "site_color_diagonal_values":
        values = vertex.get("values")
        if not isinstance(values, list) or len(values) != n:
            raise ValueError(
                "source-Higgs site_color_diagonal_values vertex requires "
                f"{n} numeric values, one per site-color component"
            )
        weights = np.asarray([float(value) for value in values], dtype=np.float64)
    elif kind == "constant_site_color_diagonal":
        weights = np.full(n, float(vertex.get("constant", 1.0)), dtype=np.float64)
    elif kind == "staggered_parity_site_color_diagonal":
        weights = np.empty(n, dtype=np.float64)
        amplitude = float(vertex.get("amplitude", 1.0))
        for site in range(geom.volume):
            coords = geom.site_coords(site)
            parity = -1.0 if sum(coords) % 2 else 1.0
            for color in range(NC):
                weights[site * NC + color] = amplitude * parity
    else:
        raise ValueError(
            "source-Higgs operator certificate must specify diagonal_vertex.kind "
            "as one of: site_color_diagonal_values, constant_site_color_diagonal, "
            "staggered_parity_site_color_diagonal"
        )
    norm = float(np.linalg.norm(weights))
    if not math.isfinite(norm) or norm <= 1.0e-30:
        raise ValueError("source-Higgs operator vertex has zero/non-finite norm")
    return weights


def _source_higgs_sparse_direction(direction: Any) -> int:
    if isinstance(direction, str):
        mapping = {"x": 1, "y": 2, "z": 3, "1": 1, "2": 2, "3": 3}
        if direction not in mapping:
            raise ValueError(f"unknown taste-radial spatial direction: {direction!r}")
        return mapping[direction]
    mu = int(direction)
    if mu not in (1, 2, 3):
        raise ValueError(f"taste-radial hypercube flip directions must be spatial 1,2,3; got {direction!r}")
    return mu


def hypercube_flip_operator(gauge: GaugeField, spatial_mu: int) -> sparse.csr_matrix:
    """Gauge-covariant blocked-hypercube bit flip for one spatial taste axis."""

    geom = gauge.geom
    if geom.spatial_l % 2 != 0:
        raise ValueError("taste-radial hypercube flip source requires even spatial_l")
    if spatial_mu not in (1, 2, 3):
        raise ValueError("hypercube flip source only supports spatial directions 1,2,3")
    n = geom.volume * NC
    rows: list[int] = []
    cols: list[int] = []
    vals: list[complex] = []
    for site in range(geom.volume):
        coords = geom.site_coords(site)
        if coords[spatial_mu] % 2 == 0:
            target = geom.shifted(coords, spatial_mu, +1)
            link = gauge.u[coords][spatial_mu]
        else:
            target = geom.shifted(coords, spatial_mu, -1)
            link = gauge.u[target][spatial_mu].conj().T
        target_site = geom.site_index(target)
        for a in range(NC):
            row = site * NC + a
            for b in range(NC):
                rows.append(row)
                cols.append(target_site * NC + b)
                vals.append(link[a, b])
    return sparse.csr_matrix((vals, (rows, cols)), shape=(n, n), dtype=np.complex128)


def taste_radial_sparse_vertex(gauge: GaugeField, vertex: dict[str, Any]) -> sparse.csr_matrix:
    directions = [_source_higgs_sparse_direction(d) for d in vertex.get("directions", [1, 2, 3])]
    if not directions:
        raise ValueError("taste-radial sparse vertex requires at least one spatial direction")
    normalization = str(vertex.get("normalization", "source_norm_matched"))
    if normalization == "source_norm_matched":
        coefficient = 1.0 / math.sqrt(float(len(directions)))
    elif normalization == "hs_unit":
        coefficient = 1.0 / math.sqrt(float(len(directions) * gauge.geom.volume * NC))
    elif normalization == "none":
        coefficient = 1.0
    else:
        coefficient = float(vertex.get("coefficient", 1.0))
    pieces = [hypercube_flip_operator(gauge, mu) for mu in directions]
    out = pieces[0].copy()
    for piece in pieces[1:]:
        out = out + piece
    return (coefficient * out).tocsr()


def source_higgs_operator_matrix(
    geom: Geometry,
    gauge: GaugeField,
    cert: dict[str, Any],
) -> sparse.csr_matrix:
    sparse_vertex = cert.get("sparse_vertex", {}) if isinstance(cert.get("sparse_vertex", {}), dict) else {}
    kind = str(sparse_vertex.get("kind", ""))
    if kind == "taste_radial_spatial_hypercube_flip":
        return taste_radial_sparse_vertex(gauge, sparse_vertex)
    weights = source_higgs_operator_weights(geom, cert).astype(np.complex128)
    return sparse.diags(weights, offsets=0, shape=(weights.size, weights.size), format="csr")


def stochastic_scalar_two_point(
    gauge: GaugeField,
    mass: float,
    rtol: float,
    maxiter: int,
    modes: list[tuple[int, int, int]],
    noise_vectors: int,
    rng: np.random.Generator,
    normal_system: NormalEquationSystem | None = None,
) -> dict[str, Any]:
    system = normal_system if normal_system is not None else build_normal_equation_system(gauge, mass)
    geom = gauge.geom
    n = geom.volume * NC
    accum: dict[str, list[complex]] = {momentum_key(mode): [] for mode in modes}
    infos: list[int] = []
    residuals: list[float] = []
    phases = {momentum_key(mode): phase_vector(geom, mode) for mode in modes}
    for _noise in range(noise_vectors):
        real = 2 * rng.integers(0, 2, size=n) - 1
        imag = 2 * rng.integers(0, 2, size=n) - 1
        eta = (real + 1j * imag).astype(np.complex128) / math.sqrt(2.0)
        for mode in modes:
            key = momentum_key(mode)
            phase = phases[key]
            y, info_y, residual_y = solve_vector_normal_eq_cached(system, np.conj(phase) * eta, rtol, maxiter)
            x, info_x, residual_x = solve_vector_normal_eq_cached(system, phase * y, rtol, maxiter)
            accum[key].append(complex(np.vdot(eta, x) / n))
            infos.extend([info_y, info_x])
            residuals.extend([residual_y, residual_x])

    mode_rows = {}
    for mode in modes:
        key = momentum_key(mode)
        values = np.asarray(accum[key], dtype=np.complex128)
        mean = complex(np.mean(values)) if values.size else complex(float("nan"), float("nan"))
        stderr = float(np.std(values.real, ddof=1) / math.sqrt(values.size)) if values.size > 1 else 0.0
        noise_stability: dict[str, Any] = {
            "available": False,
            "reason": "fewer than two noise vectors",
        }
        if values.size >= 2:
            split = values.size // 2
            first_half = values[:split]
            second_half = values[split:]
            first_mean = complex(np.mean(first_half))
            second_mean = complex(np.mean(second_half))
            delta = first_mean - second_mean
            denom = stderr if stderr > 0.0 else float("nan")
            noise_stability = {
                "available": True,
                "first_half_noise_vectors": int(first_half.size),
                "second_half_noise_vectors": int(second_half.size),
                "C_ss_real_first_half": float(first_mean.real),
                "C_ss_real_second_half": float(second_mean.real),
                "C_ss_real_half_delta": float(delta.real),
                "C_ss_real_half_delta_over_stderr": (
                    float(abs(delta.real) / denom) if math.isfinite(denom) else float("nan")
                ),
                "C_ss_imag_first_half": float(first_mean.imag),
                "C_ss_imag_second_half": float(second_mean.imag),
                "C_ss_imag_half_delta": float(delta.imag),
            }
        gamma = 1.0 / mean if abs(mean) > 1.0e-30 else complex(float("nan"), float("nan"))
        mode_rows[key] = {
            "momentum_mode": list(mode),
            "p_hat_sq": spatial_p_hat_sq(mode, geom.spatial_l),
            "noise_vectors": int(noise_vectors),
            "C_ss_real": float(mean.real),
            "C_ss_imag": float(mean.imag),
            "C_ss_real_noise_stderr": stderr,
            "Gamma_ss_real": float(gamma.real),
            "Gamma_ss_imag": float(gamma.imag),
            "noise_subsample_stability": noise_stability,
        }
    return {
        "mass": mass,
        "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
        "estimator": "Z2 stochastic trace for Tr[S V_q S V_-q] normalized by volume*colors",
        "mode_rows": mode_rows,
        "cg_infos": infos,
        "cg_residuals": residuals,
        "max_cg_residual": max(residuals) if residuals else None,
    }


def stochastic_source_higgs_cross_correlator(
    gauge: GaugeField,
    mass: float,
    rtol: float,
    maxiter: int,
    modes: list[tuple[int, int, int]],
    noise_vectors: int,
    rng: np.random.Generator,
    operator_certificate: dict[str, Any],
    operator_certificate_path: Path | None,
    normal_system: NormalEquationSystem | None = None,
) -> dict[str, Any]:
    """Estimate source/source-operator stochastic trace rows.

    This is an instrumentation path only.  It accepts an external
    same-surface operator certificate and measures the corresponding
    source/operator stochastic traces.  The certificate, not this estimator,
    carries the burden of proving that the vertex is canonical O_H.  If the
    operator is the PR230 taste-radial second source rather than canonical O_H,
    downstream analysis emits C_sx/C_xx aliases while preserving the legacy
    C_sH/C_HH schema fields.
    """
    system = normal_system if normal_system is not None else build_normal_equation_system(gauge, mass)
    geom = gauge.geom
    n = geom.volume * NC
    h_operator = source_higgs_operator_matrix(geom, gauge, operator_certificate).astype(np.complex128)
    one_operator = sparse.identity(n, dtype=np.complex128, format="csr")
    phases = {momentum_key(mode): phase_vector(geom, mode) for mode in modes}
    accum: dict[str, dict[str, list[complex]]] = {
        momentum_key(mode): {"C_ss": [], "C_sH": [], "C_HH": []} for mode in modes
    }
    infos: list[int] = []
    residuals: list[float] = []

    def estimate_pair(
        eta: np.ndarray,
        phase: np.ndarray,
        left_operator: sparse.csr_matrix,
        right_operator: sparse.csr_matrix,
    ) -> tuple[complex, list[int], list[float]]:
        right = np.conj(phase) * (right_operator @ eta)
        y, info_y, residual_y = solve_vector_normal_eq_cached(system, right, rtol, maxiter)
        left = phase * (left_operator @ y)
        x, info_x, residual_x = solve_vector_normal_eq_cached(system, left, rtol, maxiter)
        return complex(np.vdot(eta, x) / n), [info_y, info_x], [residual_y, residual_x]

    for _noise in range(noise_vectors):
        real = 2 * rng.integers(0, 2, size=n) - 1
        imag = 2 * rng.integers(0, 2, size=n) - 1
        eta = (real + 1j * imag).astype(np.complex128) / math.sqrt(2.0)
        for mode in modes:
            key = momentum_key(mode)
            phase = phases[key]
            c_ss, info_ss, residual_ss = estimate_pair(eta, phase, one_operator, one_operator)
            c_sh, info_sh, residual_sh = estimate_pair(eta, phase, one_operator, h_operator)
            c_hh, info_hh, residual_hh = estimate_pair(eta, phase, h_operator, h_operator)
            accum[key]["C_ss"].append(c_ss)
            accum[key]["C_sH"].append(c_sh)
            accum[key]["C_HH"].append(c_hh)
            infos.extend(info_ss + info_sh + info_hh)
            residuals.extend(residual_ss + residual_sh + residual_hh)

    mode_rows = {}
    for mode in modes:
        key = momentum_key(mode)
        row: dict[str, Any] = {
            "momentum_mode": list(mode),
            "p_hat_sq": spatial_p_hat_sq(mode, geom.spatial_l),
            "noise_vectors": int(noise_vectors),
        }
        for label in ("C_ss", "C_sH", "C_HH"):
            values = np.asarray(accum[key][label], dtype=np.complex128)
            mean = complex(np.mean(values)) if values.size else complex(float("nan"), float("nan"))
            real_stderr = (
                float(np.std(values.real, ddof=1) / math.sqrt(values.size)) if values.size > 1 else 0.0
            )
            imag_stderr = (
                float(np.std(values.imag, ddof=1) / math.sqrt(values.size)) if values.size > 1 else 0.0
            )
            row[f"{label}_real"] = float(mean.real)
            row[f"{label}_imag"] = float(mean.imag)
            row[f"{label}_real_noise_stderr"] = real_stderr
            row[f"{label}_imag_noise_stderr"] = imag_stderr
        mode_rows[key] = row

    return {
        "mass": mass,
        "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
        "operator": source_higgs_operator_summary(operator_certificate, operator_certificate_path),
        "firewall": source_higgs_firewall_from_certificate(operator_certificate),
        "measurement_object": (
            "C_ss/C_sx/C_xx sparse taste-radial second-source stochastic traces on the same gauge ensemble"
            if source_higgs_operator_is_taste_radial_second_source(operator_certificate)
            else "C_ss/C_sH/C_HH operator stochastic traces on the same gauge ensemble"
        ),
        "estimator": "Z2 stochastic trace for Tr[S V_A(q) S V_B(-q)] normalized by volume*colors",
        "mode_rows": mode_rows,
        "cg_infos": infos,
        "cg_residuals": residuals,
        "max_cg_residual": max(residuals) if residuals else None,
        "strict_limit": (
            "These are source/operator measurement rows only; they are not "
            "physical y_t evidence until isolated-pole, FV/IR, source-overlap "
            "or physical-response, and retained-route gates pass."
        ),
    }


def stochastic_source_higgs_time_kernel(
    gauge: GaugeField,
    mass: float,
    rtol: float,
    maxiter: int,
    modes: list[tuple[int, int, int]],
    noise_vectors: int,
    max_tau: int,
    origin_count: int,
    rng: np.random.Generator,
    operator_certificate: dict[str, Any],
    operator_certificate_path: Path | None,
    normal_system: NormalEquationSystem | None = None,
) -> dict[str, Any]:
    """Estimate same-surface scalar Euclidean-time matrix rows.

    This is default-off instrumentation for the OS transfer-kernel contract.
    It measures a source/operator 2x2 matrix between a source time slice t0
    and sink time slice t0+tau.  The supplied operator certificate still carries
    the burden of proving that the second operator is canonical O_H; taste-radial
    rows remain x rows and are aliased only for schema continuity.
    """

    system = normal_system if normal_system is not None else build_normal_equation_system(gauge, mass)
    geom = gauge.geom
    n = geom.volume * NC
    spatial_norm = geom.spatial_l**3 * NC
    h_operator = source_higgs_operator_matrix(geom, gauge, operator_certificate).astype(np.complex128)
    one_operator = sparse.identity(n, dtype=np.complex128, format="csr")
    operators = {
        "s": one_operator,
        "H": h_operator,
    }
    phases = {momentum_key(mode): phase_vector(geom, mode) for mode in modes}
    origins = [int(t0 % geom.time_l) for t0 in range(max(1, min(origin_count, geom.time_l)))]
    tau_values = [int(tau) for tau in range(0, max(0, int(max_tau)) + 1)]
    accum: dict[str, dict[int, dict[str, list[complex]]]] = {
        momentum_key(mode): {
            tau: {"C_ss": [], "C_sH": [], "C_Hs": [], "C_HH": []}
            for tau in tau_values
        }
        for mode in modes
    }
    infos: list[int] = []
    residuals: list[float] = []

    def estimate_pair(
        eta: np.ndarray,
        source_slice: np.ndarray,
        sink_slice: np.ndarray,
        phase: np.ndarray,
        sink_operator: sparse.csr_matrix,
        source_operator: sparse.csr_matrix,
    ) -> tuple[complex, list[int], list[float]]:
        right = source_slice * np.conj(phase) * (source_operator @ eta)
        y, info_y, residual_y = solve_vector_normal_eq_cached(system, right, rtol, maxiter)
        left = sink_slice * phase * (sink_operator @ y)
        x, info_x, residual_x = solve_vector_normal_eq_cached(system, left, rtol, maxiter)
        return complex(np.vdot(eta, x) / spatial_norm), [info_y, info_x], [residual_y, residual_x]

    for _noise in range(noise_vectors):
        real = 2 * rng.integers(0, 2, size=n) - 1
        imag = 2 * rng.integers(0, 2, size=n) - 1
        eta = (real + 1j * imag).astype(np.complex128) / math.sqrt(2.0)
        for mode in modes:
            key = momentum_key(mode)
            phase = phases[key]
            for origin in origins:
                source_slice = time_projector_vector(geom, origin)
                for tau in tau_values:
                    sink_slice = time_projector_vector(geom, origin + tau)
                    for sink_label, source_label, out_label in (
                        ("s", "s", "C_ss"),
                        ("s", "H", "C_sH"),
                        ("H", "s", "C_Hs"),
                        ("H", "H", "C_HH"),
                    ):
                        value, info, residual = estimate_pair(
                            eta,
                            source_slice,
                            sink_slice,
                            phase,
                            operators[sink_label],
                            operators[source_label],
                        )
                        accum[key][tau][out_label].append(value)
                        infos.extend(info)
                        residuals.extend(residual)

    mode_rows: dict[str, Any] = {}
    for mode in modes:
        key = momentum_key(mode)
        tau_rows = []
        for tau in tau_values:
            row: dict[str, Any] = {
                "tau": int(tau),
                "source_time_origins": origins,
                "noise_vectors": int(noise_vectors),
            }
            for label in ("C_ss", "C_sH", "C_Hs", "C_HH"):
                values = np.asarray(accum[key][tau][label], dtype=np.complex128)
                mean = complex(np.mean(values)) if values.size else complex(float("nan"), float("nan"))
                real_stderr = (
                    float(np.std(values.real, ddof=1) / math.sqrt(values.size))
                    if values.size > 1
                    else 0.0
                )
                imag_stderr = (
                    float(np.std(values.imag, ddof=1) / math.sqrt(values.size))
                    if values.size > 1
                    else 0.0
                )
                row[f"{label}_real"] = float(mean.real)
                row[f"{label}_imag"] = float(mean.imag)
                row[f"{label}_real_stochastic_stderr"] = real_stderr
                row[f"{label}_imag_stochastic_stderr"] = imag_stderr
            tau_rows.append(row)
        mode_rows[key] = {
            "momentum_mode": list(mode),
            "p_hat_sq": spatial_p_hat_sq(mode, geom.spatial_l),
            "tau_rows": tau_rows,
        }

    return {
        "mass": mass,
        "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
        "operator": source_higgs_operator_summary(operator_certificate, operator_certificate_path),
        "firewall": source_higgs_firewall_from_certificate(operator_certificate),
        "measurement_object": (
            "same-surface Euclidean-time C_ss/C_sx/C_xs/C_xx(t) rows for the supplied taste-radial second-source certificate"
            if source_higgs_operator_is_taste_radial_second_source(operator_certificate)
            else "same-surface Euclidean-time C_ss/C_sH/C_Hs/C_HH(t) rows for a supplied canonical-Higgs operator certificate"
        ),
        "estimator": "Z2 stochastic trace for Tr[S P_sink(t0+tau) V_A(q) S P_source(t0) V_B(-q)] normalized by spatial_volume*colors",
        "time_kernel_schema_version": "source_higgs_time_kernel_v1",
        "time_origins": origins,
        "tau_values": tau_values,
        "mode_rows": mode_rows,
        "cg_infos": infos,
        "cg_residuals": residuals,
        "max_cg_residual": max(residuals) if residuals else None,
        "strict_limit": (
            "These are scalar time-kernel instrumentation rows only.  They are "
            "not physical y_t evidence until canonical O_H or physical neutral "
            "transfer identity, pole/FV/IR/threshold, source-overlap, and "
            "retained-route gates pass."
        ),
    }


def measure_correlator(
    gauge: GaugeField,
    mass: float,
    rtol: float,
    maxiter: int,
    momentum_modes: list[tuple[int, int, int]] | None = None,
    normal_system: NormalEquationSystem | None = None,
) -> dict[str, Any]:
    system = normal_system if normal_system is not None else build_normal_equation_system(gauge, mass)
    geom = gauge.geom
    corr = np.zeros(geom.time_l, dtype=float)
    momentum_corrs = {
        momentum_key(nvec): np.zeros(geom.time_l, dtype=float)
        for nvec in (momentum_modes or [])
    }
    infos: list[int] = []
    residuals: list[float] = []
    source_site = geom.site_index((0, 0, 0, 0))
    for source_color in range(NC):
        source_index = source_site * NC + source_color
        sol, info, residual = solve_propagator_normal_eq_cached(system, source_index, rtol, maxiter)
        infos.append(info)
        residuals.append(residual)
        for site in range(geom.volume):
            t, x, y, z = geom.site_coords(site)
            block = sol[site * NC:(site + 1) * NC]
            density = float(np.vdot(block, block).real)
            corr[t] += density
            for nvec in (momentum_modes or []):
                phase_arg = (nvec[0] * x + nvec[1] * y + nvec[2] * z) / geom.spatial_l
                momentum_corrs[momentum_key(nvec)][t] += math.cos(2.0 * math.pi * phase_arg) * density
    corr /= NC
    for key in momentum_corrs:
        momentum_corrs[key] /= NC
    return {
        "mass": mass,
        "correlator": corr.tolist(),
        "momentum_correlators": {key: value.tolist() for key, value in momentum_corrs.items()},
        "cg_infos": infos,
        "cg_residuals": residuals,
        "max_cg_residual": max(residuals) if residuals else None,
    }


def jackknife_mean_err(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = values.shape[0]
    mean = np.mean(values, axis=0)
    if n <= 1:
        return mean, np.zeros_like(mean)
    jk = np.array([(np.sum(values, axis=0) - values[i]) / (n - 1) for i in range(n)])
    err = np.sqrt((n - 1) * np.mean((jk - np.mean(jk, axis=0)) ** 2, axis=0))
    return mean, err


def fit_mass(corr: np.ndarray, err: np.ndarray) -> dict[str, Any]:
    max_tau = max(2, len(corr) // 2)
    taus = np.arange(1, max_tau + 1)
    means = corr[1:max_tau + 1]
    sig = np.maximum(err[1:max_tau + 1], 1.0e-10)
    best: dict[str, Any] | None = None
    for tau_min in range(1, max(2, max_tau - 1)):
        tau_max = max_tau
        mask = (taus >= tau_min) & (means > 0.0)
        if int(np.sum(mask)) < 2:
            continue
        x = taus[mask].astype(float)
        y = np.log(means[mask])
        yerr = sig[mask] / means[mask]
        w = 1.0 / np.maximum(yerr * yerr, 1.0e-12)
        design = np.vstack([np.ones_like(x), -x]).T
        normal = design.T @ (w[:, None] * design)
        rhs = design.T @ (w * y)
        cov = np.linalg.pinv(normal)
        coeff = cov @ rhs
        residual = y - design @ coeff
        dof = max(1, len(y) - 2)
        chi2 = float(np.sum(w * residual * residual) / dof)
        candidate = {
            "tau_min": int(tau_min),
            "tau_max": int(tau_max),
            "m_lat": float(coeff[1]),
            "m_lat_err": float(math.sqrt(max(cov[1, 1], 0.0))),
            "chi2_dof": chi2,
        }
        if best is None or abs(candidate["chi2_dof"] - 1.0) < abs(best["chi2_dof"] - 1.0):
            best = candidate
    if best is None:
        return {"tau_min": 1, "tau_max": max_tau, "m_lat": float("nan"), "m_lat_err": float("nan"), "chi2_dof": float("nan")}
    return best


def effective_mass(corr: np.ndarray) -> list[dict[str, float]]:
    rows = []
    for tau in range(len(corr) - 1):
        if corr[tau] > 0.0 and corr[tau + 1] > 0.0:
            rows.append({"tau": tau, "m_eff": float(math.log(corr[tau] / corr[tau + 1]))})
    return rows


def fit_energy_from_effective(corr: np.ndarray) -> dict[str, Any]:
    estimates = []
    max_tau = min(3, len(corr) - 2)
    for tau in range(1, max_tau + 1):
        if corr[tau] > 0.0 and corr[tau + 1] > 0.0:
            estimates.append((tau, math.log(corr[tau] / corr[tau + 1])))
    if not estimates:
        return {
            "tau_min": 1,
            "tau_max": max_tau,
            "m_lat": float("nan"),
            "m_lat_err": float("nan"),
            "chi2_dof": float("nan"),
            "effective_energy_samples": [],
        }
    values = np.asarray([value for _tau, value in estimates], dtype=float)
    err = float(np.std(values, ddof=1) / math.sqrt(len(values))) if len(values) > 1 else 0.0
    return {
        "tau_min": int(estimates[0][0]),
        "tau_max": int(estimates[-1][0] + 1),
        "m_lat": float(np.mean(values)),
        "m_lat_err": err,
        "chi2_dof": 0.0 if len(values) <= 1 else float(np.var(values, ddof=1)),
        "effective_energy_samples": [
            {"tau": int(tau), "m_eff": float(value)} for tau, value in estimates
        ],
    }


def fit_first_positive_effective(corr: np.ndarray) -> dict[str, Any]:
    for tau in range(len(corr) - 1):
        if corr[tau] > 0.0 and corr[tau + 1] > 0.0:
            value = math.log(corr[tau] / corr[tau + 1])
            return {
                "tau_min": int(tau),
                "tau_max": int(tau + 1),
                "m_lat": float(value),
                "m_lat_err": 0.0,
                "chi2_dof": 0.0,
                "effective_energy_samples": [{"tau": int(tau), "m_eff": float(value)}],
            }
    return {
        "tau_min": 0,
        "tau_max": max(0, len(corr) - 1),
        "m_lat": float("nan"),
        "m_lat_err": float("nan"),
        "chi2_dof": float("nan"),
        "effective_energy_samples": [],
    }


def fit_momentum_energies(
    momentum_measurements: dict[str, list[list[float]]],
    spatial_l: int,
) -> dict[str, Any]:
    energy_fits = {}
    for key, rows in momentum_measurements.items():
        arr = np.asarray(rows, dtype=float)
        mean, err = jackknife_mean_err(arr)
        fit = fit_energy_from_effective(mean)
        nvec = tuple(int(x) for x in key.split(","))
        energy_fits[key] = {
            "momentum_mode": list(nvec),
            "p_hat_sq": spatial_p_hat_sq(nvec, spatial_l),
            "energy_lat": fit["m_lat"],
            "energy_lat_err": fit["m_lat_err"],
            "chi2_dof": fit["chi2_dof"],
            "tau_min": fit["tau_min"],
            "tau_max": fit["tau_max"],
            "effective_energy_samples": fit["effective_energy_samples"],
            "correlator": [
                {"tau": tau, "mean": float(c), "stderr": float(e)}
                for tau, (c, e) in enumerate(zip(mean, err))
            ],
        }

    zero = energy_fits.get("0,0,0")
    kinetic_fits = {}
    if zero is not None and math.isfinite(float(zero["energy_lat"])):
        e0 = float(zero["energy_lat"])
        e0_err = float(zero.get("energy_lat_err", 0.0) or 0.0)
        for key, fit in energy_fits.items():
            if key == "0,0,0":
                continue
            energy = float(fit["energy_lat"])
            delta_e = energy - e0
            if delta_e > 0.0:
                p2 = float(fit["p_hat_sq"])
                m_kin = p2 / (2.0 * delta_e)
                de_err = math.sqrt(e0_err * e0_err + float(fit.get("energy_lat_err", 0.0) or 0.0) ** 2)
                m_kin_err = abs(m_kin) * de_err / delta_e if delta_e > 0.0 else float("nan")
            else:
                m_kin = float("nan")
                m_kin_err = float("nan")
                de_err = float("nan")
            kinetic_fits[key] = {
                "momentum_mode": fit["momentum_mode"],
                "delta_e_lat": delta_e,
                "delta_e_lat_err": de_err,
                "m_kin_lat": m_kin,
                "m_kin_lat_err": m_kin_err,
            }
    return {"energy_fits": energy_fits, "kinetic_mass_fits": kinetic_fits}


def fit_scalar_source_response(
    source_measurements: dict[float, list[list[float]]],
    base_mass: float,
) -> dict[str, Any]:
    energy_fits = []
    for source_shift, rows in sorted(source_measurements.items()):
        arr = np.asarray(rows, dtype=float)
        if arr.size == 0:
            continue
        mean, err = jackknife_mean_err(arr)
        fit = fit_mass(mean, err)
        if not math.isfinite(float(fit.get("m_lat", float("nan")))):
            fit = fit_energy_from_effective(mean)
        if not math.isfinite(float(fit.get("m_lat", float("nan")))):
            fit = fit_first_positive_effective(mean)
        energy_fits.append(
            {
                "source_shift_lat": float(source_shift),
                "effective_bare_mass_lat": float(base_mass + source_shift),
                "energy_lat": fit["m_lat"],
                "energy_lat_err": fit["m_lat_err"],
                "chi2_dof": fit["chi2_dof"],
                "tau_min": fit["tau_min"],
                "tau_max": fit["tau_max"],
                "correlator": [
                    {"tau": tau, "mean": float(c), "stderr": float(e)}
                    for tau, (c, e) in enumerate(zip(mean, err))
                ],
            }
        )

    finite = [
        row
        for row in energy_fits
        if math.isfinite(float(row["source_shift_lat"]))
        and math.isfinite(float(row["energy_lat"]))
    ]
    slope = float("nan")
    slope_err = float("nan")
    fit_kind = "unavailable"
    if len(finite) >= 2:
        shifts = np.asarray([row["source_shift_lat"] for row in finite], dtype=float)
        energies = np.asarray([row["energy_lat"] for row in finite], dtype=float)
        weights = []
        for row in finite:
            err = float(row.get("energy_lat_err", 0.0) or 0.0)
            weights.append(1.0 / max(err * err, 1.0e-12))
        coeffs, cov = np.polyfit(shifts, energies, deg=1, w=np.sqrt(weights), cov="unscaled")
        slope = float(coeffs[0])
        slope_err = float(math.sqrt(max(cov[0, 0], 0.0))) if cov.shape == (2, 2) else float("nan")
        fit_kind = "linear_dE_ds"

    def effective_energy_at_tau(corr: list[float], tau: int) -> float:
        if tau < 0 or len(corr) <= tau + 1:
            return float("nan")
        c0 = float(corr[tau])
        c1 = float(corr[tau + 1])
        if c0 <= 0.0 or c1 <= 0.0:
            return float("nan")
        return float(math.log(c0 / c1))

    common_count = min((len(rows) for rows in source_measurements.values()), default=0)
    source_keys = sorted(source_measurements)
    nonzero_radii = sorted({round(abs(float(s)), 12) for s in source_keys if abs(float(s)) > 1.0e-15})
    max_tau = -1
    if common_count > 0 and source_keys:
        min_corr_len = min(
            len(source_measurements[source_shift][cfg_index])
            for source_shift in source_keys
            for cfg_index in range(common_count)
        )
        max_tau = max(min_corr_len - 2, -1)
    tau_windows = list(range(max_tau + 1))
    per_configuration_effective_energies = []
    per_configuration_slopes = []
    per_configuration_multi_tau_effective_energies = []
    per_configuration_multi_tau_slopes = []
    for cfg_index in range(common_count):
        energies_by_shift = {}
        for source_shift in source_keys:
            rows = source_measurements[source_shift]
            energy = effective_energy_at_tau(rows[cfg_index], 1)
            energies_by_shift[f"{float(source_shift):.12g}"] = energy
        per_configuration_effective_energies.append(
            {
                "configuration_index": cfg_index,
                "effective_energy_tau1_by_source_shift": energies_by_shift,
            }
        )
        multi_tau_energies_by_tau: dict[str, dict[str, float]] = {}
        for tau in tau_windows:
            tau_energies_by_shift = {}
            for source_shift in source_keys:
                rows = source_measurements[source_shift]
                energy = effective_energy_at_tau(rows[cfg_index], tau)
                tau_energies_by_shift[f"{float(source_shift):.12g}"] = energy
            multi_tau_energies_by_tau[str(tau)] = tau_energies_by_shift
        per_configuration_multi_tau_effective_energies.append(
            {
                "configuration_index": cfg_index,
                "tau_min": int(tau_windows[0]) if tau_windows else None,
                "tau_max": int(tau_windows[-1]) if tau_windows else None,
                "effective_energy_by_tau_and_source_shift": multi_tau_energies_by_tau,
            }
        )
        for radius in nonzero_radii:
            plus = energies_by_shift.get(f"{radius:.12g}")
            minus = energies_by_shift.get(f"{-radius:.12g}")
            if isinstance(plus, float) and isinstance(minus, float):
                slope_value = float((plus - minus) / (2.0 * radius)) if math.isfinite(plus) and math.isfinite(minus) else float("nan")
                per_configuration_slopes.append(
                    {
                        "configuration_index": cfg_index,
                        "source_radius": float(radius),
                        "slope_effective_energy_tau1": slope_value,
                        "finite": math.isfinite(slope_value),
                    }
                )
            multi_tau_slopes: dict[str, float] = {}
            for tau in tau_windows:
                tau_energies = multi_tau_energies_by_tau.get(str(tau), {})
                tau_plus = tau_energies.get(f"{radius:.12g}")
                tau_minus = tau_energies.get(f"{-radius:.12g}")
                if isinstance(tau_plus, float) and isinstance(tau_minus, float):
                    tau_slope = (
                        float((tau_plus - tau_minus) / (2.0 * radius))
                        if math.isfinite(tau_plus) and math.isfinite(tau_minus)
                        else float("nan")
                    )
                    multi_tau_slopes[str(tau)] = tau_slope
            per_configuration_multi_tau_slopes.append(
                {
                    "configuration_index": cfg_index,
                    "source_radius": float(radius),
                    "tau_min": int(tau_windows[0]) if tau_windows else None,
                    "tau_max": int(tau_windows[-1]) if tau_windows else None,
                    "slope_effective_energy_by_tau": multi_tau_slopes,
                    "finite_tau_count": sum(
                        1 for value in multi_tau_slopes.values() if math.isfinite(float(value))
                    ),
                }
            )

    return {
        "source_coordinate": "uniform additive lattice scalar source s entering the Dirac mass as m_bare + s",
        "base_bare_mass_lat": float(base_mass),
        "physical_higgs_normalization": "not_derived",
        "used_as_physical_yukawa_readout": False,
        "energy_fits": energy_fits,
        "slope_dE_ds_lat": slope,
        "slope_dE_ds_lat_err": slope_err,
        "fit_kind": fit_kind,
        "target_timeseries_schema_version": "fh_lsz_target_timeseries_v2_multitau",
        "target_timeseries_rule": (
            "diagnostic per-configuration tau=1 effective-energy slopes for "
            "autocorrelation/ESS gates; not a physical dE/dh readout"
        ),
        "multi_tau_target_timeseries_rule": (
            "diagnostic per-configuration adjacent-time effective-energy slopes "
            "for response-window covariance gates; not a readout switch and not "
            "a physical dE/dh observable"
        ),
        "multi_tau_window_range": {
            "tau_min": int(tau_windows[0]) if tau_windows else None,
            "tau_max": int(tau_windows[-1]) if tau_windows else None,
            "tau_windows": [int(tau) for tau in tau_windows],
        },
        "per_configuration_effective_energies": per_configuration_effective_energies,
        "per_configuration_slopes": per_configuration_slopes,
        "per_configuration_multi_tau_effective_energies": per_configuration_multi_tau_effective_energies,
        "per_configuration_multi_tau_slopes": per_configuration_multi_tau_slopes,
        "strict_limit": "dE/ds is not dE/dh until kappa_s is derived by scalar LSZ/canonical normalization",
    }


def fit_top_mass_scan_response(
    measurements: dict[float, list[list[float]]],
    selected_mass: float,
) -> dict[str, Any]:
    def effective_energy_at_tau(corr: list[float], tau: int) -> float:
        if tau < 0 or len(corr) <= tau + 1:
            return float("nan")
        c0 = float(corr[tau])
        c1 = float(corr[tau + 1])
        if c0 <= 0.0 or c1 <= 0.0:
            return float("nan")
        return float(math.log(c0 / c1))

    masses = sorted(float(mass) for mass in measurements)
    bracket_masses = []
    if len(masses) >= 2:
        lower = [mass for mass in masses if mass < float(selected_mass)]
        upper = [mass for mass in masses if mass > float(selected_mass)]
        if lower and upper:
            bracket_masses = [float(lower[-1]), float(selected_mass), float(upper[0])]
        else:
            bracket_masses = [float(masses[0]), float(masses[-1])]

    common_count = min((len(rows) for rows in measurements.values()), default=0)
    max_tau = -1
    if common_count > 0 and masses:
        min_corr_len = min(
            len(measurements[mass][cfg_index])
            for mass in masses
            for cfg_index in range(common_count)
        )
        max_tau = max(min_corr_len - 2, -1)
    tau_windows = list(range(max_tau + 1))
    per_configuration_effective_energies = []
    per_configuration_slopes = []
    per_configuration_multi_tau_effective_energies = []
    per_configuration_multi_tau_slopes = []
    finite_tau1_slope_count = 0
    finite_multi_tau_slope_count = 0

    low_mass = float(bracket_masses[0]) if len(bracket_masses) >= 2 else float("nan")
    high_mass = float(bracket_masses[-1]) if len(bracket_masses) >= 2 else float("nan")
    mass_delta = high_mass - low_mass if math.isfinite(low_mass) and math.isfinite(high_mass) else float("nan")

    for cfg_index in range(common_count):
        energies_by_mass: dict[str, float] = {}
        for mass in masses:
            energy = effective_energy_at_tau(measurements[mass][cfg_index], 1)
            energies_by_mass[f"{float(mass):.12g}"] = energy
        per_configuration_effective_energies.append(
            {
                "configuration_index": cfg_index,
                "effective_energy_tau1_by_mass": energies_by_mass,
            }
        )

        slope_value = float("nan")
        if len(bracket_masses) >= 2 and math.isfinite(mass_delta) and abs(mass_delta) > 1.0e-15:
            e_low = energies_by_mass.get(f"{low_mass:.12g}", float("nan"))
            e_high = energies_by_mass.get(f"{high_mass:.12g}", float("nan"))
            if math.isfinite(float(e_low)) and math.isfinite(float(e_high)):
                slope_value = float((float(e_high) - float(e_low)) / mass_delta)
        if math.isfinite(slope_value):
            finite_tau1_slope_count += 1
        per_configuration_slopes.append(
            {
                "configuration_index": cfg_index,
                "bracket_masses_lat": bracket_masses,
                "selected_mass_parameter": float(selected_mass),
                "slope_dE_dm_bare_tau1": slope_value,
                "finite": math.isfinite(slope_value),
            }
        )

        multi_tau_energies_by_tau: dict[str, dict[str, float]] = {}
        multi_tau_slopes: dict[str, float] = {}
        for tau in tau_windows:
            tau_energies_by_mass = {}
            for mass in masses:
                energy = effective_energy_at_tau(measurements[mass][cfg_index], tau)
                tau_energies_by_mass[f"{float(mass):.12g}"] = energy
            multi_tau_energies_by_tau[str(tau)] = tau_energies_by_mass

            tau_slope = float("nan")
            if len(bracket_masses) >= 2 and math.isfinite(mass_delta) and abs(mass_delta) > 1.0e-15:
                tau_low = tau_energies_by_mass.get(f"{low_mass:.12g}", float("nan"))
                tau_high = tau_energies_by_mass.get(f"{high_mass:.12g}", float("nan"))
                if math.isfinite(float(tau_low)) and math.isfinite(float(tau_high)):
                    tau_slope = float((float(tau_high) - float(tau_low)) / mass_delta)
            multi_tau_slopes[str(tau)] = tau_slope
            if math.isfinite(tau_slope):
                finite_multi_tau_slope_count += 1

        per_configuration_multi_tau_effective_energies.append(
            {
                "configuration_index": cfg_index,
                "tau_min": int(tau_windows[0]) if tau_windows else None,
                "tau_max": int(tau_windows[-1]) if tau_windows else None,
                "effective_energy_by_tau_and_mass": multi_tau_energies_by_tau,
            }
        )
        per_configuration_multi_tau_slopes.append(
            {
                "configuration_index": cfg_index,
                "bracket_masses_lat": bracket_masses,
                "selected_mass_parameter": float(selected_mass),
                "tau_min": int(tau_windows[0]) if tau_windows else None,
                "tau_max": int(tau_windows[-1]) if tau_windows else None,
                "slope_dE_dm_bare_by_tau": multi_tau_slopes,
                "finite_tau_count": sum(
                    1 for value in multi_tau_slopes.values() if math.isfinite(float(value))
                ),
            }
        )

    return {
        "row_schema_version": "top_mass_scan_response_v1",
        "source_coordinate": "uniform additive Dirac bare mass m_bare",
        "selected_mass_parameter": float(selected_mass),
        "mass_scan_masses_lat": masses,
        "mass_scan_bracket_masses_lat": bracket_masses,
        "configuration_count": int(common_count),
        "finite_tau1_slope_count": int(finite_tau1_slope_count),
        "finite_multi_tau_slope_count": int(finite_multi_tau_slope_count),
        "multi_tau_window_range": {
            "tau_min": int(tau_windows[0]) if tau_windows else None,
            "tau_max": int(tau_windows[-1]) if tau_windows else None,
            "tau_windows": [int(tau) for tau in tau_windows],
        },
        "per_configuration_effective_energies": per_configuration_effective_energies,
        "per_configuration_slopes": per_configuration_slopes,
        "per_configuration_multi_tau_effective_energies": per_configuration_multi_tau_effective_energies,
        "per_configuration_multi_tau_slopes": per_configuration_multi_tau_slopes,
        "used_as_physical_yukawa_readout": False,
        "physical_higgs_normalization": "not_derived",
        "strict_limit": (
            "Per-configuration top mass-scan slopes are same-ensemble response "
            "support for future covariance/subtraction gates only. They are "
            "not dE/dh, not kappa_s, and not physical y_t evidence without "
            "canonical-Higgs/source-overlap or W/Z response identity authority."
        ),
    }


def fit_scalar_two_point_lsz(
    scalar_two_point_measurements: dict[str, list[dict[str, Any]]],
    spatial_l: int,
) -> dict[str, Any]:
    mode_rows = {}
    for key, rows in scalar_two_point_measurements.items():
        if not rows:
            continue
        real_values = np.asarray([float(row["C_ss_real"]) for row in rows], dtype=float)
        imag_values = np.asarray([float(row["C_ss_imag"]) for row in rows], dtype=float)
        noise_stderr_values = [
            float(row.get("C_ss_real_noise_stderr", float("nan")))
            for row in rows
            if math.isfinite(float(row.get("C_ss_real_noise_stderr", float("nan"))))
        ]
        noise_counts = [
            int(row.get("noise_vectors", 0))
            for row in rows
            if int(row.get("noise_vectors", 0)) > 0
        ]
        half_delta_over_stderr = [
            float(row.get("noise_subsample_stability", {}).get("C_ss_real_half_delta_over_stderr", float("nan")))
            for row in rows
            if math.isfinite(
                float(row.get("noise_subsample_stability", {}).get("C_ss_real_half_delta_over_stderr", float("nan")))
            )
        ]
        c_mean = complex(float(np.mean(real_values)), float(np.mean(imag_values)))
        real_err = float(np.std(real_values, ddof=1) / math.sqrt(len(real_values))) if len(real_values) > 1 else 0.0
        imag_err = float(np.std(imag_values, ddof=1) / math.sqrt(len(imag_values))) if len(imag_values) > 1 else 0.0
        gamma = 1.0 / c_mean if abs(c_mean) > 1.0e-30 else complex(float("nan"), float("nan"))
        c_ss_timeseries = []
        for cfg_index, row in enumerate(rows):
            c_cfg = complex(float(row["C_ss_real"]), float(row["C_ss_imag"]))
            gamma_cfg = 1.0 / c_cfg if abs(c_cfg) > 1.0e-30 else complex(float("nan"), float("nan"))
            c_ss_timeseries.append(
                {
                    "configuration_index": cfg_index,
                    "C_ss_real": float(c_cfg.real),
                    "C_ss_imag": float(c_cfg.imag),
                    "Gamma_ss_real": float(gamma_cfg.real),
                    "Gamma_ss_imag": float(gamma_cfg.imag),
                }
            )
        nvec = tuple(int(x) for x in key.split(","))
        noise_subsample_stability = {
            "available": bool(half_delta_over_stderr),
            "configuration_count": len(rows),
            "noise_vectors_per_configuration": int(min(noise_counts)) if noise_counts else 0,
            "C_ss_real_noise_stderr_mean": (
                float(np.mean(noise_stderr_values)) if noise_stderr_values else float("nan")
            ),
            "C_ss_real_noise_stderr_max": (
                float(np.max(noise_stderr_values)) if noise_stderr_values else float("nan")
            ),
            "C_ss_real_half_delta_over_stderr_max": (
                float(np.max(half_delta_over_stderr)) if half_delta_over_stderr else float("nan")
            ),
        }
        mode_rows[key] = {
            "momentum_mode": list(nvec),
            "p_hat_sq": spatial_p_hat_sq(nvec, spatial_l),
            "configuration_count": len(rows),
            "C_ss_real": float(c_mean.real),
            "C_ss_imag": float(c_mean.imag),
            "C_ss_real_config_stderr": real_err,
            "C_ss_imag_config_stderr": imag_err,
            "Gamma_ss_real": float(gamma.real),
            "Gamma_ss_imag": float(gamma.imag),
            "C_ss_timeseries": c_ss_timeseries,
            "noise_subsample_stability": noise_subsample_stability,
        }

    sorted_rows = sorted(mode_rows.values(), key=lambda row: (float(row["p_hat_sq"]), row["momentum_mode"]))
    finite_difference = {
        "available": False,
        "dGamma_dp_hat_sq": float("nan"),
        "finite_residue_proxy": float("nan"),
    }
    if len(sorted_rows) >= 2 and abs(float(sorted_rows[0]["p_hat_sq"])) < 1.0e-15:
        first = None
        for row in sorted_rows[1:]:
            if float(row["p_hat_sq"]) > 0.0:
                first = row
                break
        if first is not None:
            delta_p = float(first["p_hat_sq"]) - float(sorted_rows[0]["p_hat_sq"])
            derivative = (float(first["Gamma_ss_real"]) - float(sorted_rows[0]["Gamma_ss_real"])) / delta_p
            finite_difference = {
                "available": True,
                "reference_modes": [sorted_rows[0]["momentum_mode"], first["momentum_mode"]],
                "dGamma_dp_hat_sq": derivative,
                "finite_residue_proxy": 1.0 / abs(derivative) if abs(derivative) > 1.0e-30 else float("nan"),
            }

    stability_rows = [
        row.get("noise_subsample_stability", {})
        for row in mode_rows.values()
        if row.get("noise_subsample_stability", {}).get("available") is True
    ]
    stability_ratios = [
        float(row.get("C_ss_real_half_delta_over_stderr_max", float("nan")))
        for row in stability_rows
        if math.isfinite(float(row.get("C_ss_real_half_delta_over_stderr_max", float("nan"))))
    ]
    noise_subsample_stability = {
        "available": bool(stability_rows),
        "mode_count": len(stability_rows),
        "C_ss_real_half_delta_over_stderr_max": (
            float(max(stability_ratios)) if stability_ratios else float("nan")
        ),
        "strict_limit": (
            "Noise subsample stability is an estimator diagnostic only; it is "
            "not production evidence or scalar LSZ normalization without "
            "same-source production statistics and pole/FV/IR control."
        ),
    }

    return {
        "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
        "measurement_object": "C_ss(q)=Tr[S V_q S V_-q], Gamma_ss(q)=1/C_ss(q)",
        "estimator": "Z2 stochastic trace estimator; production evidence requires saved ensembles and controlled statistics",
        "physical_higgs_normalization": "not_derived",
        "used_as_physical_yukawa_readout": False,
        "mode_rows": mode_rows,
        "noise_subsample_stability": noise_subsample_stability,
        "finite_difference_residue_proxy": finite_difference,
        "strict_limit": "finite-mode stochastic C_ss(q) is not kappa_s until an isolated pole, dGamma/dp^2 at the pole, and canonical Higgs normalization are derived",
    }


def fit_source_higgs_cross_correlator(
    source_higgs_measurements: dict[str, list[dict[str, Any]]],
    spatial_l: int,
    operator_certificate: dict[str, Any],
    operator_certificate_path: Path | None,
) -> dict[str, Any]:
    mode_rows = {}
    taste_radial_second_source = source_higgs_operator_is_taste_radial_second_source(operator_certificate)
    for key, rows in source_higgs_measurements.items():
        if not rows:
            continue
        nvec = tuple(int(x) for x in key.split(","))
        out: dict[str, Any] = {
            "momentum_mode": list(nvec),
            "p_hat_sq": spatial_p_hat_sq(nvec, spatial_l),
            "configuration_count": len(rows),
        }
        for label in ("C_ss", "C_sH", "C_HH"):
            real_values = np.asarray([float(row[f"{label}_real"]) for row in rows], dtype=float)
            imag_values = np.asarray([float(row[f"{label}_imag"]) for row in rows], dtype=float)
            real_err = (
                float(np.std(real_values, ddof=1) / math.sqrt(len(real_values)))
                if len(real_values) > 1
                else 0.0
            )
            imag_err = (
                float(np.std(imag_values, ddof=1) / math.sqrt(len(imag_values)))
                if len(imag_values) > 1
                else 0.0
            )
            out[f"{label}_real"] = float(np.mean(real_values))
            out[f"{label}_imag"] = float(np.mean(imag_values))
            out[f"{label}_real_config_stderr"] = real_err
            out[f"{label}_imag_config_stderr"] = imag_err
            out[f"{label}_timeseries"] = [
                {
                    "configuration_index": int(i),
                    f"{label}_real": float(row[f"{label}_real"]),
                    f"{label}_imag": float(row[f"{label}_imag"]),
                }
                for i, row in enumerate(rows)
            ]
        if taste_radial_second_source:
            out["C_sx_real"] = out["C_sH_real"]
            out["C_sx_imag"] = out["C_sH_imag"]
            out["C_sx_real_config_stderr"] = out["C_sH_real_config_stderr"]
            out["C_sx_imag_config_stderr"] = out["C_sH_imag_config_stderr"]
            out["C_sx_timeseries"] = [
                {
                    "configuration_index": int(item["configuration_index"]),
                    "C_sx_real": float(item["C_sH_real"]),
                    "C_sx_imag": float(item["C_sH_imag"]),
                }
                for item in out["C_sH_timeseries"]
            ]
            out["C_xx_real"] = out["C_HH_real"]
            out["C_xx_imag"] = out["C_HH_imag"]
            out["C_xx_real_config_stderr"] = out["C_HH_real_config_stderr"]
            out["C_xx_imag_config_stderr"] = out["C_HH_imag_config_stderr"]
            out["C_xx_timeseries"] = [
                {
                    "configuration_index": int(item["configuration_index"]),
                    "C_xx_real": float(item["C_HH_real"]),
                    "C_xx_imag": float(item["C_HH_imag"]),
                }
                for item in out["C_HH_timeseries"]
            ]
        c_ss = float(out.get("C_ss_real", float("nan")))
        c_sh = float(out.get("C_sH_real", float("nan")))
        c_hh = float(out.get("C_HH_real", float("nan")))
        product = c_ss * c_hh
        out["finite_row_gram"] = {
            "available": math.isfinite(product) and product > 0.0 and math.isfinite(c_sh),
            "gram_determinant_real": product - c_sh * c_sh if math.isfinite(product) else float("nan"),
            "rho_sH_real": c_sh / math.sqrt(product) if math.isfinite(product) and product > 0.0 else float("nan"),
            "strict_limit": (
                "Finite-mode rows are not pole residues.  Gram purity can only "
                "be evaluated after isolated-pole residue extraction and "
                "FV/IR/model-class gates."
            ),
        }
        mode_rows[key] = out

    return {
        "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
        "measurement_object": (
            "same-ensemble C_ss/C_sx/C_xx(q) rows for the supplied taste-radial second-source certificate"
            if taste_radial_second_source
            else "same-ensemble C_ss/C_sH/C_HH(q) rows for a supplied canonical-Higgs operator certificate"
        ),
        "operator": source_higgs_operator_summary(operator_certificate, operator_certificate_path),
        "firewall": source_higgs_firewall_from_certificate(operator_certificate),
        "mode_rows": mode_rows,
        "pole_residue_rows": [],
        "same_ensemble": True,
        "same_source_coordinate": True,
        "two_source_taste_radial_row_aliases": {
            "available": taste_radial_second_source,
            "source_operator_symbol": "x",
            "C_sx_aliases_C_sH_schema_field": taste_radial_second_source,
            "C_xx_aliases_C_HH_schema_field": taste_radial_second_source,
            "strict_limit": (
                "C_sx/C_xx aliases are second-source taste-radial rows.  They "
                "are not canonical-Higgs C_sH/C_HH rows unless a separate "
                "canonical O_H/source-overlap bridge passes."
            ),
        },
        "canonical_higgs_operator_identity_passed": operator_certificate.get(
            "canonical_higgs_operator_identity_passed"
        )
        is True,
        "used_as_physical_yukawa_readout": False,
        "strict_limit": (
            "This analysis emits finite-momentum cross-correlator rows.  It does "
            "not supply pole residues, Gram-purity closure, or retained y_t "
            "authorization without the source-Higgs certificate builder and "
            "postprocessor gates."
        ),
    }


def fit_source_higgs_time_kernel(
    source_higgs_time_kernel_measurements: dict[str, list[dict[str, Any]]],
    spatial_l: int,
    operator_certificate: dict[str, Any],
    operator_certificate_path: Path | None,
) -> dict[str, Any]:
    mode_rows: dict[str, Any] = {}
    taste_radial_second_source = source_higgs_operator_is_taste_radial_second_source(operator_certificate)
    for key, rows in source_higgs_time_kernel_measurements.items():
        if not rows:
            continue
        nvec = tuple(int(x) for x in key.split(","))
        taus = sorted(
            {
                int(tau_row["tau"])
                for row in rows
                for tau_row in row.get("tau_rows", [])
            }
        )
        tau_rows = []
        for tau in taus:
            out: dict[str, Any] = {"tau": int(tau)}
            matrix_real: list[list[float]] = []
            matrix_imag: list[list[float]] = []
            for label in ("C_ss", "C_sH", "C_Hs", "C_HH"):
                label_values: list[complex] = []
                label_series = []
                for cfg_index, row in enumerate(rows):
                    matching = [
                        tau_row
                        for tau_row in row.get("tau_rows", [])
                        if int(tau_row.get("tau", -1)) == tau
                    ]
                    if not matching:
                        continue
                    tau_row = matching[0]
                    value = complex(
                        float(tau_row.get(f"{label}_real", float("nan"))),
                        float(tau_row.get(f"{label}_imag", float("nan"))),
                    )
                    label_values.append(value)
                    label_series.append(
                        {
                            "configuration_index": int(cfg_index),
                            f"{label}_real": float(value.real),
                            f"{label}_imag": float(value.imag),
                        }
                    )
                values = np.asarray(label_values, dtype=np.complex128)
                mean = complex(np.mean(values)) if values.size else complex(float("nan"), float("nan"))
                real_err = (
                    float(np.std(values.real, ddof=1) / math.sqrt(values.size))
                    if values.size > 1
                    else 0.0
                )
                imag_err = (
                    float(np.std(values.imag, ddof=1) / math.sqrt(values.size))
                    if values.size > 1
                    else 0.0
                )
                out[f"{label}_real"] = float(mean.real)
                out[f"{label}_imag"] = float(mean.imag)
                out[f"{label}_real_config_stderr"] = real_err
                out[f"{label}_imag_config_stderr"] = imag_err
                out[f"{label}_timeseries"] = label_series

            if taste_radial_second_source:
                for canonical_label, taste_label in (
                    ("C_sH", "C_sx"),
                    ("C_Hs", "C_xs"),
                    ("C_HH", "C_xx"),
                ):
                    out[f"{taste_label}_real"] = out[f"{canonical_label}_real"]
                    out[f"{taste_label}_imag"] = out[f"{canonical_label}_imag"]
                    out[f"{taste_label}_real_config_stderr"] = out[
                        f"{canonical_label}_real_config_stderr"
                    ]
                    out[f"{taste_label}_imag_config_stderr"] = out[
                        f"{canonical_label}_imag_config_stderr"
                    ]
                    out[f"{taste_label}_timeseries"] = [
                        {
                            "configuration_index": int(item["configuration_index"]),
                            f"{taste_label}_real": float(item[f"{canonical_label}_real"]),
                            f"{taste_label}_imag": float(item[f"{canonical_label}_imag"]),
                        }
                        for item in out[f"{canonical_label}_timeseries"]
                    ]

            matrix_real = [
                [float(out.get("C_ss_real", float("nan"))), float(out.get("C_sH_real", float("nan")))],
                [float(out.get("C_Hs_real", float("nan"))), float(out.get("C_HH_real", float("nan")))],
            ]
            matrix_imag = [
                [float(out.get("C_ss_imag", float("nan"))), float(out.get("C_sH_imag", float("nan")))],
                [float(out.get("C_Hs_imag", float("nan"))), float(out.get("C_HH_imag", float("nan")))],
            ]
            out["C_matrix_real"] = matrix_real
            out["C_matrix_imag"] = matrix_imag
            if taste_radial_second_source:
                out["C_sx_matrix_real_alias"] = matrix_real
                out["C_sx_matrix_imag_alias"] = matrix_imag
            tau_rows.append(out)

        mode_rows[key] = {
            "momentum_mode": list(nvec),
            "p_hat_sq": spatial_p_hat_sq(nvec, spatial_l),
            "configuration_count": len(rows),
            "tau_rows": tau_rows,
            "C_matrix_by_t": tau_rows,
        }

    return {
        "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
        "measurement_object": (
            "same-surface Euclidean-time C_ss/C_sx/C_xs/C_xx(t) rows for the supplied taste-radial second-source certificate"
            if taste_radial_second_source
            else "same-surface Euclidean-time C_ss/C_sH/C_Hs/C_HH(t) rows for a supplied canonical-Higgs operator certificate"
        ),
        "time_kernel_schema_version": "source_higgs_time_kernel_v1",
        "operator": source_higgs_operator_summary(operator_certificate, operator_certificate_path),
        "firewall": source_higgs_firewall_from_certificate(operator_certificate),
        "mode_rows": mode_rows,
        "same_ensemble": True,
        "same_source_coordinate": True,
        "physical_higgs_normalization": "not_derived",
        "canonical_higgs_operator_identity_passed": operator_certificate.get(
            "canonical_higgs_operator_identity_passed"
        )
        is True,
        "used_as_physical_yukawa_readout": False,
        "two_source_taste_radial_row_aliases": {
            "available": taste_radial_second_source,
            "source_operator_symbol": "x",
            "C_sx_aliases_C_sH_schema_field": taste_radial_second_source,
            "C_xs_aliases_C_Hs_schema_field": taste_radial_second_source,
            "C_xx_aliases_C_HH_schema_field": taste_radial_second_source,
            "strict_limit": (
                "C_sx/C_xs/C_xx aliases are second-source taste-radial time-kernel rows. "
                "They are not canonical-Higgs rows unless a separate canonical "
                "O_H/source-overlap bridge passes."
            ),
        },
        "strict_limit": (
            "This default-off harness extension emits same-surface Euclidean-time "
            "scalar matrix rows for transfer-kernel/GEVP analysis.  It is not "
            "physical y_t evidence until canonical O_H or physical neutral "
            "transfer identity, pole/FV/IR/threshold authority, overlap "
            "normalization, and retained-route gates pass."
        ),
    }


def wz_mass_response_smoke_enabled(args: argparse.Namespace) -> bool:
    return bool(getattr(args, "wz_mass_response_smoke", False)) and bool(
        getattr(args, "wz_source_shifts_parsed", [])
    )


def synthetic_wz_mass_lat(channel: str, selected_mass: float, source_shift: float) -> float:
    """Contract-only W/Z mass model for reduced smoke rows.

    This deliberately does not use observed W/Z masses or electroweak tree
    algebra.  It only creates positive correlators with a planted source slope
    so downstream schema and covariance plumbing can be validated.
    """
    channel_factor = 1.0 if channel == "W" else 1.18
    base = channel_factor * (0.28 + 0.04 * float(selected_mass))
    slope = channel_factor * (0.21 + 0.03 * float(selected_mass))
    return max(base + slope * float(source_shift), 1.0e-6)


def measure_wz_mass_response_smoke_correlator(
    geom: Geometry,
    selected_mass: float,
    source_shift: float,
    channel: str,
    cfg_index: int,
) -> list[float]:
    mass_lat = synthetic_wz_mass_lat(channel, selected_mass, source_shift)
    amplitude = 1.0 + 0.01 * math.cos(float(cfg_index) + 3.0 * float(source_shift))
    corr = []
    for tau in range(geom.time_l):
        forward = math.exp(-mass_lat * tau)
        backward = math.exp(-mass_lat * max(geom.time_l - tau, 0))
        corr.append(float(amplitude * (forward + backward)))
    return corr


def fit_wz_mass_response_smoke(
    wz_measurements: dict[float, list[list[float]]],
    source_shifts: list[float],
    channel: str,
    selected_mass: float,
) -> dict[str, Any]:
    rows = []
    finite_pairs = []
    channel_key = "w_mass_fit" if channel == "W" else "z_mass_fit"
    slope_key = "slope_dM_W_ds" if channel == "W" else "slope_dM_Z_ds"
    covariance_key = "cov_dE_top_dM_W" if channel == "W" else "cov_dE_top_dM_Z"
    for source_shift in sorted(source_shifts):
        arr = np.asarray(wz_measurements.get(source_shift, []), dtype=float)
        if arr.size == 0:
            continue
        mean, err = jackknife_mean_err(arr)
        fit = fit_mass(mean, err)
        if not math.isfinite(float(fit.get("m_lat", float("nan")))):
            fit = fit_energy_from_effective(mean)
        if not math.isfinite(float(fit.get("m_lat", float("nan")))):
            fit = fit_first_positive_effective(mean)
        mass_lat = float(fit.get("m_lat", float("nan")))
        mass_err = float(fit.get("m_lat_err", 0.0) or 0.0)
        row = {
            "source_shift": float(source_shift),
            "configuration_count": int(arr.shape[0]),
            channel_key: {
                "mass_lat": mass_lat,
                "mass_lat_err": mass_err,
                "from_correlator": True,
                "correlator_source": "synthetic_scout_contract_not_EW_field",
                "fit_window": [int(fit.get("tau_min", 0)), int(fit.get("tau_max", 0))],
                "chi2_dof": float(fit.get("chi2_dof", float("nan"))),
            },
            "effective_mass_method": "single_state_positive_scout_correlator",
            "jackknife_or_bootstrap_block_count": int(arr.shape[0]),
            "correlator": [
                {"tau": int(tau), "mean": float(c), "stderr": float(e)}
                for tau, (c, e) in enumerate(zip(mean, err))
            ],
            "rng_seed_control": {
                "seed_control_version": "deterministic_wz_smoke_contract_v1",
                "random_numbers_used": False,
            },
        }
        rows.append(row)
        if math.isfinite(mass_lat):
            finite_pairs.append((float(source_shift), mass_lat, max(mass_err, 1.0e-12)))

    slope = float("nan")
    slope_err = float("nan")
    fit_kind = "unavailable"
    if len(finite_pairs) >= 2:
        shifts = np.asarray([item[0] for item in finite_pairs], dtype=float)
        masses = np.asarray([item[1] for item in finite_pairs], dtype=float)
        weights = np.asarray([1.0 / (item[2] * item[2]) for item in finite_pairs], dtype=float)
        coeffs, cov = np.polyfit(shifts, masses, deg=1, w=np.sqrt(weights), cov="unscaled")
        slope = float(coeffs[0])
        slope_err = float(math.sqrt(max(cov[0, 0], 0.0))) if cov.shape == (2, 2) else float("nan")
        fit_kind = f"linear_dM_{channel}_ds_scout"

    return {
        "phase": "scout",
        "source_coordinate": (
            "same numeric source-shift parameter s used by the top FH smoke run; "
            "canonical-Higgs/source identity is not certified"
        ),
        "same_source_coordinate": True,
        "same_source_identity_certified": False,
        "same_source_coordinate_certification_status": "schema_only_not_physics_authority",
        "selected_mass_parameter": float(selected_mass),
        "boson_channel": channel,
        "source_shifts": [float(x) for x in source_shifts],
        "wz_mass_fits_from_correlators": True,
        "per_source_shift_rows": rows,
        "gauge_response": {
            slope_key: slope,
            "slope_error": slope_err,
            covariance_key: float("nan"),
            "fit_kind": fit_kind,
            "covariance_status": "absent_in_smoke_schema",
        },
        "electroweak_coupling": {
            "g2": None,
            "sigma_g2": None,
            "g2_certificate": None,
            "used_observed_g2_as_selector": False,
            "status": "absent_not_required_for_smoke_schema",
        },
        "identity_certificates": {
            "same_source_sector_overlap_identity_passed": False,
            "canonical_higgs_pole_identity_passed": False,
            "retained_route_or_proposal_gate_passed": False,
        },
        "firewall": {
            "used_static_EW_mass_algebra": False,
            "used_observed_WZ_masses_as_selector": False,
            "used_observed_top_or_yukawa_as_selector": False,
            "used_static_v_overlap_selector": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
        "used_as_physical_yukawa_readout": False,
        "strict_limit": (
            "W/Z smoke rows validate harness schema only. They are synthetic "
            "positive correlators, not same-source EW production rows, and "
            "must not be fed to retained/proposed-retained gates as physics "
            "evidence."
        ),
    }


def physical_mass_gev(m_lat: float) -> float:
    a_inv = R0_OVER_A_BETA6_REFERENCE * HBARC_GEV_FM / R0_FM
    return m_lat * a_inv


def volume_seed(base_seed: int, spatial_l: int, time_l: int) -> int:
    return int(base_seed + 1000003 * spatial_l + 9176 * time_l)


def run_volume(args: argparse.Namespace, spatial_l: int, time_l: int, masses: list[float], rng: np.random.Generator) -> dict[str, Any]:
    if resolve_engine(args) == "numba":
        return run_volume_numba(args, spatial_l, time_l, masses)

    geom = Geometry(spatial_l, time_l)
    gauge = GaugeField(geom)
    t0 = time.time()
    plaquette_history = []
    for sweep in range(args.therm):
        gauge.heatbath_sweep(rng)
        for _ in range(args.overrelax):
            gauge.overrelax_sweep()
        plaquette_history.append(gauge.plaquette())
        print(f"  therm L={spatial_l} sweep={sweep + 1}/{args.therm} plaquette={plaquette_history[-1]:.6f}")

    measurements: dict[float, list[list[float]]] = {m: [] for m in masses}
    momentum_measurements: dict[float, dict[str, list[list[float]]]] = {m: {} for m in masses}
    source_response_measurements: dict[float, dict[float, list[list[float]]]] = {
        m: {s: [] for s in args.scalar_source_shifts_parsed} for m in masses
    }
    scalar_two_point_measurements: dict[float, dict[str, list[dict[str, Any]]]] = {
        m: {momentum_key(mode): [] for mode in args.scalar_two_point_modes_parsed} for m in masses
    }
    source_higgs_measurements: dict[float, dict[str, list[dict[str, Any]]]] = {
        m: {momentum_key(mode): [] for mode in args.source_higgs_cross_modes_parsed} for m in masses
    }
    source_higgs_time_kernel_measurements: dict[float, dict[str, list[dict[str, Any]]]] = {
        m: {momentum_key(mode): [] for mode in args.source_higgs_time_kernel_modes_parsed} for m in masses
    }
    wz_mass_response_measurements: dict[float, list[list[float]]] = {
        s: [] for s in args.wz_source_shifts_parsed
    }
    cg_residuals: dict[float, list[float]] = {m: [] for m in masses}
    selected_mass = selected_scalar_fh_lsz_mass(masses)
    fh_lsz_policy = selected_mass_policy_metadata(masses, args)
    plaquettes = []
    for cfg in range(args.measurements):
        for _ in range(args.separation):
            gauge.heatbath_sweep(rng)
            for _ in range(args.overrelax):
                gauge.overrelax_sweep()
        plaquettes.append(gauge.plaquette())
        meas_gauge = ape_smear_spatial(gauge, args.ape_alpha, args.ape_steps) if args.ape_steps else gauge
        normal_cache: dict[str, NormalEquationSystem] = {}
        if wz_mass_response_smoke_enabled(args):
            for source_shift in args.wz_source_shifts_parsed:
                wz_mass_response_measurements[source_shift].append(
                    measure_wz_mass_response_smoke_correlator(
                        meas_gauge.geom,
                        selected_mass,
                        source_shift,
                        args.wz_boson_channel,
                        cfg,
                    )
                )
        for mass in masses:
            normal_system = get_normal_equation_system(normal_cache, meas_gauge, mass)
            measured = measure_correlator(
                meas_gauge,
                mass,
                args.cg_rtol,
                args.cg_maxiter,
                args.momentum_modes_parsed,
                normal_system=normal_system,
            )
            measurements[mass].append(measured["correlator"])
            for key, corr in measured.get("momentum_correlators", {}).items():
                momentum_measurements[mass].setdefault(key, []).append(corr)
            cg_residuals[mass].append(float(measured["max_cg_residual"]))
            if abs(float(mass) - selected_mass) <= 1.0e-15:
                for source_shift in args.scalar_source_shifts_parsed:
                    if abs(source_shift) < 1.0e-15:
                        source_response_measurements[mass][source_shift].append(measured["correlator"])
                        continue
                    shifted_mass = mass + source_shift
                    shifted_system = get_normal_equation_system(normal_cache, meas_gauge, shifted_mass)
                    shifted = measure_correlator(
                        meas_gauge,
                        shifted_mass,
                        args.cg_rtol,
                        args.cg_maxiter,
                        [],
                        normal_system=shifted_system,
                    )
                    source_response_measurements[mass][source_shift].append(shifted["correlator"])
            if (
                abs(float(mass) - selected_mass) <= 1.0e-15
                and args.scalar_two_point_modes_parsed
                and args.scalar_two_point_noises > 0
            ):
                scalar_two_point = stochastic_scalar_two_point(
                    meas_gauge,
                    mass,
                    args.cg_rtol,
                    args.cg_maxiter,
                    args.scalar_two_point_modes_parsed,
                    args.scalar_two_point_noises,
                    rng,
                    normal_system=normal_system,
                )
                for key, row in scalar_two_point["mode_rows"].items():
                    scalar_two_point_measurements[mass].setdefault(key, []).append(row)
            if (
                abs(float(mass) - selected_mass) <= 1.0e-15
                and args.source_higgs_cross_modes_parsed
                and args.source_higgs_cross_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                source_higgs = stochastic_source_higgs_cross_correlator(
                    meas_gauge,
                    mass,
                    args.cg_rtol,
                    args.cg_maxiter,
                    args.source_higgs_cross_modes_parsed,
                    args.source_higgs_cross_noises,
                    rng,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                    normal_system=normal_system,
                )
                for key, row in source_higgs["mode_rows"].items():
                    source_higgs_measurements[mass].setdefault(key, []).append(row)
            if (
                abs(float(mass) - selected_mass) <= 1.0e-15
                and args.source_higgs_time_kernel_modes_parsed
                and args.source_higgs_time_kernel_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                source_higgs_time_kernel = stochastic_source_higgs_time_kernel(
                    meas_gauge,
                    mass,
                    args.cg_rtol,
                    args.cg_maxiter,
                    args.source_higgs_time_kernel_modes_parsed,
                    args.source_higgs_time_kernel_noises,
                    args.source_higgs_time_kernel_max_tau,
                    args.source_higgs_time_kernel_origin_count,
                    rng,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                    normal_system=normal_system,
                )
                for key, row in source_higgs_time_kernel["mode_rows"].items():
                    source_higgs_time_kernel_measurements[mass].setdefault(key, []).append(row)
        print(f"  meas L={spatial_l} cfg={cfg + 1}/{args.measurements} plaquette={plaquettes[-1]:.6f}")

    mass_scan = []
    selected_fit: dict[str, Any] | None = None
    correlator_rows = []
    selected_momentum_analysis: dict[str, Any] = {"energy_fits": {}, "kinetic_mass_fits": {}}
    selected_source_response_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "energy_fits": [],
        "slope_dE_ds_lat": float("nan"),
    }
    selected_scalar_two_point_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "mode_rows": {},
        "physical_higgs_normalization": "not_derived",
    }
    selected_source_higgs_cross_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "mode_rows": {},
        "pole_residue_rows": [],
        "used_as_physical_yukawa_readout": False,
    }
    selected_source_higgs_time_kernel_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "mode_rows": {},
        "time_kernel_schema_version": "disabled",
        "physical_higgs_normalization": "not_derived",
        "used_as_physical_yukawa_readout": False,
    }
    selected_wz_mass_response_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "phase": "disabled",
        "per_source_shift_rows": [],
        "used_as_physical_yukawa_readout": False,
    }
    for mass in masses:
        arr = np.asarray(measurements[mass], dtype=float)
        mean, err = jackknife_mean_err(arr)
        fit = fit_mass(mean, err)
        mass_scan.append(
            {
                "m_bare_lat": mass,
                "m_fit_lat": fit["m_lat"],
                "m_fit_lat_err": fit["m_lat_err"],
                "chi2_dof": fit["chi2_dof"],
                "max_cg_residual": max(cg_residuals[mass]) if cg_residuals[mass] else None,
            }
        )
        if mass == selected_mass:
            selected_fit = fit
            for tau, (c, e) in enumerate(zip(mean, err)):
                correlator_rows.append({"tau": tau, "mean": float(c), "stderr": float(e)})
            selected_momentum_analysis = fit_momentum_energies(
                momentum_measurements[mass],
                spatial_l,
            )
            if args.scalar_source_shifts_parsed:
                selected_source_response_analysis = fit_scalar_source_response(
                    source_response_measurements[mass],
                    mass,
                )
            if args.scalar_two_point_modes_parsed and args.scalar_two_point_noises > 0:
                selected_scalar_two_point_analysis = fit_scalar_two_point_lsz(
                    scalar_two_point_measurements[mass],
                    spatial_l,
                )
            if (
                args.source_higgs_cross_modes_parsed
                and args.source_higgs_cross_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                selected_source_higgs_cross_analysis = fit_source_higgs_cross_correlator(
                    source_higgs_measurements[mass],
                    spatial_l,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                )
            if (
                args.source_higgs_time_kernel_modes_parsed
                and args.source_higgs_time_kernel_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                selected_source_higgs_time_kernel_analysis = fit_source_higgs_time_kernel(
                    source_higgs_time_kernel_measurements[mass],
                    spatial_l,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                )

    if wz_mass_response_smoke_enabled(args):
        selected_wz_mass_response_analysis = fit_wz_mass_response_smoke(
            wz_mass_response_measurements,
            args.wz_source_shifts_parsed,
            args.wz_boson_channel,
            selected_mass,
        )

    top_mass_scan_response_analysis = fit_top_mass_scan_response(measurements, selected_mass)

    if selected_fit is None:
        selected_fit = mass_scan[len(mass_scan) // 2]

    elapsed = time.time() - t0
    return {
        "spatial_L": spatial_l,
        "time_L": time_l,
        "dims": [spatial_l, spatial_l, spatial_l, time_l],
        "a_fm": R0_FM / R0_OVER_A_BETA6_REFERENCE,
        "r0_over_a": R0_OVER_A_BETA6_REFERENCE,
        "boundary_conditions": {
            "gauge_spatial": "periodic",
            "gauge_time": "periodic",
            "fermion_time": "antiperiodic",
        },
        "update_algorithm": "Cabibbo-Marinari heatbath + polar overrelaxation",
        "update_engine": "python",
        "thermalization_sweeps": args.therm,
        "measurement_sweeps": args.measurements,
        "measurement_separation_sweeps": args.separation,
        "ape_smearing": {"steps": args.ape_steps, "alpha": args.ape_alpha},
        "plaquette_history": [float(x) for x in plaquette_history],
        "plaquette_measurements": [float(x) for x in plaquettes],
        "plaquette_mean": float(np.mean(plaquettes)) if plaquettes else None,
        "mass_parameter_scan": mass_scan,
        "top_mass_scan_response_analysis": top_mass_scan_response_analysis,
        "selected_mass_parameter": selected_mass,
        "fh_lsz_measurement_policy": fh_lsz_policy,
        "correlators": correlator_rows,
        "momentum_analysis": selected_momentum_analysis,
        "scalar_source_response_analysis": selected_source_response_analysis,
        "scalar_two_point_lsz_analysis": selected_scalar_two_point_analysis,
        "source_higgs_cross_correlator_analysis": selected_source_higgs_cross_analysis,
        "source_higgs_time_kernel_analysis": selected_source_higgs_time_kernel_analysis,
        "wz_mass_response_analysis": selected_wz_mass_response_analysis,
        "effective_mass": effective_mass(np.array([r["mean"] for r in correlator_rows])),
        "mass_fit": selected_fit,
        "runtime_seconds": elapsed,
    }


def run_volume_numba(args: argparse.Namespace, spatial_l: int, time_l: int, masses: list[float]) -> dict[str, Any]:
    geom = Geometry(spatial_l, time_l)
    volume_rng_seed = volume_seed(int(args.seed), spatial_l, time_l)
    nb_seed(volume_rng_seed)
    u = cold_link_array(geom)
    scalar_rng = np.random.default_rng(volume_rng_seed)
    t0 = time.time()
    plaquette_history = []
    for sweep in range(args.therm):
        nb_heatbath_sweep(u, BETA)
        for _ in range(args.overrelax):
            nb_overrelax_sweep(u)
        plaquette_history.append(float(nb_plaquette(u)))
        print(f"  therm L={spatial_l} sweep={sweep + 1}/{args.therm} plaquette={plaquette_history[-1]:.6f}")

    measurements: dict[float, list[list[float]]] = {m: [] for m in masses}
    momentum_measurements: dict[float, dict[str, list[list[float]]]] = {m: {} for m in masses}
    source_response_measurements: dict[float, dict[float, list[list[float]]]] = {
        m: {s: [] for s in args.scalar_source_shifts_parsed} for m in masses
    }
    scalar_two_point_measurements: dict[float, dict[str, list[dict[str, Any]]]] = {
        m: {momentum_key(mode): [] for mode in args.scalar_two_point_modes_parsed} for m in masses
    }
    source_higgs_measurements: dict[float, dict[str, list[dict[str, Any]]]] = {
        m: {momentum_key(mode): [] for mode in args.source_higgs_cross_modes_parsed} for m in masses
    }
    source_higgs_time_kernel_measurements: dict[float, dict[str, list[dict[str, Any]]]] = {
        m: {momentum_key(mode): [] for mode in args.source_higgs_time_kernel_modes_parsed} for m in masses
    }
    wz_mass_response_measurements: dict[float, list[list[float]]] = {
        s: [] for s in args.wz_source_shifts_parsed
    }
    cg_residuals: dict[float, list[float]] = {m: [] for m in masses}
    selected_mass = selected_scalar_fh_lsz_mass(masses)
    fh_lsz_policy = selected_mass_policy_metadata(masses, args)
    plaquettes = []
    for cfg in range(args.measurements):
        for _ in range(args.separation):
            nb_heatbath_sweep(u, BETA)
            for _ in range(args.overrelax):
                nb_overrelax_sweep(u)
        plaquettes.append(float(nb_plaquette(u)))
        gauge_view = gauge_field_from_array(geom, u)
        meas_gauge = ape_smear_spatial(gauge_view, args.ape_alpha, args.ape_steps) if args.ape_steps else gauge_view
        normal_cache: dict[str, NormalEquationSystem] = {}
        if wz_mass_response_smoke_enabled(args):
            for source_shift in args.wz_source_shifts_parsed:
                wz_mass_response_measurements[source_shift].append(
                    measure_wz_mass_response_smoke_correlator(
                        meas_gauge.geom,
                        selected_mass,
                        source_shift,
                        args.wz_boson_channel,
                        cfg,
                    )
                )
        for mass in masses:
            normal_system = get_normal_equation_system(normal_cache, meas_gauge, mass)
            measured = measure_correlator(
                meas_gauge,
                mass,
                args.cg_rtol,
                args.cg_maxiter,
                args.momentum_modes_parsed,
                normal_system=normal_system,
            )
            measurements[mass].append(measured["correlator"])
            for key, corr in measured.get("momentum_correlators", {}).items():
                momentum_measurements[mass].setdefault(key, []).append(corr)
            cg_residuals[mass].append(float(measured["max_cg_residual"]))
            if abs(float(mass) - selected_mass) <= 1.0e-15:
                for source_shift in args.scalar_source_shifts_parsed:
                    if abs(source_shift) < 1.0e-15:
                        source_response_measurements[mass][source_shift].append(measured["correlator"])
                        continue
                    shifted_mass = mass + source_shift
                    shifted_system = get_normal_equation_system(normal_cache, meas_gauge, shifted_mass)
                    shifted = measure_correlator(
                        meas_gauge,
                        shifted_mass,
                        args.cg_rtol,
                        args.cg_maxiter,
                        [],
                        normal_system=shifted_system,
                    )
                    source_response_measurements[mass][source_shift].append(shifted["correlator"])
            if (
                abs(float(mass) - selected_mass) <= 1.0e-15
                and args.scalar_two_point_modes_parsed
                and args.scalar_two_point_noises > 0
            ):
                scalar_two_point = stochastic_scalar_two_point(
                    meas_gauge,
                    mass,
                    args.cg_rtol,
                    args.cg_maxiter,
                    args.scalar_two_point_modes_parsed,
                    args.scalar_two_point_noises,
                    scalar_rng,
                    normal_system=normal_system,
                )
                for key, row in scalar_two_point["mode_rows"].items():
                    scalar_two_point_measurements[mass].setdefault(key, []).append(row)
            if (
                abs(float(mass) - selected_mass) <= 1.0e-15
                and args.source_higgs_cross_modes_parsed
                and args.source_higgs_cross_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                source_higgs = stochastic_source_higgs_cross_correlator(
                    meas_gauge,
                    mass,
                    args.cg_rtol,
                    args.cg_maxiter,
                    args.source_higgs_cross_modes_parsed,
                    args.source_higgs_cross_noises,
                    scalar_rng,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                    normal_system=normal_system,
                )
                for key, row in source_higgs["mode_rows"].items():
                    source_higgs_measurements[mass].setdefault(key, []).append(row)
            if (
                abs(float(mass) - selected_mass) <= 1.0e-15
                and args.source_higgs_time_kernel_modes_parsed
                and args.source_higgs_time_kernel_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                source_higgs_time_kernel = stochastic_source_higgs_time_kernel(
                    meas_gauge,
                    mass,
                    args.cg_rtol,
                    args.cg_maxiter,
                    args.source_higgs_time_kernel_modes_parsed,
                    args.source_higgs_time_kernel_noises,
                    args.source_higgs_time_kernel_max_tau,
                    args.source_higgs_time_kernel_origin_count,
                    scalar_rng,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                    normal_system=normal_system,
                )
                for key, row in source_higgs_time_kernel["mode_rows"].items():
                    source_higgs_time_kernel_measurements[mass].setdefault(key, []).append(row)
        print(f"  meas L={spatial_l} cfg={cfg + 1}/{args.measurements} plaquette={plaquettes[-1]:.6f}")

    mass_scan = []
    selected_fit: dict[str, Any] | None = None
    correlator_rows = []
    selected_momentum_analysis: dict[str, Any] = {"energy_fits": {}, "kinetic_mass_fits": {}}
    selected_source_response_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "energy_fits": [],
        "slope_dE_ds_lat": float("nan"),
    }
    selected_scalar_two_point_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "mode_rows": {},
        "physical_higgs_normalization": "not_derived",
    }
    selected_source_higgs_cross_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "mode_rows": {},
        "pole_residue_rows": [],
        "used_as_physical_yukawa_readout": False,
    }
    selected_source_higgs_time_kernel_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "mode_rows": {},
        "time_kernel_schema_version": "disabled",
        "physical_higgs_normalization": "not_derived",
        "used_as_physical_yukawa_readout": False,
    }
    selected_wz_mass_response_analysis: dict[str, Any] = {
        "source_coordinate": "disabled",
        "phase": "disabled",
        "per_source_shift_rows": [],
        "used_as_physical_yukawa_readout": False,
    }
    for mass in masses:
        arr = np.asarray(measurements[mass], dtype=float)
        mean, err = jackknife_mean_err(arr)
        fit = fit_mass(mean, err)
        mass_scan.append(
            {
                "m_bare_lat": mass,
                "m_fit_lat": fit["m_lat"],
                "m_fit_lat_err": fit["m_lat_err"],
                "chi2_dof": fit["chi2_dof"],
                "max_cg_residual": max(cg_residuals[mass]) if cg_residuals[mass] else None,
            }
        )
        if mass == selected_mass:
            selected_fit = fit
            for tau, (c, e) in enumerate(zip(mean, err)):
                correlator_rows.append({"tau": tau, "mean": float(c), "stderr": float(e)})
            selected_momentum_analysis = fit_momentum_energies(
                momentum_measurements[mass],
                spatial_l,
            )
            if args.scalar_source_shifts_parsed:
                selected_source_response_analysis = fit_scalar_source_response(
                    source_response_measurements[mass],
                    mass,
                )
            if args.scalar_two_point_modes_parsed and args.scalar_two_point_noises > 0:
                selected_scalar_two_point_analysis = fit_scalar_two_point_lsz(
                    scalar_two_point_measurements[mass],
                    spatial_l,
                )
            if (
                args.source_higgs_cross_modes_parsed
                and args.source_higgs_cross_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                selected_source_higgs_cross_analysis = fit_source_higgs_cross_correlator(
                    source_higgs_measurements[mass],
                    spatial_l,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                )
            if (
                args.source_higgs_time_kernel_modes_parsed
                and args.source_higgs_time_kernel_noises > 0
                and args.source_higgs_operator_certificate_data
            ):
                selected_source_higgs_time_kernel_analysis = fit_source_higgs_time_kernel(
                    source_higgs_time_kernel_measurements[mass],
                    spatial_l,
                    args.source_higgs_operator_certificate_data,
                    args.source_higgs_operator_certificate,
                )

    if wz_mass_response_smoke_enabled(args):
        selected_wz_mass_response_analysis = fit_wz_mass_response_smoke(
            wz_mass_response_measurements,
            args.wz_source_shifts_parsed,
            args.wz_boson_channel,
            selected_mass,
        )

    top_mass_scan_response_analysis = fit_top_mass_scan_response(measurements, selected_mass)

    if selected_fit is None:
        selected_fit = mass_scan[len(mass_scan) // 2]

    elapsed = time.time() - t0
    return {
        "spatial_L": spatial_l,
        "time_L": time_l,
        "dims": [spatial_l, spatial_l, spatial_l, time_l],
        "a_fm": R0_FM / R0_OVER_A_BETA6_REFERENCE,
        "r0_over_a": R0_OVER_A_BETA6_REFERENCE,
        "boundary_conditions": {
            "gauge_spatial": "periodic",
            "gauge_time": "periodic",
            "fermion_time": "antiperiodic",
        },
        "update_algorithm": "Cabibbo-Marinari heatbath + polar overrelaxation",
        "update_engine": "numba",
        "rng_seed_control": {
            "seed_control_version": "numba_gauge_seed_v1",
            "base_seed": int(args.seed),
            "volume_rng_seed": volume_rng_seed,
            "gauge_rng_seed": volume_rng_seed,
            "scalar_rng_seed": volume_rng_seed,
            "numba_gauge_seeded_before_thermalization": True,
        },
        "thermalization_sweeps": args.therm,
        "measurement_sweeps": args.measurements,
        "measurement_separation_sweeps": args.separation,
        "ape_smearing": {"steps": args.ape_steps, "alpha": args.ape_alpha},
        "plaquette_history": [float(x) for x in plaquette_history],
        "plaquette_measurements": [float(x) for x in plaquettes],
        "plaquette_mean": float(np.mean(plaquettes)) if plaquettes else None,
        "mass_parameter_scan": mass_scan,
        "top_mass_scan_response_analysis": top_mass_scan_response_analysis,
        "selected_mass_parameter": selected_mass,
        "fh_lsz_measurement_policy": fh_lsz_policy,
        "correlators": correlator_rows,
        "momentum_analysis": selected_momentum_analysis,
        "scalar_source_response_analysis": selected_source_response_analysis,
        "scalar_two_point_lsz_analysis": selected_scalar_two_point_analysis,
        "source_higgs_cross_correlator_analysis": selected_source_higgs_cross_analysis,
        "source_higgs_time_kernel_analysis": selected_source_higgs_time_kernel_analysis,
        "wz_mass_response_analysis": selected_wz_mass_response_analysis,
        "effective_mass": effective_mass(np.array([r["mean"] for r in correlator_rows])),
        "mass_fit": selected_fit,
        "runtime_seconds": elapsed,
    }


def combine_results(ensembles: list[dict[str, Any]]) -> dict[str, Any]:
    masses = []
    mass_errs = []
    for ens in ensembles:
        fit = ens.get("mass_fit", {})
        if isinstance(fit, dict) and math.isfinite(float(fit.get("m_lat", float("nan")))):
            masses.append(float(fit["m_lat"]))
            mass_errs.append(float(fit.get("m_lat_err", 0.0)))
    if not masses:
        m_lat = float("nan")
        stat_lat = float("nan")
        fv_lat = float("nan")
    else:
        m_lat = float(np.mean(masses))
        stat_lat = float(math.sqrt(sum(e * e for e in mass_errs)) / max(len(mass_errs), 1))
        fv_lat = float(np.std(masses, ddof=1)) if len(masses) > 1 else 0.0
    m_running = physical_mass_gev(m_lat) if math.isfinite(m_lat) else float("nan")
    stat = physical_mass_gev(stat_lat) if math.isfinite(stat_lat) else float("nan")
    finite_volume = physical_mass_gev(fv_lat) if math.isfinite(fv_lat) else float("nan")
    # Reduced-run placeholders are deliberately conservative and large.
    finite_spacing = max(0.20 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    scale_setting = max(0.05 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    matching = max(0.10 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    running_bridge = max(0.10 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    heavy_mass_tuning = max(0.15 * abs(m_running), 0.0) if math.isfinite(m_running) else float("nan")
    components = {
        "statistical": stat,
        "heavy_mass_tuning": heavy_mass_tuning,
        "finite_volume": finite_volume,
        "finite_spacing": finite_spacing,
        "scale_setting": scale_setting,
        "matching": matching,
        "running_bridge": running_bridge,
        "v_input": 0.0001,
    }
    total_mt = math.sqrt(sum(v * v for v in components.values() if math.isfinite(v)))
    y_t = math.sqrt(2.0) * m_running / V_GEV if math.isfinite(m_running) else float("nan")
    y_components = {k: (math.sqrt(2.0) * v / V_GEV if math.isfinite(v) else None) for k, v in components.items()}
    total_y = math.sqrt(sum(v * v for v in y_components.values() if v is not None and math.isfinite(v)))
    return {
        "m_t_running_at_v_GeV": m_running,
        "y_t_v": y_t,
        "m_t_pole_GeV": m_running,
        "uncertainties": y_components,
        "mass_uncertainties_GeV": components,
        "total_y_t_uncertainty": total_y,
        "total_m_t_pole_uncertainty_GeV": total_mt,
        "reduced_scope_delta_to_pdg_GeV": m_running - PDG_TOP_MASS_GEV if math.isfinite(m_running) else None,
        "reduced_scope_delta_to_y_t_target": y_t - YT_TARGET if math.isfinite(y_t) else None,
    }


def parse_volume_spec(spec: str) -> list[tuple[int, int]]:
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "x" in part:
            l_s, l_t = part.lower().split("x", 1)
            out.append((int(l_s), int(l_t)))
        else:
            l_s = int(part)
            out.append((l_s, 2 * l_s))
    return out


def volume_artifact_path(output_dir: Path, spatial_l: int, time_l: int) -> Path:
    return output_dir / f"L{spatial_l}xT{time_l}" / "ensemble_measurement.json"


def write_volume_artifact(output_dir: Path, ensemble: dict[str, Any]) -> Path:
    spatial_l = int(ensemble["spatial_L"])
    time_l = int(ensemble["time_L"])
    path = volume_artifact_path(output_dir, spatial_l, time_l)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ensemble, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_volume_artifact(output_dir: Path, spatial_l: int, time_l: int) -> dict[str, Any]:
    path = volume_artifact_path(output_dir, spatial_l, time_l)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"volume artifact is not a JSON object: {path}")
    return data


def build_certificate(args: argparse.Namespace, ensembles: list[dict[str, Any]]) -> dict[str, Any]:
    result = combine_results(ensembles)
    ratio_y = result["y_t_v"]
    phase = "production" if args.production_targets else "pilot" if args.pilot_targets else "reduced_scope"
    masses = [float(x) for x in args.masses.split(",") if x.strip()]
    fh_lsz_policy = selected_mass_policy_metadata(masses, args) if masses else {}
    source_higgs_enabled = bool(getattr(args, "source_higgs_cross_modes_parsed", [])) and int(
        getattr(args, "source_higgs_cross_noises", 0)
    ) > 0 and bool(getattr(args, "source_higgs_operator_certificate_data", {}))
    source_higgs_time_kernel_enabled = bool(
        getattr(args, "source_higgs_time_kernel_modes_parsed", [])
    ) and int(getattr(args, "source_higgs_time_kernel_noises", 0)) > 0 and bool(
        getattr(args, "source_higgs_operator_certificate_data", {})
    )
    source_higgs_operator = source_higgs_operator_summary(
        getattr(args, "source_higgs_operator_certificate_data", {}),
        getattr(args, "source_higgs_operator_certificate", None),
    )
    source_higgs_firewall = source_higgs_firewall_from_certificate(
        getattr(args, "source_higgs_operator_certificate_data", {})
    )
    wz_smoke_enabled = wz_mass_response_smoke_enabled(args)
    evidence_scope = {
        "production": "user-requested production targets",
        "pilot": "bounded pilot run; infrastructure and scaling evidence only",
        "reduced_scope": "reduced run is infrastructure evidence only",
    }[phase]
    ratio_source = args.g_s_source or f"not_measured_{phase}"
    g_s_lattice = args.g_s_lattice
    g_s_uncertainty = args.g_s_uncertainty
    ratio = None
    ratio_uncertainty = None
    if (
        isinstance(ratio_y, float)
        and math.isfinite(ratio_y)
        and isinstance(g_s_lattice, float)
        and math.isfinite(g_s_lattice)
        and g_s_lattice > 0.0
    ):
        ratio = ratio_y / g_s_lattice
        dy = result.get("total_y_t_uncertainty")
        dg = g_s_uncertainty
        rel2 = 0.0
        if isinstance(dy, float) and math.isfinite(dy) and ratio_y != 0.0:
            rel2 += (dy / ratio_y) ** 2
        if isinstance(dg, float) and math.isfinite(dg):
            rel2 += (dg / g_s_lattice) ** 2
        ratio_uncertainty = abs(ratio) * math.sqrt(rel2) if rel2 > 0.0 else None
    return {
        "metadata": {
            "authority": "staggered_top_correlator_mass_extraction",
            "phase": phase,
            "action": "Cl3Z3_SU3_Wilson_staggered",
            "g_bare": 1.0,
            "uses_prior_ward_chain": False,
            "uses_composite_matrix_element_route": False,
            "uses_coupling_definition_route": False,
            "scale_anchor": f"Sommer r0 = 0.5 fm external anchor; r0/a reference used for {phase} run",
            "running_bridge": (
                "production certificate must supply authoritative 4/5-loop bridge"
                if phase == "production"
                else f"{phase} run uses no authoritative SM RGE; production certificate must supply 4/5-loop bridge"
            ),
            "scalar_source_response": {
                "enabled": bool(getattr(args, "scalar_source_shifts_parsed", [])),
                "source_coordinate": "uniform additive lattice scalar source s entering the Dirac mass as m_bare + s",
                "selected_mass_only": bool(fh_lsz_policy.get("scalar_source_response_selected_mass_only", False)),
                "selected_mass_parameter": fh_lsz_policy.get("selected_mass_parameter"),
                "non_selected_masses_skipped": fh_lsz_policy.get("non_selected_masses_scalar_fh_lsz_skipped", []),
                "target_timeseries_schema_version": "fh_lsz_target_timeseries_v2_multitau",
                "multi_tau_response_serialization": bool(getattr(args, "scalar_source_shifts_parsed", [])),
                "multi_tau_response_serialization_status": (
                    "enabled_for_selected_mass_only"
                    if getattr(args, "scalar_source_shifts_parsed", [])
                    else "disabled_no_scalar_source_shifts"
                ),
                "physical_higgs_normalization": "not_derived",
                "used_as_physical_yukawa_readout": False,
            },
            "scalar_two_point_lsz": {
                "enabled": bool(getattr(args, "scalar_two_point_modes_parsed", []))
                and int(getattr(args, "scalar_two_point_noises", 0)) > 0,
                "measurement_object": "C_ss(q)=Tr[S V_q S V_-q] for the same additive scalar source",
                "noise_vectors_per_configuration": int(getattr(args, "scalar_two_point_noises", 0)),
                "selected_mass_only": bool(fh_lsz_policy.get("scalar_two_point_lsz_selected_mass_only", False)),
                "selected_mass_parameter": fh_lsz_policy.get("selected_mass_parameter"),
                "non_selected_masses_skipped": fh_lsz_policy.get("non_selected_masses_scalar_fh_lsz_skipped", []),
                "physical_higgs_normalization": "not_derived",
                "used_as_physical_yukawa_readout": False,
            },
            "top_mass_scan_response": {
                "enabled": len(masses) >= 2,
                "row_schema_version": "top_mass_scan_response_v1",
                "source_coordinate": "uniform additive Dirac bare mass m_bare",
                "selected_mass_parameter": fh_lsz_policy.get("selected_mass_parameter"),
                "mass_scan_masses_lat": masses,
                "serialization": "per_configuration_effective_energies_and_slopes",
                "extra_solve_count": 0,
                "uses_existing_three_mass_top_correlator_scan": True,
                "physical_higgs_normalization": "not_derived",
                "used_as_physical_yukawa_readout": False,
                "strict_limit": (
                    "This serializes per-configuration top mass-scan slopes "
                    "already computed for the three-mass scan. It is future "
                    "same-ensemble covariance/subtraction support only, not "
                    "dE/dh and not a retained/proposed-retained y_t readout."
                ),
            },
            "schur_kprime_kernel_rows": {
                "enabled": False,
                "implementation_status": "absent_guarded",
                "required_measurement_objects": [
                    "neutral scalar kernel partition K=[[A,B^T],[B,C]] on the same Cl3/Z3 surface",
                    "A(pole) and A_prime(pole) for the source-pole coordinate",
                    "B(pole) and B_prime(pole) for source-orthogonal neutral mixing",
                    "C(pole), C_prime(pole), and C_inverse(pole) for the orthogonal neutral block",
                    "pole isolation, finite-volume, finite-spacing, model-class, and identity certificates",
                ],
                "finite_source_only_c_ss_is_not_schur_rows": True,
                "used_as_physical_yukawa_readout": False,
                "strict_limit": (
                    "Same-source C_ss(q) rows and finite source-response slopes "
                    "must not be treated as Schur A/B/C kernel rows or as a "
                    "K-prime closure certificate.  The Schur sufficiency theorem "
                    "requires explicit same-surface kernel partition rows and "
                    "pole derivatives."
                ),
            },
            "fh_lsz_measurement_policy": fh_lsz_policy,
            "source_higgs_cross_correlator": {
                "enabled": source_higgs_enabled,
                "implementation_status": (
                    "finite_mode_measurement_enabled_pending_pole_residue_gate"
                    if source_higgs_enabled
                    else "absent_guarded"
                ),
                "required_measurement_objects": [
                    "O_H or radial canonical-Higgs observable on the same Cl3/Z3 source surface",
                    "C_sH(q)=<O_s(q) O_H(-q)> pole rows",
                    "C_HH(q)=<O_H(q) O_H(-q)> pole rows",
                    "same-ensemble C_ss/C_sH/C_HH covariance",
                ],
                "canonical_higgs_operator_realization": (
                    "certificate_supplied_unratified"
                    if source_higgs_enabled
                    else "absent"
                ),
                "operator": source_higgs_operator,
                "firewall": source_higgs_firewall,
                "modes": getattr(args, "source_higgs_cross_modes_parsed", []),
                "noise_vectors_per_configuration": int(getattr(args, "source_higgs_cross_noises", 0)),
                "selected_mass_only": bool(
                    fh_lsz_policy.get("source_higgs_cross_correlator_selected_mass_only", False)
                ),
                "selected_mass_parameter": fh_lsz_policy.get("selected_mass_parameter"),
                "used_as_physical_yukawa_readout": False,
                "strict_limit": (
                    "Finite-mode source-Higgs rows are not pole residues and "
                    "must not be treated as source-Higgs Gram purity or "
                    "canonical-Higgs normalization evidence until the "
                    "source-Higgs certificate builder, Gram-purity postprocessor, "
                    "and retained-route gates pass."
                ),
            },
            "source_higgs_time_kernel": {
                "enabled": source_higgs_time_kernel_enabled,
                "implementation_status": (
                    "same_surface_time_kernel_rows_enabled_support_only"
                    if source_higgs_time_kernel_enabled
                    else "absent_guarded"
                ),
                "required_measurement_objects": [
                    "same-surface Euclidean-time C_ss(t), C_sH(t), C_Hs(t), C_HH(t) rows",
                    "same-source covariance across matrix entries and time lags",
                    "canonical O_H or physical neutral transfer identity certificate",
                    "OS/GEVP pole extraction with FV/IR/threshold authority",
                    "source-overlap and canonical-Higgs normalization authority",
                ],
                "time_kernel_schema_version": (
                    "source_higgs_time_kernel_v1"
                    if source_higgs_time_kernel_enabled
                    else "disabled"
                ),
                "canonical_higgs_operator_realization": (
                    "certificate_supplied_unratified"
                    if source_higgs_time_kernel_enabled
                    else "absent"
                ),
                "operator": source_higgs_operator,
                "firewall": source_higgs_firewall,
                "modes": getattr(args, "source_higgs_time_kernel_modes_parsed", []),
                "noise_vectors_per_configuration": int(
                    getattr(args, "source_higgs_time_kernel_noises", 0)
                ),
                "max_tau": int(getattr(args, "source_higgs_time_kernel_max_tau", 0)),
                "origin_count": int(getattr(args, "source_higgs_time_kernel_origin_count", 1)),
                "selected_mass_only": bool(
                    fh_lsz_policy.get("source_higgs_time_kernel_selected_mass_only", False)
                ),
                "selected_mass_parameter": fh_lsz_policy.get("selected_mass_parameter"),
                "physical_higgs_normalization": "not_derived",
                "used_as_physical_yukawa_readout": False,
                "strict_limit": (
                    "Same-surface time-kernel rows are transfer-kernel/GEVP "
                    "instrumentation only. They must not be treated as physical "
                    "source-Higgs pole residues, kappa_s, or y_t evidence until "
                    "canonical O_H or physical neutral transfer identity, "
                    "pole/FV/IR/threshold authority, overlap normalization, "
                    "and retained-route gates pass."
                ),
            },
            "wz_mass_response": {
                "enabled": wz_smoke_enabled,
                "implementation_status": (
                    "smoke_schema_enabled_not_ew_production"
                    if wz_smoke_enabled
                    else "absent_guarded"
                ),
                "required_measurement_objects": [
                    "same-source W/Z correlator mass fits",
                    "fitted dM_W/ds or dM_Z/ds under the same scalar source",
                    "covariance with dE_top/ds",
                    "sector-overlap and canonical-Higgs identity certificates",
                ],
                "smoke_schema_status": (
                    "scout_contract_rows_enabled_not_production_evidence"
                    if wz_smoke_enabled
                    else "disabled"
                ),
                "boson_channel": getattr(args, "wz_boson_channel", "W"),
                "source_shifts": getattr(args, "wz_source_shifts_parsed", []),
                "same_source_identity_certified": False,
                "production_wz_rows_written": False,
                "used_as_physical_yukawa_readout": False,
                "strict_limit": (
                    "The optional W/Z smoke path emits synthetic positive "
                    "correlators for schema validation only.  This QCD "
                    "top-correlator harness still does not produce same-source "
                    "EW W/Z mass-response evidence.  Static EW algebra, smoke "
                    "slopes, or absent W/Z slopes must not be used as dM_W/ds "
                    "physics evidence."
                ),
            },
            "evidence_scope": evidence_scope,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "run_control": {
                "seed": int(args.seed),
                "volumes": args.volumes,
                "masses": [float(x) for x in args.masses.split(",") if x.strip()],
                "thermalization_sweeps": int(args.therm),
                "measurement_sweeps": int(args.measurements),
                "measurement_separation_sweeps": int(args.separation),
                "overrelaxation_sweeps": int(args.overrelax),
                "engine": resolve_engine(args),
                "seed_control_version": (
                    "numba_gauge_seed_v1"
                    if resolve_engine(args) == "numba"
                    else "python_generator_v1"
                ),
                "production_targets": bool(args.production_targets),
                "pilot_targets": bool(args.pilot_targets),
                "momentum_modes": getattr(args, "momentum_modes_parsed", []),
                "scalar_source_shifts": getattr(args, "scalar_source_shifts_parsed", []),
                "scalar_two_point_modes": getattr(args, "scalar_two_point_modes_parsed", []),
                "scalar_two_point_noises": int(getattr(args, "scalar_two_point_noises", 0)),
                "source_higgs_cross_modes": getattr(args, "source_higgs_cross_modes_parsed", []),
                "source_higgs_cross_noises": int(getattr(args, "source_higgs_cross_noises", 0)),
                "source_higgs_time_kernel_modes": getattr(
                    args, "source_higgs_time_kernel_modes_parsed", []
                ),
                "source_higgs_time_kernel_noises": int(
                    getattr(args, "source_higgs_time_kernel_noises", 0)
                ),
                "source_higgs_time_kernel_max_tau": int(
                    getattr(args, "source_higgs_time_kernel_max_tau", 0)
                ),
                "source_higgs_time_kernel_origin_count": int(
                    getattr(args, "source_higgs_time_kernel_origin_count", 1)
                ),
                "source_higgs_operator_certificate": (
                    str(args.source_higgs_operator_certificate)
                    if getattr(args, "source_higgs_operator_certificate", None) is not None
                    else None
                ),
                "wz_mass_response_smoke": bool(getattr(args, "wz_mass_response_smoke", False)),
                "wz_source_shifts": getattr(args, "wz_source_shifts_parsed", []),
                "wz_boson_channel": getattr(args, "wz_boson_channel", "W"),
                "fh_lsz_selected_mass_only": True,
                "fh_lsz_selected_mass_parameter": fh_lsz_policy.get("selected_mass_parameter"),
                "normal_equation_cache_enabled": True,
                "production_output_dir": str(args.production_output_dir),
            },
        },
        "v_input": {
            "source": "existing electroweak VEV chain",
            "treatment": "substrate_input_only",
            "v_GeV": V_GEV,
        },
        "ensembles": ensembles,
        "result": result,
        "ratio_check": {
            "y_t_lattice": ratio_y,
            "g_s_lattice": g_s_lattice,
            "g_s_source": ratio_source,
            "ratio": ratio,
            "uncertainty": ratio_uncertainty,
            "used_as_definition": False,
        },
    }


def time_component(name: str, fn: Any) -> tuple[float, Any]:
    t0 = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - t0
    print(f"  benchmark {name}: {elapsed:.6f}s", flush=True)
    return elapsed, result


def estimate_campaign_seconds(component_seconds: dict[str, float], volume: int) -> dict[str, float]:
    baseline_volume = 12**3 * 24
    volume_scale = volume / baseline_volume
    heatbath = component_seconds["heatbath_sweep"] * volume_scale
    overrelax = component_seconds["overrelax_sweep"] * volume_scale
    plaquette = component_seconds["plaquette"] * volume_scale
    ape = component_seconds["ape_smear_one_step"] * volume_scale
    measure_one_mass = component_seconds["measure_correlator_one_mass"] * volume_scale

    therm_sweeps = 1000
    saved_configurations = 1000
    separation_sweeps = 20
    overrelax_per_sweep = 4
    masses = 3

    gauge_sweeps = therm_sweeps + saved_configurations * separation_sweeps
    gauge_evolution = gauge_sweeps * (heatbath + overrelax_per_sweep * overrelax)
    plaquette_measurement = (therm_sweeps + saved_configurations) * plaquette
    correlator_measurement = saved_configurations * (ape + masses * measure_one_mass)
    total = gauge_evolution + plaquette_measurement + correlator_measurement
    return {
        "volume_scale_from_12x24": volume_scale,
        "gauge_sweeps": float(gauge_sweeps),
        "gauge_evolution_seconds": gauge_evolution,
        "plaquette_seconds": plaquette_measurement,
        "correlator_measurement_seconds": correlator_measurement,
        "total_seconds": total,
        "total_days": total / 86400.0,
    }


def run_production_benchmark(args: argparse.Namespace) -> int:
    PRODUCTION_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    volume_dir = PRODUCTION_OUTPUT_DIR / "L12xT24"
    volume_dir.mkdir(parents=True, exist_ok=True)

    engine = resolve_engine(args)
    rng = np.random.default_rng(args.seed)
    geom = Geometry(12, 24)
    component_seconds: dict[str, float] = {}

    print("=" * 78)
    print("YT direct lattice correlator production-scale benchmark")
    print("=" * 78)
    print("This benchmark is not a production certificate and does not update y_t.")
    print(f"geometry=12^3 x 24, volume={geom.volume}, matrix_size={geom.volume * NC}, engine={engine}")

    warmup_seconds = 0.0
    if engine == "numba":
        warmup_seconds = warm_numba_kernels(args.seed)
        print(f"  numba warmup/compile: {warmup_seconds:.6f}s", flush=True)
        init_seconds, u = time_component("gauge_init", lambda: cold_link_array(geom))
        component_seconds["gauge_init"] = init_seconds
        nb_seed(args.seed)
        component_seconds["heatbath_sweep"], _ = time_component("heatbath_sweep", lambda: nb_heatbath_sweep(u, BETA))
        component_seconds["overrelax_sweep"], _ = time_component("overrelax_sweep", lambda: nb_overrelax_sweep(u))
        component_seconds["plaquette"], plaquette_value = time_component("plaquette", lambda: nb_plaquette(u))
        gauge = gauge_field_from_array(geom, u)
        component_seconds["ape_smear_one_step"], smeared = time_component(
            "ape_smear_one_step", lambda: ape_smear_spatial(gauge, args.ape_alpha, 1)
        )
    else:
        init_seconds, gauge = time_component("gauge_init", lambda: GaugeField(geom))
        component_seconds["gauge_init"] = init_seconds
        component_seconds["heatbath_sweep"], _ = time_component("heatbath_sweep", lambda: gauge.heatbath_sweep(rng))
        component_seconds["overrelax_sweep"], _ = time_component("overrelax_sweep", gauge.overrelax_sweep)
        component_seconds["plaquette"], plaquette_value = time_component("plaquette", gauge.plaquette)
        component_seconds["ape_smear_one_step"], smeared = time_component(
            "ape_smear_one_step", lambda: ape_smear_spatial(gauge, args.ape_alpha, 1)
        )

    dirac_seconds, dirac = time_component("dirac_build_one_mass", lambda: build_staggered_dirac(smeared, 0.75))
    component_seconds["dirac_build_one_mass"] = dirac_seconds
    cg_seconds, cg_result = time_component(
        "single_cg_solve", lambda: solve_propagator_normal_eq(dirac, 0, args.cg_rtol, args.cg_maxiter)
    )
    component_seconds["single_cg_solve"] = cg_seconds
    measure_seconds, measured = time_component(
        "measure_correlator_one_mass",
        lambda: measure_correlator(smeared, 0.75, args.cg_rtol, args.cg_maxiter),
    )
    component_seconds["measure_correlator_one_mass"] = measure_seconds

    profile_text = None
    if args.profile_heatbath:
        profile_path = volume_dir / f"heatbath_profile_{engine}.txt"
        if engine == "python":
            profile_gauge = GaugeField(geom)
            profile = cProfile.Profile()
            t0 = time.perf_counter()
            profile.enable()
            profile_gauge.heatbath_sweep(np.random.default_rng(args.seed + 1))
            profile.disable()
            profile_elapsed = time.perf_counter() - t0
            stream = io.StringIO()
            pstats.Stats(profile, stream=stream).sort_stats("cumtime").print_stats(25)
            profile_text = f"PROFILE_ELAPSED_SECONDS {profile_elapsed:.6f}\n{stream.getvalue()}".rstrip() + "\n"
        else:
            profile_u = cold_link_array(geom)
            nb_seed(args.seed + 1)
            t0 = time.perf_counter()
            nb_heatbath_sweep(profile_u, BETA)
            profile_elapsed = time.perf_counter() - t0
            profile_text = (
                f"NUMBA_PROFILE_ELAPSED_SECONDS {profile_elapsed:.6f}\n"
                "Numba nopython kernel: Python cProfile cannot attribute time inside compiled loops.\n"
                "Use component_seconds.heatbath_sweep in the JSON benchmark for the production estimate.\n"
            )
        profile_path.write_text(profile_text, encoding="utf-8")
    else:
        profile_path = None

    estimates = {
        "12x24": estimate_campaign_seconds(component_seconds, 12**3 * 24),
        "16x32": estimate_campaign_seconds(component_seconds, 16**3 * 32),
        "24x48": estimate_campaign_seconds(component_seconds, 24**3 * 48),
    }
    total_days = sum(item["total_days"] for item in estimates.values())
    dirac_nnz_per_site = int(dirac.nnz // geom.volume)
    memory_notes = {
        "dirac_matrix_shape_12x24": list(dirac.shape),
        "dirac_nnz_12x24": int(dirac.nnz),
        "dirac_nnz_per_lattice_site": dirac_nnz_per_site,
        "estimated_dirac_nnz_24x48": dirac_nnz_per_site * (24**3 * 48),
        "normal_equation_note": "CG currently forms D^dagger D explicitly per source; memory pressure grows beyond the raw D matrix.",
    }
    benchmark = {
        "metadata": {
            "artifact": "production_scale_benchmark_not_certificate",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "numba_available": NUMBA_AVAILABLE,
            "numba_warmup_seconds": warmup_seconds,
            "engine": engine,
            "scipy_sparse_cg": "scipy.sparse.linalg.cg",
            "seed": args.seed,
        },
        "geometry": {
            "spatial_L": 12,
            "time_L": 24,
            "volume": geom.volume,
            "matrix_size": geom.volume * NC,
        },
        "component_seconds": component_seconds,
        "component_results": {
            "plaquette_after_one_sweep": plaquette_value,
            "single_cg_info": int(cg_result[1]),
            "single_cg_residual": float(cg_result[2]),
            "measure_correlator_max_cg_residual": measured["max_cg_residual"],
            "measure_correlator_cg_infos": measured["cg_infos"],
            "measure_correlator_time_slices": len(measured["correlator"]),
        },
        "production_protocol": {
            "thermalization_sweeps": 1000,
            "saved_configurations_per_volume": 1000,
            "separation_sweeps": 20,
            "overrelaxation_sweeps_per_heatbath": 4,
            "mass_points": 3,
        },
        "linear_volume_extrapolation": estimates,
        "total_three_volume_estimate_days": total_days,
        "bottleneck": {
            "primary": "gauge evolution",
            "detail": "At 12^3 x 24, one heat-bath sweep plus four overrelaxation sweeps is about "
            f"{component_seconds['heatbath_sweep'] + 4 * component_seconds['overrelax_sweep']:.2f}s before plaquette/correlator work.",
            "strict_campaign_status": "not_completed_in_this_environment",
        },
        "memory_notes": memory_notes,
        "profile_path": str(profile_path.relative_to(REPO_ROOT)) if profile_path is not None else None,
    }
    benchmark_path = volume_dir / f"production_scale_benchmark_{engine}_2026-04-30.json"
    benchmark_path.write_text(json.dumps(benchmark, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("\nBENCHMARK SUMMARY")
    print(f"  12x24 heatbath sweep        = {component_seconds['heatbath_sweep']:.6f}s")
    print(f"  12x24 overrelax sweep       = {component_seconds['overrelax_sweep']:.6f}s")
    print(f"  12x24 one-mass correlator   = {component_seconds['measure_correlator_one_mass']:.6f}s")
    print(f"  estimated three-volume run  = {total_days:.2f} days")
    print(f"  wrote benchmark             = {benchmark_path}")
    if profile_path is not None:
        print(f"  wrote heatbath profile       = {profile_path}")
    print("\nProduction campaign not completed; strict certificate is not updated.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volumes", default=None, help="Comma-separated Ls x Lt list, e.g. 12x24,16x32,24x48.")
    parser.add_argument("--masses", default="0.45,0.75,1.05", help="Comma-separated staggered bare masses.")
    parser.add_argument(
        "--momentum-modes",
        default="",
        help=(
            "Optional semicolon-separated spatial momentum triplets for kinetic-mass "
            "analysis, e.g. '0,0,0;1,0,0;1,1,0'."
        ),
    )
    parser.add_argument(
        "--scalar-source-shifts",
        default="",
        help=(
            "Optional comma-separated uniform scalar source shifts s applied as "
            "m_bare + s for Feynman-Hellmann dE/ds response analysis.  This "
            "does not define the physical Higgs normalization."
        ),
    )
    parser.add_argument(
        "--scalar-two-point-modes",
        default="",
        help=(
            "Optional semicolon-separated spatial momentum triplets for a "
            "same-source scalar two-point stochastic trace estimate, e.g. "
            "'0,0,0;1,0,0'. This is a kappa_s measurement primitive, not a "
            "physical Higgs normalization by itself."
        ),
    )
    parser.add_argument(
        "--scalar-two-point-noises",
        type=int,
        default=0,
        help="Z2 noise vectors per configuration for --scalar-two-point-modes. Zero disables the estimator.",
    )
    parser.add_argument(
        "--source-higgs-cross-modes",
        default="",
        help=(
            "Optional semicolon-separated spatial momentum triplets for "
            "same-ensemble C_ss/C_sH/C_HH source-Higgs cross-correlator rows. "
            "Requires --source-higgs-operator-certificate and "
            "--source-higgs-cross-noises > 0.  This is not a y_t readout."
        ),
    )
    parser.add_argument(
        "--source-higgs-cross-noises",
        type=int,
        default=0,
        help="Z2 noise vectors per configuration for --source-higgs-cross-modes. Zero disables the estimator.",
    )
    parser.add_argument(
        "--source-higgs-time-kernel-modes",
        default="",
        help=(
            "Optional semicolon-separated spatial momentum triplets for "
            "same-surface Euclidean-time C_ss/C_sH/C_Hs/C_HH(t) rows. "
            "Requires --source-higgs-operator-certificate and "
            "--source-higgs-time-kernel-noises > 0. This is transfer-kernel "
            "instrumentation only, not a y_t readout."
        ),
    )
    parser.add_argument(
        "--source-higgs-time-kernel-noises",
        type=int,
        default=0,
        help="Z2 noise vectors per configuration for --source-higgs-time-kernel-modes. Zero disables the estimator.",
    )
    parser.add_argument(
        "--source-higgs-time-kernel-max-tau",
        type=int,
        default=0,
        help="Maximum Euclidean time lag tau for --source-higgs-time-kernel-modes.",
    )
    parser.add_argument(
        "--source-higgs-time-kernel-origin-count",
        type=int,
        default=1,
        help="Number of source time origins for --source-higgs-time-kernel-modes.",
    )
    parser.add_argument(
        "--source-higgs-operator-certificate",
        type=Path,
        default=None,
        help=(
            "JSON certificate describing a same-surface canonical-Higgs "
            "diagonal vertex for source-Higgs cross-correlator instrumentation. "
            "The certificate carries the identity burden; the harness only measures rows."
        ),
    )
    parser.add_argument(
        "--wz-source-shifts",
        default="",
        help=(
            "Optional comma-separated source shifts for W/Z mass-response smoke "
            "schema rows. Requires --wz-mass-response-smoke. These rows are "
            "synthetic contract plumbing only, not EW production evidence."
        ),
    )
    parser.add_argument(
        "--wz-boson-channel",
        choices=("W", "Z"),
        default="W",
        help="Boson label for --wz-mass-response-smoke schema rows.",
    )
    parser.add_argument(
        "--wz-mass-response-smoke",
        action="store_true",
        help=(
            "Emit default-off W/Z mass-response smoke rows from positive "
            "synthetic correlators to validate schema plumbing. This never "
            "creates production W/Z evidence or y_t readout authority."
        ),
    )
    parser.add_argument("--therm", type=int, default=None, help="Thermalization sweeps.")
    parser.add_argument("--measurements", type=int, default=None, help="Saved configurations per volume.")
    parser.add_argument("--separation", type=int, default=None, help="Sweeps between saved configurations.")
    parser.add_argument("--overrelax", type=int, default=None, help="Overrelaxation sweeps after each heat-bath sweep.")
    parser.add_argument("--ape-steps", type=int, default=1, help="APE smearing steps for measurement links.")
    parser.add_argument("--ape-alpha", type=float, default=0.5, help="APE smearing alpha.")
    parser.add_argument("--cg-rtol", type=float, default=1.0e-8, help="CG relative residual target.")
    parser.add_argument("--cg-maxiter", type=int, default=2000, help="CG max iterations.")
    parser.add_argument("--seed", type=int, default=20260430, help="Random seed.")
    parser.add_argument("--output", type=Path, default=DEFAULT_CERTIFICATE, help="Certificate JSON output path.")
    parser.add_argument("--g-s-lattice", type=float, default=None, help="Independently measured lattice g_s for ratio check.")
    parser.add_argument("--g-s-uncertainty", type=float, default=None, help="Uncertainty for --g-s-lattice.")
    parser.add_argument(
        "--g-s-source",
        default=None,
        help="Source label for g_s. Strict requires 'independent_direct_measurement'.",
    )
    parser.add_argument(
        "--production-output-dir",
        type=Path,
        default=PRODUCTION_OUTPUT_DIR,
        help="Directory for per-volume production artifacts and benchmarks.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reuse existing per-volume artifacts from --production-output-dir when present.",
    )
    parser.add_argument(
        "--archive-copy",
        action="store_true",
        help="Always write a timestamped archive copy under outputs/yt_direct_lattice_correlator.",
    )
    parser.add_argument(
        "--engine",
        choices=("auto", "python", "numba"),
        default="auto",
        help="Gauge-update engine. auto uses numba when available and falls back to python.",
    )
    parser.add_argument(
        "--benchmark-production",
        action="store_true",
        help="Benchmark the 12^3 x 24 production-scale components and write a non-certificate artifact.",
    )
    parser.add_argument(
        "--profile-heatbath",
        action="store_true",
        help="With --benchmark-production, also write a cProfile report for one 12^3 x 24 heat-bath sweep.",
    )
    parser.add_argument(
        "--production-targets",
        action="store_true",
        help="Mark the run as production-targeted. This does not override strict validation thresholds.",
    )
    parser.add_argument(
        "--pilot-targets",
        action="store_true",
        help="Run a bounded 12^3 x 24 pilot lane. This is explicitly non-retained and strict should reject it.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.production_targets and args.pilot_targets:
        raise SystemExit("--production-targets and --pilot-targets are mutually exclusive")

    if args.benchmark_production:
        return run_production_benchmark(args)

    engine = resolve_engine(args)
    if engine == "numba":
        warmup_seconds = warm_numba_kernels(args.seed)
        print(f"numba warmup/compile: {warmup_seconds:.6f}s")

    output_was_default = args.output == DEFAULT_CERTIFICATE
    output_dir_was_default = args.production_output_dir == PRODUCTION_OUTPUT_DIR

    if args.production_targets:
        args.volumes = args.volumes or "12x24,16x32,24x48"
        args.therm = 1000 if args.therm is None else args.therm
        args.measurements = 1000 if args.measurements is None else args.measurements
        args.separation = 20 if args.separation is None else args.separation
        args.overrelax = 4 if args.overrelax is None else args.overrelax
    elif args.pilot_targets:
        args.volumes = args.volumes or "12x24"
        args.therm = 10 if args.therm is None else args.therm
        args.measurements = 3 if args.measurements is None else args.measurements
        args.separation = 2 if args.separation is None else args.separation
        args.overrelax = 2 if args.overrelax is None else args.overrelax
        if output_was_default:
            args.output = PILOT_CERTIFICATE
        if output_dir_was_default:
            args.production_output_dir = PILOT_OUTPUT_DIR
    else:
        args.volumes = args.volumes or "2x4,3x6"
        args.therm = 2 if args.therm is None else args.therm
        args.measurements = 3 if args.measurements is None else args.measurements
        args.separation = 1 if args.separation is None else args.separation
        args.overrelax = 1 if args.overrelax is None else args.overrelax

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    args.production_output_dir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    volumes = parse_volume_spec(args.volumes)
    masses = [float(x) for x in args.masses.split(",") if x.strip()]
    args.momentum_modes_parsed = parse_momentum_modes(args.momentum_modes)
    args.scalar_source_shifts_parsed = parse_float_list(args.scalar_source_shifts)
    args.scalar_two_point_modes_parsed = parse_momentum_modes(args.scalar_two_point_modes)
    args.source_higgs_cross_modes_parsed = parse_momentum_modes(args.source_higgs_cross_modes)
    args.source_higgs_time_kernel_modes_parsed = parse_momentum_modes(args.source_higgs_time_kernel_modes)
    args.wz_source_shifts_parsed = parse_float_list(args.wz_source_shifts)
    args.source_higgs_operator_certificate_data = load_source_higgs_operator_certificate(
        args.source_higgs_operator_certificate
    )
    if (args.source_higgs_cross_modes_parsed or args.source_higgs_cross_noises > 0) and not args.source_higgs_operator_certificate_data:
        print(
            "source_higgs_cross_correlator=disabled; "
            "--source-higgs-operator-certificate is required for C_sH/C_HH rows"
        )
    if (
        args.source_higgs_time_kernel_modes_parsed
        or args.source_higgs_time_kernel_noises > 0
    ) and not args.source_higgs_operator_certificate_data:
        print(
            "source_higgs_time_kernel=disabled; "
            "--source-higgs-operator-certificate is required for C_sH(t)/C_HH(t) rows"
        )
    rng = np.random.default_rng(args.seed)

    print("=" * 78)
    print("YT direct lattice correlator production harness")
    print("=" * 78)
    print(f"volumes={volumes}")
    print(f"masses={masses}")
    if args.momentum_modes_parsed:
        print(f"momentum_modes={args.momentum_modes_parsed}")
    if args.scalar_source_shifts_parsed:
        print(f"scalar_source_shifts={args.scalar_source_shifts_parsed}")
    if args.scalar_two_point_modes_parsed and args.scalar_two_point_noises > 0:
        print(
            f"scalar_two_point_modes={args.scalar_two_point_modes_parsed}, "
            f"noise_vectors={args.scalar_two_point_noises}"
        )
    if (
        args.source_higgs_cross_modes_parsed
        and args.source_higgs_cross_noises > 0
        and args.source_higgs_operator_certificate_data
    ):
        operator_id = args.source_higgs_operator_certificate_data.get("operator_id")
        print(
            f"source_higgs_cross_modes={args.source_higgs_cross_modes_parsed}, "
            f"noise_vectors={args.source_higgs_cross_noises}, operator_id={operator_id}"
        )
    if (
        args.source_higgs_time_kernel_modes_parsed
        and args.source_higgs_time_kernel_noises > 0
        and args.source_higgs_operator_certificate_data
    ):
        operator_id = args.source_higgs_operator_certificate_data.get("operator_id")
        print(
            f"source_higgs_time_kernel_modes={args.source_higgs_time_kernel_modes_parsed}, "
            f"noise_vectors={args.source_higgs_time_kernel_noises}, "
            f"max_tau={args.source_higgs_time_kernel_max_tau}, "
            f"origin_count={args.source_higgs_time_kernel_origin_count}, "
            f"operator_id={operator_id}"
        )
    if wz_mass_response_smoke_enabled(args):
        print(
            f"wz_mass_response_smoke_channel={args.wz_boson_channel}, "
            f"wz_source_shifts={args.wz_source_shifts_parsed}"
        )
    print(f"therm={args.therm}, measurements={args.measurements}, separation={args.separation}")
    print(f"output={args.output}")
    if args.pilot_targets:
        print("scope=pilot; strict runner is expected to reject this certificate")
    elif not args.production_targets:
        print("scope=reduced; strict runner is expected to reject this certificate")

    ensembles = []
    for spatial_l, time_l in volumes:
        artifact_path = volume_artifact_path(args.production_output_dir, spatial_l, time_l)
        if args.resume and artifact_path.exists():
            ensemble = load_volume_artifact(args.production_output_dir, spatial_l, time_l)
            print(f"  resume L={spatial_l}: loaded {artifact_path}")
        else:
            ensemble = run_volume(args, spatial_l, time_l, masses, rng)
            if args.production_targets or args.pilot_targets:
                written = write_volume_artifact(args.production_output_dir, ensemble)
                print(f"  wrote volume artifact: {written}")
        ensembles.append(ensemble)

    certificate = build_certificate(args, ensembles)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(certificate, f, indent=2, sort_keys=True)
        f.write("\n")
    stamped = None
    if args.archive_copy or args.output.resolve() == DEFAULT_CERTIFICATE.resolve():
        stamped = OUTPUT_DIR / f"yt_direct_lattice_correlator_{int(time.time())}.json"
        with stamped.open("w", encoding="utf-8") as f:
            json.dump(certificate, f, indent=2, sort_keys=True)
            f.write("\n")

    result = certificate["result"]
    print("\nRESULT SUMMARY")
    print(f"  m_t proxy       = {result['m_t_pole_GeV']:.6f} GeV")
    print(f"  y_t proxy       = {result['y_t_v']:.8f}")
    print(f"  total dm_t      = {result['total_m_t_pole_uncertainty_GeV']:.6f} GeV")
    print(f"  total dy_t      = {result['total_y_t_uncertainty']:.8f}")
    print(f"  wrote           = {args.output}")
    if stamped is not None:
        print(f"  archive copy    = {stamped}")
    if args.production_targets:
        print("\nThis production-targeted certificate is not retained evidence unless the strict runner passes.")
    elif args.pilot_targets:
        print("\nThis pilot certificate is not retained evidence and is expected to fail strict production validation.")
    else:
        print("\nThis reduced certificate is not retained evidence unless the strict runner passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
