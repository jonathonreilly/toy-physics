# Canonical Mass Coupling Linearity - Bounded Support

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status:** source-note proposal only; independent audit controls any
downstream effective status.
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/cl3_closure_c_bb_2026_05_10_cBB.py`](../scripts/cl3_closure_c_bb_2026_05_10_cBB.py)
**Primary runner cache:** [`logs/runner-cache/cl3_closure_c_bb_2026_05_10_cBB.txt`](../logs/runner-cache/cl3_closure_c_bb_2026_05_10_cBB.txt)

## Claim Scope

This note proves a bounded support lemma for the gravity-source chain.
Assume:

1. the canonical staggered-Dirac carrier has a scalar mass term
   `S_m = m sum_x n_x`, with local number-density operator `n_x`, as in
   [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md);
2. the gravity-source readout uses the position-density Born map
   `rho_grav(x) = <n_x>_rho`, as in
   [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md).

Then the mass contribution to the local source is exactly

```text
rho_mass(x; m) = m rho_grav(x).
```

The result is linear in the mass parameter, homogeneous under
`m -> alpha m`, and additive over independent species. This is a
bounded theorem because the staggered-Dirac carrier and the Born/source
identification remain separate audited dependencies.

## Proof

The assumed canonical mass term is

```text
S_m = m sum_x n_x.
```

For any state `rho`, the local expectation of the mass term is

```text
<m n_x>_rho = m <n_x>_rho.
```

Using the supplied Born/source map `<n_x>_rho = rho_grav(x)` gives

```text
rho_mass(x; m) = m rho_grav(x).
```

The derivative with respect to `m` is `rho_grav(x)`, and all higher
derivatives vanish. For a rescaling `m -> alpha m`,

```text
rho_mass(x; alpha m) = alpha rho_mass(x; m).
```

For independent species with masses `m_i` and density profiles
`rho_i(x)`, the source is the linear superposition

```text
rho_mass(x) = sum_i m_i rho_i(x).
```

If all species share the same normalized profile, this reduces to
`M rho_grav(x)` with `M = sum_i m_i`. If the profiles differ, the
correct statement is the displayed sum; this note does not collapse
distinct spatial profiles into one scalar mass times one common density.

## What This Supports

- The canonical mass term supplies a bounded support reason for using a
  mass-linear source once the Born/source density has already been
  supplied.
- Nonlinear replacements such as `m^2 rho_grav`, `sqrt(m) rho_grav`,
  `exp(m) rho_grav`, or `(1/m) rho_grav` are not the canonical mass
  term and fail the simple homogeneity/additivity checks of this lemma.

## Explicit Non-Claims

- This does not derive the Born/source identification itself.
- This does not derive the staggered-Dirac carrier from the physical
  `Cl(3)` local algebra on the `Z^3` spatial substrate.
- This does not close `GRAVITY_CLEAN_DERIVATION_NOTE.md`, gnewtonG3, or
  W-GNewton-Valley by itself.
- This does not add a repo-wide axiom or a new foundational premise.
- This does not rule out every possible noncanonical theory with extra
  interaction terms; it says the canonical mass term used here is
  mass-linear.

## Verification

```bash
python3 scripts/cl3_closure_c_bb_2026_05_10_cBB.py
```

The runner verifies exact symbolic affine dependence on `m`, local
source linearity, homogeneity, species additivity, and failure of the
listed nonlinear replacements to satisfy the canonical linear source
gate.

## Independent Audit Handoff

Audit status is set only by the independent audit lane. Expected row:

```text
claim_type: bounded_theorem
declared_one_hop_deps:
  - axiom_first_lattice_noether_theorem_note_2026-04-29
  - g_newton_born_as_source_positive_theorem_note_2026-05-10_gnewtong2
audit_status: unaudited
```
