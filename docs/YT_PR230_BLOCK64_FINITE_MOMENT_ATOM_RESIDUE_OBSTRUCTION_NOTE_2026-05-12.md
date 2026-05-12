# PR230 Block64 Finite-Moment Atom-Residue Obstruction

**Status:** no-go / exact negative boundary for the current PR230 surface:
finite source/Stieltjes moment prefixes do not fix the pole atom mass or scalar
LSZ residue without a separate strict determinacy or extremality certificate
**Runner:** `scripts/frontier_yt_pr230_block64_finite_moment_atom_residue_obstruction.py`
**Certificate:** `outputs/yt_pr230_block64_finite_moment_atom_residue_obstruction_2026-05-12.json`

## Claim

Block60 fixes the compact additive source-channel taste-singlet carrier,
Block61 blocks the shortcut from that carrier to `K'(pole)` or residue, and
Block62 blocks compact-source support as K-prime/residue authority.  This
block tests the next scalar shortcut:

```text
finite source/Stieltjes moments + fixed source carrier
=> fixed pole atom mass / scalar LSZ residue
```

That shortcut is not valid on the current PR230 surface.  Finite moment data
are not pole-residue authority unless an additional accepted certificate proves
determinacy, an extremal localizing condition, a direct pole-row residue
measurement, or a microscopic denominator derivative theorem.

## Executable Counterfamily

The runner checks two positive measures on `[0,1]` with the same finite moment
prefix `m_0,m_1,m_2` but different atom mass at the candidate pole `x=0`.

```text
mu_A = (1/6) delta_0 + (2/3) delta_{1/2} + (1/6) delta_1
mu_B = (1/4) delta_0 + (3/4) delta_{2/3}
```

Both have

```text
m_0 = 1,  m_1 = 1/2,  m_2 = 1/3.
```

The candidate-pole atom differs:

```text
mu_A({0}) = 1/6,  mu_B({0}) = 1/4.
```

Thus a finite positive moment prefix can agree while the atom mass, and hence a
pole-residue proxy, changes.  Current finite FH/LSZ moment, Pade, and
finite-shell data cannot be promoted to scalar LSZ residue authority without
the missing strict certificate.

## Boundary

This does not weaken the Block58 finite-volume spectral support or the Block60
source-carrier support.  It only blocks using finite moment agreement or
finite-shell Stieltjes checks as a residue theorem.

A positive scalar route now has to supply one of the missing objects directly:

- an exact moment or localizing-matrix extremality/determinacy certificate;
- a direct same-surface pole-row residue measurement with covariance;
- a microscopic `K'(pole)` theorem;
- threshold/FVIR/contact authority;
- canonical `O_H`/source-overlap authority or an equivalent physical W/Z
  response bridge.

## Parent Surface

- [Block58 compact source spectral support](YT_PR230_BLOCK58_COMPACT_SOURCE_SPECTRAL_SUPPORT_GATE_NOTE_2026-05-12.md)
- [Block59 source spectral pole-promotion obstruction](YT_PR230_BLOCK59_SOURCE_SPECTRAL_POLE_PROMOTION_OBSTRUCTION_NOTE_2026-05-12.md)
- [Block60 compact source taste-singlet carrier](YT_PR230_BLOCK60_COMPACT_SOURCE_TASTE_SINGLET_CARRIER_GATE_NOTE_2026-05-12.md)
- [Block61 post-carrier K-prime obstruction](YT_PR230_BLOCK61_POST_CARRIER_KPRIME_OBSTRUCTION_NOTE_2026-05-12.md)
- [Block62 compact-source K-prime identifiability obstruction](YT_PR230_BLOCK62_COMPACT_SOURCE_KPRIME_IDENTIFIABILITY_OBSTRUCTION_NOTE_2026-05-12.md)
- [FH-LSZ Stieltjes moment certificate gate](YT_FH_LSZ_STIELTJES_MOMENT_CERTIFICATE_GATE_NOTE_2026-05-05.md)
- [FH-LSZ Pade-Stieltjes bounds gate](YT_FH_LSZ_PADE_STIELTJES_BOUNDS_GATE_NOTE_2026-05-05.md)
- [Scalar-LSZ Carleman/Tauberian attempt](YT_PR230_SCALAR_LSZ_CARLEMAN_TAUBERIAN_DETERMINACY_ATTEMPT_NOTE_2026-05-05.md)
- [FH-LSZ finite-shell identifiability no-go](YT_FH_LSZ_FINITE_SHELL_IDENTIFIABILITY_NO_GO_NOTE_2026-05-02.md)

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not treat finite moment prefixes, Pade fits, finite-shell pole fits, or
source-carrier normalization as scalar LSZ residue authority.

It does not use `H_unit`, `yt_ward_identity`, observed top/Yukawa values,
`alpha_LM`, plaquette, `u0`, `kappa_s=1`, `c2=1`, or `Z_match=1`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block64_finite_moment_atom_residue_obstruction.py
python3 scripts/frontier_yt_pr230_block64_finite_moment_atom_residue_obstruction.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=190 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=399 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=105 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=319 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=73 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
# OK: no errors; seeded the Block64 note; invalidate_stale_audits invalidated=0

python3 docs/audit/scripts/audit_lint.py --strict
# OK: no errors; 5 existing warnings
```
