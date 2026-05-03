# `y_t` Vertex-Power Theorem: Why `alpha_s(v) = alpha_bare / u_0^2`

**Date:** 2026-04-15
**Status:** closed subderivation on an open lane; zero-input structural support
**Primary runner:** `scripts/frontier_vertex_power.py`

## Authority Role

This note provides the operator-level support for the current coupling map used
by the bounded zero-input `y_t` / `alpha_s` package.

Use it together with:

- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md)
- `YT_ZERO_IMPORT_AUTHORITY_NOTE.md` (sibling/companion authority note;
  cross-reference only — not a one-hop dep of this derivation)

It does not by itself close the renormalized `y_t` lane.

## Safe Statement

On the current lattice operator surface, the gauge vertex carries two powers of
the mean-field link dressing. The current package therefore uses

`alpha_s(v) = alpha_bare / u_0^2`

as the operator-level coupling map behind the strongest zero-input
`alpha_s(M_Z)` and `m_t` routes.

## Core Derivation

1. the hierarchy observable uses one gauge link per hopping term and therefore
   carries one power of `u_0`
2. the gauge vacuum-polarization channel contains two vertex insertions
3. each vertex insertion contributes one gauge-link dressing
4. the current operator count is therefore `n_link = 2`
5. on the current vacuum-centered coupling map,
   `alpha_eff = alpha_bare / u_0^{n_link}`
6. so the gauge-coupling route uses `alpha_s(v) = alpha_bare / u_0^2`

## Package Boundary

This theorem closes the operator-counting step. It does not close the whole
low-energy package because the full lane still includes:

- the `v` endpoint selection theorem
- the bridge-conditioned EFT transfer
- the bounded zero-input top-mass route
- the import-allowed crossover companion

## Validation Snapshot

`frontier_vertex_power.py` is the current support runner for this note.

The current package uses this theorem as support for:

- `alpha_s(v) = 0.1033`
- `alpha_s(M_Z) = 0.1181`
- the bounded zero-input top-mass route
