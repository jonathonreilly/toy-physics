# PR230 Derived-Bridge Rank-One Closure Attempt

Date: 2026-05-05

Status: exact negative boundary / derived rank-one bridge not closed on current
PR230 surface.

Runner:
`scripts/frontier_yt_pr230_derived_bridge_rank_one_closure_attempt.py`

Certificate:
`outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json`

## Target

The derivation-preferred bridge is:

```text
O_s / O_sp source pole -> canonical Higgs radial readout O_H
```

without measuring `C_sH/C_HH` or same-source W/Z rows.  The only plausible
way for source-only data to become sufficient is a microscopic theorem that
the neutral scalar response sector has a single primitive positive component.
Then Perron-Frobenius/Krein-Rutman uniqueness plus isolated-pole factorization
could force the lowest neutral pole residue to be rank one.

## Positive Contract

A future positive certificate must provide all of:

- a same-surface PR230 `Cl(3)/Z^3` neutral scalar basis;
- a nonnegative neutral transfer matrix on a certified cone;
- strong connectivity of its positive-entry graph;
- a finite positive primitive power;
- an isolated lowest neutral scalar pole with FV/IR/threshold authority;
- positive source-pole overlap;
- canonical-Higgs authority, or a theorem that bypasses it by proving all
  neutral scalar probes couple to the unique pole;
- orthogonal neutral null control;
- firewall rejection of `H_unit`, Ward authority, observed targets,
  `alpha_LM`/plaquette/`u0`, and unit-overlap shortcuts.

## Result

The current PR230 surface does not satisfy the contract.

What exists:

- a conditional Perron/rank-one support theorem;
- a primitive-cone certificate gate;
- finite witnesses showing how a future primitive matrix would close the
  rank-one part;
- no-go certificates showing source-only `C_ss`, reflection positivity,
  gauge Perron support, Burnside theorem names, commutant labels, and
  invariant-ring uniqueness do not force the bridge.

What is absent:

- strict primitive-cone certificate;
- same-surface off-diagonal neutral generator;
- neutral irreducibility theorem;
- canonical `O_H` certificate;
- `C_sH/C_HH` rows.

## Positivity Boundary

Reflection positivity, determinant positivity, and positive Euclidean measure
are not enough.  They give positivity preservation.  The bridge needs
positivity improvement/irreducibility in the neutral scalar response sector.

A reducible positive transfer matrix,

```text
[[0.91, 0.00],
 [0.00, 0.88]]
```

is nonnegative but not strongly connected and has no strictly positive
primitive power.  It can preserve all source-only rows while leaving an
orthogonal neutral scalar direction invisible to `C_ss`.

## Non-Claims

This note does not claim retained or proposed-retained top-Yukawa closure.  It
does not define `y_t_bare`, does not identify `O_sp` with `O_H`, does not treat
positivity preservation as positivity improvement, and does not use `H_unit`,
`yt_ward_identity`, observed values, `alpha_LM`, plaquette, `u0`, `R_conn`, or
unit-overlap shortcuts.

## Next Action

Make the derived bridge positive by deriving one real current-surface neutral
off-diagonal generator or primitive-cone certificate.  Otherwise return to the
measured bridge: `O_H/C_sH/C_HH` or same-source W/Z response rows.

## Verification

```bash
python3 scripts/frontier_yt_pr230_derived_bridge_rank_one_closure_attempt.py
# SUMMARY: PASS=17 FAIL=0
```
