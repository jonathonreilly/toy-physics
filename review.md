# Codex Review: `claude/relaxed-wu-a56584`

**Date:** 2026-04-26
**Branch tip reviewed:** `2d5671b22866b52ffcb0b1163aaa6b56fdb0b937`
**Verdict:** Not ready to land as retained unconditional Planck Target 3 closure.

The new runners pass and the branch contains useful object-level algebra around
the coframe carrier, Schur spectra, and Planck source normalization. The blocker
is still claim strength: the branch assigns or re-labels the physical
boundary/source identification instead of deriving it from retained authority.

Verified:

```bash
python3 scripts/frontier_planck_gravity_boundary_coframe_identification.py
# PASS=40, FAIL=0

python3 scripts/frontier_planck_target3_cubic_bivector_schur_source_principle.py
# PASS=42, FAIL=0

python3 scripts/frontier_planck_target3_synthesis_unconditional_closure.py
# PASS=35, FAIL=0

python3 scripts/frontier_planck_target3_forced_coframe_response.py
# PASS=54, FAIL=0

python3 scripts/frontier_planck_target3_gauss_flux_first_order_carrier.py
# PASS=41, FAIL=0

python3 scripts/frontier_planck_target3_schur_source_coupling_identity.py
# PASS=34, FAIL=0

python3 -m py_compile \
  scripts/frontier_planck_gravity_boundary_coframe_identification.py \
  scripts/frontier_planck_target3_cubic_bivector_schur_source_principle.py \
  scripts/frontier_planck_target3_synthesis_unconditional_closure.py \
  scripts/frontier_planck_target3_forced_coframe_response.py \
  scripts/frontier_planck_target3_gauss_flux_first_order_carrier.py \
  scripts/frontier_planck_target3_schur_source_coupling_identity.py

git diff --check origin/main...HEAD
```

## Findings

### [P1] Boundary theorem defines the carrier it needs to derive

File: `docs/PLANCK_GRAVITY_BOUNDARY_COFRAME_CARRIER_IDENTIFICATION_THEOREM_NOTE_2026-04-26.md`
Lines: 93-108

The proof moves from the scalar primitive-cell variation of
`S_grav = kL(1-phi)` to the operator assignment
`B_grav = sum_a k P_{a} = k P_A`. That assignment is exactly the disputed
coframe carrier identification. The scalar action gives a per-axis weight, but
does not canonically lift that weight to the HW=1 projector or exclude the
Hodge-dual/boundary-density reading. This verifies that `P_A` works after
choosing it, not that retained gravity uniquely forces it.

### [P1] Runner constructs the disputed carrier by assignment

File: `scripts/frontier_planck_gravity_boundary_coframe_identification.py`
Lines: 154-196

`part_a_extract_B_grav` narrates the gravity-action variation, then directly
builds `B_grav` as the sum of the four one-axis projectors. The subsequent
projector/rank checks only verify properties of the constructed `P_A`; they do
not certify that this operator is extracted uniquely from the retained gravity
action or that competing carrier conventions are excluded.

### [P1] Conditional source-unit theorem is promoted to retained closure input

File: `docs/PLANCK_GRAVITY_BOUNDARY_COFRAME_CARRIER_IDENTIFICATION_THEOREM_NOTE_2026-04-26.md`
Lines: 63-72

The import ledger treats
`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25` as retained
for the unconditional Planck pin, but that source note explicitly says it is a
retained support theorem on the conditional Planck packet and not a standalone
minimal-stack closure. Using it as a retained source-unit closure input
reintroduces the same conditional carrier premise under a new ledger label.

### [P1] Schur-to-source coupling remains an identification step

File: `docs/PLANCK_TARGET3_SYNTHESIS_UNCONDITIONAL_CLOSURE_THEOREM_NOTE_2026-04-26.md`
Lines: 297-334

Steps 3-5 combine a Schur-Feshbach boundary Green operator with the source-unit
normalization and then identify the Schur trace with the physical gravitational
source coupling per cell. That equality is the load-bearing physical source
principle the prior review asked to derive; the text still asserts the
identification after building the Schur object rather than deriving it from an
accepted retained boundary-source theorem.

### [P1] S4 uniqueness assumes the first-order source sector

File: `docs/PLANCK_TARGET3_SYNTHESIS_UNCONDITIONAL_CLOSURE_THEOREM_NOTE_2026-04-26.md`
Lines: 113-123

The S4 argument uniquely selects `H_first` only after restricting to grade-1,
first-order Clifford generators. That does not by itself select the physical
boundary carrier, because the Hodge-dual `P_3` packet is still an S4-symmetric
carrier candidate and the branch's own cubic-bivector note reports that Schur
data does not distinguish `P_1` from `P_3`. This is a conditional
first-order-source result, not retained source-selector closure.

### [P1] Synthesis runner solves after assuming source equality

File: `scripts/frontier_planck_target3_synthesis_unconditional_closure.py`
Lines: 424-460

The runner sets the Schur trace value to `1`, then solves
`4 c_cell G_Newton,lat = 1` and marks the source-coupling step as passed. That
is algebraically consistent, but it does not compute or certify the missing
physical identification between the Schur trace and gravitational source
coupling; the disputed bridge is still encoded as the premise of the solve.

## Recommended Treatment

Keep this branch scoped as a Planck consequence/control packet and
boundary-source no-go/control surface, not retained unconditional Target 3
closure.

To promote it, a retained theorem still needs to:

- derive the gravitational boundary/action carrier from retained source content
  rather than assigning `B_grav = P_A`;
- derive the physical coupling normalization
  `Tr(chi_eta rho Phi)=4 c_cell G_Newton,lat` from accepted retained
  boundary-source content;
- select `P_1` over the Hodge-dual `P_3`, or prove they are physically
  equivalent under a retained source principle;
- align status ledgers and package surfaces so support-theorem inputs are not
  presented as standalone retained closure authorities.
