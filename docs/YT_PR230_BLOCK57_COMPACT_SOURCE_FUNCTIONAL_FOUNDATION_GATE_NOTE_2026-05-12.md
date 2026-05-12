# PR230 Block57 Compact Source-Functional Foundation Gate

**Status:** exact-support / compact finite-volume scalar-source foundation,
with pole/FVIR and canonical-Higgs roots still open  
**Runner:** `scripts/frontier_yt_pr230_block57_compact_source_functional_foundation_gate.py`  
**Certificate:** `outputs/yt_pr230_block57_compact_source_functional_foundation_gate_2026-05-12.json`

## Claim

Block56 cut the current scalar-pole/FVIR shortcut stack.  This block audits a
subtle point in that cut: the existing zero-mode, flat-toron, and contact
negative results are correct, but their scope is narrower than a global no-go
against the exact compact Cl(3)/Z3 source functional.

Load-bearing parent surfaces:

- [Block56 scalar-pole/FVIR root cut](YT_PR230_BLOCK56_SCALAR_POLE_FVIR_ROOT_CUT_GATE_NOTE_2026-05-12.md)
- [Scalar zero-mode limit-order theorem](YT_SCALAR_ZERO_MODE_LIMIT_ORDER_THEOREM_NOTE_2026-05-01.md)
- [Flat-toron scalar-denominator obstruction](YT_FLAT_TORON_SCALAR_DENOMINATOR_OBSTRUCTION_NOTE_2026-05-01.md)
- [FH/LSZ contact-subtraction identifiability boundary](YT_FH_LSZ_CONTACT_SUBTRACTION_IDENTIFIABILITY_NOTE_2026-05-05.md)
- [Legendre source-pole operator construction](YT_LEGENDRE_SOURCE_POLE_OPERATOR_CONSTRUCTION_NOTE_2026-05-03.md)
- [Source-functional LSZ identifiability theorem](YT_SOURCE_FUNCTIONAL_LSZ_IDENTIFIABILITY_THEOREM_NOTE_2026-05-03.md)

The current exact support is:

```text
finite compact Cl(3)/Z3 source path integral
+ specified additive scalar source in the staggered determinant
=> finite-volume bare source curvature/contact scheme exists
```

The exact compact functional integrates flat toron sectors.  It does not
select the trivial toron.  Therefore the flat-toron obstruction blocks the
trivial-sector shortcut, not the existence of the compact finite-volume source
functional.

## No-Go Scope Audit

The runner records four applicability cuts:

- The scalar zero-mode limit-order theorem applies to the finite
  Wilson-exchange ladder with a noncompact IR regulator; it is not a proof
  that the compact Haar path integral is undefined.
- The flat-toron obstruction applies to selecting the trivial Cartan toron from
  an action-degenerate family; it is not an obstruction to integrating flat
  torons in the compact path integral.
- The contact-subtraction identifiability obstruction applies to choosing a
  continuum/local contact subtraction from finite rows or monotonicity repair;
  it is not an obstruction to defining the bare finite-volume source curvature
  by functional derivatives of the specified lattice source action.
- The source-functional LSZ identifiability theorem applies to source-only
  attempts to identify the source pole with canonical `O_H`; it does not block
  constructing a source-pole operator once an isolated source pole is supplied.

## What This Moves

This block reopens the scalar route in a narrower and more physical form:

```text
exact compact finite-volume source functional
-> thermodynamic transfer/spectral theorem
-> isolated scalar source pole and residue
-> canonical O_H/source-overlap or physical response bridge
```

The current blocker is no longer "the scalar source functional is undefined."
It is the harder retained-grade theorem: spectral/transfer authority,
isolated-pole residue, FV/IR/toron limiting order, and canonical-Higgs identity
or equivalent physical bypass.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not treat finite-volume analyticity as pole/FVIR authority.  It does
not select the trivial toron, does not choose a contact subtraction from finite
rows, and does not identify `O_s` or the LSZ-normalized source-pole operator
with canonical `O_H`.

It does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed top/Yukawa
values, `alpha_LM`, plaquette/`u0`, `kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block57_compact_source_functional_foundation_gate.py
python3 scripts/frontier_yt_pr230_block57_compact_source_functional_foundation_gate.py
# SUMMARY: PASS=14 FAIL=0
```
