# Gauge-Vacuum Plaquette First-Sector Zero-Extension Factorized-Class Theorem

**Date:** 2026-04-19
**Status:** exact constructive existence theorem on the plaquette/Wilson first-sector reopening; the proposed_retained first-sector environment packet already admits one explicit full extension inside the canonical Wilson factorized class
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_2026_04_19.py`

## Question

Once the retained first-sector packet is known, is existence of a realization
inside the canonical Wilson factorized class still open?

## Answer

No.

Take the retained normalized packet

`rho_ret = (1, 0.267139565315, 0.267139565315, 0)`

on the first-symmetric weights

`(0,0), (1,0), (0,1), (1,1)`.

Extend it by zero to all higher weights on the dominant-weight box:

- keep the retained entries above,
- set `rho_(p,q) = 0` for every other weight.

This yields one explicit full nonnegative conjugation-symmetric coefficient
sequence `rho_ext`.

Then the factorized Wilson-gauge operator

`T_ext = exp(3 J) D_6^loc diag(rho_ext) exp(3 J)`

is explicitly:

- self-adjoint,
- conjugation-symmetric,
- positive semidefinite on the truncated dominant-weight box.

And on the retained first-symmetric sector it still reconstructs the completed
three-sample triple exactly.

So existence of a factorized-class extension consistent with the retained
first-sector packet is no longer open either.

What remains open is more specific:

> the actual framework-point Wilson environment packet, not just existence of
> some packet in the factorized class.

## Commands run

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_zero_extension_factorized_class_theorem_2026_04_19.py
```

Expected summary:

- `PASS=6 FAIL=0`
