"""
Geometry of the 2x2 spatial torus for full SU(3) spin-network ED.

Notation
--------
Sites: (i, j) ∈ {0,1} × {0,1}, periodic identification.
Links:
    x-link `x_ij`: from site (i,j) to (i+1, j)  (mod 2 in i)
    y-link `y_ij`: from site (i,j) to (i, j+1)  (mod 2 in j)
Eight links total: x_00, x_10, x_01, x_11, y_00, y_10, y_01, y_11.

Plaquettes (four):
    P_ij has corners (i,j), (i+1,j), (i+1,j+1), (i,j+1).
    Boundary path (counterclockwise):
        x_ij  (forward, (i,j)→(i+1,j))
        y_{i+1,j}  (forward, (i+1,j)→(i+1,j+1))
        x_{i,j+1}^{-1}  (backward, (i+1,j+1)→(i,j+1))
        y_{i,j}^{-1}  (backward, (i,j+1)→(i,j))

Vertices (four), each 4-valent with two x-edges (incoming + outgoing) and
two y-edges (incoming + outgoing):
    Vertex (i, j) has incident edges:
        x_ij           (outgoing, from (i,j))
        x_{i-1,j}      (incoming, ending at (i,j))
        y_ij           (outgoing, from (i,j))
        y_{i,j-1}      (incoming, ending at (i,j))

For each link e in irrep λ_e, an "outgoing" leg at site (i,j) carries
V_{λ_e} (the source side of D^{λ_e}_{ab}(U_e)) and an "incoming" leg
carries V*_{λ_e} (the sink side).

At each vertex, the incident legs have:
    x_ij outgoing       → V_{λ_{x_ij}}                     [source-end of x_ij]
    x_{i-1,j} incoming  → V*_{λ_{x_{i-1,j}}}               [sink-end of x_{i-1,j}]
    y_ij outgoing       → V_{λ_{y_ij}}                     [source-end of y_ij]
    y_{i,j-1} incoming  → V*_{λ_{y_{i,j-1}}}               [sink-end of y_{i,j-1}]

Gauge invariance requires the simultaneous SU(3) action on these four
spaces to fix a vector — i.e., we need the trivial-rep multiplicity in
    V_{λ_x_out} ⊗ V*_{λ_x_in} ⊗ V_{λ_y_out} ⊗ V*_{λ_y_in}
which equals the multiplicity of trivial in
    λ_x_out ⊗ λ̄_x_in ⊗ λ_y_out ⊗ λ̄_y_in.
For SU(3), conjugate of (p,q) is (q,p).
"""

from __future__ import annotations


def conjugate(lam):
    """Conjugate of SU(3) irrep (p,q) is (q,p)."""
    return (lam[1], lam[0])


# The 8 links and 4 plaquettes
LINK_KEYS = ['x_00', 'x_10', 'x_01', 'x_11', 'y_00', 'y_10', 'y_01', 'y_11']
LINK_INDEX = {k: i for i, k in enumerate(LINK_KEYS)}

# Plaquette boundary edges with direction (+1 forward, -1 backward).
# P_ij = x_ij · y_{i+1,j} · x_{i,j+1}^{-1} · y_{i,j}^{-1}
# In Tr Up = Tr(U_x_ij · U_y_{i+1,j} · U_x_{i,j+1}^{-1} · U_y_{i,j}^{-1})
PLAQUETTE_BOUNDARY = {}
for i in [0, 1]:
    for j in [0, 1]:
        ip = (i + 1) % 2
        jp = (j + 1) % 2
        PLAQUETTE_BOUNDARY[f'P_{i}{j}'] = [
            (f'x_{i}{j}', +1),
            (f'y_{ip}{j}', +1),
            (f'x_{i}{jp}', -1),
            (f'y_{i}{j}', -1),
        ]

PLAQUETTE_KEYS = list(PLAQUETTE_BOUNDARY.keys())

# Vertex incident edges with direction (+1 outgoing from vertex, -1 incoming):
# Vertex (i,j) → outgoing x_ij, incoming x_{i-1,j}, outgoing y_ij, incoming y_{i,j-1}
VERTEX_KEYS = [(i, j) for i in [0, 1] for j in [0, 1]]
VERTEX_INCIDENT = {}
for (i, j) in VERTEX_KEYS:
    im = (i - 1) % 2
    jm = (j - 1) % 2
    VERTEX_INCIDENT[(i, j)] = [
        (f'x_{i}{j}', +1),       # outgoing
        (f'x_{im}{j}', -1),      # incoming
        (f'y_{i}{j}', +1),       # outgoing
        (f'y_{i}{jm}', -1),      # incoming
    ]


def vertex_irreps_for_config(link_irreps: dict, vertex):
    """For a vertex (i,j) and a config link_irreps[link_key] = (p,q),
    return list of (p,q) for the 4 incident legs (with conjugation
    applied for incoming edges)."""
    out = []
    for link, dirn in VERTEX_INCIDENT[vertex]:
        lam = link_irreps[link]
        if dirn == +1:
            out.append(lam)
        else:
            out.append(conjugate(lam))
    return out


def plaquette_links_directed(plaq):
    """Return the (link_key, direction) list for plaquette boundary."""
    return PLAQUETTE_BOUNDARY[plaq]


# A "link config" is a tuple of 8 (p,q) irrep labels in LINK_KEYS order.
def encode_link_config(link_irreps):
    return tuple(link_irreps[k] for k in LINK_KEYS)


def decode_link_config(config):
    return {k: c for k, c in zip(LINK_KEYS, config)}


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("LINK_KEYS:", LINK_KEYS)
    print()
    print("PLAQUETTE_BOUNDARY:")
    for p, b in PLAQUETTE_BOUNDARY.items():
        print(f"  {p}: {b}")
    print()
    print("VERTEX_INCIDENT:")
    for v, incs in VERTEX_INCIDENT.items():
        print(f"  vertex {v}: {incs}")

    # Self-consistency: each link should appear in exactly 2 plaquettes
    # and each link should appear in exactly 2 vertex-incidence lists
    # (once outgoing at source vertex, once incoming at sink vertex).
    link_in_plaq = {k: 0 for k in LINK_KEYS}
    for p, b in PLAQUETTE_BOUNDARY.items():
        for link, _ in b:
            link_in_plaq[link] += 1
    for k, c in link_in_plaq.items():
        assert c == 2, f"link {k} appears in {c} plaquettes, expected 2"

    link_in_vert = {k: 0 for k in LINK_KEYS}
    for v, incs in VERTEX_INCIDENT.items():
        for link, dirn in incs:
            link_in_vert[link] += 1
    for k, c in link_in_vert.items():
        assert c == 2, f"link {k} appears in {c} vertex incidence lists, expected 2"

    # Each link should appear once outgoing and once incoming
    for k in LINK_KEYS:
        outs = sum(1 for v, incs in VERTEX_INCIDENT.items()
                    for link, d in incs if link == k and d == +1)
        ins = sum(1 for v, incs in VERTEX_INCIDENT.items()
                    for link, d in incs if link == k and d == -1)
        assert outs == 1, f"link {k} outs={outs}"
        assert ins == 1, f"link {k} ins={ins}"

    print("\nGeometry self-consistency: OK")
