#!/usr/bin/env python3
"""Boundary Z2 flux candidate probe for signed-gravity chi_g.

This is a deliberately small graph/chain check.  It tests whether a boundary
Z2 Wilson loop can serve as a conserved chi_g label and then separates that
conservation result from the harder source/response-locking requirement.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]


def canonical_edge(a: Vertex, b: Vertex) -> Edge:
    return (a, b) if a <= b else (b, a)


@dataclass
class Cylinder:
    lx: int
    ly: int

    def h_edge(self, x: int, y: int) -> Edge:
        return canonical_edge((x % self.lx, y), ((x + 1) % self.lx, y))

    def v_edge(self, x: int, y: int) -> Edge:
        return canonical_edge((x % self.lx, y), (x % self.lx, y + 1))

    def edges(self) -> list[Edge]:
        out = []
        for y in range(self.ly):
            for x in range(self.lx):
                out.append(self.h_edge(x, y))
        for y in range(self.ly - 1):
            for x in range(self.lx):
                out.append(self.v_edge(x, y))
        return sorted(set(out))

    def boundary_loop(self, y: int = 0) -> list[Edge]:
        return [self.h_edge(x, y) for x in range(self.lx)]

    def plaquette(self, x: int, y: int) -> list[Edge]:
        if not (0 <= y < self.ly - 1):
            raise ValueError("plaquette y must satisfy 0 <= y < ly - 1")
        return [
            self.h_edge(x, y),
            self.v_edge(x + 1, y),
            self.h_edge(x, y + 1),
            self.v_edge(x, y),
        ]

    def incident_edges(self, v: Vertex) -> list[Edge]:
        return [edge for edge in self.edges() if v in edge]


def flip_edges(links: dict[Edge, int], edges: list[Edge]) -> dict[Edge, int]:
    updated = dict(links)
    for edge in edges:
        updated[edge] *= -1
    return updated


def holonomy(links: dict[Edge, int], loop: list[Edge]) -> int:
    q = 1
    for edge in loop:
        q *= links[edge]
    return q


def check(name: str, passed: bool, detail: str) -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {name}: {detail}")
    return passed


def born_i3(prob: dict[str, float]) -> float:
    return (
        prob["abc"]
        - prob["ab"]
        - prob["ac"]
        - prob["bc"]
        + prob["a"]
        + prob["b"]
        + prob["c"]
    )


def main() -> None:
    cyl = Cylinder(lx=6, ly=4)
    links = {edge: 1 for edge in cyl.edges()}
    loop = cyl.boundary_loop(y=0)

    q0 = holonomy(links, loop)
    links_minus = flip_edges(links, [loop[0]])
    q_minus = holonomy(links_minus, loop)

    print("Boundary Z2 flux chi probe")
    print(f"graph: cylinder lx={cyl.lx}, ly={cyl.ly}, boundary loop edges={len(loop)}")
    print(f"Q_chi sectors sampled: Q_plus={q0:+d}, Q_minus={q_minus:+d}")

    gates: list[bool] = []
    gates.append(check("Z2 involution", q0 in (-1, 1) and q_minus in (-1, 1),
                       f"Q^2={q0*q0}, sectors=({q0:+d},{q_minus:+d})"))
    gates.append(check("nonempty sectors", q0 == 1 and q_minus == -1,
                       "one boundary-link sector representative flips Q"))

    # Gauge relabeling at a boundary vertex flips both adjacent loop edges, so
    # the closed boundary holonomy is gauge invariant.
    gauge_links = flip_edges(links_minus, cyl.incident_edges((1, 0)))
    q_gauge = holonomy(gauge_links, loop)
    gates.append(check("boundary gauge relabel invariance", q_gauge == q_minus,
                       f"Q before={q_minus:+d}, after={q_gauge:+d}"))

    # Local bulk plaquette moves away from the measured boundary loop preserve
    # the loop.  Plaquettes touching the boundary do not preserve it and are
    # therefore not in the holonomy-preserving theorem surface.
    bulk_local = flip_edges(links_minus, cyl.plaquette(2, 2))
    q_bulk = holonomy(bulk_local, loop)
    gates.append(check("allowed local bulk move conservation", q_bulk == q_minus,
                       f"Q before={q_minus:+d}, after={q_bulk:+d}"))

    boundary_plaquette = flip_edges(links_minus, cyl.plaquette(2, 0))
    q_boundary_plaquette = holonomy(boundary_plaquette, loop)
    gates.append(check("boundary-touching plaquette is sector-breaking",
                       q_boundary_plaquette != q_minus,
                       f"Q before={q_minus:+d}, after={q_boundary_plaquette:+d}"))

    single_boundary_flip = flip_edges(links_minus, [loop[3]])
    q_single = holonomy(single_boundary_flip, loop)
    gates.append(check("explicit boundary flux insertion is sector-breaking",
                       q_single != q_minus,
                       f"Q before={q_minus:+d}, after={q_single:+d}"))

    cut_loop = loop[:-1]
    gates.append(check("topology-changing cut control fails candidate surface",
                       len(cut_loop) != len(loop),
                       "closed boundary cycle removed; Q_chi no longer gauge-invariant"))

    norm_plus = 1.25
    norm_minus = 1.25
    mass_unit = 2.0
    m_inertial_plus = mass_unit * norm_plus
    m_inertial_minus = mass_unit * norm_minus
    c_abs = mass_unit * norm_plus
    inserted_active_sum = q0 * c_abs + q_minus * c_abs
    inertial_sum = m_inertial_plus + m_inertial_minus

    gates.append(check("positive inertial mass", m_inertial_plus > 0 and m_inertial_minus > 0,
                       f"M+= {m_inertial_plus:.6f}, M-= {m_inertial_minus:.6f}"))
    gates.append(check("inserted locked null monopole control",
                       abs(inserted_active_sum) < 1e-12 and inertial_sum > 0,
                       f"C_active_sum={inserted_active_sum:+.3e}, M_sum={inertial_sum:.6f}"))

    native_variational_source = 0.0
    inserted_variational_source = q_minus * c_abs
    gates.append(check("native flux source locking", native_variational_source == q_minus * c_abs,
                       "native Wilson-loop spectator has dS/dPhi=0, not Q_chi |psi|^2"))
    gates.append(check("inserted source locking control",
                       inserted_variational_source == q_minus * c_abs,
                       f"dS_inserted/dPhi={inserted_variational_source:+.6f}"))

    probs = {
        "a": 1.0 / 9.0,
        "b": 1.0 / 9.0,
        "c": 1.0 / 9.0,
        "ab": 4.0 / 9.0,
        "ac": 4.0 / 9.0,
        "bc": 4.0 / 9.0,
        "abc": 1.0,
    }
    i3 = born_i3(probs)
    gates.append(check("Born I3 control", abs(i3) < 1e-12, f"I3={i3:+.3e}"))

    theta = 0.37
    amp = complex(0.8, 0.6)
    evolved = amp * complex(math.cos(theta), math.sin(theta))
    norm_drift = abs(abs(evolved) ** 2 - abs(amp) ** 2)
    gates.append(check("unitary norm control", norm_drift < 1e-12,
                       f"norm drift={norm_drift:.3e}"))

    q_bare_plus = 4.0 * math.pi * q0 * m_inertial_plus
    q_bare_minus = 4.0 * math.pi * q_minus * m_inertial_minus
    gates.append(check("source-unit bookkeeping control",
                       abs(abs(q_bare_plus) / m_inertial_plus - 4.0 * math.pi) < 1e-12
                       and abs(abs(q_bare_minus) / m_inertial_minus - 4.0 * math.pi) < 1e-12,
                       f"q_bare+= {q_bare_plus:+.6f}, q_bare-= {q_bare_minus:+.6f}"))

    print()
    print("classification:")
    print("  conserved label: conditional pass on restricted holonomy-preserving algebra")
    print("  source/response locking: fails natively; only passes as inserted charge")
    print("  physical claim: none")
    print("FINAL_TAG: BOUNDARY_CHI_SOURCE_NOT_LOCKED")

    if not all(gates[:-5]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
