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
* Point-source staggered correlator measurement, effective-mass fit, jackknife
  statistical errors, and strict-runner certificate emission.

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


def solve_propagator_normal_eq(D: sparse.csr_matrix, source_index: int, rtol: float, maxiter: int) -> tuple[np.ndarray, int, float]:
    rhs = np.zeros(D.shape[0], dtype=complex)
    rhs[source_index] = 1.0
    dh = D.getH()
    normal = dh @ D
    b = dh @ rhs
    sol, info = cg(normal, b, rtol=rtol, atol=0.0, maxiter=maxiter)
    residual = float(np.linalg.norm(normal @ sol - b) / max(np.linalg.norm(b), 1.0e-30))
    return sol, int(info), residual


def measure_correlator(gauge: GaugeField, mass: float, rtol: float, maxiter: int) -> dict[str, Any]:
    D = build_staggered_dirac(gauge, mass)
    geom = gauge.geom
    corr = np.zeros(geom.time_l, dtype=float)
    infos: list[int] = []
    residuals: list[float] = []
    source_site = geom.site_index((0, 0, 0, 0))
    for source_color in range(NC):
        source_index = source_site * NC + source_color
        sol, info, residual = solve_propagator_normal_eq(D, source_index, rtol, maxiter)
        infos.append(info)
        residuals.append(residual)
        for site in range(geom.volume):
            t = geom.site_coords(site)[0]
            block = sol[site * NC:(site + 1) * NC]
            corr[t] += float(np.vdot(block, block).real)
    corr /= NC
    return {
        "mass": mass,
        "correlator": corr.tolist(),
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


def physical_mass_gev(m_lat: float) -> float:
    a_inv = R0_OVER_A_BETA6_REFERENCE * HBARC_GEV_FM / R0_FM
    return m_lat * a_inv


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
    cg_residuals: dict[float, list[float]] = {m: [] for m in masses}
    plaquettes = []
    for cfg in range(args.measurements):
        for _ in range(args.separation):
            gauge.heatbath_sweep(rng)
            for _ in range(args.overrelax):
                gauge.overrelax_sweep()
        plaquettes.append(gauge.plaquette())
        meas_gauge = ape_smear_spatial(gauge, args.ape_alpha, args.ape_steps) if args.ape_steps else gauge
        for mass in masses:
            measured = measure_correlator(meas_gauge, mass, args.cg_rtol, args.cg_maxiter)
            measurements[mass].append(measured["correlator"])
            cg_residuals[mass].append(float(measured["max_cg_residual"]))
        print(f"  meas L={spatial_l} cfg={cfg + 1}/{args.measurements} plaquette={plaquettes[-1]:.6f}")

    mass_scan = []
    selected_fit: dict[str, Any] | None = None
    selected_mass = masses[len(masses) // 2]
    correlator_rows = []
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
        "selected_mass_parameter": selected_mass,
        "correlators": correlator_rows,
        "effective_mass": effective_mass(np.array([r["mean"] for r in correlator_rows])),
        "mass_fit": selected_fit,
        "runtime_seconds": elapsed,
    }


def run_volume_numba(args: argparse.Namespace, spatial_l: int, time_l: int, masses: list[float]) -> dict[str, Any]:
    geom = Geometry(spatial_l, time_l)
    u = cold_link_array(geom)
    t0 = time.time()
    plaquette_history = []
    for sweep in range(args.therm):
        nb_heatbath_sweep(u, BETA)
        for _ in range(args.overrelax):
            nb_overrelax_sweep(u)
        plaquette_history.append(float(nb_plaquette(u)))
        print(f"  therm L={spatial_l} sweep={sweep + 1}/{args.therm} plaquette={plaquette_history[-1]:.6f}")

    measurements: dict[float, list[list[float]]] = {m: [] for m in masses}
    cg_residuals: dict[float, list[float]] = {m: [] for m in masses}
    plaquettes = []
    for cfg in range(args.measurements):
        for _ in range(args.separation):
            nb_heatbath_sweep(u, BETA)
            for _ in range(args.overrelax):
                nb_overrelax_sweep(u)
        plaquettes.append(float(nb_plaquette(u)))
        gauge_view = gauge_field_from_array(geom, u)
        meas_gauge = ape_smear_spatial(gauge_view, args.ape_alpha, args.ape_steps) if args.ape_steps else gauge_view
        for mass in masses:
            measured = measure_correlator(meas_gauge, mass, args.cg_rtol, args.cg_maxiter)
            measurements[mass].append(measured["correlator"])
            cg_residuals[mass].append(float(measured["max_cg_residual"]))
        print(f"  meas L={spatial_l} cfg={cfg + 1}/{args.measurements} plaquette={plaquettes[-1]:.6f}")

    mass_scan = []
    selected_fit: dict[str, Any] | None = None
    selected_mass = masses[len(masses) // 2]
    correlator_rows = []
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
        "thermalization_sweeps": args.therm,
        "measurement_sweeps": args.measurements,
        "measurement_separation_sweeps": args.separation,
        "ape_smearing": {"steps": args.ape_steps, "alpha": args.ape_alpha},
        "plaquette_history": [float(x) for x in plaquette_history],
        "plaquette_measurements": [float(x) for x in plaquettes],
        "plaquette_mean": float(np.mean(plaquettes)) if plaquettes else None,
        "mass_parameter_scan": mass_scan,
        "selected_mass_parameter": selected_mass,
        "correlators": correlator_rows,
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
    # This is not a measured g_s in reduced scope; the strict runner should reject it.
    ratio = None
    if isinstance(ratio_y, float) and math.isfinite(ratio_y):
        ratio = ratio_y / 1.0
    return {
        "metadata": {
            "authority": "staggered_top_correlator_mass_extraction",
            "phase": "production" if args.production_targets else "reduced_scope",
            "action": "Cl3Z3_SU3_Wilson_staggered",
            "g_bare": 1.0,
            "uses_prior_ward_chain": False,
            "uses_composite_matrix_element_route": False,
            "uses_coupling_definition_route": False,
            "scale_anchor": "Sommer r0 = 0.5 fm external anchor; r0/a reference used for reduced run",
            "running_bridge": "reduced run uses no authoritative SM RGE; production certificate must supply 4/5-loop bridge",
            "evidence_scope": "reduced run is infrastructure evidence only" if not args.production_targets else "user-requested production targets",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
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
            "g_s_lattice": 1.0,
            "g_s_source": "not_measured_reduced_scope",
            "ratio": ratio,
            "uncertainty": result.get("total_y_t_uncertainty"),
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.benchmark_production:
        return run_production_benchmark(args)

    engine = resolve_engine(args)
    if engine == "numba":
        warmup_seconds = warm_numba_kernels(args.seed)
        print(f"numba warmup/compile: {warmup_seconds:.6f}s")

    if args.production_targets:
        args.volumes = args.volumes or "12x24,16x32,24x48"
        args.therm = 1000 if args.therm is None else args.therm
        args.measurements = 1000 if args.measurements is None else args.measurements
        args.separation = 20 if args.separation is None else args.separation
        args.overrelax = 4 if args.overrelax is None else args.overrelax
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
    rng = np.random.default_rng(args.seed)

    print("=" * 78)
    print("YT direct lattice correlator production harness")
    print("=" * 78)
    print(f"volumes={volumes}")
    print(f"masses={masses}")
    print(f"therm={args.therm}, measurements={args.measurements}, separation={args.separation}")
    print(f"output={args.output}")
    if not args.production_targets:
        print("scope=reduced; strict runner is expected to reject this certificate")

    ensembles = []
    for spatial_l, time_l in volumes:
        artifact_path = volume_artifact_path(args.production_output_dir, spatial_l, time_l)
        if args.resume and artifact_path.exists():
            ensemble = load_volume_artifact(args.production_output_dir, spatial_l, time_l)
            print(f"  resume L={spatial_l}: loaded {artifact_path}")
        else:
            ensemble = run_volume(args, spatial_l, time_l, masses, rng)
            if args.production_targets:
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
    else:
        print("\nThis reduced certificate is not retained evidence unless the strict runner passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
