# YT Schur-Complement K-Prime Sufficiency

```yaml
actual_current_surface_status: exact-support / Schur-complement K-prime sufficiency theorem; current rows absent
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_schur_complement_kprime_sufficiency.py`  
**Certificate:** `outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json`

## Purpose

The scalar denominator route keeps naming `K'(pole)` as a blocker.  This block
turns that target into a concrete sufficiency theorem for a mixed
source/orthogonal neutral scalar kernel.

Partition the neutral scalar kernel into a source-pole coordinate and an
orthogonal neutral block:

```text
K(x) = [[A(x), B(x)^T],
        [B(x), C(x)]]
```

After the orthogonal block is eliminated, the same-source denominator is the
Schur complement

```text
D_eff(x) = A(x) - B(x)^T C(x)^-1 B(x).
```

For one orthogonal direction this gives

```text
D_eff'(x_pole) =
  A'(x_pole)
  - 2 B(x_pole) B'(x_pole) / C(x_pole)
  + B(x_pole)^2 C'(x_pole) / C(x_pole)^2.
```

The matrix form is the same with `C^-1` and `C'` inserted in the usual
Schur/Feshbach derivative.

## Result

The runner verifies the formula against a finite-difference witness at an
exactly tuned pole:

```bash
python3 scripts/frontier_yt_schur_complement_kprime_sufficiency.py
# SUMMARY: PASS=12 FAIL=0
```

This is useful support because it replaces a vague "`K'(pole)` theorem" with
a future row contract: production or theorem rows must supply `A`, `B`, `C`
and their pole derivatives in a certified neutral scalar kernel partition.

## Boundary

This does not close PR #230.  The current surface does not provide those
same-surface Schur kernel rows, and the existing scalar denominator / K-prime
closure attempts remain open.

The support theorem also does not identify the source pole with the canonical
Higgs radial mode.  That still requires direct `O_H/C_sH/C_HH` pole rows,
same-source W/Z response rows with identity certificates, or an independent
canonical-Higgs/source-pole theorem.

This block does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`.
