#!/usr/bin/env python3
"""Helpers for periodic-lattice minimum-image geometry."""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def infer_periodic_extents(pos: np.ndarray) -> tuple[int, ...]:
    """Infer integer periodic extents from lattice coordinates.

    Assumes coordinates sit on a unit lattice, optionally with small jitter.
    """
    extents: list[int] = []
    for axis in range(pos.shape[1]):
        width = float(np.max(pos[:, axis]) - np.min(pos[:, axis])) + 1.0
        extents.append(max(1, int(round(width))))
    return tuple(extents)


def minimum_image_displacement(point_a: Sequence[float],
                               point_b: Sequence[float],
                               extents: Sequence[int]) -> tuple[float, ...]:
    """Return the minimum-image displacement from point_a to point_b."""
    disp = [float(b) - float(a) for a, b in zip(point_a, point_b)]
    for axis, extent in enumerate(extents):
        if extent <= 1:
            continue
        half = 0.5 * float(extent)
        if disp[axis] > half:
            disp[axis] -= float(extent)
        elif disp[axis] < -half:
            disp[axis] += float(extent)
    return tuple(disp)


def minimum_image_distance(point_a: Sequence[float],
                           point_b: Sequence[float],
                           extents: Sequence[int]) -> float:
    """Euclidean norm of the minimum-image displacement."""
    disp = minimum_image_displacement(point_a, point_b, extents)
    return math.hypot(*disp)
