# Site-Phase / Cube-Shift Intertwiner Note

**Date:** 2026-04-17
**Status:** exact support theorem on the full taste-cube / BZ-corner bridge
**Script:** `scripts/frontier_site_phase_cube_shift_intertwiner.py`
**Authority role:** canonical support note for moving exact statements between
the abstract taste cube `C^8` and the BZ-corner subspace of even periodic
`Z_L^3`

## Safe statement

Let `C^8 = (C^2)^{\otimes 3}` carry the cube-shifts `S_mu`, and let the even periodic
lattice `Z_L^3` carry the BZ-corner states `|X_alpha>` with
`alpha in {0,1}^3`. If `P_mu` denotes multiplication by `(-1)^(x_mu)` on
lattice wavefunctions and `Phi|alpha> = |X_alpha>`, then:

- `P_mu |X_alpha> = |X_(alpha xor e_mu)>`
- `Phi^dagger P_mu Phi = S_mu`
- the joint `P_mu` eigensystem on the BZ-corner subspace is the
  Hadamard / `Z_2^3` character transform of the computational basis

This is an exact bridge theorem. It does not by itself identify the retained
`hw=1` triplet with physical generations. Its safe role is narrower: the full
taste-cube operator algebra and the lattice BZ-corner subspace are exactly
intertwined on this restricted support.

## Classical results applied

- Fourier duality between multiplication and shift on a finite abelian group
- standard intertwiner / equivariant-linear-map language

## Framework-specific step

- identification of the exact BZ-corner basis `|X_alpha>` with the
  computational basis `|alpha>`
- restriction to the eight-corner lattice support used by the current
  taste-cube bookkeeping

## Why it matters on `main`

This is the full `C^8` companion to the retained `hw=1` observable algebra
already used in
`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`.
It is the canonical route for lifting full taste-cube statements back to
lattice BZ-corner statements without inventing a second authority surface.

## Verification

Run:

```bash
python3 scripts/frontier_site_phase_cube_shift_intertwiner.py
```

The runner checks the bit-flip law `P_mu |X_alpha> = |X_(alpha xor e_mu)>`,
the pulled-back operators `Phi^dagger P_mu Phi = S_mu`, and the transfer of
the joint eigensystem on the BZ-corner subspace.
