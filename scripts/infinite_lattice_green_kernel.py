#!/usr/bin/env python3
"""Gauge-fixed free-space 2D discrete Green kernel for the lattice Laplacian.

The kernel is constructed by solving the 5-point Poisson equation on an
expanded domain with asymptotically matched logarithmic boundary values, then
gauge-fixing by pinning G(0,0)=0. This provides a reusable approximation to
the infinite-lattice Green function:

    (L G)(dy, dz) = -delta_{dy,0} delta_{dz,0}
    G(0,0) = 0
"""

from __future__ import annotations

import math
from functools import lru_cache

def _asymptotic_boundary_value(dy: int, dz: int) -> float:
    r = math.hypot(dy, dz)
    if r <= 0.0:
        return 0.0
    return -math.log(r) / (2.0 * math.pi)


@lru_cache(maxsize=16)
def gauge_fixed_green_kernel_2d(
    max_offset: int,
    solve_halfwidth: int | None = None,
    tol: float = 1e-8,
    max_iter: int = 4000,
    omega: float = 1.9,
) -> tuple[tuple[float, ...], ...]:
    """Return cached kernel values for offsets dy,dz in [-max_offset, max_offset].

    Args:
      max_offset: largest absolute offset needed along either axis.
      solve_halfwidth: optional half-width for the expanded solve domain.
        Must be larger than max_offset. When omitted, uses a conservative
        default based on max_offset.
    """
    if max_offset < 0:
        raise ValueError("max_offset must be non-negative")
    if solve_halfwidth is None:
        solve_halfwidth = max(64, max_offset + 32)
    if solve_halfwidth <= max_offset:
        raise ValueError("solve_halfwidth must satisfy solve_halfwidth > max_offset")

    r = int(solve_halfwidth)
    n = 2 * r + 1
    c = r

    g = [[0.0] * n for _ in range(n)]

    for iy in range(n):
        dy = iy - c
        g[iy][0] = _asymptotic_boundary_value(dy, -c)
        g[iy][n - 1] = _asymptotic_boundary_value(dy, c)
    for iz in range(n):
        dz = iz - c
        g[0][iz] = _asymptotic_boundary_value(-c, dz)
        g[n - 1][iz] = _asymptotic_boundary_value(c, dz)

    for _ in range(max_iter):
        max_delta = 0.0
        for iy in range(1, n - 1):
            row = g[iy]
            up = g[iy - 1]
            dn = g[iy + 1]
            for iz in range(1, n - 1):
                src = 1.0 if (iy == c and iz == c) else 0.0
                rhs = 0.25 * (up[iz] + dn[iz] + row[iz - 1] + row[iz + 1] + src)
                old = row[iz]
                new = old + omega * (rhs - old)
                delta = abs(new - old)
                if delta > max_delta:
                    max_delta = delta
                row[iz] = new
        if max_delta < tol:
            break

    gauge_shift = g[c][c]
    for iy in range(n):
        row = g[iy]
        for iz in range(n):
            row[iz] -= gauge_shift
    g[c][c] = 0.0

    out_n = 2 * max_offset + 1
    kernel = [[0.0] * out_n for _ in range(out_n)]
    for idy, dy in enumerate(range(-max_offset, max_offset + 1)):
        src_row = g[c + dy]
        dst_row = kernel[idy]
        start = c - max_offset
        stop = c + max_offset + 1
        for idz, val in enumerate(src_row[start:stop]):
            dst_row[idz] = float(val)

    return tuple(tuple(row) for row in kernel)
